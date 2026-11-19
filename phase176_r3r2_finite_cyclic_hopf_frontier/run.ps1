param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase176_r3r2_finite_cyclic_hopf_frontier.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R2 DryRun failed' }
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r3r2_finite_cyclic_hopf_frontier/tests
        if ($LASTEXITCODE -ne 0) { throw 'R3R2 focused pytest failed' }
        python -B -m phase176_r3r2_finite_cyclic_hopf_frontier.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R2 audit failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R2 git diff --check failed' }
    }
} finally {
    Pop-Location
}
