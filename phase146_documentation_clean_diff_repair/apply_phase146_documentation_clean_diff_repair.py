from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

TARGETS = (
  "docs/design.md",
  "docs/development_log.md",
  "docs/roadmap.md",
  "docs/proof_records.md",
)

REQUIRED_MARKERS = {
  "docs/design.md": (
    "Phase 146",
    "Phase 146 closure boundary",
    "RC1",
    "RC6",
  ),
  "docs/development_log.md": (
    "Phase 146",
    "Phase 146 完了境界",
    "RC1 Argument-method ownership",
    "RC6 Final equation numbering / prose formatting",
  ),
  "docs/roadmap.md": (
    "Phase 146 — 完了",
    "Phase 147 — RC1",
    "Phase 152 — RC6",
  ),
  "docs/proof_records.md": (
    "Phase 146 historical Narrative comparison / provenance record",
    "RC1 Argument-method ownership",
    "RC6 Final equation numbering / prose formatting",
  ),
}


def git_show_head(path):
  completed = subprocess.run(
    [
      "git",
      "show",
      f"HEAD:{path}",
    ],
    cwd=ROOT,
    check=True,
    stdout=subprocess.PIPE,
  )
  return completed.stdout.decode(
    "utf-8",
    errors="strict",
  )


def main():
  print("Checking canonical HEAD documentation before restore...")

  for target in TARGETS:
    text = git_show_head(
      target
    )
    missing = tuple(
      marker
      for marker in REQUIRED_MARKERS[
        target
      ]
      if marker not in text
    )
    if missing:
      print(
        "ABORT:",
        target,
        "does not contain required Phase 146 canonical markers.",
      )
      for marker in missing:
        print(
          "  missing:",
          marker,
        )
      print(
        "No documentation files were modified."
      )
      return 2

  print(
    "Canonical HEAD contains Phase 146 closure markers in all four files."
  )

  subprocess.run(
    [
      "git",
      "checkout",
      "--",
      *TARGETS,
    ],
    cwd=ROOT,
    check=True,
  )

  print(
    "Restored the four documentation files byte-for-byte from canonical HEAD."
  )

  for target in TARGETS:
    path = ROOT / target
    data = path.read_bytes()
    data.decode(
      "utf-8",
      errors="strict",
    )
    print(
      "UTF-8 strict decode PASS:",
      target,
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
