from pathlib import Path

TARGET = Path("tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py")

if not TARGET.exists():
  raise SystemExit(f"missing test file: {TARGET}")

source = TARGET.read_text(encoding="utf-8")

old = '''from toda_group_proof_replay import (
  build_toda_group_result_proof_replay,
)
'''
new = '''from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
'''

if old not in source:
  if new in source:
    print("RC4-7D-3 test import already repaired.")
    raise SystemExit(0)
  raise SystemExit(
    "expected incorrect replay import not found"
  )

TARGET.write_text(
  source.replace(
    old,
    new,
    1,
  ),
  encoding="utf-8",
)

print("RC4-7D-3 test import repaired.")
print("Production files changed: none.")
