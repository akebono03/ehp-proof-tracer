$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = $PSScriptRoot
$Catalog = Join-Path $Root 'phase163_source_archive_catalog.json'
$Source = Join-Path $Package 'phase163_r4_r86_claim_boundary.py'
$Dest = Join-Path $Root 'phase163_r4_r86_claim_boundary.py'
$TestSource = Join-Path $Package 'tests\test_phase163_r4_r86_claim_boundary.py'
$TestDest = Join-Path $Root 'tests\test_phase163_r4_r86_claim_boundary.py'
if (-not (Test-Path $Catalog)) { throw 'R83 source archive catalog is missing.' }
if ((Get-FileHash $Catalog -Algorithm SHA256).Hash -ne (Get-FileHash (Join-Path $Package 'phase163_source_archive_catalog.json') -Algorithm SHA256).Hash) {
    throw 'Source archive differs from inspected R83 catalog; refusing registration.'
}
foreach ($Pair in @(@($Dest, $Source), @($TestDest, $TestSource))) {
    if (Test-Path $Pair[0]) {
        if ((Get-FileHash $Pair[0] -Algorithm SHA256).Hash -ne (Get-FileHash $Pair[1] -Algorithm SHA256).Hash) {
            throw "Existing file differs: $($Pair[0])"
        }
    }
}
New-Item -Path (Join-Path $Root 'tests') -ItemType Directory -Force | Out-Null
Copy-Item $Source $Dest -Force
Copy-Item $TestSource $TestDest -Force
python -m pytest -q tests/test_phase163_r4_r86_claim_boundary.py
if ($LASTEXITCODE -ne 0) { throw 'R86 focused pytest failed.' }
python phase163_r4_r86_claim_boundary.py --catalog $Catalog --output (Join-Path $Root 'phase163_r4_r86_output')
if ($LASTEXITCODE -ne 0) { throw 'R86 catalog generation failed.' }
Write-Host 'R86 review units persisted. Full pytest not run.'
