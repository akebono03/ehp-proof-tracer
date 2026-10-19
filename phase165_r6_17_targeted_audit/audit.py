from __future__ import annotations
import ast
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'phase165_r6_audit_results' / 'r6_17_targeted_audit'
CHECKS = {
 'goal_boundary': ('phase165_goal_only_search.py', 'construct_registered_group_proof'),
 'web_pi53': ('phase164_r5_web_registry_connection.py', 'build_phase164_r5_web_pi5_3_proof'),
 'prop51': ('tests/test_phase157_r2_literature_statement_boundary.py', 'test_phase157_r2_prop51_inventory_preserves_current_four_components'),
 'reference_selection': ('tests/test_phase157_r5_r4_generic_reference_selection.py', 'test_phase157_r5_r4_generic_filter_applies_without_representative_target_guard'),
 'beta': ('tests/test_phase150_rc4_5b_3_r1_beta_latex.py', 'test_phase150_rc4_5b_3_r1_beta_uses_general_greek_latex_table'),
 'historical_import': ('tests/test_phase148_rc2_4_repair_r4_1_r1.py', 'test_phase148_rc2_4_repair_r4_1_r1_argument_locations_use_current_argument_api'),
 'missing_dependency': ('tests/test_proof_repository.py', 'test_phase78_actual_steps_register_and_retrieve_without_graph_changes'),
}

def get_func(path: Path, name: str):
    tree=ast.parse(path.read_text(encoding='utf-8-sig'),filename=str(path))
    return next((node for node in ast.walk(tree) if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name==name),None)

def audit(root: Path):
    rows=[]
    for label,(relative,name) in CHECKS.items():
        file=root/relative
        if not file.is_file():
            rows.append({'id':label,'path':relative,'status':'MISSING_FILE'});continue
        try:
            node=get_func(file,name)
            if node is None:
                rows.append({'id':label,'path':relative,'status':'MISSING_FUNCTION'});continue
            lines=file.read_text(encoding='utf-8-sig').splitlines()
            rows.append({'id':label,'path':relative,'status':'FOUND','function':name,'first_line':node.lineno,'last_line':node.end_lineno,'source':'\n'.join(lines[node.lineno-1:node.end_lineno])})
        except (SyntaxError,UnicodeError) as exc:
            rows.append({'id':label,'path':relative,'status':'PARSE_ERROR','error':str(exc)})
    web=next((r for r in rows if r['id']=='web_pi53'),{})
    boundary=next((r for r in rows if r['id']=='goal_boundary'),{})
    call_args=[]
    for n in ast.walk(get_func(root/'phase164_r5_web_registry_connection.py','build_phase164_r5_web_pi5_3_proof')) if web.get('status')=='FOUND' else []:
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='construct_registered_group_proof':
            call_args=[k.arg for k in n.keywords]
    required=['goal','citing_assertion_id']
    return {'phase':'165 R6-17','mode':'read_only','generated_utc':datetime.now(timezone.utc).isoformat(),'status':'AUDITED_NO_CHANGES' if all(r['status']=='FOUND' for r in rows) else 'NEEDS_REVIEW','web_pi53_supplied_keywords':call_args,'web_pi53_missing_required_context':[k for k in required if k not in call_args], 'boundary_found':boundary.get('status')=='FOUND','items':rows,'full_pytest_run':False}

def main():
    result=audit(ROOT)
    OUT.mkdir(parents=True,exist_ok=True)
    report=OUT/'report.json';report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    concise={k:v for k,v in result.items() if k!='items'}
    concise['items']=[{'id':row['id'],'status':row['status'],'path':row['path'],'first_line':row.get('first_line')} for row in result['items']]
    print(json.dumps(concise,ensure_ascii=False,indent=2))
    print('Report:',report)
    return 0 if result['status']=='AUDITED_NO_CHANGES' else 1

if __name__=='__main__':
    raise SystemExit(main())
