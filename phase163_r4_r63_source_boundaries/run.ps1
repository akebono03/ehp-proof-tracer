$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$inventory = Join-Path $root 'phase163_r4_r62_output\remaining_definitions.json'
if (-not (Test-Path -LiteralPath $inventory -PathType Leaf)) { throw "Missing R4-R62 input: $inventory" }
$required = @('Toda_01_corrected.tex', 'Toda_03_2(2).tex', 'Toda_05_2(6).tex')
$candidates = @(
    (Join-Path $root 'phase163_r4_r42_tex_extract\inputs'),
    $root
)
$texRoot = $null
foreach ($candidate in $candidates) {
    $allPresent = $true
    foreach ($sourceFile in $required) {
        if (-not (Test-Path -LiteralPath (Join-Path $candidate $sourceFile) -PathType Leaf)) {
            $allPresent = $false
            break
        }
    }
    if ($allPresent) { $texRoot = $candidate; break }
}
if ($null -eq $texRoot) {
    throw "Missing R4-R63 TeX sources. Expected all three files in phase163_r4_r42_tex_extract\inputs or project root: $($required -join ', ')"
}
Write-Output "R4-R63 TeX source root: $texRoot"
$env:EHP_R63_TEX_ROOT = $texRoot
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r63_source_boundaries\tests\test_phase163_r4_r63_source_boundaries.py'
if ($LASTEXITCODE -ne 0) { throw 'R4-R63 focused pytest failed.' }
python '.\phase163_r4_r63_source_boundaries\phase163_r4_r63_source_boundaries.py' --inventory $inventory --tex-root $texRoot --output '.\phase163_r4_r63_output'
if ($LASTEXITCODE -ne 0) { throw 'R4-R63 audit failed.' }
Write-Output 'R4-R63 source-span audit complete. No production changes. Full pytest not run.'
