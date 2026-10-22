from __future__ import annotations
import json
import sys
from pathlib import Path
from web_group_proof import build_standard_web_group_proof_view
HERE=Path(__file__).resolve().parent
TYPES={'GeneratorSuspension','TodaEtaFamilyDefinitionStatement'}
events=[]
blocks=[]
def short(obj):
    return repr(obj)[:420]
def trace(frame, event, arg):
    fn=frame.f_code.co_name
    if event=='call' and fn=='render_toda_group_proof_narrative_argument_body_markdown':
        for name in ('blocks','local_body_blocks'):
            for j,block in enumerate(frame.f_locals.get(name,())):
                items=[{'index':i,'type':type(s.conclusion).__name__,'statement':short(s.conclusion)} for i,s in enumerate(block.steps) if type(s.conclusion).__name__ in TYPES]
                if items: blocks.append({'collection':name,'block_index':j,'role':str(block.role),'steps':items})
    if fn=='_render_generic_narrative_step' and event=='return':
        step=frame.f_locals.get('proof_step')
        if step is not None and type(step.conclusion).__name__ in TYPES:
            events.append({'function':fn,'statement_type':type(step.conclusion).__name__,'statement':short(step.conclusion),'return':str(arg)[:300]})
    if fn=='_render_generic_narrative_proof_block' and event=='call':
        idx=frame.f_locals.get('block_index')
        source=frame.f_locals.get('blocks',())
        if isinstance(idx,int) and idx<len(source):
            block=source[idx]
            blocks.append({'collection':'actual_render_block','block_index':idx,'role':str(block.role),'steps':[{'index':i,'type':type(s.conclusion).__name__,'statement':short(s.conclusion)} for i,s in enumerate(block.steps) if type(s.conclusion).__name__ in TYPES]})
    return trace

def main():
    sys.setprofile(trace)
    try: view=build_standard_web_group_proof_view(3,1,2,'narrative')
    finally: sys.setprofile(None)
    lines=[x if isinstance(x,str) else str(getattr(x,'prefix',''))+str(getattr(x,'statement_latex','') or '')+str(getattr(x,'suffix','')) for x in view.rendered_lines]
    result={'mode':'read_only','blocks':blocks,'step_render_events':events,'web_lines':lines,'production_modified':False}
    path=HERE/'origin.json'
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('READ_ONLY: relevant blocks:',len(blocks),'typed render returns:',len(events))
    print('REPORT:',path)
if __name__=='__main__':main()
