from pathlib import Path

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

wrong = r'''      + r" \\text{ is the zero map}"'''
correct = r'''      + r" \text{ is the zero map}"'''

count = text.count(wrong)

if count != 1:
  raise RuntimeError(
    "expected exactly one Phase 143-75AE "
    f"double-backslash zero-map rendering, found {count}"
  )

text = text.replace(
  wrong,
  correct,
  1,
)

path.write_text(
  text,
  encoding="utf-8",
)

print(
  "Phase 143-75AE R3 corrected "
  "double-backslash LaTeX escape."
)
