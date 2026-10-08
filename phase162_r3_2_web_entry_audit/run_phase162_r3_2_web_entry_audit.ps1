$ErrorActionPreference = "Stop"
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $bundle
if (!(Test-Path (Join-Path $repo "proof.py"))) {
    throw "Extract this folder into the EHP Proof Tracer repository root."
}
Push-Location $repo
try {
    python -B (Join-Path $bundle "audit_phase162_r3_2_web_entry.py")
    if ($LASTEXITCODE -ne 0) { throw "Local entrypoint audit failed." }
} finally {
    Pop-Location
}
