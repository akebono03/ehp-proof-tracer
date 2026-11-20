param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $args = @('-B', '-m', 'phase176_r3r20_cyclic_candidate_boundary.audit')
    if ($DryRun) { $args += '--dry-run' }
    & python @args
    if ($LASTEXITCODE -ne 0) { throw 'R3R20 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider 'phase176_r3r20_cyclic_candidate_boundary/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3R20 pytest failed' }
    }
} finally { Pop-Location }
