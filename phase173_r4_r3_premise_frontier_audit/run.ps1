param([switch]$DryRun, [int]$TimeoutSeconds = 240, [switch]$SkipRemoteCheck)
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
        Write-Output 'PHASE173_R4_R3_FOCUSED_PYTEST_START'
        & python -B -m pytest -q -p no:cacheprovider `
            'phase173_r4_r3_premise_frontier_audit/tests/test_audit.py' `
            'phase173_r4_r1_source_bound_56/tests/test_rule.py' `
            'phase170_r3_r7_toda52_ordered_db_transport/tests/test_ordered_db_toda52.py'
        if ($LASTEXITCODE -ne 0) { throw 'R4-R3 focused pytest failed' }
        Write-Output 'PHASE173_R4_R3_FOCUSED_PYTEST=PASS'
        $PythonArgs = @('-B','-m','phase173_r4_r3_premise_frontier_audit.audit',
                        '--root',$Root,'--timeout',[string]$TimeoutSeconds)
        if ($DryRun) { $PythonArgs += '--dry-run' }
        if ($SkipRemoteCheck) { $PythonArgs += '--skip-remote-check' }
        & python @PythonArgs
        if ($LASTEXITCODE -ne 0) { throw 'R4-R3 prerequisite audit requires investigation' }
        & git status -sb
        Write-Output 'PHASE173_R4_R3_AUDIT=PASS'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldEncoding
    $env:PYTHONUTF8 = $OldUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
