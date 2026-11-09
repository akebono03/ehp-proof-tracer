param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r34_prior_lower_delta_source_wiring.install --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R34 source preflight failed' }
& python -B -m phase174_r3_r7_r34_prior_lower_delta_source_wiring.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R34 audit preflight failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R34_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m phase174_r3_r7_r34_prior_lower_delta_source_wiring.install
if ($LASTEXITCODE -ne 0) { throw 'R34 guarded installation failed' }
& python -B -m phase174_r3_r7_r34_prior_lower_delta_source_wiring.audit
if ($LASTEXITCODE -ne 0) { throw 'R34 public source audit failed' }

$Groups = @(
    @{ Name='R34_STATIC'; Files=@('.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_static_helpers.py') },
    @{ Name='R34_SOURCE'; Files=@('.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_source.py') },
    @{ Name='R34_INSTALL'; Files=@('.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_install.py') },
    @{ Name='R34_PUBLIC'; Files=@('.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_public.py') },
    @{ Name='R33_SOURCE_CONTRACT'; Files=@('.\phase174_r3_r7_r33_three_premise_source_frontier\tests\test_source_contract.py') },
    @{ Name='R32_KERNEL_CONTRACT'; Files=@('.\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_kernel_contract.py') },
    @{ Name='R18_SURJECTIVITY'; Files=@('.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py') },
    @{ Name='R5_HOPF_INJECTIVITY'; Files=@('.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py') }
)
foreach ($Group in $Groups) {
    Write-Output ('PHASE174_R3R7R34_TEST_GROUP=' + $Group.Name)
    & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider @($Group.Files)
    if ($LASTEXITCODE -ne 0) { throw ('R34 focused pytest failed: ' + $Group.Name) }
}
Write-Output 'PHASE174_R3R7R34_RUN=PASS'
Write-Output 'PHASE174_R3R7R34_FULL_PYTEST=False'
Write-Output '(END)'
