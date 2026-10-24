$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
$output = Join-Path $package 'output'
New-Item -ItemType Directory -Path $output -Force | Out-Null
$python = (Get-Command python -ErrorAction Stop).Source
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = $project

function Invoke-LoggedPython {
    param([string]$Label, [string[]]$PythonArguments)
    $stdout = Join-Path $output ($Label + '_stdout.log')
    $stderr = Join-Path $output ($Label + '_stderr.log')
    $process = Start-Process -FilePath $python `
        -ArgumentList $PythonArguments `
        -WorkingDirectory $project -Wait -PassThru -NoNewWindow `
        -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    if (Test-Path $stdout) {
        Get-Content -Path $stdout -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    }
    if ((Test-Path $stderr) -and ((Get-Item $stderr).Length -gt 0)) {
        Write-Host "STDERR_LOG $stderr"
        Get-Content -Path $stderr -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    }
    Write-Host ($Label + '_EXIT ' + $process.ExitCode)
    return [int]$process.ExitCode
}

Push-Location $project
try {
    if (-not (Test-Path '.\phase168_r3_27_typed_statement_projection.py')) {
        throw 'EHP Proof Tracer project root not found. Extract ZIP at the repository root.'
    }
    Write-Host 'R3-41P7 AUDIT_ONLY: application code and existing tests are not patched.'
    $auditFileNames = @(
        'phase168_r3_27_typed_statement_projection.py',
        'phase166_r3ac_stable_notation.py',
        'phase165_r12_r11_prop42_unified.py',
        'phase165_r12_r12_ehp_consequences.py',
        'phase168_r3_5_model_renderer.py',
        'phase168_r3_3_proof_narrative_model.py'
    )
    $hashBefore = @{}
    foreach ($name in $auditFileNames) {
        $hashBefore[$name] = (Get-FileHash -LiteralPath (Join-Path $project $name) -Algorithm SHA256).Hash
    }
    (& git status --short 2>$null) | Out-File -FilePath (Join-Path $output 'git_status_before.txt') -Encoding UTF8
    $auditExit = Invoke-LoggedPython -Label 'audit' -PythonArguments @(
        '-B', '-m', 'phase168_r3_41p7_shape_boundary_audit.audit'
    )
    $tests = @(
        'phase168_r3_41p7_shape_boundary_audit/tests/test_audit_helpers.py',
        'phase166_r3ac_stable_notation/tests/test_r3ac.py',
        'phase168_r3_41p6_typed_exactness_prose/tests/test_phase168_r3_41p6_typed_exactness_prose.py',
        'phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py',
        'phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py',
        'phase168_r3_29_order_projection/tests/test_phase168_r3_29_order_projection.py',
        'phase168_r3_39a_reference_accuracy/tests/test_phase168_r3_39a_reference_accuracy.py'
    )
    $missing = @($tests | Where-Object { -not (Test-Path $_) })
    if ($missing.Count -gt 0) {
        Write-Host "MISSING_FOCUSED_TESTS $($missing -join ', ')"
        $pytestExit = 2
    } else {
        Write-Host 'Running focused pytest only. FULL pytest is deferred.'
        $pytestArgs = @('-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider') + $tests
        $pytestExit = Invoke-LoggedPython -Label 'pytest_focused' -PythonArguments $pytestArgs
    }
    $changed = @()
    foreach ($name in $auditFileNames) {
        $after = (Get-FileHash -LiteralPath (Join-Path $project $name) -Algorithm SHA256).Hash
        if ($after -ne $hashBefore[$name]) { $changed += $name }
    }
    (& git status --short 2>$null) | Out-File -FilePath (Join-Path $output 'git_status_after.txt') -Encoding UTF8
    $bundle = Join-Path $output 'review_bundle.zip'
    $items = @(Get-ChildItem -Path $output -File |
        Where-Object { $_.FullName -ne $bundle } |
        ForEach-Object { $_.FullName })
    if ($items.Count -gt 0) {
        Compress-Archive -Path $items -DestinationPath $bundle -Force
        Write-Host "REVIEW_BUNDLE $bundle"
    }
    Write-Host "AUDIT_EXIT $auditExit"
    Write-Host "FOCUSED_PYTEST_EXIT $pytestExit"
    Write-Host "APPLICATION_SOURCE_CHANGED_COUNT $($changed.Count)"
    Write-Host 'FULL_PYTEST_NOT_RUN'
    if ($changed.Count -gt 0) {
        Write-Warning ('Unexpected application source change: ' + ($changed -join ', '))
        exit 3
    }
    if ($auditExit -ne 0) { exit $auditExit }
    if ($pytestExit -ne 0) { exit $pytestExit }
    Write-Host 'R3-41P7_AUDIT_COMPLETED'
} finally {
    Pop-Location
}
