$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\web_group_proof.py')) { throw 'Run from the ehp_proof repository root.' }
python '.\phase168_r3_1_narrative_boundary_audit\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'Static audit failed' }
Write-Host 'Read-only audit complete. No pytest or production modifications.'
