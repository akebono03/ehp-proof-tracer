from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "tests" / "test_phase144_6_pi6_generic_production_route.py"

OLD = '  assert "**[R1]" not in captured.out\n'
NEW = (
  '  assert "**[R1]" in captured.out\n'
  '  assert "(5.3) / Lemma 5.2" in captured.out\n'
  '  assert "**[R2]" in captured.out\n'
  '  assert "(5.2)" in captured.out\n'
  '  assert "Proposition 5.1" in captured.out\n'
  '  assert "Proposition 4.4" in captured.out\n'
  '  assert "Proposition 2.2" not in captured.out\n'
)


def main() -> int:
  text = PATH.read_text(encoding="utf-8-sig")

  if NEW in text:
    print("Phase 144-6-R3 CLI reference assertions already aligned.")
    return 0

  if text.count(OLD) != 1:
    raise RuntimeError(
      "expected exactly one pre-R3 CLI reference assertion"
    )

  PATH.write_text(
    text.replace(OLD, NEW, 1),
    encoding="utf-8",
  )

  print("Phase 144-6-R3 second-half R4 test alignment applied.")
  print(
    "Changed only: "
    "tests/test_phase144_6_pi6_generic_production_route.py"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
