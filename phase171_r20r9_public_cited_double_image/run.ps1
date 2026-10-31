param(
    [switch]$DryRun,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if ($DryRun) {
    python -m phase171_r20r9_public_cited_double_image.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20R9 preflight failed' }
    exit 0
}
python -m phase171_r20r9_public_cited_double_image.install
if ($LASTEXITCODE -ne 0) { throw 'R20R9 install failed' }
if (-not $SkipTests) {
    # R20R8 and R20R9 both have tests/test_source.py. Collect them in
    # separate pytest processes so Python cannot conflate the modules.
    Write-Host 'PHASE171_R20R9_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r20r9_public_cited_double_image/tests/test_install.py' `
        'phase171_r20r9_public_cited_double_image/tests/test_source.py' `
        'phase171_r2j_r4_r3_double_image_bridge/tests/test_audit.py::test_rule_does_not_accept_noninferred_image_or_uncited_relation_fixture'
    if ($LASTEXITCODE -ne 0) { throw 'R20R9 focused pytest: new tests and old source guard failed' }
    Write-Host 'PHASE171_R20R9_FOCUSED_PYTEST_R9_AND_ORIGINAL=PASS'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r20r8_public_double_nonzero/tests/test_source.py'
    if ($LASTEXITCODE -ne 0) { throw 'R20R9 focused pytest: R20R8 regression failed' }
    Write-Host 'PHASE171_R20R9_FOCUSED_PYTEST_R8=PASS'
    Write-Host 'PHASE171_R20R9_FOCUSED_PYTEST=PASS'
}
python -m phase171_r20r9_public_cited_double_image.audit
if ($LASTEXITCODE -ne 0) { throw 'R20R9 public route audit failed' }
git status -sb
git diff --stat
