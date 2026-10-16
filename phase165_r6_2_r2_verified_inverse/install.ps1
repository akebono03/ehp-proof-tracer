$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Target = Join-Path $Root "phase165_r6_2_r2_verified_inverse.py"
$Source = Join-Path $PSScriptRoot "phase165_r6_2_r2_verified_inverse.py"
if ((Test-Path $Target) -and ((Get-FileHash $Target).Hash -ne (Get-FileHash $Source).Hash)) { throw "Different implementation already exists; abort" }
Copy-Item $Source $Target -Force
& (Join-Path $PSScriptRoot "run.ps1")
if ($LASTEXITCODE -ne 0) { throw "Focused tests failed" }
