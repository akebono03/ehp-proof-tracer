from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST = ROOT / "tests" / "test_phase143_42_argument_body_contribution_renderer.py"

OLD = r'''def test_phase143_42_pi6_3_group_keeps_derived_short_exact_sequence():
  (
    presentation,
    blocks,
    _argument,
    local_body_blocks,
    primary_component,
  ) = _argument_body_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  rendered = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      local_body_blocks,
      primary_component,
    )
  )

  assert (
    "この完全性と両端の写像の性質より, "
    "次の短完全列を得る."
    in rendered
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )
'''

NEW = r'''def test_phase143_42_pi6_3_group_keeps_derived_short_exact_sequence():
  (
    presentation,
    blocks,
    _argument,
    local_body_blocks,
    primary_component,
  ) = _argument_body_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  rendered = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      local_body_blocks,
      primary_component,
    )
  )

  assert (
    "この完全性と、左の写像が単射、"
    "右の写像が全射であることより、"
    "次の短完全列を得る."
    in rendered
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )
'''


def main() -> None:
  text = TEST.read_text(encoding="utf-8")

  if NEW in text:
    print("R1 test expectation already repaired.")
    return

  count = text.count(OLD)
  if count != 1:
    raise RuntimeError(
      "Expected exactly one old Phase143-42 test function; "
      f"found {count}"
    )

  TEST.write_text(
    text.replace(OLD, NEW, 1),
    encoding="utf-8",
  )
  print("RC4-5E-2-R1 stale expectation repaired.")
  print("Changed test only:")
  print("  tests/test_phase143_42_argument_body_contribution_renderer.py")
  print("Production changes: none.")


if __name__ == "__main__":
  main()
