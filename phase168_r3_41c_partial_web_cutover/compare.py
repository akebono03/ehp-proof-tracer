"""Fail unless completed four, explicit legacy and direct fallback are byte-identical."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
PACKAGE=Path(__file__).resolve().parent
OUT=PACKAGE/'output'
NAMES=('pi3_2','pi4_3','pi5_4','pi6_5','legacy_explicit','direct_fallback')

def main():
    report=[]
    for name in NAMES:
        before=(OUT/f'{name}_before.md').read_bytes()
        after=(OUT/f'{name}_after.md').read_bytes()
        same=before==after
        report.append({'case':name,'identical':same,
                       'sha256':hashlib.sha256(after).hexdigest()})
        print('UNCHANGED' if same else 'CHANGED',name)
        if not same:
            raise AssertionError(name+' narrative changed')
    (OUT/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('FOUR_COMPLETED_AND_EXPLICIT_LEGACY_AND_DIRECT_FALLBACK_BYTE_IDENTICAL')
if __name__=='__main__':
    main()
