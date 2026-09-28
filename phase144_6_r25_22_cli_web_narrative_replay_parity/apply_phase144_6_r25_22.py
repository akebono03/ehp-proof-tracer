from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_PATH = ROOT / "web_group_proof.py"


def _replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )
  return text.replace(
    old,
    new,
    1,
  )


def main() -> int:
  text = WEB_PATH.read_text(
    encoding="utf-8",
  )

  old_import = """from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
"""
  new_import = """from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)
"""

  text = _replace_once(
    text,
    old_import,
    new_import,
    "web replay import",
  )

  old_rendered_lines = """  rendered_lines = ()

  if mode != "trace":
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )

    if mode == "outline":
      markdown = (
        render_toda_group_proof_outline_markdown(
          presentation
        )
      )
    else:
      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )

    rendered_lines = (
      _build_group_proof_rendered_lines(
        markdown
      )
    )
"""

  new_rendered_lines = """  rendered_lines = ()

  if mode != "trace":
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

    if mode == "outline":
      markdown = (
        render_toda_group_proof_outline_markdown(
          presentation
        )
      )
    else:
      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )

    rendered_lines = (
      _build_group_proof_rendered_lines(
        markdown
      )
    )
"""

  text = _replace_once(
    text,
    old_rendered_lines,
    new_rendered_lines,
    "web rendered-lines branch",
  )

  WEB_PATH.write_text(
    text,
    encoding="utf-8",
  )

  print("R25-22 production repair applied.")
  print("Changed production file: web_group_proof.py")
  print("Trace replay semantics: unchanged.")
  print("Outline replay semantics: unchanged.")
  print("Narrative presentation replay: complete replay.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
