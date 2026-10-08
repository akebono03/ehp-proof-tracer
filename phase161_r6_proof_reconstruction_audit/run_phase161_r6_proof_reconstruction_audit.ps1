$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Repository root: $Root"
$Required = @('phase161_backward_goal_schema.py','phase161_r3_backward_goal_schema.py','phase161_r4_literature_premise_matching.py','phase161_r5_backward_proof_reconstruction.py','tests/test_phase59_n3_ehp_chain.py')
foreach ($Relative in $Required) {
    if (-not (Test-Path (Join-Path $Root $Relative))) {
        throw "Missing prerequisite: $Relative"
    }
}
Copy-Item (Join-Path $Package 'tests/test_phase161_r6_proof_reconstruction_audit.py') (Join-Path $Root 'tests/test_phase161_r6_proof_reconstruction_audit.py') -Force
python -B -m pytest -q tests/test_phase161_r6_proof_reconstruction_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R6 focused audit failed' }
Write-Host 'R6 focused audit passed. Entire suite NOT run.'
