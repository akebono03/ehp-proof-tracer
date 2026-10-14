$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$names = @(
    'test_phase165_r52_r17_internal_dependency.py',
    'test_phase165_r52_r9_shared_math.py',
    'test_phase165_r52_r14_root_dependency_guard.py',
    'test_phase165_r52_r15_ordered_citation.py',
    'test_phase165_r52_r16_web_citation_gate.py'
)
$dirs = @(
    '.',
    'phase165_r52_r17_r1_installer_fix',
    'phase165_r52_r17_internal_dependency',
    'phase165_r52_r14_root_dependency_guard',
    'phase165_r52_r15_ordered_citation',
    'phase165_r52_r15_r1_fixture_fix',
    'phase165_r52_r16_web_citation_gate',
    'phase165_r52_r16_r1_install_fix',
    'phase165_r52_r16_r2_nullable_record_fix'
)
$found = @()
$missing = @()
foreach ($name in $names) {
    $hit = $null
    foreach ($dir in $dirs) {
        $candidate = Join-Path (Join-Path $root $dir) $name
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $hit = $candidate
            break
        }
    }
    if ($null -ne $hit) {
        $found += $hit
        Write-Host "Found test: $hit"
    } else {
        $missing += $name
        Write-Warning "Test unavailable (not treated as passed): $name"
    }
}
if (-not ($found | Where-Object { $_ -like '*test_phase165_r52_r17_internal_dependency.py' })) {
    throw 'R17 new test file is required'
}
if ($found.Count -eq 0) { throw 'No targeted tests found' }
python -m pytest -q @found
if ($LASTEXITCODE -ne 0) { throw 'R17 targeted tests failed' }
Write-Host "R17-R2 targeted tests passed: $($found.Count) file(s)."
if ($missing.Count -gt 0) { Write-Warning "Not run: $($missing -join ', ')" }
Write-Host 'Full pytest NOT run. Production code unchanged by R17-R2.'
