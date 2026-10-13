$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r39_web_connection.py" '.\phase165_r14_r39_web_connection.py' -Force
Copy-Item "$PSScriptRoot\phase165_r14_r39_toda51.tex" '.\phase165_r14_r39_toda51.tex' -Force
python "$PSScriptRoot\install.py"
if ($LASTEXITCODE -ne 0) { throw 'Web route install failed' }
python -m pytest -q "$PSScriptRoot\test_phase165_r14_r39_web_connection.py"
if ($LASTEXITCODE -ne 0) { throw 'Targeted Web tests failed' }
Write-Host 'R39 Web pi3^2 route installed. Full pytest NOT run. Restart the Web server to display the registered proof.'
