# R15R14 — 完全な変更単位

以下の関数をそのまま置換できる単位で示す。`web_group_proof_common.py` では既存ファイルの import 部分を変更しない。追加の import は関数本体に収める。`layout.py` は変更後の全文を示す。数行の省略や `...` は用いない。

## 1. `web_group_proof_common.py` — `_group_proof_statement_latex` 全文

```python
def _group_proof_statement_latex(
  statement,
) -> tuple[
  str | None,
  str | None,
]:
  from expression import Expression
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

  public_group_latex = (
    render_toda_public_group_relation_latex(
      statement
    )
  )

  if public_group_latex is not None:
    return (
      public_group_latex,
      None,
    )

  try:
    latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    latex = (
      render_toda_proof_statement_latex(
        statement
      )
    )

  if latex is None:
    return (
      None,
      type(
        statement
      ).__name__,
    )

  return (
    latex,
    None,
  )
```

## 2. `phase173_r4_r15r13_unified_presentation/layout.py` — ファイル全文（import と両関数）

```python
"""Status-independent presentation contract for all group proof narratives.

This is a structural presentation pass. It adds no ProofStep, inference,
literature reference, group conclusion, or proof status. The existing Markdown
API remains unchanged. One Web section hierarchy is produced for every status.
"""
from __future__ import annotations


def _public_search_diagnostic_line(line: str) -> str:
    """Present a recorded diagnostic without exposing a Python object repr.

    This only changes the public display. The original diagnostic remains in
    ProofNarrativeModel and PartialProofResult for inspection and auditing.
    """
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


def canonicalize_proof_layout(markdown: str) -> str:
    """Use one Reference/Proof section layout, preserving proof body verbatim.

    Both historical Markdown spellings (plain and ## headings) represent the
    same semantic sections. Only the outer Web-owned target and Proof headers
    are suppressed when duplicates are present inside the narrative. This
    transformation never reads status, n, k, references, or mathematical data.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be str")
    lines = markdown.splitlines()
    reference_indices = [
        i for i, line in enumerate(lines)
        if line.strip() in ("使用する結果", "## 使用する結果")
    ]
    if len(reference_indices) != 1:
        return markdown
    reference_index = reference_indices[0]
    proof_indices = [
        i for i in range(reference_index + 1, len(lines))
        if lines[i].strip() in ("証明", "## 証明")
    ]
    if len(proof_indices) != 1:
        return markdown
    proof_index = proof_indices[0]

    prelude = list(lines[:reference_index])
    # WebGroupProofView already presents the group target above the narrative.
    # Remove the second copy only when the entire prelude consists of that
    # exact heading and one displayable math target. Leave unknown preludes
    # intact rather than silently discarding source content.
    meaningful = [line.strip() for line in prelude if line.strip()]
    if (len(meaningful) == 2 and meaningful[0] == "## 証明対象"
            and meaningful[1].startswith("$") and meaningful[1].endswith("$")):
        prelude = []

    reference_body = list(lines[reference_index + 1:proof_index])
    while reference_body and not reference_body[-1].strip():
        reference_body.pop()
    if reference_body and reference_body[-1].strip() == "---":
        reference_body.pop()
    while reference_body and not reference_body[-1].strip():
        reference_body.pop()
    while reference_body and not reference_body[0].strip():
        reference_body.pop(0)

    proof_body = list(lines[proof_index + 1:])
    while proof_body and not proof_body[0].strip():
        proof_body.pop(0)

    # The outer Web Proof heading owns the proof section title. All narratives
    # receive the same inner Reference heading and the same section separator.
    # Only headings and redundant duplicate-target presentation are modified.
    normalized = [*prelude, "## 使用する結果", "", *reference_body,
                  "", "---", "", *proof_body]
    in_search_diagnostics = False
    for index, line in enumerate(normalized):
        if line.startswith(("## ", "### ")):
            in_search_diagnostics = line.strip() == "## 探索診断"
        elif in_search_diagnostics and line.startswith("- "):
            normalized[index] = _public_search_diagnostic_line(line)
    result = "\n".join(normalized)
    return result.rstrip("\n") + ("\n" if markdown.endswith("\n") else "")
```

新規 `_public_search_diagnostic_line` は `canonicalize_proof_layout` の直前に追加する。既存 `_build_group_proof_rendered_lines`、既存クラス、既存 public API のシグネチャは変更しない。
