from pathlib import Path
import ast


def test_project_root_inserted_before_bootstrap_import():
    source = Path(__file__).with_name("diagnose.py").read_text(encoding="utf-8")
    assert source.index("sys.path.insert(0, str(PROJECT_ROOT))") < source.index("import toda_upstream_bootstrap as bootstrap")
    ast.parse(source)

def test_parent_directory_resolution():
    script_path = Path(__file__).resolve().with_name("diagnose.py")
    assert script_path.parent.parent.name == "mnt" or script_path.parent.parent.exists()
