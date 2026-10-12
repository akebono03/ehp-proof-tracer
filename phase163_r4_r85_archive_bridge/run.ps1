$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = $PSScriptRoot
$Registry = Join-Path $Root 'phase163_source_archive_registry.py'
$Replacement = Join-Path $Package 'phase163_source_archive_registry.py'
$NewBridge = Join-Path $Root 'phase163_r4_r85_archive_bridge.py'
$NewTest = Join-Path $Root 'tests\test_phase163_r4_r85_archive_bridge.py'
$BaselineHash = '4ae94ff465325f03c877e1b06b514cf125f5a6c77b19125f41a342e3bbbf70fb'
foreach ($required in @('phase163_r4_registry_bridge.py', 'unified_statement_registry.py', 'phase163_source_archive_catalog.json')) {
    if (-not (Test-Path (Join-Path $Root $required))) { throw "Missing $required" }
}
if (-not (Test-Path $Registry)) { throw 'R84 registry module missing.' }
$ExistingHash = (Get-FileHash $Registry -Algorithm SHA256).Hash.ToLowerInvariant()
$NewHash = (Get-FileHash $Replacement -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ExistingHash -ne $BaselineHash -and $ExistingHash -ne $NewHash) {
    throw 'R84 source registry differs from expected input; refusing overwrite.'
}
foreach ($pair in @(@($NewBridge, (Join-Path $Package 'phase163_r4_r85_archive_bridge.py')), @($NewTest, (Join-Path $Package 'tests\test_phase163_r4_r85_archive_bridge.py')))) {
    if (Test-Path $pair[0]) {
        if ((Get-FileHash $pair[0] -Algorithm SHA256).Hash -ne (Get-FileHash $pair[1] -Algorithm SHA256).Hash) {
            throw "Existing file differs: $($pair[0])"
        }
    }
}
if ($ExistingHash -eq $BaselineHash) {
    Copy-Item $Registry ($Registry + '.phase163_r85_before.py.bak') -Force
    Copy-Item $Replacement $Registry -Force
}
New-Item -Path (Join-Path $Root 'tests') -ItemType Directory -Force | Out-Null
Copy-Item (Join-Path $Package 'phase163_r4_r85_archive_bridge.py') $NewBridge -Force
Copy-Item (Join-Path $Package 'tests\test_phase163_r4_r85_archive_bridge.py') $NewTest -Force
python -m pytest -q tests/test_phase163_r4_r85_archive_bridge.py tests/test_phase163_r4_r84_source_archive_origin.py tests/test_phase163_r4_r83_source_archive_registry.py tests/test_phase163_r4_registry_bridge.py
if ($LASTEXITCODE -ne 0) { throw 'R85 focused tests failed. Check R85 backup.' }
python -c "import json; from phase163_r4_r85_archive_bridge import build_registry_bridge_with_source_archive; b=build_registry_bridge_with_source_archive(); print(json.dumps({'phase':'163 R4-R85','archive_records':len(b.records_for('source_archive')),'archive_proof_links':sum(link.assertion_id in {r.assertion_id for r in b.records_for('source_archive')} for link in b.proof_links),'proof_search_connected':False,'full_suite_run':False}, ensure_ascii=False, indent=2))"
if ($LASTEXITCODE -ne 0) { throw 'R85 audit failed.' }
Write-Host 'R85 explicit archival bridge verified. Full pytest not run.'
