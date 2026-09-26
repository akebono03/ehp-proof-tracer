from collections import Counter

from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_statement_prose,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _fallback_kind(
  proof_step,
):
  statement = proof_step.conclusion

  if (
    _render_generic_narrative_statement_prose(
      statement
    )
    is not None
  ):
    return None

  try:
    repository_latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    repository_latex = None

  if repository_latex is not None:
    return None

  toda_latex = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  if toda_latex is not None:
    return None

  if proof_step.inference_rule is not None:
    return "INFERENCE_RULE_NAME"

  return "RAW_CLASS_NAME"


def _statement_shape(
  statement,
):
  attributes = []

  for name in (
    "element",
    "group",
    "source_group",
    "target_group",
    "source",
    "target",
    "map",
    "decomposition_map",
    "isomorphism",
    "n",
    "k",
  ):
    if hasattr(
      statement,
      name,
    ):
      value = getattr(
        statement,
        name,
      )
      attributes.append(
        name
        + "="
        + type(
          value
        ).__name__
      )

  return ", ".join(
    attributes
  )


def audit_case(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  step_block_roles = {
    id(
      proof_step
    ): block.role.value
    for block in blocks
    for proof_step in block.steps
  }

  fallback_rows = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    kind = _fallback_kind(
      proof_step
    )

    if kind is None:
      continue

    rule_name = (
      proof_step.inference_rule.name
      if proof_step.inference_rule is not None
      else None
    )
    display = (
      rule_name
      if rule_name is not None
      else (
        "`"
        + type(
          proof_step.conclusion
        ).__name__
        + "`"
      )
    )

    if display not in rendered:
      continue

    fallback_rows.append(
      (
        kind,
        step_block_roles.get(
          id(
            proof_step
          ),
          "unknown",
        ),
        type(
          proof_step.conclusion
        ).__name__,
        rule_name,
        len(
          proof_step.premises
        ),
        _statement_shape(
          proof_step.conclusion
        ),
      )
    )

  counts = Counter(
    row[0]
    for row in fallback_rows
  )

  print("=" * 78)
  print(
    f"n={n}, k={k}, "
    f"fallbacks={len(fallback_rows)}, "
    f"rule_names={counts['INFERENCE_RULE_NAME']}, "
    f"raw_classes={counts['RAW_CLASS_NAME']}"
  )
  print("=" * 78)

  for index, row in enumerate(
    fallback_rows,
    start=1,
  ):
    (
      kind,
      role,
      statement_type,
      rule_name,
      premise_count,
      shape,
    ) = row

    print(
      f"{index:02d}. kind={kind}"
    )
    print(
      f"    role={role}"
    )
    print(
      f"    statement={statement_type}"
    )
    print(
      f"    rule={rule_name}"
    )
    print(
      f"    premises={premise_count}"
    )
    print(
      f"    shape={shape or '-'}"
    )

  print()
  print("--- NARRATIVE ---")
  print(
    rendered
  )
  print()


def main():
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    audit_case(
      n,
      k,
    )


if __name__ == "__main__":
  main()
