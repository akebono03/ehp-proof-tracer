param([switch]$DryRun, [int]$TimeoutSeconds = 120)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r5_lemma57_right_composition_frontier.audit --dry-run --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R5 DryRun failed' }
    } else {
        & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r3r5_lemma57_right_composition_frontier/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R5 focused tests failed' }
        & python -B -m phase176_r3r5_lemma57_right_composition_frontier.audit --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R5 audit failed' }
    }
} finally { Pop-Location }
