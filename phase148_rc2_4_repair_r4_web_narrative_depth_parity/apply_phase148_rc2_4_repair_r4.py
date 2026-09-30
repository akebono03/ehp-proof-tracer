from pathlib import Path


TARGET = Path("web_group_proof.py")
SNAPSHOT_DIR = Path(
  "phase148_rc2_4_repair_r4_web_narrative_depth_parity"
)


OLD_IMPORT = """from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)
"""

NEW_IMPORT = """from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
"""


OLD_BRANCH = """  if mode != "trace":
    presentation_replay = replay

    if mode == "narrative":
      presentation_replay = (
        build_complete_toda_group_result_proof_replay(
          group_result
        )
      )

    presentation = (
      build_toda_group_proof_presentation(
        presentation_replay
      )
    )
"""

NEW_BRANCH = """  if mode != "trace":
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )
"""


def _extract_import_snapshot(
  text: str,
) -> str:
  marker = "\n\n@dataclass"
  index = text.find(
    marker
  )
  if index < 0:
    raise RuntimeError(
      "Could not locate end of import section."
    )
  return text[
    :index
  ].rstrip() + "\n"


def _extract_function_snapshot(
  text: str,
) -> str:
  marker = (
    "def build_standard_web_group_proof_view(\n"
  )
  start = text.find(
    marker
  )
  if start < 0:
    raise RuntimeError(
      "Could not locate "
      "build_standard_web_group_proof_view."
    )
  return text[
    start:
  ].rstrip() + "\n"


def main() -> int:
  text = TARGET.read_text(
    encoding="utf-8"
  )

  if NEW_IMPORT in text and OLD_BRANCH not in text:
    print(
      "RC2-4 Repair R4 already applied."
    )
  else:
    if text.count(
      OLD_IMPORT
    ) != 1:
      raise RuntimeError(
        "Expected exactly one complete-replay "
        "import block."
      )
    if text.count(
      OLD_BRANCH
    ) != 1:
      raise RuntimeError(
        "Expected exactly one Narrative "
        "complete-replay branch."
      )

    text = text.replace(
      OLD_IMPORT,
      NEW_IMPORT,
      1,
    )
    text = text.replace(
      OLD_BRANCH,
      NEW_BRANCH,
      1,
    )
    TARGET.write_text(
      text,
      encoding="utf-8",
      newline="\n",
    )

  updated = TARGET.read_text(
    encoding="utf-8"
  )
  SNAPSHOT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    SNAPSHOT_DIR
    / "updated_web_group_proof_imports.py.txt"
  ).write_text(
    _extract_import_snapshot(
      updated
    ),
    encoding="utf-8",
    newline="\n",
  )
  (
    SNAPSHOT_DIR
    / (
      "updated_build_standard_web_group_"
      "proof_view.py.txt"
    )
  ).write_text(
    _extract_function_snapshot(
      updated
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "RC2-4 Repair R4 applied."
  )
  print(
    "Changed production file: web_group_proof.py"
  )
  print(
    "Narrative now uses the same bounded replay "
    "selected by max_depth."
  )
  print(
    "Semantic dependency closure remains the "
    "responsibility of the existing Narrative renderer."
  )
  print(
    "Trace / Outline behavior is unchanged."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
