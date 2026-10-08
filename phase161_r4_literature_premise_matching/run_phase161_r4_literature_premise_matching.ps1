$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Output "Repository root: $root"
$required = @('proof.py', 'toda_rules.py', 'phase161_backward_goal_schema.py', 'phase161_r3_backward_goal_schema.py', 'tests\test_phase59_n3_ehp_chain.py')
foreach ($file in $required) {
    if (-not (Test-Path (Join-Path $root $file))) {
        throw "Required repository file not found: $file"
    }
}
Copy-Item (Join-Path $package 'phase161_r4_literature_premise_matching.py') (Join-Path $root 'phase161_r4_literature_premise_matching.py') -Force
Copy-Item (Join-Path $package 'tests\test_phase161_r4_literature_premise_matching.py') (Join-Path $root 'tests\test_phase161_r4_literature_premise_matching.py') -Force
python -B -m pytest -q tests/test_phase161_r2_backward_goal_schema.py tests/test_phase161_r3_backward_goal_schema.py tests/test_phase161_r4_literature_premise_matching.py
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Output 'Phase 161 R4 focused tests passed; entire suite not run.'
