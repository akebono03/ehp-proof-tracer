from __future__ import annotations
import ast
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / 'toda_group_proof_narrative_references.py'
FUNCTION = 'filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary'
TESTS = [
    'tests/test_phase157_r5_r4_generic_reference_selection.py',
    'tests/test_phase157_r2_literature_statement_boundary.py',
    'tests/test_phase157_r4_r3_reference_selection_integration.py',
    'tests/test_phase157_r5_r3_boundary_catalog_expansion.py',
    'tests/test_phase156_r5_repair4_bridge_reference_inference.py',
]

def relevant_if(node):
    return (isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Attribute)
            and isinstance(node.test.left.value, ast.Name)
            and node.test.left.value.id == 'boundary'
            and node.test.left.attr == 'component_key'
            and len(node.test.ops) == 1
            and isinstance(node.test.ops[0], ast.Is)
            and len(node.test.comparators) == 1
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value is None)

def run():
    if not TARGET.is_file():
        raise SystemExit(f'Missing source: {TARGET}')
    before = TARGET.read_bytes()
    source = before.decode('utf-8-sig')
    newline = '\r\n' if '\r\n' in source else '\n'
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == FUNCTION]
    if len(functions) != 1:
        raise SystemExit('ABORT: target function not unique or missing; no files changed')
    matches = [node for node in ast.walk(functions[0]) if relevant_if(node)]
    if len(matches) != 1:
        raise SystemExit(f'ABORT: found {len(matches)} candidate component-key branches; no files changed')
    branch = matches[0]
    block_text = ast.get_source_segment(source, branch) or ''
    if 'fixed_components' not in block_text or 'retained_steps.append' not in block_text:
        raise SystemExit('ABORT: local branch differs from expected aggregate-append behavior; no files changed\n' + block_text[:1500])
    lines = source.splitlines(keepends=True)
    leading = lines[branch.lineno - 1][:branch.col_offset]
    # Allow comments or blank lines before the next AST node but only replace the branch itself.
    replacement = leading + 'if boundary.component_key is None:' + newline + leading + '  # Aggregate statements without a typed component are not citable.' + newline + leading + '  continue' + newline
    edited_lines = lines[:branch.lineno - 1] + [replacement] + lines[branch.end_lineno:]
    edited = ''.join(edited_lines)
    ast.parse(edited)
    # Leave exact import statements and other functions byte-for-byte unchanged.
    updated_bytes = (b'\xef\xbb\xbf' if before.startswith(b'\xef\xbb\xbf') else b'') + edited.encode('utf-8')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ROOT / 'phase165_r6_audit_results' / 'r6_20_reference_filter_fix' / stamp
    out.mkdir(parents=True, exist_ok=False)
    shutil.copy2(TARGET, out / TARGET.name)
    TARGET.write_bytes(updated_bytes)
    print('APPLIED:', TARGET)
    print('BACKUP:', out / TARGET.name)
    cmd = [sys.executable, '-m', 'pytest', '-q', *TESTS]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    (out / 'pytest_stdout.txt').write_text(proc.stdout, encoding='utf-8')
    (out / 'pytest_stderr.txt').write_text(proc.stderr, encoding='utf-8')
    print(proc.stdout[-8000:])
    if proc.stderr:
        print(proc.stderr[-2000:])
    report = {
        'phase': '165 R6-20 fix',
        'status': 'TARGETED_PASS' if proc.returncode == 0 else 'TARGETED_FAILED_REVIEW_REQUIRED',
        'modified_file': str(TARGET.relative_to(ROOT)),
        'changed_function': FUNCTION,
        'backup': str(out / TARGET.name),
        'before_sha256': hashlib.sha256(before).hexdigest(),
        'after_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest(),
        'pytest_returncode': proc.returncode,
        'full_pytest_run': False,
    }
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'changed_function.py').write_text(ast.get_source_segment(edited, next(n for n in ast.parse(edited).body if isinstance(n, ast.FunctionDef) and n.name == FUNCTION)) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(proc.returncode)

if __name__ == '__main__':
    run()
