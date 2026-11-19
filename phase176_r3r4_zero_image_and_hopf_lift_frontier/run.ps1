param(
    [switch] $DryRun,
    [ValidateRange(1, 1800)]
    [int] $TimeoutSeconds = 120
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r4_zero_image_and_hopf_lift_frontier.audit --dry-run --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R4 DryRun failed' }
    } else {
        & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r3r4_zero_image_and_hopf_lift_frontier/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R4 focused pytest failed' }
        & python -B -m phase176_r3r4_zero_image_and_hopf_lift_frontier.audit --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R4 audit failed' }
    }
} finally {
    Pop-Location
}
