from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_documentation"
OUTPUT_ROOT = PACKAGE_ROOT / "updated_full_documents"

DOCS = (
  Path("README.md"),
  Path("docs/design.md"),
  Path("docs/development_log.md"),
  Path("docs/roadmap.md"),
  Path("docs/proof_records.md"),
)

MARKER = "<!-- PHASE154_DOCUMENTATION_CLOSURE -->"


def read_section(name: str) -> str:
  return (
    PACKAGE_ROOT
    / "sections"
    / name
  ).read_text(
    encoding="utf-8",
  ).rstrip() + "\n"


def backup(path: Path) -> None:
  relative = path.relative_to(REPO_ROOT)
  target = BACKUP_ROOT / relative
  target.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    target,
  )


def write_full(path: Path, text: str) -> None:
  path.write_text(
    text.rstrip() + "\n",
    encoding="utf-8",
  )


def append_once(
  path: Path,
  section: str,
  marker: str,
) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  if marker in text:
    print(
      "already-current:",
      path.relative_to(REPO_ROOT),
    )
    return

  backup(path)
  write_full(
    path,
    text.rstrip()
    + "\n\n"
    + section.rstrip()
    + "\n",
  )
  print(
    "updated:",
    path.relative_to(REPO_ROOT),
  )


def update_readme(path: Path) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  old = (
    "Phase 154 returns to proof-prose generation quality. "
    "Test-suite consolidation remains a\n"
    "separate deferred maintenance task."
  )

  new = (
    "Phase 154 has completed its proof-prose generation refinement and "
    "112-group closure audit. "
    "The repository-wide final full regression remains the Phase-final step. "
    "Test-suite consolidation remains a\n"
    "separate deferred maintenance task."
  )

  if old in text:
    backup(path)
    text = text.replace(
      old,
      new,
      1,
    )
  elif new not in text:
    raise RuntimeError(
      "README Phase 154 boundary sentence not found"
    )

  section = read_section(
    "README_PHASE154.md"
  )

  if "## Phase 154 proof-prose generation refinement" not in text:
    text = (
      text.rstrip()
      + "\n\n"
      + section.rstrip()
      + "\n"
    )

  write_full(
    path,
    text,
  )
  print(
    "updated:",
    path.relative_to(REPO_ROOT),
  )


def update_roadmap(path: Path) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  start_marker = (
    "## Phase 154 — Proof prose generation refinement"
  )
  end_marker = (
    "## Test Suite Consolidation — 保留"
  )

  start = text.find(
    start_marker
  )
  end = text.find(
    end_marker,
    start,
  )

  if start < 0 or end < 0:
    raise RuntimeError(
      "roadmap Phase 154 planned section boundary not found"
    )

  replacement = read_section(
    "ROADMAP_PHASE154.md"
  )

  backup(path)
  updated = (
    text[:start]
    + replacement.rstrip()
    + "\n\n"
    + text[end:]
  )

  write_full(
    path,
    updated,
  )
  print(
    "updated:",
    path.relative_to(REPO_ROOT),
  )


def copy_full_documents() -> None:
  for relative in DOCS:
    source = REPO_ROOT / relative
    target = OUTPUT_ROOT / relative
    target.parent.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      source,
      target,
    )


def main() -> int:
  for relative in DOCS:
    path = REPO_ROOT / relative
    if not path.exists():
      raise RuntimeError(
        "missing document: "
        + str(
          relative
        )
      )

  update_readme(
    REPO_ROOT
    / "README.md"
  )

  append_once(
    REPO_ROOT
    / "docs/design.md",
    read_section(
      "DESIGN_PHASE154.md"
    ),
    MARKER,
  )

  append_once(
    REPO_ROOT
    / "docs/development_log.md",
    read_section(
      "DEVELOPMENT_LOG_PHASE154.md"
    ),
    MARKER,
  )

  update_roadmap(
    REPO_ROOT
    / "docs/roadmap.md"
  )

  append_once(
    REPO_ROOT
    / "docs/proof_records.md",
    read_section(
      "PROOF_RECORDS_PHASE154.md"
    ),
    MARKER,
  )

  copy_full_documents()

  print()
  print(
    "Full updated documents copied to:"
  )
  print(
    "  "
    + str(
      OUTPUT_ROOT
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
