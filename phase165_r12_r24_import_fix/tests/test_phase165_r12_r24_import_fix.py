"""Guard the audit import-path regression without modifying project code."""
from pathlib import Path

def test_runner_makes_project_root_importable_and_restores_environment():
    script = Path(__file__).resolve().parents[1] / 'run.ps1'
    content = script.read_text(encoding='utf-8')
    assert '$env:PYTHONPATH = if ($priorPythonPath)' in content
    assert '$project + [IO.Path]::PathSeparator + $priorPythonPath' in content
    assert '$env:PYTHONPATH = $priorPythonPath' in content
    assert "python (Join-Path $package 'audit.py')" in content
    assert "if ($LASTEXITCODE -ne 0) { throw 'R12-R24 Web search audit failed' }" in content

def test_script_and_project_modules_are_separate():
    root = Path(__file__).resolve().parents[1]
    assert (root / 'audit.py').is_file()
    assert (root / 'phase165_r12_r24_web_search_connection.py').is_file()
