"""Phase 164 R7-R9: read-only scoped closure audit.

This does not certify mathematical semantics or dynamically enumerate all possible
runtime routes. Tests are executed by run.ps1 and recorded separately.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

ENTRYPOINTS = {
    'generator': ('repository_generator_known_group_identity_lookup.py', 'find_standard_repository_generator_known_group_identity_nodes', 'validate_generator_repository_registry_links'),
    'operation': ('repository_operation_query_facade.py', 'query_standard_repository_operation_input', 'validate_repository_internal_proof_roots'),
    'group': ('toda_calculation_facade.py', 'build_standard_toda_report', 'validate_repository_internal_proof_roots'),
}
SITES = {
    'phase164_r3_registry_search_connection.py': ('resolve_registered_statement',),
    'phase164_r4_r8_registry_reconstruction.py': ('resolve_registered_statement',),
    'phase163_source_archive_registry.py': ('reference',),
    'phase164_r7_repository_root_resolution.py': ('resolve_registered_statement',),
    'phase164_r7_statement_resolution.py': ('assertion', 'reference', 'assess_phase164_r2_citation'),
}
DIRECT = ('assertion', 'reference')


def calls_of(node: ast.AST) -> list[dict]:
    result = []
    for part in ast.walk(node):
        if not isinstance(part, ast.Call):
            continue
        fn = part.func
        if isinstance(fn, ast.Name):
            result.append({'name': fn.id, 'receiver': None, 'line': part.lineno})
        elif isinstance(fn, ast.Attribute):
            result.append({'name': fn.attr, 'receiver': ast.unparse(fn.value), 'line': part.lineno})
    return result


def functions(tree: ast.AST):
    return {node.name: node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def audit(root: Path) -> dict:
    required = set(SITES) | {v[0] for v in ENTRYPOINTS.values()}
    missing = sorted(str(path) for path in required if not (root / path).is_file())
    if missing:
        return {'phase': '164 R7-R9', 'status': 'BLOCKED_MISSING_FILES', 'missing_files': missing, 'scope_closed': False}
    trees = {name: ast.parse((root / name).read_text(encoding='utf-8-sig'), filename=name) for name in required}
    endpoints = []
    for label, (file, function, guard) in ENTRYPOINTS.items():
        fn = functions(trees[file]).get(function)
        found = [] if fn is None else calls_of(fn)
        guard_calls = [call for call in found if call['name'] == guard]
        repository_calls = [call for call in found if call['name'] == 'build_standard_production_proof_repository']
        endpoints.append({'label': label, 'file': file, 'function': function, 'guard': guard,
                          'guard_calls': guard_calls, 'repository_calls': repository_calls,
                          'status': 'GUARDED' if guard_calls and repository_calls and guard_calls[0]['line'] > repository_calls[0]['line'] else 'NOT_GUARDED'})
    sites = []
    for path, expected in SITES.items():
        all_calls = calls_of(trees[path])
        for name in expected:
            found = [call for call in all_calls if call['name'] == name]
            sites.append({'file': path, 'call': name, 'locations': found, 'present': bool(found)})
    special_file = 'phase164_r4_r8_registry_reconstruction.py'
    special = functions(trees[special_file]).get('reconstruct_phase164_r4_r8_pi5_3')
    special_calls = [] if special is None else calls_of(special)
    direct_special = [call for call in special_calls if call['name'] in DIRECT and call['receiver'] is not None and ('registry' in call['receiver'] or 'bridge' in call['receiver'])]
    resolved_special = [call for call in special_calls if call['name'] == 'resolve_registered_statement']
    # Static evidence that cited assertion IDs are not auto-approved.
    resolution_src = (root / 'phase164_r7_statement_resolution.py').read_text(encoding='utf-8-sig')
    r2_src = (root / 'phase164_r2_citation_eligibility.py').read_text(encoding='utf-8-sig') if (root / 'phase164_r2_citation_eligibility.py').is_file() else ''
    boundary = {
        'special_direct_registry_getters': direct_special,
        'special_resolver_calls': resolved_special,
        'shared_resolver_has_fixed_statement_origin_check': 'FIXED_STATEMENT' in resolution_src,
        'shared_resolver_has_structured_migration_check': 'STRUCTURED' in resolution_src,
        'citation_policy_keeps_archive_denial': 'SOURCE_ARCHIVE' in r2_src,
        'citation_policy_keeps_internal_denial': 'PROOF_INTERNAL' in r2_src,
        'citation_policy_keeps_review_allowlist': 'verified_assertion_ids' in r2_src,
    }
    blockers = []
    blockers.extend(f'{e["label"]}_unguarded' for e in endpoints if e['status'] != 'GUARDED')
    if direct_special: blockers.append('pi53_direct_registry_getter_remains')
    if not resolved_special: blockers.append('pi53_no_shared_resolver_call')
    if not boundary['shared_resolver_has_fixed_statement_origin_check']: blockers.append('fixed_origin_check_missing')
    if not boundary['shared_resolver_has_structured_migration_check']: blockers.append('structured_status_check_missing')
    for item in ('citation_policy_keeps_archive_denial', 'citation_policy_keeps_internal_denial', 'citation_policy_keeps_review_allowlist'):
        if not boundary[item]: blockers.append(item + '_missing')
    # Don't mistake registration-only, resolver internals, or citation policy for bypasses.
    classification = [
        {'file': 'phase164_r3_registry_search_connection.py', 'role': 'regular_citation_shared_resolver'},
        {'file': special_file, 'role': 'confirmed_fixed_literature_shared_resolver'},
        {'file': 'phase163_source_archive_registry.py', 'role': 'source_archive_registration_only'},
        {'file': 'phase164_r7_repository_root_resolution.py', 'role': 'internal_proof_root_shared_resolver'},
        {'file': 'phase164_r7_statement_resolution.py', 'role': 'common_resolver_and_citation_delegate'},
    ]
    return {
        'phase': '164 R7-R9', 'mode': 'READ_ONLY_SCOPED_CLOSURE', 'missing_files': [],
        'entrypoints': endpoints, 'candidate_sites': sites, 'classification': classification,
        'boundaries': boundary, 'blockers': blockers, 'scope_closed': not blockers,
        'status': 'STATIC_SCOPE_CLEAR_PENDING_TARGETED_PYTEST' if not blockers else 'NOT_CLOSED',
        'production_modified': False, 'full_pytest_run': False,
        'limitations': ['AST cannot prove exhaustive runtime reachability', 'source confirmation is not independent edition or mathematical certification', 'publication ordering and citation eligibility remain separately governed'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.root.resolve())
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'audit.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    lines = ['# Phase 164 R7-R9 — 最終再監査', '', f'- 静的判定: **{result["status"]}**', '- 本番ファイル変更: なし', '- 全体 pytest: 未実施', '', '## 標準入口']
    for item in result.get('entrypoints', []):
        lines.append(f'- {item["label"]}: {item["status"]} ({item["function"]})')
    lines.extend(['', '## π₅³ 固定文献経路', f'- 共通 resolver 呼出: {len(result.get("boundaries", {}).get("special_resolver_calls", []))}', f'- Registry 直接取得の残存: {len(result.get("boundaries", {}).get("special_direct_registry_getters", []))}', '', '## 残件'])
    lines.extend(f'- {b}' for b in result.get('blockers', []))
    if not result.get('blockers'): lines.append('- 静的な対象範囲の阻害要因なし。限定 pytest の結果で完了判定。')
    lines.extend(['', '## 制約', '- AST は動的な全経路の証明ではない。', '- 原著の独立照合・数学的真偽・文献掲載順を今回認定しない。', '- ProofStep の生成統一は次の R8 の対象。', ''])
    (args.output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    print('\n'.join(lines))
    if result.get('blockers') or result.get('missing_files'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
