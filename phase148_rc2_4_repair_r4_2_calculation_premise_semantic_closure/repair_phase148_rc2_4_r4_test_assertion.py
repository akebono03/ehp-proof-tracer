from pathlib import Path


TARGET = Path(
  "tests/test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py"
)


OLD_ASSERTIONS = """  assert response.status_code == 200
  assert b"Selected depth:" in response.data
  assert b"Depth 2" in response.data
  assert b"\\\\\\\\tag{1}" in response.data
  assert (
    "は完全である".encode(
      "utf-8"
    )
    not in response.data
  )
"""

NEW_ASSERTIONS = """  assert response.status_code == 200
  assert b"Selected depth:" in response.data
  assert b"Selected depth: 2" in response.data
  assert b"\\\\\\\\tag{1}" in response.data
  assert (
    "は完全である".encode(
      "utf-8"
    )
    not in response.data
  )
"""


def main() -> int:
  text = TARGET.read_text(
    encoding="utf-8"
  )

  if NEW_ASSERTIONS in text:
    print(
      "R4 Web response assertion already repaired."
    )
    return 0

  if text.count(
    OLD_ASSERTIONS
  ) != 1:
    raise RuntimeError(
      "Expected exactly one stale R4 Web response assertion block."
    )

  TARGET.write_text(
    text.replace(
      OLD_ASSERTIONS,
      NEW_ASSERTIONS,
      1,
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Repaired stale R4 Web response assertion:"
  )
  print(
    "Depth 2 -> Selected depth: 2"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
