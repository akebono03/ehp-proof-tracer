param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldUtf8 = $env:PYTHONUTF8
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    python -B -m phase177_r16_verified_proof_tree_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R16 preflight failed' }
    if (-not $DryRun) {
        python -B -m phase177_r16_verified_proof_tree_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R16 audit failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R16 git diff check failed' }
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTHONUTF8 = $oldUtf8
    Pop-Location
}
