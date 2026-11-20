"""Narrow, fail-closed full-function replacement for R3R24."""
from __future__ import annotations
import ast
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase171_r2h_prop22_cited_hopf' / 'source.py'
REPLACEMENT = (Path(__file__).resolve().parent / 'replacement.py').read_text(encoding='utf-8')

def replacement_text(text: str) -> str:
    tree = ast.parse(text)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == '_formula_parts']
    if len(matches) != 1:
        raise RuntimeError('FORMULA_PARTS_ANCHOR_NOT_UNIQUE')
    node = matches[0]
    lines = text.splitlines(keepends=True)
    current = ''.join(lines[node.lineno - 1:node.end_lineno])
    required = ('not isinstance(alpha, HomotopyElement)', 'product.is_type_compatible()', 'expected = Composition(MapApplication(EHP_H_MAP, alpha), right)')
    if not all(anchor in current for anchor in required):
        if current.strip() == REPLACEMENT.strip():
            return text
        raise RuntimeError('FORMULA_PARTS_BASELINE_CHANGED')
    updated = lines[:node.lineno - 1] + [REPLACEMENT.rstrip() + '\n'] + lines[node.end_lineno:]
    result = ''.join(updated)
    ast.parse(result)
    return result

def verify_root() -> str:
    def git(*args: str) -> str:
        result = subprocess.run(('git', *args), cwd=ROOT, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT.resolve():
        raise RuntimeError('WRONG_REPOSITORY')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    if git('diff', '--', 'phase171_r2h_prop22_cited_hopf/source.py'):
        raise RuntimeError('TARGET_HAS_UNCOMMITTED_CHANGES')
    return git('rev-parse', 'HEAD')

def install(dry_run: bool) -> dict[str, object]:
    head = verify_root()
    original = TARGET.read_bytes()
    content = original.decode('utf-8-sig')
    patched = replacement_text(content)
    if patched == content:
        raise RuntimeError('ALREADY_PATCHED_OR_NO_CHANGE')
    if not dry_run:
        # Preserve the original EOL convention.
        if b'\r\n' in original:
            patched = patched.replace('\r\n', '\n').replace('\n', '\r\n')
        TARGET.write_bytes(patched.encode('utf-8'))
    return {'head': head, 'dry_run': dry_run, 'target': str(TARGET.relative_to(ROOT)), 'updated': not dry_run}
