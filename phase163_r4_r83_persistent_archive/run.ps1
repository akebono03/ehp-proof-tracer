$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = $PSScriptRoot
$SourcePath = Join-Path $ProjectRoot 'phase163_source_archive_registry.py'
$CatalogPath = Join-Path $ProjectRoot 'phase163_source_archive_catalog.json'
$TestPath = Join-Path $ProjectRoot 'tests\test_phase163_r4_r83_source_archive_registry.py'
foreach ($required in @('unified_statement_registry.py', 'phase163_r4_registry_bridge.py', 'toda_literature_statement_boundary.py', 'theorem_facts.py')) {
    if (-not (Test-Path (Join-Path $ProjectRoot $required))) { throw "Missing project file: $required" }
}
New-Item -Path (Join-Path $ProjectRoot 'tests') -ItemType Directory -Force | Out-Null
foreach ($pair in @(@('phase163_source_archive_registry.py', $SourcePath), @('phase163_source_archive_catalog.json', $CatalogPath), @('tests\test_phase163_r4_r83_source_archive_registry.py', $TestPath))) {
    if (Test-Path $pair[1]) {
        $existing = (Get-FileHash -Path $pair[1] -Algorithm SHA256).Hash
        $incoming = (Get-FileHash -Path (Join-Path $PackageRoot $pair[0]) -Algorithm SHA256).Hash
        if ($existing -ne $incoming) { throw "Refusing to overwrite different existing file: $($pair[1])" }
    } else {
        Copy-Item -Path (Join-Path $PackageRoot $pair[0]) -Destination $pair[1]
    }
}
python -m pytest -q tests/test_phase163_r4_r83_source_archive_registry.py
if ($LASTEXITCODE -ne 0) { throw 'R83 focused pytest failed.' }
python -c "import json; from phase163_source_archive_registry import build_registry_with_source_archive; registry, result = build_registry_with_source_archive(); print(json.dumps(result, ensure_ascii=False, indent=2))"
if ($LASTEXITCODE -ne 0) { throw 'R83 registry integration failed.' }
Write-Host 'R83 opt-in source archive registered in project source. Full pytest not run.'
