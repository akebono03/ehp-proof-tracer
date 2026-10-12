$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root

$SourceGoal = Join-Path $PSScriptRoot 'phase165_goal_only_search.py'
$SourceWiring = Join-Path $PSScriptRoot 'phase165_r9_production_wiring.py'
$SourceTest = Join-Path $PSScriptRoot 'tests/test_phase165_r9_production_wiring.py'
$SourceAudit = Join-Path $PSScriptRoot 'audit.py'
$TargetGoal = Join-Path $Root 'phase165_goal_only_search.py'
$TargetWiring = Join-Path $Root 'phase165_r9_production_wiring.py'
$TargetTest = Join-Path $Root 'tests/test_phase165_r9_production_wiring.py'

foreach ($required in @(
    $SourceGoal, $SourceWiring, $SourceTest, $SourceAudit, $TargetGoal,
    (Join-Path $Root 'phase165_r3_recursive_search.py'),
    (Join-Path $Root 'phase165_r8_rule_provider.py'),
    (Join-Path $Root 'phase165_r4_production_connection.py'),
    (Join-Path $Root 'tests/test_phase165_r3_recursive_search.py')
)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Required file missing: $required"
    }
}

Copy-Item -LiteralPath $TargetGoal -Destination "$TargetGoal.phase165_r9_backup" -Force
Copy-Item -LiteralPath $SourceGoal -Destination $TargetGoal -Force
Copy-Item -LiteralPath $SourceWiring -Destination $TargetWiring -Force
Copy-Item -LiteralPath $SourceTest -Destination $TargetTest -Force

python -m py_compile 'phase165_goal_only_search.py' 'phase165_r9_production_wiring.py' 'tests/test_phase165_r9_production_wiring.py'
if ($LASTEXITCODE -ne 0) { throw 'R9 syntax validation failed' }
python -m pytest -q 'tests/test_phase165_r9_production_wiring.py' 'tests/test_phase165_r3_recursive_search.py'
if ($LASTEXITCODE -ne 0) { throw 'R9 focused tests failed' }

$PreviousPythonPath = $env:PYTHONPATH
try {
    if ([string]::IsNullOrEmpty($PreviousPythonPath)) {
        $env:PYTHONPATH = $Root
    } else {
        $env:PYTHONPATH = "$Root$([IO.Path]::PathSeparator)$PreviousPythonPath"
    }
    python $SourceAudit
    if ($LASTEXITCODE -ne 0) { throw 'R9 live audit failed' }
} finally {
    $env:PYTHONPATH = $PreviousPythonPath
}
Write-Host 'R9 live production wiring installed; no source assertions promoted. Full pytest NOT run.'
