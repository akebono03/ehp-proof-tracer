from pathlib import Path

TARGET = Path(
  "tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py"
)

if not TARGET.exists():
  raise SystemExit(f"missing test file: {TARGET}")

source = TARGET.read_text(encoding="utf-8")

old = '''from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_report import (
  build_standard_toda_report,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)
'''

new = '''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)
'''

if old not in source:
  if new in source:
    print("RC4-7D-3 canonical import section already installed.")
    raise SystemExit(0)
  raise SystemExit("expected current import section not found")

TARGET.write_text(
  source.replace(old, new, 1),
  encoding="utf-8",
)

print("RC4-7D-3 canonical test import section installed.")
print("Production files changed: none.")
