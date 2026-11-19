param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'Expected develop branch' }
    $pins = @{
        'phase174_r3_r7_r7_composite_zero_audit/rule.py' = 'd98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6'
        'phase169_r10e5_composite_generator_image/rule.py' = '01acace3eb273d47091421a61291ee54b51c369f'
        'phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py' = '6aa48096b41714fbdf588c3ba423d264a4a13bb9'
    }
    foreach ($path in $pins.Keys) {
        $sha = (git rev-parse "HEAD:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $sha -ne $pins[$path]) { throw "Source blob mismatch: $path" }
        $worktreeSha = (git hash-object $path).Trim()
        if ($LASTEXITCODE -ne 0 -or $worktreeSha -ne $pins[$path]) { throw "Worktree source differs: $path" }
    }
    Write-Output 'PHASE175_R4R14R4_SOURCE_GUARD=PASS'
    Write-Output 'PHASE175_R4R14R4_NEW_GIVEN=0'
    Write-Output 'PHASE175_R4R14R4_PRODUCTION_CHANGED=0'
    if ($DryRun) {
        Write-Output 'PHASE175_R4R14R4_GATE=PASS_DRYRUN_SOURCE_GUARD'
        exit 0
    }
    python -m pytest --import-mode=importlib -q `
        phase175_r4r14r4_general_zero_transport/tests/test_rule.py `
        phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py `
        phase174_r3_r7_r7_composite_zero_audit/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R4 focused pytest failed' }
    Write-Output 'PHASE175_R4R14R4_GATE=PASS_ISOLATED_GENERIC_ZERO_TRANSPORT'
    Write-Output 'PHASE175_R4R14R4_PUBLIC_PROOF_COMPLETE=False'
} finally {
    Pop-Location
}
