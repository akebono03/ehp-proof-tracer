import json,sys
from pathlib import Path
from web_group_proof import build_standard_web_group_proof_view
out=Path(__file__).resolve().parent /sys.argv[1]
result={}
for n in (2,3,4,5,6):
    view=build_standard_web_group_proof_view(n,1,2,'narrative')
    lines=[x if isinstance(x,str) else str(getattr(x,'prefix',''))+str(getattr(x,'statement_latex','') or '')+str(getattr(x,'suffix','')) for x in view.rendered_lines]
    result[str(n)]={'key':view.key,'lines':lines}
    print('CAPTURE',f'pi{n+1}^{n}',view.key,len(lines),'lines')
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
