$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
$output = Join-Path $package "output"
New-Item -ItemType Directory -Path $output -Force | Out-Null
$python = (Get-Command python -ErrorAction Stop).Source
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:PYTHONPATH = $project

function Invoke-LoggedPython {
    param(
        [string]$Label,
        [string[]]$PythonArguments
    )
    $stdout = Join-Path $output ($Label + "_stdout.log")
    $stderr = Join-Path $output ($Label + "_stderr.log")
    $process = Start-Process -FilePath $python `
        -ArgumentList $PythonArguments `
        -WorkingDirectory $project `
        -Wait -PassThru -NoNewWindow `
        -RedirectStandardOutput $stdout `
        -RedirectStandardError $stderr
    if (Test-Path $stdout) { Get-Content -Path $stdout -Encoding UTF8 | ForEach-Object { Write-Host $_ } }
    if ((Test-Path $stderr) -and ((Get-Item $stderr).Length -gt 0)) {
        Write-Host "ERROR_LOG $(Join-Path $output ($Label + '_stderr.log'))"
        Get-Content -Path $stderr -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    }
    Write-Host ($Label + "_EXIT " + $process.ExitCode)
    return [int]$process.ExitCode
}

Push-Location $project
try {
    Write-Host "R3-41P4 AUDIT_ONLY: do not patch application source or tests."
    if (-not (Test-Path ".\phase168_r3_5_model_renderer.py")) {
        throw "Project root not found. Extract this package into the ehp-proof-tracer repository root."
    }
    & git status --short 2>$null | Out-File -FilePath (Join-Path $output "git_status_before.txt") -Encoding UTF8
    $auditExit = Invoke-LoggedPython -Label "audit" -PythonArguments @(
        "-B", "-m", "phase168_r3_41p4_residual_boundary_audit.audit"
    )
    Write-Host "Running focused pytest only. FULL pytest is deferred."
    $tests = @(
        "phase168_r3_41p4_residual_boundary_audit/tests/test_audit_r341p4.py",
        "phase168_r3_41p3_provenance_only/tests/test_r341p3_provenance_only.py",
        "phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py",
        "phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py",
        "phase168_r3_29_order_projection/tests/test_phase168_r3_29_order_projection.py",
        "phase168_r3_39a_reference_accuracy/tests/test_phase168_r3_39a_reference_accuracy.py",
        "phase168_r3_8_citation_origin/tests/test_phase168_r3_8_citation_origin.py"
    )
    $missing = @($tests | Where-Object { -not (Test-Path $_) })
    if ($missing.Count -gt 0) {
        Write-Host "MISSING_FOCUSED_TESTS $($missing -join ', ')"
        $pytestExit = 2
    } else {
        $pytestArgs = @("-B", "-m", "pytest", "-q", "-p", "no:cacheprovider") + $tests
        $pytestExit = Invoke-LoggedPython -Label "pytest_focused" -PythonArguments $pytestArgs
    }
    & git status --short 2>$null | Out-File -FilePath (Join-Path $output "git_status_after.txt") -Encoding UTF8

    $bundle = Join-Path $output "review_bundle.zip"
    $reviewFiles = @(Get-ChildItem -Path $output -File |
        Where-Object { $_.FullName -ne $bundle } | ForEach-Object { $_.FullName })
    if ($reviewFiles.Count -gt 0) {
        Compress-Archive -Path $reviewFiles -DestinationPath $bundle -Force
        Write-Host "REVIEW_BUNDLE $bundle"
    }
    Write-Host "AUDIT_EXIT $auditExit"
    Write-Host "FOCUSED_PYTEST_EXIT $pytestExit"
    Write-Host "FULL_PYTEST_NOT_RUN"
    Write-Host "APPLICATION_SOURCE_UNCHANGED"
    if ($auditExit -ne 0) { exit $auditExit }
    if ($pytestExit -ne 0) { exit $pytestExit }
    Write-Host "R3-41P4 AUDIT_COMPLETED"
} finally {
    Pop-Location
}
