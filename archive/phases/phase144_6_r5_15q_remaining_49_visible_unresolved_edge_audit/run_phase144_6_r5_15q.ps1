$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $repoRoot

try {
    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15Q preflight"
    Write-Host ("=" * 78)

    pytest -q `
      ".\tests\test_phase144_6_r5_15m_evidence_contributions.py" `
      ".\tests\test_phase144_6_r5_15p_evidence_contribution_vocabulary.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15Q preflight tests failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15Q audit import preflight"
    Write-Host ("=" * 78)

    python -c "import importlib.util, pathlib; p = pathlib.Path(r'$scriptDir') / 'audit_phase144_6_r5_15q.py'; s = importlib.util.spec_from_file_location('phase144_6_r5_15q_audit', p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15Q audit import preflight failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15Q remaining unresolved audit"
    Write-Host ("=" * 78)

    python (Join-Path $scriptDir "audit_phase144_6_r5_15q.py")

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15Q audit failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
