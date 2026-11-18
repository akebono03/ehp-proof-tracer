param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
  phase175_r4r12r10r1_cited_511_public/tests/test_cited_511.py `
  phase175_r4r12r10r1_cited_511_public/tests/test_lineage.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R10R1 focused pytest failed' }
$argsList = @('-B', '-m', 'phase175_r4r12r10r1_cited_511_public.audit')
if ($DryRun) { $argsList += '--dry-run' }
python @argsList
if ($LASTEXITCODE -ne 0) { throw 'R4R12R10R1 source/public audit failed' }
