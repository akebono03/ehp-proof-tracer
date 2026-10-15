from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  build_toda_group_proof_narrative_reference_entries,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  TodaProofEdge,
)


def _reference(
  locator,
):
  return LiteratureReference(
    label=(
      "Toda "
      + locator
    ),
    locator=locator,
  )


def _step(
  conclusion,
  reference,
  premises=(),
):
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=(
        "Toda "
        + reference.locator
        + " test"
      ),
      literature_reference=reference,
    ),
  )


def test_phase153_r6_prefers_reference_boundary_frontier_over_internal_used_steps():
  reference = _reference(
    "Proposition 5.6"
  )
  consumer_reference = _reference(
    "Proposition 5.8"
  )

  internal_leaf = _step(
    "internal leaf",
    reference,
  )
  boundary_statement = _step(
    "boundary statement",
    reference,
    premises=(
      internal_leaf,
    ),
  )
  same_reference_aggregate = _step(
    "same-reference aggregate",
    reference,
    premises=(
      boundary_statement,
    ),
  )
  external_consumer = _step(
    "external consumer",
    consumer_reference,
    premises=(
      boundary_statement,
    ),
  )

  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=reference,
    proof_steps=(
      internal_leaf,
      boundary_statement,
      same_reference_aggregate,
    ),
  )
  edges = (
    TodaProofEdge(
      parent_step=boundary_statement,
      premise_step=internal_leaf,
      premise_index=0,
    ),
    TodaProofEdge(
      parent_step=same_reference_aggregate,
      premise_step=boundary_statement,
      premise_index=0,
    ),
    TodaProofEdge(
      parent_step=external_consumer,
      premise_step=boundary_statement,
      premise_index=0,
    ),
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        internal_leaf,
        boundary_statement,
        same_reference_aggregate,
      ),
      edges,
    )
  )

  assert selected == (
    boundary_statement,
  )


def test_phase153_r6_keeps_r5_fallback_when_reference_has_no_boundary_crossing():
  reference = _reference(
    "Proposition 5.6"
  )

  first = _step(
    "first",
    reference,
  )
  second = _step(
    "second",
    reference,
    premises=(
      first,
    ),
  )

  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=reference,
    proof_steps=(
      first,
      second,
    ),
  )
  edge = TodaProofEdge(
    parent_step=second,
    premise_step=first,
    premise_index=0,
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        first,
        second,
      ),
      (
        edge,
      ),
    )
  )

  assert selected == (
    first,
  )


def _pi6_2_presentation():
  report = build_standard_toda_report(
    n=2,
    k=4,
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

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase153_r6_pi6_2_proposition_5_6_reference_is_granular():
  presentation = (
    _pi6_2_presentation()
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

  prop56_entry = next(
    entry
    for entry in entries
    if (
      entry.reference.locator
      == "Proposition 5.6"
    )
  )
  prop56_lines = statement_lines[
    prop56_entry.number
  ]

  assert len(
    prop56_lines
  ) == 1
  assert (
    r"\pi_{6}^{3}"
    in prop56_lines[0]
  )
  assert (
    r"\pi_{5}^{2}"
    not in prop56_lines[0]
  )
  assert (
    r"\pi_{7}^{4}"
    not in prop56_lines[0]
  )
  assert (
    r"\pi_{8}^{5}"
    not in prop56_lines[0]
  )


def test_phase153_r6_pi6_2_reference_candidate_selection_excludes_internal_prop56_statements():
  presentation = (
    _pi6_2_presentation()
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  prop56_entry = next(
    entry
    for entry in entries
    if (
      entry.reference.locator
      == "Proposition 5.6"
    )
  )

  candidate_steps = []
  seen_rendered = set()

  for proof_step in prop56_entry.proof_steps:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not (
      _is_toda_group_proof_narrative_reference_statement_candidate(
        proof_step,
        rendered,
      )
    ):
      continue

    if rendered in seen_rendered:
      continue

    seen_rendered.add(
      rendered
    )
    candidate_steps.append(
      proof_step
    )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      prop56_entry,
      tuple(
        candidate_steps
      ),
      presentation.edges,
      root_step=presentation.root_step,
    )
  )

  assert len(
    selected
  ) == 1
