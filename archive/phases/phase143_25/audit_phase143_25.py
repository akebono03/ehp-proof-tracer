from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


for n, k in (
  (3, 3),
  (5, 3),
  (8, 7),
  (9, 7),
):
  (
    presentation,
    blocks,
    _sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  print("=" * 78)
  print(f"n={n}, k={k}")

  for index, argument in enumerate(
    arguments,
    start=1,
  ):
    subject = (
      extract_toda_group_proof_narrative_argument_purpose_subject(
        argument
      )
    )
    groups = (
      extract_toda_group_proof_narrative_argument_relevant_groups(
        presentation,
        blocks,
        argument,
      )
    )

    print(
      f"A{index:02d} "
      f"{argument.role.value}: "
      f"subject={subject!r}"
    )
    print(
      f"  relevant_groups={groups!r}"
    )
