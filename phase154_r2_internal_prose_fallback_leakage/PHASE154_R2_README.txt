Phase 154-R2 — Internal prose fallback leakage elimination

対象
----
R1 で実在を確認した次の public Narrative 漏出だけを修正する。

- raw inference-rule name:
  Toda (5.6) nu_4 decomposition integration
- English statement prose:
  \text{ is injective}
  \text{ is exact}

今回触れないもの
----------------
- semantic duplication
- transition repetition
- Reference と本文の役割接続
- punctuation
- Test Suite Consolidation

変更ファイル
------------
1. toda_group_proof_generic_narrative_renderer.py
   - _render_generic_narrative_statement_prose
2. toda_group_proof_narrative_contribution_renderer.py
   - _insert_toda_group_proof_narrative_argument_contributions
3. toda_group_proof_narrative_renderer.py
   - _render_group_proof_narrative_fact
4. tests/test_phase154_r2_internal_prose_fallback_leakage.py
   - 新規追加

import
------
import の変更なし。

変更後の関数全文
----------------

[toda_group_proof_generic_narrative_renderer.py]

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


[toda_group_proof_narrative_contribution_renderer.py]

def _insert_toda_group_proof_narrative_argument_contributions(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> str:
  insertion_indices = (
    _contribution_insertion_indices(
      markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  connector_by_target_step_id = (
    _contribution_connector_lines(
      presentation,
      ordered_contributions,
    )
  )
  insertions_by_index = {}

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    for contribution_index, contribution in enumerate(
      contributions
    ):
      contribution_line = (
        _render_generic_narrative_step(
          contribution.proof_step
        )
      )
      if not contribution_line:
        continue
      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          contribution.proof_step,
          contribution_line,
        )
      ):
        continue
      if contribution_line in markdown:
        continue

      insertion_index = insertion_indices[
        argument_index
      ][
        contribution_index
      ]
      if insertion_index is None:
        continue

      connector = (
        connector_by_target_step_id.get(
          id(
            contribution.proof_step
          )
        )
      )
      lines = []
      if connector is not None:
        lines.append(
          connector
        )
      lines.append(
        contribution_line
      )

      insertions_by_index.setdefault(
        insertion_index,
        [],
      ).append(
        "\n\n".join(
          lines
        )
      )

  rendered = markdown

  for insertion_index in sorted(
    insertions_by_index,
    reverse=True,
  ):
    contribution_fragments = insertions_by_index[
      insertion_index
    ]
    insertion = (
      "\n\n"
      + "\n\n".join(
        contribution_fragments
      )
    )

    if (
      insertion_index < len(markdown)
      and not markdown[
        insertion_index:
      ].startswith(
        "\n\n"
      )
    ):
      insertion += "\n\n"

    rendered = (
      rendered[
        :insertion_index
      ]
      + insertion
      + rendered[
        insertion_index:
      ]
    )

  return rendered


[toda_group_proof_narrative_renderer.py]

def _render_group_proof_narrative_fact(
  proof_step: ProofStep,
) -> str:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  statement = proof_step.conclusion

  generic_fact = (
    _render_generic_narrative_step(
      proof_step
    )
  )
  internal_fallbacks = {
    (
      proof_step.inference_rule.name
      if proof_step.inference_rule is not None
      else None
    ),
    (
      "`"
      + type(
        statement
      ).__name__
      + "`"
    ),
  }

  if (
    generic_fact
    and generic_fact not in internal_fallbacks
  ):
    return generic_fact

  latex = (
    _render_group_proof_narrative_latex(
      proof_step
    )
  )

  if latex is not None:
    return (
      "$"
      + latex
      + "$"
    )

  label = (
    _group_proof_narrative_statement_label(
      statement
    )
  )

  if label is not None:
    return label

  return "補助結果"


実行する pytest
---------------
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase143_50_generic_statement_prose_renderer.py
- tests/test_phase143_51a_r_provenance_semantic_catalog.py
- tests/test_phase153_r8_reference_use_prose_normalization.py

全体テストは実行しない。

完了条件
--------
1. pi_10^4 に raw rule-name fallback が出ない。
2. pi_11^4 に \text{ is injective} / \text{ is exact} が出ない。
3. injective / exactness は日本語 semantic prose で表示される。
4. pi_10^4 / pi_11^4 の最終群結論を保持する。
5. diagnostic generic block の provenance 保持仕様を壊さない。
6. focused tests が PASS する。

次 Phase との境界
-----------------
R2 は内部 prose fallback の漏出だけを扱う。
重複や接続語などの文章構成は R3 の横断再監査後に扱う。
