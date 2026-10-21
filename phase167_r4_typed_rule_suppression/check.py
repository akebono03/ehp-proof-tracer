from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
before=json.loads((ROOT/'before.json').read_text(encoding='utf-8'))
after=json.loads((ROOT/'after.json').read_text(encoding='utf-8'))
assert before.keys()==after.keys()
for key in before:
    old=before[key]; new=after[key]
    assert old['key']==new['key'] and old['mode']==new['mode'], key
    if key=='pi4^3':
        filtered=[line for line in old['lines'] if line.strip()!='infinite cyclic quotient structure']
        assert len(filtered)==len(old['lines'])-1, 'expected exactly one line to remove'
        assert filtered==new['lines'], 'unrelated narrative change: '+key
    else:
        assert old==new, 'unexpected change: '+key
print('PASS: only the internal rule name removed in pi4^3; other 1-stem output unchanged')
