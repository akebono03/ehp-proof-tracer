from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair1"
BACKUP.mkdir(exist_ok=True)

REFERENCES = ROOT / "toda_group_proof_narrative_references.py"
CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
REASON = ROOT / "toda_group_proof_narrative_reason_renderer.py"
OLD_TEST = ROOT / "tests" / "test_phase157_r5_r9_fixed_definition_body_suppression.py"
NEW_TEST = ROOT / "tests" / "test_phase157_r11_reference_reason_punctuation.py"


def backup(path: Path) -> None:
  if not path.exists():
    return
  destination = BACKUP / path.name
  if not destination.exists():
    shutil.copy2(path, destination)


for path in (
  REFERENCES,
  CONTRIBUTION,
  REASON,
  OLD_TEST,
  NEW_TEST,
):
  backup(path)


def ensure_pipeline_calls() -> None:
  text = CONTRIBUTION.read_text(encoding="utf-8")

  if (
    "order_toda_group_proof_narrative_surjectivity_support(\n      rendered\n"
    in text
    and
    "insert_toda_group_proof_narrative_reference_map_values_before_surjectivity(\n      rendered,\n"
    in text
  ):
    print("Already applied: R11-R7 pipeline calls")
    return

  pattern = re.compile(
    r"""(?P<order>
  rendered = \(
    order_toda_group_proof_narrative_local_equation_derivations\(
      rendered
    \)
  \)
)(?P<gap>\s*)(?P<generic>  generic_used_step_ids = \()"""
  )

  match = pattern.search(text)
  if match is None:
    raise RuntimeError(
      "could not locate local-equation-ordering -> "
      "generic_used_step_ids pipeline boundary"
    )

  replacement = (
    match.group("order")
    + "\n"
    + """  rendered = (
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

"""
    + match.group("generic")
  )

  text = text[:match.start()] + replacement + text[match.end():]
  CONTRIBUTION.write_text(text, encoding="utf-8")
  print("Applied: R11-R7 pipeline calls")


def ensure_final_period_normalization() -> None:
  text = CONTRIBUTION.read_text(encoding="utf-8")

  if (
    "normalize_toda_group_proof_narrative_display_math_periods(\n      (\n"
    in text
  ):
    print("Already applied: public display-math period normalization")
    return

  old = """  return (
    "# Group proof narrative\\n\\n"
    "## 使用する結果\\n\\n"
    + public_reference_section
    + "\\n\\n"
    "---\\n\\n"
    "## 証明\\n\\n"
    + rendered
  )
"""

  new = """  return (
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
"""

  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      "expected exactly one public narrative return block, "
      f"found {count}"
    )

  CONTRIBUTION.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
  )
  print("Applied: public display-math period normalization")


def ensure_reason_cleanup() -> None:
  text = REASON.read_text(encoding="utf-8")

  new = """  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:
    return None
"""

  if new in text:
    print("Already applied: final-result filler suppression")
    return

  old = """  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:
    return "以上で得た群構造, 生成元, および写像に関する結果を合わせると, "
"""

  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      "expected exactly one FINAL_RESULT_DERIVATION filler, "
      f"found {count}"
    )

  REASON.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
  )
  print("Applied: final-result filler suppression")


def ensure_old_test_contract() -> None:
  if not OLD_TEST.exists():
    return

  text = OLD_TEST.read_text(encoding="utf-8")
  updated = (
    text
    .replace('"次に"', '"まず"')
    .replace('"次に, "', '"まず, "')
  )

  if updated == text:
    print("Old test opener contract already normalized")
    return

  OLD_TEST.write_text(updated, encoding="utf-8")
  print("Updated: old test opener contract 次に -> まず")


def ensure_new_tests() -> None:
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


def test_phase157_r11_r7_equation_53_reference_contains_hopf_value():
  reference, _ = _reference_and_body()

  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference
  )


def test_phase157_r11_r7_first_visible_argument_uses_mazu():
  _, body = _reference_and_body()

  assert (
    "まず, "
    r"$\nu'$ の位数を決定するために"
    in body
  )


def test_phase157_r11_r7_reference_reuse_is_explicit():
  _, body = _reference_and_body()

  assert (
    "[R1]より, "
    r"$\nu' \in \pi_{6}^{3}$."
    in body
  )


def test_phase157_r11_r7_hopf_support_precedes_surjectivity():
  _, body = _reference_and_body()

  hopf_value = (
    "[R1]より, "
    r"$H\left(\nu'\right) = \eta_{5}$."
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

  assert body.index(
    target_group
  ) < body.index(
    surjectivity
  )
  assert body.index(
    hopf_value
  ) < body.index(
    surjectivity
  )


def test_phase157_r11_r7_generic_final_filler_is_absent():
  _, body = _reference_and_body()

  assert (
    "以上で得た群構造, 生成元, "
    "および写像に関する結果を合わせると,"
    not in body
  )


def test_phase157_r11_r7_display_math_lines_end_with_period():
  rendered = _render_pi6_3()

  for line in rendered.splitlines():
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
      raise AssertionError(
        "display-math line lacks ASCII period: "
        + stripped
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

  NEW_TEST.write_text(
    test_content,
    encoding="utf-8",
  )
  print(f"Written: {NEW_TEST.relative_to(ROOT)}")


ensure_pipeline_calls()
ensure_final_period_normalization()
ensure_reason_cleanup()
ensure_old_test_contract()
ensure_new_tests()

print("")
print("Phase157 R11-R7 repair1 applied successfully.")
