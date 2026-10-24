$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Renderer = Join-Path $Repo 'phase168_r3_5_model_renderer.py'
$Backup = Join-Path $Package 'output\phase168_r3_5_model_renderer.py.before'
$Modified = $false

Push-Location $Repo
try {
    python (Join-Path $Package 'install.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-41L guarded installer failed' }
    $Modified = $true

    python -m pytest -q --import-mode=importlib `
      '.\phase168_r3_41l_reasoned_prose\tests\test_installer_guard.py' `
      '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py' `
      '.\phase168_r3_41j2_chain_test_scope_fix\tests\test_phase168_r3_41j2_citation_provenance.py' `
      '.\phase168_r3_41i_renderer_closure_audit\tests\test_audit.py' `
      '.\phase168_r3_26a_after_r3_25a\tests\test_phase168_r3_26_projection.py' `
      '.\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-41L focused pytest failed' }

    python -m phase168_r3_41l_reasoned_prose.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41L frozen-reference quality audit failed' }

    Write-Host 'R3-41L focused renderer prose repair complete. Full pytest NOT run.'
    Write-Host "UPLOAD_BUNDLE $(Join-Path $Package 'output\review_bundle.zip')"
    Write-Host "FULL_FUNCTION $(Join-Path $Package 'modified_function_full.py')"
    $Modified = $false
}
finally {
    if ($Modified) {
        if (-not (Test-Path -LiteralPath $Backup)) {
            throw 'ROLLBACK BLOCKED: original renderer backup missing'
        }
        Copy-Item -LiteralPath $Backup -Destination $Renderer -Force
        $Expected = (Get-FileHash -LiteralPath $Backup -Algorithm SHA256).Hash
        $Actual = (Get-FileHash -LiteralPath $Renderer -Algorithm SHA256).Hash
        if ($Expected -ne $Actual) { throw 'ROLLBACK VERIFICATION FAILED' }
        Write-Host 'ROLLBACK VERIFIED: Renderer restored byte-for-byte'
    }
    Pop-Location
}
