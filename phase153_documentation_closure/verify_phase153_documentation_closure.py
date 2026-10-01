from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

FILES = (
  Path("README.md"),
  Path("docs/design.md"),
  Path("docs/development_log.md"),
  Path("docs/roadmap.md"),
  Path("docs/proof_records.md"),
)

MARKER = "<!-- PHASE153_CLOSURE -->"


def main() -> None:
  failures = []

  for relative_path in FILES:
    path = REPO_ROOT / relative_path
    text = path.read_text(
      encoding="utf-8-sig"
    )
    count = text.count(
      MARKER
    )

    if count != 1:
      failures.append(
        (
          relative_path.as_posix(),
          "marker_count",
          count,
        )
      )

    output = (
      REPO_ROOT
      / "phase153_documentation_closure"
      / "output_full_documents"
      / relative_path
    )

    if not output.is_file():
      failures.append(
        (
          relative_path.as_posix(),
          "missing_full_output",
        )
      )
      continue

    output_text = output.read_text(
      encoding="utf-8-sig"
    )

    if output_text != text:
      failures.append(
        (
          relative_path.as_posix(),
          "full_output_mismatch",
        )
      )

  print(
    "=" * 72
  )
  print(
    "Phase 153 documentation closure verification"
  )
  print(
    "=" * 72
  )

  if failures:
    for failure in failures:
      print(
        "FAIL:",
        failure,
      )
    raise SystemExit(
      1
    )

  print(
    "PASS"
  )
  print(
    "All five documents contain exactly one Phase 153 closure section."
  )
  print(
    "Full-file outputs match the updated repository documents."
  )


if __name__ == "__main__":
  main()
