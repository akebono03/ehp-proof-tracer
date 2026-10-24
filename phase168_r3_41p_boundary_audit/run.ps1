param(
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:PYTHONIOENCODING = "utf-8"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
$output = Join-Path $package "output"
New-Item -ItemType Directory -Force -Path $output | Out-Null

function Invoke-LoggedPython {
    param(
        [Parameter(Mandatory = $true)][string]$Python,
        [Parameter(Mandatory = $true)][string[]]$PythonArguments,
        [Parameter(Mandatory = $true)][string]$OutputPrefix
    )

    $stdoutPath = Join-Path $output ($OutputPrefix + "_stdout.log")
    $stderrPath = Join-Path $output ($OutputPrefix + "_stderr.log")
    $combinedPath = Join-Path $output ($OutputPrefix + ".log")

    # Start-Process keeps native stderr separate from PowerShell's error stream.
    # In Windows PowerShell 5.1, 2>&1 with ErrorActionPreference=Stop can abort
    # before the Python Traceback has been saved.
    $argumentLine = ($PythonArguments | ForEach-Object {
        '"' + ($_ -replace '"', '\"') + '"'
    }) -join " "

    $process = Start-Process `
        -FilePath $Python `
        -ArgumentList $argumentLine `
        -WorkingDirectory $project `
        -Wait `
        -PassThru `
        -NoNewWindow `
        -RedirectStandardOutput $stdoutPath `
        -RedirectStandardError $stderrPath

    $stdout = ""
    $stderr = ""
    if (Test-Path -LiteralPath $stdoutPath) {
        $stdout = [string](Get-Content -LiteralPath $stdoutPath -Raw -Encoding UTF8)
    }
    if (Test-Path -LiteralPath $stderrPath) {
        $stderr = [string](Get-Content -LiteralPath $stderrPath -Raw -Encoding UTF8)
    }
    ($stdout + [Environment]::NewLine + $stderr) |
        Set-Content -LiteralPath $combinedPath -Encoding UTF8

    if ($stdout.Length -gt 0) { Write-Host $stdout }
    if ($stderr.Length -gt 0) { Write-Host $stderr -ForegroundColor Yellow }
    Write-Host ($OutputPrefix + "_EXIT " + $process.ExitCode)
    return [int]$process.ExitCode
}

Push-Location $project
try {
    if (-not (Test-Path ".\phase168_r3_5_model_renderer.py")) {
        throw "Project root is not the expected EHP Proof Tracer root."
    }
    $python = (Get-Command python -ErrorAction Stop).Source
    $testPaths = @(
        ".\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py",
        ".\phase168_r3_41n1_import_scope_fix\tests\test_phase168_r3_41n_composed_proof_display.py",
        ".\phase168_r3_29_order_projection\tests\test_phase168_r3_29_order_projection.py",
        ".\phase168_r3_39a_reference_accuracy\tests\test_phase168_r3_39a_reference_accuracy.py",
        ".\phase168_r3_8_citation_origin\tests\test_phase168_r3_8_citation_origin.py",
        ".\phase168_r3_41p_boundary_audit\tests\test_audit_error_reporting.py"
    )
    $missing = @($testPaths | Where-Object { -not (Test-Path $_) })
    if ($missing.Count -gt 0) {
        throw ("Required focused test files are missing: " + ($missing -join ", "))
    }

    Write-Host "R3-41P AUDIT_ONLY: application source files will not be patched."
    $before = (git status --porcelain 2>$null) -join "`n"
    $before | Set-Content -Encoding UTF8 (Join-Path $output "git_status_before.txt")

    $auditExit = Invoke-LoggedPython `
        -Python $python `
        -PythonArguments @("-B", (Join-Path $package "audit.py")) `
        -OutputPrefix "audit_console"

    $testExit = 0
    if (-not $SkipTests) {
        Write-Host "Running R3-41P focused tests only; full pytest NOT run."
        $pythonArgs = @("-B", "-m", "pytest", "-q", "-p", "no:cacheprovider") + $testPaths
        $testExit = Invoke-LoggedPython `
            -Python $python `
            -PythonArguments $pythonArgs `
            -OutputPrefix "pytest_focused"
    } else {
        "FOCUSED_PYTEST_SKIPPED" |
            Set-Content -Encoding UTF8 (Join-Path $output "pytest_focused.log")
    }

    $after = (git status --porcelain 2>$null) -join "`n"
    $after | Set-Content -Encoding UTF8 (Join-Path $output "git_status_after.txt")
    if ($before -cne $after) {
        Write-Warning "git status changed during audit. Inspect git_status_before/after.txt."
    }

    $reviewBundle = Join-Path $output "review_bundle.zip"
    $reviewFiles = @(Get-ChildItem -File -Path $output |
        Where-Object { $_.FullName -ne $reviewBundle } |
        ForEach-Object { $_.FullName })
    if ($reviewFiles.Count -gt 0) {
        Compress-Archive -Path $reviewFiles -DestinationPath $reviewBundle -Force
        Write-Host "REVIEW_BUNDLE $reviewBundle"
    }

    Write-Host "AUDIT_EXIT $auditExit"
    Write-Host "FOCUSED_PYTEST_EXIT $testExit"
    Write-Host "FULL_PYTEST_NOT_RUN"
    Write-Host "REPORT $(Join-Path $output 'audit.md')"
    if ($auditExit -ne 0) {
        Write-Warning "Audit identified an error. Check audit.md and *_audit_error.txt. Review bundle was still created."
        exit $auditExit
    }
    if ($testExit -ne 0) {
        Write-Warning "Focused pytest failed. Check pytest_focused.log. Review bundle was still created."
        exit $testExit
    }
    Write-Host "R3-41P audit-only collection completed. No application patch applied."
} finally {
    Pop-Location
}
