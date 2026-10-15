"""Read-only Phase 165 R5-R5 audit: candidate ownership and source-level call sites."""
from __future__ import annotations
import ast
from collections import defaultdict
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
BASE_AUDIT = PROJECT / 'phase165_renderer_r5_r2_archive_classification' / 'audit.py'
OUTPUT = PACKAGE / 'audit_output'
CANONICAL = 'toda_group_proof_narrative_renderer'
PUBLIC = {'render_narrative_proof_model', 'render_toda_group_proof_narrative_markdown', 'render_toda_partial_proof_narrative_markdown'}
ENTRY = {'render_narrative_proof_model', 'render_partial_proof_markdown', 'render_toda_group_proof_narrative_markdown', 'render_toda_partial_proof_narrative_markdown', 'render_completed_shared_narrative', 'render_incomplete_public_narrative', 'render_validated_backward_proof_markdown', 'build_standard_web_group_proof_view', 'build_partial_web_group_proof_view'}


def load_base():
    if not BASE_AUDIT.is_file():
        raise RuntimeError('R5-R2 audit missing: ' + str(BASE_AUDIT))
    spec = importlib.util.spec_from_file_location('phase165_r5_r2_read_only_audit', BASE_AUDIT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def reference_sites(source: str, filename: str, target_modules: set[str]) -> list[dict]:
    """Find import and call sites; all matches are syntactic, not runtime proofs."""
    tree = ast.parse(source, filename=filename)
    imported_functions: dict[str, tuple[str, str]] = {}
    imported_modules: dict[str, str] = {}
    rows = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in target_modules:
            for alias in node.names:
                imported_functions[alias.asname or alias.name] = (node.module, alias.name)
                rows.append({'kind': 'import_from', 'target': node.module, 'function': alias.name, 'line': node.lineno})
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in target_modules:
                    imported_modules[alias.asname or alias.name] = alias.name
                    rows.append({'kind': 'import_module', 'target': alias.name, 'function': None, 'line': node.lineno})
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        if isinstance(callee, ast.Name) and callee.id in imported_functions:
            module, name = imported_functions[callee.id]
            rows.append({'kind': 'call', 'target': module, 'function': name, 'line': node.lineno})
        if isinstance(callee, ast.Attribute) and isinstance(callee.value, ast.Name) and callee.value.id in imported_modules:
            rows.append({'kind': 'call', 'target': imported_modules[callee.value.id], 'function': callee.attr, 'line': node.lineno})
    return rows


def definition_call_sites(source: str, filename: str, target_names: set[str]) -> dict[str, list[int]]:
    tree = ast.parse(source, filename=filename)
    matches = defaultdict(list)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in target_names:
            matches[node.func.id].append(node.lineno)
    return {key: sorted(set(value)) for key, value in sorted(matches.items())}


def analyze(project: Path = PROJECT) -> dict:
    base = load_base()
    prior = base.audit(project)
    candidates = prior['potential_alternative_narrative_helpers']
    target_modules = {Path(x['path']).stem for x in candidates}
    target_modules.add(CANONICAL)
    evidence = defaultdict(list)
    invalid = []
    all_files = base.production_and_test_files(project)
    for file in all_files:
        name = file.relative_to(project).as_posix()
        try:
            source = base.source_of(file)
            records = reference_sites(source, name, target_modules)
            for rec in records:
                rec['caller'] = name
                evidence[rec['target']].append(rec)
        except (SyntaxError, UnicodeDecodeError) as exc:
            invalid.append({'file': name, 'error': str(exc)})
    classifications = []
    for candidate in candidates:
        path = candidate['path']
        module = Path(path).stem
        functions = candidate['functions']
        text = base.source_of(project / path)
        local_calls = definition_call_sites(text, path, set(functions))
        inbound = sorted(evidence.get(module, []), key=lambda e: (e['caller'], e['line'], e['kind']))
        distinct_callers = sorted({e['caller'] for e in inbound if e['kind'] == 'call'})
        canonical_calls = sorted({e['function'] for e in evidence.get(CANONICAL, []) if e['caller'] == path and e['kind'] == 'call'})
        # Only classify direct evidence: no implicit claim that an indirect call tree is unified.
        if any(fn in ENTRY for fn in functions):
            role = 'POTENTIAL_INDEPENDENT_ENTRY'
        elif distinct_callers:
            role = 'CALLED_HELPER_REVIEW'
        else:
            role = 'NO_DIRECT_CALL_FOUND_REVIEW'
        classifications.append({
            'path': path, 'functions': functions, 'role': role,
            'callers': distinct_callers, 'inbound_sites': inbound[:120],
            'inbound_truncated': max(0, len(inbound) - 120),
            'same_module_call_sites': local_calls,
            'calls_canonical_public': canonical_calls,
        })
    independent = [c for c in classifications if c['role'] == 'POTENTIAL_INDEPENDENT_ENTRY']
    return {'phase': '165 R5-R5', 'status': 'REVIEW_REQUIRED',
            'timestamp_utc': datetime.now(timezone.utc).isoformat(),
            'scope': 'production root Python modules and official tests, as R5-R2',
            'source_audit': prior['status'], 'source_audit_failures': [k for k,v in prior['checks'].items() if not v],
            'counts': {'candidates': len(candidates), 'candidate_independent_entries': len(independent),
                       'called_helpers_for_review': sum(c['role']=='CALLED_HELPER_REVIEW' for c in classifications),
                       'no_direct_caller_for_review': sum(c['role']=='NO_DIRECT_CALL_FOUND_REVIEW' for c in classifications),
                       'parse_errors': len(invalid)},
            'classifications': classifications, 'parse_errors': invalid,
            'limitations': ['Static direct imports and calls do not prove runtime reachability.',
                            'Candidate list originates from the R5-R2 name-based discovery, not all Python render functions.',
                            'An entry function is a review flag, not proof that it bypasses the canonical renderer.',
                            'A helper call may be reached from a separate legacy route; call graphs require review.',
                            'Historical Phase162 fixture failures remain unresolved; this package does not run them.',
                            'No mathematical correctness or arbitrary (n,k) search completeness is certified.']}


def main():
    OUTPUT.mkdir(exist_ok=True)
    data = analyze()
    (OUTPUT / 'audit.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Phase 165 R5-R5 補助 Renderer 呼び出し監査', '',
             f"状態: **{data['status']}**（監査結果の人手レビューが必要）", '',
             f"基準 R5-R2: `{data['source_audit']}`", '', '## 件数', '']
    lines += [f'- {key}: {value}' for key,value in data['counts'].items()]
    if data['source_audit_failures']:
        lines += ['', '## 前提検査の失敗', ''] + ['- '+v for v in data['source_audit_failures']]
    lines += ['', '## 候補ごとの分類', '']
    for item in data['classifications']:
        lines += [f"### `{item['path']}`", '', f"- 判定: `{item['role']}`",
                  '- 定義: '+', '.join('`'+x+'`' for x in item['functions']),
                  '- 直接呼出元: '+(', '.join('`'+x+'`' for x in item['callers']) if item['callers'] else '検出なし')]
        calls = [r for r in item['inbound_sites'] if r['kind']=='call']
        lines += ['- 呼出箇所: '+(', '.join(f"`{r['caller']}:{r['line']}`→`{r['function']}`" for r in calls[:25]) if calls else '検出なし')]
        if item['inbound_truncated']:
            lines += [f"- 記録省略: {item['inbound_truncated']}件（JSON にも上限あり）"]
        lines += ['']
    lines += ['## 注意', ''] + ['- '+x for x in data['limitations']]
    (OUTPUT / 'review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'status':data['status'], 'counts':data['counts'],
                      'baseline':data['source_audit'],
                      'independent_entry_candidates':[x['path'] for x in data['classifications'] if x['role']=='POTENTIAL_INDEPENDENT_ENTRY'],
                      'report':str(OUTPUT/'review.md'),'full_pytest_run':False},ensure_ascii=False,indent=2))
    if data['source_audit_failures'] or data['counts']['parse_errors']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
