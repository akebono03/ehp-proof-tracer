from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
target = root / 'phase164_r5_r2_common_replay.py'
original = target.read_text(encoding='utf-8-sig')
module = ast.parse(original)
functions = [node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == 'build_phase164_r5_r2_common_replay']
if len(functions) != 1:
    raise RuntimeError('Unexpected selector layout: no changes applied')
replacement = '''def build_phase164_r5_r2_common_replay(n: int, k: int, group_result, max_depth: int, mode: str):
    """Fail closed until a verified typed registry and common rule catalog are connected.

    No old repository replay, group-specific reconstruction, or stable-eta
    replay is an acceptable proof source in the unified Web proof route.
    """
    from phase165_goal_only_search import GoalSearchIncompleteError

    raise GoalSearchIncompleteError(
        "Registered goal/rule catalog not configured for "
        f"group (n={n}, k={k}); legacy proof selection remains disabled"
    )
'''
node=functions[0]
lines=original.splitlines(keepends=True)
updated=''.join(lines[:node.lineno-1])+replacement+''.join(lines[node.end_lineno:])
# Remove superseded top-level legacy import to avoid implying fallback exists.
updated=updated.replace('from toda_group_result_proof_replay import build_toda_group_result_proof_replay\n','')
updated=updated.replace('Existing specialized proof construction is preserved in this phase.','Legacy proof construction is explicitly disabled by Phase 165.')
ast.parse(updated)
if original != updated:
    target.write_text(updated, encoding='utf-8')
    print('Installed global fail-closed selector for all group proofs.')
else:
    print('Global fail-closed selector already installed.')
