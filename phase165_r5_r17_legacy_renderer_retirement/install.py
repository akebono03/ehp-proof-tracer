from __future__ import annotations

import ast
import json
import shutil
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
MODULES = (
    'phase162_web_narrative_integration.py',
    'phase162_r3_narrative_connection.py',
    'toda_group_proof_narrative_proof_chain_renderer.py',
    'toda_group_proof_narrative_concrete_transport.py',
)
TESTS = (
    'tests/test_phase162_r5_web_integration.py',
    'tests/test_phase162_r5_6_narrative_final_format.py',
    'tests/test_phase162_r3_narrative_connection.py',
    'tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py',
    'tests/test_phase162_r4_b3_common_renderer_fix.py',
)
REMOVAL = MODULES + TESTS
BACKUP = PROJECT / '.phase165_r5_r17_removed_backup'
GUARD_MODULES = {Path(p).stem for p in MODULES}
SKIP_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'archive', '.pytest_cache', 'site-packages'}


def imports_retired_module(source: str) -> set[str]:
    try:
        parsed = ast.parse(source)
    except SyntaxError:
        return set()
    found: set[str] = set()
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            for name in node.names:
                token = name.name.split('.')[0]
                if token in GUARD_MODULES:
                    found.add(token)
        elif isinstance(node, ast.ImportFrom) and node.module:
            token = node.module.split('.')[0]
            if token in GUARD_MODULES:
                found.add(token)
    return found


def in_active_root(path: Path) -> bool:
    rel = path.relative_to(PROJECT)
    if any(part in SKIP_DIRS or part.startswith('.phase') for part in rel.parts):
        return False
    if len(rel.parts) == 1 and rel.name.startswith('audit_'):
        return False
    return len(rel.parts) == 1 or rel.parts[0] == 'tests'


def inspect() -> dict:
    missing = [p for p in REMOVAL if not (PROJECT / p).is_file()]
    leaf = PROJECT / 'phase162_ehp_leaf_inputs.py'
    replay = PROJECT / 'phase162_pi5_3_web_replay.py'
    shared_guards = {
        'shared_leaf_exists': leaf.is_file(),
        'replay_imports_shared_leaf': replay.is_file() and 'from phase162_ehp_leaf_inputs import _phase162_ehp_leaves' in replay.read_text(encoding='utf-8-sig'),
        'common_partial_renderer_exists': (PROJECT / 'phase165_r52_partial_proof.py').is_file(),
        'common_web_exists': (PROJECT / 'web_group_proof.py').is_file(),
    }
    blockers: dict[str, list[str]] = {}
    historical: dict[str, list[str]] = {}
    excluded = {PROJECT / p for p in REMOVAL}
    for path in PROJECT.rglob('*.py'):
        if path in excluded or PACKAGE in path.parents:
            continue
        rel = path.relative_to(PROJECT)
        if any(part in SKIP_DIRS or part.startswith('.phase') for part in rel.parts):
            continue
        names = imports_retired_module(path.read_text(encoding='utf-8-sig', errors='replace'))
        if not names:
            continue
        key = rel.as_posix()
        (blockers if in_active_root(path) else historical)[key] = sorted(names)
    return {'phase': '165 R5-R17', 'missing_files': missing, 'guards': shared_guards,
            'active_import_blockers': blockers, 'historical_imports': historical,
            'planned_deletions': list(REMOVAL), 'full_pytest_run': False}


def install() -> int:
    report = inspect()
    output = PACKAGE / 'audit_output'
    output.mkdir(exist_ok=True)
    report_path = output / 'install.json'
    if BACKUP.exists():
        report['status'] = 'BACKUP_ALREADY_EXISTS_ABORT'
    elif report['missing_files']:
        report['status'] = 'MISSING_FILE_ABORT'
    elif not all(report['guards'].values()):
        report['status'] = 'SHARED_ROUTE_GUARD_FAILED'
    elif report['active_import_blockers']:
        report['status'] = 'ACTIVE_IMPORT_BLOCKERS_ABORT'
    else:
        BACKUP.mkdir()
        for rel in REMOVAL:
            dest = BACKUP / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT / rel, dest)
        for rel in REMOVAL:
            (PROJECT / rel).unlink()
        report['status'] = 'REMOVED'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'REMOVED' else 2


if __name__ == '__main__':
    sys.exit(install())
