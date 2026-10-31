# Phase 171 R20R2R2 — pytest 実行文脈の不一致診断

## 現在の確定事項

- R20R2 の限定テストは 24 PASS、2 FAIL。
- 通常の Python プロセスで `ordered_typed_reference_steps()` は 1 件の適格な `GIVEN` を返し、`reconstruct_registered_goal()` は `PROVED`。
- pytest で実行した同じ既存テストは 2 件とも失敗した。
- 当該2件のうち1件は共通探索器を直接呼び出さないため、この2件を根拠に探索器の修正失敗とは判定できない。
- GitHub `develop` の関連ソースと既存テストを参照し、出典資格の条件は変更しない。

## 診断内容

既存 pytest テストを収集した同一プロセスの `pytest_runtest_call` フックで、元の `_fixture()` を新たに生成して次の条件を記録する。

1. 同一 `AssertionOrigin` / `CitationDecision` の Enum（列挙型）が使用されているか。
2. `assess_citation()` の結果が `ALLOWED` か。
3. `ProofStepLink` が1つ存在し、その `ProofStep` が元の `GIVEN` と一致するか。
4. テストに import された `ordered_typed_reference_steps()` と本来の関数が同一か。
5. pytest の読み込み方式と外部プラグイン自動読込が結果に影響するか。

診断はプログラムのコードや証明を変更しない。テストの成否は記録し、3種類の測定を継続する。

## 対象ファイル

- 新規 `phase171_r20r2r2_pytest_context_probe/__init__.py`
- 新規 `phase171_r20r2r2_pytest_context_probe/probe_plugin.py`：`_module_info()`、`_snapshot()`、`pytest_runtest_call()`
- 新規 `phase171_r20r2r2_pytest_context_probe/run.ps1`
- 新規 `README.md`（英語）および本ファイル（日本語）

既存ファイル・既存 API・import は変更しない。

## 次工程との境界

検証結果により根本原因を特定してから、必要なら当該箇所だけを修正する。First Successful Proof Search を理由なく戻さない。全体 pytest は Phase 終了時まで実施しない。
