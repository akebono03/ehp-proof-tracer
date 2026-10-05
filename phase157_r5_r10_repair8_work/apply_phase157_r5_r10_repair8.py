from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"
BACKUP.mkdir(exist_ok=True)


def backup(path: Path) -> None:
    destination = BACKUP / path.name
    if not destination.exists():
        shutil.copy2(path, destination)


def replace_once(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        print(f"Already applied: {label}")
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"expected exactly one match for {label} in {path}, found {count}"
        )
    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )
    print(f"Applied: {label}")


phase144 = ROOT / "tests" / "test_phase144_6_r3_production_references.py"
phase156 = ROOT / "tests" / "test_phase156_r5_repair9_test_contract_after_boundary_collapse.py"
phase153 = ROOT / "tests" / "test_phase153_r11_generic_reference_attribution_filtering.py"

for path in (phase144, phase156, phase153):
    if not path.exists():
        raise RuntimeError(f"missing expected file: {path}")
    backup(path)


old_phase144 = r'''def test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section():
  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  assert "## 使用する結果" in rendered
  assert "(5.3) / Lemma 5.2" not in rendered
  assert "(5.3)" in rendered
  assert "Lemma 5.2" not in rendered
  assert "(5.2)" in rendered
  assert "Proposition 5.3" in rendered
  assert "Lemma 5.4" in rendered
  assert "Proposition 5.1" not in rendered
  assert "Proposition 2.2" not in rendered
'''

new_phase144 = r'''def test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section():
  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  reference_part = rendered.split(
    "\n## 証明\n",
    1,
  )[0]

  assert "## 使用する結果" in reference_part
  assert "(5.3) / Lemma 5.2" not in reference_part
  assert "(5.3)" in reference_part
  assert "Lemma 5.2" not in reference_part
  assert "(5.2)" not in reference_part
  assert "Proposition 5.3" in reference_part
  assert "Lemma 5.4" in reference_part
  assert "Proposition 5.6" in reference_part
  assert "Proposition 5.1" not in reference_part
  assert "Proposition 2.2" not in reference_part
'''

replace_once(
    phase144,
    old_phase144,
    new_phase144,
    "Phase144 reference-section contract follows Phase157 selection",
)


old_depth2 = r'''def test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary():
  rendered = _render_pi6_3(
    2
  )
  body = _body(
    rendered
  )

  assert rendered.startswith(
    "# Group proof narrative"
  )
  assert "## 使用する結果" in rendered
  assert "\n## 証明\n" in rendered
  assert (
    "使用する結果を先にまとめる."
    not in rendered
  )
  assert "(5.3)" in rendered
  assert "Lemma 5.2" not in rendered
  assert "$\\nu'$ を定める." not in rendered
  assert (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
    not in rendered
  )
  assert body.startswith(
    "次に, $\\nu'$ の位数を決定するために"
  )
'''

new_depth2 = r'''def test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary():
  rendered = _render_pi6_3(
    2
  )
  body = _body(
    rendered
  )
  reference_part = rendered.split(
    "\n## 証明\n",
    1,
  )[0]
  bracket_definition = (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
  )

  assert rendered.startswith(
    "# Group proof narrative"
  )
  assert "## 使用する結果" in rendered
  assert "\n## 証明\n" in rendered
  assert (
    "使用する結果を先にまとめる."
    not in rendered
  )
  assert "(5.3)" in reference_part
  assert "Lemma 5.2" not in rendered
  assert "$\\nu'$ を定める." not in body
  assert bracket_definition in reference_part
  assert bracket_definition not in body
  assert body.startswith(
    "次に, $\\nu'$ の位数を決定するために"
  )
'''

replace_once(
    phase156,
    old_depth2,
    new_depth2,
    "Phase156 depth2 checks Reference/body boundary instead of global absence",
)


old_depth3 = r'''def test_phase156_r5_repair9_depth3_public_body_starts_after_53_boundary():
  rendered = _render_pi6_3(
    3
  )
  body = _body(
    rendered
  )

  assert "(5.3)" in rendered
  assert "Lemma 5.2" not in rendered
  assert "$\\nu'$ を定める." not in rendered
  assert (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
    not in rendered
  )
  assert body.startswith(
    "次に, $\\nu'$ の位数を決定するために"
  )
'''

new_depth3 = r'''def test_phase156_r5_repair9_depth3_public_body_starts_after_53_boundary():
  rendered = _render_pi6_3(
    3
  )
  body = _body(
    rendered
  )
  reference_part = rendered.split(
    "\n## 証明\n",
    1,
  )[0]
  bracket_definition = (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
  )

  assert "(5.3)" in reference_part
  assert "Lemma 5.2" not in rendered
  assert "$\\nu'$ を定める." not in body
  assert bracket_definition in reference_part
  assert bracket_definition not in body
  assert body.startswith(
    "次に, $\\nu'$ の位数を決定するために"
  )
'''

replace_once(
    phase156,
    old_depth3,
    new_depth3,
    "Phase156 depth3 checks Reference/body boundary instead of global absence",
)


old_phase153 = r'''def test_phase153_r11_pi6_3_generic_section_excludes_root_self_reference():
  presentation, rendered = _pi6_3_rendered()

  root_reference = (
    extract_toda_group_proof_step_literature_reference(
      presentation.root_step
    )
  )
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  assert root_reference is not None
  assert root_reference.locator == "Proposition 5.6"
  assert "## 使用する結果" in reference_part
  assert "Proposition 5.6" not in reference_part
'''

new_phase153 = r'''def test_phase153_r11_pi6_3_generic_section_excludes_root_self_reference():
  presentation, rendered = _pi6_3_rendered()

  root_reference = (
    extract_toda_group_proof_step_literature_reference(
      presentation.root_step
    )
  )
  reference_part = rendered.split(
    "\n## 証明\n",
    1,
  )[0]

  assert root_reference is not None
  assert root_reference.locator == "Proposition 5.6"
  assert "## 使用する結果" in reference_part
  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    not in reference_part
  )
  assert (
    r"$\pi_{5}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$"
    in reference_part
  )
'''

replace_once(
    phase153,
    old_phase153,
    new_phase153,
    "Phase153 root-self-reference test distinguishes locator reuse from root result",
)

print("")
print("Phase157 R5-R10 repair8 patch applied successfully.")
print("Production code changes: none")
print(f"Changed: {phase144.relative_to(ROOT)}")
print(f"Changed: {phase156.relative_to(ROOT)}")
print(f"Changed: {phase153.relative_to(ROOT)}")
