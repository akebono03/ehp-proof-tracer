$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 pi_(n+1)^n stable transport repair3"
Write-Host "active-public-renderer wrapper repair"
Write-Host "=============================================================="

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Set-Location $RepositoryRoot

Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Write-Host "[1/6] Audit active public renderer definitions"
python -c "import ast, pathlib; p=pathlib.Path('toda_group_proof_narrative_renderer.py'); t=ast.parse(p.read_text(encoding='utf-8')); xs=[n for n in t.body if isinstance(n, ast.FunctionDef) and n.name=='render_toda_group_proof_narrative_markdown']; print('top-level definitions:', len(xs)); print('line numbers:', [n.lineno for n in xs])"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/6] Apply repair3 wrapper and focused tests"
python "$PackageRoot\apply_phase159_pi_nplus1_n_stable_transport_repair3.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/6] Python syntax check"
python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase159_pi_nplus1_n_stable_transport.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/6] Focused stable-transport tests"
python -m pytest `
  ".\tests\test_phase159_pi_nplus1_n_stable_transport.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/6] Related Toda45 and pi4^3 regression tests"
python -m pytest `
  ".\tests\test_phase153_r2_toda45_map_property_semantic.py" `
  ".\tests\test_phase159_pi4_3_trailing_premise_order.py" `
  ".\tests\test_phase159_pi4_3_exactness_surjectivity_unification.py" `
  ".\tests\test_phase159_pi4_3_repair2g_reference_policy.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[6/6] Show pi_5^4 Narrative"
python -c "from tests.test_phase143_19_method_evidence import _method_evidence_data; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; p,_,_,_=_method_evidence_data(4,1); print(render_toda_group_proof_narrative_markdown(p))"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair3 focused verification completed"
Write-Host "Full test suite was NOT run."
Write-Host "=============================================================="
