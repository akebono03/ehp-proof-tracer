param(
    [switch] $DryRun
)
$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $RepoRoot
try {
    & python -B -m phase171_r2g_nu_prime_registered_identity.install check
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2G_PREFLIGHT_FAILED' }
    if ($DryRun.IsPresent) {
        Write-Host 'PHASE171_R2G_RESULT=PASS_DRY_RUN'
        return
    }
    & python -B -m phase171_r2g_nu_prime_registered_identity.install apply
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2G_PATCH_FAILED' }
    $Tests = @(
        'phase171_r2g_nu_prime_registered_identity/tests/test_install_unit.py',
        'phase171_r2g_nu_prime_registered_identity/tests/test_identity.py',
        'phase168_r2_8_3_generator_identity/tests/test_r2_8_3_generator_identity.py',
        'phase171_r2e_toda53_double_source/tests/test_source.py'
    )
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider @Tests
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2G_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2G_FOCUSED_PYTEST=PASS'
    & python -B -m phase171_r2g_nu_prime_registered_identity.audit
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2G_AUDIT_FAILED' }
    Write-Host 'PHASE171_R2G_RESULT=PASS'
}
finally {
    Pop-Location
}
