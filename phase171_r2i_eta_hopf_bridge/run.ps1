param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$Python = 'python'
& $Python -m phase171_r2i_eta_hopf_bridge.install --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R2I preflight failed' }
if ($DryRun) {
    Write-Output 'PHASE171_R2I_RUN=PASS_DRY_RUN'
    exit 0
}
& $Python -m phase171_r2i_eta_hopf_bridge.install
if ($LASTEXITCODE -ne 0) { throw 'R2I install failed' }
& $Python -m pytest -q `
    phase171_r2i_eta_hopf_bridge/tests/test_cited_eta_hopf.py `
    phase171_r2h_prop22_cited_hopf/tests/test_cited_formula.py
if ($LASTEXITCODE -ne 0) { throw 'R2I focused pytest failed' }
Write-Output 'PHASE171_R2I_FOCUSED_PYTEST=PASS'
& $Python -m phase171_r2i_eta_hopf_bridge.audit
if ($LASTEXITCODE -ne 0) { throw 'R2I ancestry audit failed' }
Write-Output 'PHASE171_R2I_RUN=PASS'
