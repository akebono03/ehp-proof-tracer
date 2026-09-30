from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  render_toda_group_proof_narrative_reference_entries_markdown,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _reference_title(reference):
  return reference.locator or reference.label


def main():
  print("=" * 78)
  print("Phase 150 cross-group Reference numbering audit")
  print("Production changes: none")
  print("=" * 78)

  any_cross_group_reference_gap = False

  for n, k in TARGETS:
    (
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    ) = _method_evidence_data(n, k)

    entries = build_toda_group_proof_narrative_reference_entries(
      presentation
    )
    section = render_toda_group_proof_narrative_reference_entries_markdown(
      entries
    )
    rendered = render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )

    referenced_steps = tuple(
      node.proof_step
      for node in presentation.nodes
      if extract_toda_group_proof_step_literature_reference(
        node.proof_step
      )
      is not None
    )
    unreferenced_inference_steps = tuple(
      node.proof_step
      for node in presentation.nodes
      if (
        node.proof_step.inference_rule is not None
        and extract_toda_group_proof_step_literature_reference(
          node.proof_step
        )
        is None
      )
    )

    print("-" * 78)
    print(f"TARGET pi_{n+k}^{n}")
    print("presentation nodes:", len(presentation.nodes))
    print("reference entries:", len(entries))
    print("referenced steps:", len(referenced_steps))
    print(
      "reference applications:",
      len(semantic_sidecar.reference_application_semantics),
    )
    print("reference section visible:", bool(section and section in rendered))

    for entry in entries:
      title = _reference_title(entry.reference)
      marker = f"[R{entry.number}]"
      print(
        f"  {marker} title={title!r} "
        f"steps={len(entry.proof_steps)} "
        f"marker_visible={marker in rendered}"
      )

    if unreferenced_inference_steps:
      print(
        "inference steps without LiteratureReference:",
        len(unreferenced_inference_steps),
      )
      for step in unreferenced_inference_steps[:20]:
        print(
          "  NO_REF:",
          getattr(step.inference_rule, "name", None),
        )

    direct_reference_phrases = tuple(
      phrase
      for phrase in (
        "Toda Proposition",
        "Toda Lemma",
        "Toda (",
      )
      if phrase in rendered
    )
    print(
      "direct literature-name phrases in body:",
      direct_reference_phrases,
    )

    if (
      (n, k) != (3, 3)
      and direct_reference_phrases
      and not entries
    ):
      any_cross_group_reference_gap = True

    if (n, k) == (4, 6):
      print("PI10_4_DETAIL_BEGIN")
      for node_index, node in enumerate(presentation.nodes):
        step = node.proof_step
        rule = step.inference_rule
        if rule is None:
          continue
        reference = extract_toda_group_proof_step_literature_reference(
          step
        )
        print(
          f"  node[{node_index}] "
          f"rule_name={rule.name!r} "
          f"reference={reference!r}"
        )
      print("PI10_4_DETAIL_END")
      print("PI10_4_RENDERED_BEGIN")
      print(rendered)
      print("PI10_4_RENDERED_END")

  print("=" * 78)
  print(
    "CROSS_GROUP_REFERENCE_GAP_DETECTED=",
    any_cross_group_reference_gap,
  )
  print(
    "REFERENCE_ENTRY_MECHANISM="
    "GENERIC_LITERATURE_REFERENCE_COLLECTION"
  )
  print(
    "REFERENCE_APPLICATION_MECHANISM="
    "CURRENTLY_SPECIALIZED_TO_DEFINITION_APPLICATION"
  )
  print(
    "AUDIT_DECISION="
    "INSPECT_PI10_4_LITERATURE_REFERENCE_METADATA_AND_BODY_BINDING"
  )


if __name__ == "__main__":
  main()
