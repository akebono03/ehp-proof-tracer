from __future__ import annotations
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADAPTER = ROOT / 'phase165_r56_presentation_adapter.py'
STEPS = ROOT / 'phase165_r57_r10_step_narrative.py'

def replace_adapter(source: str) -> str:
    tree = ast.parse(source)
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'render_completed_shared_narrative']
    if len(functions) != 1:
        raise RuntimeError('adapter function not found exactly once')
    node = functions[0]
    old = '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno])
    for term in ('has_transport_proof_ancestry', 'render_completed_from_proofsteps', '_phase160_r7_render_stable_finite_cyclic_transport_narrative'):
        if term not in old:
            raise RuntimeError('adapter source differs, missing '+term)
    new = '''def render_completed_shared_narrative(result: PartialProofResult) -> str:
    """Render a completed typed proof through the existing shared Narrative renderer."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is not ProofSearchStatus.COMPLETE or result.conclusion is None:
        raise ValueError("a complete search is required")
    conclusion = result.conclusion
    if getattr(conclusion, "lhs", None) != result.target:
        raise ValueError("completed target does not match conclusion")
    structure = getattr(conclusion, "rhs", None)
    if not isinstance(structure, (FreeCyclicGroup, FiniteCyclicGroup, DirectSumGroup)):
        raise ValueError("unsupported group structure in completed goal")
    roots = [step for step in result.proven_steps if step.conclusion == conclusion]
    if len(roots) != 1 or roots[0].rule is not ProofRule.INFERENCE:
        raise ValueError("completed proof must contain exactly one derived root")
    root = roots[0]
    if isinstance(structure, FreeCyclicGroup):
        generators = (structure.generator,)
        orders = (None,)
    elif isinstance(structure, FiniteCyclicGroup):
        generators = (structure.generator,)
        orders = (structure.order,)
    else:
        raise ValueError("direct-sum presentation requires typed generators")
    entry = ProofRepositoryEntry(key="phase165:typed:completed", step=root, phase="165")
    group_result = TodaGroupResult(
        target=result.target,
        group_structure=structure,
        generators=generators,
        generator_orders=orders,
        source_entry=entry,
        proof_step=root,
    )
    replay = build_complete_toda_group_result_proof_replay(group_result)
    presentation = build_toda_group_proof_presentation(replay)
    return render_toda_group_proof_narrative_markdown(presentation)'''
    lines=source.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1])+new+'\n'+''.join(lines[node.end_lineno:])

def replace_steps(source: str) -> str:
    tree=ast.parse(source)
    remove={'_math_statement','_reference_label','render_completed_from_proofsteps'}
    found={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in remove}
    if set(found)!=remove: raise RuntimeError('old renderer functions not all present')
    lines=source.splitlines(keepends=True)
    for n in sorted(found.values(),key=lambda n:n.lineno,reverse=True):
        start=n.lineno-1
        # Include preceding blank lines but preserve section spacing
        while start>0 and not lines[start-1].strip() and (start-(n.lineno-1))>-3:
            start-=1
        del lines[start:n.end_lineno]
    output=''.join(lines)
    for oldline in (
        'from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus\n',
        'from toda_group_proof_narrative_shared_components import _render_generic_narrative_step\n',
        'from web_group_proof_common import _group_proof_statement_latex\n',
    ):
        if oldline not in output: raise RuntimeError('step module import differs: '+oldline)
        output=output.replace(oldline,'',1)
    if 'from proof import ProofRule, ProofStep\n' not in output: raise RuntimeError('proof import differs')
    ast.parse(output)
    return output

def main():
    a=ADAPTER.read_text(encoding='utf-8-sig')
    s=STEPS.read_text(encoding='utf-8-sig')
    new_a=replace_adapter(a)
    new_s=replace_steps(s)
    ast.parse(new_a); ast.parse(new_s)
    ADAPTER.write_text(new_a,encoding='utf-8')
    STEPS.write_text(new_s,encoding='utf-8')
    print('MODIFIED: phase165_r56_presentation_adapter.py: render_completed_shared_narrative')
    print('MODIFIED: phase165_r57_r10_step_narrative.py: removed 3 obsolete functions and unused imports')
    print('KEPT: ordered_proof_ancestry and has_transport_proof_ancestry')

if __name__=='__main__': main()
