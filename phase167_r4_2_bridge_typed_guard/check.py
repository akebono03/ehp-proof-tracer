import json
from pathlib import Path
p=Path(__file__).resolve().parent
before=json.loads((p/'before.json').read_text(encoding='utf-8'))
after=json.loads((p/'after.json').read_text(encoding='utf-8'))
for key,baseline in before.items():
    current=after[key]
    if key=='pi4^3':
        removed=list(baseline)
        for line in current:
            removed.remove(line)
        assert len(removed)==1,(removed,baseline,current)
        assert removed[0].replace(' ','').startswith('\\eta_{3}=E\\eta_{2}'),removed
    else:
        assert baseline==current,key
print('PASS: only duplicate typed suspension bridge removed; other 1-stem narratives identical')
