Phase 159 pi3_2 visible dependency topological ordering repair1

変更対象

1. toda_group_proof_narrative_contribution_renderer.py

追加位置:
order_toda_group_proof_narrative_visible_step_dependencies() の直前。

追加関数全文:

def normalize_toda_group_proof_narrative_zero_map_exactness_reason(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\\n\\n"
  )

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    for prefix in (
      "以上より, ",
      "したがって, ",
      "これより, ",
      "これらより, ",
      "完全性より, ",
    ):
      if stripped.startswith(
        prefix
      ):
        stripped = stripped[
          len(
            prefix
          ):
        ]
        break

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  for node in presentation.nodes:
    zero_step = node.proof_step
    zero_line = (
      _render_generic_narrative_step(
        zero_step
      )
    )

    if (
      not zero_line
      or "は零写像である."
      not in zero_line
    ):
      continue

    exactness_premises = tuple(
      premise
      for premise in zero_step.premises
      if classify_toda_proof_step_role(
        premise
      )
      in (
        TodaProofDependencyRole.EHP_EXACTNESS,
        TodaProofDependencyRole.EHP_WINDOW,
      )
    )
    injective_premises = tuple(
      premise
      for premise in zero_step.premises
      if (
        classify_toda_proof_step_role(
          premise
        )
        is TodaProofDependencyRole.MAP_PROPERTY
        and "は単射である."
        in (
          _render_generic_narrative_step(
            premise
          )
          or ""
        )
      )
    )

    if (
      len(
        exactness_premises
      )
      != 1
      or len(
        injective_premises
      )
      != 1
    ):
      continue

    target_key = paragraph_match_key(
      zero_line
    )
    matching_indices = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matching_indices
    ) != 1:
      continue

    paragraph_index = matching_indices[
      0
    ]
    paragraph = paragraphs[
      paragraph_index
    ]
    stripped = paragraph.strip()

    if stripped.startswith(
      "完全性より, "
    ):
      continue

    leading_length = (
      len(
        paragraph
      )
      - len(
        paragraph.lstrip()
      )
    )
    leading = paragraph[
      :leading_length
    ]

    paragraphs[
      paragraph_index
    ] = (
      leading
      + "完全性より, "
      + stripped
    )

  return "\\n\\n".join(
    paragraphs
  )

接続位置:
render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
内の
order_toda_group_proof_narrative_visible_step_dependencies()
直後。

追加呼び出し全文:

  rendered = (
    normalize_toda_group_proof_narrative_zero_map_exactness_reason(
      presentation,
      rendered,
    )
  )

import 変更:
なし。

2. tests/test_phase159_pi3_2_visible_dependency_topological_order.py

ファイル全文は payload/tests/ に同梱。
追加確認:
- E 同型 -> E 単射 -> Delta=0 -> H 全射
- pi2^1=0 -> H 単射
- H 単射 + H 全射 -> H 同型
- H 同型 -> eta2 定義 -> 最終群構造
- Delta=0 に proof graph に基づく「完全性より」を付与
- direct dependency edge のない pi3^3 と E 同型の相対順序は stable のまま維持

3. audit_phase159_pi3_2_visible_dependency_edges.py

修正:
スクリプト自身のディレクトリではなく repository root を sys.path に追加してから project module を import する。

完了条件:
focused pytest が全 PASS。
dependency-edge audit が ModuleNotFoundError なく実行。
public pi3^2 Narrative で Delta=0 が「完全性より」で表示。

次 Phase との境界:
- 全 renderer の再構築はしない。
- direct edge のない statement 間に新しい依存関係を推測しない。
- statement type による固定順位は導入しない。
- 全体テストは Phase 159 最終段階まで実行しない。
