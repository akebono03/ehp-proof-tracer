from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_typed_suppression_is_present_and_not_hardcoded_to_rule_name():
    src = (ROOT / "toda_group_proof_narrative_renderer.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "render_toda_group_proof_narrative_markdown"]
    assert len(functions) == 1
    body = ast.get_source_segment(src, functions[0])
    assert "isinstance(step.conclusion, CyclicStructureStatement)" in body
    assert "isinstance(premise.conclusion, QuotientIsomorphismStatement)" in body
    assert "suppressed_inference_labels" in body
    assert "infinite cyclic quotient structure" not in body

def test_no_legacy_renderer_switch():
    src = (ROOT / "phase165_r56_presentation_adapter.py").read_text(encoding="utf-8")
    assert "return render_completed_from_proofsteps" not in src
    assert "return render_toda_group_proof_narrative_markdown(presentation)" in src
