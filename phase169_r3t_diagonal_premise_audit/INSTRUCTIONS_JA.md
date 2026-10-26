# Phase 169 R3T — (5.1) の前提接続に関する読み取り専用監査

目的：π₅³ の Δ 単射を説明するのに必要な π₅⁵=Z{ι₅} が、既存の (5.1) から引用可能な前提として導出できるか確認する。

## 対象

- `phase169_r3t_diagonal_premise_audit/audit.py`：新規の読み取り専用監査。
- `tests/test_phase169_r3t_diagonal_premise_audit.py`：新規限定テスト3件。
- 既存アプリケーション、既存テスト、既存文書は変更しない。

## 注意

`diagonal_pi55_goal()` は未証明の GOAL を構築するだけである。命題を新しい GIVEN として登録しない。実際の証明木から由来を確認し、成功する場合にのみ `diagonal_proof_result=inference` と記録する。

## 実行

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3t_diagonal_premise_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3t_diagonal_premise_audit\run.ps1"
```

監査結果は `output/r3t_diagonal_premise.json`。全体 pytest は Phase 169 の終了まで実行しない。
