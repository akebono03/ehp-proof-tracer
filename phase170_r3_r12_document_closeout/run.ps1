param([switch]$DryRun)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OriginalPythonPath = $env:PYTHONPATH
$OriginalPythonEncoding = $env:PYTHONIOENCODING
$OriginalUtf8 = $env:PYTHONUTF8
$OriginalBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    $env:PYTHONPATH = "$RepoRoot;$OriginalPythonPath"
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location $RepoRoot
    try {
        if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
            throw 'python not found'
        }
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
            throw 'git not found'
        }
        & python -B -m pytest -q -p no:cacheprovider `
            '.\phase170_r3_r12_document_closeout\tests\test_document_contract.py'
        if ($LASTEXITCODE -ne 0) {
            throw "R3-R12 focused document tests failed: $LASTEXITCODE"
        }
        Write-Output 'PHASE170_R3R12_FOCUSED_PYTEST=PASS'

        $Output = Join-Path $PSScriptRoot 'output'
        if ($DryRun) {
            & python -B '.\phase170_r3_r12_document_closeout\update_docs.py' `
                --root $RepoRoot --output $Output
        } else {
            & python -B '.\phase170_r3_r12_document_closeout\update_docs.py' `
                --root $RepoRoot --output $Output --apply
        }
        $ExitCode = $LASTEXITCODE
        if ($ExitCode -ne 0) {
            throw "R3-R12 full-document generation refused, exit $ExitCode"
        }
        if (-not $DryRun) {
            & git diff --check
            if ($LASTEXITCODE -ne 0) { throw 'R3-R12 document diff whitespace check failed' }
            Write-Output 'PHASE170_R3R12_DIFF_CHECK=PASS'
        }
        & git status -sb
        Write-Output 'PHASE170_R3R12=PASS'
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $OriginalPythonPath
    $env:PYTHONIOENCODING = $OriginalPythonEncoding
    $env:PYTHONUTF8 = $OriginalUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OriginalBytecode
}
