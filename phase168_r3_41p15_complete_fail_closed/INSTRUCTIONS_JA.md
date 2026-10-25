# Phase 168 R3-41P15 — Complete Web 信頼境界の fail-closed 化

## 実装前の確認

GitHub `akebono03/ehp-proof-tracer`、`develop`、2026年10月24日時点の以下を確認した。

- `web_group_proof.py`: `build_standard_web_group_proof_view()` の完全証明で検証を迂回できる3条件
- `phase168_r3_41p13_trust_boundary/verification.py`: GIVEN 出典・文献位置、INFERENCE 照合、未対応の `ProofRule` 拒否
- `phase168_r3_41p14_trust_boundary_audit`: 既存の迂回監査とテスト
- `phase168_r3_3_proof_narrative_model.py`、`phase168_r3_4_link_bridge.py`、`phase168_r3_27_typed_statement_projection.py`、`phase168_r3_5_model_renderer.py`
- R3-41O／P12／P13／P14 および Link Bridge、Backward Search 関連テスト

アップロード済み R3-41P14 実行ログ：38件 PASS。3群の全文・Citation 一致。迂回条件3件を検出。

## 変更一覧

1. `web_group_proof.py` の **`build_standard_web_group_proof_view()` 関数全体**のみ変更。
   - `COMPLETE` の場合、検索で得た screened Bridge が無ければ `UnverifiedProofTree` を送出。
   - 引用対象の位置付き命題が確定できなければ同様に拒否。
   - それ以外の COMPLETE は無条件に既存 `verify_proof_tree_for_narrative()` に渡し、未対応 ProofRule は検証関数に拒否させる。
   - `PARTIAL`、明示的 `legacy` と `trace` は従来どおり。既存トップレベル import 変更なし。
2. `phase168_r3_41p14_trust_boundary_audit/tests/test_phase168_r3_41p14_trust_boundary_audit.py` の **`test_complete_unverified_routes_reach_model_without_invoking_boundary()` 関数全体**を修正後の期待値に更新。
   - 関数の新名称 `test_complete_web_boundary_is_always_required()`。
   - P14 監査本体・保存済み監査結果は改変しない。新規テストの import 変更なし。
3. 新規 `phase168_r3_41p15_complete_fail_closed/tests/test_phase168_r3_41p15_complete_fail_closed.py` 追加。パッケージ内の `tests/` の配下に配置。
4. `install.py`、`snapshot.py`、`restore.py`、`run.ps1` を新規追加。

変更後の Web 関数全体は `full_functions/build_standard_web_group_proof_view_FULL.py` に格納した。更新後の P14 テストファイル全文は `tests/test_phase168_r3_41p14_trust_boundary_audit_FULL.py` に格納した。変更後アプリファイル全文と更新後テストファイル全文は、実行時に `output/*.FULL.py` へ保存される。

**Model / Renderer / ProofStep / 検証関数には手を加えない。** `_stable_eta_renaming_shape()` と `prop42_exactness_indices()` は維持。

## Windows PowerShell

リポジトリルートで実行：

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p15_complete_fail_closed.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p15_complete_fail_closed\run.ps1"
```

P13・P14 が導入済みであることを前提とする。実行順序は、3群変更前 snapshot、AST 検査とバックアップ、関数差し替え、限定 pytest、変更後 snapshot、R3-41P12 文献順監査、ZIP 作成。

`run.ps1` 失敗時はバックアップと SHA-256 照合に基づき対象2ファイルを復元する。手動復元：

```powershell
python -B -m phase168_r3_41p15_complete_fail_closed.restore
```

**全体 pytest は実行しない。** R3-41P14 旧監査の `audit.py` は失敗前の履歴監査として保存し、再実行しない（現在の修正後は「迂回可能」を意味する旧期待値には一致しなくなる）。

## 完了条件

- 限定 pytest が通る。
- `missing_context` と `missing_citing_position` は検証前に拒否し Model 構築0回。
- 未対応規則は既存検証関数に渡されて拒否される。
- 本物の3群の証明本文・Reference・Citation が変更前と完全一致。
- 文献順監査 PASS、partial／互換 API 回帰 PASS。
- 実行後に変更一覧・適用 SHA・テスト結果を確認する。

## 次 Phase との境界

今回の境界は標準 Web の complete に限る。任意に渡された `InferenceRule` の真正性、人工 Bridge の探索出所、任意の `ProofNarrativeModel` の健全性は依然として保証しない。次工程ではその保証の範囲を扱うまで Renderer の形状チェックを解除しない。
