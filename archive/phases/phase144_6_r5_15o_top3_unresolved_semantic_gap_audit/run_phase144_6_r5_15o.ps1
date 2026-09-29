$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $repoRoot

try {
    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15O preflight"
    Write-Host ("=" * 78)

    if (-not (Test-Path ".\toda_group_proof_narrative_evidence_contributions.py")) {
        throw "15M evidence contribution prototype is missing."
    }

    pytest -q `
      ".\tests\test_phase144_6_r5_15m_evidence_contributions.py" `
      ".\tests\test_phase141_5_narrative_blocks_semantics.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15O preflight tests failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15O audit import preflight"
    Write-Host ("=" * 78)

    python -c "import importlib.util, pathlib; p = pathlib.Path(r'$scriptDir') / 'audit_phase144_6_r5_15o.py'; s = importlib.util.spec_from_file_location('phase144_6_r5_15o_audit', p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15O audit import preflight failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15O top-3 semantic gap audit"
    Write-Host ("=" * 78)

    python (Join-Path $scriptDir "audit_phase144_6_r5_15o.py")

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15O audit failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
