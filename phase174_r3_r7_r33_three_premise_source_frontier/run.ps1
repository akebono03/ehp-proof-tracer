param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r33_three_premise_source_frontier.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R33 Source Guard / DryRun failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R33_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m phase174_r3_r7_r33_three_premise_source_frontier.audit
if ($LASTEXITCODE -ne 0) { throw 'R33 source frontier audit failed' }

$Groups = @(
    @{ Name='R33_SOURCE_CONTRACT'; Files=@('.\phase174_r3_r7_r33_three_premise_source_frontier\tests\test_source_contract.py') },
    @{ Name='R33_REPO_AUDIT'; Files=@('.\phase174_r3_r7_r33_three_premise_source_frontier\tests\test_audit.py') },
    @{ Name='R32_KERNEL_CONTRACT'; Files=@('.\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_kernel_contract.py') },
    @{ Name='R18_SURJECTIVITY'; Files=@('.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py') },
    @{ Name='R5_HOPF_INJECTIVITY'; Files=@('.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py') }
)
foreach ($Group in $Groups) {
    Write-Output ('PHASE174_R3R7R33_TEST_GROUP=' + $Group.Name)
    & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider @($Group.Files)
    if ($LASTEXITCODE -ne 0) { throw ('R33 focused pytest failed: ' + $Group.Name) }
}
Write-Output 'PHASE174_R3R7R33_RUN=PASS'
Write-Output 'PHASE174_R3R7R33_FULL_PYTEST=False'
Write-Output '(END)'
