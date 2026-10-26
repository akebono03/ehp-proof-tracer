$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Host 'Phase 169 R3D — EHP isomorphism dependency audit'
Write-Host 'AUDIT_ONLY: no production files, existing tests or project documents patched.'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
Write-Host '[1/2] Historical-vs-common EHP proof frontier and publication checks'
python -B -m phase169_r3d_ehp_iso_dependencies.audit
if ($LASTEXITCODE -ne 0) {
    throw "R3D_AUDIT_EXIT_CODE=$LASTEXITCODE"
}
Write-Host '[2/2] Focused pytest only (no full suite)'
python -B -m pytest -q -p no:cacheprovider `
    ".\phase169_r3d_ehp_iso_dependencies\tests\test_phase169_r3d_ehp_iso_dependencies.py" `
    ".\tests\test_phase161_r3_backward_goal_schema.py" `
    ".\phase165_r12_r21_eta_generator_chain\tests\test_phase165_r12_r21_eta_generator_chain.py"
if ($LASTEXITCODE -ne 0) {
    throw "R3D_FOCUSED_PYTEST_EXIT_CODE=$LASTEXITCODE"
}
Write-Host 'PHASE169_R3D_AUDIT_COMPLETE: source unchanged; full suite not run.'
