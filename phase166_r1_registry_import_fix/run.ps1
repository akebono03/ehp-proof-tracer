$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$original = Join-Path $root 'phase166_r1_source_registry_audit'
$target = Join-Path $original 'audit.py'
$registry = Join-Path $root 'phase165_r4_production_connection.py'
Push-Location $root
try {
    if (-not (Test-Path $original)) { throw "Original R1 audit folder missing: $original" }
    if (-not (Test-Path $target)) { throw "Original audit.py missing: $target" }
    if (-not (Test-Path $registry)) {
        Write-Host 'BLOCKED: phase165_r4_production_connection.py is not at the project root.'
        Write-Host 'Potential copies (do not install archived copies automatically):'
        Get-ChildItem -Path $root -Filter phase165_r4_production_connection.py -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 20 -ExpandProperty FullName
        throw 'R1 registry audit cannot proceed until the current production module is available.'
    }
    $backup = Join-Path $original 'audit.py.phase166_r1_before_import_fix.bak'
    if (-not (Test-Path $backup)) { Copy-Item $target $backup }
    Copy-Item (Join-Path $package 'audit.py') $target -Force
    $env:PYTHONPATH = "$root;$original"
    python -c "import phase165_r4_production_connection; print('Production registry module import: PASS')"
    if ($LASTEXITCODE -ne 0) { throw 'Production module import failed. Inspect traceback; no fabricated fallback.' }
    python $target
    if ($LASTEXITCODE -ne 0) { throw 'R1 registry candidate matching failed (fail closed).' }
    python -m pytest -q (Join-Path $original 'test_audit.py') (Join-Path $package 'test_fix.py')
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
    Write-Host 'R1 registry audit PASS. Production code unchanged; full pytest NOT run.'
} finally {
    Pop-Location
}
