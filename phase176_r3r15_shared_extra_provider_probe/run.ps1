param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r15_shared_extra_provider_probe.audit --dry-run
        exit $LASTEXITCODE
    }

    python -B -m phase176_r3r15_shared_extra_provider_probe.audit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    $testFiles = @(
        'phase176_r3r15_shared_extra_provider_probe/tests/test_provider.py'
        'phase176_r3r14_isolated_two_stage_provider/tests/test_provider.py'
        'phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py'
        'phase175_r3r9_lemma57_explicit_public/tests/test_rule.py'
    )
    foreach ($testFile in $testFiles) {
        python -B -m pytest -q -p no:cacheprovider $testFile
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    exit 0
} finally {
    Pop-Location
}
