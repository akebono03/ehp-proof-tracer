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

  if (
    "build_complete_toda_group_result_proof_replay"
    not in text
  ):
    raise RuntimeError(
      "R25-22 base repair is not present. "
      "Run R25-22 before R25-22-R2."
    )

  old = '''      if math_value:
        segments.append(
          WebGroupProofInlineSegmentView(
            kind="inline_math",
            value=math_value,
          )
        )
      else:
'''

  new = '''      if math_value:
        segment_kind = (
          "display_math"
          if r"\\tag{" in math_value
          else "inline_math"
        )
        segments.append(
          WebGroupProofInlineSegmentView(
            kind=segment_kind,
            value=math_value,
          )
        )
      else:
'''

  text = _replace_once(
    text,
    old,
    new,
    "Web inline-segment adapter",
  )

  WEB_PATH.write_text(
    text,
    encoding="utf-8",
  )

  print("R25-22-R2 Web numbered-equation adapter repair applied.")
  print("Changed production file: web_group_proof.py")
  print("Changed function: _build_group_proof_inline_segments")
  print("Only inline math containing \\tag{...} is promoted to display_math.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
