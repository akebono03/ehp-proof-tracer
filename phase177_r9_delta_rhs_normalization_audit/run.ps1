param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
$previousBytecode = $env:PYTHONDONTWRITEBYTECODE
$previousUtf8 = $env:PYTHONUTF8
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    python -B -m phase177_r9_delta_rhs_normalization_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R9 preflight failed' }
    if (-not $DryRun) {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase177_r9_delta_rhs_normalization_audit/tests phase174_r3_r7_r9_composition_associativity/tests/test_rule.py phase175_r4r12r13r7_typed_nu_prime_notation/tests/test_r13r7_notation.py::test_actual_prior_and_source_are_same_strict_nu_prime_notation phase175_r4r12r13r7_typed_nu_prime_notation/tests/test_r13r7_notation.py::test_incompatible_dimensions_and_prime_or_family_rejected phase175_r4r12r13r7_typed_nu_prime_notation/tests/test_r13r7_notation.py::test_other_elements_are_not_identified_by_similar_suspension
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R9 focused tests failed' }
        python -B -m phase177_r9_delta_rhs_normalization_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R9 audit failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R9 git diff check failed' }
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
