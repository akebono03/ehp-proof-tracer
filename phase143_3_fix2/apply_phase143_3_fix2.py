from pathlib import Path

path = Path("tests/test_phase142_3_generic_proof_text.py")
text = path.read_text(encoding="utf-8")

old = r"""  assert r"2\nu' = \eta_{3}\eta_{4}\eta_{5}" in rendered
"""
new = r"""  assert r"2\nu' = \eta_{3}^{3}" in rendered
"""

if old not in text:
    raise RuntimeError(
        "Phase 142-3 expectation was not found; no file was changed."
    )

path.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
)
print("Updated:", path)
