$ErrorActionPreference = "Stop"
$repo = (Get-Location).Path
$pkg = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "=============================================================="
Write-Host "Phase 159 documentation closure - apply documentation only"
Write-Host "=============================================================="
$items = @(
    @{ Target = "README.md"; Append = "README_APPEND.md" },
    @{ Target = "docs/design.md"; Append = "design_APPEND.md" },
    @{ Target = "docs/development_log.md"; Append = "development_log_APPEND.md" },
    @{ Target = "docs/roadmap.md"; Append = "roadmap_APPEND.md" },
    @{ Target = "docs/proof_records.md"; Append = "proof_records_APPEND.md" }
)
foreach ($item in $items) {
    $target = Join-Path $repo $item.Target
    $append = Join-Path (Join-Path $pkg "updates") $item.Append
    if (-not (Test-Path $target)) { throw "Missing target: $($item.Target)" }
    $marker = "PHASE159_DOCUMENTATION_CLOSURE"
    $current = Get-Content -Raw -Encoding UTF8 $target
    if ($current.Contains($marker)) {
        Write-Host "Already updated: $($item.Target)"
        continue
    }
    $addition = Get-Content -Raw -Encoding UTF8 $append
    [System.IO.File]::WriteAllText($target, $current.TrimEnd() + "`r`n" + $addition.Replace("`n", "`r`n"), [System.Text.UTF8Encoding]::new($false))
    Write-Host "Updated: $($item.Target)"
}
Write-Host ""
Write-Host "No pytest command is executed by this closure package."
Write-Host ""
Write-Host "Changed files:"
Write-Host "  README.md"
Write-Host "  docs/design.md"
Write-Host "  docs/development_log.md"
Write-Host "  docs/roadmap.md"
Write-Host "  docs/proof_records.md"
