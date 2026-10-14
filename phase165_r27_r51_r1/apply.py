"""Phase 165 R27-R51-R1: remove legacy group report from the Web Group Query entry."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

REPLACEMENT = '''def build_standard_web_group_query_view(n: int, k: int) -> WebGroupQueryView:
    """Report only proven group structures; never consult old TodaCalculation."""
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r5_auto_search import search_group_structure_automatically
    from toda_human_readable_renderer import render_toda_public_group_relation_latex

    query = TodaGroupQuery(n=n, k=k)
    domain = classify_toda_group_query_domain(query)
    if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
        return WebGroupQueryView(
            n=n, k=k, status=TodaCalculationStatus.FOUND,
            result_latex=render_toda_group_query_domain_latex(domain),
            proof_available=False,
        )

    result = search_group_structure_automatically(n=n, k=k)
    latex = None
    if result.status is ProofSearchStatus.COMPLETE and result.conclusion is not None:
        latex = render_toda_public_group_relation_latex(result.conclusion)
    if latex is None:
        return WebGroupQueryView(
            n=n, k=k, status=TodaCalculationStatus.NOT_FOUND,
            result_latex=None, proof_available=False,
        )
    return WebGroupQueryView(
        n=n, k=k, status=TodaCalculationStatus.FOUND,
        result_latex=latex, proof_available=True,
    )
'''

OLD_IMPORTS = {'build_standard_toda_report', 'render_toda_group_result_latex'}

def _function(tree, name):
    items=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==name]
    if len(items)!=1: raise RuntimeError(f'exactly one {name} required')
    return items[0]

def transform(source: str) -> tuple[str,bool]:
    tree=ast.parse(source)
    old=_function(tree,'build_standard_web_group_query_view')
    expected=_function(ast.parse(REPLACEMENT),'build_standard_web_group_query_view')
    imports=[n for n in tree.body if isinstance(n,ast.ImportFrom) and any(a.name in OLD_IMPORTS for a in n.names)]
    if any(any(a.name not in OLD_IMPORTS for a in n.names) for n in imports):
        raise RuntimeError('legacy imports are mixed with required imports')
    if len(imports)>2:
        raise RuntimeError('unexpected multiple legacy imports')
    # Fail closed on any use outside the one intended function/import.
    for node in tree.body:
        if node is old or node in imports: continue
        if any(isinstance(n,ast.Name) and n.id in OLD_IMPORTS for n in ast.walk(node)):
            raise RuntimeError('legacy names used outside Group Query entry')
    if ast.dump(old,include_attributes=False)==ast.dump(expected,include_attributes=False):
        if imports: raise RuntimeError('new entry with stale legacy imports')
        return source,False
    # Require the existing view API and old report call OR a known prior typed rewrite.
    if not any(isinstance(n,ast.ClassDef) and n.name=='WebGroupQueryView' for n in tree.body):
        raise RuntimeError('WebGroupQueryView missing')
    legacy_used=any(isinstance(n,ast.Name) and n.id=='build_standard_toda_report' for n in ast.walk(old))
    if not legacy_used:
        # Earlier phases may already route this entry through the typed prover.
        # Never replace an unknown pre-existing implementation merely because
        # it has the same function name.
        calls={n.func.id for n in ast.walk(old) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
        typed_entry=bool(calls.intersection({
            'search_group_structure_automatically',
            'build_standard_toda_partial_result',
            'build_toda_partial_result',
        }))
        if typed_entry and not imports:
            return source,False
        raise RuntimeError('unknown Group Query implementation; refusing overwrite')
    lines=source.splitlines(keepends=True)
    changes=[(old.lineno-1,old.end_lineno,REPLACEMENT+'\n')]
    for imp in imports: changes.append((imp.lineno-1,imp.end_lineno,''))
    for a,b,repl in sorted(changes,reverse=True): lines[a:b]=[repl]
    updated=''.join(lines)
    ast.parse(updated)
    return updated,True

def apply(root:Path)->dict:
    path=root/'web_group_query.py'
    if not path.is_file(): raise FileNotFoundError(path)
    old=path.read_text(encoding='utf-8-sig')
    new,changed=transform(old)
    if changed:
        backup=root/'phase165_r27_r51_r1_backup'; backup.mkdir(exist_ok=True)
        shutil.copy2(path,backup/path.name)
        path.write_text(new,encoding='utf-8',newline='\n')
    report={'phase':'165 R27-R51-R1','status':'CHANGED' if changed else 'ALREADY_INSTALLED',
      'modified_files':[path.name] if changed else [],
      'web_group_query_legacy_report_removed':True,
      'existing_typed_entry_preserved':not changed,
      'web_group_query_search':'search_group_structure_automatically' if changed else 'existing_typed_entry',
      'legacy_toda_calculation_api_unchanged':True,
      'remaining_legacy_repository_modules':4,
      'full_pytest_run':False}
    (root/'phase165_r27_r51_r1_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    print(json.dumps(apply(Path(__file__).resolve().parent.parent),ensure_ascii=False,indent=2))
