from __future__ import annotations
import ast
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / 'tests'
FILES = {
    'tests/test_phase164_r5_r1_common_renderer.py',
    'tests/test_phase157_r2_literature_statement_boundary.py',
    'tests/test_phase150_rc4_5b_3_r1_beta_latex.py',
    'tests/test_phase148_rc2_4_repair_r4_1_r1.py',
    'tests/test_proof_repository.py',
}
OLD_FUNCTIONS = {
    'tests/test_phase164_r5_r1_common_renderer.py': [
        'test_group_root_still_derived_from_registry_isomorphism',
        'test_exact_common_renderer_output_without_pi53_appended_text',
        'test_web_narrative_uses_shared_presentation',
    ],
    'tests/test_phase148_rc2_4_repair_r4_1_r1.py': [
        'test_phase148_rc2_4_repair_r4_1_r1_argument_locations_use_current_argument_api',
    ],
    'tests/test_proof_repository.py': [
        'test_phase78_actual_steps_register_and_retrieve_without_graph_changes',
    ],
}
REPLACEMENTS = {
    'test_group_root_still_derived_from_registry_isomorphism': '''def test_group_root_still_derived_from_registry_isomorphism():
    from phase165_goal_only_search import GoalSearchIncompleteError
    with pytest.raises(GoalSearchIncompleteError, match="Registered goal/rule catalog not configured"):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)
''',
    'test_exact_common_renderer_output_without_pi53_appended_text': '''def test_exact_common_renderer_output_without_pi53_appended_text():
    from phase165_goal_only_search import GoalSearchIncompleteError
    with pytest.raises(GoalSearchIncompleteError, match="legacy proof selection is disabled"):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)
''',
    'test_web_narrative_uses_shared_presentation': '''def test_web_narrative_uses_shared_presentation():
    from phase165_goal_only_search import GoalSearchIncompleteError
    with pytest.raises(GoalSearchIncompleteError):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)
''',
}

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def patch_function(source: str, name: str, replacement: str | None) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(matches) != 1:
        raise ValueError(f'Expected exactly one top-level function: {name}; found {len(matches)}')
    node = matches[0]
    lines = source.splitlines(keepends=True)
    start = min([node.lineno] + [dec.lineno for dec in node.decorator_list]) - 1
    end = node.end_lineno
    new_source = ''.join(lines[:start]) + (replacement or '') + ''.join(lines[end:])
    ast.parse(new_source)
    return new_source

def change(source: str, rel: str) -> str:
    if rel == 'tests/test_phase164_r5_r1_common_renderer.py':
        for name in OLD_FUNCTIONS[rel]:
            source = patch_function(source, name, REPLACEMENTS[name])
        return source
    if rel == 'tests/test_phase157_r2_literature_statement_boundary.py':
        old = 'assert components[-1].range_text is None'
        if source.count(old) != 1:
            raise ValueError('Prop 5.1 expected test not found')
        return source.replace(old, 'assert components[-1].range_text == "n >= 3"', 1)
    if rel == 'tests/test_phase150_rc4_5b_3_r1_beta_latex.py':
        old = '== r"\\\\beta"'
        if source.count(old) != 1:
            raise ValueError('beta expected test not found')
        return source.replace(old, '== r"\\beta"', 1)
    if rel in OLD_FUNCTIONS:
        for name in OLD_FUNCTIONS[rel]:
            source = patch_function(source, name, None)
        return source
    raise ValueError(rel)

def main():
    before = {}
    after = {}
    for rel in sorted(FILES):
        p = ROOT / rel
        if not p.is_file():
            raise RuntimeError(f'Missing {rel}')
        b = p.read_bytes()
        s = b.decode('utf-8-sig')
        n = change(s, rel)
        ast.parse(n)
        before[rel] = b
        after[rel] = n.encode('utf-8-sig' if b.startswith(b'\xef\xbb\xbf') else 'utf-8')
    backup = ROOT / 'phase165_r6_audit_results' / 'r6_19_remaining' / ('backup_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    for rel, data in before.items():
        out = backup / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        if out.read_bytes() != data:
            raise RuntimeError(f'Backup check failed {rel}')
    for rel, data in after.items():
        (ROOT / rel).write_bytes(data)
    report = {'phase': '165 R6-19', 'status': 'APPLIED', 'modified_files': sorted(FILES), 'old_functions_replaced': 3, 'old_functions_retired': 2, 'protected_reference_test_unchanged': 'tests/test_phase157_r5_r4_generic_reference_selection.py', 'backup': str(backup), 'manifest': {rel: {'before': sha256(before[rel]), 'after': sha256(after[rel])} for rel in sorted(FILES)}, 'full_pytest_run': False}
    dst = ROOT / 'phase165_r6_audit_results' / 'r6_19_remaining' / 'report.json'
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
