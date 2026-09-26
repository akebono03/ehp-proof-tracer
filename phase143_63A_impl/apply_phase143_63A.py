from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def replace_once(
  path: Path,
  old: str,
  new: str,
) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  if old not in text:
    raise RuntimeError(
      "expected anchor not found in "
      + str(path)
    )

  updated = text.replace(
    old,
    new,
    1,
  )

  path.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "updated "
    + str(path)
  )


generic_renderer = (
  ROOT
  / "toda_group_proof_generic_narrative_renderer.py"
)

old_prose_tail = r'''  if isinstance(
    statement,
    TodaNuFamilyDefinitionStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.element
      )
      + r"$ を \(\nu\)-family の元として定める."
    )
'''

new_prose_tail = r'''  if isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    exactness_latex = (
      render_toda_proof_statement_latex(
        statement
      )
    )

    if exactness_latex is None:
      return None

    english_suffix = (
      r" \text{ is exact}"
    )

    if exactness_latex.endswith(
      english_suffix
    ):
      exactness_latex = (
        exactness_latex[
          :-len(
            english_suffix
          )
        ]
      )

    return (
      "$"
      + exactness_latex
      + "$ は完全である."
    )

  if isinstance(
    statement,
    TodaNuFamilyDefinitionStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.element
      )
      + r"$ を \(\nu\)-family の元として定める."
    )
'''

replace_once(
  generic_renderer,
  old_prose_tail,
  new_prose_tail,
)


body_renderer = (
  ROOT
  / "toda_group_proof_narrative_argument_body_renderer.py"
)

old_import = r'''from toda_group_proof_narrative_group_structure_semantics import (
  extract_toda_group_structure_narrative_redundant_direct_premise_step_ids,
)
from toda_group_proof_narrative_step_transitions import (
'''

new_import = r'''from toda_group_proof_narrative_group_structure_semantics import (
  extract_toda_group_structure_narrative_redundant_direct_premise_step_ids,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
from toda_group_proof_narrative_step_transitions import (
'''

replace_once(
  body_renderer,
  old_import,
  new_import,
)

old_relocatable = r'''def _relocatable_toda_group_proof_narrative_direct_derivation_premises(
  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ],
  sources_by_target_id: dict[
    int,
    tuple[
      ProofStep,
      ...,
    ],
  ],
  conclusion_block: TodaGroupProofNarrativeBlock,
) -> tuple[
  ProofStep,
  ...,
]:
  return tuple(
    premise_step
    for premise_step in direct_derivation_premises
    if (
      premise_step not in conclusion_block.steps
      and not sources_by_target_id.get(
        id(
          premise_step
        ),
        (),
      )
    )
  )
'''

new_relocatable = r'''def _relocatable_toda_group_proof_narrative_direct_derivation_premises(
  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ],
  sources_by_target_id: dict[
    int,
    tuple[
      ProofStep,
      ...,
    ],
  ],
  conclusion_block: TodaGroupProofNarrativeBlock,
) -> tuple[
  ProofStep,
  ...,
]:
  return tuple(
    premise_step
    for premise_step in direct_derivation_premises
    if (
      premise_step not in conclusion_block.steps
      and not sources_by_target_id.get(
        id(
          premise_step
        ),
        (),
      )
      and not (
        is_toda_group_proof_narrative_provenance_only_statement(
          premise_step.conclusion
        )
      )
    )
  )
'''

replace_once(
  body_renderer,
  old_relocatable,
  new_relocatable,
)
