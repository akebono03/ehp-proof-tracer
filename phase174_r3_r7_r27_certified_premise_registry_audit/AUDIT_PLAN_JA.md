# Phase 174 R3-R7-R27：Proposition 2.7 認証前提の Registry 境界監査

## 変更対象・追加位置

既存ソースファイル・クラス・関数・テストは変更しない。リポジトリ直下に `phase174_r3_r7_r27_certified_premise_registry_audit/` を新設する。

- `audit.py`：Git 履歴と保護ファイルを確認する `inspect_checkout()`、実際の Registry の命題・リンクを読む `inspect_registry()`、公開探索監査 `inspect_public_root()`、監査結果 `report()` を追加。
- `tests/test_audit.py`：模擬 Registry を使用した異常系・正常系を含む新規限定テスト関数を追加。
- `run.ps1`：DryRun、本監査、限定 pytest を実行。
- `README.md`：英語の説明。
- `CODE_FULL_JA.md`：今回の実行コードとテスト全文。

## 数学的境界

Toda Proposition 2.7 の一般関係は $H(\Delta(\iota_{2n+1}))=\pm2\iota_{2n-1}$、偶数 $n\ge2$。この文献の存在と独立の証明認証を混同しない。

`AssertionEntry`、`ProofStepLink`、`MigrationStatus.STRUCTURED` は、単独では出典認証済みの ProofStep を意味しない。R25/R26 の条件付き推論を無条件に公開登録しない。存在しない証明親を生成しない。

## 完了条件

Source Guard が PASS、文献照合 PASS、実 Registry の監査 PASS、R22 公開境界確認 PASS、限定 pytest PASS。新規 GIVEN と新規本番数学規則は 0 件。根の証明は未完成。全体 pytest は Phase 終了時のみ実施する。

## 次段階

R28 では認証済みの親ステップを現行の文献登録・検証経路から取得できるかを追跡する。現行 Registry で不足していれば、別の出典認証経路を監査する。単なるラベル・引用・模擬データを証明として格上げしない。
