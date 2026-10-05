from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "tests" / "test_phase150_rc4_5c_2_exactness_to_map_property.py"

OLD_FUNCTION = 'def test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion():\n  (\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    reason_sidecar,\n  ) = _pi6_reason_data()\n\n  reason = next(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .EXACTNESS_TO_MAP_PROPERTY\n    )\n  )\n  sentence = (\n    render_toda_group_proof_narrative_reason_sentence(\n      reason\n    )\n  )\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n\n  assert sentence == (\n    "この完全性と $Δ=0$ より, "\n    "$\\\\ker E=\\\\operatorname{Im}Δ=0$ である.\\n"\n    "したがって, "\n  )\n  assert rendered.count(sentence) == 1\n\n  conclusion = (\n    "$E: \\\\pi_{5}^{2} \\\\to \\\\pi_{6}^{3}$ "\n    "は単射である."\n  )\n  assert conclusion in rendered\n  assert rendered.index(sentence) < rendered.index(\n    conclusion\n  )\n'
NEW_FUNCTION = 'def test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion():\n  (\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    reason_sidecar,\n  ) = _pi6_reason_data()\n\n  reason = next(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .EXACTNESS_TO_MAP_PROPERTY\n    )\n  )\n  sentence = (\n    render_toda_group_proof_narrative_reason_sentence(\n      reason\n    )\n  )\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n\n  assert sentence == (\n    "この完全性と $Δ=0$ より, "\n    "$\\\\ker E=\\\\operatorname{Im}Δ=0$ である.\\n"\n    "したがって, "\n  )\n\n  reason_body = (\n    "この完全性と $Δ=0$ より, "\n    "$\\\\ker E=\\\\operatorname{Im}Δ=0$ である."\n  )\n  assert rendered.count(\n    reason_body\n  ) == 1\n\n  conclusion = (\n    "$E: \\\\pi_{5}^{2} \\\\to \\\\pi_{6}^{3}$ "\n    "は単射である."\n  )\n  assert conclusion in rendered\n  assert rendered.index(\n    reason_body\n  ) < rendered.index(\n    conclusion\n  )\n'

def main() -> None:
  if not TEST.exists():
    raise FileNotFoundError(TEST)
  stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  backup_dir = ROOT / ("phase159_r1_3_repair5_backup_" + stamp)
  backup_dir.mkdir(parents=True, exist_ok=False)
  shutil.copy2(TEST, backup_dir / TEST.name)

  source = TEST.read_text(encoding="utf-8-sig")
  count = source.count(OLD_FUNCTION)
  if count != 1:
    raise RuntimeError(
      "expected exactly one stale Phase 150 test function, found "
      + str(count)
    )

  source = source.replace(OLD_FUNCTION, NEW_FUNCTION, 1)
  TEST.write_text(source, encoding="utf-8", newline="\n")

  print("Phase 159-R1-3 repair5 applied.")
  print("Backup:", backup_dir)
  print("Production code changes: none")
  print("Repaired one stale Phase 150 connector expectation.")

if __name__ == "__main__":
  main()
