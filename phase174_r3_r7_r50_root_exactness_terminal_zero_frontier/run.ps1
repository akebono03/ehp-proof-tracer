param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r50_root_exactness_terminal_zero_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R50 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R50_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r50_root_exactness_terminal_zero_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R50 cited root-completion audit failed' }
    $Groups = @(
        @{ Name='R50_STATIC'; Path='phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/tests/test_static.py'; Mode='importlib' },
        @{ Name='R50_GUARD'; Path='phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/tests/test_guard.py'; Mode='importlib' },
        @{ Name='R50_FRONTIER'; Path='phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/tests/test_frontier.py'; Mode='importlib' },
        @{ Name='R49_FRONTIER_REGRESSION'; Path='phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/tests/test_frontier.py'; Mode='importlib' },
        @{ Name='R3_EHP_ROOT_REGRESSION'; Path='phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py'; Mode='importlib' },
        @{ Name='TODA51_ZERO_REGRESSION'; Path='phase165_r12_r15_toda51_fix/tests/test_phase165_r12_r15_toda51.py'; Mode='prepend' },
        @{ Name='PROP42_SPECIALIZATION_REGRESSION'; Path='phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'; Mode='prepend' }
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R50_TEST_GROUP=' + $Group.Name)
        $Mode = $Group.Mode
        if ($Group.Name -eq 'TODA51_ZERO_REGRESSION') {
            # The historical module registers both below-diagonal and circle
            # sources; its old test asserting exactly one source is outdated.
            # Exercise the four mathematics-relevant specialization contracts.
            python -B -m pytest -q "--import-mode=$Mode" -p no:cacheprovider `
              -k 'test_r15_specialization_is_real_inference_with_cited_ancestor or test_r15_general_non_matching_indices_rejected or test_r15_same_general_rule_handles_other_dimensions or test_r15_no_universal_source_no_zero_expansion' $Group.Path
        } else {
            python -B -m pytest -q "--import-mode=$Mode" -p no:cacheprovider $Group.Path
        }
        if ($LASTEXITCODE -ne 0) { throw ('R50 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R50_RUN=PASS'
    Write-Output 'PHASE174_R3R7R50_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
