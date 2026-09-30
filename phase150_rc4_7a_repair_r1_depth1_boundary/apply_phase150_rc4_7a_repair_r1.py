from pathlib import Path

RENDERER = Path("toda_group_proof_narrative_renderer.py")
TEST = Path("tests/test_phase150_rc4_7a_cross_group_reference_normalization.py")


def replace_once(text, old, new, label):
  if old not in text:
    raise RuntimeError(f"target not found: {label}")
  if text.count(old) != 1:
    raise RuntimeError(f"target is not unique: {label}")
  return text.replace(old, new, 1)


def patch_renderer():
  text = RENDERER.read_text(encoding="utf-8")

  old = """  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries
    )
  )
  reference_marker_by_step_id = {
    id(proof_step): f"[R{entry.number}]"
    for entry in reference_entries
    for proof_step in entry.proof_steps
  }
"""

  new = """  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
    if presentation.max_depth >= 2
    else ()
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries
    )
  )
  reference_marker_by_step_id = {
    id(proof_step): f"[R{entry.number}]"
    for entry in reference_entries
    for proof_step in entry.proof_steps
  }
"""

  text = replace_once(
    text,
    old,
    new,
    "depth-2 Reference boundary",
  )
  RENDERER.write_text(text, encoding="utf-8")


def patch_test():
  text = TEST.read_text(encoding="utf-8")

  addition = r"""

def test_phase150_rc4_7a_depth1_keeps_legacy_reference_free_fallback(
):
  report = build_standard_toda_report(
    n=8,
    k=7,
  )
  group_result = report.candidates[0].source_candidate.group_result

  from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
  )

  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=1,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert "## 使用する結果" not in rendered
  assert "[R1]" not in rendered
"""

  if "test_phase150_rc4_7a_depth1_keeps_legacy_reference_free_fallback" not in text:
    text += addition

  TEST.write_text(text, encoding="utf-8")


def main():
  patch_renderer()
  patch_test()
  print("Phase 150 RC4-7A Repair R1 applied.")
  print("Changed: toda_group_proof_narrative_renderer.py::render_toda_group_proof_narrative_markdown")
  print("Changed: tests/test_phase150_rc4_7a_cross_group_reference_normalization.py")
  print("Boundary restored: depth=1 keeps legacy Reference-free fallback.")
  print("RC4-7A Reference normalization remains enabled for depth>=2.")


if __name__ == "__main__":
  main()
