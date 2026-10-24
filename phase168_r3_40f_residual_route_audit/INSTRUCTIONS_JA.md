# Phase 168 R3-40F — 残存互換経路の読み取り専用監査

この監査は、R3-40E による旧延期描画ループ撤去後の作業ディレクトリを対象とする。実装ファイル、命題台帳、固定基準は変更しない。

## 監査ファイル・関数

- `audit.py`：`module_ast`、`named_function`、`has_call`、`analyze_structure`、`audit_four_cases`、`markdown_report`、`main` を新規作成した。プロジェクト実装ファイルは変更しない。
- `tests/test_phase168_r3_40f_residual_route_audit.py`：4件の新規監査テスト。既存テストは変更しない。
- `run.ps1`：Windows PowerShell の実行スクリプト。

## 実行手順

リポジトリ直下で解凍した後、次を実行する。

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_40f_residual_route_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_40f_residual_route_audit\run.ps1"
```

## 目的

1. 通常の Renderer に `after_indices` を読む旧処理が残っていないことを検査する。
2. `NarrativeOrderEntry.after_indices` を既存互換 API として維持したことを確認する。
3. 標準 Web の `narrative` は Model を既定としている一方、明示的な `legacy` と Model 未指定の fallback があることを記録する。
4. 4群について、全 Proof Step の収録、依存関係逆転0件、延期描画0件を確認する。
5. R3-40E の記録があれば、Narrative のバイト単位の一致を確認する。

## 出力・完了条件

`output/audit.json`、`output/audit.md`、4群の `*_current.md`、`output/review_bundle.zip` を生成する。限定 pytest 4件 PASS と監査 PASS が完了条件。表示経路の撤去・数学的規則の変更は今回の対象外。全体 pytest は Phase 168 の最後にだけ実行する。
