from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  for candidate in (
    PACKAGE_DIR.parent,
    Path.cwd(),
  ):
    if (
      (
        candidate
        / "tests"
        / "test_phase132_6_group_proof_narrative_renderer.py"
      ).is_file()
      and (
        candidate
        / "toda_group_proof_narrative_renderer.py"
      ).is_file()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(old)

  if count != 1:
    raise SystemExit(
      label
      + ": expected exactly one replacement target, found "
      + str(count)
      + "."
    )

  return text.replace(
    old,
    new,
    1,
  )


def main() -> None:
  repo = find_repository_root()

  path = (
    repo
    / "tests"
    / "test_phase132_6_group_proof_narrative_renderer.py"
  )

  backup_dir = (
    repo
    / "phase153_final_regression_stale_phase132_test_repair_r1_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )
  backup = backup_dir / path.name

  if not backup.exists():
    shutil.copy2(
      path,
      backup,
    )

  text = path.read_text(
    encoding="utf-8"
  )

  old_first = '''def test_phase132_6_depth_two_uses_nested_edges_before_parent_fact():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  nested_edge = next(
    edge
    for edge in presentation.edges
    if edge.parent_step
    is not presentation.root_step
  )

  parent_fact = (
    _render_group_proof_narrative_fact(
      nested_edge.parent_step
    )
  )

  child_fact = (
    _render_group_proof_narrative_fact(
      nested_edge.premise_step
    )
  )

  parent_edges = tuple(
    edge
    for edge in presentation.edges
    if edge.parent_step
    is nested_edge.parent_step
  )

  derivation_lead = (
    "このことから、"
    if len(
      parent_edges
    ) == 1
    else "これらから、"
  )

  parent_sentence = (
    derivation_lead
    + parent_fact
    + "を得る。"
  )

  assert child_fact in rendered
  assert "## 使用する結果" in rendered
  assert "**[R1] Proposition 5.15.**" in rendered
  final_result = r"$\\pi_{16}^{9} = \\mathbb{Z}/16\\{\\sigma_{9}\\}$"
  assert final_result in rendered
  assert rendered.index(child_fact) < rendered.index(final_result)
'''

  new_first = '''def test_phase132_6_depth_two_uses_nested_edges_before_parent_fact():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  nested_edge = next(
    edge
    for edge in presentation.edges
    if edge.parent_step
    is not presentation.root_step
  )

  child_fact = (
    _render_group_proof_narrative_fact(
      nested_edge.premise_step
    )
  )

  assert child_fact in rendered
  assert "**[R1] Lemma 5.14.**" in rendered
  assert "**[R1] Proposition 5.15.**" not in rendered

  final_result = (
    r"$\\pi_{16}^{9} = "
    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}$"
  )

  assert final_result in rendered
  assert (
    rendered.index(
      child_fact
    )
    < rendered.index(
      final_result
    )
  )
'''

  old_second = '''def test_phase138_4_sigma9_narrative_states_proof_purpose():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=2,
    )
  )

  rendered = data[
    "rendered"
  ]

  purpose = (
    "$\\\\sigma_{9}$ の位数を確認し、"
    "これが $\\\\pi_{16}^{9}$ を生成することを示す。"
  )

  assert "## 使用する結果" in rendered
  assert "Proposition 5.15" in rendered
  final_result = r"$\\pi_{16}^{9} = \\mathbb{Z}/16\\{\\sigma_{9}\\}$"
  assert final_result in rendered
  assert "まず、" in rendered
  assert rendered.index("Proposition 5.15") < rendered.index(final_result)
'''

  new_second = '''def test_phase138_4_sigma9_narrative_states_proof_purpose():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=2,
    )
  )

  rendered = data[
    "rendered"
  ]

  reference = (
    "**[R1] Lemma 5.14.**"
  )
  final_result = (
    r"$\\pi_{16}^{9} = "
    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}$"
  )

  assert reference in rendered
  assert "**[R1] Proposition 5.15.**" not in rendered
  assert final_result in rendered
  assert (
    rendered.index(
      reference
    )
    < rendered.index(
      final_result
    )
  )
'''

  text = replace_once(
    text,
    old_first,
    new_first,
    "Phase 132 depth-two stale Reference expectation",
  )
  text = replace_once(
    text,
    old_second,
    new_second,
    "Phase 138 sigma9 stale Reference expectation",
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 153 final regression stale Phase 132 test repair R1 applied."
  )
  print(
    "Production changes: none."
  )
  print(
    "Updated:"
  )
  print(
    "  tests/test_phase132_6_group_proof_narrative_renderer.py"
  )


if __name__ == "__main__":
  main()
