param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
    if ($DryRun) {
        & python ".\phase171_r2j_r2_cyclic_hopf_surjective\install.py" --dry-run
        if ($LASTEXITCODE -ne 0) { throw "R2J-R2 DryRun preflight failed" }
        Write-Output "PHASE171_R2J_R2_RUN=PASS_DRY_RUN"
        return
    }
    & python ".\phase171_r2j_r2_cyclic_hopf_surjective\install.py" --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R2 initial preflight failed" }
    $Target = Join-Path $Root "phase165_r52_r9_shared_math.py"
    $wasInstalled = [bool](Select-String -Path $Target -Pattern "expand_cited_cyclic_hopf_surjectivity" -Quiet)
    & python ".\phase171_r2j_r2_cyclic_hopf_surjective\install.py"
    if ($LASTEXITCODE -ne 0) { throw "R2J-R2 patch failed" }
    try {
        & python -m pytest -q `
            ".\phase171_r2j_r2_cyclic_hopf_surjective\tests\test_r2j_r2_installer_head.py" `
            ".\phase171_r2j_r2_cyclic_hopf_surjective\tests\test_cited_cyclic_hopf.py" `
            ".\phase171_r2i_eta_hopf_bridge\tests\test_cited_eta_hopf.py"
        if ($LASTEXITCODE -ne 0) { throw "R2J-R2 focused pytest failed" }
        Write-Output "PHASE171_R2J_R2_FOCUSED_PYTEST=PASS"
        & python -m phase171_r2j_r2_cyclic_hopf_surjective.audit
        if ($LASTEXITCODE -ne 0) { throw "R2J-R2 proof ancestry audit failed" }
    } catch {
        if (-not $wasInstalled) {
            & python ".\phase171_r2j_r2_cyclic_hopf_surjective\install.py" --restore
            if ($LASTEXITCODE -ne 0) { throw "R2J-R2 failed AND automatic restore failed; inspect original backup" }
        }
        throw
    }
    Write-Output "PHASE171_R2J_R2_RUN=PASS"
} finally {
    Pop-Location
}
