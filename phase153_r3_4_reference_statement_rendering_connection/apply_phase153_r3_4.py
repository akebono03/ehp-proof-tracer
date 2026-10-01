from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent


def _replace_once(
    path: Path,
    old: str,
    new: str,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )

    count = text.count(
        old
    )

    if count != 1:
        raise RuntimeError(
            str(path.relative_to(REPO_ROOT))
            + ": expected exactly one replacement target, found "
            + str(count)
        )

    path.write_text(
        text.replace(
            old,
            new,
            1,
        ),
        encoding="utf-8",
    )


TEST_CONTENT = r'''from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _phase153_r3_4_pi10_6_presentation():
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
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )


def test_phase153_r3_4_reference_renderer_accepts_statement_lines_without_breaking_old_api():
  reference = LiteratureReference(
    label="Toda test",
    locator="Proposition X",
  )
  step = ProofStep(
    conclusion="test conclusion",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name="test rule",
      literature_reference=reference,
    ),
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=reference,
    proof_steps=(
      step,
    ),
  )

  legacy = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      (
        entry,
      )
    )
  )
  connected = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      (
        entry,
      ),
      {
        1: (
          "$A = B$",
        ),
      },
    )
  )

  assert legacy == (
    "使用する結果を先にまとめる.\n\n"
    "**[R1] Proposition X.**"
  )
  assert connected == (
    "使用する結果を先にまとめる.\n\n"
    "**[R1] Proposition X.**\n"
    "$A = B$"
  )


def test_phase153_r3_4_pi10_6_builds_selected_reference_statement_lines():
  presentation = (
    _phase153_r3_4_pi10_6_presentation()
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )

  r2 = next(
    entry
    for entry in entries
    if entry.reference.locator == "(4.5)"
  )

  assert r2.number in statement_lines
  assert statement_lines[
    r2.number
  ]
  assert any(
    "同型" in line
    or r"\cong" in line
    for line in statement_lines[
      r2.number
    ]
  )


def test_phase153_r3_4_public_pi10_6_reference_section_contains_r2_statement():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase153_r3_4_pi10_6_presentation()
    )
  )

  reference_title = "**[R2] (4.5).**"
  title_index = rendered.index(
    reference_title
  )
  body_reference_index = rendered.index(
    "[R2] により、"
  )

  between = rendered[
    title_index
    + len(
      reference_title
    ):
    body_reference_index
  ]

  assert "同型" in between or r"\cong" in between


def test_phase153_r3_4_does_not_render_internal_fallback_name_in_reference_section():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase153_r3_4_pi10_6_presentation()
    )
  )
  reference_section = rendered.split(
    "[R2] により、",
    1,
  )[0]

  assert (
    "Toda 4.5 stable-range iterated suspension isomorphism"
    not in reference_section
  )
'''


def main() -> int:
    references_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_references.py"
    )
    contribution_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_contribution_renderer.py"
    )
    test_path = (
        REPO_ROOT
        / "tests"
        / "test_phase153_r3_4_reference_statement_rendering_connection.py"
    )

    old_reference_renderer = r'''def render_toda_group_proof_narrative_reference_entries_markdown(
  entries: tuple[TodaGroupProofNarrativeReferenceEntry, ...],
) -> str:
  if not isinstance(entries, tuple):
    raise TypeError("entries must be a tuple")
  if not entries:
    return ""

  lines = ["使用する結果を先にまとめる.", ""]

  for entry in entries:
    if not isinstance(entry, TodaGroupProofNarrativeReferenceEntry):
      raise TypeError(
        "entries must contain only "
        "TodaGroupProofNarrativeReferenceEntry objects"
      )
    title = entry.reference.locator or entry.reference.label
    lines.append(f"**[R{entry.number}] {title}.**")

  return "\n".join(lines)
'''

    new_reference_renderer = r'''def render_toda_group_proof_narrative_reference_entries_markdown(
  entries: tuple[TodaGroupProofNarrativeReferenceEntry, ...],
  statement_lines_by_reference_number: (
    dict[
      int,
      tuple[
        str,
        ...,
      ],
    ]
    | None
  ) = None,
) -> str:
  if not isinstance(entries, tuple):
    raise TypeError("entries must be a tuple")

  if (
    statement_lines_by_reference_number is not None
    and not isinstance(
      statement_lines_by_reference_number,
      dict,
    )
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be "
      "a dict or None"
    )

  if statement_lines_by_reference_number is not None:
    for reference_number, statement_lines in (
      statement_lines_by_reference_number.items()
    ):
      if (
        isinstance(
          reference_number,
          bool,
        )
        or not isinstance(
          reference_number,
          int,
        )
      ):
        raise TypeError(
          "statement_lines_by_reference_number keys "
          "must be integers"
        )

      if not isinstance(
        statement_lines,
        tuple,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must be tuples"
        )

      if not all(
        isinstance(
          line,
          str,
        )
        for line in statement_lines
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

  if not entries:
    return ""

  lines = ["使用する結果を先にまとめる.", ""]

  for entry in entries:
    if not isinstance(entry, TodaGroupProofNarrativeReferenceEntry):
      raise TypeError(
        "entries must contain only "
        "TodaGroupProofNarrativeReferenceEntry objects"
      )

    title = entry.reference.locator or entry.reference.label
    lines.append(f"**[R{entry.number}] {title}.**")

    statement_lines = (
      ()
      if statement_lines_by_reference_number is None
      else statement_lines_by_reference_number.get(
        entry.number,
        (),
      )
    )

    for statement_line in statement_lines:
      lines.append(
        statement_line
      )

  return "\n".join(lines)
'''

    _replace_once(
        references_path,
        old_reference_renderer,
        new_reference_renderer,
    )

    old_import = r'''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
'''

    new_import = r'''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
'''

    _replace_once(
        contribution_path,
        old_import,
        new_import,
    )

    marker = r'''def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
'''

    helpers = r'''def _is_toda_group_proof_narrative_reference_statement_candidate(
  proof_step,
  rendered_statement: str,
) -> bool:
  if not rendered_statement:
    return False

  inference_rule = proof_step.inference_rule

  if (
    inference_rule is not None
    and rendered_statement == inference_rule.name
  ):
    return False

  if (
    rendered_statement
    == "`"
    + type(
      proof_step.conclusion
    ).__name__
    + "`"
  ):
    return False

  if rendered_statement == repr(
    proof_step.conclusion
  ):
    return False

  if rendered_statement == str(
    proof_step.conclusion
  ):
    return False

  return True


def _toda_group_proof_narrative_reference_statement_lines_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    str,
    ...,
  ],
]:
  statement_lines_by_reference_number = {}

  for entry in reference_entries:
    candidate_steps = []
    rendered_by_step_id = {}
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )
      rendered_by_step_id[
        id(
          proof_step
        )
      ] = rendered_statement

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
      )
    )

    statement_lines = tuple(
      rendered_by_step_id[
        id(
          proof_step
        )
      ]
      for proof_step in selected_steps
    )

    if statement_lines:
      statement_lines_by_reference_number[
        entry.number
      ] = statement_lines

  return statement_lines_by_reference_number


'''

    contribution_text = contribution_path.read_text(
        encoding="utf-8",
    )
    if contribution_text.count(marker) != 1:
        raise RuntimeError(
            "toda_group_proof_narrative_contribution_renderer.py: "
            "expected exactly one final renderer marker"
        )

    contribution_text = contribution_text.replace(
        marker,
        helpers + marker,
        1,
    )
    contribution_path.write_text(
        contribution_text,
        encoding="utf-8",
    )

    old_reference_section = r'''  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries
    )
  )
'''

    new_reference_section = r'''  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
'''

    _replace_once(
        contribution_path,
        old_reference_section,
        new_reference_section,
    )

    test_path.write_text(
        TEST_CONTENT,
        encoding="utf-8",
    )

    print(
        "updated: toda_group_proof_narrative_references.py"
    )
    print(
        "updated: toda_group_proof_narrative_contribution_renderer.py"
    )
    print(
        "added: tests\\test_phase153_r3_4_reference_statement_rendering_connection.py"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
