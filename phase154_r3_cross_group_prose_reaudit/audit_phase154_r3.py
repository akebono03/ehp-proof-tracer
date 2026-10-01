from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


REPRESENTATIVE_GROUPS = (
  (3, 3, "pi6_3", "primary"),
  (4, 6, "pi10_4", "primary"),
  (4, 7, "pi11_4", "primary"),
  (5, 7, "pi12_5", "secondary"),
  (9, 7, "pi16_9", "secondary"),
)


KNOWN_INTERNAL_FRAGMENTS = (
  "Toda (5.6) nu_4 decomposition integration",
  r"\text{ is injective}",
  r"\text{ is exact}",
  "Toda Proposition 5.15を用いる。",
  "である.を用いる。",
)


TRANSITION_PREFIXES = (
  "まず、",
  "また、",
  "さらに、",
  "これより、",
  "これらより、",
  "このことから、",
  "これらから、",
  "したがって、",
  "以上より、",
  "以上により、",
)


def render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise RuntimeError(
      f"no candidate for n={n}, k={k}"
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def proof_body(
  rendered: str,
) -> str:
  marker = "## 証明\n"

  if marker not in rendered:
    return rendered

  return rendered.split(
    marker,
    1,
  )[1].lstrip()


def nonblank_lines(
  text: str,
) -> tuple[str, ...]:
  return tuple(
    line.strip()
    for line in text.splitlines()
    if line.strip()
  )


def find_internal_fallbacks(
  body: str,
) -> tuple[str, ...]:
  findings = []

  for fragment in KNOWN_INTERNAL_FRAGMENTS:
    for line in body.splitlines():
      if fragment in line:
        findings.append(
          line.strip()
        )

  return tuple(
    findings
  )


def find_bare_reference_markers(
  body: str,
) -> tuple[str, ...]:
  findings = []

  for line in nonblank_lines(
    body
  ):
    if re.fullmatch(
      r"(?:まず、|また、|さらに、)?\[R[0-9]+\]",
      line,
    ):
      findings.append(
        line
      )

  return tuple(
    findings
  )


def find_transition_repetition(
  body: str,
) -> tuple[str, ...]:
  lines = nonblank_lines(
    body
  )
  findings = []

  for previous, current in zip(
    lines,
    lines[1:],
  ):
    previous_prefix = next(
      (
        prefix
        for prefix in TRANSITION_PREFIXES
        if previous.startswith(
          prefix
        )
      ),
      None,
    )
    current_prefix = next(
      (
        prefix
        for prefix in TRANSITION_PREFIXES
        if current.startswith(
          prefix
        )
      ),
      None,
    )

    if (
      previous_prefix is not None
      and current_prefix is not None
      and previous_prefix == current_prefix
    ):
      findings.append(
        previous
        + " || "
        + current
      )

    if (
      previous_prefix == "また、"
      and current_prefix == "まず、"
    ):
      findings.append(
        previous
        + " || "
        + current
      )

  return tuple(
    findings
  )


def find_semantic_duplication(
  body: str,
) -> tuple[str, ...]:
  lines = nonblank_lines(
    body
  )
  counts = Counter(
    lines
  )
  findings = [
    line
    for line, count in counts.items()
    if (
      count > 1
      and not line.startswith(
        "**[R"
      )
    )
  ]

  aggregate_phrase = (
    "以上で得た群構造、生成元、および写像に関する結果を合わせると、"
  )
  if body.count(
    aggregate_phrase
  ) > 1:
    findings.append(
      aggregate_phrase
      + f" [count={body.count(aggregate_phrase)}]"
    )

  return tuple(
    findings
  )


def find_reference_linkage(
  body: str,
) -> tuple[str, ...]:
  findings = []

  for line in nonblank_lines(
    body
  ):
    if re.fullmatch(
      r"(?:まず、|また、|さらに、)?\[R[0-9]+\]を用いる。",
      line,
    ):
      findings.append(
        line
      )

  return tuple(
    findings
  )


def find_punctuation(
  body: str,
) -> tuple[str, ...]:
  findings = []

  for line in nonblank_lines(
    body
  ):
    if line.endswith("."):
      findings.append(
        line
      )
    if ".。" in line or "。." in line:
      findings.append(
        line
      )

  return tuple(
    findings
  )


def audit_rendered(
  rendered: str,
) -> dict[str, tuple[str, ...]]:
  body = proof_body(
    rendered
  )

  return {
    "internal_fallback": find_internal_fallbacks(
      body
    ),
    "bare_reference_marker": find_bare_reference_markers(
      body
    ),
    "transition_repetition": find_transition_repetition(
      body
    ),
    "semantic_duplication": find_semantic_duplication(
      body
    ),
    "reference_body_linkage_candidate": find_reference_linkage(
      body
    ),
    "punctuation": find_punctuation(
      body
    ),
  }


def write_group_report(
  output_dir: Path,
  key: str,
  n: int,
  k: int,
  tier: str,
  rendered: str,
  findings: dict[
    str,
    tuple[
      str,
      ...,
    ],
  ],
) -> None:
  lines = [
    f"# Phase 154-R3 — {key}",
    "",
    f"- group: $\\pi_{{{n + k}}}^{{{n}}}$",
    f"- tier: {tier}",
    "- view: Narrative",
    "- depth: 2",
    "",
    "## Findings",
    "",
  ]

  for category, category_findings in findings.items():
    lines.append(
      f"### {category}"
    )
    lines.append("")
    lines.append(
      f"count: {len(category_findings)}"
    )
    lines.append("")

    if category_findings:
      for finding in category_findings:
        lines.append(
          "- `"
          + finding.replace(
            "`",
            r"\`",
          )
          + "`"
        )
    else:
      lines.append(
        "- none"
      )

    lines.append("")

  lines.extend(
    (
      "## Narrative",
      "",
      rendered.rstrip(),
      "",
    )
  )

  (
    output_dir
    / f"{key}.md"
  ).write_text(
    "\n".join(
      lines
    ),
    encoding="utf-8",
  )


def main() -> int:
  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )

  if output_dir.exists():
    shutil.rmtree(
      output_dir
    )

  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  totals = Counter()
  affected = Counter()
  summary_rows = []

  for n, k, key, tier in REPRESENTATIVE_GROUPS:
    rendered = render_group(
      n,
      k,
    )
    findings = audit_rendered(
      rendered
    )

    write_group_report(
      output_dir,
      key,
      n,
      k,
      tier,
      rendered,
      findings,
    )

    row_counts = {}

    for category, category_findings in findings.items():
      count = len(
        category_findings
      )
      totals[
        category
      ] += count

      if count:
        affected[
          category
        ] += 1

      row_counts[
        category
      ] = count

    summary_rows.append(
      (
        key,
        n,
        k,
        tier,
        row_counts,
      )
    )

  summary = [
    "# Phase 154-R3 Cross-group Prose Re-audit",
    "",
    "Production changes: none.",
    "",
    "Conditions:",
    "- Narrative view",
    "- depth 2",
    "- primary: pi6_3, pi10_4, pi11_4",
    "- secondary: pi12_5, pi16_9",
    "",
    "## Category totals",
    "",
  ]

  categories = (
    "internal_fallback",
    "bare_reference_marker",
    "transition_repetition",
    "semantic_duplication",
    "reference_body_linkage_candidate",
    "punctuation",
  )

  for category in categories:
    summary.append(
      "- "
      + category
      + ": affected_groups="
      + str(
        affected[
          category
        ]
      )
      + ", findings="
      + str(
        totals[
          category
        ]
      )
    )

  summary.extend(
    (
      "",
      "## Per-group counts",
      "",
      "| group | tier | internal fallback | bare reference | transition | duplication | reference linkage candidate | punctuation |",
      "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    )
  )

  for key, n, k, tier, counts in summary_rows:
    summary.append(
      "| "
      + f"$\\pi_{{{n + k}}}^{{{n}}}$"
      + " | "
      + tier
      + " | "
      + str(
        counts[
          "internal_fallback"
        ]
      )
      + " | "
      + str(
        counts[
          "bare_reference_marker"
        ]
      )
      + " | "
      + str(
        counts[
          "transition_repetition"
        ]
      )
      + " | "
      + str(
        counts[
          "semantic_duplication"
        ]
      )
      + " | "
      + str(
        counts[
          "reference_body_linkage_candidate"
        ]
      )
      + " | "
      + str(
        counts[
          "punctuation"
        ]
      )
      + " |"
    )

  summary.extend(
    (
      "",
      "## Interpretation rule",
      "",
      "- internal_fallback / bare_reference_marker: R2 regression candidate.",
      "- transition_repetition: R4 candidate.",
      "- semantic_duplication: R4 candidate.",
      "- reference_body_linkage_candidate: R5 candidate; a hit is not automatically a defect.",
      "- punctuation: R6 candidate.",
      "- This audit does not modify production code.",
      "",
    )
  )

  (
    output_dir
    / "phase154_r3_summary.md"
  ).write_text(
    "\n".join(
      summary
    ),
    encoding="utf-8",
  )

  print(
    "\n".join(
      summary
    )
  )

  return 0


if __name__ == "__main__":
  import shutil

  raise SystemExit(
    main()
  )
