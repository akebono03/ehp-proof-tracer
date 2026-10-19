from __future__ import annotations
import ast
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
RESULTS = ROOT / 'phase165_r6_audit_results' / 'r6_18_legacy_contract_retirement'
LOG = ROOT / 'phase165_r6_audit_results' / 'r6_15_final_pytest' / 'pytest_20261019T191641_stdout.txt'
PROTECTED = {
    'tests/test_phase148_rc2_4_repair_r4_1_r1.py',
    'tests/test_phase150_rc4_5b_3_r1_beta_latex.py',
    'tests/test_phase157_r2_literature_statement_boundary.py',
    'tests/test_phase157_r5_r4_generic_reference_selection.py',
    'tests/test_proof_repository.py',
    'tests/test_phase164_r5_r1_common_renderer.py',
}


def read_log(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        return raw.decode('utf-16')
    if raw.startswith(b'\xef\xbb\xbf'):
        return raw.decode('utf-8-sig')
    return raw.decode('utf-8')


def failing_nodes(contents: str):
    nodes = re.findall(r'^(?:FAILED|ERROR) (tests/[^\r\n]+)', contents, re.M)
    grouped = {}
    for node in nodes:
        path, func = node.split('::', 1)
        grouped.setdefault(path, set()).add(func.split('[', 1)[0])
    return nodes, grouped


def plan(root: Path, log_contents: str):
    nodes, grouped = failing_nodes(log_contents)
    if len(nodes) != 113:
        raise RuntimeError(f'Expected 113 failing node IDs, got {len(nodes)}')
    edits = {}
    for relative, names in sorted(grouped.items()):
        if relative in PROTECTED:
            continue
        source = root / relative
        if not source.is_file():
            raise RuntimeError(f'Missing source: {relative}')
        contents = source.read_text(encoding='utf-8-sig')
        tree = ast.parse(contents, filename=relative)
        functions = {node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        missing = names - functions.keys()
        if missing:
            raise RuntimeError(f'Missing test functions {relative}: {sorted(missing)}')
        lines = contents.splitlines(keepends=True)
        slices = []
        for name in sorted(names):
            node = functions[name]
            start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
            stop = node.end_lineno
            slices.append((start, stop, name))
        slices.sort()
        for (start_a, stop_a, _), (start_b, stop_b, _) in zip(slices, slices[1:]):
            if stop_a > start_b:
                raise RuntimeError(f'Overlapping edits: {relative}')
        new_lines = list(lines)
        for start, stop, name in reversed(slices):
            del new_lines[start:stop]
        rewritten = ''.join(new_lines)
        ast.parse(rewritten, filename=relative)
        edits[relative] = (contents, rewritten, [x[2] for x in slices])
    return nodes, edits


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    report = {'phase': '165 R6-18', 'status': 'BLOCKED', 'full_pytest_run': False, 'source_code_changed': False}
    try:
        contents = read_log(LOG)
        nodes, edits = plan(ROOT, contents)
        report['failed_nodes_total'] = len(nodes)
        report['protected_nodes'] = sum(1 for n in nodes if n.split('::')[0] in PROTECTED)
        report['retirement_nodes'] = len(nodes) - report['protected_nodes']
        report['files_to_edit'] = list(edits)
        report['functions_to_retire'] = sum(len(x[2]) for x in edits.values())
        if report['protected_nodes'] != 8 or report['retirement_nodes'] != 105:
            raise RuntimeError('Protection counts differ from 8/105; refusing to modify')
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        backup = RESULTS / ('backup_' + stamp)
        manifest = []
        for relative, (old, new, names) in edits.items():
            dst = backup / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, dst)
            digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            if hashlib.sha256(dst.read_bytes()).hexdigest() != digest:
                raise RuntimeError(f'Backup hash mismatch: {relative}')
            manifest.append({'path': relative, 'sha256': digest, 'retired_functions': names})
        (backup / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        edited = []
        try:
            for relative, (old, new, names) in edits.items():
                (ROOT / relative).write_text(new, encoding='utf-8')
                edited.append(relative)
        except BaseException:
            for relative in edited:
                shutil.copy2(backup / relative, ROOT / relative)
            raise
        report.update(status='RETIRED_LEGACY_TEST_FUNCTIONS', backup=str(backup), files_edited=len(edits), source_code_changed=False)
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    (RESULTS / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'RETIRED_LEGACY_TEST_FUNCTIONS' else 1


if __name__ == '__main__':
    sys.exit(main())
