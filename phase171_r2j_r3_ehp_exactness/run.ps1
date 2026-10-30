param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
    $Package = ".\phase171_r2j_r3_ehp_exactness"
    & python "$Package\install.py" --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R3 preflight failed" }
    if ($DryRun) {
        Write-Output "PHASE171_R2J_R3_RUN=PASS_DRY_RUN"
        return
    }
    $Target = Join-Path $Root "phase165_r52_r9_shared_math.py"
    $WasInstalled = [bool](Select-String -Path $Target -Pattern "expand_cited_ehp_surjectivity_consequences" -Quiet)
    & python "$Package\install.py"
    if ($LASTEXITCODE -ne 0) { throw "R2J-R3 installation failed" }
    try {
        & python -m pytest -p no:cacheprovider -q `
            "$Package\tests\test_installer.py" `
            "$Package\tests\test_r2j_r3_exactness.py" `
            ".\phase171_r2j_r2_cyclic_hopf_surjective\tests\test_cited_cyclic_hopf.py" `
            ".\phase171_r2i_eta_hopf_bridge\tests\test_cited_eta_hopf.py" `
            ".\phase171_r2j_r1_prop53_ehp_audit\tests\test_audit.py"
        if ($LASTEXITCODE -ne 0) { throw "R2J-R3 focused pytest failed" }
        Write-Output "PHASE171_R2J_R3_FOCUSED_PYTEST=PASS"
        & python -m phase171_r2j_r3_ehp_exactness.audit
        if ($LASTEXITCODE -ne 0) { throw "R2J-R3 proof tree audit failed" }
    } catch {
        if (-not $WasInstalled) {
            & python "$Package\install.py" --restore
            if ($LASTEXITCODE -ne 0) { throw "R2J-R3 rollback failed: inspect backup" }
        }
        throw
    }
    Write-Output "PHASE171_R2J_R3_RUN=PASS"
} finally {
    Pop-Location
}
