param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
python -B -m pytest -q -p no:cacheprovider phase175_r4r12r9_delta_generator_image_bridge/tests/test_rule.py phase175_r4r12r9_delta_generator_image_bridge/tests/test_lineage.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R9 focused tests failed' }
$argsList = @('-B','-m','phase175_r4r12r9_delta_generator_image_bridge.audit','--root',$root)
if ($DryRun) { $argsList += '--dry-run' }
python @argsList
if ($LASTEXITCODE -ne 0) { throw 'R4R12R9 audit failed' }
