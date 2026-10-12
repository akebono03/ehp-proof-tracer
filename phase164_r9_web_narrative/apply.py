"""Phase 164 R9 guarded, rollbackable public narrative patch."""
from __future__ import annotations
import argparse
import ast
import json
import shutil
from datetime import datetime
from pathlib import Path

NAME = 'render_toda_group_proof_narrative_markdown'
TARGET = Path('toda_group_proof_narrative_renderer.py')
NEW = Path('phase164_r9_narrative_contract.py')
OLD = '''  return suppress_toda_group_proof_narrative_dangling_connectors(
    rendered
  )'''
REPLACEMENT = '''  from phase164_r9_narrative_contract import normalize_public_narrative_contract
  return normalize_public_narrative_contract(
    suppress_toda_group_proof_narrative_dangling_connectors(
      rendered
    )
  )'''


def last_function(source: str):
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == NAME]
    if not nodes:
        raise ValueError('public renderer entrypoint absent')
    return nodes[-1]


def plan(root: Path):
    target = root / TARGET
    if not target.is_file():
        raise FileNotFoundError(target)
    source = target.read_text(encoding='utf-8')
    fn = last_function(source)
    lines = source.splitlines(keepends=True)
    chunk = ''.join(lines[fn.lineno - 1:fn.end_lineno])
    if REPLACEMENT in chunk:
        state = 'already_applied'
        changed = source
    elif chunk.count(OLD) == 1:
        state = 'ready'
        changed = source.replace(chunk, chunk.replace(OLD, REPLACEMENT), 1)
    else:
        raise ValueError('unexpected public renderer body; no changes applied')
    ast.parse(changed)
    return state, source, changed


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='.')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    root = Path(args.root).resolve()
    state, source, changed = plan(root)
    output = root / 'phase164_r9_output'
    output.mkdir(exist_ok=True)
    audit = {'phase': '164 R9', 'state': state, 'changed_files': [str(TARGET), str(NEW)],
             'target': 'shared_public_narrative_renderer', 'full_pytest_run': False,
             'proof_tree_modified': False, 'mathematical_certification': False,
             'limitations': ['Text normalization is conservative; derivation and provenance require separate review.',
                             'Observed Web output must be checked after rendering, not inferred from static source.']}
    if args.dry_run:
        audit['dry_run'] = True
        print(json.dumps(audit, ensure_ascii=False, indent=2))
        return
    if state == 'ready':
        backup = root / ('phase164_r9_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
        backup.mkdir(exist_ok=False)
        shutil.copy2(root / TARGET, backup / TARGET)
        if (root / NEW).exists():
            shutil.copy2(root / NEW, backup / NEW)
        audit['backup_dir'] = str(backup)
        audit['new_module_existed'] = (backup / NEW).exists()
        (root / TARGET).write_text(changed, encoding='utf-8')
        shutil.copy2(Path(__file__).with_name(NEW.name), root / NEW)
        (output / 'backup.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    elif not (root / NEW).is_file():
        raise ValueError('renderer already patched but helper missing')
    try:
        from subprocess import run
        import sys
        tests = [str(Path(__file__).with_name('test_phase164_r9_narrative_contract.py'))]
        standard = root / 'tests' / 'test_phase164_r5_web_registry_connection.py'
        if standard.is_file():
            tests.append(str(standard))
        res = run([sys.executable, '-m', 'pytest', '-q', *tests], cwd=root)
        audit['focused_pytest_returncode'] = res.returncode
        if res.returncode:
            raise RuntimeError('focused pytest failed')
        audit['status'] = 'R9_TARGETED_PASS_WEB_RENDER_RUNTIME_REVIEW_REQUIRED'
        (output / 'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(audit, ensure_ascii=False, indent=2))
    except Exception:
        if state == 'ready':
            shutil.copy2(backup / TARGET, root / TARGET)
            if audit['new_module_existed']:
                shutil.copy2(backup / NEW, root / NEW)
            else:
                (root / NEW).unlink(missing_ok=True)
        raise


if __name__ == '__main__':
    main()
