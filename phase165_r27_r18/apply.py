import ast
from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / 'web_app.py'
OLD = ('generator_proof','generator_proof_scope','generator_applicability','generator_execution')
IMPORTS = ('web_generator_applicability','web_generator_execution','web_generator_proof','web_generator_proof_scope')

def patch(source: str) -> str:
    tree = ast.parse(source)
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'create_app'), None)
    if fn is None:
        raise RuntimeError('create_app not found')
    lines = source.splitlines(keepends=True)
    replacements = []
    for n in ast.walk(fn):
        if not isinstance(n, ast.If):
            continue
        t=n.test
        if not (isinstance(t, ast.Compare) and isinstance(t.left, ast.Name) and t.left.id=='form_kind' and len(t.comparators)==1 and isinstance(t.comparators[0],ast.Constant) and t.comparators[0].value in OLD):
            continue
        # preserve branch, replace its entire body with explicit disabled condition
        start=n.body[0].lineno-1; end=n.body[-1].end_lineno
        indent=' '*(n.body[0].col_offset)
        replacements.append((start,end,[indent+"raise ValueError('Legacy generator workflow is disabled; use the unified group proof search')\n"]))
    if len(replacements)!=4:
        raise RuntimeError(f'expected four legacy route branches, got {len(replacements)}')
    for a,b,v in sorted(replacements,reverse=True):
        lines[a:b]=v
    updated=''.join(lines)
    # Remove disabled entry imports and drop only corresponding view type annotations
    for name in IMPORTS:
        updated_tree=ast.parse(updated)
        matches=[n for n in updated_tree.body if isinstance(n, ast.ImportFrom) and n.module==name]
        if len(matches)!=1: raise RuntimeError(f'expected import {name}')
        item=matches[0]
        ll=updated.splitlines(keepends=True)
        ll[item.lineno-1:item.end_lineno]=[]
        updated=''.join(ll)
    # Remove annotations for corresponding disabled view variables (do not touch template kwargs)
    updated_tree=ast.parse(updated)
    fn=next(n for n in updated_tree.body if isinstance(n,ast.FunctionDef) and n.name=='create_app')
    expected={'generator_proof_view','generator_execution_view','generator_proof_scope_view','generator_applicability_view'}
    spans=[]
    for n in ast.walk(fn):
        if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name) and n.target.id in expected:
            spans.append((n.lineno-1,n.end_lineno))
    if len(spans)!=4: raise RuntimeError(f'expected four view annotations, got {len(spans)}')
    ll=updated.splitlines(keepends=True)
    for a,b in sorted(spans,reverse=True):ll[a:b]=[]
    updated=''.join(ll)
    # still pass None placeholders for template variables to preserve template contracts
    updated_tree=ast.parse(updated)
    fn=next(n for n in updated_tree.body if isinstance(n,ast.FunctionDef) and n.name=='create_app')
    kw_names={'generator_proof_view','generator_execution_view','generator_proof_scope_view','generator_applicability_view'}
    lines=updated.splitlines(keepends=True)
    repairs=[]
    for n in ast.walk(fn):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='render_template':
            for k in n.keywords:
                if k.arg in kw_names:
                    repairs.append((k.value.lineno-1,k.value.col_offset,k.value.end_lineno-1,k.value.end_col_offset))
    if len(repairs)!=4:raise RuntimeError(f'expected four template placeholders, got {len(repairs)}')
    for al,ac,bl,bc in sorted(repairs, reverse=True):
        if al==bl:lines[al]=lines[al][:ac]+'None'+lines[al][bc:]
        else:
            lines[al:bl+1]=[lines[al][:ac]+'None'+lines[bl][bc:]]
    updated=''.join(lines)
    ast.parse(updated)
    for forbidden in ('build_standard_web_generator_proof_view','build_standard_web_generator_proof_scope_view','build_standard_web_generator_applicability_view','build_standard_web_generator_execution_view'):
        if forbidden in updated:raise RuntimeError('legacy call remains: '+forbidden)
    return updated

def main():
    if not TARGET.exists():raise SystemExit('Missing web_app.py')
    src=TARGET.read_text(encoding='utf-8-sig')
    if 'Legacy generator workflow is disabled; use the unified group proof search' in src:
        print('R27-R18 already installed');return
    result=patch(src)
    backup=ROOT/'phase165_r27_r18'/'web_app.before_r27_r18.py'
    backup.write_text(src,encoding='utf-8')
    TARGET.write_text(result,encoding='utf-8')
    print('R27-R18 installed: four hidden legacy generator POST paths disabled')
if __name__=='__main__':main()
