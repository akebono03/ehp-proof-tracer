param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r31_delta_surjectivity_general_audit.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R31 Source Guard / DryRun failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R31_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m phase174_r3_r7_r31_delta_surjectivity_general_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R31 typed mathematical audit failed' }

$Groups = @(
    @{ Name='R31_AUDIT'; Files=@('.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_audit.py', '.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_static_helpers.py') },
    @{ Name='R5_INJECTIVITY'; Files=@('.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py') },
    @{ Name='R18_SURJECTIVITY'; Files=@('.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py') },
    @{ Name='R25_TYPED_PROP27'; Files=@('.\phase174_r3_r7_r25_prop27_isolated_inference\tests\test_rule.py') },
    @{ Name='EXISTING_PROP27'; Files=@('.\tests\test_phase50_prop27_theorem_semantics.py') }
)
foreach ($Group in $Groups) {
    Write-Output ('PHASE174_R3R7R31_TEST_GROUP=' + $Group.Name)
    & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider @($Group.Files)
    if ($LASTEXITCODE -ne 0) { throw ('R31 focused pytest failed: ' + $Group.Name) }
}

Write-Output 'PHASE174_R3R7R31_RUN=PASS'
Write-Output 'PHASE174_R3R7R31_FULL_PYTEST=False'
Write-Output '(END)'
