from pathlib import Path

path = Path("tests/test_phase143_47_multi_argument_shared_contribution_dedup.py")
text = path.read_text(encoding="utf-8")

old = r'''  assert rendered.count(
    r"$\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$ は完全である."
  ) >= 1
'''
new = r'''  assert rendered.count(
    r"$\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$ は完全である."
  ) == 0
'''

if old not in text:
    raise RuntimeError("Expected remaining R4.1 stale assertion was not found.")

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("R4.2 applied: one stale pi8_5 raw-exactness assertion changed from >= 1 to == 0.")
print("Production changes: none.")
