from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent

BODY_RENDERER_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_argument_body_renderer.py"
)
TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_provenance_priority.py"
)


OLD_DISPLAY_FILTER = '''          and (
            (
              id(
                block
              ) in preserve_provenance_block_ids
              and id(
                proof_step
              ) in redundant_direct_premise_step_ids
            )
            or id(
              proof_step
            ) not in redundant_direct_premise_step_ids
          )
'''

NEW_DISPLAY_FILTER = '''          and id(
            proof_step
          ) not in redundant_direct_premise_step_ids
'''


def main() -> int:
  source = BODY_RENDERER_PATH.read_text(
    encoding="utf-8",
  )

  occurrence_count = source.count(
    OLD_DISPLAY_FILTER
  )

  if occurrence_count != 1:
    raise RuntimeError(
      "expected exactly one provenance-vs-redundant "
      "display filter, found "
      + str(
        occurrence_count
      )
    )

  updated = source.replace(
    OLD_DISPLAY_FILTER,
    NEW_DISPLAY_FILTER,
    1,
  )

  BODY_RENDERER_PATH.write_text(
    updated,
    encoding="utf-8",
  )

  TEST_PATH.write_text(
    (
      PACKAGE_ROOT
      / "test_phase159_pi4_3_provenance_priority.py"
    ).read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 provenance-priority repair3 applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
