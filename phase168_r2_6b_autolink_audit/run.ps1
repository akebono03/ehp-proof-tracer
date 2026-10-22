$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) { throw 'Run from repository root.' }
python -m pytest '.\phase168_r2_6b_autolink_audit\tests\test_audit.py' -q
if ($LASTEXITCODE -ne 0) { throw 'Limited tests failed.' }
python -m phase168_r2_6b_autolink_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'Audit failed.' }
