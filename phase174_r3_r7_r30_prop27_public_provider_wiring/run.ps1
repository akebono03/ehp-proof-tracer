param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r30_prop27_public_provider_wiring.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R30 Source Guard failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R30_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
  phase174_r3_r7_r30_prop27_public_provider_wiring/tests/test_provider_contract.py
if ($LASTEXITCODE -ne 0) { throw 'R30R1 pre-install provider contract failed' }

& python -B -m phase174_r3_r7_r30_prop27_public_provider_wiring.install
if ($LASTEXITCODE -ne 0) { throw 'R30 guarded installation failed' }
& python -B -m phase174_r3_r7_r30_prop27_public_provider_wiring.audit
if ($LASTEXITCODE -ne 0) { throw 'R30 public shared source audit failed' }

& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
  phase174_r3_r7_r30_prop27_public_provider_wiring/tests/test_wiring.py `
  phase174_r3_r7_r30_prop27_public_provider_wiring/tests/test_provider_contract.py `
  phase174_r3_r7_r29_prop27_canonical_provider/tests/test_provider.py `
  phase174_r3_r7_r28_prop27_typed_literature_registration/tests/test_registration.py `
  phase174_r3_r7_r27_certified_premise_registry_audit/tests/test_audit.py `
  tests/test_phase50_prop27_theorem_semantics.py
if ($LASTEXITCODE -ne 0) { throw 'R30 focused pytest failed' }

Write-Output 'PHASE174_R3R7R30_RUN=PASS'
Write-Output '(END)'
