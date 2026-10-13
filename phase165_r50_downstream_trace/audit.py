from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUTPUT = ROOT / 'phase165_r50_downstream_trace_output'

STAGES = {
 'contrib': ('filter_toda_group_proof_narrative_reference_entries_by_body_usage','restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage','link_toda_group_proof_narrative_unmarked_reference_consumers','filter_toda_group_proof_narrative_reference_entries_by_step_usage','prune_toda_group_proof_narrative_root_zero_direct_premise_references','link_toda_group_proof_narrative_reference_body_consumers','finalize_phase165_r49_typed_reason_order','render_toda_group_proof_narrative_multi_argument_with_contributions_markdown'),
 'narrative': ('_phase158_baseline_render_toda_group_proof_narrative_markdown','_phase158_normalize_public_narrative_contract','_phase159_r1_7c_r4_normalize_public_map_property_prose','_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning','_phase159_r1_7c_r4_reorder_public_equation_reference_conclusions','render_toda_group_proof_narrative_markdown'),
}

def summarize(value):
 if isinstance(value,str):
  lines=[x for x in value.splitlines() if any(t in x for t in ('Im','ker','零写像','[R3]'))]
  return {'Im': 'Im' in value, 'ker':'ker' in value,'length':len(value),'relevant_lines':lines[:10]}
 if isinstance(value,tuple):
  return {'tuple_len':len(value),'str_items':[summarize(v) for v in value if isinstance(v,str)]}
 return {'type':type(value).__name__}

def main():
 import toda_group_proof_narrative_contribution_renderer as contrib
 import toda_group_proof_narrative_renderer as narrative
 from web_group_proof import build_standard_web_group_proof_view
 OUTPUT.mkdir(parents=True,exist_ok=True)
 report={'phase':'165 R50 downstream exact-loss audit','mode':'READ_ONLY','status':'error','events':[],'production_files_modified':False,'pytest_run':False}
 installed=[]
 try:
  for module, label in ((contrib,'contrib'),(narrative,'narrative')):
   for name in STAGES[label]:
    original=getattr(module,name,None)
    if not callable(original):
     report['events'].append({'stage':label+'.'+name,'status':'NOT_FOUND'})
     continue
    def wrap(*args,__original=original,__name=label+'.'+name,**kwargs):
     result=__original(*args,**kwargs)
     report['events'].append({'stage':__name,'result':summarize(result)})
     return result
    setattr(module,name,wrap)
    installed.append((module,name,original))
  view=build_standard_web_group_proof_view(n=2,k=1,max_depth=2,mode='narrative')
  text='\n'.join(line.prefix+(line.statement_latex or '')+line.suffix for line in view.rendered_lines)
  report['final_web']=summarize(text)
  report['status']='ok'
 except Exception as exc:
  report['error']=repr(exc)
 finally:
  for module,name,original in reversed(installed):
   setattr(module,name,original)
 (OUTPUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 states=[(e['stage'],e.get('result',{}).get('Im'),e.get('result',{}).get('ker')) for e in report['events']]
 (OUTPUT/'report.md').write_text('# R50 downstream audit\n\n'+ '\n'.join(f'- `{a}`: Im={b}, ker={c}' for a,b,c in states)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'events':len(report['events']),'stage_flags':states,'final_web':report.get('final_web'),'error':report.get('error'),'output_json':str(OUTPUT/'audit.json'),'production_files_modified':False,'pytest_run':False},ensure_ascii=False,indent=2))
 return 0 if report['status']=='ok' else 1

if __name__=='__main__':
 raise SystemExit(main())
