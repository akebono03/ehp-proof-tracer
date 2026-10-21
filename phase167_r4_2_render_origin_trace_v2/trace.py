from __future__ import annotations
import inspect
import json
import sys
from pathlib import Path
from web_group_proof import build_standard_web_group_proof_view

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WATCH = {'toda_group_proof_narrative_renderer.py', 'toda_group_proof_narrative_shared_components.py', 'toda_group_proof_aggregate_statement_renderer.py', 'toda_human_readable_renderer.py', 'toda_proof_narrative_renderer.py', 'toda_group_proof_narrative_blocks.py'}
KEY_TYPES = {'TodaEtaFamilyDefinitionStatement','GeneratorSuspension','GeneratorImage','Relation'}
counts = {}
events = []

def traced(frame, event, arg):
    if event != 'call':
        return
    path = Path(frame.f_code.co_filename)
    if path.name not in WATCH:
        return
    fun = frame.f_code.co_name
    counts[fun] = counts.get(fun, 0) + 1
    if len(events) >= 250:
        return
    variables = frame.f_locals
    found=[]
    for name in ('proof_step','step','statement','premise_step','parent_step'):
        obj=variables.get(name)
        if obj is not None:
            conclusion=getattr(obj,'conclusion',obj)
            kind=type(conclusion).__name__
            if kind in KEY_TYPES:
                found.append({'variable':name,'conclusion_type':kind,'repr':repr(conclusion)[:900]})
    if found:
        events.append({'file':path.name,'function':fun,'line':frame.f_code.co_firstlineno,'arguments':found})

def main():
    sys.setprofile(traced)
    try:
        view=build_standard_web_group_proof_view(3,1,2,'narrative')
    finally:
        sys.setprofile(None)
    lines=[s if isinstance(s,str) else str(getattr(s,'prefix','')) + str(getattr(s,'statement_latex','') or '') + str(getattr(s,'suffix','')) for s in view.rendered_lines]
    report={'mode':'READ_ONLY_PROFILE','key':view.key,'profiled_calls':counts,'typed_events':events,'typed_events_count':len(events),'web_lines':lines,'production_modified':False}
    (HERE/'trace_v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('READ_ONLY: matched',len(events),'typed events; Web lines:',len(lines))
    print('REPORT:',HERE/'trace_v2.json')
if __name__=='__main__':
    main()
