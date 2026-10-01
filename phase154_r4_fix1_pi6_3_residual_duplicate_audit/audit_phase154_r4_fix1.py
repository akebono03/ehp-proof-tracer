from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
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
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


@dataclass(frozen=True)
class DuplicateOccurrence:
  line_number: int
  line: str
  previous_nonblank: str | None
  next_nonblank: str | None


def build_pi6_3():
  report = build_standard_toda_report(
    n=3,
    k=3,
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
  raw_presentation = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw_presentation
  )

  return (
    raw_presentation,
    presentation,
    rendered,
  )


def previous_nonblank(
  lines: list[str],
  index: int,
) -> str | None:
  for candidate_index in range(
    index - 1,
    -1,
    -1,
  ):
    candidate = lines[
      candidate_index
    ].strip()
    if candidate:
      return candidate

  return None


def next_nonblank(
  lines: list[str],
  index: int,
) -> str | None:
  for candidate_index in range(
    index + 1,
    len(
      lines
    ),
  ):
    candidate = lines[
      candidate_index
    ].strip()
    if candidate:
      return candidate

  return None


def exact_duplicate_occurrences(
  rendered: str,
) -> dict[
  str,
  tuple[
    DuplicateOccurrence,
    ...,
  ],
]:
  lines = rendered.splitlines()
  stripped = tuple(
    line.strip()
    for line in lines
    if line.strip()
  )
  counts = Counter(
    stripped
  )
  duplicate_texts = tuple(
    line
    for line, count in counts.items()
    if count > 1
  )
  result = {}

  for duplicate_text in duplicate_texts:
    occurrences = []

    for index, line in enumerate(
      lines
    ):
      if line.strip() != duplicate_text:
        continue

      occurrences.append(
        DuplicateOccurrence(
          line_number=index + 1,
          line=duplicate_text,
          previous_nonblank=previous_nonblank(
            lines,
            index,
          ),
          next_nonblank=next_nonblank(
            lines,
            index,
          ),
        )
      )

    result[
      duplicate_text
    ] = tuple(
      occurrences
    )

  return result


def classify_duplicate(
  text: str,
  occurrences: tuple[
    DuplicateOccurrence,
    ...,
  ],
) -> str:
  contexts = {
    (
      occurrence.previous_nonblank,
      occurrence.next_nonblank,
    )
    for occurrence in occurrences
  }

  if text.startswith(
    "$"
  ):
    if len(
      contexts
    ) > 1:
      return (
        "same rendered mathematical fact appears in "
        "different local contexts; inspect ownership before suppression"
      )

    return (
      "same rendered mathematical fact repeats in the same "
      "local context; strong semantic-duplication candidate"
    )

  if text in (
    "以上より、",
    "これらより、",
    "したがって、",
  ):
    return (
      "transition connector repeats; compare its target conclusions "
      "before deciding whether it is redundant"
    )

  if len(
    contexts
  ) > 1:
    return (
      "same prose appears in different local contexts; "
      "not automatically a semantic duplicate"
    )

  return (
    "same prose repeats in the same local context; "
    "strong semantic-duplication candidate"
  )


def reason_inventory(
  presentation,
) -> tuple[
  tuple[
    str,
    str | None,
    str,
  ],
  ...,
]:
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  rows = []

  for reason in reason_sidecar.reasons:
    sentence = (
      render_toda_group_proof_narrative_reason_sentence(
        reason
      )
    )
    rows.append(
      (
        reason.kind.name,
        sentence,
        type(
          reason.conclusion_step.conclusion
        ).__name__,
      )
    )

  return tuple(
    rows
  )


def main() -> int:
  (
    _raw_presentation,
    presentation,
    rendered,
  ) = build_pi6_3()

  duplicates = exact_duplicate_occurrences(
    rendered
  )
  reasons = reason_inventory(
    presentation
  )

  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  report_lines = [
    "# Phase 154-R4 Fix1 — pi6_3 Residual Duplicate Audit",
    "",
    "Production changes: none.",
    "",
    "Conditions:",
    "- group: $\\pi_6^3$",
    "- view: Narrative",
    "- depth: 2",
    "",
    "## Exact duplicate summary",
    "",
    f"duplicate_text_count: {len(duplicates)}",
    (
      "duplicate_occurrence_excess: "
      + str(
        sum(
          len(
            occurrences
          ) - 1
          for occurrences in duplicates.values()
        )
      )
    ),
    "",
  ]

  if not duplicates:
    report_lines.extend(
      (
        "- none",
        "",
      )
    )

  for duplicate_index, (
    text,
    occurrences,
  ) in enumerate(
    duplicates.items(),
    start=1,
  ):
    report_lines.extend(
      (
        f"### Duplicate {duplicate_index}",
        "",
        f"- text: `{text}`",
        f"- count: {len(occurrences)}",
        (
          "- audit classification: "
          + classify_duplicate(
            text,
            occurrences,
          )
        ),
        "",
        "Occurrences:",
        "",
      )
    )

    for occurrence in occurrences:
      report_lines.extend(
        (
          (
            "- line "
            + str(
              occurrence.line_number
            )
          ),
          (
            "  - previous: `"
            + str(
              occurrence.previous_nonblank
            )
            + "`"
          ),
          (
            "  - current: `"
            + occurrence.line
            + "`"
          ),
          (
            "  - next: `"
            + str(
              occurrence.next_nonblank
            )
            + "`"
          ),
        )
      )

    report_lines.append("")

  report_lines.extend(
    (
      "## Reason sidecar inventory",
      "",
    )
  )

  reason_counts = Counter(
    kind
    for kind, _sentence, _conclusion_type in reasons
  )

  for kind, count in sorted(
    reason_counts.items()
  ):
    report_lines.append(
      f"- {kind}: {count}"
    )

  report_lines.extend(
    (
      "",
      "## Reason details",
      "",
    )
  )

  for index, (
    kind,
    sentence,
    conclusion_type,
  ) in enumerate(
    reasons,
    start=1,
  ):
    report_lines.extend(
      (
        f"### Reason {index}",
        "",
        f"- kind: `{kind}`",
        f"- conclusion type: `{conclusion_type}`",
        (
          "- rendered sentence: `"
          + str(
            sentence
          ).replace(
            "\n",
            r"\n",
          )
          + "`"
        ),
        "",
      )
    )

  report_lines.extend(
    (
      "## Full Narrative",
      "",
      rendered.rstrip(),
      "",
      "## Decision boundary",
      "",
      (
        "- If both residual duplicate texts are transition/prose lines "
        "with different target contexts, keep them and close R4."
      ),
      (
        "- If a mathematical fact is emitted twice from the same "
        "ProofStep ownership path, prepare R4 Fix2 using the upstream "
        "ownership rule rather than line-based deduplication."
      ),
      (
        "- Reference linkage remains R5; punctuation remains R6."
      ),
      "",
    )
  )

  report_path = (
    output_dir
    / "phase154_r4_fix1_pi6_3_residual_duplicate_audit.md"
  )
  report_path.write_text(
    "\n".join(
      report_lines
    ),
    encoding="utf-8",
  )

  narrative_path = (
    output_dir
    / "pi6_3_narrative.txt"
  )
  narrative_path.write_text(
    rendered,
    encoding="utf-8",
  )

  print(
    "\n".join(
      report_lines[
        :(
          report_lines.index(
            "## Reason sidecar inventory"
          )
        )
      ]
    )
  )
  print(
    "Report:",
    report_path,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
