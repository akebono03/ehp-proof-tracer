# Phase 168 R3-41P9 — 監査仕様

## 現状

R3-41P8 で、型付きの偽 ProofStep が ProofNarrativeModel に格納できることを確認した。安定 $\eta$ 表記と EHP 完全性の表示検証を迂回すると、数学的に誤った文章が表示される。

## 監査対象

- `phase165_r3_recursive_search.py` の `reconstruct_registered_goal()` における `find_inference_matches_for_rule()` と `derive_inference_proof_step()` の実行。
- `phase164_r8_proofstep_factory.py` の `apply_inference_match()` の実行。
- `phase165_r52_partial_proof.py` の COMPLETE 受理条件と `phase168_r3_3_proof_narrative_model.py` の Model 投影。
- `web_group_proof.py` からの公開経路と3群の全文、Reference、Citation、固定基準。

## 変更対象

アプリケーション本体のファイル・関数・クラス・import は**変更しない**。
新規パッケージ `phase168_r3_41p9_trust_path_audit` の `audit.py`、`run.ps1`、テストと監査資料だけを追加する。

## 判定の限界

- 計測したファクトリ呼び出し数と、最終 Model に含まれる推論 Step 数の差は「不正な証明」の数ではない。
- 計測で発見できない別経路から供給された Step の検証履歴を、この監査だけで完全に証明することはできない。
- 数学的チェックの削除や新しい「検証済み」フラグの追加は今回行わない。
- 全体 pytest は Phase 終了時にのみ実行する。

## 次工程との境界

R3-41P9 は信頼経路の観測までとする。表示側から数学的チェックを取り除く判断は、真に検証済みの Proof Tree の供給契約が定義・テストされてから行う。
