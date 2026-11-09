param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    python -B -m phase174_r3_r7_r24_prop27_general_typed_design.audit $(if ($DryRun) { "--dry-run" })
    if ($LASTEXITCODE -ne 0) { throw 'R24 source guard failed' }
    if (-not $DryRun) {
        python -B -m pytest -q phase174_r3_r7_r24_prop27_general_typed_design/tests/test_audit.py tests/test_phase50_prop27_theorem_semantics.py
        if ($LASTEXITCODE -ne 0) { throw 'R24 focused pytest failed' }
    }
    Write-Output ('PHASE174_R3R7R24_RUN=' + $(if ($DryRun) { 'DRYRUN_PASS' } else { 'PASS' }))
    Write-Output '(END)'
}
finally { Pop-Location }
