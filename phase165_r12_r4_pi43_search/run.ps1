$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$python = 'python'
$previousPythonPath = $env:PYTHONPATH
try {
    if ([string]::IsNullOrEmpty($previousPythonPath)) {
        $env:PYTHONPATH = $root
    } else {
        $env:PYTHONPATH = $root + [System.IO.Path]::PathSeparator + $previousPythonPath
    }
    & $python -m pytest -q '.\phase165_r12_r4_pi43_search\tests\test_phase165_r12_r4_pi43_search.py' '.\phase165_r12_r4_pi43_search\tests\test_phase165_r12_r4_encoding.py' '.\tests\test_phase165_r8_rule_provider.py' '.\tests\test_phase165_r11_wiring.py'
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed; canonical search audit not started.' }
    & $python -m phase165_r12_r4_pi43_search.audit
    if ($LASTEXITCODE -ne 0) { throw 'R12-R4 audit process failed.' }
    Write-Host 'R12-R4 read-only audit completed; inspect search_status; full pytest NOT run.'
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
