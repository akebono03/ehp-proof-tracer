from __future__ import annotations
from pathlib import Path
from types import SimpleNamespace
import ast

from proof import ProofRule
from phase167_r4_9_proofstep_reference_unification.patch import transform, function_bounds


def test_r49_existing_function_no_rule_name_or_type_specialization():
    file_path = Path(__file__).resolve().parents[1] / 'toda_group_proof_narrative_contribution_renderer.py'
    text = file_path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    a, b = function_bounds(text, 'link_toda_group_proof_narrative_reference_body_consumers')
    function = text[a:b]
    assert 'specialize_typed_statement(' not in function
    assert '"specializ"' not in function
    assert 'derived_step.premises[0] is not edge.premise_step' in function
    ast.parse(text)


def test_r49_reference_for_toda51_zero_and_diagonal_in_web():
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(3, 1, max_depth=2, mode='narrative')
    rows = [(line.prefix, line.statement_latex or '', line.suffix) for line in view.rendered_lines]
    zero_rows = [(prefix, math) for prefix, math, _ in rows if math.strip() == r'\pi_{4}^{5} = 0']
    diagonal_rows = [(prefix, math) for prefix, math, _ in rows if math.strip() == r'\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}']
    assert zero_rows, 'pi_4^5 zero not visible'
    assert any('[R' in prefix and 'より' in prefix for prefix, _ in zero_rows)
    assert diagonal_rows
    assert any('[R' in prefix and 'より' in prefix for prefix, _ in diagonal_rows)
