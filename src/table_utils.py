"""Table helper utilities for cleaning and expanding DataFrame table exports.

Provides `split_and_explode` which splits multi-value cells and expands rows
either as the Cartesian product or pairwise (zip) alignment.
"""
from __future__ import annotations

import re
from typing import Iterable, List, Sequence

import pandas as pd

DEFAULT_DELIMITER_RE = r"\s*(?:;|,|/|\n)\s*"


def _to_list(val, pattern: str, smart: bool = False) -> List[str]:
    """Convert a cell value to a list of sub-values.

    If ``smart`` is True, attempt to extract number+unit and numeric tokens as
    atomic values (e.g., "177 s 167 s" -> ["177 s", "167 s"]). Otherwise
    split on the provided regex pattern.
    """
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    s = str(val)
    s = s.strip()
    if s == "":
        return []

    # If smart, try to find number+unit groups first, then numeric groups,
    # otherwise fall back to splitting on the delimiter pattern.
    if smart:
        # Match number with optional decimal and an optional unit following it
        # Use word boundaries to avoid matching digits embedded in tokens such as
        # 'M3 Max' (we don't want to split "Apple M3 Max (16 cores)").
        number_unit_re = re.compile(r"\b\d+(?:\.\d+)?\s*[A-Za-z%/µ°]+\b")
        matches = number_unit_re.findall(s)
        if len(matches) > 1:
            return [m.strip() for m in matches]

        # Match floats/ints (useful for columns like Pages/s)
        number_re = re.compile(r"\b\d+(?:\.\d+)?\b")
        matches = number_re.findall(s)
        if len(matches) > 1:
            return [m.strip() for m in matches]

        # As a last resort split on runs of two or more spaces (visual separation)
        if "  " in s:
            parts = [p.strip() for p in re.split(r"\s{2,}", s) if p.strip()]
            if len(parts) > 1:
                return parts

    parts = [p.strip() for p in re.split(pattern, s) if p.strip()]
    return parts


def split_and_explode(
    df: pd.DataFrame,
    cols: Sequence[str],
    delimiter_regex: str = DEFAULT_DELIMITER_RE,
    mode: str = "cartesian",
    smart: bool = False,
) -> pd.DataFrame:
    """Split multi-value columns and expand rows.

    Args:
        df: Input DataFrame.
        cols: Columns to split and expand. Columns not present raise KeyError.
        delimiter_regex: Regular expression used to split cell strings. Defaults
            to matching semicolons, commas, slashes or newlines.
        mode: One of ``"cartesian"`` or ``"pairwise"``. ``cartesian`` explodes
            each column sequentially producing the cartesian product of values.
            ``pairwise`` requires each column to contain the same number of
            split values for a row and zips them together (i.e., aligns by
            position).

    Returns:
        A new DataFrame with expanded rows and the same columns as ``df``.

    Raises:
        ValueError: If ``mode=='pairwise'`` and some rows contain unequal
            numbers of items across the specified columns.
    """
    if mode not in {"cartesian", "pairwise"}:
        raise ValueError("mode must be 'cartesian' or 'pairwise'")

    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f"Columns not found in DataFrame: {missing}")

    df = df.copy()

    # Convert target columns to lists
    for c in cols:
        df[c] = df[c].apply(lambda v: _to_list(v, delimiter_regex, smart=smart))

    if mode == "cartesian":
        # Explode sequentially to get cartesian product
        for c in cols:
            df = df.explode(c, ignore_index=True)
        df = df.reset_index(drop=True)
        return df

    # pairwise mode
    def _zip_row(row):
        lists = [_to_list(row[c], delimiter_regex, smart=smart) if not isinstance(row[c], list) else row[c] for c in cols]
        lengths = [len(l) for l in lists]
        if len(set(lengths)) > 1:
            raise ValueError(f"Unequal numbers of items across columns {cols} for row index {row.name}: {lengths}")
        # If zero-length, return empty list -> row will be dropped by explode
        if lengths[0] == 0:
            return []
        return list(zip(*lists))

    df["__pairs__"] = df.apply(_zip_row, axis=1)
    df = df.explode("__pairs__", ignore_index=True)
    # Unpack pairs back into columns
    if not df.empty:
        for i, c in enumerate(cols):
            df[c] = df["__pairs__"].apply(lambda t: t[i])
    df = df.drop(columns=["__pairs__"]).reset_index(drop=True)
    return df


def detect_multivalue_columns(df: pd.DataFrame) -> List[str]:
    """Return columns that likely contain multiple values per cell.

    Uses heuristics similar to the smart splitter but conservatively avoids
    false positives like CPU model names containing embedded digits (e.g.
    "Apple M3 Max (16 cores)").
    """
    cols: List[str] = []
    # Regexes anchored with word boundaries to avoid matching digits embedded in
    # alphanumeric tokens like "M3".
    number_unit_re = re.compile(r"\b\d+(?:\.\d+)?\s*[A-Za-z%/µ°]+\b")
    number_re = re.compile(r"\b\d+(?:\.\d+)?\b")

    for c in df.columns:
        s = df[c].dropna().astype(str)
        # explicit delimiter characters
        if s.str.contains(r';|,|/|\n').any():
            cols.append(c)
            continue

        # number+unit repeated (like "177 s 167 s")
        if s.str.count(number_unit_re.pattern).gt(1).any():
            cols.append(c)
            continue

        # multiple numeric values separated by spaces
        if s.str.contains(r"\d+(?:\.\d+)?\s+\d+(?:\.\d+)?").any():
            cols.append(c)
            continue

        # multiple spaces / visual separation
        if s.str.contains(r"\s{2,}").any():
            cols.append(c)
            continue

    return cols
