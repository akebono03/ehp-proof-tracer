param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R20 git fetch failed' }
    & python -B -m phase174_r3_r7_r20_delta_image_evidence_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20 preflight failed' }
    $Tests = @(
        '.\phase174_r3_r7_r20_delta_image_evidence_audit\tests\test_audit.py',
        '.\phase174_r3_r7_r19_delta_generator_source_audit\tests\test_audit.py',
        '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py'
    )
    foreach ($TestFile in $Tests) {
        if (-not (Test-Path -LiteralPath $TestFile)) { throw "R20 missing test: $TestFile" }
        Write-Output "PHASE174_R3R7R20_TEST=$TestFile"
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider $TestFile
        if ($LASTEXITCODE -ne 0) { throw "R20 focused test failed: $TestFile" }
    }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R20_GATE=PASS_PREFLIGHT_ONLY'
    } else {
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r19_delta_generator_source_audit\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R20 public baseline failed' }
        & python -B -m phase174_r3_r7_r20_delta_image_evidence_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R20 public audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
