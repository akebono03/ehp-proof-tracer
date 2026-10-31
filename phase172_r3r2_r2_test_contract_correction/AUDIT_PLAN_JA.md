# Phase 172 R3R2：R2 回帰テストの表示契約訂正

## 監査結果

- R3 実行 HEAD：`67badf810e6b5f401c3c851b212379a974483ab9`（`develop`）。
- `PHASE172_R3_FOCUSED_1=PASS`、`PHASE172_R3_FOCUSED_2=FAIL`、`PHASE172_R3_RESTORED=PASS`。
- R2 の `test_real_complete_narrative_retains_cited_source_and_hopf_conclusion()` は、R3 が非表示にする中間式 `$\nu'\eta_{6} = \nu'E\eta_{5}$.` を本文に要求していた。
- GitHub `akebono03/ehp-proof-tracer` の `develop` において、Renderer の R2 コミット済み blob `bb267bc6...`、R2 テストの blob `0656bbd9...`、R3 関連 Projection とテストの内容を確認。
- 数学的誤り、Proof Search の失敗、Proof Tree の欠落をこのログから推定しない。R3 の新規テストが PASS していることと、本番 Renderer が復元されていることを分けて扱う。

## 変更一覧と境界

**変更する既存ファイル（1件）**

- `phase172_r2_suspension_relation_display/tests/test_projection.py`
  - 関数 `test_real_complete_narrative_retains_cited_source_and_hopf_conclusion()` 全体を訂正。本文の中間式存在条件1行を削除し、既存の `[R4] Proposition 2.2.` と `[R5] (5.3).` が Reference に残る条件に置換する。
  - import の変更なし。その他のテスト関数も変更なし。

**新規ファイル**

- `phase172_r3r2_r2_test_contract_correction/install.py`：Git 内容検査・DryRun・外部バックアップ・置換・限定テスト実行・失敗時復元。
- `phase172_r3r2_r2_test_contract_correction/run.ps1`：PowerShell 実行。
- `phase172_r3r2_r2_test_contract_correction/tests/test_install.py`：訂正ロジックの限定テスト6件。
- `phase172_r3r2_r2_test_contract_correction/payload/test_projection.py`：改訂後の R2 テストファイル全文。
- `README.md`（英語）、本計画、`CODE_FULL_JA.md`、`__init__.py`。

**R3 本体について**

- 既存の `phase172_r3_hopf_chain_display/install.py` に変更を加えず、元の検証済み Runner を再実行する。
- 成功時、元の Runner により `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` に R3 の既存予定修正が適用される。R3 コード自体の変更はない。
- 失敗時、R2 テストと Renderer をともに復元する。

## テスト

1. 訂正処理の `tests/test_install.py`：6件。
2. R3 の `phase172_r3_hopf_chain_display/tests/test_projection.py`。
3. R2 の `phase172_r2_suspension_relation_display/tests/test_projection.py`。
4. Phase 171 の η 表示テスト。
5. Phase 171 の位数4表示テスト。
6. Phase 169 の $\pi_6^4$ 叙述テスト。

各テストグループは別 pytest プロセス。全体 pytest は Phase 172 終了時のみ実行する。

## 完了条件

- `PHASE172_R3R2_RESULT=PASS_R3R2_AND_R3`。
- R3 の限定 pytest 5セットすべて PASS。
- R2 の引用済み懸垂関係は維持され、中間懸垂等式2行は非表示。
- R3 の中間 Hopf 式は表示専用に省略可能だが、最終 Hopf 等式、R3・R4・R5 出典、ProofStep 50件、Reference 8件、未解決 Goal 0、位数4証明は維持する。
- 次の R4（$H$ の全射性重複）および R5（DB prior 表示）には着手しない。
