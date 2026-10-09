$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$script = Join-Path $package 'check_phase162_r4_b3_full_text.py'
if (-not (Test-Path '.\toda_group_proof_narrative_renderer.py')) {
    throw 'Run this script from the EHP Proof Tracer repository root.'
}
python -B $script
if ($LASTEXITCODE -ne 0) { throw 'Full-text inspection failed.' }
Write-Host 'Read-only full-text inspection complete. No production files changed.'
