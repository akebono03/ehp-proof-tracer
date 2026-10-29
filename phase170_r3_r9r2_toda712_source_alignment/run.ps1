param(
    [switch]$AuditOnly,
    [switch]$AuditDomain
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedHead = 'fdf60522b6d477209e9d8d67720a63f9863e419c'
$R9Name = 'phase170_r3_r9_toda712_cited_rewrite'
$R9Root = Join-Path $RepoRoot $R9Name
$R9Source = Join-Path $R9Root 'source712.py'
$R9Runner = Join-Path $R9Root 'run.ps1'
$Fixer = Join-Path $PSScriptRoot 'fix_source712.py'
$RecoveryRoot = Join-Path $env:LOCALAPPDATA 'EHPProofTracerRecovery'
$RunStamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$Recovery = Join-Path $RecoveryRoot "phase170_r3_r9r2_$RunStamp"
$TrackedPaths = @(
    'phase168_r2_toda52_transport.py',
    'phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py'
)
$Succeeded = $false
$BackupsReady = $false
$TranscriptStarted = $false
$Python = 'python'
$OriginalPythonPath = $env:PYTHONPATH
$OriginalR9DryRun = [Environment]::GetEnvironmentVariable('PHASE170_R3R9_DRY_RUN')

try {
    New-Item -ItemType Directory -Path $Recovery -Force | Out-Null
    Start-Transcript -Path (Join-Path $Recovery 'transcript.txt') -Force | Out-Null
    $TranscriptStarted = $true
    Write-Output "PHASE170_R3R9R2_OUTPUT=$Recovery"

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'git is not on PATH'
    }
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw 'python is not on PATH'
    }

    Push-Location $RepoRoot
    try {
        $Branch = (& git branch --show-current | Out-String).Trim()
        $Head = (& git rev-parse HEAD | Out-String).Trim()
        if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
            throw "Expected local develop branch, got $Branch"
        }
        if ($Head -ne $ExpectedHead) {
            throw "Local HEAD mismatch: $Head (expected $ExpectedHead)"
        }
        $RemoteOutput = (& git ls-remote origin refs/heads/develop | Out-String).Trim()
        if ($LASTEXITCODE -ne 0 -or -not $RemoteOutput) {
            throw 'Cannot check GitHub origin/develop; do not modify code without checking'
        }
        $RemoteHead = ($RemoteOutput -split '\s+')[0]
        if ($RemoteHead -ne $ExpectedHead) {
            throw "Remote develop changed: $RemoteHead (expected $ExpectedHead)"
        }
        $TrackedStatus = (& git status --porcelain --untracked-files=no | Out-String).Trim()
        if ($LASTEXITCODE -ne 0 -or $TrackedStatus) {
            throw "Pre-existing tracked changes: $TrackedStatus"
        }
        Write-Output "PHASE170_R3R9R2_GIT_HEAD=$Head"
        Write-Output 'PHASE170_R3R9R2_TRACKED_BASELINE=CLEAN'

        if (-not (Test-Path $R9Source) -or -not (Test-Path $R9Runner)) {
            $Archive = Join-Path (Join-Path $HOME 'Downloads') 'phase170_r3_r9_toda712_cited_rewrite.zip'
            if (-not (Test-Path $Archive)) {
                throw 'Missing the original R3-R9 working package and its ZIP in Downloads'
            }
            Write-Output "PHASE170_R3R9R2_EXTRACT_ORIGINAL=$Archive"
            Expand-Archive -Path $Archive -DestinationPath $RepoRoot -Force
        }
        if (-not (Test-Path $R9Source) -or -not (Test-Path $R9Runner)) {
            throw 'Original R3-R9 source712.py or run.ps1 is still missing'
        }

        & $Python $Fixer --repo $RepoRoot --audit
        if ($LASTEXITCODE -ne 0) {
            throw 'R3-R9R2 preflight failed: original TeX or CLAUSE structure mismatch'
        }
        if ($AuditOnly) {
            $Succeeded = $true
            Write-Output 'PHASE170_R3R9R2_AUDIT_ONLY=PASS'
            return
        }

        # Both tracked files are untouched at this point. Save them before
        # invoking the original R3-R9 implementation + focused tests.
        foreach ($Relative in $TrackedPaths) {
            $Target = Join-Path $RepoRoot $Relative
            if (-not (Test-Path $Target)) {
                throw "Missing baseline: $Relative"
            }
            $Backup = Join-Path (Join-Path $Recovery 'tracked_before') $Relative
            New-Item -ItemType Directory -Path (Split-Path $Backup -Parent) -Force | Out-Null
            Copy-Item -LiteralPath $Target -Destination $Backup
        }
        Copy-Item -LiteralPath $R9Source -Destination (Join-Path $Recovery 'source712.py.before')
        $BackupsReady = $true

        & $Python $Fixer --repo $RepoRoot --apply
        if ($LASTEXITCODE -ne 0) {
            throw 'R3-R9R2 source correction refused'
        }
        Write-Output 'PHASE170_R3R9R2_SOURCE_ALIGNED=PASS'

        # Reuse R3-R9's original patch runner, its own rollback safeguards,
        # and its original focused test selection. No whole-suite pytest.
        # Force a real focused run even if the earlier dry-run flag persists.
        Remove-Item Env:\PHASE170_R3R9_DRY_RUN -ErrorAction SilentlyContinue
        & powershell -NoProfile -ExecutionPolicy Bypass -File $R9Runner
        if ($LASTEXITCODE -ne 0) {
            throw "Original R3-R9 focused runner failed (exit $LASTEXITCODE)"
        }
        Write-Output 'PHASE170_R3R9R2_ORIGINAL_FOCUSED=PASS'

        # The additional tests import fix_source712 from this package.
        $env:PYTHONPATH = "$PSScriptRoot;$RepoRoot;$OriginalPythonPath"
        $FocusedTests = @(
            (Join-Path $R9Root 'tests/test_toda712_rewrite.py'),
            (Join-Path $PSScriptRoot 'tests/test_toda712_source.py'),
            (Join-Path $PSScriptRoot 'tests/test_patch_safety.py')
        )
        & $Python -m pytest -q @FocusedTests
        if ($LASTEXITCODE -ne 0) {
            throw "R3-R9R2 added focused tests failed (exit $LASTEXITCODE)"
        }
        Write-Output 'PHASE170_R3R9R2_EXTRA_FOCUSED=PASS'

        if ($AuditDomain) {
            # The earlier R8R2 package is audit-only. Do not guess its path.
            $AuditRunners = @(
                Get-ChildItem -Path $RepoRoot -Directory -Filter 'phase170_r3_r8r2*' |
                    ForEach-Object { Join-Path $_.FullName 'run.ps1' } |
                    Where-Object { Test-Path $_ }
            )
            if ($AuditRunners.Count -ne 1) {
                throw "Expected one existing R8R2 domain audit runner, found $($AuditRunners.Count)"
            }
            & powershell -NoProfile -ExecutionPolicy Bypass -File $AuditRunners[0]
            if ($LASTEXITCODE -ne 0) {
                throw 'R8R2 domain audit runner failed'
            }
            Write-Output 'PHASE170_R3R9R2_DOMAIN_AUDIT_EXECUTED=YES'
        }

        $Succeeded = $true
        Write-Output 'PHASE170_R3R9R2=PASS'
        & git status -sb
    }
    finally {
        Pop-Location
    }
}
catch {
    Write-Output "PHASE170_R3R9R2_REFUSED=$($_.Exception.Message)"
    throw
}
finally {
    if (-not $Succeeded -and $BackupsReady) {
        foreach ($Relative in $TrackedPaths) {
            $Target = Join-Path $RepoRoot $Relative
            $Backup = Join-Path (Join-Path $Recovery 'tracked_before') $Relative
            if (Test-Path $Backup) {
                Copy-Item -LiteralPath $Backup -Destination $Target -Force
                Write-Output "PHASE170_R3R9R2_RESTORED=$Relative"
            }
        }
        $SourceBackup = Join-Path $Recovery 'source712.py.before'
        if (Test-Path $SourceBackup) {
            Copy-Item -LiteralPath $SourceBackup -Destination $R9Source -Force
            Write-Output "PHASE170_R3R9R2_RESTORED=$R9Name/source712.py"
        }
    }
    $env:PYTHONPATH = $OriginalPythonPath
    if ($null -eq $OriginalR9DryRun) {
        Remove-Item Env:\PHASE170_R3R9_DRY_RUN -ErrorAction SilentlyContinue
    } else {
        $env:PHASE170_R3R9_DRY_RUN = $OriginalR9DryRun
    }
    if ($TranscriptStarted) {
        Stop-Transcript | Out-Null
    }
}
