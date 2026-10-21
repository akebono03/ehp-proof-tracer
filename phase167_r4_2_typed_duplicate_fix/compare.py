from __future__ import annotations
import json
from pathlib import Path
base=Path(__file__).resolve().parent
before=json.loads((base/'before.json').read_text(encoding='utf-8'))
after=json.loads((base/'after.json').read_text(encoding='utf-8'))
assert before.keys()==after.keys()
for key in before:
    assert before[key]['key']==after[key]['key'] and before[key]['mode']==after[key]['mode'],key
    if key=='pi4^3':
        # R4-1 is already applied. Remove only the first, previously verified equation.
        expected=[x for x in before[key]['lines'] if x.strip()!=r'\eta_{3}=E\eta_{2}.']
        assert len(expected)==len(before[key]['lines'])-1, 'one eta-definition display expected'
        assert expected==after[key]['lines'], 'unexpected pi4^3 narrative differences'
        assert any(r'E(\eta_{2})' in x for x in after[key]['lines'])
    else:
        assert before[key]==after[key],key
print('PASS: only the duplicated eta-definition line removed; other 1-stem narratives unchanged')
