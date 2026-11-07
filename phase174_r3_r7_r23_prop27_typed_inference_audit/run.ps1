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
    if ($LASTEXITCODE -ne 0) { throw 'R23 git fetch failed' }

    & python -B -m phase174_r3_r7_r23_prop27_typed_inference_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R23 source guard failed' }

    $Groups = @(
        @{ Name = 'R23_SOURCE_AND_LINEAGE'; Path = '.\phase174_r3_r7_r23_prop27_typed_inference_audit\tests\test_audit.py' },
        @{ Name = 'EXISTING_PROP27_SEMANTICS'; Path = '.\tests\test_phase50_prop27_theorem_semantics.py' },
        @{ Name = 'R22_SOURCE_BASELINE'; Path = '.\phase174_r3_r7_r22_typed_hopf_delta_boundary_audit\tests\test_audit.py' },
        @{ Name = 'R18_DELTA_IMAGE_RULE'; Path = '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py' }
    )

    foreach ($Group in $Groups) {
        if (-not (Test-Path -LiteralPath $Group.Path)) {
            throw "R23 required test missing: $($Group.Path)"
        }
        Write-Output "PHASE174_R3R7R23_PYTEST_GROUP=$($Group.Name)"
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw "R23 pytest failed: $($Group.Name)" }
    }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R23_GATE=PASS_PREFLIGHT_ONLY'
    }
    else {
        Write-Output 'PHASE174_R3R7R23_PYTEST_GROUP=PUBLIC_SOURCE_FRONTIER'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r23_prop27_typed_inference_audit\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R23 public frontier test failed' }
        & python -B -m phase174_r3_r7_r23_prop27_typed_inference_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R23 live audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
