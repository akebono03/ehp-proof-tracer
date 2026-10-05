from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair4"
BACKUP.mkdir(exist_ok=True)

REFERENCES = ROOT / "toda_group_proof_narrative_references.py"
CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R11_TEST = ROOT / "tests" / "test_phase157_r11_reference_reason_punctuation.py"


def backup(path: Path) -> None:
  destination = BACKUP / path.name

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


for path in (
  REFERENCES,
  CONTRIBUTION,
  R11_TEST,
):
  backup(
    path
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
    print(
      f"Already applied: {label}"
    )
    return

  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"expected exactly one match for {label} "
      f"in {path}, found {count}"
    )

  path.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )

  print(
    f"Applied: {label}"
  )


old_selection = '''  used_candidates = tuple(
    step
    for step in eligible_candidates
    if id(
      step
    ) in used_candidate_step_ids
  )

  if used_candidates:
    return used_candidates
'''

new_selection = '''  used_candidate_conclusions = tuple(
    edge.premise_step.conclusion
    for edge in proof_edges
    if id(
      edge.premise_step
    ) in used_candidate_step_ids
  )

  used_candidates = tuple(
    step
    for step in eligible_candidates
    if (
      id(
        step
      ) in used_candidate_step_ids
      or any(
        step.conclusion == used_conclusion
        for used_conclusion in used_candidate_conclusions
      )
    )
  )

  if used_candidates:
    return used_candidates
'''

replace_once(
  REFERENCES,
  old_selection,
  new_selection,
  "reference statement selection matches used conclusions across duplicate ProofStep instances",
)


helper_anchor = '''def suppress_toda_group_proof_narrative_reference_body_duplicates(
'''

helper_code = r'''def _phase157_r11_reference_statement_match_key(
  line: str,
) -> str:
  if not isinstance(
    line,
    str,
  ):
    raise TypeError(
      "line must be a str"
    )

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


'''

text = CONTRIBUTION.read_text(
  encoding="utf-8"
)

if "def _phase157_r11_reference_statement_match_key(" not in text:
  if helper_anchor not in text:
    raise RuntimeError(
      "could not locate Reference/body duplicate helper insertion point"
    )

  CONTRIBUTION.write_text(
    text.replace(
      helper_anchor,
      helper_code + helper_anchor,
      1,
    ),
    encoding="utf-8",
  )

  print(
    "Applied: tagged-equation Reference match-key helper"
  )
else:
  print(
    "Already applied: tagged-equation Reference match-key helper"
  )


old_exact_loop = '''      for line in lines:
        stripped_line = line.strip()
        statement_core = statement_line.rstrip(
          ".,"
        )
        stripped_line_core = stripped_line.rstrip(
          ".,"
        )

        if stripped_line_core == statement_core:
          updated_lines.append(
            marker
            + "より, "
            + stripped_line_core
            + "."
          )
          continue

        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue
'''

new_exact_loop = '''      for line in lines:
        stripped_line = line.strip()
        statement_match_key = (
          _phase157_r11_reference_statement_match_key(
            statement_line
          )
        )
        line_match_key = (
          _phase157_r11_reference_statement_match_key(
            stripped_line
          )
        )

        if line_match_key == statement_match_key:
          display_line = stripped_line.rstrip(
            ".,"
          )
          updated_lines.append(
            marker
            + "より, "
            + display_line
            + "."
          )
          continue

        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue
'''

replace_once(
  CONTRIBUTION,
  old_exact_loop,
  new_exact_loop,
  "Reference/body standalone reuse ignores equation tags while preserving them in display",
)


def update_r11_test() -> None:
  text = R11_TEST.read_text(
    encoding="utf-8"
  )

  old_fixed_hopf = '''  fixed_hopf = (
    "[R2]より, "
    r"$H\\left(\\nu'\\right) = E^{2}\\eta_{3}$."
  )
  bridge = (
    r"$E^{2}\\eta_{3} = \\eta_{5}$."
  )
  derived_hopf = (
    r"$H\\left(\\nu'\\right) = \\eta_{5}$."
  )
'''

  new_fixed_hopf = '''  fixed_hopf = (
    "[R2]より, "
    r"$H\\left(\\nu'\\right) = E^{2}\\eta_{3}\\tag{4}$."
  )
  bridge = (
    r"$E^{2}\\eta_{3} = \\eta_{5}\\tag{5}$."
  )
  derived_hopf = (
    r"$H\\left(\\nu'\\right) = \\eta_{5}\\tag{6}$."
  )
'''

  if new_fixed_hopf not in text:
    if old_fixed_hopf not in text:
      raise RuntimeError(
        "could not locate R11 Hopf derivation expectation block"
      )

    text = text.replace(
      old_fixed_hopf,
      new_fixed_hopf,
      1,
    )

  test_name = (
    "def test_phase157_r11_r11_reference_keeps_all_used_equation_53_components():"
  )

  if test_name not in text:
    new_test = r'''


def test_phase157_r11_r11_reference_keeps_all_used_equation_53_components():
  reference, _ = _reference_and_body()

  assert "**[R2] (5.3).**" in reference
  assert (
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}$."
    in reference
  )
  assert (
    r"$H\left(\nu'\right) = E^{2}\eta_{3}$."
    in reference
  )
'''
    text = (
      text.rstrip()
      + new_test
      + "\n"
    )

  R11_TEST.write_text(
    text,
    encoding="utf-8",
  )

  print(
    "Updated: R11 tagged Reference linkage and (5.3) used-component regressions"
  )


update_r11_test()

print("")
print("Phase157 R11-R11 repair4 applied successfully.")
