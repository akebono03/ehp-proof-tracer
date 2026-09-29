$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$ImplDir = Join-Path $ProjectRoot "phase144_2_sigma_triple_prime_definition_impl"

$env:PYTHONPATH = $ProjectRoot

try {
    python (Join-Path $ImplDir "install_and_apply_phase144_2.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Apply failed with exit code $LASTEXITCODE"
    }

    Write-Host ""
    Write-Host ("=" * 78)
    Write-Host "Focused pytest"
    Write-Host ("=" * 78)

    pytest -q ".\tests\test_phase144_2_sigma_triple_prime_definition.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Focused pytest failed with exit code $LASTEXITCODE"
    }

    Write-Host ""
    python (Join-Path $ImplDir "audit_phase144_2_after_impl.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Post-implementation audit failed with exit code $LASTEXITCODE"
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
