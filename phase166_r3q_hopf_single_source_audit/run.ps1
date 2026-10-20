$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m phase166_r3q_hopf_single_source_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-Q Hopf single-source audit failed.' }
} finally {
    Pop-Location
}
