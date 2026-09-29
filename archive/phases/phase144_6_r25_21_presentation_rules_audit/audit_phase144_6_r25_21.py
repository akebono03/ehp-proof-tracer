from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
  _render_phase134_3_pi6_3_narrative_markdown,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_argument import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


TARGETS = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


@dataclass(frozen=True)
class PresentationRule:
  key: str
  title: str
  legacy_patterns: tuple[str, ...]
  generic_patterns: tuple[str, ...]
  required: bool
  note: str


RULES = (
  PresentationRule(
    "section_structure",
    "Section structure",
    (r"# Group proof narrative", r"## 証明対象", r"## 使用する結果", r"## 証明"),
    (r"使用する結果",),
    True,
    "証明対象・使用結果・証明本文・結論を視覚的に分離する。",
  ),
  PresentationRule(
    "reference_labels",
    "Reference labels [R1], [R2], ...",
    (r"\[R1\]", r"\[R2\]"),
    (r"\[R1\]", r"\[R2\]"),
    True,
    "外部定理・補題を本文の式番号とは別 namespace で参照する。",
  ),
  PresentationRule(
    "equation_number_assignment",
    "Equation number assignment (1), (2), ...",
    (r"\\tag\{1\}", r"\\tag\{20\}"),
    (r"\\tag\{1\}",),
    True,
    "読者が後続推論で参照する主要式・主要写像性質・最終結論だけに連番を付ける。",
  ),
  PresentationRule(
    "equation_dependency_reference",
    "Equation dependency references",
    (
      r"\(1\), \(2\)",
      r"\(5\), \(15\)",
      r"\(8\), \(14\), \(18\)",
      r"\(7\), \(17\), \(19\)",
    ),
    (r"\([0-9]+\).+より",),
    True,
    "番号を単に表示するだけでなく、後続 Argument の根拠として参照する。",
  ),
  PresentationRule(
    "argument_sections",
    "Argument-level paragraph structure",
    (
      r"まず, Lemma 5\.2",
      r"\\nu'.+位数を決定",
      r"最後に, \$\\pi_\{6\}\^\{3\}\$ の群構造",
    ),
    (r"まず", r"したがって"),
    True,
    "definition/membership・order・group structure を論証単位の段落として構成する。",
  ),
  PresentationRule(
    "deduplicate_definitions",
    "Definition deduplication",
    (r"定め",),
    (r"定義",),
    True,
    "同一 definition を近接箇所で繰り返さず、最初の導入後は参照にする。",
  ),
  PresentationRule(
    "hide_internal_derivations",
    "Internal derivation suppression",
    (r"2\\nu'.+\\eta_\{3\}",),
    (r"22\\nu_",),
    True,
    "機械的正規化・内部 bookkeeping を主要 Narrative から隠す。",
  ),
  PresentationRule(
    "localized_map_properties",
    "Localized exactness/map-property prose",
    (r"は完全である", r"は単射である", r"は全射である"),
    (r"\\text\{ is exact\}|\\text\{ is injective\}|\\text\{ is surjective\}",),
    True,
    "raw English statement suffix を出さず、日本語の数学文として表示する。",
  ),
  PresentationRule(
    "short_exact_sequence",
    "Short exact sequence as a major result",
    (
      r"0\\longrightarrow\\pi_\{5\}\^\{2\}",
      r"\\pi_\{6\}\^\{3\}",
      r"\\longrightarrow 0",
    ),
    (r"0\\longrightarrow", r"\\longrightarrow 0"),
    True,
    "完全性・単射・全射をまとめ、短完全列を主要式として提示する。",
  ),
  PresentationRule(
    "final_conclusion",
    "Explicit final conclusion",
    (r"以上により", r"\\tag\{20\}"),
    (r"したがって",),
    True,
    "最後に target group を明示し、証明本文から結論を分離する。",
  ),
)


def _build_generic(n: int, k: int) -> str:
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_complete_toda_group_result_proof_replay(group_result)
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    sidecar,
  )
  return render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def _build_legacy_pi6_3() -> str:
  report = build_standard_toda_report(n=3, k=3)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_complete_toda_group_result_proof_replay(group_result)
  presentation = build_toda_group_proof_presentation(replay)
  return _render_phase134_3_pi6_3_narrative_markdown(presentation)


def _all(text: str, patterns: tuple[str, ...]) -> bool:
  return all(re.search(pattern, text, re.MULTILINE | re.DOTALL) for pattern in patterns)


def _count_tags(text: str) -> int:
  return len(re.findall(r"\\tag\{[0-9]+\}", text))


def _count_reference_labels(text: str) -> int:
  return len(re.findall(r"\[R[0-9]+\]", text))


def _duplicate_definition_lines(text: str) -> tuple[str, ...]:
  lines = [
    line.strip()
    for line in text.splitlines()
    if "定義を用いる" in line
  ]
  duplicates = []
  for left, right in zip(lines, lines[1:]):
    if left == right:
      duplicates.append(left)
  return tuple(duplicates)


def main() -> int:
  out_dir = Path(__file__).resolve().parent / "output"
  out_dir.mkdir(parents=True, exist_ok=True)

  legacy = _build_legacy_pi6_3()
  (out_dir / "legacy_pi6_3_presentation_specimen.md").write_text(
    legacy,
    encoding="utf-8",
  )

  generics = {}
  for label, n, k in TARGETS:
    text = _build_generic(n, k)
    generics[label] = text
    (out_dir / f"{label}_generic.md").write_text(
      text,
      encoding="utf-8",
    )

  lines = [
    "# Phase 144-6 R25-21 presentation rules audit",
    "",
    "## 目的",
    "",
    "旧 $\\pi_6^3$ Narrative を presentation specification として分解し、",
    "代表6群の generic production Narrative に不足する一般表示規則を確定する。",
    "",
    "この監査は production code を変更しない。",
    "",
    "## 旧 $\\pi_6^3$ の番号依存構造",
    "",
    "- (1), (2) → (3): Lemma 5.2 の仮定から $\\nu'\\in\\pi_6^3$。",
    "- (5), (15) → (16): $2\\nu'=\\eta_3^3$ と $\\operatorname{ord}(\\eta_3^3)=2$ から $\\operatorname{ord}(\\nu')=4$。",
    "- (4), (17) → (18): $H(\\nu')=\\eta_5$ と $\\pi_6^5=\\mathbb Z/2\\{\\eta_5\\}$ から $H$ の全射性。",
    "- (8), (14), (18) → (19): EHP 完全列・$E$ の単射性・$H$ の全射性から短完全列。",
    "- (7), (17), (19) および (3), (16) → (20): 群の位数と位数4の生成元から最終群構造。",
    "",
    "したがって equation numbering は装飾ではなく Argument dependency の表示である。",
    "",
    "## Presentation rule inventory",
    "",
    "| rule | legacy $\\pi_6^3$ | generic 6群 | 判定 |",
    "|---|---:|---:|---|",
  ]

  missing_keys = []
  for rule in RULES:
    legacy_has = _all(legacy, rule.legacy_patterns)
    generic_count = sum(
      1 for text in generics.values()
      if _all(text, rule.generic_patterns)
    )
    if rule.key == "hide_internal_derivations":
      generic_count = sum(
        1 for text in generics.values()
        if not _all(text, rule.generic_patterns)
      )
      status = (
        "不足"
        if generic_count < len(generics)
        else "一般化済み"
      )
    elif rule.key == "localized_map_properties":
      raw_count = sum(
        1 for text in generics.values()
        if _all(text, rule.generic_patterns)
      )
      generic_count = len(generics) - raw_count
      status = (
        "不足"
        if raw_count > 0
        else "一般化済み"
      )
    else:
      status = (
        "一般化済み"
        if generic_count == len(generics)
        else "不足"
      )

    if rule.required and status == "不足":
      missing_keys.append(rule.key)

    lines.append(
      f"| {rule.title} | {'yes' if legacy_has else 'no'} | "
      f"{generic_count}/{len(generics)} | **{status}** |"
    )

  lines.extend(
    [
      "",
      "## 6群の観測値",
      "",
      "| group | chars | equation tags | [R#] labels | adjacent duplicate definitions | raw English map property | internal `22\\\\nu` |",
      "|---|---:|---:|---:|---:|---:|---:|",
    ]
  )

  for label, _, _ in TARGETS:
    text = generics[label]
    duplicates = _duplicate_definition_lines(text)
    raw_english = len(
      re.findall(
        r"\text\{ is (?:exact|injective|surjective)\}",
        text,
      )
    )
    internal_22 = len(re.findall(r"22\\nu_", text))
    lines.append(
      f"| {label} | {len(text)} | {_count_tags(text)} | "
      f"{_count_reference_labels(text)} | {len(duplicates)} | "
      f"{raw_english} | {internal_22} |"
    )

  lines.extend(
    [
      "",
      "## R25-22 以降に実装すべき一般 presentation rules",
      "",
    ]
  )

  for index, rule in enumerate(RULES, start=1):
    lines.extend(
      [
        f"### P{index:02d}. {rule.title}",
        "",
        f"- key: `{rule.key}`",
        f"- 目的: {rule.note}",
        "- 実装原則: 群座標や $\\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。",
        "",
      ]
    )

  lines.extend(
    [
      "## 実装順序案",
      "",
      "1. Argument dependency に基づく主要式選択と equation numbering。",
      "2. 番号付き主要式を根拠として参照する dependency prose。",
      "3. Reference [R#] と equation number の namespace 分離。",
      "4. definition / precondition / order / group structure の Argument 段落化。",
      "5. 重複 definition と内部 derivation の抑制。",
      "6. exact/injective/surjective の日本語化と EHP / short exact sequence の主要式化。",
      "7. final conclusion の独立表示。",
      "",
      "## Phase boundary",
      "",
      "R25-21 は audit only。production source は変更しない。",
      "R25-22 から、この一覧の一般 presentation rules を generic renderer に実装する。",
      "$\\pi_6^3$ 専用分岐を新設しない。",
      "",
      "## Missing rule keys",
      "",
      ", ".join(missing_keys) if missing_keys else "(none)",
      "",
    ]
  )

  report = "\n".join(lines) + "\n"
  report_path = out_dir / "r25_21_presentation_rules_audit.md"
  report_path.write_text(report, encoding="utf-8")

  print("=" * 78)
  print("Phase 144-6 R25-21 presentation rules audit")
  print("AUDIT ONLY: production changes = none")
  print("=" * 78)
  print()
  print(report)
  print("Generated:")
  print(f"  {report_path}")
  print("  legacy_pi6_3_presentation_specimen.md")
  for label, _, _ in TARGETS:
    print(f"  {label}_generic.md")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
