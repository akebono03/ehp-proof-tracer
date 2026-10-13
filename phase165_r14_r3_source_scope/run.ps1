$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r3_source_scope.py" ".\phase165_r14_r3_source_scope.py" -Force
$OldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($OldPythonPath) {
        "$Root$([IO.Path]::PathSeparator)$OldPythonPath"
    } else {
        $Root
    }
    python -m pytest -q "$PSScriptRoot\test_phase165_r14_r3_source_scope.py" `
        "tests/test_phase165_r12_typed_binding.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$PSScriptRoot\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
}
Write-Host "Phase 165 R14-R3 targeted verification done; full pytest NOT run."
