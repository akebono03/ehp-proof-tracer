# Phase 168 R3-41I — 共通 Renderer 終了条件・固定基準監査

読み取り専用。固定原文・実装・証明探索を変更しない。

| 群 | ProofStep | Reference 本文あり | Reference 差分行 | 証明差分行 | 基準説明の不足 |
|---|---:|---:|---:|---:|---|
| pi3_2 | 18 | 4/4 | 16 | 33 | なし（限定項目） |
| pi4_3 | 25 | 4/4 | 18 | 31 | なし（限定項目） |
| pi5_4 | 10 | 3/3 | 12 | 14 | なし（限定項目） |

## 公開経路の確認

- standard_model_is_default: `True`
- standard_explicit_legacy_retained: `True`
- standard_builds_linked_model: `True`
- explicit_partial_builds_model: `True`
- flask_standard_routes_to_model: `True`
- flask_partial_uses_model: `True`
- adapter_explicit_model_uses_common_renderer: `True`
- adapter_legacy_fallback_retained: `True`
- partial_step_uses_model_citation_numbers: `True`

## pi3_2

- 判定: MANUAL_FROZEN_TEXT_REVIEW_REQUIRED
- 証明本文に番号が現れない Reference: [2]
- 有: H の単射を完全性から導いたことを明記 (`exactness_for_injectivity`)
- 有: Im Δ = ker E = 0 を明記 (`delta_image_kernel_zero`)
- 有: H の同型性を単射性と全射性から説明 (`hopf_iso_from_bijectivity`)
- 有: 基準にない一般円周公式の本文再掲がない (`no_generic_circle_in_proof`)
- 比較ファイル: `pi3_2_frozen.txt`, `pi3_2_current.md`, `pi3_2_reference.diff`, `pi3_2_proof.diff`

## pi4_3

- 判定: MANUAL_FROZEN_TEXT_REVIEW_REQUIRED
- 証明本文に番号が現れない Reference: [1, 4]
- 有: E の全射を完全性から導いたことを明記 (`surjectivity_from_exactness`)
- 有: ker E の具体的な表示 (`kernel_presentation`)
- 有: 準同型定理を明記 (`quotient_theorem`)
- 有: 基準にも存在する対角群の一般式 (`diagonal_general_in_proof`)
- 比較ファイル: `pi4_3_frozen.txt`, `pi4_3_current.md`, `pi4_3_reference.diff`, `pi4_3_proof.diff`

## pi5_4

- 判定: MANUAL_FROZEN_TEXT_REVIEW_REQUIRED
- 証明本文に番号が現れない Reference: [1]
- 有: (4.5) への (n,m,k)=(3,4,1) の代入 (`toda45_explicit_substitution`)
- 有: (4.5) を引用して適用したことを明記 (`specialization_citation_in_proof`)
- 有: 引用する群構造を生成元の像より先に示す (`source_before_generator_image`)
- 有: 具体的な E 同型を表示 (`specific_map_isomorphism`)
- 比較ファイル: `pi5_4_frozen.txt`, `pi5_4_current.md`, `pi5_4_reference.diff`, `pi5_4_proof.diff`

## 判定上の境界

- 固定原文の論証内容・順序・詳しさを評価する。Reference 番号・順序は固定対象ではない。
- 差分行数は数学的誤りの件数ではない。説明項目の通過は全文一致を意味しない。
- Reference の未使用番号は注意情報であり、必要な数学的根拠が欠けるとの断定ではない。
- 以前の4群のバイト同一性は回帰試験であり、固定原文との同一性ではない。
- R3-41H で確認した有限巡回群構造の未解決問題は探索側の課題であり、この監査では修正しない。
- 残存する明示的 legacy API は互換境界として報告し、今回撤去しない。
- 全体 pytest は Phase 168 の終了時まで実行しない。
