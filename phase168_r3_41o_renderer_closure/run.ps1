$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Renderer = Join-Path $Repo 'phase168_r3_5_model_renderer.py'
$RendererBackup = Join-Path $Package 'output\phase168_r3_5_model_renderer.py.before'
$NTest = Join-Path $Repo 'phase168_r3_41n1_import_scope_fix\tests\test_phase168_r3_41n_composed_proof_display.py'
$NTestBackup = Join-Path $Package 'output\test_phase168_r3_41n_composed_proof_display.py.before'
$Patched = $false
Push-Location $Repo
try {
    python (Join-Path $Package 'install.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-41O installer failed' }
    $Patched = $true
    python -m pytest -q --import-mode=importlib `
      '.\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py' `
      '.\phase168_r3_41n1_import_scope_fix\tests\test_phase168_r3_41n_composed_proof_display.py' `
      '.\phase168_r3_41n1_import_scope_fix\tests\test_phase168_r3_41n1_import_scope.py' `
      '.\phase168_r3_41m2_registry_locator_fix\tests\test_phase168_r3_41m2_registry_locator_fix.py' `
      '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py' `
      '.\phase168_r3_41j2_chain_test_scope_fix\tests\test_phase168_r3_41j2_citation_provenance.py' `
      '.\phase168_r3_41i_renderer_closure_audit\tests\test_audit.py' `
      '.\phase168_r3_26a_after_r3_25a\tests\test_phase168_r3_26_projection.py' `
      '.\phase168_r3_10_registered_alias\tests\test_phase168_r3_10_registered_alias.py' `
      '.\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-41O focused pytest failed' }
    python -m phase168_r3_41o_renderer_closure.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41O fulltext audit failed' }
    Write-Host 'R3-41O focused validation complete; full pytest NOT run.'
    Write-Host "UPLOAD_BUNDLE $(Join-Path $Package 'output\review_bundle.zip')"
    $Patched = $false
}
finally {
    if ($Patched) {
        foreach ($Pair in @(@($Renderer, $RendererBackup), @($NTest, $NTestBackup))) {
            $Target = $Pair[0]
            $Backup = $Pair[1]
            if (-not (Test-Path -LiteralPath $Backup)) { throw "Missing backup: $Backup" }
            Copy-Item -LiteralPath $Backup -Destination $Target -Force
            $Want = (Get-FileHash -LiteralPath $Backup -Algorithm SHA256).Hash
            $Got = (Get-FileHash -LiteralPath $Target -Algorithm SHA256).Hash
            if ($Want -ne $Got) { throw "Rollback verification failed: $Target" }
        }
        Write-Host 'RESTORED renderer and related test byte-for-byte'
    }
    Pop-Location
}
