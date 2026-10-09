$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not (Test-Path (Join-Path $repo 'phase162_pi5_3_backward_selection.py'))) {
    throw 'Phase 162 backward selection is missing. Unzip this package in the repository root.'
}
$oldPythonPath = $env:PYTHONPATH
try {
    $parts = @($repo, (Join-Path $repo 'tests'), $PSScriptRoot)
    if (-not [string]::IsNullOrEmpty($oldPythonPath)) { $parts += $oldPythonPath }
    $env:PYTHONPATH = $parts -join ';'
    python -B -m pytest -q (Join-Path $PSScriptRoot 'test_phase162_pi5_3_renderer_audit.py')
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
    $output = Join-Path $PSScriptRoot 'pi5_3_reconstructed_narrative.md'
    @'
from pathlib import Path
from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data
from toda_rules import toda_eta_family_definition_statement
from phase162_pi5_3_renderer_audit import render_phase162_pi5_3_reconstructed_proof
import sys
pi4_2_step = build_phase59_2_data()['result_steps'][0]
definitions = tuple(ProofStep(conclusion=toda_eta_family_definition_statement(i), premises=(), rule=ProofRule.GIVEN) for i in (3, 4))
leaves = build_phase59_3_data()['premise_steps']
audit = render_phase162_pi5_3_reconstructed_proof(pi4_2_step, definitions, leaves)
Path(sys.argv[1]).write_text(audit.markdown, encoding='utf-8')
print('Root:', repr(audit.final_step.conclusion))
print('Presentation nodes:', len(audit.presentation.nodes))
print('Presentation edges:', len(audit.presentation.edges))
print('Markdown characters:', len(audit.markdown))
print('Output:', sys.argv[1])
print('\n----- PUBLIC NARRATIVE -----\n')
print(audit.markdown)
'@ | python -B - $output
    if ($LASTEXITCODE -ne 0) { throw "Renderer audit failed: $LASTEXITCODE" }
    Write-Host 'Focused renderer audit completed. Full suite not run.'
} finally {
    $env:PYTHONPATH = $oldPythonPath
}
