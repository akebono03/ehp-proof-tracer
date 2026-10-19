$ErrorActionPreference = 'Stop'
Write-Host 'PHASE165 RESUMABLE R6 FIX: audited collection scope enabled'
$root = (Get-Location).Path
if (-not (Test-Path '.\phase165_r52_r4_flask_bridge.py')) { throw 'Run from ehp_proof repository root.' }
$required = @(
  '.\phase165_r3_architecture_guard\tests\test_phase165_r3_architecture_guard.py',
  '.\phase165_r4_golden_baseline\tests\test_phase165_r4_golden_baseline.py',
  '.\phase165_r4_golden_baseline\baselines\pi3_2.json',
  '.\phase165_r4_golden_baseline\baselines\pi4_3.json'
)
foreach ($path in $required) { if (-not (Test-Path $path)) { throw "Missing prerequisite: $path" } }
$results = Join-Path $root 'phase165_r6_audit_results'
New-Item -ItemType Directory -Force -Path $results | Out-Null
$env:PYTHONPATH = "$root;$env:PYTHONPATH"
$env:PYTHONIOENCODING = 'utf-8'
$before = @{}
foreach ($name in @('pi3_2', 'pi4_3')) {
  $before[$name] = (Get-FileHash ".\phase165_r4_golden_baseline\baselines\$name.json" -Algorithm SHA256).Hash
}
$guardExit = -1
$goldenExit = -1
$fullExit = -1
$fullRan = $false
try {
  & python -m pytest -q '.\phase165_r3_architecture_guard\tests\test_phase165_r3_architecture_guard.py' 2>&1 | Tee-Object -FilePath (Join-Path $results 'r3_pytest.log')
  $guardExit = $LASTEXITCODE
  if ($guardExit -eq 0) {
    & python -m pytest -q '.\phase165_r4_golden_baseline\tests\test_phase165_r4_golden_baseline.py' 2>&1 | Tee-Object -FilePath (Join-Path $results 'r4_pytest.log')
    $goldenExit = $LASTEXITCODE
  }
  if ($guardExit -eq 0 -and $goldenExit -eq 0) {
    $fullRan = $true
    & python -X utf8 '.\phase165_r6_closure_audit\resumable_full_pytest.py' --root $root --results (Join-Path $results 'resumable_full') --chunk-size 40
    $fullExit = $LASTEXITCODE
  }
} finally {
  $after = @{}
  foreach ($name in @('pi3_2', 'pi4_3')) {
    $after[$name] = (Get-FileHash ".\phase165_r4_golden_baseline\baselines\$name.json" -Algorithm SHA256).Hash
  }
  $unchanged = ($before['pi3_2'] -eq $after['pi3_2']) -and ($before['pi4_3'] -eq $after['pi4_3'])
  $data = [ordered]@{
    phase = '165 R6'
    timestamp = (Get-Date).ToString('o')
    r3_exit_code = $guardExit
    r4_exit_code = $goldenExit
    full_pytest_run = $fullRan
    full_pytest_exit_code = $fullExit
    baseline_hashes_before = $before
    baseline_hashes_after = $after
    baselines_unchanged = $unchanged
    browser_visual_check = 'NOT_VERIFIED'
    phase_closure = 'PENDING_MANUAL_WEB_CHECK_AND_LOG_REVIEW'
    full_pytest_state = (Join-Path $results 'resumable_full\state.json')
  }
  $data | ConvertTo-Json -Depth 6 | Set-Content -Path (Join-Path $results 'audit_result.json') -Encoding UTF8
  Write-Host "R6 report: $(Join-Path $results 'audit_result.json')"
  Write-Host "R3 exit=$guardExit R4 exit=$goldenExit full pytest executed=$fullRan exit=$fullExit baselines unchanged=$unchanged"
}
if ($guardExit -ne 0 -or $goldenExit -ne 0 -or $fullExit -ne 0 -or -not $unchanged) { throw 'R6 automated checks did not pass. Inspect phase165_r6_audit_results logs.' }
Write-Host 'R6 automated checks PASS. Web browser visual confirmation is still required.'
