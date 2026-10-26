$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Host 'Phase 169 R3G1: (5.3) Hopf relation and Proposition 5.1 composite source audit'
Write-Host 'R3G1_AUDIT_ONLY: no application, existing tests or docs patched'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
if ($LASTEXITCODE -ne 0) { throw 'Git HEAD unavailable' }
Write-Host '[0/3] Preflight: R3F3 terminal integration, source, tests, and Python module access'
$files = @(
    (Join-Path $package 'audit.py'),
    (Join-Path $package 'tests\test_phase169_r3g_hopf_source_and_composite_audit.py'),
    (Join-Path $repo 'sources\toda\Toda_05_2.tex'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'phase165_r52_r9_shared_math.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py')
)
foreach ($path in $files) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "R3G_MISSING=$path" }
}
python -B -c 'from phase165_r14_r5_ehp_connection import expand_registered_ehp_terminal_goal; assert callable(expand_registered_ehp_terminal_goal)'
if ($LASTEXITCODE -ne 0) { throw 'R3G1 requires successfully installed R3F3' }
Write-Host 'R3G1_R3F3_PRESENT=True'
Write-Host '[1/3] Existing and new focused pytest only'
python -B -m pytest -q -p no:cacheprovider `
    (Join-Path $package 'tests\test_phase169_r3g_hopf_source_and_composite_audit.py') `
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py') `
    (Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py')
$pytest_code = $LASTEXITCODE
Write-Host "R3G1_FOCUSED_PYTEST_EXIT_CODE=$pytest_code"
if ($pytest_code -ne 0) { throw "R3G1_FOCUSED_PYTEST_EXIT_CODE=$pytest_code" }
Write-Host '[2/3] Inspect real citation-screened pi5^3 proof context'
python -B -m phase169_r3g1_powershell_preflight_quote_fix.audit
$audit_code = $LASTEXITCODE
Write-Host "R3G1_AUDIT_EXIT_CODE=$audit_code"
if ($audit_code -ne 0) { throw "R3G1_AUDIT_EXIT_CODE=$audit_code" }
Write-Host '[3/3] Completion'
Write-Host 'R3G1_COMPLETE: literature and proof ancestry diagnosed; full suite NOT run.'
