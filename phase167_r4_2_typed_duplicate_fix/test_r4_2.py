from __future__ import annotations
import ast
from pathlib import Path

def test_typed_duplicate_uses_two_statement_types():
    src=(Path(__file__).resolve().parent.parent/'toda_group_proof_narrative_renderer.py').read_text(encoding='utf-8')
    tree=ast.parse(src)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='render_toda_group_proof_narrative_markdown')
    code=ast.get_source_segment(src,fn)
    assert 'isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)' in code
    assert 'isinstance(step.conclusion, GeneratorSuspension)' in code
    assert 'suspension.source_generator == iterated.expression' in code
    assert 'suspension.target_generator == definition.element' in code

def test_r4_1_suppression_preserved():
    src=(Path(__file__).resolve().parent.parent/'toda_group_proof_narrative_renderer.py').read_text(encoding='utf-8')
    assert 'suppressed_inference_labels' in src
