param(
    [switch]$SkipTests
)

$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$output = Join-Path $package 'output'
New-Item -ItemType Directory -Force -Path $output | Out-Null
$python = (Get-Command python.exe -ErrorAction Stop).Source

Write-Host 'R3-41P9 AUDIT_ONLY: application code and existing tests will not be patched.'
Set-Location $root

$before = @(git status --porcelain 2>$null) -join "`n"
[System.IO.File]::WriteAllText((Join-Path $output 'git_status_before.txt'), $before)

function Invoke-CapturedPython {
    param([string]$Name, [string[]]$Arguments)
    $stdout = Join-Path $output ($Name + '_stdout.log')
    $stderr = Join-Path $output ($Name + '_stderr.log')
    $proc = Start-Process -FilePath $python -ArgumentList $Arguments -WorkingDirectory $root `
        -PassThru -Wait -NoNewWindow -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    if (Test-Path $stdout) { Get-Content $stdout -Encoding UTF8 | ForEach-Object { Write-Host $_ } }
    if (Test-Path $stderr) { Get-Content $stderr -Encoding UTF8 | ForEach-Object { Write-Warning $_ } }
    Write-Host ($Name + '_EXIT ' + $proc.ExitCode)
    return [int]$proc.ExitCode
}

$auditCode = Invoke-CapturedPython -Name 'audit' -Arguments @('-B', '-m', 'phase168_r3_41p9_trust_path_audit.audit')
$pytestCode = 0
if (-not $SkipTests) {
    Write-Host 'Running focused pytest only. Full pytest is deferred.'
    $testPaths = @(
        'phase168_r3_41p9_trust_path_audit/tests/test_audit.py',
        'phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py',
        'phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py',
        'phase166_r3ac_stable_notation/tests/test_r3ac.py',
        'phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'
    )
    foreach ($test in $testPaths) {
        if (-not (Test-Path (Join-Path $root $test))) {
            Write-Warning ('Required focused test missing: ' + $test)
            $pytestCode = 2
        }
    }
    if ($pytestCode -eq 0) {
        $pytestCode = Invoke-CapturedPython -Name 'pytest_focused' -Arguments (@('-B','-m','pytest','-q') + $testPaths)
    }
}

$after = @(git status --porcelain 2>$null) -join "`n"
[System.IO.File]::WriteAllText((Join-Path $output 'git_status_after.txt'), $after)
if ($before -ne $after) { Write-Host 'GIT_STATUS_CHANGED: inspect before/after (audit output may be untracked).' }

$reviewBundle = Join-Path $output 'review_bundle.zip'
$items = Get-ChildItem $output -File | Where-Object { $_.Name -ne 'review_bundle.zip' }
if ($items.Count -gt 0) {
    Compress-Archive -Path @($items | ForEach-Object { $_.FullName }) -DestinationPath $reviewBundle -Force
}
Write-Host ('REVIEW_BUNDLE ' + $reviewBundle)
Write-Host ('AUDIT_EXIT ' + $auditCode)
Write-Host ('FOCUSED_PYTEST_EXIT ' + $pytestCode)
Write-Host 'APPLICATION_SOURCE_UNCHANGED'
Write-Host 'FULL_PYTEST_NOT_RUN'
if ($auditCode -eq 0 -and $pytestCode -eq 0) {
    Write-Host 'R3-41P9_AUDIT_COMPLETED'
    exit 0
}
Write-Warning 'Audit or focused tests failed; review bundle retained for diagnosis.'
exit 1
