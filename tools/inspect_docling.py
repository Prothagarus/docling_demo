import inspect
import pkgutil
import pathlib
import docling

print('docling package path:', pathlib.Path(docling.__file__).parents[0])

found = False
p = pathlib.Path(docling.__file__).parents[0]
for f in p.rglob('*.py'):
    txt = f.read_text(errors='ignore')
    if any(k in txt for k in ('export_to_dataframe', 'export_to_html', 'to_markdown', 'to_csv')):
        print('found match in', f)
        lines = txt.splitlines()
        for i, line in enumerate(lines):
            if any(k in line for k in ('def ', 'export_to_html', 'export_to_dataframe', 'to_markdown', 'to_csv')):
                start = max(0, i-3)
                end = min(len(lines), i+6)
                print('\n'.join(lines[start:end]))
                break
        found = True
    if 'class Table' in txt or 'class TableElement' in txt:
        print('class definition candidate in', f)
        lines = txt.splitlines()
        for i, line in enumerate(lines):
            if 'class Table' in line or 'class TableElement' in line:
                start = max(0, i-3)
                end = min(len(lines), i+10)
                print('\n'.join(lines[start:end]))
                break

if not found:
    print('export_to_dataframe not found in docling package files')
