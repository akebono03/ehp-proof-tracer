from __future__ import annotations
import json
import sys
from pathlib import Path
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import render_partial_proof_markdown
from web_group_proof import build_standard_web_group_proof_view

out=Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
# Phase 167 R4: 1-stem only. n=2,3: unstable; n>=4 stable.
for n in (2,3,4,5,6):
    res=search_group_from_registered_goal(n=n,k=1)
    view=build_standard_web_group_proof_view(n,1,2,'narrative')
    rendered=[]
    for line in view.rendered_lines:
        if isinstance(line,str):rendered.append(line)
        else:rendered.append(str(getattr(line,'prefix',''))+' '+str(getattr(line,'statement_latex','') or '')+' '+str(getattr(line,'suffix','')))
    payload={
        'status':res.status.value,
        'conclusion':repr(res.conclusion),
        'open_goals':[repr(x) for x in res.open_goals],
        'steps':[{'rule':str(getattr(step.rule,'value',step.rule)), 'conclusion':repr(step.conclusion), 'inference':str(getattr(step.inference_rule,'name','')),'premises':[repr(p.conclusion) for p in step.premises]} for step in res.proven_steps],
        'web_key':view.key,'web_mode':view.mode,
        'web_lines':rendered,
        'markdown':render_partial_proof_markdown(res),
    }
    (out/f'pi{n+1}_{n}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'CAPTURE pi{n+1}^{n}: {payload["status"]}, {len(rendered)} web lines')
