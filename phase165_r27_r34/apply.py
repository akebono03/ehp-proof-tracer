"""R27-R34 AST-safe installation of common typed lookup / Web operation entry."""
import ast
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / 'web_operation_query.py'

FUNCTION = '''def build_standard_web_operation_query_view(query_input: str) -> WebOperationQueryView:
    if not isinstance(query_input, str):
        raise TypeError("query_input must be a str")
    query_input = query_input.strip()
    if not query_input:
        raise ValueError("operation query is required")
    from phase165_r27_r34_typed_lookup import search_typed_operation_statements
    from toda_proof_narrative_renderer import render_toda_proof_statement_latex
    result = search_typed_operation_statements(query_input)
    items = []
    for step in result.proven_steps:
        statement_latex = render_toda_proof_statement_latex(step.conclusion)
        if not isinstance(statement_latex, str) or not statement_latex:
            continue
        items.append(WebOperationQueryItemView(statement_latex=statement_latex, provenance_count=1))
    return WebOperationQueryView(query_input=query_input, found=bool(items), items=tuple(items))
'''


def transform(source):
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'build_standard_web_operation_query_view']
    if len(matches) != 1:
        raise RuntimeError('Web Operation Query entry not found uniquely')
    node = matches[0]
    lines = source.splitlines(keepends=True)
    rewritten = ''.join(lines[:node.lineno - 1]) + FUNCTION + ''.join(lines[node.end_lineno:])
    # Drop the two obsolete, eager legacy imports. Their facade imports
    # a Bootstrap module that was deleted in R27-R26.
    legacy_names = {
        "repository_operation_query_facade",
        "repository_operation_query_presentation",
    }
    lines = rewritten.splitlines(keepends=True)
    drop = set()
    for statement in ast.parse(rewritten).body:
        if isinstance(statement, ast.ImportFrom) and statement.module in legacy_names:
            drop.update(range(statement.lineno - 1, statement.end_lineno))
    rewritten = "".join(line for index, line in enumerate(lines) if index not in drop)
    ast.parse(rewritten)
    return rewritten


def apply():
    code = (HERE / 'phase165_r27_r34_typed_lookup.py').read_bytes()
    ast.parse(code.decode('utf-8'))
    dest = ROOT / 'phase165_r27_r34_typed_lookup.py'
    if dest.exists() and dest.read_bytes() != code:
        raise RuntimeError('existing typed lookup differs; do not overwrite')
    source = TARGET.read_text(encoding='utf-8')
    updated = transform(source)
    if updated != source:
        backup = HERE / 'web_operation_query.before_r34.py'
        if not backup.exists():
            shutil.copy2(TARGET, backup)
        TARGET.write_text(updated, encoding='utf-8')
    dest.write_bytes(code)
    print('R27-R34 installed: common typed Generator/Operation search and Web Operation entry')


if __name__ == '__main__':
    apply()
