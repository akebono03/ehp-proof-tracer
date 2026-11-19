param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r12r13r8r4_body_citation'
$installer = Join-Path $package 'installer.py'
if (-not (Test-Path $installer)) { throw 'Run from repository root' }
if ($DryRun) {
    & python -B $installer --root $repo --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R13R8R4 DryRun failed' }
    Write-Output 'PHASE175_R13R8R4_GATE=DRYRUN_PASS'
    exit 0
}
& python -B $installer --root $repo
if ($LASTEXITCODE -ne 0) { throw 'R13R8R4 installer failed' }
& python -B -m pytest -q -p no:cacheprovider (Join-Path (Join-Path $package 'tests') 'test_citation_prefix.py') (Join-Path (Join-Path 'phase175_r4r12r13r8r3_verified_reference_body' 'tests') 'test_verified_reference.py')
if ($LASTEXITCODE -ne 0) { throw 'R13R8R4 focused pytest failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R13R8R4 git diff check failed' }
Write-Output 'PHASE175_R13R8R4_GATE=BODY_CITATION_FOCUSED_TESTED'
