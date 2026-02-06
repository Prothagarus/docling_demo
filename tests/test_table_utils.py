import pandas as pd
import pytest

from table_utils import split_and_explode, detect_multivalue_columns


def test_single_column_split_and_explode():
    df = pd.DataFrame({"A": ["x; y", "z"]})
    out = split_and_explode(df, ["A"], mode="cartesian")
    assert list(out["A"]) == ["x", "y", "z"]


def test_smart_split_number_unit_pairs():
    df = pd.DataFrame({"TTS": ["177 s 167 s", "103 s 92 s"]})
    out = split_and_explode(df, ["TTS"], mode="cartesian", smart=True)
    assert list(out["TTS"]) == ["177 s", "167 s", "103 s", "92 s"]


def test_smart_split_numeric_pairs():
    df = pd.DataFrame({"Pages/s": ["1.27 1.34", "0.94 1.57"]})
    out = split_and_explode(df, ["Pages/s"], mode="cartesian", smart=True)
    assert list(out["Pages/s"]) == ["1.27", "1.34", "0.94", "1.57"]


def test_cartesian_explode_two_cols():
    df = pd.DataFrame({"A": ["1;2"], "B": ["a;b"]})
    out = split_and_explode(df, ["A", "B"], mode="cartesian")
    pairs = set(zip(out["A"], out["B"]))
    assert pairs == {("1", "a"), ("1", "b"), ("2", "a"), ("2", "b")}


def test_cartesian_explode_two_cols():
    df = pd.DataFrame({"A": ["1;2"], "B": ["a;b"]})
    out = split_and_explode(df, ["A", "B"], mode="cartesian")
    pairs = set(zip(out["A"], out["B"]))
    assert pairs == {("1", "a"), ("1", "b"), ("2", "a"), ("2", "b")}


def test_pairwise_zip():
    df = pd.DataFrame({"A": ["1;2"], "B": ["a;b"]})
    out = split_and_explode(df, ["A", "B"], mode="pairwise")
    assert list(zip(out["A"], out["B"])) == [("1", "a"), ("2", "b")]


def test_pairwise_smart_number_unit_alignment():
    df = pd.DataFrame({"TTS": ["177 s 167 s"], "Pages/s": ["1.27 1.34"]})
    out = split_and_explode(df, ["TTS", "Pages/s"], mode="pairwise", smart=True)
    assert list(zip(out["TTS"], out["Pages/s"])) == [("177 s", "1.27"), ("167 s", "1.34")]


def test_pairwise_smart_numeric_alignment():
    df = pd.DataFrame({"A": ["4 16"], "B": ["1 2"]})
    out = split_and_explode(df, ["A", "B"], mode="pairwise", smart=True)
    assert list(zip(out["A"], out["B"])) == [("4", "1"), ("16", "2")]


def test_detect_multivalue_columns_excludes_cpu():
    df = pd.DataFrame({
        "CPU": ["Apple M3 Max (16 cores)"],
        "TTS": ["177 s 167 s"],
        "Pages/s": ["1.27 1.34"],
    })
    cols = detect_multivalue_columns(df)
    assert "CPU" not in cols
    assert "TTS" in cols and "Pages/s" in cols


def test_pairwise_unequal_raises():
    df = pd.DataFrame({"A": ["1;2"], "B": ["a"]})
    with pytest.raises(ValueError):
        split_and_explode(df, ["A", "B"], mode="pairwise")
