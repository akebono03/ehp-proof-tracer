"""Read-only AST dependency audit of failed pytest collection tests."""
import argparse
import ast
import collections
import json
from pathlib import Path

TARGET = 'toda_pi4_3_delta_image_free_cyclic_inference_rule'

def imports_for(path):
    try:
        tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    except (OSError, SyntaxError, UnicodeError) as exc:
        return [], str(exc)
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                names.append(node.module)
        elif isinstance(node, ast.Import):
            names.extend(x.name for x in node.names)
    return sorted(set(names)), None

def analyze(root, triage):
    root = Path(root).resolve()
    records = json.loads(Path(triage).read_text(encoding='utf-8'))['records']
    failed = [r for r in records if r['detail'].find(TARGET) >= 0]
    paths = {}
    for folder in (root / 'tests', root / 'probes'):
        if folder.is_dir():
            for path in folder.rglob('*.py'):
                if any(p in {'__pycache__', 'archive', 'backup'} for p in path.parts):
                    continue
                name = path.relative_to(root).with_suffix('').as_posix().replace('/', '.')
                paths[name] = path
                if name.startswith('tests.test_'):
                    paths.setdefault(name.rsplit('.', 1)[-1], path)
    for path in root.glob('*.py'):
        paths[path.stem] = path
    edges = {}; errors = {}
    for module, path in paths.items():
        deps, err = imports_for(path)
        edges[module] = [x for x in deps if x in paths]
        if err:
            errors[module] = err
    culprit = 'probes.probe_phase50_capabilities'
    results = []
    for record in failed:
        test_name = Path(record['test_path']).stem
        q = collections.deque([(test_name, [test_name])]); visited = {test_name}; chain = None
        while q:
            node, route = q.popleft()
            if node == culprit:
                chain = route
                break
            for dependency in edges.get(node, []):
                if dependency not in visited:
                    visited.add(dependency)
                    q.append((dependency, route + [dependency]))
        results.append({'test_path':record['test_path'], 'path_to_legacy_probe':chain,
                        'classification':'PROVEN_STATIC_CHAIN' if chain else 'UNRESOLVED_STATIC_CHAIN'})
    counts = dict(collections.Counter(x['classification'] for x in results))
    return {'status':'READ_ONLY_STATIC_AUDIT', 'target':TARGET,
            'root_cause_candidate':culprit, 'failed_test_count':len(failed),
            'classification_counts':counts, 'test_dependencies':results,
            'ast_read_errors':errors,
            'limitations':['Static AST imports do not prove runtime execution.',
                           'A missing path does not establish that a test is obsolete.',
                           'No files were edited or excluded and pytest was not rerun.']}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--triage', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    output = analyze(args.root, args.triage)
    dest = Path(args.out); dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Failed tests:', output['failed_test_count'])
    print('Static dependency classifications:', output['classification_counts'])
    print('Report:', dest)
    print('READ ONLY; no tests or production files changed.')

if __name__ == '__main__':
    main()
