from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent

RUNNER = (
  PACKAGE_ROOT
  / "run_phase156_closure.ps1"
)
VALIDATOR = (
  PACKAGE_ROOT
  / "validate_phase156_closure_documents.py"
)


def main() -> int:
  runner = RUNNER.read_text(
    encoding="utf-8-sig",
  )
  validator = VALIDATOR.read_text(
    encoding="utf-8",
  )

  required_runner_fragments = (
    "$BuilderScript = Join-Path",
    "$ValidatorScript = Join-Path",
    "$PackageRoot",
  )

  forbidden_runner_fragments = (
    r".\phase156_closure\build_phase156_closure_documents.py",
    r".\phase156_closure\validate_phase156_closure_documents.py",
  )

  failures = []

  for fragment in required_runner_fragments:
    if fragment not in runner:
      failures.append(
        (
          "missing runner fragment",
          fragment,
        )
      )

  for fragment in forbidden_runner_fragments:
    if fragment in runner:
      failures.append(
        (
          "stale hard-coded runner path",
          fragment,
        )
      )

  if "unique groups: 112" not in validator:
    failures.append(
      (
        "validator marker",
        "unique groups: 112",
      )
    )

  if "112 unique groups" in validator:
    failures.append(
      (
        "stale validator marker",
        "112 unique groups",
      )
    )

  if failures:
    print(
      "FAIL: closure package self-check"
    )

    for failure in failures:
      print(
        "  "
        + repr(
          failure
        )
      )

    return 1

  print(
    "PASS: closure package uses its own builder/validator "
    "and contains the corrected proof_records marker."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
