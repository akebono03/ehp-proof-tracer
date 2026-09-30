from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST = ROOT / "tests" / "test_phase150_rc4_5f_2_final_group_structure_reason.py"

START = "def test_phase150_rc4_5f_2_final_reason_is_visible_before_final_group_conclusion():\n"
END = "\ndef test_phase150_rc4_5f_2_classifier_has_no_target_or_rule_name_special_case():\n"

REPLACEMENT = """def test_phase150_rc4_5f_2_final_reason_is_visible_before_final_group_conclusion():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reasons,
  ) = _pi6_final_reason_data()

  reason = reasons[0]
  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert sentence is not None
  assert "この短完全列と両端の群の位数より" in sentence
  assert r"中央の群の位数は $2\\cdot2=4$" in sentence
  assert "中央の群を生成する" in sentence
  assert rendered.count(sentence) == 1

  conclusion = r"$\\pi_{6}^{3} = \\mathbb{Z}/4\\{\\nu\'\\}$"
  assert conclusion in rendered
  assert rendered.index(sentence) < rendered.index(conclusion)

"""


def main() -> None:
  text = TEST.read_text(encoding="utf-8")
  start_index = text.find(START)
  if start_index < 0:
    raise RuntimeError("Target visible test function was not found.")
  end_index = text.find(END, start_index)
  if end_index < 0:
    raise RuntimeError("Next test function boundary was not found.")
  repaired = text[:start_index] + REPLACEMENT + text[end_index + 1:]
  TEST.write_text(repaired, encoding="utf-8")
  print("RC4-5F-2-R2 visible test function repaired.")
  print("Production changes: none.")


if __name__ == "__main__":
  main()
