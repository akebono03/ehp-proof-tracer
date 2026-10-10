"""Regression test: packaged audit must import the installed project module."""
import os
from pathlib import Path
import subprocess
import sys


def test_packaged_audit_imports_project_root_registration_module():
    project_root = Path(__file__).resolve().parents[1]
    audit_path = project_root / "phase163_r4_r12_prop51_prop53" / "audit.py"
    assert audit_path.is_file()
    command = (
        "import runpy, sys; "
        "from pathlib import Path; "
        f"runpy.run_path({str(audit_path)!r}, run_name='audit_import_probe'); "
        "module = sys.modules['phase163_r4_r12_literature_registration']; "
        f"assert Path(module.__file__).resolve() == Path({str(project_root / 'phase163_r4_r12_literature_registration.py')!r}) "
        "and Path(module.__file__).is_file()"
    )
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(project_root)
    result = subprocess.run(
        [sys.executable, "-B", "-c", command],
        cwd=project_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
