from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _phase154_r5_reference_source_steps_by_number,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
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


def _insert_contributions_if_available(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  base_markdown,
):
  import toda_group_proof_narrative_contribution_renderer as contribution_renderer

  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )

  return (
    contribution_renderer
    ._insert_toda_group_proof_narrative_argument_contributions(
      presentation,
      base_markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )


def build_state():
  report = build_standard_toda_report(
    n=4,
    k=7,
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
  raw_presentation = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar,
  )
  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  contribution_markdown = (
    _insert_contributions_if_available(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      base_markdown,
    )
  )
  reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    semantic_sidecar,
  )
  rendered = insert_toda_group_proof_narrative_reason_prose(
    contribution_markdown,
    reason_sidecar,
  )

  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )
  entries, statement_lines = (
    exclude_toda_group_proof_narrative_root_reference(
      entries,
      statement_lines,
      presentation.root_step,
    )
  )

  rendered = (
    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
      presentation,
      rendered,
      entries,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      rendered,
      statement_lines,
    )
  )

  return (
    presentation,
    entries,
    statement_lines,
    rendered,
  )


def main() -> int:
  (
    presentation,
    entries,
    statement_lines,
    body,
  ) = build_state()

  print("==============================================================================")
  print("Phase 154-R5 Fix1 Diagnostic")
  print("==============================================================================")
  print("")
  print("BODY BEFORE LINKAGE")
  print("-------------------")
  print(body)
  print("")
  print("REFERENCE ENTRIES AFTER ROOT EXCLUSION")
  print("--------------------------------------")

  sources_by_number = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      entries,
    )
  )

  children = defaultdict(list)
  for edge in presentation.edges:
    children[id(edge.premise_step)].append(
      edge.parent_step
    )

  for entry in entries:
    number = entry.number
    marker = f"[R{number}]"
    print("")
    print(marker, entry.reference.label, entry.reference.locator)
    print("statement_lines:", statement_lines.get(number, ()))
    print("marker_present:", marker in body)
    print(
      "neutral_marker_present:",
      marker + "を用いる。" in body,
    )

    source_steps = sources_by_number.get(
      number,
      (),
    )
    print("source_step_count:", len(source_steps))

    source_ids = {id(step) for step in source_steps}
    queue = deque(
      (step, 0)
      for step in source_steps
    )
    visited = set()

    print("DESCENDANTS")
    while queue:
      step, distance = queue.popleft()
      step_id = id(step)
      key = (step_id, distance)
      if key in visited:
        continue
      visited.add(key)

      for child in children.get(step_id, ()):
        child_id = id(child)
        rendered_child = _render_generic_narrative_step(
          child
        )
        print(
          " distance=",
          distance + 1,
          " source_owned=",
          child_id in source_ids,
          " root=",
          child is presentation.root_step,
          " body_contains=",
          bool(
            rendered_child
            and rendered_child in body
          ),
          " type=",
          type(child.conclusion).__name__,
        )
        print(
          "  rendered=",
          repr(rendered_child),
        )

        if (
          child_id in source_ids
          or child is presentation.root_step
        ):
          continue

        queue.append(
          (
            child,
            distance + 1,
          )
        )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
