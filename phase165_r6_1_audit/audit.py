"""Phase 165 R6-1: non-destructive audit of production search connections."""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = (
    'phase165_r3_recursive_search.py',
    'phase165_r52_r9_shared_math.py',
    'phase165_r52_r23_existing_rule_adapter.py',
    'phase165_r57_r26_generic_search_connection.py',
    'phase165_r57_r24_candidate_discovery.py',
    'phase165_r57_r25_premise_generation.py',
    'phase165_r52_r2_search_adapter.py',
    'phase165_goal_only_search.py',
    'phase165_r52_r7_registered_common_proof.py',
    'phase165_r14_r34_backward_search.py',
    'proof.py',
)
KEYWORDS = re.compile(r'pi\d+_\d+|pi\d\d|phase165_r52_r23|expand_existing_pi43_rules|_objects\(|goal\.lhs\s*==\s*target|group_dim\s*==\s*sphere\s*\+\s*1', re.I)
SEARCH_MARKERS = ('expansion', 'backward', 'goal', 'search', 'rule', 'adapter', 'proof')


def scan(root: Path) -> dict:
    if not root.is_dir():
        raise ValueError('repository root not found')
    results = []
    for path in sorted(root.glob('*.py')):
        if not any(marker in path.stem.lower() for marker in SEARCH_MARKERS):
            continue
        source = path.read_text(encoding='utf-8-sig')
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            results.append({'file': path.name, 'category': 'PARSE_ERROR', 'line': exc.lineno})
            continue
        lines = source.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            fragment = '\n'.join(lines[node.lineno - 1: node.end_lineno])
            hit = KEYWORDS.search(fragment)
            if hit:
                results.append({'file': path.name, 'function': node.name, 'line': node.lineno,
                                'category': 'REVIEW_CANDIDATE', 'evidence': hit.group(0)})
    for filename in CORE:
        if not (root / filename).is_file():
            results.append({'file': filename, 'category': 'MISSING_CORE_FILE'})
    shared = root / 'phase165_r52_r9_shared_math.py'
    adapter = root / 'phase165_r52_r23_existing_rule_adapter.py'
    connection = root / 'phase165_r57_r26_generic_search_connection.py'
    shared_source = shared.read_text(encoding='utf-8-sig') if shared.exists() else ''
    adapter_source = adapter.read_text(encoding='utf-8-sig') if adapter.exists() else ''
    generic_source = connection.read_text(encoding='utf-8-sig') if connection.exists() else ''
    edges = {
        'shared_imports_pi43_adapter': 'from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules' in shared_source,
        'shared_calls_pi43_adapter': bool(re.search(r'^\s*expand_existing_pi43_rules\s*,', shared_source, re.M)),
        'shared_calls_generic_provider': 'generic_provider(goal)' in shared_source,
        'pi43_adapter_contains_fixed_group_targets': 'TodaPrimaryGroup(4, 3)' in adapter_source,
        'generic_provider_uses_discovery': 'discover_explicit_goal_candidates(rules, goal)' in generic_source,
    }
    return {'phase': '165 R6-1', 'mode': 'READ_ONLY', 'full_pytest_run': False,
            'core_files': list(CORE), 'connection_checks': edges,
            'candidates': results,
            'scope': 'top-level Python files with search-related module names; inspect candidates manually',
            'warning': 'A text/AST match is an audit candidate, not proof of active runtime routing.'}


def main() -> None:
    report = scan(ROOT)
    output = Path(__file__).resolve().parent / 'audit_report.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'phase': report['phase'], 'connection_checks': report['connection_checks'],
                      'candidates': len(report['candidates']), 'output': str(output)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
