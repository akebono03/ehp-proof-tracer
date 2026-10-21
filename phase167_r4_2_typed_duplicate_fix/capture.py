from __future__ import annotations
import json
from pathlib import Path
from web_group_proof import build_standard_web_group_proof_view

OUT = Path(__file__).resolve().parent
rows = {}
for n in range(2, 7):
    name=f'pi{n+1}^{n}'
    view=build_standard_web_group_proof_view(n, 1, 2, 'narrative')
    lines = []
    for line in view.rendered_lines:
        if isinstance(line, str):
            lines.append(line)
        else:
            lines.append(str(getattr(line, 'prefix', '')) + ' ' + str(getattr(line, 'statement_latex', '') or '') + ' ' + str(getattr(line, 'suffix', '')))
    text='\n'.join(lines)
    rows[name]={'key':view.key,'mode':view.mode,'lines':lines}
    print('CAPTURE', name, view.key, len(lines), 'lines')
(OUT / 'capture.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
