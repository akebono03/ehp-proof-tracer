$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$testFiles = @(
 'tests/test_phase49_probe.py::test_phase49_probe_derives_eta_2_definition',
 'tests/test_phase49_probe.py::test_phase49_probe_derives_h_eta_2_equals_iota_3',
 'tests/test_phase56_probe.py::test_phase56_probe_derives_phase49_eta2_dependencies',
 'tests/test_phase56_probe.py::test_phase56_probe_derives_all_phase56_intermediate_results'
)
$stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$out = Join-Path $root "phase165_r6_audit_results\phase49_56_root_check\$stamp"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$log = Join-Path $out 'targeted_pytest.log'
python -m pytest -q @testFiles 2>&1 | Tee-Object -FilePath $log
$code = $LASTEXITCODE
@{status='DIAGNOSTIC_COMPLETE';pytest_exit_code=$code;tested=$testFiles;full_pytest_run=$false;repository_files_modified=0;log=$log} | ConvertTo-Json -Depth 6 | Tee-Object -FilePath (Join-Path $out 'report.json')
Write-Host 'Diagnostic completed. FAIL is expected while the Phase49 root issue remains.'
exit 0
