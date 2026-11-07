param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R19 git fetch failed' }

    & python -B -m phase174_r3_r7_r19_delta_generator_source_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R19 source-first preflight failed' }

    $Groups = @(
        @{ Name = 'R19_SOURCE_AND_GIT_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r19_delta_generator_source_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R18_MATH_RULE'; Paths = @(
            '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py'
        ) },
        @{ Name = 'R18_PUBLIC_BASELINE'; Paths = @(
            '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_public_frontier.py'
        ) },
        @{ Name = 'EXISTING_DELTA_IMAGE'; Paths = @(
            '.\phase165_r57_r19_delta_image_backward\test_phase165_r57_r19_delta_image_backward.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($Path in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $Path)) {
                throw "R19 required reviewed test missing: $Path"
            }
        }
        Write-Output "PHASE174_R3R7R19_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "R19 focused pytest failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R19_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R19_GATE=PASS_PREFLIGHT_ONLY'
    }
    else {
        Write-Output 'PHASE174_R3R7R19_PYTEST_GROUP=PUBLIC_SOURCE_FRONTIER'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r19_delta_generator_source_audit\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R19 public frontier pytest failed' }

        & python -B -m phase174_r3_r7_r19_delta_generator_source_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R19 live source-first audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
