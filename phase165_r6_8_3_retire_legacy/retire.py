"""Remove an isolated obsolete forward-probe chain, refusing unknown consumers."""
from __future__ import annotations

import ast
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = (
    'probes/probe_phase53_capabilities.py',
    'probes/probe_phase54_capabilities.py',
    'probes/probe_phase55_capabilities.py',
    'probes/probe_phase57_capabilities.py',
    'phase162_ehp_leaf_inputs.py',
    'phase162_pi5_3_web_replay.py',
    'tests/test_phase59_n3_ehp_chain.py',
    'tests/test_phase55_prop51_phase52_phase54_dependency.py',
)


def module_name(path: str) -> str:
    return path[:-3].replace('/', '.')


def check_consumers(root: Path) -> dict[str, list[str]]:
    """Only project root, probes and tests are scanned; parse failures block deletion."""
    excluded = set(CANDIDATES)
    targets = {module_name(path): path for path in CANDIDATES}
    blockers: dict[str, list[str]] = {path: [] for path in CANDIDATES}
    files = sorted(root.glob('*.py')) + sorted((root / 'probes').glob('*.py')) + sorted((root / 'tests').glob('*.py'))
    for path in files:
        rel = path.relative_to(root).as_posix()
        if rel in excluded:
            continue
        try:
            source = path.read_text(encoding='utf-8-sig')
            tree = ast.parse(source, filename=rel)
        except (OSError, SyntaxError, UnicodeError) as exc:
            for target in blockers:
                blockers[target].append(f'{rel}: unreadable/unparseable: {exc}')
            continue
        for node in ast.walk(tree):
            found = set()
            if isinstance(node, ast.Import):
                found = {alias.name for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                found = {node.module}
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {'__import__'}:
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    found = {node.args[0].value}
            for imported in found:
                for mod, target in targets.items():
                    if imported == mod or imported.startswith(mod + '.'):
                        entry = f'{rel}:{getattr(node, "lineno", 0)} imports {imported}'
                        if entry not in blockers[target]:
                            blockers[target].append(entry)
    return {path: issues for path, issues in blockers.items() if issues}


def main() -> int:
    missing = [p for p in CANDIDATES if not (ROOT / p).is_file()]
    blockers = check_consumers(ROOT)
    report = {'phase': '165 R6-8(3)', 'action': 'blocked' if blockers or missing else 'retired',
              'candidates': list(CANDIDATES), 'missing': missing, 'blocking_consumers': blockers,
              'full_pytest_run': False}
    out = ROOT / 'phase165_r6_8_3_retirement_report.json'
    if blockers or missing:
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(report, ensure_ascii=False, indent=2))
        print('STOP: no files deleted; resolve consumers before retirement.')
        return 2
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = ROOT / f'phase165_r6_8_3_retired_{stamp}.zip'
    with ZipFile(backup, 'w', compression=ZIP_DEFLATED) as archive:
        for rel in CANDIDATES:
            archive.write(ROOT / rel, arcname=rel)
    with ZipFile(backup) as archive:
        if set(archive.namelist()) != set(CANDIDATES):
            raise RuntimeError('backup manifest mismatch; nothing deleted')
    for rel in CANDIDATES:
        (ROOT / rel).unlink()
    report['backup'] = backup.name
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
