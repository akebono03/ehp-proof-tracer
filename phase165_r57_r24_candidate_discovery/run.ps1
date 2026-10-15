$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo
if (-not (Test-Path -LiteralPath (Join-Path $repo 'phase165_r57_r23_conclusion_unification.py'))) {
    throw 'R23 module missing. Run Phase 165 R57-R23-R1 first.'
}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'phase165_r57_r24_candidate_discovery.py') -Destination (Join-Path $repo 'phase165_r57_r24_candidate_discovery.py') -Force
Write-Output 'R24 candidate discovery installed (new module only).'
python -m pytest -q (Join-Path $PSScriptRoot 'test_phase165_r57_r24_candidate_discovery.py')
if ($LASTEXITCODE -ne 0) { throw 'R24 targeted pytest FAILED' }
Write-Output 'R24 targeted pytest PASSED; full pytest NOT run.'
