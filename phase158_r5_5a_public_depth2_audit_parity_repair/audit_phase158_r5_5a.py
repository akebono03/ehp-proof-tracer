from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  WebGroupProofRenderedLineView,
  build_standard_web_group_proof_view,
)


MAX_DEPTH = 2

TARGETS = (
  (
    "pi6_3_reference",
    3,
    3,
  ),
  (
    "pi8_5_former_dedicated",
    5,
    3,
  ),
  (
    "pi15_8_former_dedicated",
    8,
    7,
  ),
  (
    "pi7_4_former_legacy",
    4,
    3,
  ),
  (
    "pi10_4_generic",
    4,
    6,
  ),
  (
    "pi11_4_prose_target",
    4,
    7,
  ),
  (
    "pi12_5_generic",
    5,
    7,
  ),
  (
    "pi16_9_generic",
    9,
    7,
  ),
  (
    "pi4_3_small_unstable",
    3,
    1,
  ),
)

OUTPUT_DIR = (
  Path(__file__).resolve().parent
  / "audit_output"
)

REFERENCE_PREFIX_RE = re.compile(
  r"^\[R\d+\](?:(?:より)|(?:を用いて)|(?:を用いる))?"
  r"[\s,、.。]*"
)

TRAILING_PUNCTUATION = (
  ".",
  "。",
  ",",
  "、",
)


@dataclass(frozen=True)
class VisibleStep:
  replay_index: int
  proof_step: object
  rendered: str
  body_index: int


@dataclass(frozen=True)
class DerivationFinding:
  kind: str
  premise_index: int
  consumer_index: int
  premise_text: str
  consumer_text: str


def render_web_line(
  line: WebGroupProofRenderedLineView,
) -> str:
  if line.kind == "heading":
    return "## " + line.prefix

  if line.kind == "separator":
    return "---"

  parts = []

  for segment in line.segments:
    if segment.kind == "text":
      parts.append(
        segment.value
      )
    elif segment.kind == "strong":
      parts.append(
        "**"
        + segment.value
        + "**"
      )
    elif segment.kind == "inline_math":
      parts.append(
        "$"
        + segment.value
        + "$"
      )
    elif segment.kind == "display_math":
      parts.append(
        "$"
        + segment.value
        + "$"
      )
    else:
      raise ValueError(
        "unsupported inline segment kind: "
        + segment.kind
      )

  if parts:
    return "".join(
      parts
    )

  if line.statement_latex is not None:
    return (
      line.prefix
      + "$"
      + line.statement_latex
      + "$"
      + line.suffix
    )

  return (
    line.prefix
    + line.suffix
  )


def normalize_visible_text(
  text: str,
) -> str:
  normalized = " ".join(
    text.strip().split()
  )

  normalized = REFERENCE_PREFIX_RE.sub(
    "",
    normalized,
    count=1,
  )

  while (
    normalized
    and normalized[
      -1
    ] in TRAILING_PUNCTUATION
  ):
    normalized = normalized[
      :-1
    ].rstrip()

  return normalized


def is_reference_use_line(
  text: str,
) -> bool:
  stripped = text.strip()

  return (
    stripped.startswith(
      "[R"
    )
    and (
      "]より" in stripped
      or "]を用いて" in stripped
      or "]を用いる" in stripped
    )
  )


def is_standalone_connector(
  text: str,
) -> bool:
  return normalize_visible_text(
    text
  ) in {
    "以上より",
    "したがって",
    "これより",
    "これらより",
  }


def proof_body_lines(
  rendered_lines: tuple[
    WebGroupProofRenderedLineView,
    ...,
  ],
) -> tuple[
  str,
  ...,
]:
  in_proof = False
  body = []

  for line in rendered_lines:
    if (
      line.kind == "heading"
      and line.prefix == "証明"
    ):
      in_proof = True
      continue

    if not in_proof:
      continue

    body.append(
      render_web_line(
        line
      )
    )

  return tuple(
    text
    for text in body
    if text.strip()
  )


def rendered_step_key(
  proof_step,
) -> str | None:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  if not rendered:
    return None

  return normalize_visible_text(
    rendered
  )


def build_body_key_positions(
  body_lines: tuple[
    str,
    ...,
  ],
) -> dict[
  str,
  tuple[
    int,
    ...,
  ],
]:
  positions = {}

  for index, line in enumerate(
    body_lines
  ):
    key = normalize_visible_text(
      line
    )

    if not key:
      continue

    positions.setdefault(
      key,
      [],
    ).append(
      index
    )

  return {
    key: tuple(
      indices
    )
    for key, indices in positions.items()
  }


def visible_steps_for_replay(
  replay,
  body_lines: tuple[
    str,
    ...,
  ],
) -> tuple[
  tuple[
    VisibleStep,
    ...,
  ],
  tuple[
    tuple[
      int,
      str,
      tuple[
        int,
        ...,
      ],
    ],
    ...,
  ],
]:
  positions_by_key = (
    build_body_key_positions(
      body_lines
    )
  )
  visible = []
  ambiguous = []

  for replay_index, replay_step in enumerate(
    replay.steps
  ):
    rendered = (
      _render_generic_narrative_step(
        replay_step.proof_step
      )
    )

    if not rendered:
      continue

    key = normalize_visible_text(
      rendered
    )
    positions = positions_by_key.get(
      key,
      (),
    )

    if len(
      positions
    ) == 1:
      visible.append(
        VisibleStep(
          replay_index=replay_index,
          proof_step=replay_step.proof_step,
          rendered=rendered,
          body_index=positions[
            0
          ],
        )
      )
    elif len(
      positions
    ) > 1:
      ambiguous.append(
        (
          replay_index,
          rendered,
          positions,
        )
      )

  return (
    tuple(
      visible
    ),
    tuple(
      ambiguous
    ),
  )


def direct_derivation_findings(
  visible_steps: tuple[
    VisibleStep,
    ...,
  ],
) -> tuple[
  DerivationFinding,
  ...,
]:
  visible_by_id = {
    id(
      item.proof_step
    ): item
    for item in visible_steps
  }
  findings = []

  for consumer in visible_steps:
    for premise in consumer.proof_step.premises:
      premise_visible = visible_by_id.get(
        id(
          premise
        )
      )

      if premise_visible is None:
        continue

      if (
        premise_visible.body_index
        < consumer.body_index
      ):
        kind = (
          "ORDERED_VISIBLE_DERIVATION"
        )
      else:
        kind = (
          "OUT_OF_ORDER_DERIVATION"
        )

      findings.append(
        DerivationFinding(
          kind=kind,
          premise_index=(
            premise_visible.body_index
          ),
          consumer_index=(
            consumer.body_index
          ),
          premise_text=(
            premise_visible.rendered
          ),
          consumer_text=(
            consumer.rendered
          ),
        )
      )

  return tuple(
    findings
  )


def reference_use_mapping(
  replay,
  body_lines: tuple[
    str,
    ...,
  ],
) -> tuple[
  tuple[
    int,
    str,
    str,
  ],
  ...,
]:
  step_keys = {}

  for replay_step in replay.steps:
    key = rendered_step_key(
      replay_step.proof_step
    )

    if not key:
      continue

    step_keys.setdefault(
      key,
      type(
        replay_step.proof_step.conclusion
      ).__name__,
    )

  rows = []

  for index, line in enumerate(
    body_lines
  ):
    if not is_reference_use_line(
      line
    ):
      continue

    key = normalize_visible_text(
      line
    )

    statement_type = step_keys.get(
      key,
      "",
    )

    rows.append(
      (
        index,
        line,
        statement_type,
      )
    )

  return tuple(
    rows
  )


def audit_target(
  label: str,
  n: int,
  k: int,
):
  view = (
    build_standard_web_group_proof_view(
      n,
      k,
      max_depth=MAX_DEPTH,
      mode="narrative",
    )
  )

  if view.mode != "narrative":
    raise AssertionError(
      "public view mode drifted from narrative"
    )

  if view.max_depth != MAX_DEPTH:
    raise AssertionError(
      "public view depth drifted from 2"
    )

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

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=MAX_DEPTH,
    )
  )

  body_lines = proof_body_lines(
    view.rendered_lines
  )

  (
    visible_steps,
    ambiguous_steps,
  ) = visible_steps_for_replay(
    replay,
    body_lines,
  )

  derivations = (
    direct_derivation_findings(
      visible_steps
    )
  )

  reference_rows = (
    reference_use_mapping(
      replay,
      body_lines,
    )
  )

  standalone = tuple(
    (
      index,
      line,
    )
    for index, line in enumerate(
      body_lines
    )
    if is_standalone_connector(
      line
    )
  )

  return {
    "label": label,
    "n": n,
    "k": k,
    "group": f"pi_{n + k}^{n}",
    "view": view,
    "body_lines": body_lines,
    "visible_steps": visible_steps,
    "ambiguous_steps": ambiguous_steps,
    "derivations": derivations,
    "reference_rows": reference_rows,
    "standalone": standalone,
  }


def write_rendered_snapshot(
  target,
) -> None:
  rendered_dir = (
    OUTPUT_DIR
    / "rendered"
  )
  rendered_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  path = (
    rendered_dir
    / (
      target[
        "label"
      ]
      + ".txt"
    )
  )

  lines = [
    (
      f"{index:03d}: {line}"
    )
    for index, line in enumerate(
      target[
        "body_lines"
      ]
    )
  ]

  path.write_text(
    "\n".join(
      lines
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  summary_rows = []
  derivation_rows = []
  reference_rows = []
  ambiguous_rows = []
  connector_rows = []
  exception_rows = []
  category_counts = Counter()

  for label, n, k in TARGETS:
    try:
      target = audit_target(
        label,
        n,
        k,
      )
    except Exception as exc:
      exception_rows.append(
        {
          "label": label,
          "n": n,
          "k": k,
          "exception_type": type(
            exc
          ).__name__,
          "message": str(
            exc
          ),
        }
      )
      continue

    write_rendered_snapshot(
      target
    )

    out_of_order = 0
    ordered = 0

    for item in target[
      "derivations"
    ]:
      category_counts[
        item.kind
      ] += 1

      if (
        item.kind
        == "OUT_OF_ORDER_DERIVATION"
      ):
        out_of_order += 1
      else:
        ordered += 1

      derivation_rows.append(
        {
          "label": label,
          "group": target[
            "group"
          ],
          "kind": item.kind,
          "premise_index": (
            item.premise_index
          ),
          "consumer_index": (
            item.consumer_index
          ),
          "premise_text": (
            item.premise_text
          ),
          "consumer_text": (
            item.consumer_text
          ),
        }
      )

    unmapped_reference = 0

    for (
      body_index,
      rendered,
      statement_type,
    ) in target[
      "reference_rows"
    ]:
      if statement_type:
        kind = (
          "MAPPED_REFERENCE_PROSE"
        )
      else:
        kind = (
          "UNMAPPED_RENDERED_USE"
        )
        unmapped_reference += 1

      category_counts[
        kind
      ] += 1

      reference_rows.append(
        {
          "label": label,
          "group": target[
            "group"
          ],
          "kind": kind,
          "body_index": body_index,
          "statement_type": (
            statement_type
          ),
          "rendered": rendered,
        }
      )

    for (
      replay_index,
      rendered,
      positions,
    ) in target[
      "ambiguous_steps"
    ]:
      category_counts[
        "AMBIGUOUS_STEP_MAPPING"
      ] += 1
      ambiguous_rows.append(
        {
          "label": label,
          "group": target[
            "group"
          ],
          "replay_index": (
            replay_index
          ),
          "rendered": rendered,
          "positions": repr(
            positions
          ),
        }
      )

    for (
      body_index,
      rendered,
    ) in target[
      "standalone"
    ]:
      category_counts[
        "STANDALONE_CONNECTOR"
      ] += 1
      connector_rows.append(
        {
          "label": label,
          "group": target[
            "group"
          ],
          "body_index": body_index,
          "rendered": rendered,
        }
      )

    summary_rows.append(
      {
        "label": label,
        "n": n,
        "k": k,
        "group": target[
          "group"
        ],
        "body_lines": len(
          target[
            "body_lines"
          ]
        ),
        "visible_steps": len(
          target[
            "visible_steps"
          ]
        ),
        "ordered_derivations": (
          ordered
        ),
        "out_of_order_derivations": (
          out_of_order
        ),
        "mapped_reference_prose": (
          sum(
            1
            for (
              _,
              _,
              statement_type,
            ) in target[
              "reference_rows"
            ]
            if statement_type
          )
        ),
        "unmapped_reference_prose": (
          unmapped_reference
        ),
        "ambiguous_step_mappings": len(
          target[
            "ambiguous_steps"
          ]
        ),
        "standalone_connectors": len(
          target[
            "standalone"
          ]
        ),
      }
    )

  def write_csv(
    filename,
    fieldnames,
    rows,
  ):
    with (
      OUTPUT_DIR
      / filename
    ).open(
      "w",
      encoding="utf-8",
      newline="",
    ) as handle:
      writer = csv.DictWriter(
        handle,
        fieldnames=fieldnames,
      )
      writer.writeheader()
      writer.writerows(
        rows
      )

  write_csv(
    "summary.csv",
    (
      "label",
      "n",
      "k",
      "group",
      "body_lines",
      "visible_steps",
      "ordered_derivations",
      "out_of_order_derivations",
      "mapped_reference_prose",
      "unmapped_reference_prose",
      "ambiguous_step_mappings",
      "standalone_connectors",
    ),
    summary_rows,
  )

  write_csv(
    "derivations.csv",
    (
      "label",
      "group",
      "kind",
      "premise_index",
      "consumer_index",
      "premise_text",
      "consumer_text",
    ),
    derivation_rows,
  )

  write_csv(
    "reference_prose.csv",
    (
      "label",
      "group",
      "kind",
      "body_index",
      "statement_type",
      "rendered",
    ),
    reference_rows,
  )

  write_csv(
    "ambiguous_mappings.csv",
    (
      "label",
      "group",
      "replay_index",
      "rendered",
      "positions",
    ),
    ambiguous_rows,
  )

  write_csv(
    "standalone_connectors.csv",
    (
      "label",
      "group",
      "body_index",
      "rendered",
    ),
    connector_rows,
  )

  write_csv(
    "exceptions.csv",
    (
      "label",
      "n",
      "k",
      "exception_type",
      "message",
    ),
    exception_rows,
  )

  details = [
    "=" * 96,
    "Phase 158-R5-5a — Public depth=2 audit parity repair",
    "=" * 96,
    "",
    "Production code changes: none",
    "Test code changes: none",
    "Public output source:",
    "  build_standard_web_group_proof_view(..., max_depth=2, mode='narrative')",
    "",
    "Ordering contract:",
    "  premise position < consumer position",
    "",
  ]

  for row in summary_rows:
    details.extend(
      (
        "-" * 96,
        (
          f"{row['label']}: "
          f"{row['group']}"
        ),
        "-" * 96,
        (
          "ordered_derivations: "
          f"{row['ordered_derivations']}"
        ),
        (
          "out_of_order_derivations: "
          f"{row['out_of_order_derivations']}"
        ),
        (
          "mapped_reference_prose: "
          f"{row['mapped_reference_prose']}"
        ),
        (
          "unmapped_reference_prose: "
          f"{row['unmapped_reference_prose']}"
        ),
        (
          "ambiguous_step_mappings: "
          f"{row['ambiguous_step_mappings']}"
        ),
        (
          "standalone_connectors: "
          f"{row['standalone_connectors']}"
        ),
        "",
      )
    )

    for item in derivation_rows:
      if (
        item[
          "label"
        ]
        != row[
          "label"
        ]
      ):
        continue

      if (
        item[
          "kind"
        ]
        != "OUT_OF_ORDER_DERIVATION"
      ):
        continue

      details.extend(
        (
          "[OUT_OF_ORDER_DERIVATION]",
          (
            "premise_index: "
            f"{item['premise_index']}"
          ),
          (
            "consumer_index: "
            f"{item['consumer_index']}"
          ),
          (
            "premise: "
            f"{item['premise_text']}"
          ),
          (
            "consumer: "
            f"{item['consumer_text']}"
          ),
          "",
        )
      )

    for item in reference_rows:
      if (
        item[
          "label"
        ]
        != row[
          "label"
        ]
      ):
        continue

      if (
        item[
          "kind"
        ]
        != "UNMAPPED_RENDERED_USE"
      ):
        continue

      details.extend(
        (
          "[UNMAPPED_RENDERED_USE]",
          (
            "body_index: "
            f"{item['body_index']}"
          ),
          (
            "rendered: "
            f"{item['rendered']}"
          ),
          "",
        )
      )

  (
    OUTPUT_DIR
    / "details.txt"
  ).write_text(
    "\n".join(
      details
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  summary = [
    "=" * 96,
    "Phase 158-R5-5a — Public depth=2 audit parity repair",
    "=" * 96,
    f"targets: {len(TARGETS)}",
    f"rendered: {len(summary_rows)}",
    f"exceptions: {len(exception_rows)}",
    "",
    "Categories:",
  ]

  for kind in (
    "ORDERED_VISIBLE_DERIVATION",
    "OUT_OF_ORDER_DERIVATION",
    "MAPPED_REFERENCE_PROSE",
    "UNMAPPED_RENDERED_USE",
    "AMBIGUOUS_STEP_MAPPING",
    "STANDALONE_CONNECTOR",
  ):
    summary.append(
      (
        f"  {kind}: "
        f"{category_counts[kind]}"
      )
    )

  summary.extend(
    (
      "",
      "Interpretation:",
      (
        "  Public Narrative is read from the same web adapter "
        "used by the actual depth=2 route."
      ),
      (
        "  A visible direct proof dependency is valid only when "
        "its premise is rendered before its consumer."
      ),
      (
        "  Reference-prefixed prose is normalized before mapping "
        "back to the depth=2 replay step."
      ),
      "",
      "Boundary:",
      "  Audit only. No production repair is performed.",
      (
        "  R5-5b may repair only confirmed general ordering defects "
        "reported by this audit."
      ),
      "",
      "Output:",
      "  audit_output/summary.txt",
      "  audit_output/details.txt",
      "  audit_output/summary.csv",
      "  audit_output/derivations.csv",
      "  audit_output/reference_prose.csv",
      "  audit_output/ambiguous_mappings.csv",
      "  audit_output/standalone_connectors.csv",
      "  audit_output/exceptions.csv",
      "  audit_output/rendered/*.txt",
      "=" * 96,
    )
  )

  (
    OUTPUT_DIR
    / "summary.txt"
  ).write_text(
    "\n".join(
      summary
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    "\n".join(
      summary
    )
  )

  if exception_rows:
    return 1

  if len(
    summary_rows
  ) != len(
    TARGETS
  ):
    return 2

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
