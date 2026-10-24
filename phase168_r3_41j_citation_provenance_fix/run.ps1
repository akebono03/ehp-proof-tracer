$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Target = Join-Path $Repo 'phase168_r3_5_model_renderer.py'
$Backup = Join-Path $Package 'output\phase168_r3_5_model_renderer.py.before'
$Patched = $false

Push-Location $Repo
try {
    python (Join-Path $Package 'install.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-41J guarded installer failed' }
    $Patched = $true

    python -m pytest -q --import-mode=importlib `
      '.\phase168_r3_41j_citation_provenance_fix\tests\test_phase168_r3_41j_citation_provenance.py' `
      '.\phase168_r3_41i_renderer_closure_audit\tests\test_audit.py' `
      '.\phase168_r3_26a_after_r3_25a\tests\test_phase168_r3_26_projection.py' `
      '.\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-41J limited pytest failed' }

    python -m phase168_r3_41j_citation_provenance_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-41J cited provenance audit failed' }

    Write-Host 'R3-41J citation-only renderer patch complete; full pytest NOT run.'
    Write-Host "UPLOAD_BUNDLE $(Join-Path $Package 'output\review_bundle.zip')"
    Write-Host "FULL_FUNCTION $(Join-Path $Package 'modified_function_full.py')"
    Write-Host "FULL_FILE $(Join-Path $Package 'output\full_file.py')"
    $Patched = $false
}
finally {
    if ($Patched -and (Test-Path -LiteralPath $Backup)) {
        Copy-Item -LiteralPath $Backup -Destination $Target -Force
        Write-Host 'ROLLBACK: restored phase168_r3_5_model_renderer.py from byte-for-byte backup'
    }
    Pop-Location
}
