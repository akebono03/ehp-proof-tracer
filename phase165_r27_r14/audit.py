"""Phase 165 R27-R14: read-only root consumer triage from R27-R13 evidence."""
from __future__ import annotations

import ast
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

SCOPES = frozenset({'PUBLIC_ENTRY_OR_BRIDGE', 'ROOT_PRODUCTION_OR_UNCLASSIFIED'})
PROTECTED = frozenset({'unified_statement_registry.py', 'phase163_r4_registry_bridge.py', 'phase165_r52_r2_search_adapter.py', 'proof.py', 'toda_rules.py', 'theorem_facts.py'})
PUBLIC_MODULES = ('main.py', 'cli.py', 'web_app.py', 'web_generator_proof.py', 'web_generator_exploration.py', 'web_generator_applicability.py', 'web_operation_query.py', 'web_group_proof.py')
TARGET_SYMBOLS = frozenset({'build_standard_production_proof_repository', 'build_standard_proof_repository', 'build_toda_prop515_upper_bootstrap', 'ProofRepository', 'ProofRepositoryEntry', 'build_standard_toda_report', 'build_toda_group_result_proof_replay'})

def source_bucket(path: str) -> str:
    if '.phase' in path or '_backup' in path or 'backup_' in path:
        return 'BACKUP_ROOT_FALSE_POSITIVE'
    if path.startswith('repository_generator_') or 'generator' in path:
        return 'GENERATOR_CONSUMER_REVIEW'
    if 'operation' in path:
        return 'OPERATION_CONSUMER_REVIEW'
    if path.startswith('standard_') or 'bootstrap' in path:
        return 'LEGACY_BUILDER_REVIEW'
    if path.startswith('phase'):
        return 'PHASE_BRIDGE_REVIEW'
    if path in PUBLIC_MODULES or path.startswith('web_'):
        return 'PUBLIC_ENTRY_REVIEW'
    return 'OTHER_ROOT_CONSUMER_REVIEW'

def collect(root: Path) -> dict:
    report_path = root / 'phase165_r27_r13' / 'audit_report.json'
    if not report_path.is_file():
        raise FileNotFoundError('R27-R13 audit_report.json is required; run R27-R13-R1 first')
    source = json.loads(report_path.read_text(encoding='utf-8'))
    if source.get('phase') != '165 R27-R13' or source.get('mode') != 'READ_ONLY_CLASSIFY_DEPENDENCY_EDGES':
        raise ValueError('unexpected R27-R13 evidence contract')
    events = [x for x in source['entries'] if x['scope'] in SCOPES]
    per_path = defaultdict(list)
    for item in events:
        per_path[item['path']].append(item)
    rows = []
    for path, items in sorted(per_path.items()):
        candidate = root / path
        exists = candidate.is_file()
        parse_ok = False
        funcs = set()
        if exists:
            try:
                tree = ast.parse(candidate.read_text(encoding='utf-8-sig'), filename=path)
            except (SyntaxError, UnicodeError):
                pass
            else:
                parse_ok = True
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        funcs.add(node.name)
        symbols = sorted({x['symbol'] for x in items})
        rows.append({'path':path, 'category':source_bucket(path), 'scopes':';'.join(sorted({x['scope'] for x in items})), 'symbols':';'.join(symbols), 'reference_events':len(items), 'functions_declared':';'.join(sorted(funcs)), 'exists':exists, 'parses':parse_ok, 'classification':'CANDIDATE_NOT_RUNTIME_VERIFIED'})
    direct_importers = []
    for filename in PUBLIC_MODULES:
        source_file = root / filename
        if not source_file.is_file():
            continue
        try:
            parsed = ast.parse(source_file.read_text(encoding='utf-8-sig'))
        except (SyntaxError, UnicodeError):
            continue
        for node in ast.walk(parsed):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name in TARGET_SYMBOLS or (node.module and (node.module.startswith('repository_') or node.module in ('standard_production_repository','toda_calculation_facade'))):
                        direct_importers.append({'entry':filename,'dependency_module':node.module or '', 'symbol':alias.name,'line':node.lineno,'verification':'STATIC_IMPORT_ONLY'})
    counts = Counter(row['category'] for row in rows)
    return {'phase':'165 R27-R14', 'mode':'READ_ONLY_LIVE_CONSUMER_TRIAGE', 'production_files_modified':False, 'full_pytest_run':False,'deletion_authorized':False,'upstream_reference_events':len(events),'candidate_root_files':len(rows),'candidate_counts_by_category':dict(sorted(counts.items())), 'public_entry_static_imports':direct_importers, 'review_rows':rows,'protected_files':sorted(PROTECTED),'dynamic_imports_and_runtime_use_verified':False, 'reachable_from_public_entry_certified':False,'next_action':'Inspect Generator/Operation public call chains function-by-function before migrating consumers or deleting builders'}

def main() -> int:
    root = Path.cwd()
    report = collect(root)
    out = Path(__file__).resolve().parent
    (out / 'audit_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    with (out / 'live_consumer_candidates.csv').open('w',newline='',encoding='utf-8-sig') as f:
        fieldnames=['path','category','scopes','symbols','reference_events','functions_declared','exists','parses','classification']
        writer = csv.DictWriter(f, fieldnames=fieldnames);writer.writeheader();writer.writerows(report['review_rows'])
    (out / 'public_entry_imports.json').write_text(json.dumps(report['public_entry_static_imports'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('review_rows','public_entry_static_imports')},ensure_ascii=False,indent=2))
    print('Public entry static imports:',len(report['public_entry_static_imports']))
    print('Report:',out / 'audit_report.json')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
