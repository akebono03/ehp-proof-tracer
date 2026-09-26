from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{path.name}: expected exactly one replacement target, found {count}"
        )
    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )


catalog_path = ROOT / "toda_group_proof_narrative_catalog.py"
arguments_path = ROOT / "toda_group_proof_narrative_arguments.py"

replace_once(
    catalog_path,
    """from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
)
""",
    """from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaLemma513Statement,
  TodaNuFamilyDefinitionStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
)
""",
)

replace_once(
    catalog_path,
    """DEFINITION_STATEMENT_TYPES = (
  TodaNuFamilyDefinitionStatement,
  TodaSigmaFamilyDefinitionStatement,
)
""",
    """DEFINITION_STATEMENT_TYPES = (
  TodaLemma513Statement,
  TodaNuFamilyDefinitionStatement,
  TodaSigmaFamilyDefinitionStatement,
)
""",
)

replace_once(
    arguments_path,
    """from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
""",
    """from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_rules import (
  TodaLemma513Statement,
)
""",
)

replace_once(
    arguments_path,
    """def extract_toda_group_proof_narrative_argument_purpose_subject(
  argument: TodaGroupProofNarrativeArgument,
):
""",
    """def _definition_statement_subject(
  statement,
):
  if isinstance(
    statement,
    TodaLemma513Statement,
  ):
    return statement.sigma_triple_prime

  return getattr(
    statement,
    "element",
    None,
  )


def extract_toda_group_proof_narrative_argument_purpose_subject(
  argument: TodaGroupProofNarrativeArgument,
):
""",
)

replace_once(
    arguments_path,
    """    for proof_step in argument.conclusion_block.steps:
      statement = proof_step.conclusion
      if not hasattr(statement, "element"):
        continue
      subject = statement.element
      if subject not in subjects:
        subjects.append(subject)
""",
    """    for proof_step in argument.conclusion_block.steps:
      statement = proof_step.conclusion
      subject = _definition_statement_subject(
        statement
      )
      if subject is None:
        continue
      if subject not in subjects:
        subjects.append(subject)
""",
)

replace_once(
    arguments_path,
    """    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    ):
      if not hasattr(
        statement,
        "element",
      ):
        continue
      if statement.element != purpose_subject:
        continue
      candidates.append(
        proof_step
      )
      continue
""",
    """    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    ):
      statement_subject = (
        _definition_statement_subject(
          statement
        )
      )
      if statement_subject is None:
        continue
      if statement_subject != purpose_subject:
        continue
      candidates.append(
        proof_step
      )
      continue
""",
)

print("Phase 144-2 sigma triple-prime definition implementation applied.")
