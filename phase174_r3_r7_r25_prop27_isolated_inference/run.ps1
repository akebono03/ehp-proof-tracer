param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& python -B -m phase174_r3_r7_r25_prop27_isolated_inference.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R25 Source Guard failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R25_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}
& python -B -m pytest -q -p no:cacheprovider `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_rule.py `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_lineage.py `
  tests/test_phase50_prop27_theorem_semantics.py `
  phase174_r3_r7_r24_prop27_general_typed_design/tests/test_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R25 focused pytest failed' }
Write-Output 'PHASE174_R3R7R25_RUN=PASS'
Write-Output '(END)'
