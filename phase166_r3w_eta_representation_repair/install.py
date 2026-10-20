"""Idempotent, narrow install on R3-U and R3-V working tree."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODULE = ROOT / 'phase166_r3v_generator_transport.py'
SHARED = ROOT / 'phase165_r52_r9_shared_math.py'
GATE = ROOT / 'phase165_r57_r11_proof_order_gate.py'
TEST = ROOT / 'phase166_r3v_existing_evidence_bridge' / 'test_r3v.py'
OLD = 'options.extend(expand_generator_transport_normalization(goal))'
NEW = 'options.extend(expand_generator_transport_normalization(goal, tuple(available)))'

TEST_SOURCE = '''def test_r3v_registered_prior_and_shared_search_connection():
    transported, named, witness = _case()
    bridge = build_shared_typed_bridge()
    target_id = 'shared:2:toda:adopted:prop5.1:higher_eta_group_relation'
    screened = screen_shared_proof_context(
        bridge, goal=named, citing_assertion_id=target_id,
        explicit_publication_target=True,
    )
    prior = [
        link.step.conclusion for link in screened.proof_links
        if link.step is not None
        and isinstance(link.step.conclusion, Relation)
        and link.step.conclusion.lhs == TodaPrimaryGroup(4, 3)
        and isinstance(link.step.conclusion.rhs, FiniteCyclicGroup)
        and link.step.conclusion.rhs.order == 2
    ]
    assert prior
    options = shared_expansion_provider(screened, proof_target=named)(named)
    assert any(
        option.subgoals[0].rhs.generator.expression == prior[0].rhs.generator
        and option.subgoals[1] == witness
        for option in options
        if len(option.subgoals) == 2
        and isinstance(option.subgoals[0], Relation)
        and isinstance(option.subgoals[0].rhs, FiniteCyclicGroup)
        and isinstance(option.subgoals[0].rhs.generator, IteratedSuspension)
    )
'''

GATE_SOURCE = '''def _proved_generator_suspension_normalization_shape(root_goal: object, expansion: GoalExpansion) -> bool:
    """Permit a proven eta-name normalization, not unproved group self-citation."""
    from expression import IteratedSuspension
    from homotopy_groups import TodaSuspensionMap
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase165_r12_r28_presentation_connection import _matching_eta_name

    if getattr(expansion.rule, "name", None) != "proved generator suspension normalizes transported cyclic group":
        return False
    if len(expansion.subgoals) != 2:
        return False
    transported, witness = expansion.subgoals
    if not (isinstance(root_goal, Relation)
            and root_goal.relation_type is RelationType.EQUALITY
            and isinstance(root_goal.rhs, FiniteCyclicGroup)
            and isinstance(transported, Relation)
            and transported.relation_type is RelationType.EQUALITY
            and isinstance(transported.rhs, FiniteCyclicGroup)
            and isinstance(witness, GeneratorSuspension)
            and isinstance(witness.map, TodaSuspensionMap)):
        return False
    generator = transported.rhs.generator
    return (
        transported != root_goal
        and transported.lhs == root_goal.lhs == witness.map.target_group
        and transported.rhs.order == root_goal.rhs.order
        and isinstance(generator, IteratedSuspension)
        and generator.exponent == 1
        and _matching_eta_name(generator.expression, witness.source_generator)
        and _matching_eta_name(root_goal.rhs.generator, witness.target_generator)
        and witness.map.source_group != witness.map.target_group
    )
'''


def replace_function(source: str, name: str, replacement: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError('Missing or ambiguous ' + name)
    lines = source.splitlines(keepends=True)
    old = matches[0]
    newline = '\r\n' if '\r\n' in source else '\n'
    converted = replacement.rstrip().replace('\n', newline) + newline + newline
    return ''.join(lines[:old.lineno-1]) + converted + ''.join(lines[old.end_lineno:])


def main():
    module_code = (HERE/'phase166_r3v_generator_transport.py').read_text(encoding='utf-8')
    ast.parse(module_code)
    if not all(x.exists() for x in (MODULE, SHARED, GATE, TEST)):
        raise RuntimeError('R3-V prerequisite files are missing')
    shared_src = SHARED.read_text(encoding='utf-8')
    gate_src = GATE.read_text(encoding='utf-8')
    test_src = TEST.read_text(encoding='utf-8')
    if NEW not in shared_src:
        if shared_src.count(OLD) != 1:
            raise RuntimeError('Unrecognized R3-V shared provider')
        shared_new = shared_src.replace(OLD, NEW, 1)
    else:
        shared_new = shared_src
    if '_proved_generator_suspension_normalization_shape' not in gate_src:
        raise RuntimeError('R3-V gate patch not installed')
    gate_new = replace_function(gate_src, '_proved_generator_suspension_normalization_shape', GATE_SOURCE)
    test_new = replace_function(test_src, 'test_r3v_registered_prior_and_shared_search_connection', TEST_SOURCE)
    for src in (shared_new, gate_new, test_new):
        ast.parse(src)
    updates = {MODULE: module_code, SHARED: shared_new, GATE: gate_new, TEST: test_new}
    changed = {p: s for p, s in updates.items() if p.read_text(encoding='utf-8') != s}
    if not changed:
        print('ALREADY INSTALLED: no changes')
        return
    backup = HERE/'backups'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup.mkdir(parents=True)
    for path, value in changed.items():
        shutil.copy2(path, backup/path.name)
        path.write_text(value, encoding='utf-8')
        print('PATCHED:', path)
    print('BACKUP:', backup)
    tree = ast.parse(gate_new)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=='_proved_generator_suspension_normalization_shape')
    (HERE/'modified_gate_function.txt').write_text(ast.get_source_segment(gate_new,node)+'\n',encoding='utf-8')
    tree = ast.parse(shared_new)
    node = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='shared_expansion_provider')
    (HERE/'modified_shared_expansion_provider.txt').write_text(ast.get_source_segment(shared_new,node)+'\n',encoding='utf-8')
    print('FULL FUNCTIONS:', HERE/'modified_gate_function.txt', HERE/'modified_shared_expansion_provider.txt')

if __name__ == '__main__':
    main()
