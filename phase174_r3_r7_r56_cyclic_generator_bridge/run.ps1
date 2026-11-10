param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r56_cyclic_generator_bridge.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R56 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R56_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }

    python -B -m phase174_r3_r7_r56_cyclic_generator_bridge.install
    if ($LASTEXITCODE -ne 0) { throw 'R56 shared rule connection failed' }

    $Tests = @(
        '.\phase174_r3_r7_r56_cyclic_generator_bridge\tests\test_installer.py',
        '.\phase174_r3_r7_r56_cyclic_generator_bridge\tests\test_rule.py',
        '.\phase174_r3_r7_r37_upper_delta_surjectivity_isolated\tests\test_rule.py',
        '.\phase174_r3_r7_r35_isolated_cyclic_delta_kernel\tests\test_rule.py',
        '.\phase174_r3_r7_r56_cyclic_generator_bridge\tests\test_public.py'
    )
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Tests
    if ($LASTEXITCODE -ne 0) { throw 'R56 focused pytest failed' }

    python -B -m phase174_r3_r7_r56_cyclic_generator_bridge.audit
    if ($LASTEXITCODE -ne 0) { throw 'R56 public proof certification failed' }

    Write-Output 'PHASE174_R56_FOCUSED_TESTS=PASS'
    Write-Output 'PHASE174_R56_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
