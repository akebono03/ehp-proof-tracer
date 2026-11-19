param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Join-Path $root 'phase175_r4r12r13r8r2_live_citation_trace'
$script = Join-Path $package 'trace.py'
$test = Join-Path (Join-Path $package 'tests') 'test_trace.py'
if (-not (Test-Path $script)) { throw 'Run from repository root' }
$branch = & git branch --show-current
if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'Expected develop branch' }
$before = (& git status --porcelain) -join "`n"
if ($DryRun) {
    & python -B -m pytest -q -p no:cacheprovider $test
    if ($LASTEXITCODE -ne 0) { throw 'Focused tracer tests failed' }
    Write-Output 'PHASE175_R13R8R2_DRYRUN=PASS_TESTS_ONLY'
} else {
    & python -B -m pytest -q -p no:cacheprovider $test
    if ($LASTEXITCODE -ne 0) { throw 'Focused tracer tests failed' }
    $output = Join-Path $env:TEMP 'EHP_Phase175_R13R8R2_live_citation_trace.json'
    & python -B $script --root $root --output $output
    if ($LASTEXITCODE -ne 0) { throw 'Live reference trace failed; inspect report' }
}
$after = (& git status --porcelain) -join "`n"
if ($before -ne $after) { throw 'Repository working tree status changed' }
Write-Output 'PHASE175_R13R8R2_SOURCE_UNCHANGED=PASS'
