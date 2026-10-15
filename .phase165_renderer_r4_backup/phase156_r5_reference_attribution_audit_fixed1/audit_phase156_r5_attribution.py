from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  select_toda_group_proof_narrative_reference_statement_steps,
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


N_RANGE = range(2, 16)
K_RANGE = range(0, 8)
MAX_DEPTH = 2
EXPECTED_GROUPS = 112

CLASS_SINGLE_SOURCE = "single_source"
CLASS_COMPOSITE_REFERENCE = "composite_reference"
CLASS_COMPOSITE_CONSUMER_OVERLAP = (
  "composite_reference_contains_consumer_reference"
)
CLASS_COMPOSITE_CONSUMER_RULE_OVERLAP = (
  "composite_reference_contains_consumer_rule_reference"
)

KNOWN_PI6_REFERENCE = "(5.3) / Lemma 5.2"


def _group_label(
  n: int,
  k: int,
) -> str:
  return (
    "pi_"
    + str(
      n + k
    )
    + "^"
    + str(
      n
    )
  )


def _reference_title(
  reference,
) -> str:
  return (
    reference.locator
    or reference.label
  )


def _normalize_reference_token(
  text: str,
) -> str:
  normalized = text.strip()
  normalized = re.sub(
    r"^Toda\s+",
    "",
    normalized,
  )
  normalized = normalized.rstrip(
    "."
  )
  normalized = re.sub(
    r"\s+",
    " ",
    normalized,
  )
  return normalized


def split_reference_components(
  title: str,
) -> tuple[
  str,
  ...,
]:
  if not isinstance(
    title,
    str,
  ):
    raise TypeError(
      "title must be a str"
    )

  return tuple(
    component
    for component in (
      _normalize_reference_token(
        part
      )
      for part in title.split(
        "/"
      )
    )
    if component
  )


def _reference_component_in_text(
  component: str,
  text: str,
) -> bool:
  normalized_component = (
    _normalize_reference_token(
      component
    )
  )
  normalized_text = (
    _normalize_reference_token(
      text
    )
  )

  if not normalized_component:
    return False

  return (
    normalized_component
    in normalized_text
  )


def classify_reference_attribution(
  *,
  reference_title: str,
  consumer_reference_titles: tuple[
    str,
    ...,
  ],
  consumer_rule_names: tuple[
    str,
    ...,
  ],
) -> str:
  components = split_reference_components(
    reference_title
  )

  if len(
    components
  ) <= 1:
    return CLASS_SINGLE_SOURCE

  for consumer_title in consumer_reference_titles:
    if any(
      _reference_component_in_text(
        component,
        consumer_title,
      )
      for component in components
    ):
      return (
        CLASS_COMPOSITE_CONSUMER_OVERLAP
      )

  for rule_name in consumer_rule_names:
    if any(
      _reference_component_in_text(
        component,
        rule_name,
      )
      for component in components
    ):
      return (
        CLASS_COMPOSITE_CONSUMER_RULE_OVERLAP
      )

  return CLASS_COMPOSITE_REFERENCE


def _candidate_steps(
  entry,
) -> tuple:
  candidates = []
  seen_rendered = set()

  for proof_step in entry.proof_steps:
    rendered_statement = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not (
      _is_toda_group_proof_narrative_reference_statement_candidate(
        proof_step,
        rendered_statement,
      )
    ):
      continue

    if rendered_statement in seen_rendered:
      continue

    seen_rendered.add(
      rendered_statement
    )
    candidates.append(
      proof_step
    )

  return tuple(
    candidates
  )


def _external_consumers(
  presentation,
  entry,
  proof_step,
) -> tuple:
  entry_step_ids = {
    id(
      step
    )
    for step in entry.proof_steps
  }

  return tuple(
    edge.parent_step
    for edge in presentation.edges
    if (
      edge.premise_step is proof_step
      and id(
        edge.parent_step
      )
      not in entry_step_ids
    )
  )


def _consumer_reference_titles(
  consumers,
) -> tuple[
  str,
  ...,
]:
  result = []
  seen = set()

  for consumer in consumers:
    reference = (
      extract_toda_group_proof_step_literature_reference(
        consumer
      )
    )

    if reference is None:
      continue

    title = _reference_title(
      reference
    )

    if title in seen:
      continue

    seen.add(
      title
    )
    result.append(
      title
    )

  return tuple(
    result
  )


def _consumer_rule_names(
  consumers,
) -> tuple[
  str,
  ...,
]:
  result = []
  seen = set()

  for consumer in consumers:
    inference_rule = (
      consumer.inference_rule
    )

    if inference_rule is None:
      continue

    name = inference_rule.name

    if name in seen:
      continue

    seen.add(
      name
    )
    result.append(
      name
    )

  return tuple(
    result
  )


def _write_csv(
  path: Path,
  fieldnames: tuple[
    str,
    ...,
  ],
  rows: list[
    dict[
      str,
      object,
    ]
  ],
) -> None:
  with path.open(
    "w",
    encoding="utf-8-sig",
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


def run_audit(
  output_dir: Path,
) -> dict[
  str,
  object,
]:
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  groups_seen = 0
  exceptions = []
  rows = []
  group_rows = []
  classification_counts = Counter()
  classification_groups = defaultdict(
    set
  )
  known_pi6_defect_detected = False

  for n in N_RANGE:
    for k in K_RANGE:
      groups_seen += 1
      group = _group_label(
        n,
        k,
      )
      group_selected = 0
      group_composite = 0

      try:
        report = build_standard_toda_report(
          n=n,
          k=k,
        )

        if not report.candidates:
          raise AssertionError(
            "no report candidate for n="
            + str(
              n
            )
            + ", k="
            + str(
              k
            )
          )

        group_result = (
          report.candidates[
            0
          ].source_candidate.group_result
        )
        replay = (
          build_toda_group_result_proof_replay(
            group_result,
            max_depth=MAX_DEPTH,
          )
        )
        raw_presentation = (
          build_toda_group_proof_presentation(
            replay
          )
        )
        presentation = (
          build_toda_group_proof_narrative_semantic_closure_presentation(
            raw_presentation
          )
        )
        entries = (
          build_toda_group_proof_narrative_reference_entries(
            presentation
          )
        )

        for entry in entries:
          candidates = _candidate_steps(
            entry
          )
          selected = (
            select_toda_group_proof_narrative_reference_statement_steps(
              entry,
              candidates,
              presentation.edges,
              root_step=presentation.root_step,
            )
          )

          for proof_step in selected:
            group_selected += 1
            reference_title = (
              _reference_title(
                entry.reference
              )
            )
            consumers = (
              _external_consumers(
                presentation,
                entry,
                proof_step,
              )
            )
            consumer_reference_titles = (
              _consumer_reference_titles(
                consumers
              )
            )
            consumer_rule_names = (
              _consumer_rule_names(
                consumers
              )
            )
            classification = (
              classify_reference_attribution(
                reference_title=reference_title,
                consumer_reference_titles=(
                  consumer_reference_titles
                ),
                consumer_rule_names=(
                  consumer_rule_names
                ),
              )
            )

            classification_counts[
              classification
            ] += 1
            classification_groups[
              classification
            ].add(
              group
            )

            if classification != CLASS_SINGLE_SOURCE:
              group_composite += 1

            rendered_statement = (
              _render_generic_narrative_step(
                proof_step
              )
            )

            if (
              group
              == "pi_6^3"
              and reference_title
              == KNOWN_PI6_REFERENCE
            ):
              known_pi6_defect_detected = True

            rows.append(
              {
                "n": n,
                "k": k,
                "group": group,
                "reference_number": entry.number,
                "reference_title": reference_title,
                "reference_components": (
                  " || ".join(
                    split_reference_components(
                      reference_title
                    )
                  )
                ),
                "classification": classification,
                "statement": rendered_statement,
                "external_consumer_count": len(
                  consumers
                ),
                "consumer_reference_titles": (
                  " || ".join(
                    consumer_reference_titles
                  )
                ),
                "consumer_rule_names": (
                  " || ".join(
                    consumer_rule_names
                  )
                ),
              }
            )

        group_rows.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "selected_reference_statements": (
              group_selected
            ),
            "composite_reference_statements": (
              group_composite
            ),
          }
        )

      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "exception_type": type(
              exc
            ).__name__,
            "exception_message": str(
              exc
            ),
          }
        )

  suspicious_classes = (
    CLASS_COMPOSITE_REFERENCE,
    CLASS_COMPOSITE_CONSUMER_OVERLAP,
    CLASS_COMPOSITE_CONSUMER_RULE_OVERLAP,
  )
  suspicious_rows = [
    row
    for row in rows
    if row[
      "classification"
    ]
    in suspicious_classes
  ]

  summary_rows = [
    {
      "classification": classification,
      "occurrences": classification_counts.get(
        classification,
        0,
      ),
      "affected_groups": len(
        classification_groups.get(
          classification,
          set(),
        )
      ),
    }
    for classification in (
      CLASS_SINGLE_SOURCE,
      *suspicious_classes,
    )
  ]

  _write_csv(
    output_dir
    / "phase156_r5_attribution_all_selected_statements.csv",
    (
      "n",
      "k",
      "group",
      "reference_number",
      "reference_title",
      "reference_components",
      "classification",
      "statement",
      "external_consumer_count",
      "consumer_reference_titles",
      "consumer_rule_names",
    ),
    rows,
  )

  _write_csv(
    output_dir
    / "phase156_r5_attribution_suspicious.csv",
    (
      "n",
      "k",
      "group",
      "reference_number",
      "reference_title",
      "reference_components",
      "classification",
      "statement",
      "external_consumer_count",
      "consumer_reference_titles",
      "consumer_rule_names",
    ),
    suspicious_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r5_attribution_group_summary.csv",
    (
      "n",
      "k",
      "group",
      "selected_reference_statements",
      "composite_reference_statements",
    ),
    group_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r5_attribution_classification_summary.csv",
    (
      "classification",
      "occurrences",
      "affected_groups",
    ),
    summary_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r5_attribution_exceptions.csv",
    (
      "n",
      "k",
      "group",
      "exception_type",
      "exception_message",
    ),
    exceptions,
  )

  passed = (
    groups_seen
    == EXPECTED_GROUPS
    and not exceptions
    and known_pi6_defect_detected
  )

  payload = {
    "phase": "Phase156-R5 Reference attribution audit",
    "production_changes": False,
    "scope": {
      "n": "2..15",
      "k": "0..7",
      "depth": MAX_DEPTH,
      "expected_groups": EXPECTED_GROUPS,
    },
    "groups_seen": groups_seen,
    "exceptions": len(
      exceptions
    ),
    "selected_reference_statements": len(
      rows
    ),
    "suspicious_reference_statements": len(
      suspicious_rows
    ),
    "classification_counts": {
      row[
        "classification"
      ]: row[
        "occurrences"
      ]
      for row in summary_rows
    },
    "classification_affected_groups": {
      row[
        "classification"
      ]: row[
        "affected_groups"
      ]
      for row in summary_rows
    },
    "known_pi6_defect_detected": (
      known_pi6_defect_detected
    ),
    "pass": passed,
    "repair_boundary": (
      "This audit only identifies attribution candidates. "
      "Production literature_reference metadata must be repaired "
      "only after the cross-group population is reviewed."
    ),
  }

  (
    output_dir
    / "phase156_r5_attribution_result.json"
  ).write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  summary = [
    "=" * 78,
    "Phase156-R5 — Reference attribution audit",
    "=" * 78,
    "production changes: none",
    "scope: n=2..15, k=0..7, depth=2",
    "",
    "groups: "
    + str(
      groups_seen
    ),
    "exceptions: "
    + str(
      len(
        exceptions
      )
    ),
    "selected Reference statements: "
    + str(
      len(
        rows
      )
    ),
    "suspicious composite Reference statements: "
    + str(
      len(
        suspicious_rows
      )
    ),
    "known pi_6^3 attribution defect detected: "
    + str(
      known_pi6_defect_detected
    ),
    "",
    "Classification:",
  ]

  for row in summary_rows:
    summary.append(
      "  "
      + str(
        row[
          "classification"
        ]
      )
      + ": occurrences="
      + str(
        row[
          "occurrences"
        ]
      )
      + ", affected_groups="
      + str(
        row[
          "affected_groups"
        ]
      )
    )

  summary.extend(
    [
      "",
      "Interpretation:",
      (
        "  single_source: the displayed Reference has one literature "
        "locator."
      ),
      (
        "  composite_reference: the displayed Reference combines two or "
        "more literature locators and requires ownership review."
      ),
      (
        "  composite_reference_contains_consumer_reference: one component "
        "of the composite Reference also appears as an external consumer "
        "Reference."
      ),
      (
        "  composite_reference_contains_consumer_rule_reference: one "
        "component also appears in an external consumer rule name; this "
        "is the strongest signal that an application theorem/lemma has "
        "been mixed into the premise source attribution."
      ),
      "",
      "R5 boundary:",
      (
        "  No production code or proof data is changed by this audit."
      ),
      (
        "  The next repair step must use the suspicious CSV to separate "
        "premise source attribution from theorem/lemma application "
        "attribution by a general rule."
      ),
      "=" * 78,
    ]
  )

  summary_text = "\n".join(
    summary
  ) + "\n"

  (
    output_dir
    / "phase156_r5_attribution_summary.txt"
  ).write_text(
    summary_text,
    encoding="utf-8",
  )

  print(
    summary_text
  )

  return payload


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_attribution_audit_output"
    ),
  )
  args = parser.parse_args()

  result = run_audit(
    args.output_dir
  )

  if result[
    "pass"
  ]:
    print(
      "PASS: 112-group attribution population reproduced and "
      "the known pi_6^3 defect was detected."
    )
    return 0

  print(
    "FAIL: attribution audit population or known-defect detection "
    "is incomplete."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
