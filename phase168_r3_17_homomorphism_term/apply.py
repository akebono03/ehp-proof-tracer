from __future__ import annotations

import ast
from pathlib import Path


def main() -> None:
    repo = Path.cwd()
    target = repo / 'toda_group_proof_narrative_renderer.py'
    if not target.is_file():
        raise FileNotFoundError(target)
    original = target.read_text(encoding='utf-8-sig')
    old = 'if "第一同型定理" not in "\\n\\n".join(paragraphs):'
    new = 'if "準同型定理" not in "\\n\\n".join(paragraphs):'
    if original.count(old) != 1:
        if original.count(new) == 1:
            print('ALREADY_PATCHED:', target)
            updated = original
        else:
            raise ValueError('Expected unique old guard; repository was not changed')
    else:
        updated = original.replace(old, new, 1)
        backup = Path(__file__).resolve().parent / 'backup'
        backup.mkdir(exist_ok=True)
        (backup / target.name).write_text(original, encoding='utf-8')
        ast.parse(updated)
        target.write_text(updated, encoding='utf-8')
        print('PATCHED:', target)
    # Full, unabridged affected function, extracted from the installed code.
    parsed = ast.parse(updated)
    function = next((node for node in parsed.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'render_toda_group_proof_narrative_markdown'), None)
    if function is None:
        raise ValueError('public function not found')
    lines = updated.splitlines(keepends=True)
    out = Path(__file__).resolve().parent / 'output'
    out.mkdir(exist_ok=True)
    (out / 'render_toda_group_proof_narrative_markdown_FULL.py').write_text(''.join(lines[function.lineno - 1:function.end_lineno]), encoding='utf-8')
    # Imports unchanged; save entire import region as verification artifact.
    first_function = min(n.lineno for n in parsed.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)))
    (out / 'imports_and_prefix_FULL.py').write_text(''.join(lines[:first_function-1]), encoding='utf-8')
    print('FULL_FUNCTION:', out / 'render_toda_group_proof_narrative_markdown_FULL.py')


if __name__ == '__main__':
    main()
