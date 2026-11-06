# R17 変更後の関数全文

変更対象: `web_group_proof_common.py` の `_group_proof_statement_latex`。

この関数内の import ブロックも省略せず含みます。ファイル先頭の import は変更ありません。

```python
def _group_proof_statement_latex(
  statement,
) -> tuple[
  str | None,
  str | None,
]:
  from expression import Expression
  from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
  from phase165_r12_r2_quotient_rules import CyclicStructureStatement
  from proof import Relation, RelationType
  from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaSuspensionMap
  from phase165_r14_r6_generic_iso import MapInjective, MapIsomorphism, MapSurjective
  from phase168_r3_27_typed_statement_projection import group_tex, map_symbol_tex

  # A display projection of the typed map property, never a proof claim.
  if isinstance(statement, (MapInjective, MapSurjective, MapIsomorphism)):
    mapping = statement.map
    if isinstance(mapping, (TodaDeltaMap, TodaSuspensionMap, TodaHopfInvariantMap)):
      source = group_tex(mapping.source_group)
      target = group_tex(mapping.target_group)
      symbol = map_symbol_tex(mapping)
      if source is not None and target is not None and symbol is not None:
        arrow = (
          r'\hookrightarrow' if isinstance(statement, MapInjective)
          else r'\twoheadrightarrow' if isinstance(statement, MapSurjective)
          else r'\xrightarrow{\cong}'
        )
        return (f'{symbol}: {source} {arrow} {target}', None)

  if (
    isinstance(statement, CyclicStructureStatement)
    and isinstance(statement.group, TodaPrimaryGroup)
    and isinstance(statement.generator, Expression)
    and (
      statement.order is None
      or (type(statement.order) is int and statement.order >= 1)
    )
  ):
    structure = (
      FreeCyclicGroup(statement.generator)
      if statement.order is None
      else FiniteCyclicGroup(statement.order, statement.generator)
    )
    try:
      cyclic_latex = render_toda_public_group_relation_latex(
        Relation(
          lhs=statement.group,
          rhs=structure,
          relation_type=RelationType.EQUALITY,
        )
      )
    except (TypeError, ValueError):
      cyclic_latex = None
    if cyclic_latex is not None:
      return cyclic_latex, None

  abstract_group = getattr(statement, "group", None)
  abstract_invariants = getattr(statement, "invariant_summands", None)
  if (isinstance(abstract_group, TodaPrimaryGroup)
      and type(abstract_group.group_dimension) is int
      and type(abstract_group.sphere_dimension) is int
      and isinstance(abstract_invariants, tuple)):
    # A typed, already verified abstract invariant has no named generator.
    # This is a generic statement formatter, not an inference or Narrative.
    from phase173_r4_r15r9_shared_abstract_renderer.projection import (
      abstract_invariants_latex,
    )
    invariant_latex = abstract_invariants_latex(abstract_invariants)
    return (
      rf"\pi_{{{abstract_group.group_dimension}}}^{{{abstract_group.sphere_dimension}}}"
      rf" \cong {invariant_latex}",
      None,
    )

  public_group_latex = (
    render_toda_public_group_relation_latex(
      statement
    )
  )

  if public_group_latex is not None:
    return (
      public_group_latex,
      None,
    )

  try:
    latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    latex = (
      render_toda_proof_statement_latex(
        statement
      )
    )

  if latex is None:
    return (
      None,
      type(
        statement
      ).__name__,
    )

  return (
    latex,
    None,
  )
```
