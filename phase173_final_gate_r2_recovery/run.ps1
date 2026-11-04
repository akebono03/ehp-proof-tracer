param(
    [switch]$DryRun,
    [string]$PreviousEvidencePath,
    [switch]$AllowMissingPriorEvidence
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'

$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$GitRoot = (& git -C $Root --no-pager rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($GitRoot)) {
    throw 'Git repository root was not found'
}
if (-not [string]::Equals(
    [IO.Path]::GetFullPath($Root).TrimEnd([char]'\', [char]'/'),
    [IO.Path]::GetFullPath($GitRoot).TrimEnd([char]'\', [char]'/'),
    [StringComparison]::OrdinalIgnoreCase
)) {
    throw 'Extract Phase 173 R2 ZIP at repository root'
}

$RecordParent = if ([string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
    $env:TEMP
} else {
    $env:LOCALAPPDATA
}
$DefaultPrevious = Join-Path $RecordParent 'EHPProofTracerRecovery\phase173_final_gate'
$KnownPreviousProfile = 'C:\Users\oomae\AppData\Local\EHPProofTracerRecovery\phase173_final_gate'
$RequiredPreviousFiles = @(
    'phase173_full_test_report.json',
    'phase173_full_test_attempt.json',
    'active_suite_stdout.txt',
    'active_suite_stderr.txt'
)
function Test-CompletePreviousEvidence {
    param([string]$Directory)
    foreach ($File in $RequiredPreviousFiles) {
        if (-not (Test-Path -LiteralPath (Join-Path $Directory $File) -PathType Leaf)) {
            return $false
        }
    }
    return $true
}
if (-not [string]::IsNullOrWhiteSpace($PreviousEvidencePath)) {
    $PreviousEvidence = [IO.Path]::GetFullPath($PreviousEvidencePath)
} elseif (Test-CompletePreviousEvidence $DefaultPrevious) {
    $PreviousEvidence = $DefaultPrevious
} elseif (Test-CompletePreviousEvidence $KnownPreviousProfile) {
    $PreviousEvidence = $KnownPreviousProfile
} elseif ($AllowMissingPriorEvidence) {
    $PreviousEvidence = $DefaultPrevious
    Write-Output 'PHASE173_FINAL_R2_MISSING_PRIOR_ACKNOWLEDGED=True'
} else {
    Write-Output 'PHASE173_FINAL_R2_PRIOR_EVIDENCE=NOT_FOUND'
    foreach ($Directory in @($DefaultPrevious, $KnownPreviousProfile) | Select-Object -Unique) {
        $Missing = @($RequiredPreviousFiles | Where-Object {
            -not (Test-Path -LiteralPath (Join-Path $Directory $_) -PathType Leaf)
        })
        Write-Output "PHASE173_FINAL_R2_CHECKED_DIR=$Directory"
        Write-Output "PHASE173_FINAL_R2_MISSING_FILES=$($Missing -join ',')"
    }
    throw 'Original Phase 173 failure evidence is missing. Use -PreviousEvidencePath with the unmodified four-file evidence directory.'
}
if (-not (Test-CompletePreviousEvidence $PreviousEvidence)) {
    $Missing = @($RequiredPreviousFiles | Where-Object {
        -not (Test-Path -LiteralPath (Join-Path $PreviousEvidence $_) -PathType Leaf)
    })
    Write-Output "PHASE173_FINAL_R2_PRIOR_EVIDENCE_DIR=$PreviousEvidence"
    Write-Output "PHASE173_FINAL_R2_MISSING_FILES=$($Missing -join ',')"
    if (-not $AllowMissingPriorEvidence -or $Missing.Count -ne $RequiredPreviousFiles.Count) {
        throw 'Partial previous evidence cannot be treated as missing; review the original files.'
    }
    Write-Output 'PHASE173_FINAL_R2_PRIOR_FAILURE_EVIDENCE=UNAVAILABLE_ORIGINAL_FILES'
} else {
    Write-Output 'PHASE173_FINAL_R2_PRIOR_FAILURE_EVIDENCE=VERIFIED_FOUR_FILES'
}
Write-Output "PHASE173_FINAL_R2_PRIOR_EVIDENCE_DIR=$PreviousEvidence"
$PriorArguments = @()
if ($AllowMissingPriorEvidence) {
    $PriorArguments += '--allow-missing-prior-evidence'
}
$Evidence = Join-Path $RecordParent 'EHPProofTracerRecovery\phase173_final_gate_r2'
$Report = Join-Path $Evidence 'phase173_full_test_report_r2.json'
$Attempt = Join-Path $Evidence 'phase173_full_test_attempt_r2.json'
$Stdout = Join-Path $Evidence 'active_suite_stdout_r2.txt'
$Stderr = Join-Path $Evidence 'active_suite_stderr_r2.txt'

Push-Location $Root
try {
    Write-Output 'PHASE173_FINAL_R2_SCOPE=CORRECTIVE_PHASE_END_ACTIVE_SUITE'
    Write-Output 'PHASE173_FINAL_R2_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
    Write-Output 'PHASE173_FINAL_R2_PRODUCTION_WRITES=NONE'
    Write-Output 'PHASE173_FINAL_R2_PREVIOUS_REPORT=IMMUTABLE'
    Write-Output 'PHASE173_FINAL_R2_BROWSER_PIXEL_LAYOUT=UNCONFIRMED'
    $BeforeIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to record Git index tree' }
    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'Unable to fetch origin/develop' }

    Write-Output '=== PHASE 173 FINAL R2 CONTRACT TESTS ==='
    & python -B -m pytest -q --tb=short -p no:cacheprovider `
        phase173_final_gate_r2_recovery/tests/test_gate_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'Final R2 gate contract tests failed' }

    & python -B -m phase173_final_gate_r2_recovery.gate preflight `
        --repo $Root --prior $PreviousEvidence @PriorArguments --attempt $Attempt --report $Report
    if ($LASTEXITCODE -ne 0) { throw 'Final R2 source/prior evidence preflight failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_FINAL_R2_DRY_RUN=PASS'
        Write-Output 'PHASE173_FINAL_R2_FULL_PYTEST=NOT_RUN_IN_DRY_RUN'
    }
    else {
        if (Test-Path $Report) {
            $Recorded = Get-Content -Path $Report -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($Recorded.status -ne 'PASS') { throw 'Prior R2 report is not PASS' }
            Write-Output 'PHASE173_FINAL_R2_FULL_PYTEST=PASS_PREVIOUSLY_RECORDED'
            Write-Output "PHASE173_FINAL_R2_FULL_PYTEST_PASSED=$($Recorded.pytest_passed_count)"
            Write-Output "PHASE173_FINAL_R2_REPORT=$Report"
        }
        else {
            & python -B -m phase173_final_gate_r2_recovery.gate start `
                --repo $Root --prior $PreviousEvidence @PriorArguments --attempt $Attempt --report $Report
            if ($LASTEXITCODE -ne 0) { throw 'Unable to record exclusive R2 attempt' }
            $PythonPath = (Get-Command python).Source
            Write-Output '=== PHASE 173 R2 ACTIVE FULL PYTEST (CORRECTIVE EXECUTION) ==='
            $Args = @('-B', '-m', 'pytest', '-q', '--tb=short', '--disable-warnings',
                '-p', 'no:cacheprovider', 'tests')
            $Process = Start-Process -FilePath $PythonPath -ArgumentList $Args `
                -WorkingDirectory $Root -RedirectStandardOutput $Stdout `
                -RedirectStandardError $Stderr -NoNewWindow -Wait -PassThru
            $TestExit = $Process.ExitCode
            Write-Output "PHASE173_FINAL_R2_PYTEST_EXIT=$TestExit"
            if (Test-Path $Stdout) { Get-Content $Stdout -Tail 45 }
            if ((Test-Path $Stderr) -and (Get-Item $Stderr).Length -gt 0) {
                Write-Output '=== R2 PYTEST STDERR ==='
                Get-Content $Stderr -Tail 30
            }
            & python -B -m phase173_final_gate_r2_recovery.gate finalize `
                --repo $Root --prior $PreviousEvidence @PriorArguments --attempt $Attempt `
                --report $Report --stdout $Stdout --stderr $Stderr --exit-code $TestExit
            if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R2 active pytest failed' }
        }
        Write-Output 'PHASE173_FINAL_R2_GATE=PASS'
        Write-Output 'PHASE173_FINAL_R2_PHASE_FORMALLY_CLOSED=NO_DOCUMENTATION_PENDING'
    }

    $AfterIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0 -or $AfterIndex -ne $BeforeIndex) {
        throw 'Phase 173 R2 modified the Git index'
    }
    Write-Output 'PHASE173_FINAL_R2_GIT_INDEX_PRESERVED=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read final Git status' }
    & git --no-pager diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read final Git diff'
    }
}
finally {
    Pop-Location
}
