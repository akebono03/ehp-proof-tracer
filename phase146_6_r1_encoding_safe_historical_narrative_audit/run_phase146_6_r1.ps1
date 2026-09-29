$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146-6-R1 Encoding-Safe Historical Narrative Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$HistoricalCommit = "908e24db89669750949fa9ad149f5e306ac05546"
$Worktree = Join-Path $env:TEMP "ehp_phase146_6_r1_historical"
$HistoricalOutput = Join-Path $ScriptDir "historical_phase136_2_pi6_3.utf8"
$CurrentOutput = Join-Path $ScriptDir "current_pi6_3.utf8"

$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile "$ScriptDir\audit_phase146_6_r1.py"
    if ($LASTEXITCODE -ne 0) { throw "Syntax preflight failed." }

    Write-Host ""
    Write-Host "B. Verifying historical commit..."
    git cat-file -e "$HistoricalCommit^{commit}"
    if ($LASTEXITCODE -ne 0) {
        git fetch origin $HistoricalCommit
        if ($LASTEXITCODE -ne 0) { throw "Could not fetch historical commit." }
    }

    Write-Host ""
    Write-Host "C. Creating temporary historical worktree..."
    if (Test-Path $Worktree) {
        git worktree remove --force $Worktree 2>$null
        Remove-Item -Recurse -Force $Worktree -ErrorAction SilentlyContinue
    }
    git worktree add --detach $Worktree $HistoricalCommit
    if ($LASTEXITCODE -ne 0) { throw "Could not create historical worktree." }

    Write-Host ""
    Write-Host "D. Capturing historical output as raw UTF-8 bytes..."
    Push-Location $Worktree
    try {
        $env:PYTHONPATH = $Worktree
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "python"
        $psi.Arguments = "main.py group-proof 3 3 --depth 2 --mode narrative"
        $psi.WorkingDirectory = $Worktree
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
        $psi.StandardErrorEncoding = [System.Text.Encoding]::UTF8
        $p = [System.Diagnostics.Process]::Start($psi)
        $stdout = $p.StandardOutput.ReadToEnd()
        $stderr = $p.StandardError.ReadToEnd()
        $p.WaitForExit()
        if ($p.ExitCode -ne 0) { throw "Historical rendering failed: $stderr" }
        [System.IO.File]::WriteAllText($HistoricalOutput, $stdout, (New-Object System.Text.UTF8Encoding($false)))
    }
    finally {
        Pop-Location
        Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    }

    Write-Host ""
    Write-Host "E. Capturing current output as raw UTF-8 bytes..."
    Push-Location $RepoRoot
    try {
        $env:PYTHONPATH = $RepoRoot
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "python"
        $psi.Arguments = "main.py group-proof 3 3 --depth 2 --mode narrative"
        $psi.WorkingDirectory = $RepoRoot
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
        $psi.StandardErrorEncoding = [System.Text.Encoding]::UTF8
        $p = [System.Diagnostics.Process]::Start($psi)
        $stdout = $p.StandardOutput.ReadToEnd()
        $stderr = $p.StandardError.ReadToEnd()
        $p.WaitForExit()
        if ($p.ExitCode -ne 0) { throw "Current rendering failed: $stderr" }
        [System.IO.File]::WriteAllText($CurrentOutput, $stdout, (New-Object System.Text.UTF8Encoding($false)))
    }
    finally {
        Pop-Location
        Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    }

    Write-Host ""
    Write-Host "F. Running encoding-safe semantic comparison..."
    Push-Location $RepoRoot
    try {
        python "$ScriptDir\audit_phase146_6_r1.py" $HistoricalOutput $CurrentOutput
        if ($LASTEXITCODE -ne 0) { throw "Audit failed." }
    }
    finally {
        Pop-Location
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
    if (Test-Path $Worktree) {
        Push-Location $RepoRoot
        try { git worktree remove --force $Worktree 2>$null }
        finally { Pop-Location }
        Remove-Item -Recurse -Force $Worktree -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 146-6-R1 audit complete."
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="
