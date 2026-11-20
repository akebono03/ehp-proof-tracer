param([switch]$DryRun, [int]$TimeoutSeconds = 120)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase176_r3r3_finite_hopf_image_subgroup_design.audit --dry-run --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R3 DryRun failed' }
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r3r3_finite_hopf_image_subgroup_design/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R3 focused tests failed' }
        python -B -m phase176_r3r3_finite_hopf_image_subgroup_design.audit --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R3 audit failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R3 diff check failed' }
    }
} finally {
    Pop-Location
}
