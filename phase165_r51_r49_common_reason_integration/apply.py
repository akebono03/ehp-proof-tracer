"""Move the existing, tested R49 function to the shared reason renderer.

Do not change its body or public signature.  Archive the superseded module
only after focused regression tests succeed.
"""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
HELPER = ROOT / 'phase165_r49_display_order.py'
REASON = ROOT / 'toda_group_proof_narrative_reason_renderer.py'
CONTRIBUTION = ROOT / 'toda_group_proof_narrative_contribution_renderer.py'
TEST = ROOT / 'tests' / 'test_phase165_r49_display_fix.py'
BACKUP = PACKAGE / 'backup_before_apply'
NAME = 'finalize_phase165_r49_typed_reason_order'
OLD_IMPORT = 'from phase165_r49_display_order import finalize_phase165_r49_typed_reason_order'
REASON_IMPORT = 'from toda_group_proof_narrative_reason_renderer import finalize_phase165_r49_typed_reason_order'


def function_source(source: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == NAME]
    if len(matches) != 1:
        raise RuntimeError('expected one R49 function in original module')
    lines = source.splitlines(keepends=True)
    return ''.join(lines[matches[0].lineno-1:matches[0].end_lineno]).rstrip() + '\n'


def apply() -> None:
    if not all(path.is_file() for path in (REASON, CONTRIBUTION, TEST)):
        raise RuntimeError('required sources missing; no change made')
    reason = REASON.read_text(encoding='utf-8')
    contribution = CONTRIBUTION.read_text(encoding='utf-8')
    test = TEST.read_text(encoding='utf-8')
    if NAME in reason and REASON_IMPORT in test and OLD_IMPORT not in contribution:
        print('R49 common reason integration already installed')
        return
    if not HELPER.is_file():
        raise RuntimeError('original R49 helper missing; no change made')
    helper = HELPER.read_text(encoding='utf-8')
    source = function_source(helper)
    if ('from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step' not in helper
        or 'from toda_group_proof_narrative_reasons import TodaGroupProofNarrativeReasonKind' not in helper):
        raise RuntimeError('unexpected helper dependencies; no change made')
    if NAME in reason or contribution.count(OLD_IMPORT) != 1 or test.count(OLD_IMPORT) != 1:
        raise RuntimeError('unexpected target state; no change made')
    anchor = '\ndef insert_toda_group_proof_narrative_reason_prose('
    if reason.count(anchor) != 1:
        raise RuntimeError('shared renderer insertion anchor unavailable')
    updated_reason = reason.replace(anchor, '\n\n' + source + anchor, 1)
    # Preserve the existing grouped import and remove the standalone phase import.
    updated_contribution = contribution.replace(OLD_IMPORT + '\n', '', 1)
    grouped = 'from toda_group_proof_narrative_reason_renderer import (\n'
    if updated_contribution.count(grouped) != 1:
        raise RuntimeError('existing shared reason import block missing')
    updated_contribution = updated_contribution.replace(grouped, grouped + '  finalize_phase165_r49_typed_reason_order,\n', 1)
    updated_test = test.replace(OLD_IMPORT, REASON_IMPORT, 1)
    for path, text in [(REASON, updated_reason), (CONTRIBUTION, updated_contribution), (TEST, updated_test)]:
        ast.parse(text, filename=str(path))
    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in (HELPER, REASON, CONTRIBUTION, TEST):
        shutil.copy2(path, BACKUP / path.name)
    # Atomic per-file updates; the backups permit restoration on test failure.
    for path, text in [(REASON, updated_reason), (CONTRIBUTION, updated_contribution), (TEST, updated_test)]:
        path.write_text(text, encoding='utf-8', newline='')
    (PACKAGE / 'R49_FUNCTION_FULL.py').write_text(source, encoding='utf-8')
    print('R49 typed-reason ordering moved to shared reason renderer; prior code backed up')


def restore() -> None:
    if not BACKUP.is_dir():
        return
    for path in (REASON, CONTRIBUTION, TEST):
        prior = BACKUP / path.name
        if prior.is_file():
            shutil.copy2(prior, path)
    print('R49 integration rolled back after test failure')


def finalize() -> None:
    if not HELPER.exists():
        print('R49 standalone helper already absent')
        return
    archived = PACKAGE / 'superseded_after_tests' / HELPER.name
    archived.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(HELPER), str(archived))
    print('R49 standalone helper archived after targeted tests passed')


if __name__ == '__main__':
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else 'apply'
    if action == 'apply':
        apply()
    elif action == 'restore':
        restore()
    elif action == 'finalize':
        finalize()
    else:
        raise ValueError(action)
