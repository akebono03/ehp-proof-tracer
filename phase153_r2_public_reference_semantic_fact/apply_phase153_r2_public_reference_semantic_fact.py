from pathlib import Path


RENDERER = Path("toda_group_proof_narrative_renderer.py")
TEST = Path(
    "tests/test_phase153_r2_public_reference_semantic_fact.py"
)


def replace_once(
    text: str,
    old: str,
    new: str,
    label: str,
) -> str:
    if new in text:
        print(label + ": already applied")
        return text
    if old not in text:
        raise RuntimeError(
            "target not found: "
            + label
        )
    if text.count(old) != 1:
        raise RuntimeError(
            "target is not unique: "
            + label
        )
    print(label + ": applied")
    return text.replace(
        old,
        new,
        1,
    )


def patch_renderer() -> None:
    text = RENDERER.read_text(
        encoding="utf-8"
    )

    old_import = '''from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
'''
    new_import = '''from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
'''
    text = replace_once(
        text,
        old_import,
        new_import,
        "add generic step renderer import",
    )

    old_reference_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
'''
    new_reference_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
'''
    text = replace_once(
        text,
        old_reference_import,
        new_reference_import,
        "add provenance-only predicate import",
    )

    old_function = '''def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
  expanded_step_ids: set[int],
  reference_marker_by_step_id: dict[int, str] | None = None,
) -> None:
  parent_id = id(
    parent_step
  )

  if parent_id in active_step_ids:
    return

  active_step_ids.add(
    parent_id
  )

  edges = (
    _narrative_edges_for_parent(
      presentation,
      parent_step,
    )
  )

  for index, edge in enumerate(
    edges
  ):
    premise_step = edge.premise_step
    premise_id = id(
      premise_step
    )
    premise_fact = (
      _render_group_proof_narrative_fact(
        premise_step
      )
    )
    premise_reference_marker = (
      None
      if (
        reference_marker_by_step_id is None
        or isinstance(
          premise_step.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      else reference_marker_by_step_id.get(
        premise_id
      )
    )
    lead = (
      _premise_lead(
        index,
        len(
          edges
        ),
      )
    )

    if premise_id in expanded_step_ids:
      if parent_step is presentation.root_step:
        lines.append(
          (
            lead
            + "、すでに得た"
            + premise_fact
            + "を用いる。"
          )
        )
      continue

    premise_edges = (
      _narrative_edges_for_parent(
        presentation,
        premise_step,
      )
    )

    if premise_edges:
      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
        reference_marker_by_step_id,
      )

      lines.append(
        (
          _derivation_lead(
            len(
              premise_edges
            )
          )
          + "、"
          + premise_fact
          + "を得る。"
        )
      )
    else:
      lines.append(
        (
          lead
          + "、"
          + (
            premise_reference_marker
            if premise_reference_marker is not None
            else premise_fact
          )
          + "を用いる。"
        )
      )

    expanded_step_ids.add(
      premise_id
    )

  active_step_ids.remove(
    parent_id
  )
'''

    new_function = '''def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
  expanded_step_ids: set[int],
  reference_marker_by_step_id: dict[int, str] | None = None,
) -> None:
  parent_id = id(
    parent_step
  )

  if parent_id in active_step_ids:
    return

  active_step_ids.add(
    parent_id
  )

  edges = (
    _narrative_edges_for_parent(
      presentation,
      parent_step,
    )
  )

  for index, edge in enumerate(
    edges
  ):
    premise_step = edge.premise_step
    premise_id = id(
      premise_step
    )
    premise_fact = (
      _render_group_proof_narrative_fact(
        premise_step
      )
    )
    premise_reference_marker = (
      None
      if (
        reference_marker_by_step_id is None
        or isinstance(
          premise_step.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      else reference_marker_by_step_id.get(
        premise_id
      )
    )
    lead = (
      _premise_lead(
        index,
        len(
          edges
        ),
      )
    )

    if premise_id in expanded_step_ids:
      if parent_step is presentation.root_step:
        lines.append(
          (
            lead
            + "、すでに得た"
            + premise_fact
            + "を用いる。"
          )
        )
      continue

    premise_edges = (
      _narrative_edges_for_parent(
        presentation,
        premise_step,
      )
    )

    if premise_edges:
      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
        reference_marker_by_step_id,
      )

      lines.append(
        (
          _derivation_lead(
            len(
              premise_edges
            )
          )
          + "、"
          + premise_fact
          + "を得る。"
        )
      )
    else:
      generic_premise_fact = (
        _render_generic_narrative_step(
          premise_step
        )
      )
      inference_rule = (
        premise_step.inference_rule
      )
      generic_fact_is_fallback = (
        (
          inference_rule is not None
          and generic_premise_fact
          == inference_rule.name
        )
        or generic_premise_fact
        == (
          "`"
          + type(
            premise_step.conclusion
          ).__name__
          + "`"
        )
        or generic_premise_fact
        == repr(
          premise_step.conclusion
        )
        or generic_premise_fact
        == str(
          premise_step.conclusion
        )
      )
      reference_plus_semantic_fact = (
        premise_reference_marker
        is not None
        and not (
          is_toda_group_proof_narrative_provenance_only_statement(
            premise_step.conclusion
          )
        )
        and not generic_fact_is_fallback
      )

      if reference_plus_semantic_fact:
        if (
          generic_premise_fact.startswith(
            "$"
          )
          and generic_premise_fact.endswith(
            "$"
          )
        ):
          lines.append(
            (
              lead
              + "、"
              + premise_reference_marker
              + " により、"
              + generic_premise_fact
              + "を得る。"
            )
          )
        else:
          lines.append(
            (
              lead
              + "、"
              + premise_reference_marker
              + " により、"
              + generic_premise_fact
            )
          )
      else:
        lines.append(
          (
            lead
            + "、"
            + (
              premise_reference_marker
              if premise_reference_marker is not None
              else premise_fact
            )
            + "を用いる。"
          )
        )

    expanded_step_ids.add(
      premise_id
    )

  active_step_ids.remove(
    parent_id
  )
'''

    text = replace_once(
        text,
        old_function,
        new_function,
        "reference + semantic fact leaf rule",
    )

    RENDERER.write_text(
        text,
        encoding="utf-8",
    )


def write_test() -> None:
    TEST.write_text(
        '''from toda_calculation_facade import (
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


def _phase153_r2_public_pi10_6_narrative() -> str:
  report = build_standard_toda_report(
    n=6,
    k=4,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def test_phase153_r2_public_pi10_6_keeps_reference_and_shows_toda45_fact():
  rendered = (
    _phase153_r2_public_pi10_6_narrative()
  )

  assert "**[R2] (4.5).**" in rendered
  assert "[R2] により、" in rendered
  assert "は同型写像である." in rendered
  assert (
    "Toda 4.5 stable-range iterated suspension isomorphism"
    not in rendered
  )
  assert "[R2]を用いる。" not in rendered


def test_phase153_r2_public_pi10_6_keeps_provenance_only_reference_compact():
  rendered = (
    _phase153_r2_public_pi10_6_narrative()
  )

  assert "**[R1] Proposition 5.8.**" in rendered
  assert "まず、[R1]を用いる。" in rendered
  assert (
    "Toda Proposition 5.8 finite-dimensional integration"
    not in rendered
  )
''',
        encoding="utf-8",
    )


def main() -> int:
    patch_renderer()
    write_test()

    print(
        "Applied Phase153-R2 public Narrative "
        "reference + semantic fact repair."
    )
    print(
        "Changed: toda_group_proof_narrative_renderer.py"
    )
    print(
        "Added: "
        "tests/test_phase153_r2_public_reference_semantic_fact.py"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
