"""Phase 165 R27-R29: retire obsolete Prop. 5.6 generator and its private chain."""
from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

TARGETS = (
    'toda_prop56_zero_bootstrap.py',
    'toda_midstream_bootstrap.py',
    'toda_phase65_bootstrap.py',
)
REGISTRATION = 'phase163_r4_r12_literature_registration.py'
FUNCTION = 'existing_prop51_prop53_candidates'
MESSAGE = (
    'Legacy Phase 163 bootstrap-derived candidate extraction is retired; '
    'register explicitly supplied typed LiteratureComponentInput values instead.'
)


def replace_legacy_candidate_helper(source: str) -> tuple[str, bool]:
    tree = ast.parse(source)
    definitions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == FUNCTION]
    if len(definitions) != 1 or not isinstance(definitions[0], ast.FunctionDef):
        raise RuntimeError('Expected exactly one legacy candidate helper')
    function = definitions[0]
    # Keep the historical callable signature but stop importing the old bootstrap.
    replacement = (
        f'def {FUNCTION}() -> tuple[LiteratureComponentInput, ...]:\n'
        '    """Retired historical proof-step extraction, not a registration API."""\n'
        f'    raise RuntimeError({MESSAGE!r})\n'
    )
    lines = source.splitlines(keepends=True)
    old = ''.join(lines[function.lineno - 1:function.end_lineno])
    if ast.dump(ast.parse(old), include_attributes=False) == ast.dump(ast.parse(replacement), include_attributes=False):
        return source, False
    newline = '\r\n' if '\r\n' in source else '\n'
    new_lines = replacement.replace('\n', newline)
    new_source = ''.join(lines[:function.lineno - 1]) + new_lines + ''.join(lines[function.end_lineno:])
    ast.parse(new_source)
    return new_source, True


def active_imports(root: Path, *, replacement: str | None = None) -> list[dict[str, object]]:
    modules = {Path(name).stem for name in TARGETS}
    refs = []
    for path in sorted(root.glob('*.py')):
        if path.name in TARGETS:
            continue
        source = replacement if path.name == REGISTRATION and replacement is not None else path.read_text(encoding='utf-8-sig')
        tree = ast.parse(source, filename=str(path))
        for node in ast.walk(tree):
            candidates = []
            if isinstance(node, ast.ImportFrom) and node.module:
                candidates.append(node.module.split('.')[0])
            if isinstance(node, ast.Import):
                candidates.extend(alias.name.split('.')[0] for alias in node.names)
            for module in candidates:
                if module in modules:
                    refs.append({'file': path.name, 'line': node.lineno, 'module': module})
    return refs


def apply(root: Path | None = None) -> dict[str, object]:
    root = Path.cwd() if root is None else Path(root)
    target = root / REGISTRATION
    if not target.is_file():
        raise RuntimeError(f'Required registration module not found: {REGISTRATION}')
    original = target.read_text(encoding='utf-8-sig')
    changed_source, changed = replace_legacy_candidate_helper(original)
    refs = active_imports(root, replacement=changed_source)
    audit = root / 'phase165_r27_r29_audit.json'
    if refs:
        result = {'phase':'165 R27-R29','status':'BLOCKED','references':refs,'deleted':[],'full_pytest_run':False}
        audit.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        raise RuntimeError(f'Active imports found; no changes made. See {audit.name}')
    backups = root / 'phase165_r27_r29_removed_backup'
    originals = [root / name for name in TARGETS if (root / name).exists()]
    to_save = list(originals) + ([target] if changed else [])
    # Preflight all backups before making any changes.
    for path in to_save:
        dest = backups / path.name
        if dest.exists() and dest.read_bytes() != path.read_bytes():
            raise RuntimeError(f'Backup collision for {path.name}')
    if to_save:
        backups.mkdir(exist_ok=True)
        for path in to_save:
            shutil.copy2(path, backups / path.name)
    if changed:
        target.write_text(changed_source, encoding='utf-8')
    deleted = []
    for path in originals:
        path.unlink()
        deleted.append(path.name)
    result = {'phase':'165 R27-R29','status':'REMOVED' if deleted else 'ALREADY_REMOVED','registration_helper_retired':True,'registration_module_changed':changed,'references':[],'deleted':deleted,'full_pytest_run':False}
    audit.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result


if __name__ == '__main__':
    print(json.dumps(apply(), ensure_ascii=False, indent=2))
