$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
$output = Join-Path $package 'output'
New-Item -ItemType Directory -Force -Path $output | Out-Null
Push-Location $project
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $python = (Get-Command python -ErrorAction Stop).Source
    Write-Host 'R3-41P8 AUDIT_ONLY: no application source or tests will be patched.'
    git status --porcelain 1> (Join-Path $output 'git_status_before.txt') 2>$null
    & $python -B -m phase168_r3_41p8_trust_boundary_audit.audit 1> (Join-Path $output 'audit_stdout.log') 2> (Join-Path $output 'audit_stderr.log')
    $auditExit = $LASTEXITCODE
    Get-Content (Join-Path $output 'audit_stdout.log') -ErrorAction SilentlyContinue | Write-Host
    if ($auditExit -ne 0) {
        Get-Content (Join-Path $output 'audit_stderr.log') -ErrorAction SilentlyContinue | Write-Host
    }
    Write-Host "audit_EXIT $auditExit"
    $tests = @(
        '.\phase168_r3_41p8_trust_boundary_audit\tests\test_audit_utilities.py',
        '.\phase168_r3_41p8_trust_boundary_audit\tests\test_phase168_r3_41p8_trust_boundary.py',
        '.\phase166_r3ac_stable_notation\tests\test_r3ac.py',
        '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
        '.\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py',
        '.\phase168_r3_41n1_import_scope_fix\tests\test_phase168_r3_41n_composed_proof_display.py',
        '.\phase168_r3_29_order_projection\tests\test_phase168_r3_29_order_projection.py',
        '.\phase168_r3_39a_reference_accuracy\tests\test_phase168_r3_39a_reference_accuracy.py',
        '.\phase168_r3_8_citation_origin\tests\test_phase168_r3_8_citation_origin.py'
    )
    $missing = @($tests | Where-Object { -not (Test-Path $_) })
    if ($missing.Count -ne 0) {
        Write-Host "MISSING_FOCUSED_TESTS $($missing -join '; ')"
        $testExit = 2
    } else {
        Write-Host 'Running focused tests only; FULL pytest NOT run.'
        & $python -B -m pytest -q -p no:cacheprovider @tests 1> (Join-Path $output 'pytest_focused_stdout.log') 2> (Join-Path $output 'pytest_focused_stderr.log')
        $testExit = $LASTEXITCODE
        Get-Content (Join-Path $output 'pytest_focused_stdout.log') -ErrorAction SilentlyContinue | Write-Host
        if ($testExit -ne 0) {
            Get-Content (Join-Path $output 'pytest_focused_stderr.log') -ErrorAction SilentlyContinue | Write-Host
        }
    }
    Write-Host "pytest_focused_EXIT $testExit"
    git status --porcelain 1> (Join-Path $output 'git_status_after.txt') 2>$null
    $files = @(Get-ChildItem -Path $output -File | Where-Object { $_.Name -ne 'review_bundle.zip' } | Select-Object -ExpandProperty FullName)
    $archive = Join-Path $output 'review_bundle.zip'
    if (Test-Path $archive) { Remove-Item $archive -Force }
    if ($files.Count -ne 0) { Compress-Archive -LiteralPath $files -DestinationPath $archive -Force }
    Write-Host "REVIEW_BUNDLE $archive"
    Write-Host 'APPLICATION_SOURCE_UNCHANGED'
    Write-Host 'FULL_PYTEST_NOT_RUN'
    Write-Host "AUDIT_EXIT $auditExit"
    Write-Host "FOCUSED_PYTEST_EXIT $testExit"
    if ($auditExit -ne 0 -or $testExit -ne 0) {
        Write-Warning 'R3-41P8 encountered errors; inspect output/review_bundle.zip.'
    } else {
        Write-Host 'R3-41P8_AUDIT_COMPLETED'
    }
} finally {
    Pop-Location
}
