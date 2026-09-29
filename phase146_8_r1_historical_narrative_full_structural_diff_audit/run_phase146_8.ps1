$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146-8 Historical Narrative Full Structural Diff Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$HistoricalCommit = "908e24db89669750949fa9ad149f5e306ac05546"
$Worktree = Join-Path $ScriptDir "_historical_phase136_2"
$HistoricalOut = Join-Path $ScriptDir "historical_pi6_3_narrative.txt"
$CurrentOut = Join-Path $ScriptDir "current_pi6_3_narrative.txt"
$Report = Join-Path $RepoRoot "phase146_8_historical_narrative_structural_diff.md"

$env:PYTHONIOENCODING = "utf-8"

function Invoke-Utf8Process {
    param(
        [string]$WorkingDirectory,
        [string]$FileName,
        [string[]]$Arguments,
        [string]$OutputPath
    )

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.FileName = $FileName
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
    $psi.StandardErrorEncoding = [System.Text.Encoding]::UTF8
    function Quote-ProcessArgument {
        param([string]$Value)

        if ($null -eq $Value) {
            return '""'
        }

        if ($Value -notmatch '[\s"]') {
            return $Value
        }

        return '"' + ($Value -replace '(\\*)"', '$1$1\\"' -replace '(\\+)$', '$1$1') + '"'
    }

    $psi.Arguments = (
        $Arguments |
        ForEach-Object {
            Quote-ProcessArgument $_
        }
    ) -join " "

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    [void]$process.Start()
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()

    if ($process.ExitCode -ne 0) {
        throw "Command failed: $FileName $($Arguments -join ' ')`n$stderr"
    }

    [System.IO.File]::WriteAllText(
        $OutputPath,
        $stdout,
        (New-Object System.Text.UTF8Encoding($false))
    )
}

try {
    Write-Host ""
    Write-Host "A. Preparing Phase 136-2 detached worktree..."
    if (Test-Path $Worktree) {
        git worktree remove --force $Worktree 2>$null
        Remove-Item -Recurse -Force $Worktree -ErrorAction SilentlyContinue
    }
    git worktree add --detach $Worktree $HistoricalCommit
    if ($LASTEXITCODE -ne 0) { throw "git worktree add failed." }

    Write-Host ""
    Write-Host "B. Capturing historical Phase 136-2 Narrative as strict UTF-8..."
    Invoke-Utf8Process `
      -WorkingDirectory $Worktree `
      -FileName "python" `
      -Arguments @("main.py", "group-proof", "3", "3", "--depth", "2", "--mode", "narrative") `
      -OutputPath $HistoricalOut

    Write-Host ""
    Write-Host "C. Capturing current local Narrative as strict UTF-8..."
    Write-Host "   This includes the locally applied Phase 146-7 change."
    Invoke-Utf8Process `
      -WorkingDirectory $RepoRoot `
      -FileName "python" `
      -Arguments @("main.py", "group-proof", "3", "3", "--depth", "2", "--mode", "narrative") `
      -OutputPath $CurrentOut

    Write-Host ""
    Write-Host "D. Running full structural diff classification..."
    python "$ScriptDir\audit_phase146_8.py" `
      $HistoricalOut `
      $CurrentOut `
      $Report
    if ($LASTEXITCODE -ne 0) { throw "Structural audit failed." }

    Write-Host ""
    Write-Host "E. UTF-8 integrity check..."
    python -c "from pathlib import Path; [Path(p).read_text(encoding='utf-8', errors='strict') for p in [r'$HistoricalOut', r'$CurrentOut', r'$Report']]; print('UTF-8 strict decode: PASS')"
    if ($LASTEXITCODE -ne 0) { throw "UTF-8 integrity check failed." }

    Write-Host ""
    Write-Host "F. Audit artifact..."
    Write-Host "   $Report"
}
finally {
    if (Test-Path $Worktree) {
        git worktree remove --force $Worktree 2>$null
        Remove-Item -Recurse -Force $Worktree -ErrorAction SilentlyContinue
    }
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 146-8 audit complete."
Write-Host "Production changes: none"
Write-Host "Full pytest suite intentionally not run."
Write-Host "=============================================================="
