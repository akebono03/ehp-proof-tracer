$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path '.\phase165_r52_r4_flask_bridge.py')) { throw 'Run from ehp_proof repository root.' }
$runner = Join-Path $root 'phase165_r6_closure_audit\resumable_full_pytest.py'
if (-not (Test-Path $runner)) { throw 'Missing resumable runner.' }
& python -X utf8 $runner --root $root --results (Join-Path $root 'phase165_r6_audit_results\resumable_full') --chunk-size 40 --defer-failed-batches
$exitCode = $LASTEXITCODE
Write-Host "Runner exit code: $exitCode. All failures remain failures in state.json."
if ($exitCode -ne 0) { Write-Host 'Phase 165 closure BLOCKED until remaining failures are audited.' }
exit $exitCode
