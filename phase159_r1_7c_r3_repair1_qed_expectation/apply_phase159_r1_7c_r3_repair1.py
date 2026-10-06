from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TEST_FILE = (
  REPO_ROOT
  / "tests"
  / "test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py"
)


OLD = '  assert body.rstrip().endswith(\n    r"$\\\\square$"\n  )\n'
NEW = '  assert body.rstrip().endswith(\n    "□"\n  )\n'


def main() -> None:
  if not TEST_FILE.exists():
    raise FileNotFoundError(
      f"focused test not found: {TEST_FILE}"
    )

  source = TEST_FILE.read_text(
    encoding="utf-8"
  )

  if NEW in source:
    print(
      "R3 repair1 already applied."
    )
    return

  count = source.count(
    OLD
  )

  if count != 1:
    raise RuntimeError(
      "expected exactly one stale QED expectation; "
      f"found {count}"
    )

  TEST_FILE.write_text(
    source.replace(
      OLD,
      NEW,
      1,
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R3 repair1 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Updated test:",
    TEST_FILE,
  )


if __name__ == "__main__":
  main()
