param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsAudit = @('-m', 'phase175_r4r12r13r2_delta_injective_e_surjective.audit', '--root', $root)
    if ($DryRun) { $argsAudit += '--dry-run' }
    python @argsAudit
    if ($LASTEXITCODE -ne 0) { throw 'R13R2 audit failed' }
    python -m pytest -q phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R13R2 focused tests failed' }
} finally { Pop-Location }
