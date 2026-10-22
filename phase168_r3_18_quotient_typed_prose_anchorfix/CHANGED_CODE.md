# R3-18 修正版

対象は `toda_group_proof_narrative_shared_components.py` の `_render_generic_narrative_statement_prose()` です。実装関数全文は実行時に `output/_render_generic_narrative_statement_prose_FULL.py` へ保存します。import の変更はありません。

## パッチ適用コード全文

```python
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

```

## 限定テスト全文（import を含む）

```python
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r12_r2_quotient_rules import QuotientIsomorphismStatement
from toda_group_proof_narrative_shared_components import _render_generic_narrative_statement_prose

def test_pi43_quotient_uses_homomorphism_theorem():
    result=search_group_from_registered_goal(n=3,k=1,bridge=build_shared_typed_bridge())
    items=[s.conclusion for s in result.proven_steps if isinstance(s.conclusion,QuotientIsomorphismStatement)]
    assert len(items)==1
    prose=_render_generic_narrative_statement_prose(items[0])
    assert "準同型定理より" in prose
    assert r"\cong" in prose
    assert r"\mathbb{Z}" in prose
    assert "first isomorphism" not in prose

def test_unrelated_statement_is_not_rewritten():
    assert _render_generic_narrative_statement_prose(object()) is None

```
