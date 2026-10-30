param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Installer = Join-Path $PSScriptRoot "install.py"
$OriginalRunner = Join-Path $Repo "phase171_r2j_r4_r5_short_exact_sequence\run.ps1"
Push-Location $Repo
try {
    if (-not (Test-Path $OriginalRunner)) {
        throw "The existing R4-R5 package run.ps1 is required"
    }
    if ($DryRun) {
        python -B $Installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw "R4-R5-R1 guard preflight failed" }
        powershell -NoProfile -ExecutionPolicy Bypass -File $OriginalRunner -DryRun
        if ($LASTEXITCODE -ne 0) { throw "R4-R5 original dry-run failed" }
        Write-Output "PHASE171_R2J_R4_R5_R1_RESULT=PASS_DRY_RUN"
    }
    else {
        python -B $Installer
        if ($LASTEXITCODE -ne 0) { throw "R4-R5-R1 guarded patch failed" }
        powershell -NoProfile -ExecutionPolicy Bypass -File $OriginalRunner
        if ($LASTEXITCODE -ne 0) { throw "R4-R5 focused pytest or proof replay failed" }
        Write-Output "PHASE171_R2J_R4_R5_R1_RESULT=PASS"
    }
}
finally {
    Pop-Location
}
