"""R27-R13: conservative classification of legacy dependencies; read-only."""
from __future__ import annotations
import ast
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

SYMBOLS = (
 'build_standard_production_proof_repository','build_standard_proof_repository',
 'build_toda_prop515_upper_bootstrap','build_toda_prop515_sigma_chain_bootstrap',
 'build_toda_upstream_bootstrap','build_standard_toda_report',
 'build_toda_group_result_proof_replay','ProofRepository','ProofRepositoryEntry',
 'build_standard_web_group_proof_view',
)
PROTECTED = frozenset((
 'unified_statement_registry.py','phase163_r4_registry_bridge.py',
 'phase165_r52_r2_search_adapter.py','toda_rules.py','proof.py','theorem_facts.py',
))
REQUIRED = ('web_group_proof.py','web_group_proof_common.py','main.py',
 'web_app.py','standard_production_repository.py','proof_repository.py',
 'phase165_r52_r5_auto_search.py','phase165_r52_r3_web_adapter.py')
ROOT_API = frozenset(('main.py','web_app.py','web_group_query.py','web_group_proof.py',
 'phase165_r52_r4_flask_bridge.py','phase165_r52_r5_auto_search.py',
 'phase165_r52_r3_web_adapter.py','toda_calculation_facade.py',
 'phase165_r9_production_wiring.py'))

def category(rel: Path) -> str:
    name = rel.name
    if rel.as_posix() in PROTECTED:
        return 'PROTECTED'
    if name.startswith('test_') or 'tests' in rel.parts:
        return 'TEST_ONLY_REFERENCE'
    if len(rel.parts) > 1:
        return 'HISTORICAL_OR_PACKAGE_REFERENCE'
    if name.startswith('audit_') or name.startswith('probe_'):
        return 'ROOT_AUDIT_REFERENCE'
    if name in ROOT_API:
        return 'PUBLIC_ENTRY_OR_BRIDGE'
    return 'ROOT_PRODUCTION_OR_UNCLASSIFIED'

def refs(tree: ast.AST):
    records = []
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and node.name in SYMBOLS:
            records.append((node.name,'definition',node.lineno))
        elif isinstance(node,ast.ImportFrom):
            for a in node.names:
                if a.name in SYMBOLS:
                    records.append((a.name,'import',node.lineno))
        elif isinstance(node,ast.Call):
            callee=node.func
            name=callee.id if isinstance(callee,ast.Name) else callee.attr if isinstance(callee,ast.Attribute) else ''
            if name in SYMBOLS:
                records.append((name,'call',node.lineno))
        elif isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load) and node.id in SYMBOLS:
            records.append((node.id,'name_read',node.lineno))
    return sorted(set(records),key=lambda x:(x[2],x[0],x[1]))

def collect(root: Path)->dict:
    missing=[p for p in REQUIRED if not (root/p).is_file()]
    if missing: raise FileNotFoundError('Required R27-R11 installation missing: '+', '.join(missing))
    entries=[]; skipped=[]
    for p in sorted(root.rglob('*.py')):
        rel=p.relative_to(root)
        if any(x in ('.git','.venv','venv','__pycache__','site-packages') for x in rel.parts): continue
        try: tree=ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
        except (UnicodeError,SyntaxError) as error:
            skipped.append({'file':rel.as_posix(),'reason':type(error).__name__});continue
        scope=category(rel)
        for sym,kind,line in refs(tree):
            entries.append({'path':rel.as_posix(),'scope':scope,'symbol':sym,'kind':kind,'line':line,
             'review_status':'LIVE_DEPENDENCY_REVIEW_REQUIRED' if scope in ('PUBLIC_ENTRY_OR_BRIDGE','ROOT_PRODUCTION_OR_UNCLASSIFIED','PROTECTED') else 'REFERENCE_ONLY_NOT_PROOF_OF_LIVENESS'})
    counts=dict(sorted(Counter(e['scope'] for e in entries).items()))
    files=dict(sorted(Counter(scope for path, scope in {(x['path'], x['scope']) for x in entries}).items()))
    live=sorted({e['path'] for e in entries if e['scope'] in ('PUBLIC_ENTRY_OR_BRIDGE','ROOT_PRODUCTION_OR_UNCLASSIFIED') and e['kind']!='definition'})
    return {'phase':'165 R27-R13','mode':'READ_ONLY_CLASSIFY_DEPENDENCY_EDGES',
     'production_files_modified':False,'full_pytest_run':False,'deletion_authorized':False,
     'files_with_references':len({e['path'] for e in entries}),'reference_events':len(entries),
     'event_counts_by_scope':counts,'file_counts_by_scope':files,
     'live_consumer_review_paths':live,'protected_files':sorted(PROTECTED),
     'dynamic_imports_and_runtime_use_verified':False,
     'unused_code_certified':False,'parse_skips':skipped,'entries':entries,
     'next_action':'Review root production/public consumers and dynamic calls before approving any deletion'}

def main()->int:
    report=collect(Path.cwd());out=Path(__file__).resolve().parent
    (out/'audit_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (out/'dependency_edges.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=('path','scope','symbol','kind','line','review_status'));w.writeheader();w.writerows(report['entries'])
    summary={k:v for k,v in report.items() if k not in ('entries','parse_skips')}
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print('Report:',out/'audit_report.json')
    return 0
if __name__=='__main__': raise SystemExit(main())
