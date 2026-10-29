param(
    [switch] $DryRun
)
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $package '..')).Path
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $repo
try {
    python -B -m phase171_r2e_toda53_double_source.install check
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2E_PREFLIGHT_FAILED' }
    if ($DryRun.IsPresent) {
        Write-Host 'PHASE171_R2E_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2e_toda53_double_source.install install
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2E_INSTALL_FAILED' }
    $tests = @(
        'phase171_r2e_toda53_double_source/tests/test_install_unit.py',
        'phase171_r2e_toda53_double_source/tests/test_source.py',
        'phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py',
        'test_phase165_r52_r9_shared_math.py'
    )
    python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider @tests
    $testExit = $LASTEXITCODE
    if ($testExit -ne 0) {
        Write-Warning 'Focused tests failed: restoring R2E modifications.'
        python -B -m phase171_r2e_toda53_double_source.install restore
        if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2E_RESTORE_FAILED' }
        throw "PHASE171_R2E_FOCUSED_PYTEST_EXIT=$testExit"
    }
    Write-Host 'PHASE171_R2E_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2e_toda53_double_source.audit
    $auditExit = $LASTEXITCODE
    if ($auditExit -ne 0) {
        Write-Warning 'Post-install source audit failed: restoring R2E modifications.'
        python -B -m phase171_r2e_toda53_double_source.install restore
        if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2E_RESTORE_FAILED' }
        throw "PHASE171_R2E_AUDIT_EXIT=$auditExit"
    }
    Write-Host 'PHASE171_R2E_RESULT=PASS'
}
finally {
    Pop-Location
}
