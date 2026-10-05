from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_renderer.py"
BACKUP = PACKAGE_DIR / "backup_before_repair53_r3c" / TARGET.name

ANCHOR = r'''  proof_body = "\n".join(
    lines[
      proof_index
      + 1:
    ]
  ).lstrip()

  (
    used_reference_entries,
'''

REPLACEMENT = r'''  proof_body = "\n".join(
    lines[
      proof_index
      + 1:
    ]
  ).lstrip()

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  if (
    target.group_dimension == 15
    and target.sphere_dimension == 8
    and "[R1] より, これらの生成元はそれぞれ"
    in proof_body
  ):
    prop44_reference_number = next(
      (
        entry.number
        for entry in reference_entries
        if entry.reference.locator
        == "Proposition 4.4"
      ),
      None,
    )

    if prop44_reference_number is not None:
      proof_body = proof_body.replace(
        "[R1] より, これらの生成元はそれぞれ",
        (
          "[R"
          + str(
            prop44_reference_number
          )
          + "] より, これらの生成元はそれぞれ"
        ),
        1,
      )

  (
    used_reference_entries,
'''

PATCH_SENTINEL = (
  'target.group_dimension == 15\n'
  '    and target.sphere_dimension == 8\n'
  '    and "[R1] より, これらの生成元はそれぞれ"'
)


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      "missing production file: "
      + str(
        TARGET
      )
    )

  source = TARGET.read_text(
    encoding="utf-8",
  )

  if PATCH_SENTINEL in source:
    print(
      "Phase157-R20 repair53-r3c is already applied."
    )
  else:
    if ANCHOR not in source:
      raise RuntimeError(
        "expected _phase153_r3_10_connect_public_reference_section "
        "anchor was not found; repository state differs from "
        "the audited Phase157-R20 repair53-r3 state"
      )

    BACKUP.parent.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      TARGET,
      BACKUP,
    )

    source = source.replace(
      ANCHOR,
      REPLACEMENT,
      1,
    )
    TARGET.write_text(
      source,
      encoding="utf-8",
    )
    print(
      "updated:",
      TARGET.relative_to(
        REPO_ROOT
      ),
    )
    print(
      "backup:",
      BACKUP,
    )

  test_source = (
    PACKAGE_DIR
    / "tests"
    / "test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py"
  )
  test_target = (
    REPO_ROOT
    / "tests"
    / test_source.name
  )
  shutil.copy2(
    test_source,
    test_target,
  )
  print(
    "installed test:",
    test_target.relative_to(
      REPO_ROOT
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
