from pathlib import Path

TARGET = Path("toda_proof_narrative_renderer.py")

text = TARGET.read_text(encoding="utf-8")

old = """      + render_toda_expression_latex(
        statement.sign_parameter
      )
      + r"\\text{ is the sign parameter}"
"""

new = """      + _render_scalar_latex(
        statement.sign_parameter
      )
      + r"\\text{ is the sign parameter}"
"""

count = text.count(old)
if count != 1:
  raise SystemExit(
    "Expected exactly one Phase 143-75AB-3 sign-parameter block; "
    f"found {count}."
  )

backup = TARGET.with_suffix(
  TARGET.suffix + ".phase143_75ab3_r2_backup"
)
if not backup.exists():
  backup.write_text(
    TARGET.read_text(encoding="utf-8"),
    encoding="utf-8",
  )

TARGET.write_text(
  text.replace(old, new, 1),
  encoding="utf-8",
)

print("Phase 143-75AB-3-R2 scalar-renderer repair applied.")
