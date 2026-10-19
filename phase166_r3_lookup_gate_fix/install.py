from __future__ import annotations
import ast
from pathlib import Path
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r3_recursive_search.py'
NEW_FUNCTION = '''def _typed_reference_steps(
    bridge: RegistryBridgeResult,
    goal: object,
    citing_assertion_id: str,
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> tuple[ProofStep, ...]:
    """Use the established citation policy for direct typed references."""
    from phase165_r52_r15_ordered_citation import ordered_typed_reference_steps

    return ordered_typed_reference_steps(
        bridge,
        goal,
        citing_assertion_id,
        verified_assertion_ids=verified_assertion_ids,
    )
'''
OLD_CALL = 'options = list(_typed_reference_steps(bridge, target))'
NEW_CALL = '''options = list(_typed_reference_steps(
                    bridge, target, citing_assertion_id,
                    verified_assertion_ids=verified_assertion_ids,
                ))'''

def main() -> None:
    if not TARGET.is_file():
        raise SystemExit(f'Missing production module: {TARGET}')
    text = TARGET.read_text(encoding='utf-8-sig')
    tree = ast.parse(text)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == '_typed_reference_steps']
    if len(functions) != 1:
        raise SystemExit('Expected exactly one _typed_reference_steps function')
    if text.count(NEW_CALL) == 1 and 'Use the established citation policy for direct typed references.' in text:
        print('ALREADY PATCHED: phase165_r3_recursive_search.py')
        return
    if text.count(OLD_CALL) != 1:
        raise SystemExit('Expected exact single old call site; current code may have changed. No patch applied.')
    node = functions[0]
    lines = text.splitlines(keepends=True)
    old_function = ''.join(lines[node.lineno-1:node.end_lineno])
    if 'def _typed_reference_steps(bridge: RegistryBridgeResult, goal: object)' not in old_function or 'step.rule is not ProofRule.GIVEN' not in old_function:
        raise SystemExit('Unexpected existing helper; no patch applied')
    updated = ''.join(lines[:node.lineno-1]) + NEW_FUNCTION.rstrip('\n') + ''.join(lines[node.end_lineno:])
    updated = updated.replace(OLD_CALL, NEW_CALL)
    ast.parse(updated)
    backup_dir = ROOT / 'phase166_r3_lookup_gate_fix' / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / ('phase165_r3_recursive_search_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.py')
    shutil.copy2(TARGET, backup)
    TARGET.write_text(updated, encoding='utf-8')
    print(f'PATCHED: {TARGET}')
    print(f'BACKUP: {backup}')
    print('Modified: _typed_reference_steps; reconstruct_registered_goal typed_reference call site')

if __name__ == '__main__':
    main()
