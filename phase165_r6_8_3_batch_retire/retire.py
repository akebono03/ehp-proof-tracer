"""Conservative batch retirement of unused historical modules; no adapter."""
from __future__ import annotations
import argparse
import ast
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

CANDIDATES = (
    'probes/probe_phase53_capabilities.py',
    'probes/probe_phase54_capabilities.py',
    'probes/probe_phase55_capabilities.py',
    'probes/probe_phase57_capabilities.py',
    'phase162_ehp_leaf_inputs.py',
    'phase162_pi5_3_web_replay.py',
    'tests/test_phase59_n3_ehp_chain.py',
    'tests/test_phase55_prop51_phase52_phase54_dependency.py',
)
SKIP_DIRS = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', 'node_modules'}

def module(path: str) -> str:
    return path.removesuffix('.py').replace('/', '.')

def consumers(root: Path, candidates=CANDIDATES):
    targets = {module(p): p for p in candidates}
    edges = {p: set() for p in candidates}
    errors = []
    for path in sorted(root.rglob('*.py')):
        rel = path.relative_to(root).as_posix()
        if set(path.relative_to(root).parts) & SKIP_DIRS:
            continue
        # Archived installation packages are not live imports; root-level and
        # active probes/tests matter. Other directories are reported separately.
        if len(path.relative_to(root).parts) > 2:
            continue
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=rel)
        except (OSError, UnicodeError, SyntaxError) as exc:
            errors.append(f'{rel}: {exc}')
            continue
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [x.name for x in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    names = [node.module]
                    names += [node.module + '.' + x.name for x in node.names]
                elif node.level == 0:
                    names = [x.name for x in node.names]
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == '__import__':
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    names = [node.args[0].value]
            for name in names:
                for imported, target in targets.items():
                    if name == imported or name.startswith(imported + '.'):
                        edges[target].add(f'{rel}:{node.lineno}')
    return edges, errors

def plan(root: Path):
    missing = [p for p in CANDIDATES if not (root / p).is_file()]
    edges, errors = consumers(root)
    active = set(CANDIDATES) - set(missing)
    # Eliminate only a module with zero consumers among BOTH existing modules
    # and modules already selected for retirement; uses a maximal fixed point.
    retired = set()
    while True:
        newly = {
            p for p in active - retired
            if all(location.split(':')[0] in retired for location in edges[p])
        }
        if not newly:
            break
        retired |= newly
    # A deletion candidate that imports another candidate is safe ONLY if all
    # modules that import it are also deleted (already required above).
    if errors:
        retired.clear()
    return {'phase':'165 R6-8(3)', 'retirable':sorted(retired),
            'blocked':{p:sorted(edges[p]) for p in sorted(active-retired)},
            'missing':missing,'parse_errors':errors,'full_pytest_run':False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    root=args.root.resolve()
    info=plan(root)
    info['action']='preview'
    if args.apply and info['retirable']:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        backup=root / f'phase165_r6_8_3_backup_{stamp}.zip'
        with ZipFile(backup,'w',ZIP_DEFLATED) as z:
            for rel in info['retirable']:
                z.write(root/rel,rel)
        with ZipFile(backup) as z:
            if set(z.namelist()) != set(info['retirable']):
                raise RuntimeError('Backup verification failed')
        for rel in info['retirable']:
            (root/rel).unlink()
        info['action']='removed_safe_subset'
        info['backup']=backup.name
    elif args.apply:
        info['action']='no_safe_removals'
    report=root / 'phase165_r6_8_3_batch_retire_report.json'
    report.write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(info,ensure_ascii=False,indent=2))
    print('Report:',report)
    print('Full pytest NOT run.')
    return 0
if __name__=='__main__':
    raise SystemExit(main())
