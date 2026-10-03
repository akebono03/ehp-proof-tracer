from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"
BACKUP.mkdir(exist_ok=True)

REFERENCES = ROOT / "toda_group_proof_narrative_references.py"
CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
REASON = ROOT / "toda_group_proof_narrative_reason_renderer.py"
TEST = ROOT / "tests" / "test_phase157_r11_reference_reason_punctuation.py"
OLD_TEST = ROOT / "tests" / "test_phase157_r5_r9_fixed_definition_body_suppression.py"


def backup(path: Path) -> None:
  if not path.exists():
    return

  destination = BACKUP / path.name

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


def replace_once(
  path: Path,
  old: str,
  new: str,
  label: str,
) -> None:
  text = path.read_text(
    encoding="utf-8"
  )

  if new in text:
    print(f"Already applied: {label}")
    return

  count = text.count(old)

  if count != 1:
    raise RuntimeError(
      f"expected exactly one match for {label} in {path}, found {count}"
    )

  path.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
  )

  print(f"Applied: {label}")


for path in (
  REFERENCES,
  CONTRIBUTION,
  REASON,
  OLD_TEST,
  TEST,
):
  backup(path)


old_reference_branch = '''    if locator == "(5.3)":
      retained_steps = entry.proof_steps
    else:
'''

new_reference_branch = '''    if locator == "(5.3)":
      retained_steps_list = list(
        entry.proof_steps
      )
      retained_component_keys = {
        boundary.component_key
        for proof_step in retained_steps_list
        for boundary in (
          classify_toda_literature_statement_step(
            proof_step
          ),
        )
        if boundary is not None
      }

      if "nu_prime_hopf_relation" not in retained_component_keys:
        stack = [
          root_step,
        ]
        visited_step_ids = set()

        while stack:
          current_step = stack.pop()
          current_step_id = id(
            current_step
          )

          if current_step_id in visited_step_ids:
            continue

          visited_step_ids.add(
            current_step_id
          )
          boundary = classify_toda_literature_statement_step(
            current_step
          )

          if (
            boundary is not None
            and boundary.classification
            is TodaLiteratureStatementClassification.FIXED_STATEMENT
            and boundary.reference_locator == "(5.3)"
            and boundary.component_key == "nu_prime_hopf_relation"
          ):
            retained_steps_list.append(
              current_step
            )
            break

          stack.extend(
            reversed(
              current_step.premises
            )
          )

      retained_steps = tuple(
        retained_steps_list
      )
    else:
'''

replace_once(
  REFERENCES,
  old_reference_branch,
  new_reference_branch,
  "retain existing (5.3) Hopf component in pi6_3 Reference",
)


old_exact_duplicate = '''        if line.strip() == statement_line:
          continue
'''

new_exact_duplicate = '''        if line.strip() == statement_line:
          updated_lines.append(
            marker
            + "より, "
            + statement_line
          )
          continue
'''

replace_once(
  CONTRIBUTION,
  old_exact_duplicate,
  new_exact_duplicate,
  "turn exact Reference/body reuse into explicit [R#] citation",
)


old_normalize_return = '''  return "\\n\\n".join(
    retained
  )
'''

new_normalize_return = '''  normalized = "\\n\\n".join(
    retained
  )

  normalized_paragraphs = normalized.split(
    "\\n\\n"
  )

  for index, paragraph in enumerate(
    normalized_paragraphs
  ):
    stripped = paragraph.strip()

    if not stripped:
      continue

    if stripped.startswith(
      "次に, "
    ):
      normalized_paragraphs[
        index
      ] = paragraph.replace(
        "次に, ",
        "まず, ",
        1,
      )

    break

  return "\\n\\n".join(
    normalized_paragraphs
  )
'''

replace_once(
  CONTRIBUTION,
  old_normalize_return,
  new_normalize_return,
  "normalize first visible argument connector from 次に to まず",
)


insert_anchor = "def order_toda_group_proof_narrative_local_equation_derivations(\n"

new_helpers = r'''def order_toda_group_proof_narrative_surjectivity_support(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  for map_index, paragraph in enumerate(
    tuple(
      paragraphs
    )
  ):
    stripped = paragraph.strip()

    if (
      not stripped.startswith(
        "$H:"
      )
      or " は全射である." not in stripped
      or r"\to " not in stripped
    ):
      continue

    target_fragment = stripped.split(
      r"\to ",
      1,
    )[1].split(
      "$",
      1,
    )[0].strip()

    group_index = next(
      (
        index
        for index in range(
          map_index + 1,
          len(paragraphs),
        )
        if paragraphs[index].strip().startswith(
          "$" + target_fragment + " = "
        )
      ),
      None,
    )

    if group_index is None:
      continue

    group_paragraph = paragraphs.pop(
      group_index
    )
    paragraphs.insert(
      map_index,
      group_paragraph,
    )

  return "\n\n".join(
    paragraphs
  )


def insert_toda_group_proof_narrative_reference_map_values_before_surjectivity(
  markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    for statement_line in statement_lines:
      if not (
        statement_line.startswith(
          "$H\\left("
        )
        and " = " in statement_line
      ):
        continue

      if any(
        statement_line in paragraph
        for paragraph in paragraphs
      ):
        continue

      map_index = next(
        (
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if (
            paragraph.strip().startswith(
              "$H:"
            )
            and " は全射である." in paragraph
          )
        ),
        None,
      )

      if map_index is None:
        continue

      paragraphs.insert(
        map_index,
        (
          "[R"
          + str(reference_number)
          + "]より, "
          + statement_line
        ),
      )

  return "\n\n".join(
    paragraphs
  )


def normalize_toda_group_proof_narrative_display_math_periods(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  normalized_lines = []

  for line in markdown.splitlines():
    stripped = line.strip()

    if (
      stripped.startswith(
        "$"
      )
      and stripped.endswith(
        "$"
      )
      and stripped != r"$\square$"
    ):
      line = line.rstrip() + "."

    normalized_lines.append(
      line
    )

  return "\n".join(
    normalized_lines
  )


'''

text = CONTRIBUTION.read_text(
  encoding="utf-8"
)

if "def order_toda_group_proof_narrative_surjectivity_support(" not in text:
  if insert_anchor not in text:
    raise RuntimeError(
      "could not find insertion point for R11 helpers"
    )

  text = text.replace(
    insert_anchor,
    new_helpers + insert_anchor,
    1,
  )

  CONTRIBUTION.write_text(
    text,
    encoding="utf-8",
  )

  print(
    "Applied: generic R11 ordering/reference/punctuation helpers"
  )
else:
  print("Already applied: R11 helper functions")


old_pipeline = '''  rendered = (
    order_toda_group_proof_narrative_local_equation_derivations(
      rendered
    )
  )

  generic_used_step_ids = (
'''

new_pipeline = '''  rendered = (
    order_toda_group_proof_narrative_local_equation_derivations(
      rendered
    )
  )
  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      rendered
    )
  )
  rendered = (
    insert_toda_group_proof_narrative_reference_map_values_before_surjectivity(
      rendered,
      statement_lines_by_reference_number,
    )
  )

  generic_used_step_ids = (
'''

replace_once(
  CONTRIBUTION,
  old_pipeline,
  new_pipeline,
  "order surjectivity support and insert Reference-backed H values",
)


old_final_return = '''  return (
    "# Group proof narrative\\n\\n"
    "## 使用する結果\\n\\n"
    + public_reference_section
    + "\\n\\n"
    "---\\n\\n"
    "## 証明\\n\\n"
    + rendered
  )
'''

new_final_return = '''  return (
    normalize_toda_group_proof_narrative_display_math_periods(
      (
        "# Group proof narrative\\n\\n"
        "## 使用する結果\\n\\n"
        + public_reference_section
        + "\\n\\n"
        "---\\n\\n"
        "## 証明\\n\\n"
        + rendered
      )
    )
  )
'''

replace_once(
  CONTRIBUTION,
  old_final_return,
  new_final_return,
  "apply display-math ASCII period policy after structural rendering",
)


old_final_reason = '''  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:
    return "以上で得た群構造, 生成元, および写像に関する結果を合わせると, "
'''

new_final_reason = '''  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:
    return None
'''

replace_once(
  REASON,
  old_final_reason,
  new_final_reason,
  "remove non-informative generic final-result filler sentence",
)


if OLD_TEST.exists():
  old_test_text = OLD_TEST.read_text(
    encoding="utf-8"
  )
  old_test_text = old_test_text.replace('"次に"', '"まず"')
  old_test_text = old_test_text.replace('"次に, "', '"まず, "')
  OLD_TEST.write_text(
    old_test_text,
    encoding="utf-8",
  )
  print("Updated: Phase157-R5/R9 opener contract 次に -> まず")


test_content = r'''from toda_calculation_facade import (
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
    n=3,
    k=3,
  )
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _reference_and_body() -> tuple[str, str]:
  rendered = _render_pi6_3()
  reference, body = rendered.split(
    "\n## 証明\n",
    1,
  )

  return reference, body


def test_phase157_r11_r7_equation_53_reference_contains_hopf_value():
  reference, _ = _reference_and_body()

  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference
  )


def test_phase157_r11_r7_first_visible_argument_uses_mazu():
  _, body = _reference_and_body()

  assert (
    "まず, " r"$\nu'$ の位数を決定するために"
    in body
  )


def test_phase157_r11_r7_reference_reuse_is_explicit():
  _, body = _reference_and_body()

  assert (
    "[R1]より, " r"$\nu' \in \pi_{6}^{3}$."
    in body
  )


def test_phase157_r11_r7_hopf_support_precedes_surjectivity():
  _, body = _reference_and_body()

  hopf_value = (
    "[R1]より, " r"$H\left(\nu'\right) = \eta_{5}$."
  )
  target_group = (
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$."
  )
  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である."
  )

  assert hopf_value in body
  assert target_group in body
  assert surjectivity in body
  assert body.index(target_group) < body.index(surjectivity)
  assert body.index(hopf_value) < body.index(surjectivity)


def test_phase157_r11_r7_generic_final_filler_is_absent():
  _, body = _reference_and_body()

  assert (
    "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"
    not in body
  )


def test_phase157_r11_r7_display_math_lines_end_with_period():
  rendered = _render_pi6_3()

  for line in rendered.splitlines():
    stripped = line.strip()

    if (
      stripped.startswith("$")
      and stripped.endswith("$")
      and stripped != r"$\square$"
    ):
      raise AssertionError(
        "display-math line lacks ASCII period: " + stripped
      )


def test_phase157_r11_r7_exact_sequence_ends_with_period():
  _, body = _reference_and_body()

  assert (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$."
    in body
  )
'''

TEST.write_text(
  test_content,
  encoding="utf-8",
)

print(f"Written: {TEST.relative_to(ROOT)}")
print("Phase157 R11-R7 patch applied.")