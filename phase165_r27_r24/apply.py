from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_calculation_facade.py'
BACKUP = Path(__file__).resolve().parent / 'toda_calculation_facade.before_r24.py'

REPLACEMENT = '''def build_standard_toda_report(
  n: int,
  k: int,
) -> TodaCalculationReportResult:
  """Retired legacy standard entry; use the common typed search instead."""
  raise RuntimeError(
    "Legacy standard calculation is retired in Phase 165 R27-R24; "
    "use search_group_structure_automatically(n=n, k=k) "
    "and inspect COMPLETE, PARTIAL, or SEARCH_FAILED."
  )
'''

def transform(source: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'build_standard_toda_report']
    if len(functions) != 1:
        raise RuntimeError('Expected exactly one legacy standard calculation function; no changes made')
    fn = functions[0]
    body = ast.get_source_segment(source, fn) or ''
    if 'Legacy standard calculation is retired in Phase 165 R27-R24' in body:
        return source
    if not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'build_standard_production_proof_repository' for n in ast.walk(fn)):
        raise RuntimeError('Unexpected standard calculation implementation; no changes made')
    blocks=[]
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module in {'standard_production_repository','phase164_r7_repository_root_resolution'}:
            blocks.append((node.lineno,node.end_lineno,''))
    blocks.append((fn.lineno,fn.end_lineno,REPLACEMENT))
    for start,end,replacement in sorted(blocks,reverse=True):
        lines[start-1:end]=[replacement]
    result=''.join(lines)
    ast.parse(result)
    if 'def build_toda_report(' not in result:
        raise RuntimeError('Explicit repository entry disappeared; no changes made')
    return result

def apply() -> None:
    old=TARGET.read_text(encoding='utf-8-sig')
    new=transform(old)
    if new==old:
        print('R27-R24 already installed')
        return
    if not BACKUP.exists():
        shutil.copy2(TARGET,BACKUP)
    TARGET.write_text(new,encoding='utf-8')
    print('R27-R24 installed: legacy standard calculation builder removed; explicit repository API preserved')

if __name__=='__main__':
    apply()
