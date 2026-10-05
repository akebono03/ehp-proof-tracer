from __future__ import annotations

import inspect
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
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
  _phase153_r3_10_connect_public_reference_section,
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
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)


def _build_data():
  report = build_standard_toda_report(
    n=8,
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


def _parse_public(
  rendered: str,
):
  reference_marker = "\n## 使用する結果\n"
  proof_marker = "\n## 証明\n"

  if reference_marker not in rendered:
    raise RuntimeError(
      "public Reference section is missing"
    )

  if proof_marker not in rendered:
    raise RuntimeError(
      "public proof section is missing"
    )

  tail = rendered.split(
    reference_marker,
    1,
  )[1]
  reference_section, body = tail.split(
    proof_marker,
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
    for match in re.finditer(
      r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*",
      reference_section,
    )
  )

  body_markers = tuple(
    int(
      match.group(
        1
      )
    )
    for match in re.finditer(
      r"\[R([0-9]+)\]",
      body,
    )
  )

  return (
    reference_section,
    body,
    headers,
    body_markers,
  )


def _boundary_summary(
  step,
):
  boundary = classify_toda_literature_statement_step(
    step
  )

  if boundary is None:
    return None

  return {
    "classification": boundary.classification.value,
    "reference_locator": boundary.reference_locator,
    "component_key": boundary.component_key,
  }


def _filtered_entry_for_pi14_7(
  prop515_entry: TodaGroupProofNarrativeReferenceEntry,
) -> TodaGroupProofNarrativeReferenceEntry:
  retained_steps = tuple(
    step
    for step in prop515_entry.proof_steps
    if (
      (
        boundary := classify_toda_literature_statement_step(
          step
        )
      )
      is not None
      and boundary.classification.value
      == "fixed_statement"
      and boundary.reference_locator
      == "Proposition 5.15"
      and boundary.component_key
      == "pi14_7_group_relation"
    )
  )

  if len(
    retained_steps
  ) != 1:
    raise RuntimeError(
      "expected exactly one Proposition 5.15 "
      "pi14_7 fixed component, found "
      + str(
        len(
          retained_steps
        )
      )
    )

  return TodaGroupProofNarrativeReferenceEntry(
    number=prop515_entry.number,
    reference=prop515_entry.reference,
    proof_steps=retained_steps,
  )


def main() -> int:
  (
    presentation,
    rendered,
  ) = _build_data()

  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  raw_statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )

  prop515_entry = next(
    (
      entry
      for entry in entries
      if entry.reference.locator
      == "Proposition 5.15"
    ),
    None,
  )
  prop44_entry = next(
    (
      entry
      for entry in entries
      if entry.reference.locator
      == "Proposition 4.4"
    ),
    None,
  )

  if prop515_entry is None:
    raise RuntimeError(
      "Proposition 5.15 graph entry is missing"
    )

  if prop44_entry is None:
    raise RuntimeError(
      "Proposition 4.4 graph entry is missing"
    )

  pi14_entry = _filtered_entry_for_pi14_7(
    prop515_entry
  )
  aligned_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      (
        pi14_entry,
        prop44_entry,
      ),
    )
  )

  (
    reference_section,
    body,
    headers,
    body_markers,
  ) = _parse_public(
    rendered
  )

  connector_source = inspect.getsource(
    _phase153_r3_10_connect_public_reference_section
  )

  print(
    "=" * 104
  )
  print(
    "Phase157-R20 repair53-r6 - post-r5 internal alignment closure audit"
  )
  print(
    "=" * 104
  )
  print(
    "Production code changes: none"
  )
  print(
    "Test changes: none"
  )
  print(
    "Repository-wide pytest: not run"
  )
  print()

  print(
    "R5 CONNECTOR SENTINELS"
  )
  print(
    "-" * 104
  )
  print(
    "pi14 linkage sentinel:",
    (
      "pi_14^7 finite cyclic"
      in connector_source
    ),
  )
  print(
    "post-filter statement refresh sentinel:",
    (
      "filtered_reference_entries"
      in connector_source
      and (
        "_toda_group_proof_narrative_reference_statement_lines_by_number"
        in connector_source
      )
    ),
  )

  print()
  print(
    "PROPOSITION 5.15 GRAPH STEPS"
  )
  print(
    "-" * 104
  )

  for index, step in enumerate(
    prop515_entry.proof_steps,
    start=1,
  ):
    print(
      {
        "step_index": index,
        "conclusion_type": type(
          step.conclusion
        ).__name__,
        "rule": (
          step.inference_rule.name
          if step.inference_rule is not None
          else None
        ),
        "boundary": _boundary_summary(
          step
        ),
      }
    )

  print()
  print(
    "RAW STATEMENT LINES BEFORE COMPONENT FILTER"
  )
  print(
    "-" * 104
  )
  print(
    {
      "Proposition 5.15": raw_statement_lines.get(
        prop515_entry.number,
        (),
      ),
      "Proposition 4.4": raw_statement_lines.get(
        prop44_entry.number,
        (),
      ),
    }
  )

  print()
  print(
    "POST-FILTER INTERNAL ALIGNMENT"
  )
  print(
    "-" * 104
  )

  pi14_step = pi14_entry.proof_steps[
    0
  ]
  pi14_boundary = classify_toda_literature_statement_step(
    pi14_step
  )
  pi14_lines = aligned_lines.get(
    pi14_entry.number,
    (),
  )

  print(
    {
      "locator": pi14_entry.reference.locator,
      "remaining_step_type": type(
        pi14_step.conclusion
      ).__name__,
      "remaining_rule": (
        pi14_step.inference_rule.name
        if pi14_step.inference_rule is not None
        else None
      ),
      "boundary": _boundary_summary(
        pi14_step
      ),
      "statement_lines": pi14_lines,
    }
  )

  print()
  print(
    "PUBLIC REFERENCE"
  )
  print(
    "-" * 104
  )
  print(
    "headers:",
    headers,
  )
  print(
    reference_section.strip()
  )

  print()
  print(
    "PUBLIC PROOF BODY"
  )
  print(
    "-" * 104
  )
  print(
    "body markers:",
    body_markers,
  )
  print(
    body.strip()
  )

  failures = []

  if "pi_14^7 finite cyclic" not in connector_source:
    failures.append(
      "r5 pi14 linkage sentinel is missing"
    )

  if (
    "_toda_group_proof_narrative_reference_statement_lines_by_number"
    not in connector_source
    or "filtered_reference_entries"
    not in connector_source
  ):
    failures.append(
      "r5 post-filter statement refresh sentinel is missing"
    )

  if pi14_boundary is None:
    failures.append(
      "pi14_7 step has no literature-boundary classification"
    )
  else:
    if pi14_boundary.classification.value != "fixed_statement":
      failures.append(
        "pi14_7 step is not classified FIXED_STATEMENT"
      )

    if (
      pi14_boundary.reference_locator
      != "Proposition 5.15"
    ):
      failures.append(
        "pi14_7 step is not attributed to Proposition 5.15"
      )

    if (
      pi14_boundary.component_key
      != "pi14_7_group_relation"
    ):
      failures.append(
        "pi14_7 step has unexpected component key"
      )

  expected_pi14 = (
    r"$\pi_{14}^{7} = "
    r"\mathbb{Z}/8\{\sigma'\}$"
  )

  if pi14_lines != (
    expected_pi14,
  ):
    failures.append(
      "post-filter Proposition 5.15 statement lines "
      "are not exactly the pi14_7 component"
    )

  if any(
    r"\pi_{15}^{8}"
    in line
    for line in pi14_lines
  ):
    failures.append(
      "root pi15_8 component remains in post-filter "
      "Proposition 5.15 statement lines"
    )

  if headers != (
    (
      1,
      "Proposition 5.15",
    ),
    (
      2,
      "Proposition 4.4",
    ),
  ):
    failures.append(
      "public Reference headers are not "
      "[R1] Proposition 5.15, [R2] Proposition 4.4"
    )

  if body_markers != (
    1,
    2,
  ):
    failures.append(
      "public proof-body markers are not exactly (1, 2)"
    )

  if expected_pi14 not in reference_section:
    failures.append(
      "public Proposition 5.15 Reference does not show pi14_7"
    )

  if (
    r"$\pi_{15}^{8} \cong"
    in reference_section
  ):
    failures.append(
      "root pi15_8 Proposition 5.15 component leaked into Reference"
    )

  if (
    "[R1] より,"
    not in body
    or expected_pi14.replace(
      "$",
      "",
    )
    not in body
  ):
    failures.append(
      "proof body does not link [R1] to pi14_7"
    )

  if (
    "[R2] より, これらの生成元はそれぞれ"
    not in body
  ):
    failures.append(
      "proof body does not link [R2] to Proposition 4.4 use"
    )

  print()
  print(
    "CLOSURE RESULT"
  )
  print(
    "-" * 104
  )

  if failures:
    print(
      "FAIL"
    )
    for failure in failures:
      print(
        "- "
        + failure
      )
  else:
    print(
      "PASS"
    )
    print(
      "- internal pi14_7 fixed-component alignment is correct"
    )
    print(
      "- root pi15_8 component is excluded from Reference"
    )
    print(
      "- public Reference numbering is [R1] Prop.5.15 / [R2] Prop.4.4"
    )
    print(
      "- proof body markers are exactly (1, 2)"
    )

  print()
  print(
    "No production file is modified."
  )
  print(
    "No test file is modified."
  )
  print(
    "Repository-wide pytest is intentionally NOT run."
  )

  return (
    1
    if failures
    else 0
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
