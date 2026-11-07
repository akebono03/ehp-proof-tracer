param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R21 git fetch failed' }

    & python -B -m phase174_r3_r7_r21_delta_hopf_chain_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R21 source preflight failed' }

    $Groups = @(
        @{ Name = 'R21_SOURCE_CONTRACT'; Path = '.\phase174_r3_r7_r21_delta_hopf_chain_audit\tests\test_audit.py' },
        @{ Name = 'R20_SOURCE_CONTRACT'; Path = '.\phase174_r3_r7_r20_delta_image_evidence_audit\tests\test_audit.py' },
        @{ Name = 'R19_SOURCE_CONTRACT'; Path = '.\phase174_r3_r7_r19_delta_generator_source_audit\tests\test_audit.py' },
        @{ Name = 'R18_MATH_RULE'; Path = '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py' }
    )
    foreach ($Group in $Groups) {
        if (-not (Test-Path -LiteralPath $Group.Path)) {
            throw "R21 related test missing: $($Group.Path)"
        }
        Write-Output "PHASE174_R3R7R21_PYTEST_GROUP=$($Group.Name)"
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw "R21 focused pytest failed: $($Group.Name)" }
    }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R21_GATE=PASS_PREFLIGHT_ONLY'
    }
    else {
        Write-Output 'PHASE174_R3R7R21_PYTEST_GROUP=PUBLIC_FRONTIER'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r21_delta_hopf_chain_audit\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R21 public regression failed' }
        & python -B -m phase174_r3_r7_r21_delta_hopf_chain_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R21 live audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    Pop-Location
}
