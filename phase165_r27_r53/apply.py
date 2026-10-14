"""R27-R53: defer old calculation imports without altering legacy API signatures."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
OLD_IMPORTS = {
 'proof_repository', 'phase164_r7_repository_root_resolution',
 'standard_production_repository', 'toda_calculation_report',
 'toda_calculation_report_result',
}
IMPORTS = '''from __future__ import annotations
from typing import TYPE_CHECKING
from toda_group_query import TodaGroupQuery

if TYPE_CHECKING:
    from proof_repository import ProofRepository
    from toda_calculation_report_result import TodaCalculationReportResult
'''
LEGACY_FUNCTIONS = '''def build_toda_report(repository: ProofRepository, n: int, k: int) -> TodaCalculationReportResult:
    from toda_calculation_report import build_toda_calculation_report_result
    query = TodaGroupQuery(n=n, k=k)
    return build_toda_calculation_report_result(repository, query)


def build_standard_toda_report(n: int, k: int) -> TodaCalculationReportResult:
    from phase164_r7_repository_root_resolution import validate_repository_internal_proof_roots
    from standard_production_repository import build_standard_production_proof_repository
    repository = build_standard_production_proof_repository()
    validate_repository_internal_proof_roots(repository)
    return build_toda_report(repository, n=n, k=k)
'''


def transform(source: str) -> tuple[str, bool]:
    tree = ast.parse(source)
    funcs = {node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
    required = ('build_toda_report','build_standard_toda_report','build_toda_partial_result','build_standard_toda_partial_result')
    if any(name not in funcs for name in required):
        raise RuntimeError('R52 typed and legacy facade APIs must exist')
    if not any(isinstance(n,ast.ImportFrom) and n.module=='toda_group_query' for n in tree.body):
        raise RuntimeError('missing group query import')
    # Reject nonstandard legacy implementations instead of erasing their behavior.
    for name in required[:2]:
        node=funcs[name]
        calls={n.func.id for n in ast.walk(node) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
        if name == 'build_toda_report' and 'build_toda_calculation_report_result' not in calls:
            raise RuntimeError('unexpected build_toda_report implementation')
        if name == 'build_standard_toda_report' and 'build_toda_report' not in calls:
            raise RuntimeError('unexpected build_standard_toda_report implementation')
    if any(isinstance(node,ast.ImportFrom) and node.module in OLD_IMPORTS for node in tree.body):
        old = [node for node in tree.body if isinstance(node,ast.ImportFrom) and node.module in OLD_IMPORTS]
    else:
        # Idempotent when the module was already migrated.
        if any(isinstance(n,ast.ImportFrom) and n.module=='__future__' for n in tree.body) and any(isinstance(n,ast.If) and isinstance(n.test,ast.Name) and n.test.id=='TYPE_CHECKING' for n in tree.body):
            return source,False
        raise RuntimeError('unrecognized import state')
    permitted={'ProofRepository','validate_repository_internal_proof_roots','build_standard_production_proof_repository','build_toda_calculation_report_result','TodaCalculationReportResult'}
    if any(alias.asname or alias.name not in permitted for node in old for alias in node.names):
        raise RuntimeError('unexpected legacy facade import; refusing deletion')
    lines=source.splitlines(keepends=True)
    replacements=[]
    for node in old:
        replacements.append((node.lineno-1,node.end_lineno,''))
    for name in required[:2]:
        node=funcs[name]
        new=next(n for n in ast.parse(LEGACY_FUNCTIONS).body if isinstance(n,ast.FunctionDef) and n.name==name)
        # Keep API contract (name, args, annotations); only substitute old implementation with function-local imports.
        if len(node.args.args)!=len(new.args.args) or [a.arg for a in node.args.args]!=[a.arg for a in new.args.args]:
            raise RuntimeError(f'unsupported API signature: {name}')
        code=ast.get_source_segment(LEGACY_FUNCTIONS,new)
        replacements.append((node.lineno-1,node.end_lineno,code+'\n\n'))
    # Replace original group-query import as well, using a complete import section.
    for node in tree.body:
        if isinstance(node,ast.ImportFrom) and node.module=='toda_group_query':
            if [(a.name,a.asname) for a in node.names] != [('TodaGroupQuery',None)]:
                raise RuntimeError('unexpected group query import')
            replacements.append((node.lineno-1,node.end_lineno,''))
    for node in tree.body:
        if isinstance(node,ast.ImportFrom) and node.module=='__future__':
            raise RuntimeError('unexpected __future__ import; refusing automatic insertion')
    for a,b,t in sorted(replacements,reverse=True):
        lines[a:b]=[t]
    result=IMPORTS+'\n'+''.join(lines).lstrip('\r\n')
    ast.parse(result)
    if any(isinstance(n,ast.ImportFrom) and n.module in OLD_IMPORTS for n in ast.parse(result).body):
        raise RuntimeError('legacy imports remain at module level')
    return result,True


def apply(root:Path=ROOT)->dict:
    path=root/'toda_calculation_facade.py'
    if not path.is_file(): raise FileNotFoundError(path)
    if not (root/'toda_typed_group_facade.py').is_file(): raise RuntimeError('R52 independent typed facade required')
    original=path.read_text(encoding='utf-8-sig')
    updated,changed=transform(original)
    if changed:
        backup=root/'phase165_r27_r53_backup'
        backup.mkdir(exist_ok=True)
        b=backup/path.name
        if b.exists() and b.read_bytes()!=path.read_bytes():
            raise RuntimeError('conflicting backup; refusing overwrite')
        if not b.exists(): shutil.copy2(path,b)
        path.write_text(updated,encoding='utf-8',newline='\n')
    result={'phase':'165 R27-R53','status':'CHANGED' if changed else 'ALREADY_INSTALLED',
            'modified_files':[path.name] if changed else [],
            'legacy_eager_imports_removed':True,'typed_api_preserved':True,
            'legacy_api_preserved':True,'old_repository_modules_deleted':[],
            'remaining_legacy_repository_modules':4,'full_pytest_run':False}
    (root/'phase165_r27_r53_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

if __name__=='__main__':
    print(json.dumps(apply(),indent=2,ensure_ascii=False))
