from __future__ import annotations

import importlib
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


def _step_summary(
  step,
) -> tuple[
  str,
  str | None,
]:
  conclusion_type = type(
    step.conclusion
  ).__name__
  rule_name = (
    step.inference_rule.name
    if step.inference_rule is not None
    else None
  )
  return (
    conclusion_type,
    rule_name,
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


def _parse_public_reference_entries(
  rendered: str,
):
  if "## 使用する結果" not in rendered:
    return ()

  reference_tail = rendered.split(
    "## 使用する結果",
    1,
  )[1]
  reference_part = reference_tail.split(
    "## 証明",
    1,
  )[0]

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


def _public_body(
  rendered: str,
) -> str:
  if "## 証明" not in rendered:
    return rendered

  return rendered.split(
    "## 証明",
    1,
  )[1].lstrip()


def _boundary_module_report() -> tuple[
  str,
  ...,
]:
  lines = []

  try:
    module = importlib.import_module(
      "toda_literature_statement_boundary"
    )
  except ModuleNotFoundError:
    return (
      "module: toda_literature_statement_boundary",
      "status: not found",
    )

  lines.append(
    "module: "
    + module.__name__
  )
  lines.append(
    "path: "
    + str(
      getattr(
        module,
        "__file__",
        None,
      )
    )
  )

  public_names = tuple(
    sorted(
      name
      for name in dir(
        module
      )
      if (
        not name.startswith(
          "_"
        )
        and (
          "boundary" in name.lower()
          or "fixed" in name.lower()
          or "classif" in name.lower()
          or "identity" in name.lower()
        )
      )
    )
  )

  lines.append(
    "public boundary-related names:"
  )

  if not public_names:
    lines.append(
      "  (none)"
    )
  else:
    lines.extend(
      "  "
      + name
      for name in public_names
    )

  for name in public_names:
    value = getattr(
      module,
      name,
    )
    if inspect.isfunction(
      value
    ):
      try:
        signature = inspect.signature(
          value
        )
      except (
        TypeError,
        ValueError,
      ):
        signature = None

      lines.append(
        "  function "
        + name
        + str(
          signature
          if signature is not None
          else ""
        )
      )

  return tuple(
    lines
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
    "=" * 104
  )
  print(
    "Phase157-R20 repair53-r4 - pi15^8 post-remap Reference consistency audit"
  )
  print(
    "=" * 104
  )
  print(
    "Production code changes: none"
  )
  print(
    "pytest: not run"
  )
  print()

  print(
    "GRAPH ENTRIES"
  )
  print(
    "-" * 104
  )

  for entry in entries:
    print(
      {
        "number": entry.number,
        "locator": entry.reference.locator,
        "label": entry.reference.label,
        "proof_steps": tuple(
          _step_summary(
            step
          )
          for step in entry.proof_steps
        ),
      }
    )

  print()
  print(
    "GRAPH STATEMENT LINES"
  )
  print(
    "-" * 104
  )

  for entry in entries:
    print(
      {
        "number": entry.number,
        "locator": entry.reference.locator,
        "statement_lines": statement_lines.get(
          entry.number,
          (),
        ),
      }
    )

  print()
  print(
    "AFTER ROOT EXCLUSION / CURRENT REFERENCE BOUNDARY"
  )
  print(
    "-" * 104
  )

  for entry in non_root_entries:
    print(
      {
        "number": entry.number,
        "locator": entry.reference.locator,
        "label": entry.reference.label,
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
    "LITERATURE STATEMENT BOUNDARY MODULE"
  )
  print(
    "-" * 104
  )

  for line in _boundary_module_report():
    print(
      line
    )

  print()
  print(
    "PUBLIC REFERENCE ENTRIES"
  )
  print(
    "-" * 104
  )

  if not public_entries:
    print(
      "(none)"
    )
  else:
    for entry in public_entries:
      print(
        entry
      )

  print()
  print(
    "PUBLIC BODY MARKERS"
  )
  print(
    "-" * 104
  )
  print(
    body_marker_numbers
  )

  marker_lines = tuple(
    line
    for line in body.splitlines()
    if re.search(
      r"\[R[0-9]+\]",
      line,
    )
  )

  print(
    "marker lines:"
  )
  for line in marker_lines:
    print(
      repr(
        line
      )
    )

  print()
  print(
    "PUBLIC BODY"
  )
  print(
    "-" * 104
  )
  print(
    body.rstrip()
  )

  public_numbers = {
    entry[
      "number"
    ]
    for entry in public_entries
  }
  used_numbers = set(
    body_marker_numbers
  )

  missing_marker_targets = sorted(
    used_numbers
    - public_numbers
  )
  unused_public_references = sorted(
    public_numbers
    - used_numbers
  )

  graph_locator_set = {
    entry.reference.locator
    for entry in non_root_entries
    if entry.reference.locator is not None
  }
  public_locator_set = {
    entry[
      "locator"
    ]
    for entry in public_entries
  }

  omitted_graph_locators = sorted(
    graph_locator_set
    - public_locator_set
  )
  public_only_locators = sorted(
    public_locator_set
    - graph_locator_set
  )

  duplicate_public_numbers = sorted(
    number
    for number in public_numbers
    if sum(
      1
      for entry in public_entries
      if entry[
        "number"
      ] == number
    )
    > 1
  )

  duplicate_public_locators = sorted(
    locator
    for locator in public_locator_set
    if sum(
      1
      for entry in public_entries
      if entry[
        "locator"
      ] == locator
    )
    > 1
  )

  print()
  print(
    "CONSISTENCY CANDIDATES"
  )
  print(
    "-" * 104
  )
  print(
    "body markers without public target:",
    missing_marker_targets,
  )
  print(
    "public References without body marker:",
    unused_public_references,
  )
  print(
    "non-root graph locators omitted from public:",
    omitted_graph_locators,
  )
  print(
    "public locators absent from non-root graph:",
    public_only_locators,
  )
  print(
    "duplicate public numbers:",
    duplicate_public_numbers,
  )
  print(
    "duplicate public locators:",
    duplicate_public_locators,
  )

  prop44_public = tuple(
    entry
    for entry in public_entries
    if entry[
      "locator"
    ] == "Proposition 4.4"
  )
  prop515_public = tuple(
    entry
    for entry in public_entries
    if entry[
      "locator"
    ] == "Proposition 5.15"
  )

  print()
  print(
    "TARGETED PI15^8 CHECKS"
  )
  print(
    "-" * 104
  )
  print(
    "Proposition 4.4 public count:",
    len(
      prop44_public
    ),
  )
  print(
    "Proposition 5.15 public count:",
    len(
      prop515_public
    ),
  )

  if prop44_public:
    prop44_number = prop44_public[
      0
    ][
      "number"
    ]
    print(
      "Proposition 4.4 public number:",
      prop44_number,
    )
    print(
      "Proposition 4.4 marker used in body:",
      prop44_number in used_numbers,
    )
    print(
      "Proposition 4.4 statement:",
      prop44_public[
        0
      ][
        "statement"
      ],
    )

  if prop515_public:
    prop515_number = prop515_public[
      0
    ][
      "number"
    ]
    print(
      "Proposition 5.15 public number:",
      prop515_number,
    )
    print(
      "Proposition 5.15 marker used in body:",
      prop515_number in used_numbers,
    )
    print(
      "Proposition 5.15 statement:",
      prop515_public[
        0
      ][
        "statement"
      ],
    )

  hard_failures = []

  if missing_marker_targets:
    hard_failures.append(
      "body marker without public Reference target"
    )

  if duplicate_public_numbers:
    hard_failures.append(
      "duplicate public Reference number"
    )

  if duplicate_public_locators:
    hard_failures.append(
      "duplicate public Reference locator"
    )

  if len(
    prop44_public
  ) != 1:
    hard_failures.append(
      "Proposition 4.4 public count is not exactly one"
    )
  elif (
    prop44_public[
      0
    ][
      "number"
    ]
    not in used_numbers
  ):
    hard_failures.append(
      "Proposition 4.4 public marker is not used in body"
    )

  print()
  print(
    "AUDIT RESULT"
  )
  print(
    "-" * 104
  )

  if hard_failures:
    print(
      "FAIL"
    )
    for failure in hard_failures:
      print(
        "- "
        + failure
      )
  else:
    print(
      "PASS: no hard Reference-number / marker consistency defect detected."
    )
    print(
      "Review the candidate lists above before deciding whether repair53 needs another production change."
    )

  print()
  print(
    "No production file is modified."
  )
  print(
    "No pytest is run."
  )
  print(
    "Repository-wide pytest remains reserved for the end of Phase 157."
  )

  return (
    1
    if hard_failures
    else 0
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
