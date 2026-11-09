param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r32_lower_delta_kernel_audit.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R32 Source Guard / DryRun failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R32_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m phase174_r3_r7_r32_lower_delta_kernel_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R32 conditional mathematical audit failed' }

$Groups = @(
    @{ Name='R32_CONTRACT'; Files=@('.\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_kernel_contract.py') },
    @{ Name='R32_AUDIT'; Files=@('.\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_audit.py') },
    # R31's HEAD-pinned audit is historically correct but no longer runnable
    # after its merge. Execute only the reusable source/typed regressions;
    # R31 files and historical assertions remain unchanged.
    @{ Name='R31_REUSABLE_REGRESSION'; Files=@(
        '.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_static_helpers.py',
        '.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_audit.py::test_git_blob_computation_and_lf_crlf_allowance',
        '.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_audit.py::test_toda_proposition_source_dependency_order',
        '.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_audit.py::test_toda_source_mutated_lower_kernel_is_rejected',
        '.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_audit.py::test_all_git_pins_are_whole_file_pins',
        '.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_audit.py::test_typed_hopf_delta_bridge_has_distinct_independent_goals'
    ) },
    @{ Name='R18_SURJECTIVITY'; Files=@('.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py') },
    @{ Name='R5_HOPF_INJECTIVITY'; Files=@('.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py') }
)
foreach ($Group in $Groups) {
    Write-Output ('PHASE174_R3R7R32_TEST_GROUP=' + $Group.Name)
    & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider @($Group.Files)
    if ($LASTEXITCODE -ne 0) { throw ('R32 focused pytest failed: ' + $Group.Name) }
}

Write-Output 'PHASE174_R3R7R32_RUN=PASS'
Write-Output 'PHASE174_R3R7R32_FULL_PYTEST=False'
Write-Output '(END)'
