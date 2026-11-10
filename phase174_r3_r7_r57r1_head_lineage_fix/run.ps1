param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r57r1_head_lineage_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R57R1 source and HEAD-lineage guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R57R1_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r57r1_head_lineage_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R57R1 guarded installer correction failed' }
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r57r1_head_lineage_fix/tests/test_lineage.py
    if ($LASTEXITCODE -ne 0) { throw 'R57R1 focused pytest failed' }
    Write-Output 'PHASE174_R57R1_INSTALL_GATE=PASS'
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r57_narrative_source_cleanup\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R57 amended DryRun failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r57_narrative_source_cleanup\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R57 public proof audit failed' }
    Write-Output 'PHASE174_R57R1_FULL_PYTEST=False'
    Write-Output 'PHASE174_R57R1_GATE=PASS_R57R1_HEAD_LINEAGE_AND_R57_PUBLIC'
    Write-Output '(END)'
} finally {
    Pop-Location
}
