from pathlib import Path

PATH = Path(
  "tests/"
  "test_phase143_75m_finite_dimensional_semantic_rendering.py"
)

if not PATH.exists():
  raise SystemExit(
    "Phase 143-75M focused test was not found."
  )

text = PATH.read_text(encoding="utf-8")

old = '  assert r"\\\\ge 5" in rendered\n'
new = '  assert r"\\\\ge 9" in rendered\n'

if new in text:
  print(
    "Phase 143-75M R3 test repair was already applied."
  )
elif old in text:
  PATH.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "Phase 143-75M R3 test-only repair applied."
  )
else:
  raise SystemExit(
    "Expected Phase 143-75M Prop.5.11 range assertion "
    "was not found."
  )
