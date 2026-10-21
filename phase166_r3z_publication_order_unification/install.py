from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
MAIN = ROOT / 'phase165_r52_r9_shared_math.py'
AUDIT = ROOT / 'phase165_r12_r8_typed_source_connection.py'

OLD_MAIN = '''    # R12-R7: enforce reviewed dependencies before using cited proof leaves.
    from phase165_r12_r7_proof_order_guard import restrict_registered_ordered_claims
    proof_context = restrict_registered_ordered_claims(proof_context, goal)
    if proof_use_order == "registered":
        from phase165_r52_r19_prop51_binding import resolve_registered_proof_use_order
        proof_use_order = resolve_registered_proof_use_order(proof_context, goal)
    if proof_use_order is not None:
        from phase165_r52_r18_proof_order import restrict_by_proof_use_order
        proof_context = restrict_by_proof_use_order(
            proof_context, goal=goal, policy=proof_use_order,
        )
'''
OLD_AUDIT_IMPORT = '    from phase165_r12_r7_proof_order_guard import restrict_registered_ordered_claims\n'
OLD_AUDIT_CALL = '    screened = restrict_registered_ordered_claims(screened, target)\n'

def load(path: Path) -> tuple[str, str]:
    if not path.is_file():
        raise RuntimeError('Required source missing: ' + str(path))
    raw = path.read_bytes()
    newline = '\r\n' if b'\r\n' in raw else '\n'
    return raw.decode('utf-8').replace('\r\n', '\n'), newline


def function_text(source: str, name: str) -> str:
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    if len(nodes) != 1:
        raise RuntimeError(f'Expected exactly one function {name}')
    n = nodes[0]
    return ''.join(source.splitlines(keepends=True)[n.lineno - 1:n.end_lineno])


def prepare():
    main, nl_main = load(MAIN)
    audit, nl_audit = load(AUDIT)
    if main.count(OLD_MAIN) != 1 or audit.count(OLD_AUDIT_IMPORT) != 1 or audit.count(OLD_AUDIT_CALL) != 1:
        raise RuntimeError('Existing code differs from audited baseline; no files modified. Re-audit the local changes.')
    main_new = main.replace(OLD_MAIN, '', 1)
    audit_new = audit.replace(OLD_AUDIT_IMPORT, '', 1).replace(OLD_AUDIT_CALL, '', 1)
    for data in (main_new, audit_new):
        ast.parse(data)
    return [(MAIN, main_new, nl_main, 'search_shared_group_goal'),
            (AUDIT, audit_new, nl_audit, 'audit_real_pi43_quotient_connection')]


def main():
    modifications = prepare()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = ROOT / 'phase166_r3z_backups' / stamp
    backup.mkdir(parents=True, exist_ok=False)
    for target, data, newline, name in modifications:
        shutil.copy2(target, backup / target.name)
        temp = target.with_suffix(target.suffix + '.r3z.tmp')
        temp.write_bytes(data.replace('\n', newline).encode('utf-8'))
        temp.replace(target)
        (PACKAGE / (name + '.installed_full.py.txt')).write_text(function_text(data, name), encoding='utf-8')
        print('PATCHED:', target.name, 'FUNCTION:', name)
    print('BACKUP:', backup)
    print('UNCHANGED: phase166_r3c_publication_order.py / precedes_citing_assertion')
    print('UNCHANGED: phase165_r52_r16_web_citation_gate.py / screen_shared_proof_context')
    print('NOTE: legacy optional proof_use_order parameter is retained for API compatibility, but no longer filters the shared context.')

if __name__ == '__main__':
    main()
