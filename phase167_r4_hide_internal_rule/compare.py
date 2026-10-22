import json,sys,difflib
from pathlib import Path
before,after=map(Path,sys.argv[1:3]); target='infinite cyclic quotient structure'
for n in (2,3,4,5,6):
    name=f'pi{n+1}_{n}.json'
    a=json.loads((before/name).read_text(encoding='utf-8'))
    b=json.loads((after/name).read_text(encoding='utf-8'))
    assert a['status']==b['status']=='complete',(name,'status')
    for key in ('conclusion','open_goals','steps','web_key','web_mode'):
        assert a[key]==b[key],(name,key)
    # Only standalone internal-rule display lines may disappear, without changing any other visible characters.
    for key in ('web_lines','markdown'):
        x=a[key];y=b[key]
        if isinstance(x,list):
            # Web rows are presentation objects; disallow changes other than the precise internal-rule-only row.
            expected=[v for v in x if v.strip()!=target]
            if y != expected and y!=[('' if v.strip()==target else v) for v in x]:
                raise AssertionError(f'{name} {key} changed beyond permitted rule suppression: {list(difflib.unified_diff(x,y))[:30]}')
        else:
            expected='\n'.join(line for line in x.split('\n') if line.strip()!=target)
            if y != expected and y!=x.replace(target,''):
                raise AssertionError(f'{name} {key} unexpected text change: {list(difflib.unified_diff(x.splitlines(),y.splitlines()))[:30]}')
    if n==3:
        assert target in '\n'.join(a['web_lines'])+'\n'+a['markdown']
        assert target not in '\n'.join(b['web_lines'])+'\n'+b['markdown']
    print('PASS',name,'only intended internal label suppression')
print('PASS: 1-stem baselines preserved except exact internal rule label')
