param(
    [switch]$DryRun,
    [ValidateRange(1, 7200)][int]$TimeoutSeconds = 300
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldPythonEncoding = $env:PYTHONIOENCODING
$OldPythonUtf8 = $env:PYTHONUTF8
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    $env:PYTHONPATH = "$RepoRoot;$OldPythonPath"
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location $RepoRoot
    try {
        Write-Output 'PHASE175_R3R5_GIT_STATUS_BEFORE'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R3R5 git status failed' }

        & python -B -m pytest -q --disable-warnings -p no:cacheprovider -o addopts= `
            --import-mode=importlib `
            '.\phase175_r3r5_pi73_lemma57_frontier\tests\test_source.py' `
            '.\phase175_r3r5_pi73_lemma57_frontier\tests\test_audit.py' `
            '.\phase175_r3r5_pi73_lemma57_frontier\tests\test_frontier.py' `
            '.\phase175_r3_pi73_hopf_lift\tests\test_audit.py' `
            '.\phase175_r3_pi73_hopf_lift\tests\test_rule.py' `
            '.\phase175_r3_pi73_hopf_lift\tests\test_frontier.py' `
            '.\phase175_r2_k4_frontier_audit\tests\test_audit.py' `
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3R5 focused pytest failed' }
        Write-Output 'PHASE175_R3R5_FOCUSED_PYTEST=PASS'

        $Arguments = @(
            '-B', '-m', 'phase175_r3r5_pi73_lemma57_frontier.audit',
            '--root', $RepoRoot, '--timeout-seconds', [string]$TimeoutSeconds
        )
        if ($DryRun) { $Arguments += '--dry-run' }
        & python @Arguments
        $AuditExit = $LASTEXITCODE
        Write-Output 'PHASE175_R3R5_GIT_STATUS_AFTER'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R3R5 git status after failed' }
        if ($AuditExit -ne 0) { throw "R3R5 audit failed: $AuditExit" }
        Write-Output 'PHASE175_R3R5=PASS'
        Write-Output '(END)'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldPythonEncoding
    $env:PYTHONUTF8 = $OldPythonUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
