param([switch]$SkipTests)

$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$output = Join-Path $package 'output'
New-Item -ItemType Directory -Path $output -Force | Out-Null
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $pythonCommand) { throw 'python not found' }
$pythonExe = $pythonCommand.Source

function Invoke-PythonProcess {
    param([string]$Name, [string[]]$Params)
    $out = Join-Path $output ($Name + '_stdout.log')
    $err = Join-Path $output ($Name + '_stderr.log')
    $process = Start-Process -FilePath $pythonExe -ArgumentList $Params `
        -Wait -PassThru -NoNewWindow -RedirectStandardOutput $out -RedirectStandardError $err
    if (Test-Path $out) { Get-Content $out -Encoding UTF8 | ForEach-Object { Write-Host $_ } }
    if (Test-Path $err) { Get-Content $err -Encoding UTF8 | ForEach-Object { Write-Host $_ } }
    Write-Host ($Name + '_EXIT ' + $process.ExitCode)
    return [int]$process.ExitCode
}

Push-Location $root
try {
    Write-Host 'R3-41P11 AUDIT_ONLY: application source and existing tests will not be patched.'
    (& git status --porcelain 2>$null) | Set-Content -Path (Join-Path $output 'git_status_before.txt') -Encoding UTF8
    $auditExit = Invoke-PythonProcess -Name 'audit' -Params @('-B', '-m', 'phase168_r3_41p11_given_provenance_audit.audit')
    $pytestExit = 0
    if (-not $SkipTests) {
        Write-Host 'Running focused tests only. Full pytest NOT run.'
        $testFiles = @(
            'phase168_r3_41p11_given_provenance_audit/tests/test_audit_helpers.py',
            'phase165_r3_recursive_search/tests/test_phase165_r3_recursive_search.py',
            'phase166_r3ac_stable_notation/tests/test_r3ac.py',
            'phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py',
            'phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py'
        )
        foreach ($file in $testFiles) {
            if (-not (Test-Path $file)) { throw ('Required focused test missing: ' + $file) }
        }
        $pytestExit = Invoke-PythonProcess -Name 'pytest_focused' -Params (@('-B', '-m', 'pytest', '-q') + $testFiles)
    } else {
        Write-Host 'FOCUSED_PYTEST_SKIPPED_BY_REQUEST'
    }
    (& git status --porcelain 2>$null) | Set-Content -Path (Join-Path $output 'git_status_after.txt') -Encoding UTF8

    # Never archive within the folder selected for archiving, and never touch temp ZIPs.
    # Some Dropbox configurations hold ZIPs open briefly, so use a fresh timestamped name.
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $bundlePath = Join-Path $output ('review_bundle_' + $stamp + '.zip')
    $paths = @(Get-ChildItem -LiteralPath $output -File | Where-Object {
        $_.Extension -ne '.zip' -and $_.Name -notlike '*.tmp.zip'
    } | Select-Object -ExpandProperty FullName)
    if ($paths.Count -eq 0) { throw 'No audit output files to archive' }
    Compress-Archive -LiteralPath $paths -DestinationPath $bundlePath -Force
    Write-Host ('REVIEW_BUNDLE ' + $bundlePath)
    Write-Host ('AUDIT_EXIT ' + $auditExit)
    Write-Host ('FOCUSED_PYTEST_EXIT ' + $pytestExit)
    Write-Host 'APPLICATION_SOURCE_UNCHANGED'
    Write-Host 'FULL_PYTEST_NOT_RUN'
    if ($auditExit -ne 0 -or $pytestExit -ne 0) { exit 1 }
    Write-Host 'R3-41P11_AUDIT_COMPLETED'
    exit 0
} finally {
    Pop-Location
}
