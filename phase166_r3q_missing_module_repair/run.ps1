$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$source = Join-Path $PSScriptRoot "phase166_r3q_hopf_image_relation.py"
$target = Join-Path $root "phase166_r3q_hopf_image_relation.py"
Push-Location $root
try {
    if (Test-Path $target) {
        $oldHash = (Get-FileHash -Algorithm SHA256 $target).Hash
        $newHash = (Get-FileHash -Algorithm SHA256 $source).Hash
        if ($oldHash -ne $newHash) {
            throw "Existing module differs; refusing to overwrite: $target"
        }
        Write-Host "ALREADY_PRESENT:" $target
    } else {
        Copy-Item $source $target
        Write-Host "INSTALLED:" $target
    }
    python -c "import phase166_r3q_hopf_image_relation as x; print('IMPORT_OK:', x.__file__)"
    if ($LASTEXITCODE -ne 0) { throw "Required module import failed" }
    python -m pytest -q `
        .\phase166_r3q_generatorimage_canonical\test_phase166_r3q_generatorimage_canonical.py `
        .\phase166_r3d_pi32_regression\tests\test_phase166_r3d_pi32_regression.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Targeted pytest failed. Inspect output before any further changes."
        throw "R3-Q repair tests failed"
    }
    Write-Host "R3-Q missing module repaired; full pytest NOT run."
} finally {
    Pop-Location
}
