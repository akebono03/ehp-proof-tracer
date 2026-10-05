from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"
BACKUP.mkdir(exist_ok=True)

SEMANTICS = ROOT / "toda_group_proof_narrative_semantics.py"
CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
PHASE148_TEST = (
    ROOT
    / "tests"
    / "test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py"
)
R11_TEST = (
    ROOT
    / "tests"
    / "test_phase157_r11_reference_reason_punctuation.py"
)
R5_R9_TEST = (
    ROOT
    / "tests"
    / "test_phase157_r5_r9_fixed_definition_body_suppression.py"
)


def backup(path: Path) -> None:
    if not path.exists():
        return
    destination = BACKUP / path.name
    if not destination.exists():
        shutil.copy2(path, destination)


for path in (
    SEMANTICS,
    CONTRIBUTION,
    PHASE148_TEST,
    R11_TEST,
    R5_R9_TEST,
):
    backup(path)


def replace_once(path: Path, old: str, new: str, label: str) -> None:
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


old_import = '''from toda_proof_dependency import (
  TodaProofEdge,
  extract_toda_recursive_proof_provenance,
)
'''

new_import = '''from toda_proof_dependency import (
  TodaProofDependencyRole,
  TodaProofEdge,
  classify_toda_proof_step_role,
  extract_toda_recursive_proof_provenance,
)
'''

replace_once(
    SEMANTICS,
    old_import,
    new_import,
    "semantic closure proof-dependency imports",
)


old_semantic_block = '''  for calculation_step_id in (
    order_calculation_step_ids
  ):
    for edge in edges_by_parent_step_id.get(
      calculation_step_id,
      (),
    ):
      premise_statement = (
        edge.premise_step.conclusion
      )

      if (
        not isinstance(
          premise_statement,
          Relation,
        )
        or premise_statement.relation_type
        is not RelationType.EQUALITY
      ):
        continue

      selected_step_ids.add(
        id(
          edge.premise_step
        )
      )

  changed = True
'''

new_semantic_block = '''  for calculation_step_id in (
    order_calculation_step_ids
  ):
    for edge in edges_by_parent_step_id.get(
      calculation_step_id,
      (),
    ):
      premise_statement = (
        edge.premise_step.conclusion
      )

      if (
        not isinstance(
          premise_statement,
          Relation,
        )
        or premise_statement.relation_type
        is not RelationType.EQUALITY
      ):
        continue

      selected_step_ids.add(
        id(
          edge.premise_step
        )
      )

  map_property_equality_step_ids = set()

  for node in presentation.nodes:
    if (
      classify_toda_proof_step_role(
        node.proof_step
      )
      is not TodaProofDependencyRole.MAP_PROPERTY
    ):
      continue

    for edge in edges_by_parent_step_id.get(
      id(
        node.proof_step
      ),
      (),
    ):
      premise_statement = (
        edge.premise_step.conclusion
      )

      if (
        isinstance(
          premise_statement,
          Relation,
        )
        and premise_statement.relation_type
        is RelationType.EQUALITY
      ):
        map_property_equality_step_ids.add(
          id(
            edge.premise_step
          )
        )

  for equality_step_id in (
    map_property_equality_step_ids
  ):
    for edge in edges_by_parent_step_id.get(
      equality_step_id,
      (),
    ):
      premise_statement = (
        edge.premise_step.conclusion
      )

      if (
        not isinstance(
          premise_statement,
          Relation,
        )
        or premise_statement.relation_type
        is not RelationType.EQUALITY
      ):
        continue

      selected_step_ids.add(
        id(
          edge.premise_step
        )
      )

  changed = True
'''

replace_once(
    SEMANTICS,
    old_semantic_block,
    new_semantic_block,
    "generic one-level equality closure for selected map properties",
)


def remove_reference_map_value_call() -> None:
    text = CONTRIBUTION.read_text(encoding="utf-8")
    call = '''  rendered = (
    insert_toda_group_proof_narrative_reference_map_values_before_surjectivity(
      rendered,
      statement_lines_by_reference_number,
    )
  )
'''
    if call not in text:
        print("Already absent: renderer-side Reference H-value insertion call")
        return

    CONTRIBUTION.write_text(
        text.replace(call, "", 1),
        encoding="utf-8",
    )
    print("Removed: renderer-side Reference H-value insertion call")


remove_reference_map_value_call()


phase148_append = r'''


def test_phase157_r11_map_property_closure_adds_direct_equality_premises():
  presentation = _depth2_presentation()
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  hopf_fixed = (
    r"H\left(\nu'\right) = E^{2}\eta_{3}"
  )
  suspension_bridge = (
    r"E^{2}\eta_{3} = \eta_{5}"
  )
  hopf_value = (
    r"H\left(\nu'\right) = \eta_{5}"
  )

  assert not _contains_rendered_fragment(
    presentation,
    hopf_fixed,
  )
  assert not _contains_rendered_fragment(
    presentation,
    suspension_bridge,
  )
  assert _contains_rendered_fragment(
    presentation,
    hopf_value,
  )

  assert _contains_rendered_fragment(
    closure,
    hopf_fixed,
  )
  assert _contains_rendered_fragment(
    closure,
    suspension_bridge,
  )
  assert _contains_rendered_fragment(
    closure,
    hopf_value,
  )


def test_phase157_r11_map_property_equality_closure_is_one_level_only():
  presentation = _depth2_presentation()
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  original_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  closure_ids = {
    id(
      node.proof_step
    )
    for node in closure.nodes
  }

  added_hopf_premises = tuple(
    node.proof_step
    for node in closure.nodes
    if (
      id(
        node.proof_step
      )
      not in original_ids
      and (
        r"H\left(\nu'\right) = E^{2}\eta_{3}"
        in _render_generic_narrative_step(
          node.proof_step
        )
        or
        r"E^{2}\eta_{3} = \eta_{5}"
        in _render_generic_narrative_step(
          node.proof_step
        )
      )
    )
  )

  assert len(
    added_hopf_premises
  ) == 2

  for added_step in added_hopf_premises:
    for premise_step in added_step.premises:
      if (
        not isinstance(
          premise_step.conclusion,
          Relation,
        )
        or premise_step.conclusion.relation_type
        is not RelationType.EQUALITY
      ):
        continue

      if id(
        premise_step
      ) in original_ids:
        continue

      assert id(
        premise_step
      ) not in closure_ids
'''

phase148_text = PHASE148_TEST.read_text(encoding="utf-8")
if (
    "def test_phase157_r11_map_property_closure_adds_direct_equality_premises()"
    not in phase148_text
):
    PHASE148_TEST.write_text(
        phase148_text.rstrip() + phase148_append + "\n",
        encoding="utf-8",
    )
    print("Added: Phase157 R11 semantic-closure regression tests")
else:
    print("Already applied: Phase157 R11 semantic-closure regression tests")


r11_test_content = r'''from toda_calculation_facade import (
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


def _render_pi6_3() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _reference_and_body() -> tuple[
  str,
  str,
]:
  rendered = _render_pi6_3()
  reference, body = rendered.split(
    "\n## 証明\n",
    1,
  )

  return (
    reference,
    body,
  )


def test_phase157_r11_r11_equation_53_reference_contains_fixed_hopf_value():
  reference, _ = _reference_and_body()

  assert "**[R2] (5.3).**" in reference
  assert (
    r"$H\left(\nu'\right) = E^{2}\eta_{3}$."
    in reference
  )


def test_phase157_r11_r11_first_visible_argument_uses_mazu():
  _, body = _reference_and_body()

  assert (
    "まず, "
    r"$\nu'$ の位数を決定するために"
    in body
  )


def test_phase157_r11_r11_reference_reuse_is_explicit():
  _, body = _reference_and_body()

  assert (
    "[R2]より, "
    r"$\nu' \in \pi_{6}^{3}$."
    in body
  )


def test_phase157_r11_r11_hopf_derivation_precedes_surjectivity():
  _, body = _reference_and_body()

  fixed_hopf = (
    "[R2]より, "
    r"$H\left(\nu'\right) = E^{2}\eta_{3}$."
  )
  bridge = (
    r"$E^{2}\eta_{3} = \eta_{5}$."
  )
  derived_hopf = (
    r"$H\left(\nu'\right) = \eta_{5}$."
  )
  target_group = (
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$."
  )
  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である."
  )

  assert fixed_hopf in body
  assert bridge in body
  assert derived_hopf in body
  assert target_group in body
  assert surjectivity in body

  assert body.index(
    fixed_hopf
  ) < body.index(
    derived_hopf
  )
  assert body.index(
    bridge
  ) < body.index(
    derived_hopf
  )
  assert body.index(
    derived_hopf
  ) < body.index(
    surjectivity
  )
  assert body.index(
    target_group
  ) < body.index(
    surjectivity
  )


def test_phase157_r11_r11_generic_final_filler_is_absent():
  _, body = _reference_and_body()

  assert (
    "以上で得た群構造, 生成元, "
    "および写像に関する結果を合わせると,"
    not in body
  )


def test_phase157_r11_r11_display_math_lines_end_with_period():
  rendered = _render_pi6_3()

  for line in rendered.splitlines():
    stripped = line.strip()

    if (
      stripped.startswith(
        "$"
      )
      and stripped.endswith(
        "$"
      )
      and stripped != r"$\square$"
    ):
      raise AssertionError(
        "display-math line lacks ASCII period: "
        + stripped
      )


def test_phase157_r11_r11_exact_sequence_ends_with_period():
  _, body = _reference_and_body()

  assert (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$."
    in body
  )
'''

R11_TEST.write_text(
    r11_test_content,
    encoding="utf-8",
)
print(f"Written: {R11_TEST.relative_to(ROOT)}")


def normalize_r5_r9_test() -> None:
    text = R5_R9_TEST.read_text(encoding="utf-8")

    start = text.find(
        "def test_phase157_r5_r9_body_starts_with_next_argument_after_reference_boundary():"
    )
    if start < 0:
        raise RuntimeError("could not locate historical R5/R9 opener test")

    next_def = text.find("\ndef ", start + 1)
    if next_def < 0:
        next_def = len(text)

    new_function = '''def test_phase157_r5_r9_body_starts_with_next_argument_after_reference_boundary():
  rendered = _pi6_3_rendered()
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[
    1
  ]

  assert (
    "まず, "
    r"$\\nu'$ の位数を決定するために"
    in body
  )
'''

    updated = text[:start] + new_function + text[next_def:]
    R5_R9_TEST.write_text(
        updated,
        encoding="utf-8",
    )
    print(
        "Updated: R5/R9 opener test uses public proof boundary, not fixed R number"
    )


normalize_r5_r9_test()

print("")
print("Phase157 R11-R11 patch applied successfully.")
