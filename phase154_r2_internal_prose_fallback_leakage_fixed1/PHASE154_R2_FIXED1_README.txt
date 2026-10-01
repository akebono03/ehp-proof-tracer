Phase 154-R2 Fixed1 — ν4 decomposition semantic prose

原因
----
初版 R2 では contribution insertion 側の raw fallback は抑制したが、
pi_10^4 の raw rule-name は base multi-argument Narrative の
preserved provenance derivation source から既に出力されていた。

この statement は Toda56Nu4DecompositionStatement という typed statement なので、
削除するのではなく generic semantic prose を与える。

変更対象
--------
toda_group_proof_generic_narrative_renderer.py

変更するもの
------------
- import: Toda56Nu4DecompositionStatement を追加
- _render_generic_narrative_statement_prose() 全体

変更後 import 全文
------------------
from expression import (
  Composition,
  HomotopyElement,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaDeltaMap,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from proof import (
  ProofStep,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_aggregate_statement_renderer import (
  render_toda_group_proof_aggregate_statement_prose,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_proof_statement_latex,
  render_toda_raw_group_structure_latex,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda45IsomorphismStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaNuFamilyDefinitionStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp59FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionSurjectiveStatement,
)


変更後関数全文
--------------
def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
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


新規テスト
----------
tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase154_r2_fixed1_pi10_4_replaces_raw_nu4_rule_name_with_semantic_prose():
  rendered = _render_group(
    4,
    6,
  )

  assert (
    "Toda (5.6) nu_4 decomposition integration"
    not in rendered
  )
  assert (
    r"$\nu_{4}$ の分解を用いる."
    in rendered
  )
  assert (
    r"\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}"
    in rendered
  )


def test_phase154_r2_fixed1_pi11_4_keeps_previous_r2_semantic_repairs():
  rendered = _render_group(
    4,
    7,
  )

  assert r"\text{ is injective}" not in rendered
  assert r"\text{ is exact}" not in rendered
  assert "は単射である." in rendered
  assert "は完全である." in rendered
  assert r"\pi_{11}^{4} = 0" in rendered


今回触れないもの
----------------
- semantic duplication
- transition repetition
- Reference linkage
- punctuation
- Test Suite Consolidation

完了条件
--------
1. pi_10^4 から raw rule-name
   "Toda (5.6) nu_4 decomposition integration"
   が消える。
2. 代わりに "$\nu_4$ の分解を用いる." が出る。
3. 初版 R2 で直した pi_11^4 の is injective / is exact が再発しない。
4. focused tests が PASS。
5. 全体テストは実行しない。

次 Phase 境界
------------
R2 完了後に R3 で代表群を横断再監査する。
