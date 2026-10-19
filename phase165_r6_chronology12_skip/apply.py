from __future__ import annotations

import ast
import datetime
import json
import shutil
from pathlib import Path

MANIFEST = Path(__file__).with_name("manifest.json")
REASON = "Phase 165 R6: retired historical forward-engine round ordering; mathematical tests retained"


def _functions(source: str, rel: str):
    tree = ast.parse(source, filename=rel)
    return {node.name: node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")}


def main() -> None:
    root = Path.cwd()
    if not (root / 'phase165_r55_nk_only_goal.py').is_file():
        raise RuntimeError('Execute at EHP Proof Tracer repository root')
    entries = json.loads(MANIFEST.read_text(encoding='utf-8'))
    assert len(entries) == 12
    grouped: dict[str, list[str]] = {}
    for entry in entries:
        grouped.setdefault(entry['file'], []).append(entry['name'])
    patched: dict[Path, str] = {}
    previous: dict[Path, bytes] = {}
    expected_count = 0
    for rel, names in grouped.items():
        path = root / rel
        raw = path.read_bytes()
        source = raw.decode('utf-8-sig')
        if '\r\n' in source:
            newline = '\r\n'
        else:
            newline = '\n'
        tree = ast.parse(source, filename=rel)
        functions = _functions(source, rel)
        if len(names) != len(set(names)) or any(name not in functions for name in names):
            raise RuntimeError(f'Function set differs from reviewed manifest: {rel}')
        lines = source.splitlines(keepends=True)
        insert_at = []
        for name in names:
            fn = functions[name]
            body = ast.get_source_segment(source, fn) or ''
            if not ('round_results' in body or 'round_count' in body):
                raise RuntimeError(f'Refusing to mark non-chronology function: {rel}::{name}')
            if fn.decorator_list:
                raise RuntimeError(f'Unexpected existing decorator: {rel}::{name}')
            insert_at.append(fn.lineno - 1)
            expected_count += 1
        if source.lstrip().startswith('import pytest') or '\nimport pytest\n' in source:
            needs_pytest_import = False
        else:
            needs_pytest_import = True
        for line_number in sorted(insert_at, reverse=True):
            lines.insert(line_number, '@pytest.mark.skip(reason=' + repr(REASON) + ')' + newline)
        updated = ''.join(lines)
        if needs_pytest_import:
            # No future import occurs in these six reviewed test files.
            updated = 'import pytest' + newline + updated
        ast.parse(updated, filename=rel)
        after = _functions(updated,rel)
        if set(after) != set(functions):
            raise RuntimeError(f'Test functions changed: {rel}')
        for name in names:
            decorators = after[name].decorator_list
            if len(decorators) != 1 or not isinstance(decorators[0], ast.Call):
                raise RuntimeError(f'Missing marker after patch: {name}')
        patched[path] = updated
        previous[path] = raw
    assert expected_count == 12
    backup = root / 'phase165_r6_audit_results' / 'runner_backup' / ('chronology12_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    backup.mkdir(parents=True, exist_ok=False)
    for path, raw in previous.items():
        destination = backup / path.relative_to(root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
    for path, source in patched.items():
        path.write_bytes(source.encode('utf-8'))
    report = {'status':'APPLIED','skipped_tests':12,'files':len(patched),
              'other_tests_retained':71,'mathematical_coverage_equivalence_verified':False,
              'backup':str(backup),'full_pytest_run':False}
    out = root/'phase165_r6_audit_results'/'chronology12'
    out.mkdir(parents=True,exist_ok=True)
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
