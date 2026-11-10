param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r57_narrative_source_cleanup.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R57 guarded preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R57_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r57_narrative_source_cleanup.install
    if ($LASTEXITCODE -ne 0) { throw 'R57 install failed' }
    $Tests = @(
        'phase174_r3_r7_r57_narrative_source_cleanup/tests/test_static.py',
        'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py',
        'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_public.py',
        'phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_rule.py'
    )
    foreach ($Test in $Tests) {
        Write-Output ('PHASE174_R57_FOCUSED_PYTEST=' + $Test)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Test
        if ($LASTEXITCODE -ne 0) { throw ('R57 focused pytest failed: ' + $Test) }
    }
    python -B -m phase174_r3_r7_r57_narrative_source_cleanup.audit
    if ($LASTEXITCODE -ne 0) { throw 'R57 real source-first narrative audit failed' }
    Write-Output 'PHASE174_R57_FULL_PYTEST=False'
    Write-Output 'PHASE174_R57_GATE=PASS_R57_LOCAL_FOCUSED_AND_PUBLIC'
    Write-Output '(END)'
} finally {
    Pop-Location
}
