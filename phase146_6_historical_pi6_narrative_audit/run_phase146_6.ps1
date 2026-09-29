$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146-6 Historical pi_6^3 Narrative vs Current Generic Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$HistoricalCommit = "908e24db89669750949fa9ad149f5e306ac05546"
$Worktree = Join-Path $env:TEMP "ehp_phase146_6_historical"
$HistoricalOutput = Join-Path $ScriptDir "historical_phase136_2_pi6_3.txt"
$CurrentOutput = Join-Path $ScriptDir "current_generic_pi6_3.txt"
$DiffOutput = Join-Path $RepoRoot "phase146_6_historical_vs_current.diff"

$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile "$ScriptDir\audit_phase146_6.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Syntax preflight failed."
    }

    Write-Host ""
    Write-Host "B. Verifying historical commit..."
    git cat-file -e "$HistoricalCommit^{commit}"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Historical commit is not available locally; fetching it..."
        git fetch origin $HistoricalCommit
        if ($LASTEXITCODE -ne 0) {
            throw "Could not fetch historical commit."
        }
    }

    Write-Host ""
    Write-Host "C. Creating temporary historical worktree..."
    if (Test-Path $Worktree) {
        git worktree remove --force $Worktree 2>$null
        Remove-Item -Recurse -Force $Worktree -ErrorAction SilentlyContinue
    }
    git worktree add --detach $Worktree $HistoricalCommit
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create historical worktree."
    }

    Write-Host ""
    Write-Host "D. Rendering historical Phase 136-2 pi_6^3 Narrative..."
    Push-Location $Worktree
    try {
        $env:PYTHONPATH = $Worktree
        python main.py group-proof 3 3 --depth 2 --mode narrative |
            Out-File -FilePath $HistoricalOutput -Encoding utf8
        if ($LASTEXITCODE -ne 0) {
            throw "Historical Narrative rendering failed."
        }
    }
    finally {
        Pop-Location
        Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    }

    Write-Host ""
    Write-Host "E. Rendering current pi_6^3 Narrative..."
    Push-Location $RepoRoot
    try {
        $env:PYTHONPATH = $RepoRoot
        python main.py group-proof 3 3 --depth 2 --mode narrative |
            Out-File -FilePath $CurrentOutput -Encoding utf8
        if ($LASTEXITCODE -ne 0) {
            throw "Current Narrative rendering failed."
        }
    }
    finally {
        Pop-Location
        Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    }

    Write-Host ""
    Write-Host "F. Comparing historical and current output..."
    Push-Location $RepoRoot
    try {
        python "$ScriptDir\audit_phase146_6.py" `
            $HistoricalOutput `
            $CurrentOutput
        if ($LASTEXITCODE -ne 0) {
            throw "Historical/current comparison failed."
        }
    }
    finally {
        Pop-Location
    }

    if (Test-Path (Join-Path $RepoRoot "phase146_6_historical_vs_current.diff")) {
        Write-Host ""
        Write-Host "Diff file:"
        Write-Host "  $DiffOutput"
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue

    if (Test-Path $Worktree) {
        Push-Location $RepoRoot
        try {
            git worktree remove --force $Worktree 2>$null
        }
        finally {
            Pop-Location
        }
        Remove-Item -Recurse -Force $Worktree -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 146-6 audit complete."
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="
