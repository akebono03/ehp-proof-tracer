$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r16_web_citation_gate.py')) { throw 'Run from repository root.' }
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $folder 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Guarded patch failed.' }
python -m pytest -q (Join-Path $folder 'test_phase166_r3h_uniform_assertion_source.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-H targeted tests failed.' }
Write-Host 'R3-H targeted PASS; full pytest NOT run.'
