from pathlib import Path

path = Path("toda_group_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

old_import = """from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
  TodaDeltaZeroStatement,
  TodaEtaFamilyDefinitionStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaPi32Eta2DefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp56Pi8_5QuotientStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
)
"""

new_import = """from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda45IsomorphismStatement,
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
  TodaDeltaZeroStatement,
  TodaEtaFamilyDefinitionStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaPi32Eta2DefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp56Pi8_5QuotientStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
)
"""

if old_import not in text:
    raise SystemExit(
        "Expected toda_rules import block was not found. "
        "Production file was not changed."
    )

text = text.replace(old_import, new_import, 1)

needle = """  if isinstance(
    statement,
    TodaSuspensionIsomorphismStatement,
  ):
    return (
      r"E: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \\xrightarrow{\\cong} "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
    )

"""

addition = """  if isinstance(
    statement,
    Toda45IsomorphismStatement,
  ):
    return (
      r"E^{"
      + _render_scalar_latex(
        statement.map.exponent
      )
      + r"}: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \\xrightarrow{\\cong} "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
    )

  if isinstance(
    statement,
    TodaHopfInvariantIsomorphismStatement,
  ):
    return (
      r"H: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \\xrightarrow{\\cong} "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
    )

  if isinstance(
    statement,
    TodaProp44SecondSummandRestrictionStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.decomposition_map.gamma
      )
      + r" \\mapsto "
      + render_toda_expression_latex(
        statement.composition
      )
    )

"""

if needle not in text:
    raise SystemExit(
        "Expected suspension-isomorphism rendering block was not found. "
        "Production file was not changed."
    )

text = text.replace(needle, needle + addition, 1)
path.write_text(text, encoding="utf-8")
print("Phase 143-75C implementation applied.")
print("Changed: toda_group_proof_narrative_renderer.py")
