from phase148_rc2_4_repair_r5_two_group_exposure_path_audit.audit_phase148_rc2_4_repair_r5 import (
  CASES,
  _build_case,
  _normalized_exactness_rendering,
)
from toda_group_proof_narrative_renderer import (
  _narrative_edges_for_parent,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


def _reference_marker_by_step_id(
  presentation,
):
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  return {
    id(proof_step): f"[R{entry.number}]"
    for entry in entries
    for proof_step in entry.proof_steps
  }


def audit_case(
  label,
  n,
  k,
):
  (
    _presentation,
    closure,
    _sidecar,
    _blocks,
    _arguments,
    rendered,
  ) = _build_case(
    label,
    n,
    k,
  )

  marker_by_step_id = (
    _reference_marker_by_step_id(
      closure
    )
  )

  exactness_steps = tuple(
    node.proof_step
    for node in closure.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  print("=" * 100)
  print(label)
  print("=" * 100)

  for index, proof_step in enumerate(
    exactness_steps
  ):
    normalized = (
      _normalized_exactness_rendering(
        proof_step
      )
    )
    reference = (
      extract_toda_group_proof_step_literature_reference(
        proof_step
      )
    )
    child_edges = (
      _narrative_edges_for_parent(
        closure,
        proof_step,
      )
    )
    marker = marker_by_step_id.get(
      id(
        proof_step
      )
    )

    print(
      "EXACTNESS["
      + str(index)
      + "]"
    )
    print(
      "  leaf="
      + str(
        not child_edges
      )
    )
    print(
      "  child_edge_count="
      + str(
        len(
          child_edges
        )
      )
    )
    print(
      "  reference="
      + repr(
        reference
      )
    )
    print(
      "  marker="
      + repr(
        marker
      )
    )
    print(
      "  normalized_visible="
      + str(
        normalized in rendered
      )
    )
    print(
      "  marker_use_visible="
      + str(
        (
          marker + "を用いる"
          if marker is not None
          else ""
        )
        in rendered
        if marker is not None
        else False
      )
    )
    print(
      "  normalized="
      + normalized
    )

  phrase_count = (
    rendered.count(
      "は完全である"
    )
    + rendered.count(
      r"\text{ is exact}"
    )
  )
  print(
    "VISIBLE_EXACTNESS_PHRASE_COUNT="
    + str(
      phrase_count
    )
  )
  print()


def main():
  print(
    "Phase 150 RC4-7A regression diagnosis"
  )
  print(
    "Production changes: none"
  )
  print()

  for label, n, k in CASES:
    audit_case(
      label,
      n,
      k,
    )

  print(
    "DIAGNOSIS_COMPLETE=True"
  )


if __name__ == "__main__":
  main()
