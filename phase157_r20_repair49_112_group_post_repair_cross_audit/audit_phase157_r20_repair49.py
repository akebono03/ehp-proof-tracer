from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from proof import (
  Relation,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
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


EXPECTED_GROUPS = 112
MAX_DEPTH = 2
OUTPUT_DIR = (
  Path(__file__).resolve().parent
  / "audit_output"
)


def statement_match_key(
  line: str,
) -> str:
  normalized = line.strip().rstrip(
    ".,"
  )
  marker = r"\tag{"

  while True:
    marker_index = normalized.find(
      marker
    )

    if marker_index < 0:
      break

    number_start = (
      marker_index
      + len(
        marker
      )
    )
    number_end = normalized.find(
      "}",
      number_start,
    )

    if number_end < 0:
      break

    number_text = normalized[
      number_start:
      number_end
    ]

    if not number_text.isdigit():
      break

    normalized = (
      normalized[
        :marker_index
      ]
      + normalized[
        number_end + 1:
      ]
    )

  return normalized


def strip_reference_prefix(
  paragraph: str,
) -> str:
  stripped = paragraph.strip()

  if not stripped.startswith(
    "[R"
  ):
    return stripped

  marker_end = stripped.find(
    "]"
  )

  if marker_end < 0:
    return stripped

  suffix = stripped[
    marker_end + 1:
  ]

  for prefix in (
    "より, ",
    "を用いて, ",
  ):
    if suffix.startswith(
      prefix
    ):
      return suffix[
        len(
          prefix
        ):
      ]

  return stripped


def paragraph_key(
  paragraph: str,
) -> str:
  return statement_match_key(
    strip_reference_prefix(
      paragraph
    )
  )


def dangling_connector(
  paragraph: str,
) -> bool:
  standalone = {
    "以上より,",
    "したがって,",
    "これより,",
    "これらより,",
  }
  lines = tuple(
    line.strip()
    for line in paragraph.splitlines()
    if line.strip()
  )

  if not lines:
    return False

  if lines[
    -1
  ] in standalone:
    return True

  last = lines[
    -1
  ]

  return (
    last.startswith(
      "("
    )
    and last.endswith(
      "より,"
    )
    and ") と (" in last
    and "$" not in last
    and "[R" not in last
  )


def visible_reason_paragraph(
  reason,
) -> str | None:
  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )

  if sentence is None:
    return None

  lines = sentence.splitlines()

  while (
    lines
    and lines[
      -1
    ].strip()
    in {
      "以上より,",
      "したがって,",
      "これより,",
      "これらより,",
    }
  ):
    lines.pop()

  rendered = "\n".join(
    lines
  ).strip()

  return (
    rendered
    if rendered
    else None
  )


def paragraph_index_for_step(
  paragraphs: tuple[
    str,
    ...,
  ],
  proof_step,
) -> int | None:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  if not rendered:
    return None

  target_key = statement_match_key(
    rendered
  )
  matches = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if paragraph_key(
      paragraph
    )
    == target_key
  )

  if len(
    matches
  ) != 1:
    return None

  return matches[
    0
  ]


def audit_group(
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
    max_depth=MAX_DEPTH,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
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
  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )

  findings = []

  if "\n## 証明\n" not in rendered:
    findings.append(
      (
        "missing_proof_section",
        "",
      )
    )
    return (
      rendered,
      presentation,
      reason_sidecar,
      findings,
    )

  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]
  paragraphs = tuple(
    paragraph
    for paragraph in body.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  if not body.strip():
    findings.append(
      (
        "empty_body",
        "",
      )
    )

  if not body.rstrip().endswith(
    r"$\square$"
  ):
    findings.append(
      (
        "missing_qed",
        body[
          -160:
        ],
      )
    )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if dangling_connector(
      paragraph
    ):
      findings.append(
        (
          "dangling_connector",
          f"paragraph={index}: {paragraph}",
        )
      )

    if any(
      paragraph.strip().startswith(
        prefix
      )
      for prefix in (
        "以上より, [R",
        "したがって, [R",
        "これより, [R",
        "これらより, [R",
      )
    ):
      findings.append(
        (
          "redundant_connector_before_reference",
          f"paragraph={index}: {paragraph}",
        )
      )

  exact_counts = Counter(
    paragraph.strip()
    for paragraph in paragraphs
  )

  for paragraph, count in exact_counts.items():
    if count > 1:
      findings.append(
        (
          "exact_duplicate_paragraph",
          f"count={count}: {paragraph}",
        )
      )

  step_ids_by_key = {}

  for node in presentation.nodes:
    rendered_step = (
      _render_generic_narrative_step(
        node.proof_step
      )
    )

    if not rendered_step:
      continue

    key = statement_match_key(
      rendered_step
    )
    step_ids_by_key.setdefault(
      key,
      set(),
    ).add(
      id(
        node.proof_step
      )
    )

  body_key_counts = Counter(
    paragraph_key(
      paragraph
    )
    for paragraph in paragraphs
  )

  for key, step_ids in step_ids_by_key.items():
    if (
      len(
        step_ids
      ) == 1
      and body_key_counts.get(
        key,
        0,
      ) > 1
    ):
      findings.append(
        (
          "unique_step_repeated",
          (
            f"count={body_key_counts[key]} "
            f"key={key}"
          ),
        )
      )

  for node in presentation.nodes:
    consumer = node.proof_step

    if not isinstance(
      consumer.conclusion,
      Relation,
    ):
      continue

    consumer_index = (
      paragraph_index_for_step(
        paragraphs,
        consumer,
      )
    )

    if consumer_index is None:
      continue

    for premise in consumer.premises:
      if not isinstance(
        premise.conclusion,
        Relation,
      ):
        continue

      premise_index = (
        paragraph_index_for_step(
          paragraphs,
          premise,
        )
      )

      if premise_index is None:
        continue

      if premise_index > consumer_index:
        findings.append(
          (
            "relation_premise_after_consumer",
            (
              f"premise={premise_index} "
              f"consumer={consumer_index} "
              f"premise_text="
              f"{_render_generic_narrative_step(premise)} "
              f"consumer_text="
              f"{_render_generic_narrative_step(consumer)}"
            ),
          )
        )

  for reason in reason_sidecar.reasons:
    if (
      reason.kind
      is not TodaGroupProofNarrativeReasonKind
      .INJECTIVE_IMAGE_ORDER
    ):
      continue

    reason_paragraph = (
      visible_reason_paragraph(
        reason
      )
    )

    if reason_paragraph is None:
      continue

    matching_reason_indices = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == reason_paragraph
    )

    conclusion_index = (
      paragraph_index_for_step(
        paragraphs,
        reason.conclusion_step,
      )
    )
    premise_indices = tuple(
      paragraph_index_for_step(
        paragraphs,
        premise,
      )
      for premise in reason.premise_steps
    )

    if (
      len(
        matching_reason_indices
      ) != 1
      or conclusion_index is None
      or any(
        index is None
        for index in premise_indices
      )
    ):
      findings.append(
        (
          "injective_image_reason_unresolved_visibility",
          repr(
            (
              matching_reason_indices,
              premise_indices,
              conclusion_index,
            )
          ),
        )
      )
      continue

    reason_index = (
      matching_reason_indices[
        0
      ]
    )

    if not (
      max(
        premise_indices
      )
      < reason_index
      < conclusion_index
    ):
      findings.append(
        (
          "injective_image_reason_ordering",
          repr(
            (
              premise_indices,
              reason_index,
              conclusion_index,
            )
          ),
        )
      )

    if (
      conclusion_index
      != reason_index + 1
    ):
      findings.append(
        (
          "injective_image_reason_not_adjacent",
          repr(
            (
              reason_index,
              conclusion_index,
            )
          ),
        )
      )

  return (
    rendered,
    presentation,
    reason_sidecar,
    findings,
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  findings_rows = []
  group_rows = []
  exception_rows = []
  finding_counter = Counter()

  scanned = 0

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      scanned += 1
      label = (
        f"pi_{n + k}^{n}"
      )

      try:
        (
          rendered,
          presentation,
          reason_sidecar,
          findings,
        ) = audit_group(
          n,
          k,
        )
      except Exception as exc:
        exception_rows.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "exception_type": type(
              exc
            ).__name__,
            "message": str(
              exc
            ),
          }
        )
        group_rows.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "status": "EXCEPTION",
            "findings": 0,
          }
        )
        continue

      for kind, detail in findings:
        finding_counter[
          kind
        ] += 1
        findings_rows.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "kind": kind,
            "detail": detail,
          }
        )

      group_rows.append(
        {
          "n": n,
          "k": k,
          "group": label,
          "status": (
            "PASS"
            if not findings
            else "REVIEW"
          ),
          "findings": len(
            findings
          ),
        }
      )

  with (
    OUTPUT_DIR
    / "group_summary.csv"
  ).open(
    "w",
    encoding="utf-8",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "group",
        "status",
        "findings",
      ),
    )
    writer.writeheader()
    writer.writerows(
      group_rows
    )

  with (
    OUTPUT_DIR
    / "findings.csv"
  ).open(
    "w",
    encoding="utf-8",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "group",
        "kind",
        "detail",
      ),
    )
    writer.writeheader()
    writer.writerows(
      findings_rows
    )

  with (
    OUTPUT_DIR
    / "exceptions.csv"
  ).open(
    "w",
    encoding="utf-8",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "group",
        "exception_type",
        "message",
      ),
    )
    writer.writeheader()
    writer.writerows(
      exception_rows
    )

  review_groups = sum(
    1
    for row in group_rows
    if row[
      "status"
    ]
    == "REVIEW"
  )

  summary_lines = [
    "=" * 96,
    "Phase157-R20 repair49 - 112-group post-repair cross-audit",
    "=" * 96,
    "Production code changes: none",
    f"Range: n=2..15, k=0..7, depth={MAX_DEPTH}",
    f"Expected groups: {EXPECTED_GROUPS}",
    "",
    f"scanned groups: {scanned}",
    f"exceptions: {len(exception_rows)}",
    f"review groups: {review_groups}",
    f"total findings: {len(findings_rows)}",
    "",
    "Finding counts:",
  ]

  if finding_counter:
    for kind, count in sorted(
      finding_counter.items()
    ):
      summary_lines.append(
        f"  {kind}: {count}"
      )
  else:
    summary_lines.append(
      "  none"
    )

  summary_lines.extend(
    (
      "",
      "Output:",
      "  audit_output/group_summary.csv",
      "  audit_output/findings.csv",
      "  audit_output/exceptions.csv",
    )
  )

  summary = "\n".join(
    summary_lines
  )

  (
    OUTPUT_DIR
    / "summary.txt"
  ).write_text(
    summary
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    summary
  )

  if scanned != EXPECTED_GROUPS:
    print("")
    print(
      "AUDIT HARNESS ERROR: "
      "unexpected group count"
    )
    return 2

  print("")
  print(
    "AUDIT COMPLETE"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
