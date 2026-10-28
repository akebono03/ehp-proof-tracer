# Phase 169 R10ET-R1 監査設計

## 監査対象

GitHub `develop` の確認済み HEAD: `36e4dc41427ec4437009c96b01cacb07dc165bf6`。

対象は $\pi_{69}^{43}$、$\pi_{56}^{30}$、$\pi_{41}^{30}$、$\pi_{44}^{30}$、$\pi_{46}^{30}$、$\pi_{39}^{30}$ に加え、1-stem の $\pi_3^2$、$\pi_4^3$、$\pi_5^4$ と、2-stem の $\pi_4^2$、$\pi_5^3$、$\pi_6^4$。

## 現行コードで確認された事実

1. `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` は、`expand_cited_eta_generator`、`expand_cited_stable_family`、`expand_composite_generator_image` を先に呼び、これらが空の場合だけ `expand_defined_stable_element_image` を呼ぶ。したがって共通 Definition 適用可能性と現行採用経路は一致するとは限らない。
2. `phase168_r3_4_link_bridge.py` は検索で使用された GIVEN のみを引用リンクへ接続する。
3. `phase168_r3_3_proof_narrative_model.py` は ProofStep に紐づく出典だけを Reference に投影する。
4. `phase169_r10ec_direct_sum_narrative_projection/projection.py` は共通 Definition のゼロ前提推論と引用付き推論を区別し、証明木を改変しない圧縮表示を行う。
5. 共通 Definition は安定範囲・型・元の同一性の検証を必要とする。名前の似た元や次数だけの一致では同一視しない。

## 報告の読み方

各証明に対して `proof_steps.json` に ProofStep の番号、推論規則、前提の番号、直接引用、`GeneratorImage` の GIVEN 祖先引用、共通 Definition の適用可能性、実際に採用された共通 Definition 規則の検査結果を出力する。

`audit.json` の `references` は、引用が root の祖先であるか、GIVEN に直接対応するか、`GeneratorImage` の祖先か、証明本文に引用マーカーがあるかを示す。

`image_cited_but_common_eligible` が正でも、それだけで引用を除去してよいとは結論しない。変更が必要なら、次の段階で証明探索側の選択順と ProofStep の支持関係を最小限変更し、Trust Boundary と引用の一致を再検証する。

## 変更範囲と次段階

本 R1 で既存コード・テスト・文書は変更しない。ZIP 内に独立した監査ファイルと実行スクリプトを新規追加するだけ。全体 pytest は行わず、既存の限定テストだけ実行する。監査結果を確認してから R10ET-R2 の最小修正範囲を確定する。
