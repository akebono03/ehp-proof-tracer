$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
Set-Location $project
$decisions = Join-Path $project 'phase163_r4_r66_output\boundary_decisions.json'
$context = Join-Path $project 'phase163_r4_r67_output\context_review.json'
if (-not (Test-Path -LiteralPath $decisions -PathType Leaf)) { throw "Missing R66 results: $decisions" }
if (-not (Test-Path -LiteralPath $context -PathType Leaf)) { throw "Missing R67 results: $context" }
$env:PYTHONPATH = "$PSScriptRoot;$project"
python -m pytest -q '.\phase163_r4_r68_unnumbered_reference\tests\test_phase163_r4_r68_unnumbered_reference.py'
if ($LASTEXITCODE -ne 0) { throw 'R68 focused pytest failed' }
python '.\phase163_r4_r68_unnumbered_reference\phase163_r4_r68_unnumbered_reference.py' --decisions $decisions --context $context --output '.\phase163_r4_r68_output'
if ($LASTEXITCODE -ne 0) { throw 'R68 proposal generation failed' }
Write-Output 'R68 read-only proposals generated. Full pytest not run.'
