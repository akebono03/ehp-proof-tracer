from pathlib import Path
import shutil


package_root = Path(__file__).resolve().parent
repo_root = package_root.parent
sections = package_root / "sections"
generated = package_root / "generated_full_docs"


def read_section(
  name: str,
) -> str:
  return (
    sections
    / name
  ).read_text(
    encoding="utf-8",
  ).rstrip() + "\n"


def append_once(
  path: Path,
  marker: str,
  section: str,
) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  if marker in text:
    raise SystemExit(
      "Phase 160 documentation marker "
      "already exists in "
      + str(
        path
      )
    )

  path.write_text(
    text.rstrip()
    + "\n\n\n"
    + section,
    encoding="utf-8",
  )


readme = repo_root / "README.md"

readme_text = readme.read_text(
  encoding="utf-8",
)

old_stem2 = (
  r"\pi_{n+2}^n=\mathbb Z/2\{\eta_n\eta_{n+1}\},"
)
new_stem2 = (
  r"\pi_{n+2}^n=\mathbb Z/2\{\eta_n^2\},"
)

if old_stem2 in readme_text:
  readme_text = readme_text.replace(
    old_stem2,
    new_stem2,
  )

readme.write_text(
  readme_text,
  encoding="utf-8",
)

append_once(
  readme,
  "<!-- PHASE160_DOCUMENTATION_CLOSURE -->",
  read_section(
    "README_phase160.md"
  ),
)

append_once(
  repo_root / "docs" / "design.md",
  "<!-- PHASE160_DOCUMENTATION_CLOSURE -->",
  read_section(
    "design_phase160.md"
  ),
)

append_once(
  repo_root / "docs" / "development_log.md",
  "<!-- PHASE160_DOCUMENTATION_CLOSURE -->",
  read_section(
    "development_log_phase160.md"
  ),
)

append_once(
  repo_root / "docs" / "roadmap.md",
  "<!-- PHASE160_DOCUMENTATION_CLOSURE -->",
  read_section(
    "roadmap_phase160.md"
  ),
)

append_once(
  repo_root / "docs" / "proof_records.md",
  "<!-- PHASE160_DOCUMENTATION_CLOSURE -->",
  read_section(
    "proof_records_phase160.md"
  ),
)


if generated.exists():
  shutil.rmtree(
    generated
  )

(generated / "docs").mkdir(
  parents=True
)

shutil.copy2(
  readme,
  generated / "README.md",
)

for name in (
  "design.md",
  "development_log.md",
  "roadmap.md",
  "proof_records.md",
):
  shutil.copy2(
    repo_root / "docs" / name,
    generated / "docs" / name,
  )


print("Applied Phase 160 documentation closure:")
print("  README.md")
print("  docs/design.md")
print("  docs/development_log.md")
print("  docs/roadmap.md")
print("  docs/proof_records.md")
print("")
print("Full updated files were also copied to:")
print("  phase160_documentation_closure/generated_full_docs/")
print("")
print("No tests were run.")
