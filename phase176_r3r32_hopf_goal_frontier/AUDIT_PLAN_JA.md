# Phase 176 R3R32 監査

## 変更対象

- 新規 `phase176_r3r32_hopf_goal_frontier/audit.py`：`function_names`、`review_file`、`git_status`、`make_report`、`main` を追加。
- 新規 `phase176_r3r32_hopf_goal_frontier/tests/test_audit.py`：限定テスト3件。
- 新規 `phase176_r3r32_hopf_goal_frontier/run.ps1`：DryRun・本実行・限定 pytest。
- 新規 `README.md` と `AUDIT_PLAN_JA.md`。既存5文書は変更しない。

## 数学的な監査対象

```text
H(ν′) = η₅                Toda (5.3)
H(α ∘ Eβ) = H(α) ∘ Eβ   Toda Proposition 2.2
E(η₅²) = η₆²             Suspension による合成の保存
H(ν′η₆²) = η₅³
η₅³ = 4ν₅               Toda (5.5), n=5
```

この監査だけでは各行の型付き証明・出典ゲート通過・共通 Backward Proof Search 到達を確認したことにはならない。

## 完了条件と境界

必要ファイルの存在と構文が確認でき、監査レポートが生成され、限定テストが通過すること。Hopf 像や群構造の証明完成は判定しない。後続でローカル R3R31 の候補生成・型付き同一性・出典ゲートを調査し、必要な場合だけ一般規則を最小限修正する。全体 pytest は Phase の最後だけ実施する。
