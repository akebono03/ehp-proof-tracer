# Phase 168 R3-41H — 有限巡回群の前提停止の読み取り監査

変更する既存ファイル・クラス・関数・import はありません。追加するのは監査パッケージのみです。

## 実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41h_finite_cyclic_blocker_audit.zip" `
  -DestinationPath "." `
  -Force
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41h_finite_cyclic_blocker_audit\run.ps1"
```

R3-41G の監査パッケージが同じ作業ディレクトリに残っていることが必要です。

## 監査対象

- $\pi_6^4$ と $\pi_6^3$ の実際の検索を再実行する。
- 展開0件の有限巡回群構造の前提を取り出す。
- screened `ProofStepLink` と、元の `FIXED_STATEMENT` 登録を**区別**する。
- 型付き `CyclicStructureStatement` を結論とする一般規則の登録を記録する（登録は証明ではない）。
- 実行中に証明ステップ、命題、出典を追加しない。

## 実行する pytest

```powershell
python -m pytest -q `
  ".\phase168_r3_41h_finite_cyclic_blocker_audit\tests\test_phase168_r3_41h_finite_cyclic_blocker_audit.py" `
  ".\phase168_r3_41g_zero_step_search_trace\tests\test_phase168_r3_41g_zero_step_search_trace.py"
```

## 完了条件

- 限定テストが PASS、2群を捕捉でき、根の候補・有限巡回群前提の展開0件・出典の使用可否を区別した報告書ができる。
- 証明不能な Goal を証明済みに変更しない。
- Phase 168 の Renderer を修正せず、証明探索の改善は次 Phase に分離する。
- 全体 pytest は Phase 終了まで実行しない。

出力 `phase168_r3_41h_finite_cyclic_blocker_audit\output\review_bundle.zip` を添付してください。
