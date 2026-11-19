param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 120
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r6_lemma57_source_screening_probe.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R6 DryRun failed' }
    } else {
        & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r3r6_lemma57_source_screening_probe/tests
        if ($LASTEXITCODE -ne 0) { throw 'R3R6 focused pytest failed' }
        & python -B -m phase176_r3r6_lemma57_source_screening_probe.audit --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'R3R6 source audit failed' }
    }
} finally {
    Pop-Location
}
