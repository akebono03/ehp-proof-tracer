# Phase 174 R73 — 主要5文書の全文出力・正式終了前整理

## 1. 背景

ユーザー実行の R72 は Source Guard 10件、限定 pytest 38 PASS、R71 の完成8群の保存証拠を確認。$\pi_{12}^{4}$ と $\pi_{35}^{4}$ の記名 Goal は `SEARCH_FAILED` のまま、`PASS_R72_FOCUSED_AND_PREFLIGHT`。R72 レポートは主要5文書の Phase 174 Closeout 記録が未掲載であることを明示した。

GitHub `akebono03/ehp-proof-tracer` `develop` を R73 実装前に再確認し、`b66099598177d74e979492f1d04a916e6f0821a8` の主要5文書の blob SHA を固定した。R73 は R72 までの数学的結果を文書へ記録する工程であり、数学的実装は含まない。

## 2. 変更対象

既存の本番ソース、既存テスト、ProofStep、GIVEN、Inference Rule は変更しない。新規パッケージ `phase174_r3_r7_r73_closeout_documents/` に、`audit.py`、`tests/test_audit.py`、`run.ps1`、`updates/` の5文書セクション、英語 README、日本語監査記録と完全コード仕様を追加する。

実行時に更新する主要文書は次の5ファイルのみ。

1. `README.md`：英語の最新状態節を Phase 173 の過去記録より前へ挿入。旧本文は保持。
2. `docs/design.md`：日本語の現行経路と共通 Renderer の証拠境界を追記。
3. `docs/development_log.md`：日本語の R56〜R73 の履歴を追記。
4. `docs/roadmap.md`：日本語の Phase 174 現在地、最後の Gate、次 Phase との境界を追記。
5. `docs/proof_records.md`：日本語の2つの完成証明、引用件数、未完成例の証拠を追記。

### 全文ファイルの扱い

インストーラは**ローカルの現行本文をバイト単位で保存したうえで**新節を追加し、各文書の**全文を `output/full_files/` に出力**する。同じ全文を正規の5ファイルへ適用する。`output/original_files/` に旧全文の原本を残し、`output/phase174_r73_complete_documents.zip` に改訂後の全文5ファイルをまとめる。ZIP 同梱の `updates/` は挿入・追記する新節のみであり、全文そのものは Source Guard を満たしたユーザー環境で生成する。ダウンロード ZIP に元文書本文を勝手に推定して組み込まない。

## 3. Source Guard と安全性

- `HEAD` と `origin/develop` が一致し、`develop` が審査済み `b6609959` の子孫であること。
- `HEAD:<document path>` の5つの Git blob SHA と R72 監査スクリプトの Git blob SHA が GitHub 監査時と一致すること。
- staged の追跡済み変更は存在せず、実行前に既存の tracked 変更が存在しないこと。
- R72 保存 JSON が `174-R72`、完成8群、未完成2群、限定テストという監査範囲と一致すること。
- 旧 Phase 173 marker と TeX 原文を保持し、R73 節は一度だけ追加する。
- 適用前に全文5ファイルと旧全文5ファイルをファイル出力し、ZIP で照合できるようにする。ファイル変更時の OS エラーでは書き戻しを試みる。

## 4. 限定テストと Gate

新規単体テスト20件は作成環境で PASS。Windows の実リポジトリでは R73 の `run.ps1` が新規テストと R72 関連テストだけを走らせ、最後に `PASS_R73_FOCUSED_AND_FIVE_FULL_DOCUMENTS` を出力する。R73 の全文更新後、`git status -sb` には主要5文書の追跡済み変更と新規パッケージが現れるのが正常である。

R73 の成功は Phase 174 正式終了の認定ではない。R74 相当の最終 Gate で現行アクティブ `tests/` 全体 pytest を1回実行し、成功・失敗を保存し、文書に反映したうえで Closeout を判断する。任意の $n,k$ の証明完成や、全文数学意味検証はこの Gate の認定対象外とする。
