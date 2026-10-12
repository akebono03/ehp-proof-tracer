$ErrorActionPreference = "Stop"
$project = Split-Path -Parent $PSScriptRoot
Set-Location $project
$required = @('Toda_01_corrected.tex', 'Toda_03_2(2).tex', 'Toda_05_2(6).tex')
$candidates = @( (Join-Path $project 'phase163_r4_r42_tex_extract\inputs'), $project )
$texRoot = $null
foreach ($candidate in $candidates) {
    $present = $true
    foreach ($name in $required) {
        if (-not (Test-Path -LiteralPath (Join-Path $candidate $name) -PathType Leaf)) { $present = $false; break }
    }
    if ($present) { $texRoot = $candidate; break }
}
if ($null -eq $texRoot) { throw 'Missing R4-R63 TeX sources in R42 inputs or project root.' }
$env:EHP_R67_TEX_ROOT = $texRoot
$env:PYTHONPATH = "$PSScriptRoot;$project"
python -m pytest -q .\phase163_r4_r67_context_expansion\tests\test_phase163_r4_r67_context_expansion.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python .\phase163_r4_r67_context_expansion\phase163_r4_r67_context_expansion.py --decisions .\phase163_r4_r66_output\boundary_decisions.json --tex-root $texRoot --output .\phase163_r4_r67_output
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
