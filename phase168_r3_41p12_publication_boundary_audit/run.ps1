param([switch]$SkipTests)
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$output = Join-Path $package 'output'
New-Item -Path $output -ItemType Directory -Force | Out-Null
$python = 'python'
Push-Location $root
try {
    Write-Host 'R3-41P12 AUDIT_ONLY: application source and existing tests will not be patched.'
    $auditStdout = Join-Path $output 'audit_stdout.log'
    $auditStderr = Join-Path $output 'audit_stderr.log'
    & $python -B -m phase168_r3_41p12_publication_boundary_audit.audit 1> $auditStdout 2> $auditStderr
    $auditExit = $LASTEXITCODE
    Get-Content -Path $auditStdout -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    if ((Test-Path $auditStderr) -and (Get-Item $auditStderr).Length -gt 0) {
        Get-Content -Path $auditStderr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
    }
    Write-Host "audit_EXIT $auditExit"

    $testExit = 0
    if (-not $SkipTests) {
        Write-Host 'Running focused tests only. FULL pytest NOT run.'
        $targets = @(
            'phase168_r3_41p12_publication_boundary_audit/tests/test_publication_gate.py',
            'phase166_r3t_goal_source_binding/test_connection.py',
            'phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py',
            'phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py'
        )
        $pytestStdout = Join-Path $output 'pytest_focused_stdout.log'
        $pytestStderr = Join-Path $output 'pytest_focused_stderr.log'
        & $python -B -m pytest -q @targets 1> $pytestStdout 2> $pytestStderr
        $testExit = $LASTEXITCODE
        Get-Content -Path $pytestStdout -Encoding UTF8 | ForEach-Object { Write-Host $_ }
        if ((Test-Path $pytestStderr) -and (Get-Item $pytestStderr).Length -gt 0) {
            Get-Content -Path $pytestStderr -Encoding UTF8 | ForEach-Object { Write-Warning $_ }
        }
    }
    Write-Host "pytest_focused_EXIT $testExit"

    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $bundle = Join-Path $output "review_bundle_$stamp.zip"
    $items = @('audit.json','audit.md','audit_stdout.log','audit_stderr.log',
               'pytest_focused_stdout.log','pytest_focused_stderr.log',
               'pi3_2_current.md','pi4_3_current.md','pi5_4_current.md')
    $sources = @($items | ForEach-Object { Join-Path $output $_ } | Where-Object { Test-Path $_ })
    if ($sources.Count -gt 0) {
        Compress-Archive -LiteralPath $sources -DestinationPath $bundle -CompressionLevel Optimal
        Write-Host "REVIEW_BUNDLE $bundle"
    }
    Write-Host 'APPLICATION_SOURCE_UNCHANGED'
    Write-Host 'FULL_PYTEST_NOT_RUN'
    if ($auditExit -ne 0 -or $testExit -ne 0) { exit 1 }
    Write-Host 'R3-41P12_AUDIT_COMPLETED'
} finally {
    Pop-Location
}
