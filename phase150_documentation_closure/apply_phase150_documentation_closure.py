from pathlib import Path
import shutil

repo = Path.cwd()
package = Path(__file__).resolve().parent
marker = "<!-- PHASE150_CLOSURE -->"

targets = (
    (repo / "README.md", package / "README_PHASE150_APPEND.md"),
    (repo / "docs" / "design.md", package / "design_PHASE150_APPEND.md"),
    (repo / "docs" / "development_log.md", package / "development_log_PHASE150_APPEND.md"),
    (repo / "docs" / "roadmap.md", package / "roadmap_PHASE150_APPEND.md"),
    (repo / "docs" / "proof_records.md", package / "proof_records_PHASE150_APPEND.md"),
)

backup = repo / "phase150_documentation_closure_backup"
output = package / "output_full_documents"
backup.mkdir(parents=True, exist_ok=True)
output.mkdir(parents=True, exist_ok=True)

for target, appendix in targets:
  if not target.exists():
    raise SystemExit(f"Missing document: {target}")

  current = target.read_text(encoding="utf-8-sig")
  backup_target = backup / target.relative_to(repo)
  backup_target.parent.mkdir(parents=True, exist_ok=True)
  if not backup_target.exists():
    shutil.copy2(target, backup_target)

  if marker not in current:
    addition = appendix.read_text(encoding="utf-8")
    updated = current.rstrip() + "\n" + addition
    target.write_text(updated, encoding="utf-8")
    print(f"Updated: {target.relative_to(repo)}")
  else:
    print(f"Already contains Phase 150 closure: {target.relative_to(repo)}")

  full_output = output / target.relative_to(repo)
  full_output.parent.mkdir(parents=True, exist_ok=True)
  shutil.copy2(target, full_output)

print("")
print("Full updated documents written to:")
print(output)
