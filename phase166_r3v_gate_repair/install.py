"""Narrow R3-V correction: preserve cited generator conversion at root gate."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
FILE = ROOT / 'phase165_r57_r11_proof_order_gate.py'
NEW_FUNC = '''def _proved_generator_suspension_normalization_shape(root_goal: object, expansion: GoalExpansion) -> bool:
    """Permit a same-group intermediate only with a separately proved E-image goal."""
    from expression import IteratedSuspension
    from homotopy_groups import TodaSuspensionMap
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension

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
        and generator.expression == witness.source_generator
        and root_goal.rhs.generator == witness.target_generator
        and witness.map.source_group != witness.map.target_group
    )
'''
ANCHOR = 'def is_unordered_root_structure_specialization('
EXISTING = '    if _proved_generator_substitution_shape(root_goal, expansion):\n        return False'
REPLACEMENT = EXISTING + '\n    if _proved_generator_suspension_normalization_shape(root_goal, expansion):\n        return False'

def main():
    src = FILE.read_text(encoding='utf-8')
    ast.parse(src)
    if 'def _proved_generator_suspension_normalization_shape(' in src and REPLACEMENT in src:
        print('ALREADY INSTALLED: gate unchanged')
        return
    if 'def _proved_generator_suspension_normalization_shape(' in src or src.count(ANCHOR) != 1 or src.count(EXISTING) != 1:
        raise RuntimeError('Unexpected gate code; refusing automatic modification')
    new = src.replace(ANCHOR, NEW_FUNC + '\n\n' + ANCHOR, 1).replace(EXISTING, REPLACEMENT, 1)
    ast.parse(new)
    folder = HERE/'backups'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    folder.mkdir(parents=True)
    shutil.copy2(FILE,folder/FILE.name)
    FILE.write_text(new,encoding='utf-8')
    tree=ast.parse(new)
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('_proved_generator_suspension_normalization_shape','is_unordered_root_structure_specialization')]
    (HERE/'modified_functions.txt').write_text('\n\n'.join(ast.get_source_segment(new,n) for n in funcs)+'\n',encoding='utf-8')
    print('PATCHED:',FILE)
    print('BACKUP:',folder)
    print('FULL FUNCTIONS:',HERE/'modified_functions.txt')

if __name__=='__main__':
    main()
