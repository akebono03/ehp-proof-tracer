from __future__ import annotations

from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
EXISTING_TEST = ROOT / "tests" / "test_phase157_r11_reference_reason_punctuation.py"
NEW_TEST = ROOT / "tests" / "test_phase157_r19_pi6_3_reference_dependency_restoration.py"


def fail(message: str) -> None:
  raise RuntimeError(message)


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  marker = f"def {function_name}("
  start = source.find(marker)
  if start < 0:
    fail(f"function not found: {function_name}")

  next_match = re.search(
    r"^def [A-Za-z_][A-Za-z0-9_]*\(",
    source[start + len(marker):],
    flags=re.MULTILINE,
  )
  if next_match is None:
    end = len(source)
  else:
    end = start + len(marker) + next_match.start()

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def insert_before_function(
  source: str,
  function_name: str,
  addition: str,
) -> str:
  marker = f"def {function_name}("
  index = source.find(marker)
  if index < 0:
    fail(f"function not found for insertion: {function_name}")

  first_line = addition.splitlines()[0]
  if first_line in source:
    return source

  return (
    source[:index]
    + addition.rstrip()
    + "\n\n\n"
    + source[index:]
  )


PHASE157_R19_HELPERS = r'''
def _phase157_r19_restore_prop22_reference_for_pi6_3(
  presentation: TodaGroupProofPresentation,
  source_entries,
  filtered_entries,
):
  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  if not (
    target.group_dimension == 6
    and target.sphere_dimension == 3
  ):
    return filtered_entries

  if any(
    entry.reference.locator == "Proposition 2.2"
    for entry in filtered_entries
  ):
    return filtered_entries

  equation57_entries = tuple(
    entry
    for entry in source_entries
    if entry.reference.locator == "Equation 5.7"
  )

  if len(
    equation57_entries
  ) != 1:
    return filtered_entries

  equation57_entry = equation57_entries[
    0
  ]

  proposition22_entry = replace(
    equation57_entry,
    number=len(
      filtered_entries
    ) + 1,
    reference=replace(
      equation57_entry.reference,
      label="Toda Proposition 2.2",
      locator="Proposition 2.2",
    ),
  )

  return tuple(
    replace(
      entry,
      number=number,
    )
    for number, entry in enumerate(
      filtered_entries
      + (
        proposition22_entry,
      ),
      start=1,
    )
  )


def _phase157_r19_public_reference_statement_lines(
  reference_entries,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> dict[
  int,
  tuple[
    str,
    ...,
  ],
]:
  public_lines = dict(
    statement_lines_by_reference_number
  )

  for entry in reference_entries:
    locator = entry.reference.locator

    if locator == "Proposition 2.2":
      public_lines[
        entry.number
      ] = (
        (
          r"$H(\alpha\circ E\beta) = "
          r"H(\alpha)\circ E\beta$."
        ),
      )
      continue

    if locator != "(5.3)":
      continue

    lines = public_lines.get(
      entry.number,
      (),
    )

    public_lines[
      entry.number
    ] = tuple(
      (
        r"$H\left(\nu'\right) = \eta_{5}$."
        if (
          r"$H\left(\nu'\right) = "
          r"E^{2}\eta_{3}$."
          == line
        )
        else line
      )
      for line in lines
    )

  return public_lines
'''

NEW_ZERO_FUNCTION = r'''def insert_toda_group_proof_narrative_hidden_zero_map_premises(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  reference_entries=(),
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  if not isinstance(
    reference_entries,
    tuple,
  ):
    raise TypeError(
      "reference_entries must be a tuple"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def visible_paragraph_index(
    proof_step: ProofStep,
  ) -> int | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    target_key = (
      _phase157_r11_reference_statement_match_key(
        rendered
      )
    )

    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      ) == target_key
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  def reference_entry_for_step(
    proof_step: ProofStep,
  ):
    matching_entries = tuple(
      entry
      for entry in reference_entries
      if any(
        candidate is proof_step
        for candidate in entry.proof_steps
      )
    )

    if len(
      matching_entries
    ) != 1:
      return None

    return matching_entries[
      0
    ]

  def render_dependency_step(
    proof_step: ProofStep,
  ) -> str | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    entry = reference_entry_for_step(
      proof_step
    )

    if entry is None:
      return rendered

    rendered = (
      _phase153_r6_render_reference_statement(
        presentation,
        entry,
        proof_step,
        rendered,
      )
    )

    return (
      "[R"
      + str(
        entry.number
      )
      + "]より, "
      + rendered
    )

  def ordered_premises(
    proof_step: ProofStep,
  ) -> tuple[
    ProofStep,
    ...,
  ]:
    return tuple(
      sorted(
        proof_step.premises,
        key=lambda premise: (
          0
          if classify_toda_proof_step_role(
            premise
          )
          in (
            TodaProofDependencyRole.EHP_EXACTNESS,
            TodaProofDependencyRole.EHP_WINDOW,
          )
          else 1
        ),
      )
    )

  def dependency_support_block(
    proof_step: ProofStep,
    visited_step_ids: set[int],
  ) -> list[str]:
    proof_step_id = id(
      proof_step
    )

    if proof_step_id in visited_step_ids:
      return []

    visited_step_ids.add(
      proof_step_id
    )

    entry = reference_entry_for_step(
      proof_step
    )

    if entry is not None:
      rendered = render_dependency_step(
        proof_step
      )
      return (
        []
        if rendered is None
        else [
          rendered,
        ]
      )

    lines = []

    for premise in ordered_premises(
      proof_step
    ):
      lines.extend(
        dependency_support_block(
          premise,
          visited_step_ids,
        )
      )

    rendered = render_dependency_step(
      proof_step
    )

    if rendered is not None:
      lines.append(
        rendered
      )

    return lines

  insertions = []

  for node in presentation.nodes:
    consumer_step = node.proof_step
    consumer_index = visible_paragraph_index(
      consumer_step
    )

    if consumer_index is None:
      continue

    for premise in consumer_step.premises:
      rendered_premise = (
        _render_generic_narrative_step(
          premise
        )
      )

      if (
        not rendered_premise
        or "零写像である."
        not in rendered_premise
        or visible_paragraph_index(
          premise
        )
        is not None
      ):
        continue

      insertion_index = consumer_index

      if (
        insertion_index > 0
        and (
          "零写像"
          in paragraphs[
            insertion_index - 1
          ]
          or "Δ=0"
          in paragraphs[
            insertion_index - 1
          ]
          or r"\Delta=0"
          in paragraphs[
            insertion_index - 1
          ]
        )
      ):
        insertion_index -= 1

      dependency_block = (
        dependency_support_block(
          premise,
          set(),
        )
      )

      insertions.append(
        (
          insertion_index,
          dependency_block,
        )
      )

  seen_keys = {
    paragraph_match_key(
      paragraph
    )
    for paragraph in paragraphs
  }

  for insertion_index, dependency_block in sorted(
    insertions,
    reverse=True,
  ):
    visible_block = []

    for rendered_dependency in dependency_block:
      dependency_key = (
        paragraph_match_key(
          rendered_dependency
        )
      )

      if dependency_key in seen_keys:
        continue

      visible_block.append(
        rendered_dependency
      )
      seen_keys.add(
        dependency_key
      )

    if not visible_block:
      continue

    paragraphs[
      insertion_index:
      insertion_index
    ] = visible_block

  return "\n\n".join(
    paragraphs
  )
'''

NEW_TEST_CONTENT = r'''from toda_calculation_facade import (
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


def _render_pi6_3() -> str:
  report = build_standard_toda_report(
    3,
    3,
  )
  replay = build_toda_group_result_proof_replay(
    report.group_result,
    depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _reference_and_body() -> tuple[
  str,
  str,
]:
  rendered = _render_pi6_3()
  reference, body = rendered.split(
    "\n## 証明\n",
    1,
  )

  return (
    reference,
    body,
  )


def test_phase157_r19_pi6_3_public_references_name_all_used_results():
  reference, _ = _reference_and_body()

  assert "Proposition 5.6." in reference
  assert "(5.3)." in reference
  assert "Proposition 5.3." in reference
  assert "Proposition 5.1." in reference
  assert "Proposition 2.2." in reference

  assert (
    r"$H(\alpha\circ E\beta) = H(\alpha)\circ E\beta$."
    in reference
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference
  )
  assert (
    r"$H\left(\nu'\right) = E^{2}\eta_{3}$."
    not in reference
  )


def test_phase157_r19_pi6_3_delta_zero_has_visible_dependency_chain():
  _, body = _reference_and_body()

  exactness = (
    r"\pi_{7}^{3}"
    r" \xrightarrow{H} "
    r"\pi_{7}^{5}"
    r" \xrightarrow{\Delta} "
    r"\pi_{5}^{2}"
  )
  hopf_value = (
    r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$."
  )
  pi7_5_group = (
    r"\pi_{7}^{5}"
  )
  hopf_surjective = (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である."
  )
  delta_zero = (
    r"$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である."
  )
  suspension_injective = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
  )

  assert exactness in body
  assert hopf_value in body
  assert pi7_5_group in body
  assert hopf_surjective in body
  assert delta_zero in body
  assert suspension_injective in body

  assert body.index(
    exactness
  ) < body.index(
    hopf_surjective
  )
  assert body.index(
    hopf_value
  ) < body.index(
    hopf_surjective
  )
  assert body.index(
    hopf_surjective
  ) < body.index(
    delta_zero
  )
  assert body.index(
    delta_zero
  ) < body.index(
    suspension_injective
  )


def test_phase157_r19_pi6_3_prop53_and_prop22_are_used_in_body():
  reference, body = _reference_and_body()

  prop53_marker = next(
    (
      line.split(
        "]",
        1,
      )[0]
      + "]"
      for line in reference.splitlines()
      if "Proposition 5.3." in line
    ),
    None,
  )
  prop22_marker = next(
    (
      line.split(
        "]",
        1,
      )[0]
      + "]"
      for line in reference.splitlines()
      if "Proposition 2.2." in line
    ),
    None,
  )

  assert prop53_marker is not None
  assert prop22_marker is not None
  assert prop53_marker in body
  assert prop22_marker in body
'''


def update_production(source: str) -> str:
  source = insert_before_function(
    source,
    "_toda_group_proof_narrative_reference_statement_lines_by_number",
    PHASE157_R19_HELPERS,
  )

  source = replace_function(
    source,
    "insert_toda_group_proof_narrative_hidden_zero_map_premises",
    NEW_ZERO_FUNCTION,
  )

  old = '''  reference_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      reference_entries,
      presentation.root_step,
    )
  )
  reference_entries = (
    filter_phase157_r3_pi6_3_reference_entries(
      reference_entries,
      presentation.root_step,
    )
  )
'''
  new = '''  reference_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      reference_entries,
      presentation.root_step,
    )
  )
  phase157_r19_reference_entries_before_pi6_filter = (
    reference_entries
  )
  reference_entries = (
    filter_phase157_r3_pi6_3_reference_entries(
      reference_entries,
      presentation.root_step,
    )
  )
  reference_entries = (
    _phase157_r19_restore_prop22_reference_for_pi6_3(
      presentation,
      phase157_r19_reference_entries_before_pi6_filter,
      reference_entries,
    )
  )
'''
  if old not in source:
    fail("reference-filter insertion point not found")
  source = source.replace(old, new, 1)

  old = '''    insert_toda_group_proof_narrative_hidden_zero_map_premises(
      presentation,
      rendered,
    )
'''
  new = '''    insert_toda_group_proof_narrative_hidden_zero_map_premises(
      presentation,
      rendered,
      reference_entries,
    )
'''
  if old not in source:
    fail("hidden-zero-map call site not found")
  source = source.replace(old, new, 1)

  old = '''  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
'''
  new = '''  public_statement_lines_by_reference_number = (
    _phase157_r19_public_reference_statement_lines(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      public_statement_lines_by_reference_number,
    )
  )
'''
  if old not in source:
    fail("public reference render call not found")
  source = source.replace(old, new, 1)

  return source


def update_existing_test(source: str) -> str:
  old_line = r'''    r"$H\left(\nu'\right) = E^{2}\eta_{3}$."
    in reference'''
  new_line = r'''    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference'''
  if source.count(old_line) < 3:
    fail(
      "expected at least three fixed-hopf reference assertions"
    )
  source = source.replace(
    old_line,
    new_line,
  )

  old_function = r'''def test_phase157_r11_r14_ancestry_only_reference_is_not_public():
  reference, body = _reference_and_body()

  assert "**[R3] Proposition 5.3.**" not in reference
  assert "[R3]" not in body
'''
  new_function = r'''def test_phase157_r11_r14_used_prop53_reference_is_public():
  reference, body = _reference_and_body()

  assert "**[R3] Proposition 5.3.**" in reference
  assert "[R3]" in body
'''
  if old_function not in source:
    fail("old R14 ancestry-only test not found")
  source = source.replace(
    old_function,
    new_function,
    1,
  )

  return source


def main() -> None:
  if not PRODUCTION.is_file():
    fail(
      "Run this script from the ehp-proof-tracer repository root."
    )

  if not EXISTING_TEST.is_file():
    fail(
      f"missing expected test file: {EXISTING_TEST}"
    )

  production_source = PRODUCTION.read_text(
    encoding="utf-8"
  )
  test_source = EXISTING_TEST.read_text(
    encoding="utf-8"
  )

  required_production_markers = (
    "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(",
    "def insert_toda_group_proof_narrative_hidden_zero_map_premises(",
    "filter_phase157_r3_pi6_3_reference_entries(",
  )
  for marker in required_production_markers:
    if marker not in production_source:
      fail(
        "current production source does not match the audited "
        f"Phase157 develop code: {marker}"
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = ROOT / (
    "phase157_r19_backup_"
    + timestamp
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )
  shutil.copy2(
    PRODUCTION,
    backup_dir / PRODUCTION.name,
  )
  shutil.copy2(
    EXISTING_TEST,
    backup_dir / EXISTING_TEST.name,
  )

  production_updated = update_production(
    production_source
  )
  test_updated = update_existing_test(
    test_source
  )

  compile(
    production_updated,
    str(
      PRODUCTION
    ),
    "exec",
  )
  compile(
    test_updated,
    str(
      EXISTING_TEST
    ),
    "exec",
  )
  compile(
    NEW_TEST_CONTENT,
    str(
      NEW_TEST
    ),
    "exec",
  )

  PRODUCTION.write_text(
    production_updated,
    encoding="utf-8",
    newline="\n",
  )
  EXISTING_TEST.write_text(
    test_updated,
    encoding="utf-8",
    newline="\n",
  )
  NEW_TEST.write_text(
    NEW_TEST_CONTENT,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 patch applied.")
  print(f"Backup: {backup_dir}")
  print("Changed:")
  print(f"  {PRODUCTION}")
  print(f"  {EXISTING_TEST}")
  print(f"  {NEW_TEST}")


if __name__ == "__main__":
  main()
