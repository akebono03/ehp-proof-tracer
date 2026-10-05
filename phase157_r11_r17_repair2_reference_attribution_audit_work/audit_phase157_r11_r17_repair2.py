from __future__ import annotations

import re
import sys
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

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
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  filter_phase157_r3_pi6_3_reference_entries,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
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


TARGETS = (
  (3, 3),
  (4, 6),
  (5, 7),
  (9, 7),
)

REFERENCE_HEADER_RE = re.compile(
  r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*"
)


def _build(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  return (
    presentation,
    rendered,
  )


def _reference_identity(
  step,
):
  reference = (
    extract_toda_group_proof_step_literature_reference(
      step
    )
  )

  if reference is None:
    return None

  return (
    reference.locator
    or reference.label
  )


def _entry_map(
  presentation,
):
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries,
      presentation.root_step,
    )
  )
  entries = (
    filter_phase157_r3_pi6_3_reference_entries(
      entries,
      presentation.root_step,
    )
  )

  return {
    (
      entry.reference.locator
      or entry.reference.label
    ): entry
    for entry in entries
  }


def main() -> int:
  lines = [
    "=" * 78,
    "Phase157 R11-R17 repair2 pre-audit — Reference attribution",
    "=" * 78,
    "Production code changes: none",
    "Test code changes: none",
    "",
  ]

  for n, k in TARGETS:
    presentation, rendered = _build(
      n,
      k,
    )
    reference, body = rendered.split(
      "\n## 証明\n",
      1,
    )
    headers = tuple(
      (
        int(
          match.group(
            1
          )
        ),
        match.group(
          2
        ),
      )
      for match in REFERENCE_HEADER_RE.finditer(
        reference
      )
    )
    entries = _entry_map(
      presentation
    )
    consumers_by_step_id = {}

    for edge in presentation.edges:
      consumers_by_step_id.setdefault(
        id(
          edge.premise_step
        ),
        [],
      ).append(
        edge.parent_step
      )

    lines.extend(
      (
        "-" * 78,
        f"pi_{n + k}^{n}",
        "-" * 78,
        "PUBLIC HEADERS:",
      )
    )

    for number, title in headers:
      lines.append(
        f"  [R{number}] {title}"
      )

      entry = entries.get(
        title
      )

      if entry is None:
        lines.append(
          "    raw entry lookup: FAILED"
        )
        continue

      for step in entry.proof_steps:
        rendered_step = (
          _render_generic_narrative_step(
            step
          )
        )
        lines.append(
          "    SOURCE: "
          + rendered_step
        )

        for consumer in consumers_by_step_id.get(
          id(
            step
          ),
          (),
        ):
          rendered_consumer = (
            _render_generic_narrative_step(
              consumer
            )
          )
          owner = _reference_identity(
            consumer
          )
          visible = (
            bool(
              rendered_consumer
            )
            and rendered_consumer in body
          )
          is_root = (
            consumer is presentation.root_step
          )

          lines.append(
            "      CONSUMER: "
            + rendered_consumer
          )
          lines.append(
            "        visible="
            + str(
              visible
            )
            + " root="
            + str(
              is_root
            )
            + " owner="
            + repr(
              owner
            )
          )

    lines.append(
      "BODY MARKERS:"
    )

    for number, title in headers:
      marker = (
        "[R"
        + str(
          number
        )
        + "]"
      )
      lines.append(
        "  "
        + marker
        + " count="
        + str(
          body.count(
            marker
          )
        )
      )

    lines.append("")

  report = (
    "\n".join(
      lines
    )
    + "\n"
  )

  output_dir = PACKAGE_DIR / "audit_output"
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    output_dir
    / "reference_attribution.txt"
  ).write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
