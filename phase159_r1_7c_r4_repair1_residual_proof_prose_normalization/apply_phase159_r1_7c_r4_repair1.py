from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"


def replace_once(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )

    if new in text and old not in text:
        print(f"[already applied] {label}")
        return

    count = text.count(
        old
    )

    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one old fragment, found {count}"
        )

    path.write_text(
        text.replace(
            old,
            new,
            1,
        ),
        encoding="utf-8",
    )
    print(f"[updated] {label}")


def backup_file(
    relative_path: str,
) -> None:
    source = REPO_ROOT / relative_path
    target = BACKUP_DIR / relative_path
    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        source,
        target,
    )


def main() -> None:
    files = (
        "toda_group_proof_narrative_reason_renderer.py",
        "toda_group_proof_generic_narrative_renderer.py",
        "toda_group_proof_narrative_renderer.py",
        "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py",
        "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py",
        "tests/test_phase157_r11_reference_reason_punctuation.py",
    )

    if BACKUP_DIR.exists():
        shutil.rmtree(
            BACKUP_DIR
        )

    for relative_path in files:
        backup_file(
            relative_path
        )

    reason_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_reason_renderer.py"
    )

    replace_once(
        reason_path,
        '''    return (
      "この完全性と "
      f"${first_map_name}=0$ より, "
      f"$\\\\ker {second_map_name}"
      f"=\\\\operatorname{{Im}}{first_map_name}=0$ "
      "である.\\n"
      "したがって, "
    )
''',
        '''    return (
      "この完全性と "
      f"${first_map_name}=0$ より, "
      f"$\\\\ker {second_map_name}"
      f"=\\\\operatorname{{Im}}{first_map_name}=0$.\\n"
      "したがって, "
    )
''',
        "EXACTNESS_TO_MAP_PROPERTY prose",
    )

    replace_once(
        reason_path,
        '''    return (
      f"$\\\\operatorname{{ord}}({ordered_latex})=2$ "
      f"かつ $2{target_latex}={ordered_latex}$ より, "
      f"$4{target_latex}=0$ かつ "
      f"$2{target_latex}\\\\neq0$ である.\\n"
      "したがって, "
    )
''',
        '''    return (
      f"$\\\\operatorname{{ord}}({ordered_latex})=2$ "
      f"かつ $2{target_latex}={ordered_latex}$ より, "
      f"$4{target_latex}=0$ かつ "
      f"$2{target_latex}\\\\neq0$.\\n"
      "したがって, "
    )
''',
        "MULTIPLE_RELATION_TO_ORDER prose",
    )

    replace_once(
        reason_path,
        '''    return (
      "この短完全列と両端の群の位数より, "
      f"中央の群の位数は ${left_order}\\\\cdot"
      f"{right_order}={middle_order}$ である.\\n"
      f"また, ${generator_latex}$ は中央の群に属し, "
      f"$\\\\operatorname{{ord}}({generator_latex})"
      f"={order_statement.rhs}={middle_order}$ であるから, "
      f"${generator_latex}$ は中央の群を生成する.\\n"
      "したがって, "
    )
''',
        '''    return (
      "この短完全列と両端の群の位数より, "
      f"中央の群の位数は ${left_order}\\\\cdot"
      f"{right_order}={middle_order}$.\\n"
      f"また, ${generator_latex}$ は中央の群に属し, "
      f"$\\\\operatorname{{ord}}({generator_latex})"
      f"={order_statement.rhs}={middle_order}$ より, "
      f"${generator_latex}$ は中央の群を生成する.\\n"
      "したがって, "
    )
''',
        "FINAL_GROUP_STRUCTURE prose",
    )

    generic_path = (
        REPO_ROOT
        / "toda_group_proof_generic_narrative_renderer.py"
    )

    replace_once(
        generic_path,
        '''def _generic_short_exact_sequence_reason_prose(
  presentation: TodaGroupProofPresentation,
  exactness_step: ProofStep,
) -> str | None:
  short_exact_sequence_latex = (
    _generic_short_exact_sequence_latex(
      presentation,
      exactness_step,
    )
  )

  if short_exact_sequence_latex is None:
    return None

  return (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
''',
        '''def _generic_short_exact_sequence_reason_prose(
  presentation: TodaGroupProofPresentation,
  exactness_step: ProofStep,
) -> str | None:
  short_exact_sequence_latex = (
    _generic_short_exact_sequence_latex(
      presentation,
      exactness_step,
    )
  )

  if short_exact_sequence_latex is None:
    return None

  return (
    "この完全性と, 左の写像の単射性, "
    "右の写像の全射性より, "
    "次の短完全列が成り立つ."
  )
''',
        "short exact sequence reason prose",
    )

    narrative_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_renderer.py"
    )

    insertion_anchor = '''def _phase158_normalize_public_narrative_contract(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
'''

    helper = '''def _phase159_r1_7c_r4_normalize_proof_body_prose(
  proof_body: list[str],
) -> list[str]:
  if not isinstance(
    proof_body,
    list,
  ):
    raise TypeError(
      "proof_body must be a list"
    )

  normalized = []

  for source_line in proof_body:
    if not isinstance(
      source_line,
      str,
    ):
      raise TypeError(
        "proof_body must contain only strings"
      )

    line = source_line
    stripped = line.strip()

    if (
      stripped.startswith(
        "$"
      )
      and stripped.endswith(
        "$ である."
      )
    ):
      leading = line[
        :len(line)
        - len(line.lstrip())
      ]
      trailing = line[
        len(line.rstrip()):
      ]
      stripped = (
        stripped[
          :-len(
            " である."
          )
        ]
        + "."
      )
      line = (
        leading
        + stripped
        + trailing
      )

    for redundant_prefix in (
      "以上より, この完全性と ",
      "したがって, この完全性と ",
    ):
      stripped = line.strip()

      if not stripped.startswith(
        redundant_prefix
      ):
        continue

      leading = line[
        :len(line)
        - len(line.lstrip())
      ]
      trailing = line[
        len(line.rstrip()):
      ]
      stripped = (
        "この完全性と "
        + stripped[
          len(
            redundant_prefix
          ):
        ]
      )
      line = (
        leading
        + stripped
        + trailing
      )
      break

    normalized.append(
      line
    )

  return normalized


'''

    text = narrative_path.read_text(
        encoding="utf-8",
    )

    if helper not in text:
        if insertion_anchor not in text:
            raise RuntimeError(
                "public narrative normalization insertion anchor not found"
            )
        text = text.replace(
            insertion_anchor,
            helper + insertion_anchor,
            1,
        )
        narrative_path.write_text(
            text,
            encoding="utf-8",
        )
        print(
            "[updated] add Phase159 R4 proof-body prose normalizer"
        )
    else:
        print(
            "[already applied] add Phase159 R4 proof-body prose normalizer"
        )

    replace_once(
        narrative_path,
        '''  proof_body = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )

  lines = [
''',
        '''  proof_body = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )
  proof_body = (
    _phase159_r1_7c_r4_normalize_proof_body_prose(
      proof_body
    )
  )

  lines = [
''',
        "connect proof-body prose normalizer",
    )

    short_test_path = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py"
    )

    replace_once(
        short_test_path,
        '''  expected = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
''',
        '''  expected = (
    "この完全性と, 左の写像の単射性, "
    "右の写像の全射性より, "
    "次の短完全列が成り立つ."
  )
''',
        "short exact helper expectation",
    )

    replace_once(
        short_test_path,
        '''  reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
''',
        '''  reason = (
    "この完全性と, 左の写像の単射性, "
    "右の写像の全射性より, "
    "次の短完全列が成り立つ."
  )
''',
        "short exact visible prose expectation",
    )

    punctuation_test_path = (
        REPO_ROOT
        / "tests/test_phase157_r11_reference_reason_punctuation.py"
    )

    replace_once(
        punctuation_test_path,
        '''  short_exact_reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
''',
        '''  short_exact_reason = (
    "この完全性と, 左の写像の単射性, "
    "右の写像の全射性より, "
    "次の短完全列が成り立つ."
  )
''',
        "Phase157 short exact public expectation",
    )

    final_test_path = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py"
    )

    text = final_test_path.read_text(
        encoding="utf-8",
    )
    anchor = '''  assert "中央の群を生成する" in sentence
  assert rendered.count(sentence) == 1
'''
    replacement = '''  assert "中央の群を生成する" in sentence
  assert "である." not in sentence
  assert "であるから" not in sentence
  assert rendered.count(sentence) == 1
'''

    if replacement not in text:
        count = text.count(
            anchor
        )
        if count != 1:
            raise RuntimeError(
                "FINAL_GROUP_STRUCTURE test anchor count "
                f"must be 1, found {count}"
            )
        final_test_path.write_text(
            text.replace(
                anchor,
                replacement,
                1,
            ),
            encoding="utf-8",
        )
        print(
            "[updated] final group structure normalized prose assertions"
        )
    else:
        print(
            "[already applied] final group structure normalized prose assertions"
        )

    focused_test = (
        REPO_ROOT
        / "tests/test_phase159_r1_7c_r4_repair1_residual_proof_prose_normalization.py"
    )

    focused_test.write_text(
        (
            PACKAGE_DIR
            / "test_phase159_r1_7c_r4_repair1_residual_proof_prose_normalization.py"
        ).read_text(
            encoding="utf-8",
        ),
        encoding="utf-8",
    )
    print(
        "[added] Phase159 R4 repair1 focused regression test"
    )

    print("")
    print("Phase 159 R1-7c R4 repair1 applied.")
    print("Production files changed: 3")
    print("Existing test files changed: 3")
    print("Focused test file added: 1")
    print("Imports changed: none")


if __name__ == "__main__":
    main()
