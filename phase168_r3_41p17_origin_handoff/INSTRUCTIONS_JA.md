# Phase 168 R3-41P17 — 探索時生成元の由来を受け渡す限定実装

## 目的と境界

R3-41P16 は、固定基準の3群で INFERENCE 39件すべてが既存 `derive_inference_proof_step()` により生成され、GIVEN 14件が探索に使用した選別済み Bridge と同一であることを観測した。

今回の R3-41P17 では、1回の探索中に Factory が生成した ProofStep の**オブジェクト同一性**だけをセッション内に記録し、一般の Matcher を再実行せずに、選別済み Bridge・文献順と組み合わせて共通 Narrative Model を試験的に構築する。

**これは数学的に独立した検証済み証明書ではない。** 呼び出し側が作成した任意の InferenceMatch / InferenceRule / Bridge を独立に認証せず、オブジェクト内部の事後変異を防ぐものでもない。したがって、標準 Web 経路は **R3-41P15 の fail-closed と R3-41P13 の matcher 再検証を引き続き使用**し、Renderer にある2つの数学的再判定も維持する。

## 変更ファイルと関数

- 変更：`phase164_r8_proofstep_factory.py` の `derive_inference_proof_step()` **関数全体**。
- 変更：`phase165_r52_r2_search_adapter.py` の `search_registered_partial_proof()` **関数全体**。既存の `proved` 通知を利用して探索で採用された ProofStep の同一性を記録。
- 新規：`proof_origin_capture.py`（Repository ルート）。`SearchOriginObservation` クラス、`capture_search_origins()`、`note_factory_inference()`、`note_accepted_search_step()`、`require_active_observation()` を新規定義。追加位置は独立モジュール内。
- 新規：`phase168_r3_41p17_origin_handoff/origin_handoff.py`。`build_origin_bound_narrative_model()` を新規定義。追加位置はパッケージ内の独立モジュール。
- 新規：`phase168_r3_41p17_origin_handoff/tests/test_phase168_r3_41p17_origin_handoff.py` に限定テストを追加。
- 既存トップレベル import の変更はない。変更対象の関数では `proof_origin_capture` の遅延 import を追加する。

変更関数全文：`full_functions/derive_inference_proof_step_FULL.py` および `full_functions/search_registered_partial_proof_FULL.py`。各 `*_BEFORE.py` に変更前の関数全文を収録。
新規モジュール・テストはそれぞれファイル全文を収録。`install.py` が変更後ファイル全文を `output/phase164_r8_proofstep_factory.py.FULL.py` および `output/phase165_r52_r2_search_adapter.py.FULL.py` に出力する。


## R1 修正（64 PASS・1 FAIL 後の再実行）

最初の実行では、偽造 INFERENCE は正しく拒否されたが、テストが期待した例外メッセージが実際の判定順序と異なった。判定はまず「探索が採用していない」を拒否するため、テスト関数 `test_forged_inference_is_rejected_before_factory_origin_check()` は `not accepted by this search` を確認する。証明探索や数学的チェックは変更していない。

失敗時の復元によりアプリの2ファイルは復旧され、`proof_origin_capture.py` は削除されたが、`output/*.before` と `output/manifest.restored.json` は残る。この復元済み状態からの再実行に対応するため、`install.py::install()` は既存バックアップが現在の原本とバイト単位で同一の場合だけ再利用し、不一致なら中断する。`restore.py::main()` は再度の復元で `manifest.restored.json` が既存でも安全に置換する。

追加テスト `test_retry_install_after_restore_reuses_only_identical_backups()` は、インストール・復元の2サイクルと改変バックアップの拒否を検証する。

修正版 ZIP ファイル名：`phase168_r3_41p17_origin_handoff_r1_retry_fix.zip`。ZIP 内のフォルダ名は従来と同じ `phase168_r3_41p17_origin_handoff` であり、`Expand-Archive -Force` によりプログラムを差し替える。**既存のバックアップを手動削除する必要はない。**

修正版の対象は `install.py::install()`・`restore.py::main()` および限定テスト2関数（元の偽造拒否テスト1件の変更、再実行テスト1件の追加）に限る。トップレベル import は変更しない。既存アプリコードの変更範囲は R3-41P17 のままである。

## インストールと限定 pytest

PowerShell で Repository のルートへ移動し、以下を実行。

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p17_origin_handoff_r1_retry_fix.zip" `
  -DestinationPath "." `
  -Force
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p17_origin_handoff\run.ps1"
```

`run.ps1` は、変更前後の3群の公開 Web 証明本文・Reference・Citation の完全比較、今回の限定 pytest、R3-41P12 文献順監査を実行する。全体 pytest は**実行しない**。

既存ファイルのバックアップは `output/phase164_r8_proofstep_factory.py.before` および `output/phase165_r52_r2_search_adapter.py.before`。失敗時には元のファイルをバイト単位で復元し、新規の `proof_origin_capture.py` を削除する。手動復元する場合：

```powershell
python -B -m phase168_r3_41p17_origin_handoff.restore
```

## 完了条件

1. 限定 pytest が PASS。
2. 3群について Factory の出力記録と探索の `proved` 採用記録が Proof Tree に対応する。
3. 偽の INFERENCE・コピー GIVEN・前回セッションの記録を受け付けない。
4. 新しい試験的 handoff が matcher を再実行しない。
5. 3群の証明本文・Reference・Citation が従来とバイト単位で一致する。
6. 標準 Web・partial・既存 API・Renderer の防御がそのままである。

## 次工程との境界

今回の観測ログを Model の検証済みフラグとして扱わない。将来の Phase では、探索内での**規則出所・選別済み Bridge の真正性**と、ログの改変耐性をさらに確定した場合に限り、標準 Web 経路への採用と既存 matcher の再検証削除を判断する。
