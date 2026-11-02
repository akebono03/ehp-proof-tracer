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
        Write-Output 'PHASE173_R4_R8_INSTALL_TESTS_START'
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            'phase173_r4_r8_public_connection/tests/test_install.py'
        if ($LASTEXITCODE -ne 0) { throw 'R4-R8 installer focused pytest failed' }
        Write-Output 'PHASE173_R4_R8_INSTALL_TESTS=PASS'
        $ArgsForPython = @('-B','-m','phase173_r4_r8_public_connection.install',
                          '--root',$Root)
        if ($DryRun) { $ArgsForPython += '--dry-run' }
        if ($SkipRemoteCheck) { $ArgsForPython += '--skip-remote-check' }
        & python @ArgsForPython
        if ($LASTEXITCODE -ne 0) { throw 'R4-R8 guarded installation refused' }
        if ($DryRun) {
            & git status -sb
            Write-Output 'PHASE173_R4_R8_DRY_RUN=PASS'
            return
        }
        Write-Output 'PHASE173_R4_R8_FOCUSED_PYTEST_START'
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            'phase173_r4_r8_public_connection/tests/test_route.py' `
            'phase173_r4_r7r2_pi84_prior_selection/tests/test_context.py' `
            'phase173_r4_r7_source_first_rule/tests/test_rule.py' `
            'phase173_r4_r1_public_connection/tests/test_install.py'
        if ($LASTEXITCODE -ne 0) { throw 'R4-R8 scoped focused pytest failed' }
        Write-Output 'PHASE173_R4_R8_FOCUSED_PYTEST=PASS'
        & python -B -m phase173_r4_r8_public_connection.verify
        if ($LASTEXITCODE -ne 0) { throw 'Three normal public/Web proofs were not certified' }
        & python -B -m phase173_r4_r1_public_connection.verify
        if ($LASTEXITCODE -ne 0) { throw 'Existing pi_7^4 public proof regression failed' }
        Write-Output 'PHASE173_R4_R8_PI74_REGRESSION=PASS'
        & git status -sb
        & git diff --stat
        Write-Output 'PHASE173_R4_R8_RUN=PASS'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldEncoding
    $env:PYTHONUTF8 = $OldUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
