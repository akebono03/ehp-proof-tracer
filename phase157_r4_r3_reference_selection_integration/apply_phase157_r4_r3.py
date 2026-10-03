from pathlib import Path

REFERENCES = Path("toda_group_proof_narrative_references.py")
CONTRIBUTION = Path("toda_group_proof_narrative_contribution_renderer.py")
RENDERER = Path("toda_group_proof_narrative_renderer.py")


BOUNDARY_IMPORT = '''from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_component,
  is_toda_fixed_statement_component_reference_eligible,
)
'''

FILTER_FUNCTION = r'''

def filter_phase157_r4_representative_reference_entries_by_fixed_statement_boundary(
  entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  root_step: ProofStep,
) -> tuple[
  TodaGroupProofNarrativeReferenceEntry,
  ...,
]:
  if not isinstance(
    entries,
    tuple,
  ):
    raise TypeError(
      "entries must be a tuple"
    )

  if not all(
    isinstance(
      entry,
      TodaGroupProofNarrativeReferenceEntry,
    )
    for entry in entries
  ):
    raise TypeError(
      "entries must contain only "
      "TodaGroupProofNarrativeReferenceEntry objects"
    )

  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  conclusion = root_step.conclusion
  lhs = getattr(
    conclusion,
    "lhs",
    None,
  )

  target = (
    getattr(
      lhs,
      "group_dimension",
      None,
    ),
    getattr(
      lhs,
      "sphere_dimension",
      None,
    ),
  )

  representative_targets = {
    (8, 5),
    (10, 4),
    (12, 5),
    (15, 8),
    (16, 9),
  }

  if target not in representative_targets:
    return entries

  root_boundary = (
    classify_toda_literature_statement_step(
      root_step
    )
  )

  target_reference_locator = (
    None
    if root_boundary is None
    else root_boundary.reference_locator
  )
  target_component_key = (
    None
    if root_boundary is None
    else root_boundary.component_key
  )

  retained_entries = []

  for entry in entries:
    retained_steps = []

    for proof_step in entry.proof_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is None
        or boundary.classification
        != TodaLiteratureStatementClassification.FIXED_STATEMENT
        or boundary.component_key is None
      ):
        continue

      component = (
        get_toda_fixed_statement_component(
          boundary.reference_locator,
          boundary.component_key,
        )
      )

      if component is None:
        continue

      if (
        target_reference_locator is not None
        and target_component_key is not None
        and not is_toda_fixed_statement_component_reference_eligible(
          component,
          target_reference_locator,
          target_component_key,
        )
      ):
        continue

      retained_steps.append(
        proof_step
      )

    if not retained_steps:
      continue

    retained_entries.append(
      replace(
        entry,
        number=len(
          retained_entries
        ) + 1,
        proof_steps=tuple(
          retained_steps
        ),
      )
    )

  return tuple(
    retained_entries
  )
'''


def insert_boundary_import(text: str) -> str:
    if "from toda_literature_statement_boundary import (" in text:
        return text

    anchor = "from toda_group_proof_presentation import (\n"
    index = text.find(anchor)
    if index < 0:
        raise SystemExit(
            "references import anchor not found"
        )

    return (
        text[:index]
        + BOUNDARY_IMPORT
        + text[index:]
    )


def insert_filter_function(text: str) -> str:
    name = (
        "def filter_phase157_r4_representative_reference_entries_"
        "by_fixed_statement_boundary("
    )
    if name in text:
        return text

    anchor = (
        "\ndef filter_toda_group_proof_narrative_reference_entries_by_step_usage("
    )
    index = text.find(anchor)
    if index < 0:
        raise SystemExit(
            "reference filter insertion anchor not found"
        )

    return (
        text[:index]
        + FILTER_FUNCTION
        + text[index:]
    )


def add_reference_import_name(
    text: str,
) -> str:
    name = (
        "filter_phase157_r4_representative_reference_entries_"
        "by_fixed_statement_boundary"
    )
    if name in text:
        return text

    anchor = (
        "  filter_toda_group_proof_narrative_reference_entries_by_body_usage,\n"
    )
    if anchor not in text:
        raise SystemExit(
            "reference import-name anchor not found"
        )

    return text.replace(
        anchor,
        (
            "  filter_phase157_r4_representative_reference_entries_"
            "by_fixed_statement_boundary,\n"
            + anchor
        ),
        1,
    )


BUILD_BLOCK = '''  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
'''

FILTER_BLOCK = '''  reference_entries = (
    filter_phase157_r4_representative_reference_entries_by_fixed_statement_boundary(
      reference_entries,
      presentation.root_step,
    )
  )
'''


def insert_filter_after_build(
    text: str,
    expected_minimum: int,
) -> str:
    already = text.count(
        "filter_phase157_r4_representative_reference_entries_by_fixed_statement_boundary(\n"
        "      reference_entries,"
    )
    if already >= expected_minimum:
        return text

    count = text.count(
        BUILD_BLOCK
    )
    if count < expected_minimum:
        raise SystemExit(
            "not enough reference build blocks found: "
            + str(count)
        )

    parts = text.split(
        BUILD_BLOCK
    )
    output = parts[0]

    inserted = 0
    for part in parts[1:]:
        output += BUILD_BLOCK
        if inserted < expected_minimum:
            output += FILTER_BLOCK
            inserted += 1
        output += part

    return output


def main():
    for path in (
        REFERENCES,
        CONTRIBUTION,
        RENDERER,
    ):
        if not path.exists():
            raise SystemExit(
                f"target not found: {path}"
            )

    references_text = REFERENCES.read_text(
        encoding="utf-8"
    )
    references_text = insert_boundary_import(
        references_text
    )
    references_text = insert_filter_function(
        references_text
    )
    REFERENCES.write_text(
        references_text,
        encoding="utf-8",
        newline="\n",
    )

    contribution_text = CONTRIBUTION.read_text(
        encoding="utf-8"
    )
    contribution_text = add_reference_import_name(
        contribution_text
    )
    contribution_text = insert_filter_after_build(
        contribution_text,
        expected_minimum=1,
    )
    CONTRIBUTION.write_text(
        contribution_text,
        encoding="utf-8",
        newline="\n",
    )

    renderer_text = RENDERER.read_text(
        encoding="utf-8"
    )
    renderer_text = add_reference_import_name(
        renderer_text
    )
    renderer_text = insert_filter_after_build(
        renderer_text,
        expected_minimum=3,
    )
    RENDERER.write_text(
        renderer_text,
        encoding="utf-8",
        newline="\n",
    )

    print("Phase157-R4-R3 changes applied.")
    print(f"updated: {REFERENCES.resolve()}")
    print(f"updated: {CONTRIBUTION.resolve()}")
    print(f"updated: {RENDERER.resolve()}")


if __name__ == "__main__":
    main()
