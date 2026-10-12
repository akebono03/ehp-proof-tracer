param(
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$OutputDir = ''
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $ProjectRoot).Path.TrimEnd('\', '/')
$registryFile = Join-Path $root 'unified_statement_registry.py'
if (-not (Test-Path -LiteralPath $registryFile -PathType Leaf)) {
    throw 'EHP Proof Tracer project root not found: unified_statement_registry.py is missing.'
}
if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $OutputDir = Join-Path $root 'repository_cleanup_r1_output'
}
$out = [System.IO.Path]::GetFullPath($OutputDir).TrimEnd('\', '/')
$rootPrefix = $root + [System.IO.Path]::DirectorySeparatorChar
$outPrefix = $out + [System.IO.Path]::DirectorySeparatorChar
if (-not $out.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'OutputDir must be a child directory of ProjectRoot.'
}
New-Item -ItemType Directory -Path $out -Force | Out-Null

$files = @(Get-ChildItem -LiteralPath $root -Recurse -File -Force | Where-Object {
    $full = $_.FullName
    -not $full.StartsWith($outPrefix, [System.StringComparison]::OrdinalIgnoreCase) -and
    -not $full.StartsWith((Join-Path $root '.git') + '\', [System.StringComparison]::OrdinalIgnoreCase)
})

$records = @(
    foreach ($f in $files) {
        $rel = $f.FullName.Substring($root.Length).TrimStart('\', '/').Replace('\', '/')
        $name = $f.Name
        $category = 'REVIEW'
        $reason = 'Check usage and reproducibility before any deletion.'
        if ($rel -match '(^|/)(__pycache__|\.pytest_cache|\.mypy_cache|\.ruff_cache)(/|$)' -or $name -match '\.(pyc|pyo)$') {
            $category = 'CACHE_CANDIDATE'
            $reason = 'Regenerable cache candidate; not deleted by R1.'
        } elseif ($rel -match '(^|/)(docs|tests)/' -or $name -match '^(test_.*\.py|.*_test\.py)$' -or
                  $rel -match '^(README\.md|\.gitignore|pyproject\.toml|pytest\.ini|conftest\.py|requirements[^/]*|unified_statement_registry\.py|phase163_source_archive_registry\.py|phase163_source_archive_catalog\.json|phase163_r4_r85_archive_bridge\.py)$' -or
                  $rel -match '(^|/)(proof_records|development_log|design|roadmap)\.md$') {
            $category = 'PRESERVE'
            $reason = 'Core code, tests, documentation, or statement registry.'
        } elseif ($name -match '\.(json|tex|bib)$') {
            $category = 'PRESERVE'
            $reason = 'Structured data, source transcription, or bibliography.'
        } elseif ($name -match '\.bak$' -or $rel -match '(^|/)(backup[^/]*|[^/]*_backup[^/]*|[^/]*_output[^/]*|archive)/' -or $rel -match '^phase[0-9]+[^/]*/') {
            $category = 'REVIEW'
            $reason = 'Phase artifact, archived material, or backup: provenance may matter.'
        }
        [pscustomobject]@{
            Path = $rel
            Category = $category
            Reason = $reason
            Bytes = $f.Length
            LastWriteUtc = $f.LastWriteTimeUtc.ToString('o')
        }
    }
)
$records = @($records | Sort-Object Path)
$csvFile = Join-Path $out 'inventory.csv'
$jsonFile = Join-Path $out 'inventory.json'
$reportFile = Join-Path $out 'report.md'
$records | Export-Csv -LiteralPath $csvFile -NoTypeInformation -Encoding UTF8
ConvertTo-Json -InputObject $records -Depth 4 | Set-Content -LiteralPath $jsonFile -Encoding UTF8

$cacheCount = @($records | Where-Object { $_.Category -eq 'CACHE_CANDIDATE' }).Count
$reviewCount = @($records | Where-Object { $_.Category -eq 'REVIEW' }).Count
$preserveCount = @($records | Where-Object { $_.Category -eq 'PRESERVE' }).Count
$examples = @($records | Where-Object { $_.Category -eq 'CACHE_CANDIDATE' } | Select-Object -First 30 | ForEach-Object {
    '- ' + $_.Path
})
$lines = @(
    '# Repository Cleanup R1 - Read-only inventory',
    '',
    '- Project: ' + $root,
    '- Total files: ' + $records.Count,
    '- CACHE_CANDIDATE: ' + $cacheCount,
    '- REVIEW: ' + $reviewCount,
    '- PRESERVE: ' + $preserveCount,
    '',
    '## Cache candidate examples (up to 30)'
) + $examples + @(
    '',
    '## Interpretation',
    '- CACHE_CANDIDATE: cache only; no file has been deleted.',
    '- REVIEW: dependency and historical evidence check required.',
    '- PRESERVE: protected by conservative path or name rules.',
    '- This is a preliminary name/path classification, NOT a dependency audit.',
    '- R1 does not delete, move, or modify existing project files and does not run pytest.',
    '- R2 should inspect import and script references before deletion.',
    '- All classified files are listed in inventory.csv.'
)
$lines | Set-Content -LiteralPath $reportFile -Encoding UTF8
Write-Host "R1 complete: $($records.Count) files; CACHE_CANDIDATE=$cacheCount REVIEW=$reviewCount PRESERVE=$preserveCount"
Write-Host "Report: $reportFile"
