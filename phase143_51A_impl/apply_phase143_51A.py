from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERIC = ROOT / "toda_group_proof_generic_narrative_renderer.py"
ARGUMENT = ROOT / "toda_group_proof_narrative_argument_body_renderer.py"


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(old)

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def patch_generic_renderer() -> None:
  text = GENERIC.read_text(
    encoding="utf-8"
  )

  old_import = '''from homotopy_groups import (
  TodaDeltaMap,
  TodaHopfInvariantMap,
  TodaSuspensionMap,
)
'''
  new_import = '''from homotopy_groups import (
  TodaDeltaMap,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
'''
  text = replace_once(text, old_import, new_import, "homotopy_groups import")

  old_catalog_import = '''from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
'''
  new_catalog_import = '''from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_catalog import (
  REFERENCE_STATEMENT_TYPES,
)
'''
  text = replace_once(text, old_catalog_import, new_catalog_import, "narrative catalog import")

  old_rules_import = '''from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)
'''
  new_rules_import = '''from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionSurjectiveStatement,
)
'''
  text = replace_once(text, old_rules_import, new_rules_import, "toda_rules import")

  old_statement_prose = r'''def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  if isinstance(
    statement,
    _GENERIC_INJECTIVE_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は単射である."
    )

  if isinstance(
    statement,
    _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は全射である."
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

  return None
'''
  new_statement_prose = r'''def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  if isinstance(
    statement,
    _GENERIC_INJECTIVE_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は単射である."
    )

  if isinstance(
    statement,
    _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は全射である."
    )

  if isinstance(
    statement,
    _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は同型写像である."
    )

  if isinstance(
    statement,
    _GENERIC_ZERO_MAP_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は零写像である."
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

  if isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.element
      )
      + r"$ を \(\sigma\)-family の元として定める."
    )

  return None
'''
  text = replace_once(text, old_statement_prose, new_statement_prose, "statement prose renderer")

  old_types = '''_GENERIC_SURJECTIVE_STATEMENT_TYPES = (
  TodaHopfInvariantSurjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)


def _generic_group_map_name(
'''
  new_types = '''_GENERIC_SURJECTIVE_STATEMENT_TYPES = (
  TodaHopfInvariantSurjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)


_GENERIC_ISOMORPHISM_STATEMENT_TYPES = (
  TodaHopfInvariantIsomorphismStatement,
  TodaSuspensionIsomorphismStatement,
)


_GENERIC_ZERO_MAP_STATEMENT_TYPES = (
  TodaDeltaZeroStatement,
  TodaHopfInvariantZeroStatement,
)


_GENERIC_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES = (
  *REFERENCE_STATEMENT_TYPES,
  TodaProp44DecompositionMap,
)


def _is_generic_narrative_provenance_only_statement(
  statement,
) -> bool:
  return isinstance(
    statement,
    _GENERIC_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES,
  )


def _generic_group_map_name(
'''
  text = replace_once(text, old_types, new_types, "generic statement type groups")

  old_map = r'''def _generic_group_map_name(
  group_map,
) -> str | None:
  if isinstance(
    group_map,
    TodaSuspensionMap,
  ):
    return "E"

  if isinstance(
    group_map,
    TodaHopfInvariantMap,
  ):
    return "H"

  if isinstance(
    group_map,
    TodaDeltaMap,
  ):
    return r"\Delta"

  return None
'''
  new_map = r'''def _generic_group_map_name(
  group_map,
) -> str | None:
  if isinstance(
    group_map,
    TodaSuspensionMap,
  ):
    return "E"

  if isinstance(
    group_map,
    TodaIteratedSuspensionMap,
  ):
    exponent = group_map.exponent

    if (
      not isinstance(
        exponent,
        int,
      )
      or isinstance(
        exponent,
        bool,
      )
      or exponent < 1
    ):
      return None

    if exponent == 1:
      return "E"

    return (
      r"E^{"
      + str(
        exponent
      )
      + "}"
    )

  if isinstance(
    group_map,
    TodaHopfInvariantMap,
  ):
    return "H"

  if isinstance(
    group_map,
    TodaDeltaMap,
  ):
    return r"\Delta"

  return None
'''
  text = replace_once(text, old_map, new_map, "group map name renderer")

  old_block_sig = '''def _render_generic_narrative_proof_block(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
  show_dependency_labels: bool = True,
) -> tuple[
'''
  new_block_sig = '''def _render_generic_narrative_proof_block(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
  show_dependency_labels: bool = True,
  suppress_provenance_only: bool = False,
) -> tuple[
'''
  text = replace_once(text, old_block_sig, new_block_sig, "proof block signature")

  old_validation = '''  if not isinstance(
    show_dependency_labels,
    bool,
  ):
    raise TypeError(
      "show_dependency_labels must be a bool"
    )

  block = blocks[
'''
  new_validation = '''  if not isinstance(
    show_dependency_labels,
    bool,
  ):
    raise TypeError(
      "show_dependency_labels must be a bool"
    )

  if not isinstance(
    suppress_provenance_only,
    bool,
  ):
    raise TypeError(
      "suppress_provenance_only must be a bool"
    )

  block = blocks[
'''
  text = replace_once(text, old_validation, new_validation, "proof block validation")

  old_loop = '''  for proof_step in block.steps:
    lines.append(
      _render_generic_narrative_step(
        proof_step
      )
    )
    lines.append(
      ""
    )

    short_exact_sequence_latex = (
'''
  new_loop = '''  for proof_step in block.steps:
    if (
      suppress_provenance_only
      and _is_generic_narrative_provenance_only_statement(
        proof_step.conclusion
      )
    ):
      continue

    lines.append(
      _render_generic_narrative_step(
        proof_step
      )
    )
    lines.append(
      ""
    )

    short_exact_sequence_latex = (
'''
  text = replace_once(text, old_loop, new_loop, "proof block step loop")

  GENERIC.write_text(text, encoding="utf-8")
  print(f"updated {GENERIC}")


def patch_argument_renderer() -> None:
  text = ARGUMENT.read_text(encoding="utf-8")

  old_call = '''      _render_generic_narrative_proof_block(
        presentation,
        blocks,
        block_index,
        show_dependency_labels=False,
      )
'''
  new_call = '''      _render_generic_narrative_proof_block(
        presentation,
        blocks,
        block_index,
        show_dependency_labels=False,
        suppress_provenance_only=True,
      )
'''
  text = replace_once(text, old_call, new_call, "argument generic block call")

  ARGUMENT.write_text(text, encoding="utf-8")
  print(f"updated {ARGUMENT}")


def main() -> None:
  patch_generic_renderer()
  patch_argument_renderer()


if __name__ == "__main__":
  main()
