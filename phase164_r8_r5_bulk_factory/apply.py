"""Guarded Phase 164 R8-R5 bulk migration, executed in the project root."""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / 'r8_r4_audit.json').read_text(encoding='utf-8'))
FACTORY = 'phase164_r8_proofstep_factory.py'
BASELINE = (HERE / 'factory_baseline.py').read_bytes()
ADDITIONS = (HERE / 'phase164_r8_factory_additions.py').read_text(encoding='utf-8')
TARGET_CATEGORIES = {
    'given_source_boundary_review': ('ProofStep', 'create_legacy_given_proof_step'),
    'inference_constructor_provenance_review': ('ProofStep', 'create_legacy_specialization_proof_step'),
    'inference_factory_migrate': ('apply_inference_match', 'derive_inference_proof_step'),
}
NAME_TO_CATEGORY = {v[1]: k for k, v in TARGET_CATEGORIES.items()}
FACTORY_INTERNAL_EXCLUDES = {FACTORY, 'proof.py'}


def digest(value):
    return hashlib.sha256(value).hexdigest()


def call_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def rule_of(call):
    for keyword in call.keywords:
        if keyword.arg == 'rule':
            return call_name(keyword.value)
    return None


def source_sites(root, relative_path):
    data = (root / relative_path).read_bytes()
    encoding = 'utf-8-sig' if data.startswith(b'\xef\xbb\xbf') else 'utf-8'
    source = data.decode(encoding)
    tree = ast.parse(source, filename=relative_path)
    result = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = call_name(node.func)
        if name == 'ProofStep':
            rule = rule_of(node)
            category = ('given_source_boundary_review' if rule == 'GIVEN'
                        else 'inference_constructor_provenance_review' if rule == 'INFERENCE'
                        else None)
        elif name == 'apply_inference_match':
            category = 'inference_factory_migrate'
        else:
            continue
        if category is None:
            continue
        result.append((node, category))
    return data, source, tree, result


def expected_sites():
    by_file = defaultdict(list)
    for site in AUDIT['sites']:
        category = site['category']
        if category not in TARGET_CATEGORIES:
            continue
        if site['file'] in FACTORY_INTERNAL_EXCLUDES:
            continue
        by_file[site['file']].append(site)
    return dict(by_file)


def byte_replacement(source, sites):
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    edits = []
    names = set()
    for node, category in sites:
        old_name, new_name = TARGET_CATEGORIES[category]
        fn = node.func
        if not isinstance(fn, ast.Name):
            raise ValueError(f'qualified call needs manual review: line {node.lineno}')
        if node.args or any(keyword.arg is None for keyword in node.keywords):
            if category != 'inference_factory_migrate':
                raise ValueError(f'constructor non-keyword args need review: line {node.lineno}')
        start = offsets[fn.lineno - 1] + fn.col_offset
        end = offsets[fn.end_lineno - 1] + fn.end_col_offset
        if source[start:end] != old_name:
            raise ValueError(f'call token mismatch at line {node.lineno}')
        edits.append((start, end, new_name))
        names.add(new_name)
    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]
    return source, names


def add_imports(source, symbols):
    import_line = 'from phase164_r8_proofstep_factory import (\n'
    import_line += ''.join('    ' + name + ',\n' for name in sorted(symbols))
    import_line += ')\n'
    tree = ast.parse(source)
    # Insert after the initial continuous import section (and after any future import).
    first_import = next((i for i, n in enumerate(tree.body)
                         if isinstance(n, (ast.Import, ast.ImportFrom))), None)
    if first_import is None:
        raise ValueError('no import section')
    last = tree.body[first_import]
    for node in tree.body[first_import + 1:]:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last = node
        else:
            break
    parts = source.splitlines(keepends=True)
    parts.insert(last.end_lineno, '\n' + import_line)
    result = ''.join(parts)
    ast.parse(result)
    return result


def changed_code(source, relative_path, symbols):
    tree = ast.parse(source)
    lines = source.splitlines()
    imports = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append('\n'.join(lines[node.lineno - 1:node.end_lineno]))

    # For class modifications print the entire class, not only its member.
    # For other changes print the entire affected top-level function.
    blocks = []
    for node in tree.body:
        if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        found = False
        for descendant in ast.walk(node):
            if isinstance(descendant, ast.Call) and call_name(descendant.func) in symbols:
                found = True
                break
        if found:
            blocks.append('\n'.join(lines[node.lineno - 1:node.end_lineno]))
    if not blocks:
        raise ValueError(f'could not locate changed class/function in {relative_path}')
    return ('\n## ' + relative_path + '\n\n### 変更後の import 全文\n\n```python\n'
            + '\n'.join(imports) + '\n```\n\n### 変更クラス・関数全文\n\n'
            + '\n\n'.join('```python\n' + c + '\n```' for c in blocks) + '\n')


def migrate(root: Path, *, dry_run=False):
    root = Path(root)
    expected = expected_sites()
    prepared = {}
    actual_counts = Counter()
    for relative, sites in sorted(expected.items()):
        data, source, tree, calls = source_sites(root, relative)
        exp_counts = Counter(s['category'] for s in sites)
        got_counts = Counter(category for node, category in calls)
        if got_counts != exp_counts:
            raise ValueError(f'PRECHECK FAILED {relative}: expected {dict(exp_counts)}; actual {dict(got_counts)}')
        changed, symbols = byte_replacement(source, calls)
        if not symbols:
            raise ValueError(f'empty symbols for {relative}')
        changed = add_imports(changed, symbols)
        prepared[relative] = (data, changed.encode('utf-8'), symbols, changed)
        actual_counts.update(got_counts)
    factory = root / FACTORY
    if not factory.is_file():
        raise ValueError('R8-R2 factory not installed')
    original_factory = factory.read_bytes()
    if digest(original_factory) != digest(BASELINE):
        raise ValueError('R8-R2 factory differs from verified baseline; no changes applied')
    enhanced_factory = original_factory + b'\n' + ADDITIONS.encode('utf-8')
    ast.parse(enhanced_factory.decode('utf-8'))
    for relative, (before, after, _, _) in prepared.items():
        if after == before:
            raise ValueError(f'no-op candidate: {relative}')
    if dry_run:
        return {'files': len(prepared), 'counts': dict(actual_counts), 'dry_run': True}
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = root / f'phase164_r8_r5_backup_{stamp}'
    backup_dir.mkdir(exist_ok=False)
    all_files = {FACTORY: (original_factory, enhanced_factory, set(), enhanced_factory.decode('utf-8'))}
    all_files.update(prepared)
    for relative, (before, after, symbols, new_source) in all_files.items():
        backup = backup_dir / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(before)
    changed_written = []
    try:
        for relative, (before, after, symbols, source) in all_files.items():
            path = root / relative
            if path.read_bytes() != before:
                raise RuntimeError(f'file changed after precheck: {relative}')
            path.write_bytes(after)
            changed_written.append(relative)
    except Exception:
        for relative in changed_written:
            (root / relative).write_bytes((backup_dir / relative).read_bytes())
        raise
    output = root / 'phase164_r8_r5_output'
    output.mkdir(exist_ok=True)
    report = {'status': 'MIGRATED_LEGACY_STATUS_PRESERVED',
              'files_modified': len(all_files), 'site_counts': dict(actual_counts),
              'backup_dir': str(backup_dir), 'full_pytest_run': False,
              'unresolved_categories': {'dataclass_replace_type_review': 66,
                                        'core_engine_keep_or_internal_refactor': 10,
                                        'other_constructor_review': 1},
              'limitation': 'Legacy GIVEN / INFERENCE construction is centralized but not mathematical validation or statement-registry certification.'}
    (output / 'audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    code = '# R8-R5 変更コード全文\n\n新規 Factory 関数は以下。各ファイルの変更後 import と変更関数全文も続く。\n\n```python\n' + ADDITIONS + '\n```\n'
    for relative, (_, _, symbols, source) in sorted(prepared.items()):
        code += changed_code(source, relative, symbols)
    (output / 'CHANGED_CODE.md').write_text(code, encoding='utf-8')
    return report


if __name__ == '__main__':
    root = Path.cwd()
    report = migrate(root, dry_run='--dry-run' in sys.argv)
    print(json.dumps(report, ensure_ascii=False, indent=2))
