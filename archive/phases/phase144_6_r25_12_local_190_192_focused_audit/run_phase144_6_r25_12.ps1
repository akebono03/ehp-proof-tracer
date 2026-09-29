$ErrorActionPreference = "Stop"

$Base = "5a7c4f077b"
$Out = Join-Path $PSScriptRoot "phase144_6_r25_12_local_diff_report.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-12 Local 190 -> 192 Focused Audit"
Write-Host "Production changes: NONE"
Write-Host "Historical worktree search: NONE"
Write-Host "=============================================================="

if (-not (Test-Path ".git")) {
    throw "Run this script from the ehp-proof-tracer repository root."
}

git cat-file -e "$Base^{commit}"
if ($LASTEXITCODE -ne 0) {
    throw "Base commit $Base is not available locally."
}

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("Phase 144-6 R25-12 Local 190 -> 192 Focused Audit")
$lines.Add("base=$Base")
$lines.Add("head=$(git rev-parse HEAD)")
$lines.Add("branch=$(git branch --show-current)")
$lines.Add("")

$lines.Add("=== A. git status --short ===")
$lines.AddRange([string[]](git status --short))
$lines.Add("")

$lines.Add("=== B. committed production diff: base -> HEAD ===")
$committed = git diff --name-status $Base HEAD -- "*.py"
$committed = @($committed | Where-Object {
    $_ -notmatch '(^|[\\/])tests[\\/]' -and
    $_ -notmatch '(^|[\\/])phase144_6_' -and
    $_ -notmatch '(^|[\\/])audit_'
})
if ($committed.Count -eq 0) {
    $lines.Add("(none)")
} else {
    $lines.AddRange([string[]]$committed)
}
$lines.Add("")

$lines.Add("=== C. local production diff: HEAD -> working tree ===")
$local = git diff --name-status HEAD -- "*.py"
$local = @($local | Where-Object {
    $_ -notmatch '(^|[\\/])tests[\\/]' -and
    $_ -notmatch '(^|[\\/])phase144_6_' -and
    $_ -notmatch '(^|[\\/])audit_'
})
if ($local.Count -eq 0) {
    $lines.Add("(none)")
} else {
    $lines.AddRange([string[]]$local)
}
$lines.Add("")

$lines.Add("=== D. local production patch ===")
$patch = git diff HEAD -- "*.py"
if ([string]::IsNullOrWhiteSpace(($patch -join "`n"))) {
    $lines.Add("(none)")
} else {
    $lines.AddRange([string[]]$patch)
}
$lines.Add("")

$lines.Add("=== E. TodaSuspensionInjectiveStatement occurrences in changed production files ===")
$changedFiles = @()
foreach ($entry in $local) {
    $parts = $entry -split "`t"
    if ($parts.Count -ge 2) {
        $path = $parts[-1]
        if (Test-Path $path) {
            $changedFiles += $path
        }
    }
}
if ($changedFiles.Count -eq 0) {
    $lines.Add("(no locally changed production files)")
} else {
    foreach ($path in $changedFiles) {
        $hits = Select-String -Path $path -Pattern "TodaSuspensionInjectiveStatement|argument_frontier_hidden_step_ids|semantic_closure|participating" -Context 5,5
        if ($hits) {
            $lines.Add("--- $path ---")
            foreach ($hit in $hits) {
                $lines.Add($hit.ToString())
            }
        }
    }
}
$lines.Add("")

$lines.Add("=== F. diff against known 190 commit for changed production files only ===")
if ($changedFiles.Count -eq 0) {
    $lines.Add("(no locally changed production files)")
} else {
    foreach ($path in ($changedFiles | Sort-Object -Unique)) {
        $lines.Add("--- $path ---")
        $d = git diff $Base -- $path
        if ([string]::IsNullOrWhiteSpace(($d -join "`n"))) {
            $lines.Add("(no diff)")
        } else {
            $lines.AddRange([string[]]$d)
        }
    }
}

$lines | Set-Content -Encoding UTF8 $Out

Write-Host ""
Write-Host "Audit complete."
Write-Host "Report:"
Write-Host "  $Out"
Write-Host ""
Write-Host "Please paste the report contents back into ChatGPT."
