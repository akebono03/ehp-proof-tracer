from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

TEST = ROOT / "tests" / "test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py"


TEST_SOURCE = r'''from toda_calculation_facade import (
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


def _pi3_2_public_narrative() -> str:
  report = build_standard_toda_report(
    n=2,
    k=1,
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


def test_phase159_r1_7c_r4_pi3_2_keeps_only_longer_exact_sequence():
  rendered = _pi3_2_public_narrative()
  paragraphs = tuple(
    paragraph.strip()
    for paragraph in rendered.split(
      "\n\n"
    )
  )

  longer_core = (
    r"\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}"
  )
  shorter_bare = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1}$."
  )
  shorter_exact = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1}$ は完全である."
  )

  assert any(
    longer_core
    in paragraph
    for paragraph in paragraphs
  )
  assert shorter_bare not in paragraphs
  assert shorter_exact not in paragraphs


def test_phase159_r1_7c_r4_pi3_2_keeps_injective_surjective_structure():
  rendered = _pi3_2_public_narrative()

  assert (
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    in rendered
  )
  assert "は単射" in rendered
  assert "は全射" in rendered
  assert "(1), (2) より" in rendered
  assert "は同型" in rendered


def test_phase159_r1_7c_r4_pi3_2_eta2_wording_is_unchanged():
  rendered = _pi3_2_public_narrative()

  assert (
    "この同型写像により"
    in rendered
  )
  assert (
    r"H(\eta_{2}) = \iota_{3}"
    in rendered
    or r"H\left(\eta_{2}\right) = \iota_{3}"
    in rendered
  )
  assert (
    r"\eta_{2} \in \pi_{3}^{2}"
    in rendered
  )
'''


def main() -> None:
    BACKUP.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        TEST,
        BACKUP / TEST.name,
    )

    TEST.write_text(
        TEST_SOURCE,
        encoding="utf-8",
    )

    print(
        "Phase 159 R1-7c R4 exact-sequence subsequence suppression repair1 fix1 applied."
    )
    print(
        "Production code changes: none"
    )
    print(
        "Updated focused test formatting expectations only."
    )


if __name__ == "__main__":
    main()
