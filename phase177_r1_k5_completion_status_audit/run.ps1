param([switch]$DryRun, [int]$TimeoutSeconds = 180)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase177_r1_k5_completion_status_audit.audit --dry-run --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R1 DryRun failed' }
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase177_r1_k5_completion_status_audit/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R1 focused tests failed' }
        python -B -m phase177_r1_k5_completion_status_audit.audit --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R1 audit failed' }
    }
} finally {
    Pop-Location
}
