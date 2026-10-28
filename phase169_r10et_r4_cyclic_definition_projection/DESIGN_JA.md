# Phase 169 R10ET-R4 — 巡回群の共通 Definition 表示の最小実装

## R3B の確認事項

R3B の実行結果では、共通 Definition の Proof Tree で巡回群 $\pi_{28}^{22}$ と $\pi_{32}^{22}$ の Projection を回復できた。直和群の既存 Projection は維持された。一方、引用番号のない巡回群で本文に「より,」が残った。10 ケースすべて `complete`、Trust Boundary PASS、限定 pytest 48 PASS であった。

## 変更対象（先に列挙）

1. `phase169_r10a_verified_stable_chain_projection/projection.py` の `project_verified_stable_image_chain()` 全体。旧来の型付き根・反復懸垂・生成元・利用関係・他の利用者に関する検証をそのまま保持し、最後の引用祖先取得のみ R4 のポリシーへ変更。
2. `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` 全体。関数内部の import を明示し、引用なしの認証済み巡回群の文章を `Definition より,` に変更。その他の文章生成処理は維持。
3. 新規 `phase169_r10et_r4_cyclic_definition_projection/policy.py`。`canonical_definition_image()`、`_verified_index()`、`_ancestor_given_numbers()`、`verified_cyclic_generator_image_citation_numbers()` を新規定義する。既存の引用付き Proof Tree は元の引用検査に従う。
4. 新規 `tests/test_r10et_r4_live.py` と `tests/test_r10et_r4_patch.py`。すべてのテスト関数と import を ZIP に同梱。

新規関数は `policy.py` の module import 部分の後に、上記の順に配置する。既存ファイルの top-level import は変更しない。変更後の関数全文とファイル全文は ZIP の `patch.py` が検査済み現在版から生成し `output/<日時>/` へ保存する。元ファイルも `.before` で保持する。

## 証明と引用の境界

共通 Definition は、既存の `expand_defined_stable_element_image()` が認証できる型付き推論だけを採用する。引用付きの `GeneratorImage` は従来どおり登録済み GIVEN 祖先の検証を受ける。Definition の推論がゼロ前提でも、根の DB prior と Toda (4.5) に独立した GIVEN 引用があることを検証する。表示関数は ProofStep、Reference、引用対応を変更しない。ν、η、σ 等の名前による分岐を導入しない。

## テストと完了条件

既存の R10A、R10EQ、R10ER、R10EN、R10EL、R10ES と新規 R4 の限定 pytest を実行。共通 Definition をメモリ内で優先する検索を10ケース再実行し、完成証明・Trust Boundary、巡回群の Projection 復旧、直和群の非退行、DB prior と Toda (4.5) の維持、引用なしの不正な「より」の解消を確認する。失敗すれば本体2ファイルをバックアップから復帰する。全体 pytest は Phase 169 の終了時に限る。

## 次の段階との境界

R4 では `shared_expansion_provider()` の優先順位を変更しない。旧 cited-family 展開ルートの削除、古いテスト期待値の改訂、Reference 構造の整理も先取りしない。R5 で共通 Definition 優先を本番探索に採用するか改めて判断する。
