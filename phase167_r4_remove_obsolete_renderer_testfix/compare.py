import json,sys
from pathlib import Path
base=Path(sys.argv[1]);after=Path(sys.argv[2]); diffs=[]
for n in (2,3,4,5,6):
    name=f'pi{n+1}_{n}.json'
    x=json.loads((base/name).read_text(encoding='utf-8'))
    y=json.loads((after/name).read_text(encoding='utf-8'))
    for key in x:
        if x[key]!=y[key]:diffs.append(f'{name}: {key}')
print('CHANGED FIELDS:',diffs)
if diffs:sys.exit(1)
print('PASS: 1-stem search/proof/Narrative unchanged for n=2..6')
