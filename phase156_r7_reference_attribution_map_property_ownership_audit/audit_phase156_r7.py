from __future__ import annotations

import argparse
import json
from pathlib import Path

from homotopy_groups import (
  TodaPrimaryGroup,
  TodaSuspensionIsomorphismStatement,
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
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_prop56_zero_bootstrap import (
  _build_prop51_step,
)
from toda_rules import (
  TodaHopfInvariantSurjectiveStatement,
)


def _pi6_presentation(
  depth: int,
):
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
    max_depth=depth,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def _reference_label(
  step,
) -> str | None:
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


def _rule_name(
  step,
) -> str | None:
  inference_rule = step.inference_rule

  if inference_rule is None:
    return None

  return inference_rule.name


def _step_record(
  presentation,
  step,
):
  node = next(
    node
    for node in presentation.nodes
    if node.proof_step is step
  )

  parents = tuple(
    edge.parent_step
    for edge in presentation.edges
    if edge.premise_step is step
  )
  premises = tuple(
    edge.premise_step
    for edge in presentation.edges
    if edge.parent_step is step
  )

  return {
    "depth": node.depth,
    "rendered": (
      _render_generic_narrative_step(
        step
      )
    ),
    "statement_type": type(
      step.conclusion
    ).__name__,
    "rule": _rule_name(
      step
    ),
    "reference": _reference_label(
      step
    ),
    "premises": [
      {
        "rendered": (
          _render_generic_narrative_step(
            premise
          )
        ),
        "rule": _rule_name(
          premise
        ),
        "reference": _reference_label(
          premise
        ),
      }
      for premise in premises
    ],
    "consumers": [
      {
        "rendered": (
          _render_generic_narrative_step(
            parent
          )
        ),
        "rule": _rule_name(
          parent
        ),
        "reference": _reference_label(
          parent
        ),
      }
      for parent in parents
    ],
  }


def _is_group_relation(
  step,
  group_dimension: int,
  sphere_dimension: int,
) -> bool:
  statement = step.conclusion

  return (
    isinstance(
      statement,
      Relation,
    )
    and statement.lhs
    == TodaPrimaryGroup(
      group_dimension=group_dimension,
      sphere_dimension=sphere_dimension,
    )
  )


def _find_unique(
  presentation,
  predicate,
  label: str,
):
  matches = tuple(
    node.proof_step
    for node in presentation.nodes
    if predicate(
      node.proof_step
    )
  )

  if len(
    matches
  ) != 1:
    raise RuntimeError(
      label
      + ": expected exactly one step, found "
      + str(
        len(
          matches
        )
      )
    )

  return matches[
    0
  ]


def _find_optional_unique(
  presentation,
  predicate,
  label: str,
):
  matches = tuple(
    node.proof_step
    for node in presentation.nodes
    if predicate(
      node.proof_step
    )
  )

  if len(
    matches
  ) > 1:
    raise RuntimeError(
      label
      + ": expected zero or one step, found "
      + str(
        len(
          matches
        )
      )
    )

  if not matches:
    return None

  return matches[
    0
  ]


def _reference_entries_record(
  presentation,
):
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )

  (
    filtered_entries,
    filtered_lines,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      entries,
      lines,
      presentation.root_step,
    )
  )

  return {
    "before_root_exclusion": [
      {
        "number": entry.number,
        "reference": (
          entry.reference.locator
          or entry.reference.label
        ),
        "statements": list(
          lines.get(
            entry.number,
            (),
          )
        ),
      }
      for entry in entries
    ],
    "after_root_exclusion": [
      {
        "number": entry.number,
        "reference": (
          entry.reference.locator
          or entry.reference.label
        ),
        "statements": list(
          filtered_lines.get(
            entry.number,
            (),
          )
        ),
      }
      for entry in filtered_entries
    ],
  }


def _prop51_higher_eta_record():
  prop51_step = _build_prop51_step()
  statement = prop51_step.conclusion
  higher = statement.higher_eta_group_relation

  return {
    "prop51_rule": _rule_name(
      prop51_step
    ),
    "prop51_reference": _reference_label(
      prop51_step
    ),
    "higher_eta_statement": repr(
      higher
    ),
    "higher_eta_group_dimension": repr(
      getattr(
        higher,
        "lhs",
        None,
      )
    ),
    "higher_eta_rendered_via_container": (
      _render_generic_narrative_step(
        prop51_step
      )
    ),
  }


def _print_step(
  title: str,
  record,
) -> None:
  print()
  print(
    "--- "
    + title
    + " ---"
  )
  print(
    "depth:",
    record[
      "depth"
    ],
  )
  print(
    "rendered:",
    record[
      "rendered"
    ],
  )
  print(
    "type:",
    record[
      "statement_type"
    ],
  )
  print(
    "rule:",
    record[
      "rule"
    ],
  )
  print(
    "reference:",
    record[
      "reference"
    ],
  )

  print(
    "premises:",
    len(
      record[
        "premises"
      ]
    ),
  )
  for index, premise in enumerate(
    record[
      "premises"
    ],
    start=1,
  ):
    print(
      "  P"
      + str(
        index
      )
      + ": "
      + premise[
        "rendered"
      ]
    )
    print(
      "      rule=",
      premise[
        "rule"
      ],
    )
    print(
      "      reference=",
      premise[
        "reference"
      ],
    )

  print(
    "consumers:",
    len(
      record[
        "consumers"
      ]
    ),
  )
  for index, consumer in enumerate(
    record[
      "consumers"
    ],
    start=1,
  ):
    print(
      "  C"
      + str(
        index
      )
      + ": "
      + consumer[
        "rendered"
      ]
    )
    print(
      "      rule=",
      consumer[
        "rule"
      ],
    )
    print(
      "      reference=",
      consumer[
        "reference"
      ],
    )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r7_audit_output"
    ),
  )
  args = parser.parse_args()
  args.output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  output = {
    "depths": {},
    "prop51": (
      _prop51_higher_eta_record()
    ),
  }

  for depth in (
    2,
    3,
  ):
    presentation = _pi6_presentation(
      depth
    )

    pi5_2 = _find_optional_unique(
      presentation,
      lambda step: _is_group_relation(
        step,
        5,
        2,
      ),
      "pi_5^2",
    )
    pi5_3 = _find_unique(
      presentation,
      lambda step: _is_group_relation(
        step,
        5,
        3,
      ),
      "pi_5^3",
    )
    pi6_5 = _find_unique(
      presentation,
      lambda step: _is_group_relation(
        step,
        6,
        5,
      ),
      "pi_6^5",
    )
    e_iso = _find_optional_unique(
      presentation,
      lambda step: (
        isinstance(
          step.conclusion,
          TodaSuspensionIsomorphismStatement,
        )
        and step.conclusion.map.source_group
        == TodaPrimaryGroup(
          group_dimension=4,
          sphere_dimension=2,
        )
        and step.conclusion.map.target_group
        == TodaPrimaryGroup(
          group_dimension=5,
          sphere_dimension=3,
        )
      ),
      "E: pi_4^2 -> pi_5^3 isomorphism",
    )
    h_surj = _find_unique(
      presentation,
      lambda step: isinstance(
        step.conclusion,
        TodaHopfInvariantSurjectiveStatement,
      ),
      "H: pi_6^3 -> pi_6^5 surjective",
    )

    depth_record = {
      "root": {
        "rendered": (
          _render_generic_narrative_step(
            presentation.root_step
          )
        ),
        "rule": _rule_name(
          presentation.root_step
        ),
        "reference": _reference_label(
          presentation.root_step
        ),
      },
      "references": (
        _reference_entries_record(
          presentation
        )
      ),
      "steps": {
        "pi5_2": (
          None
          if pi5_2 is None
          else _step_record(
            presentation,
            pi5_2,
          )
        ),
        "pi5_3": _step_record(
          presentation,
          pi5_3,
        ),
        "pi6_5": _step_record(
          presentation,
          pi6_5,
        ),
        "e_iso_pi4_2_to_pi5_3": (
          None
          if e_iso is None
          else _step_record(
            presentation,
            e_iso,
          )
        ),
        "h_surjective": _step_record(
          presentation,
          h_surj,
        ),
      },
    }

    output[
      "depths"
    ][
      str(
        depth
      )
    ] = depth_record

  depth2 = output[
    "depths"
  ][
    "2"
  ]
  depth3 = output[
    "depths"
  ][
    "3"
  ]

  findings = {
    "pi5_2_present_depth2": (
      depth2[
        "steps"
      ][
        "pi5_2"
      ]
      is not None
    ),
    "pi5_2_reference_is_prop56_if_present": (
      depth2[
        "steps"
      ][
        "pi5_2"
      ]
      is not None
      and depth2[
        "steps"
      ][
        "pi5_2"
      ][
        "reference"
      ]
      == "Proposition 5.6"
    ),
    "pi5_2_removed_by_root_reference_exclusion": (
      any(
        entry[
          "reference"
        ]
        == "Proposition 5.6"
        and any(
          r"\pi_{5}^{2}"
          in statement
          for statement in entry[
            "statements"
          ]
        )
        for entry in depth2[
          "references"
        ][
          "before_root_exclusion"
        ]
      )
      and not any(
        entry[
          "reference"
        ]
        == "Proposition 5.6"
        for entry in depth2[
          "references"
        ][
          "after_root_exclusion"
        ]
      )
    ),
    "pi6_5_current_reference_is_lemma54": (
      depth2[
        "steps"
      ][
        "pi6_5"
      ][
        "reference"
      ]
      == "Lemma 5.4"
    ),
    "pi5_3_current_reference_is_prop53": (
      depth2[
        "steps"
      ][
        "pi5_3"
      ][
        "reference"
      ]
      == "Proposition 5.3"
    ),
    "h_surjective_current_reference_is_prop53": (
      depth2[
        "steps"
      ][
        "h_surjective"
      ][
        "reference"
      ]
      == "Proposition 5.3"
    ),
    "e_iso_visible_by_depth3": (
      depth3[
        "steps"
      ][
        "e_iso_pi4_2_to_pi5_3"
      ]
      is not None
    ),
    "e_iso_current_reference_is_prop53_if_visible": (
      depth3[
        "steps"
      ][
        "e_iso_pi4_2_to_pi5_3"
      ]
      is not None
      and depth3[
        "steps"
      ][
        "e_iso_pi4_2_to_pi5_3"
      ][
        "reference"
      ]
      == "Proposition 5.3"
    ),
  }

  output[
    "findings"
  ] = findings

  (
    args.output_dir
    / "phase156_r7_audit.json"
  ).write_text(
    json.dumps(
      output,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  print(
    "=" * 86
  )
  print(
    "Phase156-R7 — Reference attribution + derived map-property ownership audit"
  )
  print(
    "=" * 86
  )
  print(
    "Production changes: none"
  )

  for depth in (
    "2",
    "3",
  ):
    record = output[
      "depths"
    ][
      depth
    ]
    print()
    print(
      "### pi_6^3 depth "
      + depth
    )
    print(
      "root:",
      record[
        "root"
      ],
    )

    print()
    print(
      "References before root exclusion:"
    )
    for entry in record[
      "references"
    ][
      "before_root_exclusion"
    ]:
      print(
        " ",
        entry,
      )

    print()
    print(
      "References after root exclusion:"
    )
    for entry in record[
      "references"
    ][
      "after_root_exclusion"
    ]:
      print(
        " ",
        entry,
      )

    for key, title in (
      (
        "pi5_2",
        "pi_5^2",
      ),
      (
        "pi5_3",
        "pi_5^3",
      ),
      (
        "pi6_5",
        "pi_6^5",
      ),
      (
        "e_iso_pi4_2_to_pi5_3",
        "E: pi_4^2 -> pi_5^3 isomorphism",
      ),
      (
        "h_surjective",
        "H: pi_6^3 -> pi_6^5 surjective",
      ),
    ):
      step_record = record[
        "steps"
      ][
        key
      ]

      if step_record is None:
        print()
        print(
          "--- "
          + title
          + " ---"
        )
        print(
          "not visible at this depth"
        )
        continue

      _print_step(
        title,
        step_record,
      )

  print()
  print(
    "### Proposition 5.1 aggregate inspection"
  )
  for key, value in output[
    "prop51"
  ].items():
    print(
      key
      + ":",
      value,
    )

  print()
  print(
    "### Findings"
  )
  for key, value in findings.items():
    print(
      key
      + ":",
      value,
    )

  print()
  print(
    "AUDIT COMPLETE"
  )
  print(
    "No production files changed."
  )
  print(
    "Repository-wide pytest is intentionally NOT run."
  )
  print(
    "=" * 86
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
