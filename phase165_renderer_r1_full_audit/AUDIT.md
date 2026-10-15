# Phase 165 Renderer 一本化 R1 — 監査仕様

## 既存コードとテストの確認

GitHub `akebono03/ehp-proof-tracer` で `toda_group_proof_narrative_renderer.py`、`phase165_r52_partial_proof.py`、`phase165_r52_r3_web_adapter.py`、`phase165_r56_presentation_adapter.py`、`web_group_proof.py`、`test_phase165_r52_r11_common_renderer.py` および過去の `phase165_renderer_architecture_audit/audit.py` を確認した。

掲載されている `toda_group_proof_narrative_renderer.py` には同名の `render_toda_group_proof_narrative_markdown` が2定義あり、過去の source には Generic モジュール import が見える。ただし GitHub とユーザーのローカルには直近 ZIP 適用による差がある。実体の判定は ZIP 実行時のローカル監査から行う。

## 変更対象

- 新規 `phase165_renderer_r1_full_audit/audit.py`：`is_production_path`、`module_name`、`parse_file`、`gather`、`report_markdown`、`main`。
- 新規 `phase165_renderer_r1_full_audit/test_audit.py`：独立した7個の監査テスト。
- 新規 `phase165_renderer_r1_full_audit/run.ps1`：限定 pytest と監査の実行。
- `README.md`、`AUDIT.md`、`CHANGED_CODE.md`：パッケージ説明のみ。プロジェクト直下の既存ドキュメントは変更しない。

## 非変更境界

既存ソース・推論規則・ProofStep・Renderer・API・登録命題・既存テスト・ドキュメントは変更しない。全体 pytest は行わない。

## 完了条件

7件の対象テスト成功、`audit.json`・`review.md` の出力、旧互換名の残存と重複定義の事実確認。監査結果だけで直ちに削除を確定しない。

## R2 との境界

R2 では R1 の結果を入力として、完成・未完成 Narrative の中間表現を統一する。R1 は実装変更を先取りしない。
