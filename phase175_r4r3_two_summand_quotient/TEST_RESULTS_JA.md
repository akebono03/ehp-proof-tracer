# Phase 175 R4R3R2 — テスト記録

## R4R3R2 — HEAD 系譜修正の検証

- Windows 実測：限定 pytest **72 passed**、`R4R3_R4_HEAD_OR_PINS_CHANGED` で停止。Source PIN は **18件**、対象未完成は不変。
- GitHub `c77a26fd` → `20622a30` は1コミットの監査専用変更と pytest キャッシュのみ。既存の数学ソースを編集していない。
- 新しい `validate_r4_lineage()` は同一 HEAD、審査済み正確な1コミット、未審査コミット、第一親不一致、実 HEAD 不一致、予期しない差分をテストする。
- 作成環境では3ファイル同時の限定 pytest が **85 passed**（模擬依存ランタイム）。模擬依存テストは実 GitHub リポジトリの証明検証の代わりではない。
- Windows DryRun / 本実行 Gate は未確認。全体 pytest 未実施。

## 前段 R4R3R1 — テスト収集修正の検証

- `run.ps1` の pytest コマンドに `--import-mode=importlib` を追加し、`-p no:cacheprovider` と3つの対象テストファイルを保持。
- 模擬依存の限定ランタイムを隔離して利用し、3テストファイル同時収集：**72 passed**。この結果は数学的な実コード検証ではない。
- 2つの異なるフォルダ内の同名 `test_audit.py` を使った独立再現で、既定モードは `import file mismatch`、`--import-mode=importlib` は2件 PASS。
- 配布コードの Python 構文、ZIP 整合性を検証。
- Windows の実コードによる DryRun・本実行 Gate は未確認。

## R4R3 作成時点の予備検査（履歴）

- Python コンパイル（全新規 `.py`）：PASS。
- 模擬データ型と模擬推論照合器を用いた限定の構造テスト：**48 passed**。
- 模擬ランタイムはテスト対象を組み立てるためのみに使用し、配布 ZIP には含めない。
- GitHub 接続で現行の主要コードと関連テストを確認した。
- 作成環境から GitHub リポジトリを clone できないため、**実際の `proof.py` を読み込んだ pytest は未実施**。

## 利用者のチェックアウトで実行する限定テスト

```powershell
python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
  phase175_r4r3_two_summand_quotient/tests/test_rule.py `
  phase175_r4r3_two_summand_quotient/tests/test_audit.py `
  phase175_r4_pi95_audit/tests/test_audit.py
```

`run.ps1` はこの限定テストの成功後、R4 Source PIN と実測報告を検査する。

## 完了条件（作成時点）

- Gate `PASS_R4R3_ISOLATED_RULE_DRYRUN`：未確認、利用者実行待ち。
- Gate `PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC`：未確認、利用者実行待ち。
- 新規一般推論規則 1件、GIVEN 0件、公開 Provider 追加 0件。
- $\pi_9^5$ の完成証明：未完了。
- Phase 全体 pytest：未実施。
