import importlib.util
from pathlib import Path


# def test_main_prints_hello(capsys):
#     """Load `src/main.py` and assert the printed output from `main()`."""
#     src_path = Path(__file__).parent.parent / "src" / "main.py"
#     spec = importlib.util.spec_from_file_location("docling.main", src_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)

#     module.main()

#     captured = capsys.readouterr()
#     assert "Hello from docling!" in captured.out
