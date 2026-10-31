param(
    [switch]$DryRun,
    [switch]$Quick
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE
Push-Location $Root
try {
    $Branch = (& git branch --show-current).Trim()
    $Head = (& git rev-parse HEAD).Trim()
    Write-Host ('PHASE171_R20R2R3_BRANCH=' + $Branch)
    Write-Host ('PHASE171_R20R2R3_HEAD=' + $Head)
    if ($Branch -ne 'develop') {
        throw 'Expected develop branch. No files were changed.'
    }
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '.\phase171_r20r2r3_canonical_test_runner\anchored_pytest.py')
    if ($DryRun) { $Arguments += '--dry-run' }
    if ($Quick) { $Arguments += '--quick' }
    & python @Arguments
    $PythonExit = $LASTEXITCODE
    if ($PythonExit -ne 0) {
        throw ('R20R2R3 check failed with exit code ' + $PythonExit)
    }
    if (-not $DryRun) {
        Write-Host 'PHASE171_R20R2R3_RESULT=PASS'
        & git status -sb
        & git diff --stat
    }
} finally {
    if ($null -eq $PreviousNoBytecode) {
        Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue
    } else {
        $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    }
    Pop-Location
}
