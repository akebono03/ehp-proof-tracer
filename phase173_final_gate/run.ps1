param([switch]$DryRun)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'

$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$GitRoot = (& git -C $Root --no-pager rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($GitRoot)) {
    throw 'Git repository root not found'
}
if (-not [string]::Equals(
    [IO.Path]::GetFullPath($Root).TrimEnd([char]'\', [char]'/'),
    [IO.Path]::GetFullPath($GitRoot).TrimEnd([char]'\', [char]'/'),
    [StringComparison]::OrdinalIgnoreCase
)) {
    throw 'Extract Phase 173 final-gate ZIP at the repository root'
}

$RecordParent = if ([string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
    $env:TEMP
} else {
    $env:LOCALAPPDATA
}
$Evidence = Join-Path $RecordParent 'EHPProofTracerRecovery\phase173_final_gate'
$Report = Join-Path $Evidence 'phase173_full_test_report.json'
$Attempt = Join-Path $Evidence 'phase173_full_test_attempt.json'
$Stdout = Join-Path $Evidence 'active_suite_stdout.txt'
$Stderr = Join-Path $Evidence 'active_suite_stderr.txt'

Push-Location $Root
try {
    Write-Output 'PHASE173_FINAL_SCOPE=END_OF_PHASE_ACTIVE_TEST_SUITE'
    Write-Output 'PHASE173_FINAL_GIT_RESET_CLEAN_STAGE_COMMIT=NONE'
    Write-Output 'PHASE173_FINAL_PRODUCTION_WRITES=NONE'
    Write-Output 'PHASE173_FINAL_BROWSER_CONTENT_CHECKED=FOUR_CASES'
    Write-Output 'PHASE173_FINAL_BROWSER_PIXEL_LAYOUT_VERIFIED=UNCONFIRMED'
    $IndexBefore = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read current Git index tree' }
    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'Unable to fetch origin/develop' }

    Write-Output '=== PHASE 173 FINAL GATE CONTRACT TESTS ==='
    & python -B -m pytest -q -p no:cacheprovider phase173_final_gate/tests/test_gate_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'Phase 173 final gate contract tests failed' }

    & python -B -m phase173_final_gate.gate preflight --repo $Root --report $Report
    if ($LASTEXITCODE -ne 0) { throw 'Phase 173 preflight failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_FINAL_DRY_RUN=PASS'
        Write-Output 'PHASE173_FINAL_FULL_PYTEST=NOT_RUN_IN_DRY_RUN'
    } else {
        if (Test-Path $Report) {
            $Previous = Get-Content $Report -Raw -Encoding UTF8 | ConvertFrom-Json
            $Head = (& git --no-pager rev-parse HEAD).Trim()
            if ($Previous.status -eq 'PASS' -and $Previous.head -eq $Head) {
                Write-Output 'PHASE173_FINAL_FULL_PYTEST=PASS_PREVIOUSLY_RECORDED'
                Write-Output "PHASE173_FINAL_FULL_PYTEST_PASSED=$($Previous.pytest_passed_count)"
                Write-Output "PHASE173_FINAL_REPORT=$Report"
            } else {
                throw 'An earlier full-suite report exists; review it before another execution'
            }
        } else {
            if (Test-Path $Attempt) {
                throw 'A previous full-suite attempt exists; review its log before retrying'
            }
            New-Item -ItemType Directory -Force -Path $Evidence | Out-Null
            $Head = (& git --no-pager rev-parse HEAD).Trim()
            $Start = [ordered]@{
                phase = 173
                status = 'STARTED'
                head = $Head
                started_utc = [DateTime]::UtcNow.ToString('o')
                command = 'python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests'
            }
            $Start | ConvertTo-Json -Depth 4 | Set-Content -Path $Attempt -Encoding UTF8
            $PythonPath = (Get-Command python).Source
            Write-Output '=== PHASE 173 ACTIVE FULL PYTEST (ONE PHASE-END EXECUTION) ==='
            $Args = @('-B', '-m', 'pytest', '-q', '--tb=short', '--disable-warnings',
                '-p', 'no:cacheprovider', 'tests')
            $Process = Start-Process -FilePath $PythonPath -ArgumentList $Args `
                -WorkingDirectory $Root -RedirectStandardOutput $Stdout `
                -RedirectStandardError $Stderr -NoNewWindow -Wait -PassThru
            $TestExit = $Process.ExitCode
            Write-Output "PHASE173_FINAL_PYTEST_EXIT=$TestExit"
            if (Test-Path $Stdout) { Get-Content $Stdout -Tail 45 }
            if ((Test-Path $Stderr) -and (Get-Item $Stderr).Length -gt 0) {
                Write-Output '=== PYTEST STDERR ==='
                Get-Content $Stderr -Tail 30
            }
            & python -B -m phase173_final_gate.gate finalize --repo $Root `
                --report $Report --stdout $Stdout --stderr $Stderr `
                --exit-code $TestExit
            if ($LASTEXITCODE -ne 0) { throw 'Phase 173 active full pytest failed' }
        }
        Write-Output 'PHASE173_FINAL_GATE=PASS'
        Write-Output 'PHASE173_FINAL_PHASE_FORMALLY_CLOSED=NO_DOCUMENTATION_PENDING'
    }

    $IndexAfter = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0 -or $IndexBefore -ne $IndexAfter) {
        throw 'Phase 173 gate changed the Git index'
    }
    Write-Output 'PHASE173_FINAL_GIT_INDEX_PRESERVED=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed' }
} finally {
    Pop-Location
}
