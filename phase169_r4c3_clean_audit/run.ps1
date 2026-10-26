$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  python -m phase169_r4c3_clean_audit.runner
  if ($LASTEXITCODE -ne 0) {
    throw 'R4C3 focused proof audit or tracked-status verification failed.'
  }
} finally {
  Pop-Location
}
