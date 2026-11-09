param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& python -B -m phase174_r3_r7_r29_prop27_canonical_provider.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R29 Source Guard failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R29_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}
& python -B -m phase174_r3_r7_r29_prop27_canonical_provider.audit
if ($LASTEXITCODE -ne 0) { throw 'R29 canonical proof audit failed' }
& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
  phase174_r3_r7_r29_prop27_canonical_provider/tests/test_provider.py `
  phase174_r3_r7_r28_prop27_typed_literature_registration/tests/test_registration.py `
  phase174_r3_r7_r27_certified_premise_registry_audit/tests/test_audit.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_bridge.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_audit.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_run_import_mode.py `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_rule.py `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_lineage.py `
  phase174_r3_r7_r24_prop27_general_typed_design/tests/test_audit.py `
  tests/test_phase50_prop27_theorem_semantics.py
if ($LASTEXITCODE -ne 0) { throw 'R29 focused pytest failed' }
Write-Output 'PHASE174_R3R7R29_RUN=PASS'
Write-Output '(END)'
