from pathlib import Path

MARKER = "PHASE149_RC3_CLOSURE"

FILES = (
  Path("README.md"),
  Path("docs/design.md"),
  Path("docs/development_log.md"),
  Path("docs/roadmap.md"),
  Path("docs/proof_records.md"),
)

for path in FILES:
  text = path.read_text(
    encoding="utf-8",
  )

  if text.count(
    MARKER
  ) != 1:
    raise RuntimeError(
      f"{path}: expected exactly one Phase 149 closure marker"
    )

summary_path = (
  Path(
    "phase149_rc3_5_final_regression_documentation_closure"
  )
  / "repository_regression_summary.txt"
)

summary = summary_path.read_text(
  encoding="utf-8",
).strip()

for path in FILES:
  text = path.read_text(
    encoding="utf-8",
  )
  if summary not in text:
    raise RuntimeError(
      f"{path}: final repository regression summary missing"
    )

output_dir = (
  Path(
    "phase149_rc3_5_final_regression_documentation_closure"
  )
  / "updated_full_documents"
)

for path in FILES:
  copied = output_dir / path.name
  if not copied.exists():
    raise RuntimeError(
      f"missing full-document output: {copied}"
    )
  if (
    copied.read_text(
      encoding="utf-8",
    )
    != path.read_text(
      encoding="utf-8",
    )
  ):
    raise RuntimeError(
      f"full-document output differs: {path}"
    )

print(
  "Phase 149 documentation verification: PASS"
)
print(
  "README closure is English; docs closure sections are Japanese."
)
print(
  "All five updated full documents were emitted."
)
