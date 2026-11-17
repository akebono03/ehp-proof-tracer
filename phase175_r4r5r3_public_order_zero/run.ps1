param(
    [switch] $DryRun,
    [string] $R4R5R2Report = ""
)
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$target = Join-Path $root 'phase165_r52_r9_shared_math.py'
$original = $null
Push-Location $root
try {
    $tests = @(
        'phase175_r4r5r3_public_order_zero/tests/test_provider.py',
        'phase175_r4r5r3_public_order_zero/tests/test_installer.py',
        'phase175_r4r5r3_public_order_zero/tests/test_head_lineage.py',
        'phase175_r4r5_eta7_annihilator_isolated/tests/test_rule.py',
        'phase175_r4r5_eta7_annihilator_isolated/tests/test_audit.py',
        'phase175_r4r4_pi95_premise_frontier/tests/test_audit.py',
        'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
        'phase175_r4r3_two_summand_quotient/tests/test_audit.py',
        'phase175_r4_pi95_audit/tests/test_audit.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R5R3 focused baseline pytest failed' }
    Write-Output 'PHASE175_R4R5R3_FOCUSED_BASELINE_PYTEST=PASS'

    if (-not $DryRun) {
        $original = [System.IO.File]::ReadAllBytes($target)
    }
    $command = @('-B', '-m', 'phase175_r4r5r3_public_order_zero.audit', '--root', $root)
    if ($DryRun) { $command += '--dry-run' }
    if ($R4R5R2Report -ne '') { $command += @('--r4r5r2-report', $R4R5R2Report) }
    & python @command
    if ($LASTEXITCODE -ne 0) { throw 'R4R5R3 source guard or public wiring failed' }

    if (-not $DryRun) {
        Write-Output 'PHASE175_R4R5R3_PRODUCTION_PATCH=APPLIED'
    }
    Write-Output 'PHASE175_R4R5R3_EXIT_CODE=0'
    exit 0
} catch {
    if ($null -ne $original) {
        [System.IO.File]::WriteAllBytes($target, $original)
        Write-Output 'PHASE175_R4R5R3_PRODUCTION_PATCH=ROLLED_BACK'
    }
    Write-Output ('PHASE175_R4R5R3_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R5R3_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
