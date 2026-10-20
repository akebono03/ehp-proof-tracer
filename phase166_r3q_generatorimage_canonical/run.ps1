$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase166_r3q_generatorimage_canonical.apply
    if ($LASTEXITCODE -ne 0) { throw "R3-Q installation failed." }
    python -m pytest -q `
        .\phase166_r3q_generatorimage_canonical\test_phase166_r3q_generatorimage_canonical.py `
        .\phase166_r3d_pi32_regression\tests\test_phase166_r3d_pi32_regression.py
    if ($LASTEXITCODE -ne 0) {
        $backup = Get-ChildItem ".\phase166_r3q_generatorimage_canonical_backups" -Directory |
            Sort-Object Name -Descending | Select-Object -First 1
        if ($null -ne $backup) {
            Copy-Item (Join-Path $backup.FullName "phase166_r3p_position_binding.py") ".\phase166_r3p_position_binding.py" -Force
            Copy-Item (Join-Path $backup.FullName "phase165_r52_r9_shared_math.py") ".\phase165_r52_r9_shared_math.py" -Force
            Write-Host "RESTORED:" $backup.FullName
        }
        throw "R3-Q canonical source targeted regression failed; production files restored."
    }
    Write-Host "R3-Q canonical GeneratorImage 10 targeted tests PASS; full pytest NOT run."
} finally {
    Pop-Location
}
