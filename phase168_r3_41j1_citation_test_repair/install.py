"""R3-41J1 installer: replace one verified complete renderer function."""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / 'phase168_r3_5_model_renderer.py'
FULL_FUNCTION = PACKAGE / 'modified_function_full.py'
OUTPUT = PACKAGE / 'output'
BACKUP = OUTPUT / 'phase168_r3_5_model_renderer.py.before'
EXPECTED_SHA256 = '068490ef45f2072d537dd674db04cf0704832c1a9832394c29f5c04e11fcc588'


def function_span(source: str) -> tuple[int, int]:
    nodes = [node for node in ast.parse(source).body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == 'render_model_backed_narrative_markdown']
    if len(nodes) != 1:
        raise RuntimeError('expected exactly one existing common renderer function')
    return nodes[0].lineno, nodes[0].end_lineno


def main() -> int:
    original_bytes = TARGET.read_bytes()
    observed = hashlib.sha256(original_bytes).hexdigest()
    if observed != EXPECTED_SHA256:
        raise RuntimeError('renderer SHA256 differs from R3-41I pre-R3-41J snapshot; no change. '
                           f'expected={EXPECTED_SHA256} current={observed}')
    original = original_bytes.decode('utf-8-sig')
    current_lines = original.splitlines(keepends=True)
    first, last = function_span(original)
    old_function = ''.join(current_lines[first - 1:last])
    required = (
        'project_exactness_chains(model)',
        'project_narrative_order(model, suppressed_exactness)',
        'project_toda45_specialization_citation_numbers(',
        'model.step_citation_numbers[index]',
        'project_stable_eta_notation_transition(model, index)',
    )
    if not all(part in old_function for part in required):
        raise RuntimeError('existing renderer contract changed; no modification')
    replacement = FULL_FUNCTION.read_text(encoding='utf-8')
    new_node = ast.parse(replacement).body
    if len(new_node) != 1 or not isinstance(new_node[0], ast.FunctionDef):
        raise RuntimeError('replacement must contain exactly one whole function')
    if new_node[0].name != 'render_model_backed_narrative_markdown':
        raise RuntimeError('replacement function name differs')
    newline = '\r\n' if b'\r\n' in original_bytes else '\n'
    replacement = replacement.replace('\n', newline)
    result = ''.join(current_lines[:first - 1]) + replacement + ''.join(current_lines[last:])
    ast.parse(result)
    out_bytes = (b'\xef\xbb\xbf' if original_bytes.startswith(b'\xef\xbb\xbf') else b'') + result.encode('utf-8')
    OUTPUT.mkdir(exist_ok=True)
    if BACKUP.exists():
        if BACKUP.read_bytes() != original_bytes:
            raise RuntimeError('backup differs from current source; no modification')
    else:
        BACKUP.write_bytes(original_bytes)
    (OUTPUT / 'full_file.py').write_bytes(out_bytes)
    try:
        TARGET.write_bytes(out_bytes)
    except BaseException:
        TARGET.write_bytes(original_bytes)
        raise
    status = {
        'status': 'PATCHED', 'target': str(TARGET),
        'before_sha256': observed,
        'after_sha256': hashlib.sha256(out_bytes).hexdigest(),
        'backup_path': str(BACKUP), 'full_function': str(FULL_FUNCTION),
        'full_file': str(OUTPUT / 'full_file.py'),
        'changed_function_count': 1,
        'production_files_modified': ['phase168_r3_5_model_renderer.py'],
        'full_pytest_run': False,
    }
    (OUTPUT / 'install.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PATCHED', TARGET)
    print('BACKUP', BACKUP)
    print('FULL_FUNCTION', FULL_FUNCTION)
    print('FULL_FILE', OUTPUT / 'full_file.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
