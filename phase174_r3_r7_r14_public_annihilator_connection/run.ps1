param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$PatchAttempted = $false
$BackupPath = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r3_r7_r14\phase165_r52_r9_shared_math.original.py'
$TargetPath = Join-Path $RepoRoot 'phase165_r52_r9_shared_math.py'

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Preflight must run before modifying a single tracked source file.
    & python -B -m phase174_r3_r7_r14_public_annihilator_connection.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R14 source-first preflight failed: $LASTEXITCODE" }
    & python -B -m phase174_r3_r7_r14_public_annihilator_connection.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R14 guarded patch dry-run failed: $LASTEXITCODE" }

    # Each group runs in a separate process to avoid test_rule.py basename collisions.
    $Groups = @(
        @{ Name = 'R14'; Paths = @(
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_patch.py',
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_audit.py'
        ) },
        @{ Name = 'R13'; Paths = @(
            '.\phase174_r3_r7_r13_cited_annihilator_bridge\tests\test_registry.py',
            '.\phase174_r3_r7_r13_cited_annihilator_bridge\tests\test_audit.py'
        ) },
        @{ Name = 'R12'; Paths = @(
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_source.py',
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_rule.py',
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_audit.py'
        ) },
        @{ Name = 'R11'; Paths = @(
            '.\phase174_r3_r7_r11_canonical_fixture_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R10'; Paths = @(
            '.\phase174_r3_r7_r10_cited_family_gap_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R9'; Paths = @(
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py',
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_audit.py'
        ) },
        @{ Name = 'R8'; Paths = @(
            '.\phase174_r3_r7_r8_composite_image_gap\tests\test_audit.py'
        ) },
        @{ Name = 'R7'; Paths = @(
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_rule.py',
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R6'; Paths = @(
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_rule.py',
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_audit.py'
        ) },
        @{ Name = 'R5'; Paths = @(
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py',
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_audit.py'
        ) },
        @{ Name = 'R4'; Paths = @(
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
        ) },
        @{ Name = 'R3'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py'
        ) },
        @{ Name = 'MATH_REGRESSION'; Paths = @(
            '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
            '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py',
            '.\phase165_r14_r9_ehp_exactness\test_phase165_r14_r9_ehp_exactness.py'
        ) },
        @{ Name = 'FAMILY_REGRESSION'; Paths = @(
            '.\phase169_r10d2_general_family_definition\tests\test_r10d2_general_family.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Missing focused test: $TestPath"
            }
        }
    }
    Write-Output 'PHASE174_R3R7R14_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R14_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) {
            throw "R14 $($Group.Name) focused pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R14_FOCUSED_PYTEST=PASS'
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R14_GATE=PASS_PREFLIGHT'
    }
    else {
        $PatchAttempted = $true
        & python -B -m phase174_r3_r7_r14_public_annihilator_connection.patch
        if ($LASTEXITCODE -ne 0) { throw "R14 guarded apply failed: $LASTEXITCODE" }
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw "R14 public integration pytest failed: $LASTEXITCODE" }
        & python -B -m phase174_r3_r7_r14_public_annihilator_connection.audit
        if ($LASTEXITCODE -ne 0) { throw "R14 public source-first audit failed: $LASTEXITCODE" }
    }
    Write-Output '(END)'
}
catch {
    $TrackedAfterError = @(git diff --name-only)
    if ($PatchAttempted -and (Test-Path -LiteralPath $BackupPath) -and
        ($TrackedAfterError -contains 'phase165_r52_r9_shared_math.py')) {
        Copy-Item -LiteralPath $BackupPath -Destination $TargetPath -Force
        Write-Output 'PHASE174_R3R7R14_ROLLBACK=ORIGINAL_SOURCE_RESTORED'
    }
    throw
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
