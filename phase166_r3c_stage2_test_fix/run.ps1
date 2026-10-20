$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $target = Join-Path $root 'phase166_r3c_stage2\test_stage2.py'
    if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { throw 'Original R3-C stage 2 test file is missing' }
    $old = Get-Content -LiteralPath $target -Raw -Encoding UTF8
    if ($old -match '\[78, 79, None\]') {
        Write-Host 'Corrected test already installed'
    } elseif ($old.Contains('[77, 76, None]')) {
        $backup = Join-Path $PSScriptRoot 'test_stage2_before_fix.py.bak'
        Copy-Item -LiteralPath $target -Destination $backup -Force
        $new = $old.Replace('[77, 76, None]', '[78, 79, None]')
        [System.IO.File]::WriteAllText($target, $new, (New-Object System.Text.UTF8Encoding($false)))
        Write-Host 'Corrected parameter cases: 78, 79, None'
    } else {
        throw 'Unexpected test content. No replacement performed.'
    }
    python -m pytest -q '.\phase166_r3c_stage2\test_stage2.py' '.\tests\test_phase165_r3_recursive_search.py' '.\phase166_r3_ordered_lookup\tests\test_phase166_r3_ordered_lookup.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-C stage 2 focused tests failed' }
    Write-Host 'R3-C stage 2 targeted PASS; full pytest NOT run.'
} finally {
    Pop-Location
}
