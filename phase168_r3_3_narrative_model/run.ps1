$ErrorActionPreference = 'Stop'
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $bundle
Push-Location $root
try {
    $target = Join-Path $root 'phase168_r3_3_proof_narrative_model.py'
    if (Test-Path $target) {
        if ((Get-FileHash $target -Algorithm SHA256).Hash -ne (Get-FileHash (Join-Path $bundle 'phase168_r3_3_proof_narrative_model.py') -Algorithm SHA256).Hash) {
            throw 'Existing production target differs; refusing overwrite'
        }
    } else {
        Copy-Item (Join-Path $bundle 'phase168_r3_3_proof_narrative_model.py') $target
    }
    python -m pytest -q (Join-Path $bundle 'tests\test_phase168_r3_3_proof_narrative_model.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-3 focused pytest failed' }
    Write-Host 'R3-3 model installed. Existing files unchanged. Full suite not run.'
} finally {
    Pop-Location
}
