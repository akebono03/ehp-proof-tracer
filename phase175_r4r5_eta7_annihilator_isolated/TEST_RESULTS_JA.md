# Phase 175 R4R5R2 — テスト記録

## 実施済み（作成環境）

- GitHub `develop` の現行 HEAD・関連本番ファイル・関連テストを確認。
- `rule.py` と `audit.py` の構文検査を実施。
- 構造型・一般推論マッチャーを模擬した**隔離の限定テスト**：**67 passed**。
- 既存 R4R5R1 の `test_rule.py` と `test_audit.py` のテストを維持し、直和・誤用拒否のテストを追加。
- ZIP 内容の整合性・解凍検査をパッケージ作成時に実施。

## 未実施（Windows の実行結果を待つ）

- 現行 EHP Proof Tracer の実コードによる限定 pytest。
- 現行 `sphere.csv` を使った `pi_8^7`、`pi_8^4` の DB prior 認証。
- 実際の π₈⁴ の2つの生成元について、型付き一般規則を利用した ProofStep の生成。
- Web での公開証明の完成：対象外。
- 全体 pytest：Phase 175 終了時のみ。

**模擬限定テストの PASS は、実環境 Gate の PASS を意味しない。** DryRun・本実行に失敗した場合は、その出力をもとに修正する。

## 成功条件

`PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_DRYRUN` と `PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_ISOLATED_NOT_PUBLIC` がそれぞれ終了コード0で得られること。特に直和の2成分それぞれから零関係が生成され、先行完成証明の再探索は行わないこと。
