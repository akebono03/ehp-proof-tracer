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

function_name = (
  "def test_phase143_75m_prop511_renders_nu_squared_range():"
)
start = text.find(function_name)

if start < 0:
  raise SystemExit(
    "Prop.5.11 focused test function was not found."
  )

next_function = text.find(
  "\ndef ",
  start + len(function_name),
)

if next_function < 0:
  end = len(text)
else:
  end = next_function + 1

replacement = '''def test_phase143_75m_prop511_renders_nu_squared_range():
  rendered = _target_facts()[
    "TodaProp511NuSquaredFiniteDimensionalStatement"
  ]

  assert r"\\ge 9" in rendered
  assert r"\\mathbb{Z}/2" in rendered
'''

new_text = (
  text[:start]
  + replacement
  + text[end:]
)

PATH.write_text(
  new_text,
  encoding="utf-8",
)

print(
  "Phase 143-75M R4 test-only repair applied."
)
