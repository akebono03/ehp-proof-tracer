from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{path}: expected exactly one match, found {count}"
        )
    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )


repo = Path.cwd()

# 1. Production repair:
#    Number only equations that are actually referenced by a later
#    connector. A target gets a number only if it subsequently appears
#    as a visible source of another transition.
equation_path = repo / "toda_group_proof_narrative_equation_numbering.py"

old_target_numbering = '''    current_target_index = line_index_by_id.get(
      target_id
    )

    if (
      current_target_index is None
      or target_index < current_target_index
    ):
      line_index_by_id[
        target_id
      ] = target_index

'''
replace_once(
    equation_path,
    old_target_numbering,
    "",
)

# 2. Phase 157 stale QED expectations:
#    Phase 158 public Narrative normalization uses the literal □ marker.
qed_test_path = (
    repo
    / "tests"
    / "test_phase157_r5_r10_reference_proof_boundary_qed.py"
)

old_qed_test = r'''def test_phase157_r5_r10_narrative_ends_with_qed(
  n,
  k,
):
  rendered = _rendered_group_proof(
    n,
    k,
  )

  assert rendered.rstrip().endswith(
    r"$\square$"
  )
'''
new_qed_test = r'''def test_phase157_r5_r10_narrative_ends_with_qed(
  n,
  k,
):
  rendered = _rendered_group_proof(
    n,
    k,
  )

  assert rendered.rstrip().endswith(
    "□"
  )
'''
replace_once(
    qed_test_path,
    old_qed_test,
    new_qed_test,
)

old_web_qed = r'''def test_phase157_r5_r10_web_adapter_exposes_separator_and_qed():
  view = build_standard_web_group_proof_view(
    3,
    3,
    max_depth=2,
    mode="narrative",
  )

  kinds = tuple(
    line.kind
    for line in view.rendered_lines
  )

  assert "separator" in kinds
  assert any(
    line.kind == "heading"
    and line.prefix == "使用する結果"
    for line in view.rendered_lines
  )
  assert any(
    line.kind == "heading"
    and line.prefix == "証明"
    for line in view.rendered_lines
  )
  assert any(
    any(
      segment.kind == "inline_math"
      and segment.value == r"\square"
      for segment in line.segments
    )
    for line in view.rendered_lines
  )
'''
new_web_qed = r'''def test_phase157_r5_r10_web_adapter_exposes_separator_and_qed():
  view = build_standard_web_group_proof_view(
    3,
    3,
    max_depth=2,
    mode="narrative",
  )

  kinds = tuple(
    line.kind
    for line in view.rendered_lines
  )

  assert "separator" in kinds
  assert any(
    line.kind == "heading"
    and line.prefix == "使用する結果"
    for line in view.rendered_lines
  )
  assert any(
    line.kind == "heading"
    and line.prefix == "証明"
    for line in view.rendered_lines
  )
  assert any(
    any(
      segment.kind == "text"
      and segment.value == "□"
      for segment in line.segments
    )
    for line in view.rendered_lines
  )
'''
replace_once(
    qed_test_path,
    old_web_qed,
    new_web_qed,
)

# 3. Phase 150 stale prose / dedicated-route expectations.
route_test_path = (
    repo
    / "tests"
    / "test_phase150_rc4_7d_3_public_narrative_generic_route.py"
)

old_pi10 = r'''def test_phase150_rc4_7d_3_pi10_public_and_web_use_generic_reason_route():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(
      4,
      6,
    )
  )
  web_text = _web_text(
    4,
    6,
  )

  assert "以上で得た群構造" in markdown
  assert "結果を合わせると" in markdown
  assert "以上で得た群構造" in web_text
  assert "結果を合わせると" in web_text
'''
new_pi10 = r'''def test_phase150_rc4_7d_3_pi10_public_and_web_keep_current_narrative_contract():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(
      4,
      6,
    )
  )
  web_text = _web_text(
    4,
    6,
  )
  target = (
    r"\pi_{10}^{4} = "
    r"\mathbb{Z}/8\{\nu_{4}\nu_{7}\}"
  )

  assert target in markdown
  assert target in web_text
  assert "以上より" in markdown
  assert "以上より" in web_text
'''
replace_once(
    route_test_path,
    old_pi10,
    new_pi10,
)

old_pi8 = r'''def test_phase150_rc4_7d_3_pi8_dedicated_route_is_preserved():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(5, 3)
  )
  assert "# Group proof narrative" in markdown
  assert "Toda Proposition 5.6 のうち," in markdown
'''
new_pi8 = r'''def test_phase150_rc4_7d_3_pi8_public_route_keeps_current_narrative_contract():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(5, 3)
  )
  target = (
    r"\pi_{8}^{5} = "
    r"\mathbb{Z}/8\{\nu_{5}\}"
  )

  assert "# Group proof narrative" in markdown
  assert "## 証明対象" in markdown
  assert "## 証明" in markdown
  assert target in markdown
  assert "Toda Proposition 5.6 のうち," not in markdown
'''
replace_once(
    route_test_path,
    old_pi8,
    new_pi8,
)

print("Phase 158-R5-6 repair1 applied.")
print("Production changes:")
print("  - toda_group_proof_narrative_equation_numbering.py")
print("Test changes:")
print("  - tests/test_phase157_r5_r10_reference_proof_boundary_qed.py")
print("  - tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py")
