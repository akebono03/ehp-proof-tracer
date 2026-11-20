param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r7_lemma57_derived_source_proof.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R7 DryRun failed' }
    } else {
        python -B -m pytest -q phase176_r3r7_lemma57_derived_source_proof/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R7 focused pytest failed' }
        python -B -m phase176_r3r7_lemma57_derived_source_proof.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R7 audit failed' }
    }
} finally {
    Pop-Location
}
