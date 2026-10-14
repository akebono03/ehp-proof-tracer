# R27 追加コード全文

## install.py

```python
"""Retire two pi3^2-specific inference factories without inventing new premises."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

NAMES = ('toda_pi3_2_define_eta2_inference_rule', 'toda_pi3_2_eta2_hopf_relation_inference_rule')
SOURCES = ('toda_rules.py', 'toda_upstream_bootstrap.py', 'probes/probe_phase49_capabilities.py', 'standard_production_applicability_catalog.py', 'toda_prop56_zero_bootstrap.py')

def _remove_lines(source, ranges):
    lines = source.splitlines(keepends=True)
    for a,b in sorted(ranges,reverse=True):
        del lines[a:b]
    result = ''.join(lines)
    ast.parse(result)
    return result

def transform(source: str, path: str) -> tuple[str,int]:
    tree = ast.parse(source)
    edits=[]
    lines=source.splitlines(keepends=True)
    if path=='toda_rules.py':
        for name in NAMES:
            nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name]
            if len(nodes)!=1:raise RuntimeError(f'{path}: expected exactly one {name} definition, got {len(nodes)}')
            n=nodes[0]; edits.append((n.lineno-1,n.end_lineno))
    elif path in ('toda_upstream_bootstrap.py','probes/probe_phase49_capabilities.py'):
        for name in NAMES:
            imports=[n for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and any(a.name==name for a in n.names)]
            calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==name]
            if len(imports)!=1 or len(calls)!=1:raise RuntimeError(f'{path} {name}: import/call count not 1/1')
            for n,value in [(imports[0],name+','),(calls[0],name+'(),')]:
                hits=[i for i in range(n.lineno-1,n.end_lineno) if lines[i].strip()==value]
                if len(hits)!=1:raise RuntimeError(f'{path} {name}: not standalone {value}')
                edits.append((hits[0],hits[0]+1))
    elif path=='standard_production_applicability_catalog.py':
        for name in NAMES:
            candidates=[n for n in ast.walk(tree) if isinstance(n,ast.Constant) and n.value==name]
            if len(candidates)!=1:raise RuntimeError(f'{path} {name}: expected one metadata key; found {len(candidates)}')
            key=candidates[0]
            enclosing=[n for n in ast.walk(tree) if isinstance(n,ast.Dict) and key in n.keys]
            if len(enclosing)!=1:raise RuntimeError('Unexpected catalog dictionary structure')
            d=enclosing[0]; index=d.keys.index(key)
            val=d.values[index]
            if not isinstance(val,ast.Attribute) and not isinstance(val,ast.Tuple):
                raise RuntimeError('Unexpected catalog value shape')
            a=key.lineno-1;b=val.end_lineno
            if b < len(lines) and lines[b].strip()=='),':
                b+=1
            elif not lines[b-1].strip().endswith('),'):
                raise RuntimeError('Catalog metadata value is not standalone')
            if not lines[a].strip().startswith('"'+name+'"') and not lines[a].strip().startswith("'"+name+"'"):
                raise RuntimeError('Catalog metadata key is not standalone')
            edits.append((a,b))
    elif path=='toda_prop56_zero_bootstrap.py':
        # R26-R1 already switched pi3^2 to typed common search. The Hopf relation
        # is independently present as an existing GIVEN source in Phase50.
        funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_build_prop51_step']
        if len(funcs)!=1:raise RuntimeError('Missing _build_prop51_step')
        f=funcs[0]
        section=''.join(lines[f.lineno-1:f.end_lineno])
        marker='  eta2_hopf_step = _find_unique_step(\n'
        next_marker='  delta_step = _find_unique_step(\n'
        if section.count(marker)!=1 or section.count(next_marker)!=1:raise RuntimeError('Unexpected Hopf step lookup')
        a=section.index(marker);b=section.index(next_marker,a)
        old=section[a:b]
        if 'phase49[' not in old or 'MapApplication' not in old:raise RuntimeError('Unexpected old Hopf source')
        new=old.replace('phase49[\n      "result"\n    ].steps,','phase50[\n      "premise_steps"\n    ],',1)
        if new==old:raise RuntimeError('Hopf source replacement did not apply')
        newsection=section[:a]+new+section[b:]
        candidate=''.join(lines[:f.lineno-1])+newsection+''.join(lines[f.end_lineno:])
        ast.parse(candidate)
        return candidate,1
    result=_remove_lines(source,edits)
    for name in NAMES:
        if name in result:raise RuntimeError(f'{path}: still refers to {name}')
    return result,len(edits)

def install(root:Path)->dict:
    root=root.resolve(); planned={}
    for path in SOURCES:
        file=root/path
        if not file.is_file():raise FileNotFoundError(file)
        original=file.read_text(encoding='utf-8')
        if path=='toda_prop56_zero_bootstrap.py':
            if 'phase50[\n      "premise_steps"\n    ],' in original:
                result,count=original,0
            else:result,count=transform(original,path)
        elif not any(name in original for name in NAMES):result,count=original,0
        else:result,count=transform(original,path)
        planned[path]=(original,result,count)
    counts={path:planned[path][2] for path in SOURCES}
    if counts not in ({'toda_rules.py':2,'toda_upstream_bootstrap.py':4,'probes/probe_phase49_capabilities.py':4,'standard_production_applicability_catalog.py':2,'toda_prop56_zero_bootstrap.py':1},dict.fromkeys(SOURCES,0)):
        raise RuntimeError(f'Inconsistent source state; aborting: {counts}')
    if any(counts.values()):
        for path,(old,new,n) in planned.items():
            if old!=new:
                target=root/path
                backup=target.with_name(target.name+'.phase165_r52_r27_backup')
                if backup.exists():raise RuntimeError(f'Backup exists: {backup}')
        for path,(old,new,n) in planned.items():
            if old!=new:
                target=root/path
                shutil.copy2(target,target.with_name(target.name+'.phase165_r52_r27_backup'))
                target.write_text(new,encoding='utf-8',newline='')
    out=Path(__file__).parent/'audit_output';out.mkdir(exist_ok=True)
    report={'phase':'165 R52-R27','status':'REMOVED' if any(counts.values()) else 'ALREADY_REMOVED','edits':counts,'full_pytest_run':False}
    (out/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if any(counts.values()):
        f=ast.parse(planned['toda_prop56_zero_bootstrap.py'][1]);fn=next(n for n in f.body if isinstance(n,ast.FunctionDef) and n.name=='_build_prop51_step')
        lines=planned['toda_prop56_zero_bootstrap.py'][1].splitlines(keepends=True)
        (out/'MODIFIED_FUNCTION.md').write_text('# _build_prop51_step (complete)\n\n```python\n'+''.join(lines[fn.lineno-1:fn.end_lineno])+'\n```\n',encoding='utf-8')
    return report

if __name__=='__main__':print(json.dumps(install(Path(__file__).resolve().parent.parent),ensure_ascii=False,indent=2))

```

## test_retirement.py

```python
from pathlib import Path
import ast
from install import NAMES

ROOT=Path(__file__).resolve().parent.parent

def test_specialized_factories_removed():
    tree=ast.parse((ROOT/'toda_rules.py').read_text(encoding='utf-8'))
    assert all(n.name not in NAMES for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)))

def test_legacy_consumers_and_catalog_cleared():
    for relative in ('toda_upstream_bootstrap.py','probes/probe_phase49_capabilities.py','standard_production_applicability_catalog.py'):
        source=(ROOT/relative).read_text(encoding='utf-8')
        ast.parse(source)
        assert all(name not in source for name in NAMES),relative

def test_phase50_existing_hopf_source_selected():
    text=(ROOT/'toda_prop56_zero_bootstrap.py').read_text(encoding='utf-8')
    f=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='_build_prop51_step')
    seg=''.join(text.splitlines(keepends=True)[f.lineno-1:f.end_lineno])
    part=seg.split('  eta2_hopf_step = _find_unique_step(',1)[1].split('  delta_step = _find_unique_step(',1)[0]
    assert 'phase50[' in part and '"premise_steps"' in part
    assert 'phase49[' not in part

```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$package = $PSScriptRoot
$root = Split-Path -Parent $package
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$env:PYTHONPATH = "$package;$root" + $(if ($env:PYTHONPATH) { ";$env:PYTHONPATH" } else { '' })
python -m pytest -q (Join-Path $package 'test_retirement.py') (Join-Path $root 'test_phase165_r52_r9_shared_math.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27 targeted tests passed; full pytest NOT run.'

```
