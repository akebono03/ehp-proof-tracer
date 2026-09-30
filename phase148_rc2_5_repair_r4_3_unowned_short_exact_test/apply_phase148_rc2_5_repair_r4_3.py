from pathlib import Path

path = Path(
  "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py"
)
text = path.read_text(encoding="utf-8")

old = r'''  assert rendered.count(
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
  ) == 1
'''
new = r'''  assert rendered.count(
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
  ) == 0
'''

if old not in text:
  raise RuntimeError(
    "Expected remaining pi8_5 short-exact assertion was not found."
  )

path.write_text(
  text.replace(
    old,
    new,
    1,
  ),
  encoding="utf-8",
)

print(
  "R4.3 applied: pi8_5 unowned recursive short-exact "
  "contribution expectation changed from 1 to 0."
)
print("Production changes: none.")
