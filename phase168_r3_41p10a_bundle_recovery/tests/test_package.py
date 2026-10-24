"""Static regression checks for R3-41P10A archive recovery."""
from pathlib import Path
import hashlib

PACKAGE = Path(__file__).resolve().parents[1]


def test_full_runner_uses_no_temporary_zip():
    source = (PACKAGE / "run_FIXED.ps1").read_text(encoding="utf-8")
    assert "review_bundle.tmp.zip" not in source
    assert "Copy-Item -Path $tempZip" not in source
    assert "Remove-Item -Path $tempZip" not in source
    assert "Compress-Archive -LiteralPath $entries" in source
    assert "review_bundle*.zip" in source


def test_bundle_only_does_not_rerun_audit_or_tests():
    source = (PACKAGE / "run_FIXED.ps1").read_text(encoding="utf-8")
    assert "param([switch]$SkipTests, [switch]$BundleOnly)" in source
    bundle_branch = source.split("if ($BundleOnly) {", 1)[1].split("Write-Host 'R3-41P10 AUDIT_ONLY", 1)[0]
    assert "Write-ReviewBundle" in bundle_branch
    assert "AUDIT_NOT_RERUN" in bundle_branch
    assert "PYTEST_NOT_RERUN" in bundle_branch
    assert "exit 0" in bundle_branch
    assert "Invoke-CapturedPython" not in bundle_branch


def test_guarded_backup_and_checksum():
    launcher = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    runner = (PACKAGE / "run_FIXED.ps1").read_bytes()
    digest = hashlib.sha256(runner).hexdigest()
    assert digest in launcher
    assert "Copy-Item -LiteralPath $target -Destination $backup" in launcher
    assert "Unknown R3-41P10 runner checksum" in launcher
    assert "-BundleOnly" in launcher


def test_preserves_failure_status_and_focus_only():
    source = (PACKAGE / "run_FIXED.ps1").read_text(encoding="utf-8")
    assert "if (($auditExit -eq 0) -and ($testExit -eq 0))" in source
    assert "FULL_PYTEST_NOT_RUN" in source
    assert "phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py" in source
