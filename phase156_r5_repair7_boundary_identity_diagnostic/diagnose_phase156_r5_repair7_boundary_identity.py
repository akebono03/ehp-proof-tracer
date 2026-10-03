from __future__ import annotations

from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_purpose_sentence,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
  _render_generic_narrative_step,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _ref(step):
  rule = step.inference_rule
  if rule is None:
    return None
  ref = rule.literature_reference
  if ref is None:
    return None
  return (
    ref.label,
    ref.locator,
  )


def _data(depth: int):
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
    max_depth=depth,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  reasons = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    sidecar,
  )
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  lines = _toda_group_proof_narrative_reference_statement_lines_by_number(
    presentation,
    entries,
  )
  entries, lines = exclude_toda_group_proof_narrative_root_reference(
    entries,
    lines,
    presentation.root_step,
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  return (
    presentation,
    sidecar,
    blocks,
    arguments,
    reasons,
    entries,
    lines,
    rendered,
  )


def main() -> int:
  out = []

  for depth in (
    2,
    3,
  ):
    (
      presentation,
      sidecar,
      blocks,
      arguments,
      reasons,
      entries,
      lines,
      rendered,
    ) = _data(
      depth
    )

    out.append(
      "=" * 78
    )
    out.append(
      "DEPTH "
      + str(
        depth
      )
    )
    out.append(
      "=" * 78
    )

    out.append(
      "REFERENCE ENTRIES"
    )

    for entry in entries:
      if entry.reference.locator != "(5.3)":
        continue

      out.append(
        "ENTRY number="
        + str(
          entry.number
        )
        + " label="
        + entry.reference.label
        + " locator="
        + str(
          entry.reference.locator
        )
      )

      candidate_steps = []
      for step in entry.proof_steps:
        rendered_step = _render_generic_narrative_step(
          step
        )
        if rendered_step:
          candidate_steps.append(
            step
          )

      selected = select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
      selected_ids = {
        id(
          step
        )
        for step in selected
      }

      for index, step in enumerate(
        entry.proof_steps,
        start=1,
      ):
        out.append(
          "  STEP "
          + str(
            index
          )
        )
        out.append(
          "    id="
          + str(
            id(
              step
            )
          )
        )
        out.append(
          "    selected="
          + str(
            id(
              step
            )
            in selected_ids
          )
        )
        out.append(
          "    rule="
          + str(
            (
              step.inference_rule.name
              if step.inference_rule is not None
              else None
            )
          )
        )
        out.append(
          "    ref="
          + str(
            _ref(
              step
            )
          )
        )
        out.append(
          "    rendered="
          + str(
            _render_generic_narrative_step(
              step
            )
          )
        )

    out.append(
      ""
    )
    out.append(
      "REASONS"
    )

    entry_step_ids = {
      id(
        step
      )
      for entry in entries
      for step in entry.proof_steps
    }

    for index, reason in enumerate(
      reasons.reasons,
      start=1,
    ):
      sentence = render_toda_group_proof_narrative_reason_sentence(
        reason
      )
      if (
        "Lemma 5.2"
        not in (
          sentence
          or ""
        )
        and "definition"
        not in reason.kind.value
      ):
        continue

      conclusion = reason.conclusion_step
      out.append(
        "REASON "
        + str(
          index
        )
      )
      out.append(
        "  kind="
        + reason.kind.value
      )
      out.append(
        "  conclusion_id="
        + str(
          id(
            conclusion
          )
        )
      )
      out.append(
        "  conclusion_in_any_reference_entry="
        + str(
          id(
            conclusion
          )
          in entry_step_ids
        )
      )
      out.append(
        "  conclusion_rule="
        + str(
          (
            conclusion.inference_rule.name
            if conclusion.inference_rule is not None
            else None
          )
        )
      )
      out.append(
        "  conclusion_ref="
        + str(
          _ref(
            conclusion
          )
        )
      )
      out.append(
        "  conclusion_rendered="
        + str(
          _render_generic_narrative_step(
            conclusion
          )
        )
      )
      out.append(
        "  sentence="
        + repr(
          sentence
        )
      )
      for premise_index, premise in enumerate(
        reason.premise_steps
      ):
        out.append(
          "  premise["
          + str(
            premise_index
          )
          + "] id="
          + str(
            id(
              premise
            )
          )
          + " rule="
          + str(
            (
              premise.inference_rule.name
              if premise.inference_rule is not None
              else None
            )
          )
          + " ref="
          + str(
            _ref(
              premise
            )
          )
        )

    out.append(
      ""
    )
    out.append(
      "ARGUMENTS"
    )

    for index, argument in enumerate(
      arguments,
      start=1,
    ):
      purpose = render_toda_group_proof_narrative_argument_purpose_sentence(
        argument
      )
      if (
        purpose is None
        or "定める" not in purpose
      ):
        continue

      conclusion = extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      out.append(
        "ARGUMENT "
        + str(
          index
        )
      )
      out.append(
        "  purpose="
        + str(
          purpose
        )
      )
      out.append(
        "  conclusion_id="
        + str(
          (
            id(
              conclusion
            )
            if conclusion is not None
            else None
          )
        )
      )
      out.append(
        "  conclusion_in_any_reference_entry="
        + str(
          (
            conclusion is not None
            and id(
              conclusion
            )
            in entry_step_ids
          )
        )
      )
      if conclusion is not None:
        out.append(
          "  conclusion_rule="
          + str(
            (
              conclusion.inference_rule.name
              if conclusion.inference_rule is not None
              else None
            )
          )
        )
        out.append(
          "  conclusion_ref="
          + str(
            _ref(
              conclusion
            )
          )
        )
        out.append(
          "  conclusion_rendered="
          + str(
            _render_generic_narrative_step(
              conclusion
            )
          )
        )

    out.append(
      ""
    )
    out.append(
      "PUBLIC BODY"
    )
    if "まず" in rendered:
      out.append(
        "まず"
        + rendered.split(
          "まず",
          1,
        )[1]
      )
    else:
      out.append(
        rendered
      )

  text = "\n".join(
    out
  )
  print(
    text
  )

  output_path = Path(
    "phase156_r5_repair7_boundary_identity_diagnostic.txt"
  )
  output_path.write_text(
    text,
    encoding="utf-8",
  )

  print()
  print(
    "PASS: diagnostic completed."
  )
  print(
    "Production changes: none."
  )
  print(
    "Repository-wide pytest is intentionally NOT run."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
