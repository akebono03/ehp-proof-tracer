param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r56r1_audit_path_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R56R1 guarded audit correction DryRun failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R56R1_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }

    python -B -m phase174_r3_r7_r56r1_audit_path_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R56R1 audit correction failed' }

    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider '.\phase174_r3_r7_r56r1_audit_path_fix\tests\test_audit_path.py'
    if ($LASTEXITCODE -ne 0) { throw 'R56R1 focused report-path tests failed' }

    python -B -m phase174_r3_r7_r56_cyclic_generator_bridge.audit
    if ($LASTEXITCODE -ne 0) { throw 'R56 public proof certification failed after report-path fix' }

    Write-Output 'PHASE174_R56R1_FOCUSED_TESTS=PASS'
    Write-Output 'PHASE174_R56R1_FULL_PYTEST=False'
    Write-Output 'PHASE174_R56R1_GATE=PASS_R56R1_REPORT_PATH_AND_R56_PUBLIC_AUDIT'
    Write-Output '(END)'
} finally {
    Pop-Location
}
