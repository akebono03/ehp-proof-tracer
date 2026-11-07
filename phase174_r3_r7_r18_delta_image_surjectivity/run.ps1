param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$SavedPythonPath = $env:PYTHONPATH
$SavedNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R18 git fetch failed' }

    & python -B -m phase174_r3_r7_r18_delta_image_surjectivity.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R18 source-first DryRun failed' }

    $Groups = @(
        @{ Name = 'R18_MATH_RULE'; Paths = @(
            '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py'
        ) },
        @{ Name = 'R18_AUDIT_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_audit.py'
        ) },
        @{ Name = 'R3_EHP_ROOT'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py'
        ) },
        @{ Name = 'R17_PUBLIC_DISPLAY'; Paths = @(
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_public.py'
        ) },
        @{ Name = 'EXISTING_DELTA_IMAGE'; Paths = @(
            '.\phase165_r57_r19_delta_image_backward\test_phase165_r57_r19_delta_image_backward.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($Path in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $Path)) {
                throw "Missing reviewed test: $Path"
            }
        }
        Write-Output "PHASE174_R3R7R18_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "R18 focused pytest failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R18_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R18_GATE=PASS_PREFLIGHT'
    }
    else {
        Write-Output 'PHASE174_R3R7R18_PYTEST_GROUP=PUBLIC_FRONTIER'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_public_frontier.py'
        if ($LASTEXITCODE -ne 0) { throw 'R18 focused public frontier test failed' }

        & python -B -m phase174_r3_r7_r18_delta_image_surjectivity.audit
        if ($LASTEXITCODE -ne 0) { throw 'R18 isolated delta source-first audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $SavedPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $SavedNoBytecode
    Pop-Location
}
