from __future__ import annotations

from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase158_baseline_render_toda_group_proof_narrative_markdown,
  _phase159_r1_7b_exactness_matches_map_property,
  _phase159_r1_7b_exactness_step_latex,
  _phase159_r1_7b_map_property_signature,
  _phase159_r1_7b_normalize_public_exact_sequences,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


ROOT = Path.cwd()
OUTPUT_DIR = (
  ROOT
  / "phase159_r1_7b_repair13_matching_runtime_diagnosis"
  / "audit_output"
)


def _presentation():
  report = build_standard_toda_report(
    n=4,
    k=7,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )

  return build_toda_group_proof_presentation(
    replay
  )


def _proof_body(
  rendered: str,
) -> list[str]:
  marker = "## 証明"
  lines = rendered.rstrip().splitlines()
  marker_index = lines.index(
    marker
  )
  body = lines[
    marker_index + 1:
  ]

  while (
    body
    and not body[0].strip()
  ):
    body.pop(
      0
    )

  while (
    body
    and body[-1].strip()
    in (
      "□",
      r"$\square$",
      r"\(\square\)",
      r"\square",
    )
  ):
    body.pop()

  return body


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  presentation = _presentation()
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  candidates = tuple(
    latex
    for latex in (
      _phase159_r1_7b_exactness_step_latex(
        node.proof_step
      )
      for node in closure.nodes
      if isinstance(
        node.proof_step.conclusion,
        TodaProp42ExactnessStatement,
      )
    )
    if latex is not None
  )

  baseline = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  body = _proof_body(
    baseline
  )

  report = [
    "# Phase 159-R1-7b repair13 matching runtime diagnosis",
    "",
    "## Exactness candidates",
    "",
  ]

  for index, candidate in enumerate(
    candidates,
    start=1,
  ):
    report.extend(
      (
        f"### candidate {index}",
        "",
        f"`{candidate!r}`",
        "",
      )
    )

  report.extend(
    (
      "## Baseline proof body",
      "",
    )
  )

  for index, line in enumerate(
    body
  ):
    if (
      "完全性" not in line
      and r"\Delta" not in line
      and "Δ" not in line
      and "全射" not in line
      and r"\xrightarrow{" not in line
    ):
      continue

    signature = (
      _phase159_r1_7b_map_property_signature(
        line
      )
    )
    matches = tuple(
      candidate
      for candidate in candidates
      if (
        signature is not None
        and _phase159_r1_7b_exactness_matches_map_property(
          candidate,
          signature,
        )
      )
    )

    report.extend(
      (
        f"### line {index}",
        "",
        f"- repr: `{line!r}`",
        (
          "- startswith 完全性より,: "
          + repr(
            line.strip().startswith(
              "完全性より,"
            )
          )
        ),
        (
          "- equals 完全性より,: "
          + repr(
            line.strip()
            == "完全性より,"
          )
        ),
        (
          "- signature: "
          + repr(
            signature
          )
        ),
        (
          "- matching candidates: "
          + repr(
            matches
          )
        ),
        "",
      )
    )

    if line.strip().startswith(
      "完全性より,"
    ):
      remainder = line.strip()[
        len(
          "完全性より,"
        ):
      ].strip()
      remainder_signature = (
        _phase159_r1_7b_map_property_signature(
          remainder
        )
        if remainder
        else None
      )
      remainder_matches = tuple(
        candidate
        for candidate in candidates
        if (
          remainder_signature is not None
          and _phase159_r1_7b_exactness_matches_map_property(
            candidate,
            remainder_signature,
          )
        )
      )

      report.extend(
        (
          "- connector remainder: "
          + repr(
            remainder
          ),
          "- remainder signature: "
          + repr(
            remainder_signature
          ),
          "- remainder matching candidates: "
          + repr(
            remainder_matches
          ),
          "",
        )
      )

  normalized = (
    _phase159_r1_7b_normalize_public_exact_sequences(
      presentation,
      body,
    )
  )

  report.extend(
    (
      "## Normalized relevant lines",
      "",
    )
  )

  for index, line in enumerate(
    normalized
  ):
    if (
      "完全性" not in line
      and r"\Delta" not in line
      and "Δ" not in line
      and "全射" not in line
      and r"\xrightarrow{" not in line
      and line.strip()
      not in (
        r"\[",
        r"\]",
      )
    ):
      continue

    report.append(
      f"- {index}: `{line!r}`"
    )

  report.append("")

  text = "\n".join(
    report
  )

  (
    OUTPUT_DIR
    / "diagnosis.md"
  ).write_text(
    text,
    encoding="utf-8",
  )
  (
    OUTPUT_DIR
    / "baseline_pi11_4.md"
  ).write_text(
    baseline,
    encoding="utf-8",
  )
  (
    OUTPUT_DIR
    / "normalized_pi11_4.txt"
  ).write_text(
    "\n".join(
      normalized
    ),
    encoding="utf-8",
  )

  print(
    text
  )
  print("")
  print("Production code changes: none")
  print("Test changes: none")
  print("pytest: not run")

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
