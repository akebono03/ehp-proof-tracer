$ErrorActionPreference = 'Stop'
$Repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $Repo '.git'))) {
    throw 'Run this command from the ehp_proof repository root.'
}
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B '.\phase173_r3_head_guard_fix\audit.py'
if ($LASTEXITCODE -ne 0) {
    throw 'Phase 173 R3 head-guard audit failed.'
}
git status -sb
