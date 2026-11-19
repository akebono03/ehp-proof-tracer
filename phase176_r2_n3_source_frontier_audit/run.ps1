param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase176_r2_n3_source_frontier_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R2 DryRun failed' }
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r2_n3_source_frontier_audit/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R2 focused pytest failed' }
        python -B -m phase176_r2_n3_source_frontier_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R2 Source Frontier audit failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R2 git diff check failed' }
    }
} finally {
    Pop-Location
}
