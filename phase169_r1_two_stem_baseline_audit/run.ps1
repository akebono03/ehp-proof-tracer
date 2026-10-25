# Phase 169 R1 — audit only. Execute from any PowerShell working directory.
$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
if (-not (Test-Path ".git")) {
    throw "Not a Git working tree: $repo"
}
if (-not (Test-Path "web_group_proof.py")) {
    throw "Missing web_group_proof.py in repository root"
}
$output = Join-Path $package "output"
New-Item -ItemType Directory -Force -Path $output | Out-Null
$gitLog = Join-Path $output "git_state.txt"

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add("AUDIT_ONLY — no checkout, reset, source patch, or commit")
$lines.Add("REPOSITORY: $repo")
$lines.Add("EXPECTED_REMOTE_DEVELOP: d24d909c3c19ec731bdf4fca90aa682dfc1555ed")
$lines.Add("LOCAL_BRANCH:")
$lines.AddRange([string[]]@(& git branch --show-current))
$lines.Add("LOCAL_HEAD:")
$lines.AddRange([string[]]@(& git rev-parse HEAD))
$lines.Add("LOCAL_STATUS:")
$lines.AddRange([string[]]@(& git status --short --untracked-files=normal))
$lines.Add("LOCAL_RECENT_COMMITS:")
$lines.AddRange([string[]]@(& git log -5 --pretty=format:'%h %cI %s'))
$lines.Add("REMOTE_FETCH:")
# Windows PowerShell 5.1 treats even normal native stderr output as a
# NativeCommandError when ErrorActionPreference is Stop. Git commonly writes
# successful fetch progress to stderr; capture both streams as files instead.
$fetchStdout = Join-Path $output "git_fetch_stdout.txt"
$fetchStderr = Join-Path $output "git_fetch_stderr.txt"
$fetchCode = -1
try {
    $fetchProcess = Start-Process `
        -FilePath "git.exe" `
        -ArgumentList @("fetch", "origin", "develop") `
        -WorkingDirectory $repo `
        -NoNewWindow `
        -Wait `
        -PassThru `
        -RedirectStandardOutput $fetchStdout `
        -RedirectStandardError $fetchStderr
    $fetchCode = $fetchProcess.ExitCode
} catch {
    $lines.Add("FETCH_INVOCATION_ERROR: $($_.Exception.Message)")
}
if (Test-Path $fetchStdout) {
    foreach ($line in (Get-Content -Path $fetchStdout)) {
        $lines.Add("stdout: $line")
    }
}
if (Test-Path $fetchStderr) {
    foreach ($line in (Get-Content -Path $fetchStderr)) {
        $lines.Add("stderr: $line")
    }
}
$lines.Add("FETCH_EXIT_CODE: $fetchCode")
if ($fetchCode -eq 0) {
    $lines.Add("REMOTE_DEVELOP_HEAD:")
    $lines.AddRange([string[]]@(& git rev-parse origin/develop))
    $lines.Add("LOCAL_VS_REMOTE_DEVELOP_LEFT_RIGHT: (left=local only; right=remote only)")
    $lines.AddRange([string[]]@(& git rev-list --left-right --count HEAD...origin/develop))
    $lines.Add("UNCOMMITTED_CHANGED_PATHS:")
    $lines.AddRange([string[]]@(& git diff HEAD --name-only))
}
$lines | Set-Content -Path $gitLog -Encoding UTF8
Get-Content -Path $gitLog

Write-Host "PHASE169_R1_AUDIT_ONLY: no production files or tests patched."
& python -B (Join-Path $package "audit.py")
$auditExitCode = $LASTEXITCODE
Write-Host "AUDIT_EXIT_CODE: $auditExitCode"

# Focused tests only. Whole-suite pytest is reserved for Phase 169 closeout.
& python -B -m pytest -q --tb=short `
    tests/test_phase165_goal_only_cutover.py `
    tests/test_phase165_r12_r5_structure_bridge.py `
    tests/test_phase167_r3_generic_resolver.py `
    tests/test_phase168_r3_4_link_bridge.py `
    tests/test_phase161_r3_backward_goal_schema.py
$testExitCode = $LASTEXITCODE
Write-Host "FOCUSED_PYTEST_EXIT_CODE: $testExitCode"
if ($auditExitCode -ne 0 -or $testExitCode -ne 0) {
    throw "Phase 169 R1 needs review. See $output."
}
Write-Host "PHASE169_R1_AUDIT_COMPLETE: no production changes; full suite not run."
