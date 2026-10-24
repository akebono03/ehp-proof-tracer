$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Files = @(
    'phase168_r3_5_model_renderer.py',
    'phase165_r12_r20_eta_definition.py',
    'phase168_r3_41j2_chain_test_scope_fix\tests\test_phase168_r3_41j2_citation_provenance.py',
    'phase168_r3_37c_reference_projection.py',
    'phase168_r3_39f_frozen_comparison\audit.py',
    'phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py'
)
$Modified = $false

Push-Location $Repo
try {
    python (Join-Path $Package 'install.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-41M2 installation failed' }
    $Modified = $true

    python -m pytest -q --import-mode=importlib `
      '.\phase168_r3_41m2_registry_locator_fix\tests\test_phase168_r3_41m2_registry_locator_fix.py' `
      '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py' `
      '.\phase168_r3_41j2_chain_test_scope_fix\tests\test_phase168_r3_41j2_citation_provenance.py' `
      '.\phase168_r3_41i_renderer_closure_audit\tests\test_audit.py' `
      '.\phase168_r3_26a_after_r3_25a\tests\test_phase168_r3_26_projection.py' `
      '.\phase168_r3_10_registered_alias\tests\test_phase168_r3_10_registered_alias.py' `
      '.\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-41M2 focused pytest failed' }

    python -m phase168_r3_41m2_registry_locator_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41M2 frozen comparison audit failed' }

    Write-Host 'R3-41M2 completed; full pytest NOT run.'
    Write-Host "UPLOAD_BUNDLE $(Join-Path $Package 'output\review_bundle.zip')"
    $Modified = $false
}
finally {
    if ($Modified) {
        foreach ($Name in $Files) {
            $Target = Join-Path $Repo $Name
            $Leaf = Split-Path $Target -Leaf
            $Backup = Join-Path $Package ("output\" + $Leaf + '.before')
            if (-not (Test-Path -LiteralPath $Backup)) { throw "ROLLBACK MISSING: $Backup" }
            Copy-Item -LiteralPath $Backup -Destination $Target -Force
            $Expected = (Get-FileHash -LiteralPath $Backup -Algorithm SHA256).Hash
            $Actual = (Get-FileHash -LiteralPath $Target -Algorithm SHA256).Hash
            if ($Expected -ne $Actual) { throw "ROLLBACK HASH MISMATCH: $Target" }
            Write-Host "RESTORED $Target"
        }
        Write-Host 'ROLLBACK VERIFIED: 6 files byte-for-byte'
    }
    Pop-Location
}
