"""Capture completed common Narratives, explicit legacy, and direct fallback unchanged."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
from phase168_r3_38_frozen_fulltext_audit.audit import capture
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from web_group_proof import build_standard_web_group_proof_view

PACKAGE=Path(__file__).resolve().parent
OUT=PACKAGE/'output'
CASES=(('pi3_2',2,1),('pi4_3',3,1),('pi5_4',4,1),('pi6_5',5,1))

def view_text(view):
    return '\n'.join(''.join(segment.value for segment in line.segments)
                     for line in view.rendered_lines)

def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ('before','after'):
        raise SystemExit('usage: capture before|after')
    stage=sys.argv[1]
    OUT.mkdir(parents=True,exist_ok=True)
    summary=[]
    for key,n,k in CASES:
        markdown,model,view=capture(n,k)
        if view.partial_result:
            raise AssertionError('Expected complete '+key)
        content=markdown.encode('utf-8')
        (OUT/f'{key}_{stage}.md').write_bytes(content)
        summary.append({'case':key,'sha256':hashlib.sha256(content).hexdigest(),
                        'steps':len(model.steps),'refs':len(model.citations)})
        print(stage,key,'steps',len(model.steps),'refs',len(model.citations))
    legacy=build_standard_web_group_proof_view(2,1,citation_source='legacy')
    (OUT/f'legacy_explicit_{stage}.md').write_text(view_text(legacy),encoding='utf-8')
    partial=make_partial_proof_result(n=3,k=2,status=ProofSearchStatus.PARTIAL,
                                      open_goals=('unknown',))
    fallback=build_partial_web_group_proof_view(partial)
    (OUT/f'direct_fallback_{stage}.md').write_text(view_text(fallback),encoding='utf-8')
    (OUT/f'capture_{stage}.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

if __name__=='__main__':
    main()
