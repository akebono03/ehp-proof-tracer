param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase176_r3_n3_rule_sufficiency_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3 DryRun failed' }
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r3_n3_rule_sufficiency_audit/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3 focused pytest failed' }
        python -B -m phase176_r3_n3_rule_sufficiency_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3 audit failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3 git diff check failed' }
    }
} finally {
    Pop-Location
}
