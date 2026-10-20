$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    $previous = $env:PYTHONPATH
    $env:PYTHONPATH = $root + [IO.Path]::PathSeparator + $previous
    try {
        python -m phase166_r3t_connection_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3-T runtime audit failed' }
        python -m pytest -q `
            'phase166_r3h_uniform_assertion_source/test_phase166_r3h_uniform_assertion_source.py' `
            'phase165_r57_r7_toda45_backward_connection/test_phase165_r57_r7_toda45_backward_connection.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3-T focused pytest failed' }
    } finally {
        $env:PYTHONPATH = $previous
    }
} finally {
    Pop-Location
}
Write-Host 'R3-T diagnostic complete; production untouched; full pytest NOT run.'
