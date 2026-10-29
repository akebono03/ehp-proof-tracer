param(
    [switch] $DryRun,
    [switch] $Search
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
    python -B -m phase171_r2f_pi63_extension_gap_audit.audit --root $repo --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_DRY_RUN_FAILED' }
    if ($DryRun.IsPresent) { return }
    $tests = @(
        'phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py',
        'phase171_r2e_toda53_double_source/tests/test_source.py',
        'phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py',
        'test_phase165_r52_r9_shared_math.py'
    )
    python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider @tests
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2F_FOCUSED_PYTEST=PASS'
    $argsAudit = @('-B', '-m', 'phase171_r2f_pi63_extension_gap_audit.audit', '--root', $repo)
    if ($Search.IsPresent) { $argsAudit += '--search' }
    & python @argsAudit
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_AUDIT_FAILED' }
}
finally {
    Pop-Location
}
