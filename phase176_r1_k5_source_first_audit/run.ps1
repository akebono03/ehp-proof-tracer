param([switch]$DryRun, [int]$TimeoutSeconds = 90)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase176_r1_k5_source_first_audit.audit --dry-run --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R1 DryRun failed' }
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r1_k5_source_first_audit/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R1 focused tests failed' }
        python -B -m phase176_r1_k5_source_first_audit.audit --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R1 audit failed' }
    }
} finally {
    Pop-Location
}
