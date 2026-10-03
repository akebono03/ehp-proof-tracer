import inspect

import pytest

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_owned_step_ids,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
)


CASES = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _render_case(n, k):
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(n, k)
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  return (
    presentation,
    semantic_sidecar,
    reason_sidecar,
    rendered,
  )


def test_phase150_rc4_5_pi6_reason_is_visible_before_definition():
  (
    presentation,
    semantic_sidecar,
    reason_sidecar,
    rendered,
  ) = _render_case(
    3,
    3,
  )

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .DEFINITION_APPLICABILITY
    )
  )
  sentence = render_toda_group_proof_narrative_reason_sentence(
    reason
  )

  reference_entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  empty_statement_lines = {
    entry.number: ()
    for entry in reference_entries
  }
  (
    reference_entries,
    _,
  ) = exclude_toda_group_proof_narrative_root_reference(
    reference_entries,
    empty_statement_lines,
    presentation.root_step,
  )
  owned_step_ids = (
    _toda_group_proof_narrative_reference_owned_step_ids(
      presentation,
      reference_entries,
    )
  )

  assert sentence is not None
  assert id(
    reason.conclusion_step
  ) in owned_step_ids
  assert sentence not in rendered


@pytest.mark.parametrize("_label,n,k", CASES)
@pytest.mark.parametrize("_label,n,k", CASES)
def test_phase150_rc4_5_visible_reason_count_matches_current_deduplication_contract(
  _label,
  n,
  k,
):
  (
    presentation,
    semantic_sidecar,
    reason_sidecar,
    rendered,
  ) = _render_case(
    n,
    k,
  )

  reference_entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  empty_statement_lines = {
    entry.number: ()
    for entry in reference_entries
  }
  (
    reference_entries,
    _,
  ) = exclude_toda_group_proof_narrative_root_reference(
    reference_entries,
    empty_statement_lines,
    presentation.root_step,
  )
  owned_step_ids = (
    _toda_group_proof_narrative_reference_owned_step_ids(
      presentation,
      reference_entries,
    )
  )

  sentence_reasons = {}

  for reason in reason_sidecar.reasons:
    sentence = (
      render_toda_group_proof_narrative_reason_sentence(
        reason
      )
    )

    if sentence is None:
      continue

    sentence_reasons.setdefault(
      sentence,
      [],
    ).append(
      reason
    )

  for sentence, reasons in sentence_reasons.items():
    visible_reasons = tuple(
      reason
      for reason in reasons
      if id(
        reason.conclusion_step
      )
      not in owned_step_ids
    )

    if any(
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .FINAL_RESULT_DERIVATION
      for reason in visible_reasons
    ):
      assert rendered.count(
        sentence
      ) == 1
      continue

    assert rendered.count(
      sentence
    ) == len(
      visible_reasons
    )


def test_phase150_rc4_5_does_not_invent_untyped_reason_prose():
  for _label, n, k in CASES:
    (
      presentation,
      semantic_sidecar,
      reason_sidecar,
      rendered,
    ) = _render_case(n, k)

    if not reason_sidecar.reasons:
      assert (
        "この前提条件を満たすので、"
        "次の定義を用いる."
        not in rendered
      )


def test_phase150_rc4_5_renderer_has_no_pi6_specific_branch():
  import toda_group_proof_narrative_reason_renderer as module

  source = inspect.getsource(module)
  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )
  for fragment in forbidden_fragments:
    assert fragment not in source
