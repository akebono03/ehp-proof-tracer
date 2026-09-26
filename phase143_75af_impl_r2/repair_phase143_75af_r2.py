from pathlib import Path

path = Path(
  "phase143_75af_impl/"
  "test_phase143_75af_first_summand_rendering.py"
)
text = path.read_text(encoding="utf-8")

old = (
  r'    r"\left.\left(E\beta + \delta\right)"'
  "\n"
  r'    r"\right|_{\pi_{11}^{5}}"'
  "\n"
  r'    r" = E: \pi_{11}^{5} \to \pi_{12}^{6}"'
)

new = (
  r'    r"\left.\left(Eβ + δ\right)"'
  "\n"
  r'    r"\right|_{\pi_{11}^{5}}"'
  "\n"
  r'    r" = E: \pi_{11}^{5} \to \pi_{12}^{6}"'
)

if old not in text:
  if new in text:
    print(
      "Phase 143-75AF R2 test expectation "
      "already corrected."
    )
  else:
    raise RuntimeError(
      "Phase 143-75AF expected test anchor "
      "not found"
    )
else:
  text = text.replace(
    old,
    new,
    1,
  )
  path.write_text(
    text,
    encoding="utf-8",
  )
  print(
    "Phase 143-75AF R2 corrected only "
    "the Unicode renderer expectation."
  )
