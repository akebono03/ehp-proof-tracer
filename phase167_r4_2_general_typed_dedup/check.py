from pathlib import Path
import json,difflib
here=Path(__file__).resolve().parent
before=json.loads((here/'before.json').read_text(encoding='utf8'))
after=json.loads((here/'after.json').read_text(encoding='utf8'))
for n in ('2','4','5','6'):
    assert after[n]==before[n],f'Unexpected 1-stem change: {n}'
assert before['3']['key']==after['3']['key']=='generic-complete-proof'
old=before['3']['lines'];new=after['3']['lines']
removed=list(difflib.ndiff(old,new))
deleted=[x[2:] for x in removed if x.startswith('- ')]
added=[x[2:] for x in removed if x.startswith('+ ')]
assert len(deleted)==1 and not added,(deleted,added)
assert deleted[0] in (r'\eta_{3}=E\eta_{2}.',r'E(\eta_{2}) = \eta_{3}.'),deleted
assert len(new)==len(old)-1
print('PASS: one duplicate identity removed; all other lines unchanged')
