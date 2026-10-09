from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_transport_link.py'
source = TARGET.read_text(encoding='utf-8')
module = ast.parse(source)
fn = next(x for x in module.body if isinstance(x, ast.FunctionDef) and x.name=='render_suspension_transport_link')
old = ''.join(source.splitlines(keepends=True)[fn.lineno-1:fn.end_lineno])
new = '''def render_suspension_transport_link(
    root: ProofStep,
    render_step_latex: Callable[[ProofStep], str | None],
) -> str | None:
    """Describe a transport only when its destination is the current goal.

    A transport found solely in a subsidiary proof cannot be appended to
    the narrative of an unrelated target group.
    """
    facts = extract_suspension_transport_facts(root)
    if facts is None:
        return None
    if root.conclusion.lhs == facts.source_group_step.conclusion.lhs:
        return None
    if not _concrete_toda_group_matches_structural_group(
        root.conclusion.lhs,
        facts.transported_group_step.conclusion.lhs,
    ):
        return None
    source = render_step_latex(facts.source_group_step)
    isomorphism = render_step_latex(facts.isomorphism_step)
    transported = render_step_latex(facts.transported_group_step)
    bridge = render_step_latex(facts.generator_bridge_step)
    if not all((source, isomorphism, transported, bridge)):
        return None
    return (
        "証明木に記録された群構造の移送について、"
        f"${source}$ と ${isomorphism}$ から ${transported}$ を得る。"
        f"生成元の対応は ${bridge}$ である。"
    )
'''
imports = '''from toda_stable_group_transport import (
    _concrete_toda_group_matches_structural_group,
)
'''
assert '_concrete_toda_group_matches_structural_group' not in source
assert old in source
updated = source.replace('from proof import ProofStep\n', 'from proof import ProofStep\n'+imports, 1).replace(old,new,1)
ast.parse(updated)
backup = TARGET.with_suffix('.py.phase162_r10_r7.bak')
shutil.copy2(TARGET,backup)
TARGET.write_text(updated, encoding='utf-8')
print('Updated:',TARGET)
print('Backup:',backup)
