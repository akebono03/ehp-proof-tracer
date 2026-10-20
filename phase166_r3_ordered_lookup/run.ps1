$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$source = Join-Path $PSScriptRoot 'phase165_r52_r15_ordered_citation.py'
$destination = Join-Path $root 'phase165_r52_r15_ordered_citation.py'
$testSource = Join-Path $PSScriptRoot 'test_phase165_r52_r15_ordered_citation.py'
$testDestination = Join-Path $root 'phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py'
$backupDir = Join-Path $root 'phase166_r3_ordered_lookup_backups'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
if (-not (Test-Path $destination)) { throw 'Production file missing' }
if (-not (Test-Path $testDestination)) { throw 'Existing R15 test file missing' }
$old = Get-Content $destination -Raw -Encoding UTF8
if (($old -notmatch 'def ordered_typed_reference_steps') -or ($old -notmatch 'assess_phase164_r2_citation|assess_citation')) {
    throw 'Unexpected existing code. No changes applied.'
}
$stamp = Get-Date -Format 'yyyyMMddTHHmmss'
Copy-Item $destination (Join-Path $backupDir "phase165_r52_r15_ordered_citation.$stamp.bak")
Copy-Item $testDestination (Join-Path $backupDir "test_phase165_r52_r15_ordered_citation.$stamp.bak")
Copy-Item $source $destination -Force
Copy-Item $testSource $testDestination -Force
python -m py_compile $destination
if ($LASTEXITCODE -ne 0) { throw 'Compile failed' }
python -m pytest -q phase166_r3_ordered_lookup/tests/test_phase166_r3_ordered_lookup.py tests/test_phase163_r3_registry_validation.py phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py tests/test_phase165_r3_recursive_search.py
if ($LASTEXITCODE -ne 0) { throw 'Targeted tests FAILED. Restore backup before continuing.' }
Write-Host 'R3 ordered lookup targeted PASS. Production Web default path unchanged. Full pytest NOT run.'
