$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Renderer = Join-Path $Repo 'phase168_r3_5_model_renderer.py'
$TestFile = Join-Path $Repo 'phase168_r3_26a_after_r3_25a\tests\test_phase168_r3_26_projection.py'
$RendererBackup = Join-Path $Package 'output\phase168_r3_5_model_renderer.py.before'
$TestBackup = Join-Path $Package 'output\test_phase168_r3_26_projection.py.before'
$Patched = $false

Push-Location $Repo
try {
    python (Join-Path $Package 'install.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-41J2 guarded installer failed' }
    $Patched = $true

    python -m pytest -q --import-mode=importlib `
      '.\phase168_r3_41j2_chain_test_scope_fix\tests\test_phase168_r3_41j2_citation_provenance.py' `
      '.\phase168_r3_41i_renderer_closure_audit\tests\test_audit.py' `
      '.\phase168_r3_26a_after_r3_25a\tests\test_phase168_r3_26_projection.py' `
      '.\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-41J2 limited pytest failed' }

    python -m phase168_r3_41j2_chain_test_scope_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41J2 citation quality audit failed' }

    Write-Host 'R3-41J2 limited citation repair complete. Full pytest NOT run.'
    Write-Host "UPLOAD_BUNDLE $(Join-Path $Package 'output\review_bundle.zip')"
    Write-Host "FULL_FUNCTION $(Join-Path $Package 'modified_function_full.py')"
    Write-Host "FULL_TEST_FUNCTION $(Join-Path $Package 'modified_test_function_full.py')"
    $Patched = $false
}
finally {
    if ($Patched) {
        if (-not (Test-Path -LiteralPath $RendererBackup) -or -not (Test-Path -LiteralPath $TestBackup)) {
            throw 'ROLLBACK BLOCKED: one of the two backups is missing'
        }
        Copy-Item -LiteralPath $RendererBackup -Destination $Renderer -Force
        Copy-Item -LiteralPath $TestBackup -Destination $TestFile -Force
        $RendererActual = (Get-FileHash -LiteralPath $Renderer -Algorithm SHA256).Hash
        $RendererExpected = (Get-FileHash -LiteralPath $RendererBackup -Algorithm SHA256).Hash
        $TestActual = (Get-FileHash -LiteralPath $TestFile -Algorithm SHA256).Hash
        $TestExpected = (Get-FileHash -LiteralPath $TestBackup -Algorithm SHA256).Hash
        if ($RendererActual -ne $RendererExpected -or $TestActual -ne $TestExpected) {
            throw 'ROLLBACK VERIFICATION FAILED: source or test differs from backup'
        }
        Write-Host 'ROLLBACK VERIFIED: Renderer and R3-26a test restored byte-for-byte'
    }
    Pop-Location
}
