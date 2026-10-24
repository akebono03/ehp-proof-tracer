$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
$output = Join-Path $package 'output'
New-Item -ItemType Directory -Force -Path $output | Out-Null
Push-Location $project
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $python = (Get-Command python -ErrorAction Stop).Source
    $testPaths = @(
        '.\phase168_r3_41p6_typed_exactness_prose\tests\test_phase168_r3_41p6_typed_exactness_prose.py',
        '.\phase168_r3_41p5_rule_name_independent\tests\test_phase168_r3_41p5_rule_name_independent.py',
        '.\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py',
        '.\phase168_r3_41n1_import_scope_fix\tests\test_phase168_r3_41n_composed_proof_display.py',
        '.\phase168_r3_29_order_projection\tests\test_phase168_r3_29_order_projection.py',
        '.\phase168_r3_39a_reference_accuracy\tests\test_phase168_r3_39a_reference_accuracy.py',
        '.\phase168_r3_8_citation_origin\tests\test_phase168_r3_8_citation_origin.py'
    )
    foreach ($path in $testPaths) {
        if (-not (Test-Path $path)) { throw "Missing focused test file: $path" }
    }
    Write-Host 'R3-41P6: patch only typed_sentence() with checksum guard.'
    & $python -B -m phase168_r3_41p6_typed_exactness_prose.patch 1> (Join-Path $output 'patch_stdout.log') 2> (Join-Path $output 'patch_stderr.log')
    $patchExit = $LASTEXITCODE
    Get-Content (Join-Path $output 'patch_stdout.log') -ErrorAction SilentlyContinue | Write-Host
    if ($patchExit -ne 0) {
        Get-Content (Join-Path $output 'patch_stderr.log') -ErrorAction SilentlyContinue | Write-Host
        throw "R3-41P6 PATCH FAILED: exit $patchExit. No intentional source change."
    }
    Write-Host 'Running focused pytest and three-group fulltext comparison. NO full suite.'
    & $python -B -m pytest -q -p no:cacheprovider @testPaths 1> (Join-Path $output 'pytest_stdout.log') 2> (Join-Path $output 'pytest_stderr.log')
    $testExit = $LASTEXITCODE
    Get-Content (Join-Path $output 'pytest_stdout.log') -ErrorAction SilentlyContinue | Write-Host
    if ($testExit -ne 0) {
        Get-Content (Join-Path $output 'pytest_stderr.log') -ErrorAction SilentlyContinue | Write-Host
        Write-Warning 'Focused tests failed; reverting Typed Projection from its backup.'
        & $python -B -m phase168_r3_41p6_typed_exactness_prose.restore
        if ($LASTEXITCODE -ne 0) { throw 'RESTORE FAILED: Inspect backup and post_patch.json.' }
        throw "R3-41P6 FOCUSED TEST FAILED: $testExit. Application source restored."
    }
    Write-Host 'R3-41P6_FOCUSED_PASS'
    Write-Host '3_GROUP_FULLTEXT_IDENTICAL_TO_R3_41P5'
    Write-Host 'FULL_PYTEST_NOT_RUN'
    Write-Host "FULL_FUNCTION $(Join-Path $output 'typed_sentence_FULL.py')"
    Write-Host "BACKUP $(Join-Path $output 'backups\phase168_r3_27_typed_statement_projection.py')"
} finally {
    Pop-Location
}
