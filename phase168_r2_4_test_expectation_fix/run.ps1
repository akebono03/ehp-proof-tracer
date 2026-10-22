$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python ".\phase168_r2_4_test_expectation_fix\install.py"
    if ($LASTEXITCODE -ne 0) { throw 'Test installation failed' }
    python -m pytest -q ".\phase166_r3t_goal_source_binding\test_connection.py" ".\phase168_r2_4_nk_citation_binding\test_binding.py"
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
    Write-Host 'Targeted pytest PASS; full pytest NOT run.'
} finally {
    Pop-Location
}
