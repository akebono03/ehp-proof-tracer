$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 -c 'import sys; assert sys.version_info >= (3, 10)' 2>$null
  if ($LASTEXITCODE -eq 0) { $python = @('py', '-3') }
}
if (-not $python -and (Get-Command python -ErrorAction SilentlyContinue)) {
  & python -c 'import sys; assert sys.version_info >= (3, 10)' 2>$null
  if ($LASTEXITCODE -eq 0) { $python = @('python') }
}
if (-not $python) { throw 'Python 3.10+ not found. Run from the project Python environment.' }
$exe = $python[0]
$prefix = @()
if ($python.Length -gt 1) { $prefix = $python[1..($python.Length - 1)] }
$required = @('phase164_r7_statement_resolution.py', 'phase164_r7_repository_root_resolution.py', 'phase164_r4_r8_registry_reconstruction.py')
foreach ($item in $required) { if (-not (Test-Path (Join-Path $root $item))) { throw "Missing project file: $item" } }
$env:PYTHONPATH = "$folder;$root"
& $exe @prefix -m pytest -q (Join-Path $folder 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R7-R9 audit unit tests failed' }
$output = Join-Path $root 'phase164_r7_r9_output'
& $exe @prefix (Join-Path $folder 'audit.py') --root $root --output $output
if ($LASTEXITCODE -ne 0) { throw 'R7-R9 static closure audit blocked. Inspect phase164_r7_r9_output/report.md' }
$tests = @(
  'tests/test_phase164_r7_r8_fixed_literature_resolution.py',
  'tests/test_phase164_r4_r8_registry_reconstruction.py',
  'tests/test_phase164_r3_registry_search_connection.py',
  'tests/test_phase164_r2_citation_eligibility.py',
  'tests/test_phase109_3_recursive_known_group_identity_lookup.py',
  'tests/test_phase110_5_minimal_operation_query_core.py'
)
$tests = @($tests | Where-Object { Test-Path (Join-Path $root $_) })
if ($tests.Count -lt 6) { throw 'Targeted test files are missing; refusing closure decision' }
& $exe @prefix -m pytest -q @tests
if ($LASTEXITCODE -ne 0) { throw 'R7-R9 targeted regression tests failed' }
$report = Join-Path $output 'report.md'
Add-Content -Path $report -Value "`n## 限定 pytest`n- 指定6ファイル: PASS（詳細は PowerShell 出力）`n- R7 判定: **R7_SCOPED_CLOSED**。全経路の動的網羅性・数学的証明は認定しない。`n" -Encoding UTF8
Write-Host 'Phase 164 R7-R9: R7_SCOPED_CLOSED; targeted tests PASS; full pytest NOT run.'
