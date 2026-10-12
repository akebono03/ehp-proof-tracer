$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
if (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 "$PSScriptRoot/apply.py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  & python "$PSScriptRoot/apply.py"
} else {
  throw "Python is required; documentation was not modified."
}
if ($LASTEXITCODE -ne 0) { throw "Documentation update failed; see error above." }
