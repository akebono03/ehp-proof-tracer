# Phase 168 R3-41M2 — eta 出典登録元の正規化と文章の簡潔化

## 変更対象（既存ファイル）

1. `phase165_r12_r20_eta_definition.py` — `build_cited_eta_family_definition()` の登録 locator を `Chapter V, i)` に短縮。`reference_id`, `source_id`, 命題、ProofStepLink は変更しない。import は変更なし。関数全文は `eta_definition_function_full.py`、ファイル全文は `eta_definition_full.py`。
2. `phase168_r3_5_model_renderer.py` — `render_model_backed_narrative_markdown()` 関数全文置換。M の簡潔化に加え、長い locator を表示時だけ隠す処理を削除。全文 `renderer_function_full.py`。
3. `phase168_r3_37c_reference_projection.py` — `project_reference_bodies()` 関数全文置換。全文 `reference_function_full.py`。
4. `phase168_r3_39f_frozen_comparison/audit.py` — `assess()` を更新（原文は保持）。全文 `assess_function_full.py`。
5. `phase168_r3_41l_reasoned_prose/tests/test_phase168_r3_41l_reasoned_prose.py` — 既存テスト更新。全文 `updated_r341l_test_full.py`。
6. `phase168_r3_41j2_chain_test_scope_fix/tests/test_phase168_r3_41j2_citation_provenance.py` — 出典検索文字列を正規化。変更後テスト関数全文は `updated_j2_test_function_full.py`、ファイル全文・import は `updated_j2_test_full.py` に収録し、実行時 output にも出力。

新規 `tests/test_phase168_r3_41m_concise_renderer.py` を追加し、登録情報・本文の正規化と Web 公開経路を限定検証。

`phase168_r3_10_registered_alias` の過去互換性テストも限定実行するが、そのテストの古い人工例は変更しない。文献掲載順は実装済みの `Chapter V, i)` と整合する。

## 完了条件

限定 pytest 全 PASS、原文と登録 source identity の保持、Reference 文の省略と本文簡潔化、証明の数学的事項と引用の維持、監査 ZIP 作成。全体 pytest は Phase 168 終了時だけ。

今回は R3-41M ZIP の代替であり、双方を続けて実行しない。先に R3-41M を適用済みの場合、この Installer は変更を行わず中止するため、既存ファイルを確認する必要がある。
