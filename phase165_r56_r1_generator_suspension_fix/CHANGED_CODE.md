# R56-R1 変更後の関数全文

変更対象: `toda_group_proof_generic_narrative_renderer.py` の `_render_generic_narrative_statement_prose()`。import の変更なし。

```python
def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  # phase165_r42_generic_typed_prose: these are shared typed map and
  # generator-image statements; never use target-specific prose.
  kind = type(statement).__name__
  # phase165_r56_r1_generator_suspension: shared typed statement prose
  if kind == "GeneratorSuspension":
    map_name = _generic_group_map_name(statement.map)
    if map_name is not None:
      return (
        "$" + map_name + "("
        + render_toda_expression_latex(statement.source_generator)
        + ") = "
        + render_toda_expression_latex(statement.target_generator)
        + "$."
      )
  if kind == "GeneratorImage":
    map_name = _generic_group_map_name(statement.map)
    if map_name is not None:
      return (
        "$" + map_name + "("
        + render_toda_expression_latex(statement.source_generator)
        + ") = "
        + render_toda_expression_latex(statement.target_generator)
        + "$."
      )
  if kind in ("MapIsomorphism", "MapInjective", "MapSurjective"):
    map_latex = _render_generic_narrative_group_map_latex(statement.map)
    if map_latex is not None:
      meaning = {
        "MapIsomorphism": "同型写像",
        "MapInjective": "単射",
        "MapSurjective": "全射",
      }[kind]
      return "$" + map_latex + "$ は" + meaning + "である."

  reference_prose = (
    _render_phase153_r3_9_reference_statement_prose(
      statement
    )
  )

  if reference_prose is not None:
    return reference_prose

  reference_prose = (
    _render_phase153_r3_6_reference_statement_prose(
      statement
    )
  )

  if reference_prose is not None:
    return reference_prose

  aggregate_prose = (
    render_toda_group_proof_aggregate_statement_prose(
      statement
    )
  )

  if aggregate_prose is not None:
    return aggregate_prose

  if isinstance(
    statement,
    Toda56Nu4DecompositionStatement,
  ):
    return (
      r"$\nu_{4}$ の分解を用いる."
    )

  if isinstance(
    statement,
    Toda56Nu4DecompositionIsomorphismStatement,
  ):
    return (
      r"$\nu_{4}$ の分解写像は同型写像である."
    )

  if isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    window = statement.window
    return (
      "$"
      + render_toda_primary_group_latex(
        window.source_term
      )
      + r" \xrightarrow{"
      + window.first_map.name
      + r"} "
      + render_toda_primary_group_latex(
        window.middle_term
      )
      + r" \xrightarrow{"
      + window.second_map.name
      + r"} "
      + render_toda_primary_group_latex(
        window.target_term
      )
      + "$ は完全である."
    )

  if isinstance(
    statement,
    TodaDeltaImageFreeCyclicStatement,
  ):
    map_name = _generic_group_map_name(
      statement.map
    )

    if map_name is None:
      return None

    return (
      r"$\operatorname{Im}"
      + map_name
      + " = "
      + render_toda_raw_group_structure_latex(
        statement.image_group
      )
      + "$."
    )

  if isinstance(
    statement,
    TodaSuspensionKernelFreeCyclicStatement,
  ):
    map_name = _generic_group_map_name(
      statement.map
    )

    if map_name is None:
      return None

    return (
      r"$\ker "
      + map_name
      + " = "
      + render_toda_raw_group_structure_latex(
        statement.kernel_group
      )
      + "$."
    )

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
    TodaPi32Eta2DefinitionStatement,
  ):
    return (
      "$H("
      + render_toda_expression_latex(
        statement.element
      )
      + ") = "
      + render_toda_expression_latex(
        statement.image
      )
      + "$ を満たす $"
      + render_toda_expression_latex(
        statement.element
      )
      + r" \in "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + "$ を定める."
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
```
