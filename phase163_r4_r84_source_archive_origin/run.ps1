$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = $PSScriptRoot
$Script = Join-Path $PackageRoot 'phase163_r4_r84_apply.py'
$TargetTest = Join-Path $ProjectRoot 'tests\test_phase163_r4_r84_source_archive_origin.py'
$TargetHelper = Join-Path $ProjectRoot 'phase163_r4_r84_apply.py'
if (-not (Test-Path $TargetHelper)) {
    Copy-Item $Script $TargetHelper
} else {
    if ((Get-FileHash $TargetHelper -Algorithm SHA256).Hash -ne (Get-FileHash $Script -Algorithm SHA256).Hash) { throw 'Existing R84 helper differs.' }
}
if (-not (Test-Path (Join-Path $ProjectRoot 'phase163_source_archive_registry.py'))) { throw 'R83 must be installed first.' }
if (-not (Test-Path (Join-Path $ProjectRoot 'unified_statement_registry.py'))) { throw 'Missing unified registry.' }
if (-not (Test-Path $TargetTest)) {
    Copy-Item (Join-Path $PackageRoot 'tests\test_phase163_r4_r84_source_archive_origin.py') $TargetTest
} else {
    $Expected = (Get-FileHash (Join-Path $PackageRoot 'tests\test_phase163_r4_r84_source_archive_origin.py') -Algorithm SHA256).Hash
    $Actual = (Get-FileHash $TargetTest -Algorithm SHA256).Hash
    if ($Expected -ne $Actual) { throw 'Existing R84 test differs.' }
}
python $Script --project $ProjectRoot --package $PackageRoot
if ($LASTEXITCODE -ne 0) { throw 'R84 guarded application failed.' }
python -m pytest -q tests/test_phase163_r4_r84_source_archive_origin.py tests/test_phase163_r4_r83_source_archive_registry.py tests/test_phase163_r2_unified_registry.py
if ($LASTEXITCODE -ne 0) { throw 'R84 focused tests failed. Restore from .phase163_r84_before.py.bak backups.' }
python -c "from phase163_source_archive_registry import build_registry_with_source_archive; from unified_statement_registry import AssertionOrigin; r,s=build_registry_with_source_archive(); print({'phase':'163 R4-R84','source_archive_count':sum(r.assertion(k).origin is AssertionOrigin.SOURCE_ARCHIVE for k in s['source_text_assertion_ids']),'proof_eligible_count':s['proof_eligible_count'],'production_auto_connected':False,'full_suite_run':False})"
if ($LASTEXITCODE -ne 0) { throw 'R84 audit failed.' }
Write-Host 'R84 source archive origin verified. Full pytest not run.'
