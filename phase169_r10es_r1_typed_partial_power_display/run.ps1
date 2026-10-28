$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$expectedHead = 'f94d8bff28692e5a2b293e7cbbb654e89284e1ba'
$target = Join-Path $root 'toda_human_readable_renderer.py'
$branch = (& git branch --show-current).Trim()
$head = (& git rev-parse HEAD).Trim()
Write-Host "R10ES_BRANCH=$branch"
Write-Host "R10ES_HEAD=$head"
if ($branch -ne 'develop') {
    throw 'R10ES requires develop branch'
}
if ($head -ne $expectedHead) {
    throw 'R10ES HEAD differs from independently inspected GitHub develop'
}
$dirty = @(& git diff --name-only HEAD)
if ($LASTEXITCODE -ne 0) {
    throw 'R10ES failed to inspect existing tracked changes'
}
if ($dirty.Count -gt 0) {
    throw "R10ES pre-existing tracked changes require separate review: $($dirty -join ',')"
}
Write-Host 'R10ES_PREEXISTING_TRACKED_DIFF='
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
$runDirectory = Join-Path $PSScriptRoot "output\run_$stamp"
$null = New-Item -ItemType Directory -Path $runDirectory -Force
$backup = Join-Path $runDirectory 'toda_human_readable_renderer.py.before'
try {
    Write-Host 'R10ES_PATCH_START'
    & python -m phase169_r10es_r1_typed_partial_power_display.patch $runDirectory
    if ($LASTEXITCODE -ne 0) { throw 'R10ES guarded patch failed' }

    Write-Host 'R10ES_LIMITED_TEST_START'
    & python -m pytest -p no:cacheprovider -q `
      phase169_r10es_r1_typed_partial_power_display/tests/test_r10es_display.py `
      phase169_r10eb_typed_composition_power/tests/test_r10eb_typed_composition_power.py `
      phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py
    if ($LASTEXITCODE -ne 0) { throw 'R10ES limited pytest failed' }

    Write-Host 'R10ES_LIVE_AUDIT_START'
    $auditDirectory = Join-Path $runDirectory 'audit'
    & python -m phase169_r10es_r1_typed_partial_power_display.audit $auditDirectory
    if ($LASTEXITCODE -ne 0) { throw 'R10ES live audit failed' }

    $changed = @(& git diff --name-only HEAD)
    if ($LASTEXITCODE -ne 0) { throw 'R10ES failed to inspect tracked changes' }
    if ($changed.Count -ne 1 -or $changed[0] -ne 'toda_human_readable_renderer.py') {
        throw "R10ES unexpected tracked diff: $($changed -join ',')"
    }
    Write-Host 'R10ES_EXPECTED_PRODUCTION_FILE=toda_human_readable_renderer.py'
    Write-Host 'R10ES_PROOF_RULES_CHANGED=False'
    Write-Host 'R10ES_FULL_TEST_RUN=False'
    Write-Host "R10ES_OUTPUT=$runDirectory"
    Write-Host 'R10ES_COMPLETE=PASS'
}
catch {
    if (Test-Path -LiteralPath $backup) {
        Copy-Item -LiteralPath $backup -Destination $target -Force
        Write-Host 'R10ES_RESTORED=toda_human_readable_renderer.py'
    }
    throw
}
