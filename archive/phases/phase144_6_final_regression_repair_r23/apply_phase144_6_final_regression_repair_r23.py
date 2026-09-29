from pathlib import Path

path = Path("tests/test_phase143_61b_r_semantic_suppression_priority.py")
text = path.read_text(encoding="utf-8-sig")

old = '''def test_phase143_61b_r_keeps_pi6_3_local_connector():
  rendered = _render(
    3,
    3,
  )

  assert "これらより、" in rendered
  assert (
    "以上より、\\n\\n"
    r"$\\operatorname{ord}\\left(\\nu'\\right) = 4$"
    in rendered
  )
'''

new = '''def test_phase143_61b_r_keeps_pi6_3_local_connector():
  rendered = _render(
    3,
    3,
  )

  assert "(1) と (2) より、" in rendered
  assert "(4) と (5) より、" in rendered
  assert (
    "以上より、\\n\\n"
    r"$\\operatorname{ord}\\left(\\nu'\\right) = 4$"
    in rendered
  )
'''

if old not in text:
    raise RuntimeError(
        "Phase143-61b-R stale connector test anchor not found"
    )

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Phase 144-6 R23 applied.")
print("Production changes: none.")
print("Test updated:")
print("  tests/test_phase143_61b_r_semantic_suppression_priority.py")
print("  test_phase143_61b_r_keeps_pi6_3_local_connector")
