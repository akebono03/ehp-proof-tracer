from pathlib import Path

path = Path(
  "phase143_75an_impl/"
  "test_phase143_75an_indeterminacy_rendering.py"
)
text = path.read_text(encoding="utf-8")

old = '      r"2E^{n - 3}\\nu^{\\prime}"'
new = '      r"2E^{n - 3}\\nu\'"'

if old not in text:
  if new in text:
    print(
      "Phase 143-75AN-R2 test expectation "
      "already repaired."
    )
  else:
    raise RuntimeError(
      "target nu-prime expectation not found"
    )
else:
  text = text.replace(old, new, 1)
  compile(text, str(path), "exec")
  path.write_text(text, encoding="utf-8")
  print(
    "Phase 143-75AN-R2 test expectation "
    "repaired."
  )
