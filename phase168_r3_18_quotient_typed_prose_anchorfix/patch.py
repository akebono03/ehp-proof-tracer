from pathlib import Path
import ast
import shutil

def main():
    target = Path.cwd() / "toda_group_proof_narrative_shared_components.py"
    if not target.is_file():
        raise FileNotFoundError(target)
    original = target.read_text(encoding="utf-8-sig")
    tree = ast.parse(original)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "_render_generic_narrative_statement_prose"]
    if len(matches) != 1:
        raise ValueError("Expected one shared typed-prose function")
    node = matches[0]
    lines = original.splitlines(keepends=True)
    body = "".join(lines[node.lineno-1:node.end_lineno])
    anchor = "  reference_prose = (\n"
    if body.count(anchor) < 1:
        raise ValueError("Typed-prose insertion anchor changed")
    branch = """  # R3-18: use typed quotient facts, never inference-rule names.
  from phase165_r12_r2_quotient_rules import QuotientIsomorphismStatement
  if isinstance(statement, QuotientIsomorphismStatement):
    from phase165_r12_r34_r2_semantic_narrative import _element, _group
    if type(statement.multiple) is not int or statement.multiple < 1:
      return None
    try:
      return (
        "全射性と核の決定から, 準同型定理より $"
        + _group(statement.codomain)
        + r" \\\\cong "
        + _group(statement.domain)
        + r"/\\\\mathbb{Z}\\\\{"
        + str(statement.multiple)
        + _element(statement.source_generator)
        + r"\\\\}$ を得る."
      )
    except (TypeError, ValueError, AttributeError):
      return None

"""
    # Doubling is only for embedding string in the patch script; collapse
    branch=branch.replace(r"\\", "\\")
    if "# R3-18: use typed quotient facts" in body:
        print("ALREADY_PATCHED", target)
        return
    updated=original.replace(body,body.replace(anchor,branch+anchor,1),1)
    ast.parse(updated)
    backup=Path(__file__).resolve().parent/"backup"
    backup.mkdir(exist_ok=True)
    shutil.copy2(target,backup/target.name)
    target.write_text(updated,encoding="utf-8")
    out=Path(__file__).resolve().parent/"output"
    out.mkdir(exist_ok=True)
    full=ast.parse(updated)
    fn=next(n for n in full.body if isinstance(n,ast.FunctionDef) and n.name=="_render_generic_narrative_statement_prose")
    newlines=updated.splitlines(keepends=True)
    (out/"_render_generic_narrative_statement_prose_FULL.py").write_text("".join(newlines[fn.lineno-1:fn.end_lineno]),encoding="utf-8")
    print("PATCHED",target)
    print("FULL_FUNCTION",out/"_render_generic_narrative_statement_prose_FULL.py")

if __name__=="__main__":
    main()
