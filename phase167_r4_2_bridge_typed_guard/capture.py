from pathlib import Path
import json
from web_group_proof import build_standard_web_group_proof_view
out=Path(__file__).resolve().parent
results={}
for n in range(2,7):
    view=build_standard_web_group_proof_view(n,1,2,'narrative')
    lines=[x if isinstance(x,str) else str(getattr(x,'prefix',''))+str(getattr(x,'statement_latex','') or '')+str(getattr(x,'suffix','')) for x in view.rendered_lines]
    results[f'pi{n+1}^{n}']=lines
    print('CAPTURE',f'pi{n+1}^{n}',len(lines),'lines')
(out / ('after.json' if __import__('sys').argv[-1]=='after' else 'before.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
