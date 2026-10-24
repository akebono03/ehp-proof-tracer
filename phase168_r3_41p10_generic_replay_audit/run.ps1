param([switch]$SkipTests, [switch]$BundleOnly)

$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$output = Join-Path $package 'output'
New-Item -ItemType Directory -Force -Path $output | Out-Null

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $pythonCommand) {
    throw 'Python was not found on PATH.'
}
$python = $pythonCommand.Source

function Invoke-CapturedPython {
    param(
        [string]$Label,
        [string[]]$Arguments
    )
    $standardOutput = Join-Path $output ($Label + '_stdout.log')
    $standardError = Join-Path $output ($Label + '_stderr.log')
    $process = Start-Process -FilePath $python -ArgumentList $Arguments `
        -Wait -PassThru -NoNewWindow `
        -RedirectStandardOutput $standardOutput -RedirectStandardError $standardError
    if (Test-Path $standardOutput) {
        Get-Content -Path $standardOutput -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    }
    if (Test-Path $standardError) {
        Get-Content -Path $standardError -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    }
    Write-Host ($Label + '_EXIT ' + $process.ExitCode)
    return [int]$process.ExitCode
}

function Write-ReviewBundle {
    # Archive only audit/report files; exclude previous review bundles.
    $entries = @(
        Get-ChildItem -LiteralPath $output -File |
            Where-Object { $_.Name -notlike 'review_bundle*.zip' } |
            ForEach-Object { $_.FullName }
    )
    if ($entries.Count -eq 0) {
        throw 'No audit report files found to bundle.'
    }
    $target = Join-Path $output 'review_bundle.zip'
    try {
        Compress-Archive -LiteralPath $entries -DestinationPath $target `
            -CompressionLevel Optimal -Force -ErrorAction Stop
    } catch {
        # Dropbox or antivirus may temporarily lock the existing fixed-name ZIP.
        # Preserve the successful audit and use a fresh filename instead.
        Write-Warning ('Fixed review_bundle.zip unavailable: ' + $_.Exception.Message)
        $unique = ('review_bundle_' + [guid]::NewGuid().ToString('N') + '.zip')
        $target = Join-Path $output $unique
        Compress-Archive -LiteralPath $entries -DestinationPath $target `
            -CompressionLevel Optimal -ErrorAction Stop
    }
    if (-not (Test-Path -LiteralPath $target)) {
        throw ('Review bundle was not created: ' + $target)
    }
    Write-Host ('REVIEW_BUNDLE ' + $target)
}

Push-Location $root
try {
    if ($BundleOnly) {
        $auditJson = Join-Path $output 'audit.json'
        if (-not (Test-Path -LiteralPath $auditJson)) {
            throw 'Existing audit.json is missing; cannot recover prior results.'
        }
        Write-Host 'R3-41P10A BUNDLE_ONLY: existing audit and pytest results are preserved.'
        Write-ReviewBundle
        Write-Host 'AUDIT_NOT_RERUN'
        Write-Host 'PYTEST_NOT_RERUN'
        Write-Host 'FULL_PYTEST_NOT_RUN'
        Write-Host 'APPLICATION_SOURCE_UNCHANGED'
        exit 0
    }
    Write-Host 'R3-41P10 AUDIT_ONLY: existing application modules and tests will not be patched.'
    (& git status --porcelain 2>$null) | Set-Content -Path (Join-Path $output 'git_status_before.txt') -Encoding UTF8

    $auditExit = Invoke-CapturedPython -Label 'audit' -Arguments @(
        '-B', '-m', 'phase168_r3_41p10_generic_replay_audit.audit'
    )
    $testExit = 0
    if (-not $SkipTests) {
        Write-Host 'Running focused pytest only. Full pytest will NOT run.'
        $paths = @(
            'phase168_r3_41p10_generic_replay_audit/tests/test_audit_helpers.py',
            'phase165_r3_recursive_search/tests/test_phase165_r3_recursive_search.py',
            'phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py',
            'phase166_r3ac_stable_notation/tests/test_r3ac.py',
            'phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py',
            'phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py'
        )
        foreach ($path in $paths) {
            if (-not (Test-Path $path)) {
                throw ('Required focused test is missing: ' + $path)
            }
        }
        $pytestArgs = @('-B', '-m', 'pytest', '-q') + $paths
        $testExit = Invoke-CapturedPython -Label 'pytest_focused' -Arguments $pytestArgs
    } else {
        Write-Host 'FOCUSED_TESTS_SKIPPED_BY_REQUEST'
    }

    (& git status --porcelain 2>$null) | Set-Content -Path (Join-Path $output 'git_status_after.txt') -Encoding UTF8
    Write-ReviewBundle
    Write-Host ('AUDIT_EXIT ' + $auditExit)
    Write-Host ('FOCUSED_PYTEST_EXIT ' + $testExit)
    Write-Host 'APPLICATION_SOURCE_UNCHANGED'
    Write-Host 'FULL_PYTEST_NOT_RUN'
    if (($auditExit -eq 0) -and ($testExit -eq 0)) {
        Write-Host 'R3-41P10_AUDIT_COMPLETED'
        exit 0
    }
    Write-Warning 'Review audit.md and stdout/stderr logs in review_bundle.zip.'
    exit 1
} finally {
    Pop-Location
}
