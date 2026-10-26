# Phase 169 R3G1 — 文献命題と証明祖先の監査

## R3G1 修正内容

前回の `python -B -c` は、PowerShell 経由で `print("R3G_R3F3_PRESENT=True")` の二重引用符が失われ、`print(R3G_R3F3_PRESENT=True)` として実行された。これは `print()` が存在しないキーワード引数を受け取ったことによる起動エラーであり、R3F3 が欠けている証拠ではない。

R3G1 では `-c` 内の二重引用符を完全に廃止し、`from ... import ...; assert callable(...)` として確認する。成功したら PowerShell の `Write-Host` で表示する。

監査ロジック・新規テスト3件・本番コードを変更しない。

## 変更対象

- 本番の既存ファイル・クラス・関数：**変更なし**。
- 新規 `phase169_r3g1_powershell_preflight_quote_fix/audit.py`：`audit()` ほか監査専用関数を追加。
- 新規 `tests/test_phase169_r3g_hopf_source_and_composite_audit.py`：限定テスト3件を追加。
- 新規 `run.ps1`：事前検査、限定 pytest、実探索を一度だけ実行。

## 監査の意味

Toda (5.3) は Proposition 5.3 より前で $H(\nu')=\eta_5$ を述べる。
ただし、原文の存在・文献順・台帳上のメタデータ・型付き出典・受理された ProofStep は異なる。
これらを混同しない。

Proposition 5.1 の `TodaProp51FiniteDimensionalStatement` は文献 GIVEN として存在する。
既存の EHP 終端規則は `ProofRule.INFERENCE` という前提条件を持つ。
GIVEN を名前だけ変更して INFERENCE として扱わない。

## 実行対象 pytest

```powershell
python -B -m pytest -q -p no:cacheprovider `
  ".\phase169_r3g1_powershell_preflight_quote_fix\tests\test_phase169_r3g_hopf_source_and_composite_audit.py" `
  ".\phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py" `
  ".\tests\test_phase161_r3_backward_goal_schema.py"
```

退役した `tests.test_phase59_n3_ehp_chain` に依存する旧テストは今回は収集しない。

## 完了条件・Phase 境界

`R3G1_FOCUSED_PYTEST_EXIT_CODE=0`、`R3G1_AUDIT_EXIT_CODE=0`、`output/source_and_composite.json` が存在する。
証明の完成を主張しない。R3H は監査結果から真に不足する引用・導出規則だけを扱う。
全体 pytest は Phase 169 の最後にのみ実施。
