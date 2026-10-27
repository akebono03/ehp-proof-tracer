# Phase 169 R10A1 — 判定条件と再実行時のバックアップ修正

## 原因

`$E^{4}` は Toda (4.5) による群同型と、生成元の輸送等式の両方に現れる。2回の出現は正常であり、前回のテストと監査の `markdown.count("$E^{4}") == 1` は誤っていた。

## 更新対象（ファイル全文を同梱）

1. `phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py`：`test_r10a_4fold_eta_square_is_single_certified_display` 全体。import は変更なし。
2. `phase169_r10a_verified_stable_chain_projection/audit.py`：`main` 全体。import は変更なし。
3. `phase169_r10a_verified_stable_chain_projection/patch.py`：`main` 全体。import は変更なし。前回 rollback 後に残ったバックアップを、元ファイルのバイト列が一致するときだけ再利用する。既存バックアップを上書きしない。

`run.ps1`、`projection.py`、Renderer の変更仕様、および他の既存 API は一切変更していない。

## 実行

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10a1_count_assertion_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10a_verified_stable_chain_projection\run.ps1"
```

## 限定テスト

`run.ps1` は R10A 既存の4ファイルに対して限定 pytest を実行し、その後 `audit.py` を実行する。**全体 pytest は実行しない。**

## 完了条件

- 前回 rollback 済みの Renderer が pristine baseline と一致し、既存バックアップを安全に再利用できる。
- 限定 pytest が全件 PASS。
- `$E^{4}:` の群同型が一回表示される。
- `$E^{4}(\eta_{4}^{2})=\eta_{8}^{2}$` の生成元輸送等式が一回だけ表示される。
- Proof Tree の全ステップ、Reference、complete 状態、他の 2-stem 結果を保持する。

## 次 Phase との境界

R10A1 は判定条件と再実行可能性のみを修正する。`HyoujiGen.csv` に基づく一般の系列同定は次の R10B で扱う。全体 pytest は Phase 169 の最後に行う。
