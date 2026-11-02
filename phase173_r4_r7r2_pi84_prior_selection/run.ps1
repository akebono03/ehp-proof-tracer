param([switch]$DryRun, [switch]$SkipRemoteCheck)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldEncoding = $env:PYTHONIOENCODING
$OldUtf8 = $env:PYTHONUTF8
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    $env:PYTHONPATH = "$Root;$OldPythonPath"
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location $Root
    try {
        Write-Output 'PHASE173_R4_R7R2_INSTALL_TESTS_START'
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            'phase173_r4_r7r2_pi84_prior_selection/tests/test_install.py'
        if ($LASTEXITCODE -ne 0) { throw 'Installer focused pytest failed' }
        Write-Output 'PHASE173_R4_R7R2_INSTALL_TESTS=PASS'
        $InstallArgs = @('-B','-m','phase173_r4_r7r2_pi84_prior_selection.install',
                         '--root',$Root)
        if ($DryRun) { $InstallArgs += '--dry-run' }
        if ($SkipRemoteCheck) { $InstallArgs += '--skip-remote-check' }
        & python @InstallArgs
        if ($LASTEXITCODE -ne 0) { throw 'R4-R7R2 guarded installation failed' }
        if ($DryRun) {
            & git status -sb
            Write-Output 'PHASE173_R4_R7R2_DRY_RUN=PASS'
            return
        }
        Write-Output 'PHASE173_R4_R7R2_FOCUSED_PYTEST_START'
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            'phase173_r4_r7r2_pi84_prior_selection/tests/test_context.py' `
            'phase173_r4_r7_source_first_rule/tests/test_rule.py' `
            'phase173_r4_r7r1_pi84_premise_diagnostic/tests/test_audit.py' `
            'phase173_r4_r1_lemma54_source_bridge/tests/test_source.py' `
            'phase173_r4_r1_source_bound_56/tests/test_rule.py'
        if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed' }
        Write-Output 'PHASE173_R4_R7R2_FOCUSED_PYTEST=PASS'
        & python -B -m phase173_r4_r7r2_pi84_prior_selection.verify
        if ($LASTEXITCODE -ne 0) { throw 'Isolated source-first proof search not complete' }
        & python -B -m phase173_r4_r1_public_connection.verify
        if ($LASTEXITCODE -ne 0) { throw 'pi_7^4 public proof regression failed' }
        Write-Output 'PHASE173_R4_R7R2_PI74_REGRESSION=PASS'
        & git status -sb
        & git diff --stat
        Write-Output 'PHASE173_R4_R7R2_RUN=PASS'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldEncoding
    $env:PYTHONUTF8 = $OldUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
