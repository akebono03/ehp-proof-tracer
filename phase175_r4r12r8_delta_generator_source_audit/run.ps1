param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = 'phase175_r4r12r8_delta_generator_source_audit'
python -B -m pytest -q --import-mode=prepend -p no:cacheprovider ".\$package\tests\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R4R12R8 focused pytest failed' }
$arguments = @('-B', '-m', "$package.audit", '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { throw 'R4R12R8 read-only audit failed' }
