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
        Write-Output 'PHASE173_R4_R7R1_FOCUSED_PYTEST_START'
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            'phase173_r4_r7r1_pi84_premise_diagnostic/tests/test_audit.py' `
            'phase173_r4_r7_source_first_rule/tests/test_rule.py' `
            'phase173_r4_r1_source_bound_56/tests/test_rule.py'
        if ($LASTEXITCODE -ne 0) { throw 'R4-R7R1 focused pytest failed' }
        Write-Output 'PHASE173_R4_R7R1_FOCUSED_PYTEST=PASS'
        $ArgsList = @('-B', '-m', 'phase173_r4_r7r1_pi84_premise_diagnostic.audit',
                      '--root', $Root)
        if ($DryRun) { $ArgsList += '--dry-run' }
        if ($SkipRemoteCheck) { $ArgsList += '--skip-remote-check' }
        & python @ArgsList
        if ($LASTEXITCODE -ne 0) { throw 'R4-R7R1 diagnostic failed' }
        if (-not $DryRun) {
            & python -B -m phase173_r4_r1_public_connection.verify
            if ($LASTEXITCODE -ne 0) { throw 'pi_7^4 public proof regression failed' }
            Write-Output 'PHASE173_R4_R7R1_PI74_REGRESSION=PASS'
        }
        & git status -sb
        Write-Output 'PHASE173_R4_R7R1_RUN=PASS'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldEncoding
    $env:PYTHONUTF8 = $OldUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
