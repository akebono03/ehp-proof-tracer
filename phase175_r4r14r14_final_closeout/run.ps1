param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase175_r4r14r14_final_closeout.gate --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R4R14R14 DryRun failed' }
    } else {
        # The only tests run before the Phase-end full suite are focused tests.
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
            phase175_r4r14r14_final_closeout/tests `
            phase175_r4r14r13_final_gate_preflight/tests
        if ($LASTEXITCODE -ne 0) { throw 'R4R14R14 focused tests failed; full pytest NOT run' }
        python -B -m phase175_r4r14r14_final_closeout.gate
        if ($LASTEXITCODE -ne 0) { throw 'R4R14R14 final gate failed; inspect saved evidence before any retry' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R4R14R14 git diff check failed' }
    }
} finally {
    Pop-Location
}
