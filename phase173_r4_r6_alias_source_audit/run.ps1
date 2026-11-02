param([switch]$DryRun, [switch]$SkipRemoteCheck)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldEncoding = $env:PYTHONIOENCODING
$OldUtf8 = $env:PYTHONUTF8
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    $env:PYTHONPATH = "$Root;$OldPythonPath"
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location $Root
    try {
        Write-Output 'PHASE173_R4_R6_FOCUSED_PYTEST_START'
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            'phase173_r4_r6_alias_source_audit/tests/test_audit.py' `
            'phase173_r4_r5_blocker_diagnostic/tests/test_audit.py' `
            'phase173_r4_r4_typed_generator_audit/tests/test_audit.py' `
            'phase173_r4_r1_lemma54_source_bridge/tests/test_source.py'
        if ($LASTEXITCODE -ne 0) { throw 'R4-R6 focused pytest failed' }
        Write-Output 'PHASE173_R4_R6_FOCUSED_PYTEST=PASS'
        $Args = @('-B', '-m', 'phase173_r4_r6_alias_source_audit.audit', '--root', $Root)
        if ($DryRun) { $Args += '--dry-run' }
        if ($SkipRemoteCheck) { $Args += '--skip-remote-check' }
        & python @Args
        if ($LASTEXITCODE -ne 0) { throw 'R4-R6 audit failed' }
        if (-not $DryRun) {
            & python -B -m phase173_r4_r1_public_connection.verify
            if ($LASTEXITCODE -ne 0) { throw 'Existing pi_7^4 public regression failed' }
            Write-Output 'PHASE173_R4_R6_PI74_REGRESSION=PASS'
        }
        & git status -sb
        Write-Output 'PHASE173_R4_R6_AUDIT=PASS'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldEncoding
    $env:PYTHONUTF8 = $OldUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
}
