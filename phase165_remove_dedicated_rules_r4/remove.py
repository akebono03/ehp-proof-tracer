from __future__ import annotations
import ast
import json
import re
import shutil
import sys
from pathlib import Path

NAMES = (
    'toda_pi4_3_delta_image_free_cyclic_inference_rule',
    'toda_pi4_3_finite_cyclic_inference_rule',
    'toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule',
    'toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule',
    'toda_pi4_3_eta3_generator_inference_rule',
    'toda_45_pi4_3_finite_cyclic_transport_inference_rule',
)
NAMESET = set(NAMES)
ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
TESTS = ROOT / 'tests'
CATALOG = ROOT / 'standard_production_applicability_catalog.py'
SOURCE_CANDIDATES = [ROOT / 'toda_rules.py', ROOT / 'toda_rules' / '__init__.py', ROOT / 'toda_upstream_bootstrap.py']


def spans_for_functions(path: Path, *, tests: bool) -> tuple[list[tuple[int, int]], list[str]]:
    lines = path.read_text(encoding='utf-8-sig').splitlines(keepends=True)
    tree = ast.parse(''.join(lines), filename=str(path))
    spans = []
    found = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if (not tests and node.name in NAMESET) or (tests and node.name.startswith('test_') and any(isinstance(n, ast.Name) and n.id in NAMESET for n in ast.walk(node))):
                first = min([node.lineno] + [x.lineno for x in node.decorator_list])
                spans.append((first, node.end_lineno))
                found.append(node.name)
    return spans, found


def prune_test_imports(content: str) -> str:
    # Remove only dedicated names in multiline parenthesized imports; refuse other shapes.
    result = []
    for line in content.splitlines(keepends=True):
        if re.fullmatch(r'\s*(' + '|'.join(NAMES) + r')\s*,\s*\r?\n?', line):
            continue
        result.append(line)
    return ''.join(result)


def build() -> dict:
    if not CATALOG.exists() or not TESTS.is_dir():
        raise RuntimeError('Expected repository root with catalog and tests')
    updates: dict[Path, str] = {}
    source_found = set()
    # Source definitions: discover in root production files, not archived or installer snapshots.
    for path in ROOT.glob('*.py'):
        if path.name.startswith('phase'):
            continue
        original = path.read_text(encoding='utf-8-sig')
        try:
            spans, names = spans_for_functions(path, tests=False)
        except SyntaxError:
            continue
        source_found.update(names)
        if spans:
            ls = original.splitlines(keepends=True)
            for a, b in reversed(spans):
                del ls[a-1:b]
            updates[path] = ''.join(ls)
    # Dedicated functions may be in package submodules.
    package = ROOT / 'toda_rules'
    if package.is_dir():
        for path in package.glob('*.py'):
            original = path.read_text(encoding='utf-8-sig')
            spans, names = spans_for_functions(path, tests=False)
            source_found.update(names)
            if spans:
                ls = original.splitlines(keepends=True)
                for a,b in reversed(spans):
                    del ls[a-1:b]
                updates[path] = ''.join(ls)
    cat = CATALOG.read_text(encoding='utf-8-sig')
    cat_lines = cat.splitlines(keepends=True)
    pattern = re.compile(r'^\s*[\'\"](' + '|'.join(NAMES) + r')[\'\"]\s*:\s*\(\s*$')
    cat_count = 0
    i = 0
    while i < len(cat_lines):
        if pattern.match(cat_lines[i]):
            j = i + 1
            while j < len(cat_lines) and not re.match(r'^\s*\),?\s*$', cat_lines[j]):
                j += 1
            if j == len(cat_lines) or j - i > 5:
                raise RuntimeError('Unexpected catalog entry shape')
            del cat_lines[i:j+1]
            cat_count += 1
        else:
            i += 1
    if cat_count:
        updates[CATALOG] = ''.join(cat_lines)
    removed_tests = {}
    for path in TESTS.glob('test_*.py'):
        raw = path.read_text(encoding='utf-8-sig')
        if not any(x in raw for x in NAMES):
            continue
        spans, names = spans_for_functions(path, tests=True)
        if not spans:
            continue
        ls = raw.splitlines(keepends=True)
        for a,b in reversed(spans):
            del ls[a-1:b]
        pruned = prune_test_imports(''.join(ls))
        ast.parse(pruned, filename=str(path))
        if any(isinstance(n, ast.Name) and n.id in NAMESET for n in ast.walk(ast.parse(pruned))):
            raise RuntimeError(f'Unremoved test-time use: {path}')
        updates[path] = pruned
        removed_tests[str(path.relative_to(ROOT))] = names
    # No remaining references in root production modules (old snapshots, audit runners excluded).
    for path in ROOT.glob('*.py'):
        if path.name.startswith(('test_', 'probe_')):
            continue
        content = updates.get(path)
        if content is None:
            content = path.read_text(encoding='utf-8-sig')
        if path == CATALOG:
            continue
        try:
            tree = ast.parse(content, filename=str(path))
        except SyntaxError:
            continue
        used = sorted({n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id in NAMESET})
        if used:
            raise RuntimeError(f'Live references remain in {path.name}: {used}; no files changed')
    for p, s in updates.items():
        ast.parse(s, filename=str(p))
    # Write only after all validation. Backups in one explicit local folder.
    backup = HERE / 'backups'
    backup.mkdir(exist_ok=True)
    for p, s in updates.items():
        dest = backup / p.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            shutil.copy2(p, dest)
        p.write_text(s, encoding='utf-8')
    return {'status': 'REMOVED' if updates else 'ALREADY_ABSENT', 'source_definitions_removed': sorted(source_found), 'catalog_entries_removed': cat_count, 'test_functions_removed': removed_tests, 'modified_files': sorted(str(p.relative_to(ROOT)) for p in updates), 'full_pytest_run': False}


if __name__ == '__main__':
    try:
        report = build()
    except Exception as exc:
        report = {'status': 'BLOCKED', 'error': str(exc), 'full_pytest_run': False}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(1)
    path = HERE / 'audit_result.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(path.read_text(encoding='utf-8'))
