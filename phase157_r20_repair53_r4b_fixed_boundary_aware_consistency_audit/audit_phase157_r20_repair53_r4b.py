from __future__ import annotations

import dataclasses
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
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
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
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_components,
  select_toda_fixed_statement_reference_components,
)


def _step_summary(
  step,
) -> dict:
  reference = (
    step.inference_rule.literature_reference
    if (
      step.inference_rule is not None
      and step.inference_rule.literature_reference is not None
    )
    else None
  )

  return {
    "conclusion_type": type(
      step.conclusion
    ).__name__,
    "rule": (
      step.inference_rule.name
      if step.inference_rule is not None
      else None
    ),
    "reference_locator": (
      reference.locator
      if reference is not None
      else None
    ),
  }


def _object_summary(
  value,
):
  if value is None:
    return None

  if dataclasses.is_dataclass(
    value
  ):
    return {
      field.name: getattr(
        value,
        field.name,
      )
      for field in dataclasses.fields(
        value
      )
    }

  if isinstance(
    value,
    tuple,
  ):
    return tuple(
      _object_summary(
        item
      )
      for item in value
    )

  return repr(
    value
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
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )
  (
    non_root_entries,
    non_root_statement_lines,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      entries,
      statement_lines,
      presentation.root_step,
    )
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  return (
    presentation,
    entries,
    statement_lines,
    non_root_entries,
    non_root_statement_lines,
    rendered,
  )


def _public_reference_part(
  rendered: str,
) -> str:
  marker = "\n## 使用する結果\n"
  if marker not in rendered:
    return ""

  tail = rendered.split(
    marker,
    1,
  )[1]

  proof_marker = "\n## 証明\n"
  if proof_marker not in tail:
    return tail

  return tail.split(
    proof_marker,
    1,
  )[0]


def _public_body(
  rendered: str,
) -> str:
  marker = "\n## 証明\n"
  if marker not in rendered:
    return rendered

  return rendered.split(
    marker,
    1,
  )[1].lstrip()


def _parse_public_reference_entries(
  rendered: str,
):
  reference_part = _public_reference_part(
    rendered
  )

  matches = list(
    re.finditer(
      r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*",
      reference_part,
    )
  )

  parsed = []

  for index, match in enumerate(
    matches
  ):
    start = match.end()
    end = (
      matches[
        index + 1
      ].start()
      if index + 1 < len(
        matches
      )
      else len(
        reference_part
      )
    )

    statement = reference_part[
      start:
      end
    ].strip()

    if statement.endswith(
      "---"
    ):
      statement = statement[
        :-3
      ].rstrip()

    parsed.append(
      {
        "number": int(
          match.group(
            1
          )
        ),
        "locator": match.group(
          2
        ),
        "statement": statement,
      }
    )

  return tuple(
    parsed
  )


def main() -> int:
  (
    presentation,
    entries,
    statement_lines,
    non_root_entries,
    non_root_statement_lines,
    rendered,
  ) = _build_data()

  public_entries = (
    _parse_public_reference_entries(
      rendered
    )
  )
  body = _public_body(
    rendered
  )

  body_marker_numbers = tuple(
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

  print(
    "=" * 108
  )
  print(
    "Phase157-R20 repair53-r4b - fixed-boundary-aware pi15^8 Reference consistency audit"
  )
  print(
    "=" * 108
  )
  print(
    "Production code changes: none"
  )
  print(
    "pytest: not run"
  )
  print()

  print(
    "RAW GRAPH REFERENCE ENTRIES"
  )
  print(
    "-" * 108
  )

  for entry in entries:
    print(
      {
        "number": entry.number,
        "locator": entry.reference.locator,
        "proof_steps": tuple(
          _step_summary(
            step
          )
          for step in entry.proof_steps
        ),
        "statement_lines": statement_lines.get(
          entry.number,
          (),
        ),
      }
    )

  print()
  print(
    "FIXED-BOUNDARY CLASSIFICATION BY STEP"
  )
  print(
    "-" * 108
  )

  for entry in entries:
    print(
      "ENTRY",
      entry.number,
      entry.reference.locator,
    )

    for index, step in enumerate(
      entry.proof_steps,
      start=1,
    ):
      boundary = (
        classify_toda_literature_statement_step(
          step
        )
      )

      print(
        {
          "step_index": index,
          **_step_summary(
            step
          ),
          "boundary": _object_summary(
            boundary
          ),
        }
      )

  print()
  print(
    "FIXED COMPONENT CATALOG"
  )
  print(
    "-" * 108
  )

  locators = tuple(
    dict.fromkeys(
      entry.reference.locator
      for entry in entries
      if entry.reference.locator is not None
    )
  )

  for locator in locators:
    try:
      components = (
        get_toda_fixed_statement_components(
          locator
        )
      )
    except Exception as exc:
      print(
        {
          "locator": locator,
          "error": (
            type(
              exc
            ).__name__
            + ": "
            + str(
              exc
            )
          ),
        }
      )
      continue

    print(
      {
        "locator": locator,
        "components": _object_summary(
          components
        ),
      }
    )

  print()
  print(
    "CROSS-REFERENCE COMPONENT SELECTION"
  )
  print(
    "-" * 108
  )

  for source_locator in locators:
    for target_locator in locators:
      try:
        source_components = (
          get_toda_fixed_statement_components(
            source_locator
          )
        )
      except Exception:
        continue

      for component in source_components:
        component_key = getattr(
          component,
          "component_key",
          None,
        )

        if component_key is None:
          continue

        try:
          selected = (
            select_toda_fixed_statement_reference_components(
              source_locator,
              target_locator,
              component_key,
            )
          )
        except Exception as exc:
          print(
            {
              "source_locator": source_locator,
              "target_locator": target_locator,
              "component_key": component_key,
              "error": (
                type(
                  exc
                ).__name__
                + ": "
                + str(
                  exc
                )
              ),
            }
          )
          continue

        if selected:
          print(
            {
              "source_locator": source_locator,
              "target_locator": target_locator,
              "component_key": component_key,
              "selected": _object_summary(
                selected
              ),
            }
          )

  print()
  print(
    "AFTER ROOT EXCLUSION"
  )
  print(
    "-" * 108
  )

  for entry in non_root_entries:
    print(
      {
        "number": entry.number,
        "locator": entry.reference.locator,
        "proof_steps": tuple(
          _step_summary(
            step
          )
          for step in entry.proof_steps
        ),
        "statement_lines": non_root_statement_lines.get(
          entry.number,
          (),
        ),
      }
    )

  print()
  print(
    "PUBLIC REFERENCE ENTRIES"
  )
  print(
    "-" * 108
  )

  for entry in public_entries:
    print(
      entry
    )

  print()
  print(
    "PUBLIC BODY MARKERS - EXACT PROOF SECTION ONLY"
  )
  print(
    "-" * 108
  )
  print(
    body_marker_numbers
  )

  for line in body.splitlines():
    if re.search(
      r"\[R[0-9]+\]",
      line,
    ):
      print(
        repr(
          line
        )
      )

  print()
  print(
    "PUBLIC PROOF BODY"
  )
  print(
    "-" * 108
  )
  print(
    body.rstrip()
  )

  print()
  print(
    "TARGETED PROPOSITION 5.15 CHECK"
  )
  print(
    "-" * 108
  )

  prop515_entries = tuple(
    entry
    for entry in entries
    if entry.reference.locator
    == "Proposition 5.15"
  )

  for entry in prop515_entries:
    for index, step in enumerate(
      entry.proof_steps,
      start=1,
    ):
      print(
        {
          "step_index": index,
          **_step_summary(
            step
          ),
          "boundary": _object_summary(
            classify_toda_literature_statement_step(
              step
            )
          ),
        }
      )

  print()
  print(
    "TARGETED STATEMENT/STEP ALIGNMENT CHECK"
  )
  print(
    "-" * 108
  )

  suspicious_alignment = []

  for entry in non_root_entries:
    lines = non_root_statement_lines.get(
      entry.number,
      (),
    )

    print(
      {
        "locator": entry.reference.locator,
        "remaining_step_types": tuple(
          type(
            step.conclusion
          ).__name__
          for step in entry.proof_steps
        ),
        "remaining_rules": tuple(
          (
            step.inference_rule.name
            if step.inference_rule is not None
            else None
          )
          for step in entry.proof_steps
        ),
        "statement_lines": lines,
      }
    )

    if (
      entry.reference.locator
      == "Proposition 5.15"
      and any(
        "pi_14^7 finite cyclic"
        in (
          step.inference_rule.name
          if step.inference_rule is not None
          else ""
        )
        for step in entry.proof_steps
      )
      and not any(
        r"\pi_{14}^{7}"
        in line
        for line in lines
      )
    ):
      suspicious_alignment.append(
        "Proposition 5.15 retains pi_14^7 step "
        "but its statement lines do not contain pi_14^7."
      )

  print()
  print(
    "AUDIT INTERPRETATION"
  )
  print(
    "-" * 108
  )

  if suspicious_alignment:
    print(
      "REVIEW REQUIRED"
    )
    for finding in suspicious_alignment:
      print(
        "- "
        + finding
      )
  else:
    print(
      "No step/statement alignment mismatch detected by the targeted check."
    )

  print()
  print(
    "Public Proposition 4.4 count:",
    sum(
      1
      for entry in public_entries
      if entry[
        "locator"
      ] == "Proposition 4.4"
    ),
  )
  print(
    "Public Proposition 5.15 count:",
    sum(
      1
      for entry in public_entries
      if entry[
        "locator"
      ] == "Proposition 5.15"
    ),
  )
  print(
    "Exact proof-body marker numbers:",
    body_marker_numbers,
  )

  print()
  print(
    "No production file is modified."
  )
  print(
    "No test file is modified."
  )
  print(
    "No pytest is run."
  )
  print(
    "Repository-wide pytest remains reserved for the end of Phase 157."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
