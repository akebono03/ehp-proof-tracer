"""Non-destructive inventory of Phase 49/56 legacy test dependencies."""
import ast
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
DEST = ROOT / 'phase165_r6_audit_results' / 'phase49_56_boundary'
DEST.mkdir(parents=True, exist_ok=True)
FILES = (
    'tests/test_phase49_probe.py',
    'tests/test_phase56_probe.py',
    'tests/test_phase56_pi_i_minus_1_1_zero.py',
    'tests/test_phase56_prop44_eta2_specialization.py',
    'tests/test_phase56_prop44_second_summand_restriction.py',
    'tests/test_phase56_toda52_composition_isomorphism.py',
)
records = []
for name in FILES:
    path = ROOT / name
    if not path.is_file():
        records.append({'file':name,'status':'MISSING','tests':[]})
        continue
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=name)
    tests = [n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test_')]
    imports = sorted({alias.name for n in ast.walk(tree) if isinstance(n,ast.Import) for alias in n.names} | {n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module})
    records.append({'file':name,'status':'REVIEW_REQUIRED','test_count':len(tests),'tests':tests,'imports':imports,
                    'replacement_coverage_verified':False,'action':'KEEP pending equivalence review'})
report = {'phase':'165 R6','generated_utc':datetime.now(timezone.utc).isoformat(),
          'status':'READ_ONLY','files':records,'repo_files_modified':0,
          'legacy_tests_retired':0,'coverage_equivalence_verified':False,
          'note':'Current search boundary tests do not replace mathematical proof-ancestry assertions.'}
output=DEST/'report.json'
output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'files_checked':len(records),'test_functions':sum(x.get('test_count',0) for x in records),'coverage_equivalence_verified':False,'report':str(output)},ensure_ascii=False,indent=2))
