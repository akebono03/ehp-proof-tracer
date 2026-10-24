# Phase 168 R3-41G — 実探索で ProofStep が0件となる原因の読み取り専用監査

## 変更対象

既存のソースファイル、クラス、関数、テストは変更しない。追加するのは次のファイルのみ。

- `phase168_r3_41g_zero_step_search_trace/audit.py`
- `phase168_r3_41g_zero_step_search_trace/tests/test_phase168_r3_41g_zero_step_search_trace.py`
- `phase168_r3_41g_zero_step_search_trace/run.ps1`
- `phase168_r3_41g_zero_step_search_trace/__init__.py`
- `phase168_r3_41g_zero_step_search_trace/README.md`
- `phase168_r3_41g_zero_step_search_trace/INSTRUCTIONS_JA.md`

## 実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41g_zero_step_search_trace.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41g_zero_step_search_trace\run.ps1"
```

## 監査内容

本番検索入口を使用して、$\pi_6^4$、$\pi_6^3$ と完成対照群 $\pi_5^4$、$\pi_4^3$ を観測する。

- Root Goal の展開候補数と規則名
- 子 Goal の展開と未解決イベント
- 検証済み ProofStep の採用イベント
- `PartialProofResult.proven_steps` に実際に残った証明ステップ数
- 使用可能な Given / Reference Link の件数
- `found 0` が「候補なし」「前提不成立」「探索前段階」のどれに相当するか

`audit.json` の分類は監査用であり、数学的な真偽判定や新しい証明を意味しない。
採用イベントがあっても、証明検索結果に含まれないものは Renderer に補充しない。

## テスト・完了条件

限定 pytest: 新規5件と既存の関連テストだけ。全体 pytest は実行しない。

4群の実際の検索と観測が例外なしで終了し、`output/review_bundle.zip` を生成できれば監査実行完了。
分類とログから次の Phase の対象を決める。未解決の数学的根拠は捏造しない。
