"""R15R14 minimal, source-guarded presentation changes.

There is no generator- or dimension-specific rendering branch. The public
Web model continues to own proof status, Goal collection, and source evidence.
"""
from __future__ import annotations


def patch_common(source: str) -> str:
    """Reuse the existing group Relation renderer for typed cyclic pending goals."""
    anchor = "  public_group_latex = (\n"
    replacement = """  from expression import Expression
  from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
  from phase165_r12_r2_quotient_rules import CyclicStructureStatement
  from proof import Relation, RelationType

  if (
    isinstance(statement, CyclicStructureStatement)
    and isinstance(statement.group, TodaPrimaryGroup)
    and isinstance(statement.generator, Expression)
    and (
      statement.order is None
      or (type(statement.order) is int and statement.order >= 1)
    )
  ):
    structure = (
      FreeCyclicGroup(statement.generator)
      if statement.order is None
      else FiniteCyclicGroup(statement.order, statement.generator)
    )
    try:
      cyclic_latex = render_toda_public_group_relation_latex(
        Relation(
          lhs=statement.group,
          rhs=structure,
          relation_type=RelationType.EQUALITY,
        )
      )
    except (TypeError, ValueError):
      cyclic_latex = None
    if cyclic_latex is not None:
      return cyclic_latex, None

""" + anchor
    if source.count(anchor) != 1 or '  from phase165_r12_r2_quotient_rules import CyclicStructureStatement\n' in source:
        raise ValueError('Common typed renderer anchor changed or patch already applied')
    return source.replace(anchor, replacement, 1)


def patch_layout(source: str) -> str:
    """Keep evidence text untouched; project diagnostics in the Web display only."""
    anchor = 'def canonicalize_proof_layout(markdown: str) -> str:\n'
    helper = """def _public_search_diagnostic_line(line: str) -> str:
    \"\"\"Present a recorded diagnostic without exposing a Python object repr.

    This only changes the public display. The original diagnostic remains in
    ProofNarrativeModel and PartialProofResult for inspection and auditing.
    \"\"\"
    if not line.startswith("- "):
        return line
    message = line[2:].strip()
    prefix = "expected a verified registered derivation for "
    if message.startswith(prefix):
        before, separator, count = message.rpartition(", found ")
        if separator and before.startswith(prefix) and count.isdecimal():
            return (
                "- 登録済みの前提から証明目標を導く検証済みの推論が見つかりませんでした"
                f"（導出候補 {count} 件）。"
            )
    if any(token in message for token in (
        "Relation(", "TodaPrimaryGroup(", "HomotopyElement(",
        "GeneratorSymbol(",
    )):
        return "- 型付き証明目標の内部診断があります。詳細は監査ログを参照してください。"
    return line


""" + anchor
    old = """    normalized = [*prelude, "## 使用する結果", "", *reference_body,
                  "", "---", "", *proof_body]
    result = "\\n".join(normalized)
"""
    new = """    normalized = [*prelude, "## 使用する結果", "", *reference_body,
                  "", "---", "", *proof_body]
    in_search_diagnostics = False
    for index, line in enumerate(normalized):
        if line.startswith(("## ", "### ")):
            in_search_diagnostics = line.strip() == "## 探索診断"
        elif in_search_diagnostics and line.startswith("- "):
            normalized[index] = _public_search_diagnostic_line(line)
    result = "\\n".join(normalized)
"""
    if source.count(anchor) != 1 or source.count(old) != 1 or 'def _public_search_diagnostic_line' in source:
        raise ValueError('Existing common layout contract anchor changed or patch already applied')
    return source.replace(anchor, helper, 1).replace(old,new,1)
