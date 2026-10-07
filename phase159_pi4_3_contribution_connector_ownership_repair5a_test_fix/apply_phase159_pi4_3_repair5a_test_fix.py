from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent

TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_contribution_connector_ownership.py"
)


def main() -> int:
  TEST_PATH.write_text(
    (
      PACKAGE_ROOT
      / "test_phase159_pi4_3_contribution_connector_ownership.py"
    ).read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 repair5a test-only return-order fix applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
