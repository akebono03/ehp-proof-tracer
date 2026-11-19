# Phase 175 R4R12R13R4 — H 零写像を中間命題とする一般推論

## 現状

R13R3：E の全射候補が 1 件、Δ の単射候補が 0 件。公開 Web は部分証明。すべての推論前提を再帰的に証明する必要がある。

## 変更対象

- 新規 `rule.py`：`hopf_zero_inputs`、`hopf_zero_from_injective_delta_rule`、`expand_hopf_zero_from_injective_delta`、`suspension_surjective_inputs`、`suspension_surjective_from_zero_hopf_rule`、`expand_suspension_surjective_from_zero_hopf`
- 新規 `provider.py`：`expand_public_hopf_zero_ehp`
- 既存 `phase165_r52_r9_shared_math.py`：`shared_expansion_provider` の単一の接続箇所
- 新規 `installer.py`、`audit.py`、`tests/test_rule.py`、`run.ps1`

## 監査の要点

1. `π₉⁹=0` と `H:π₉⁵→π₉⁹=0` を区別する。
2. Proposition 4.2 の H–Δ と E–H の連続した完全性を、次数まで照合する。
3. Δ の単射性は独立した証明済み ProofStep として要求する。
4. 正しい型の全前提が揃う場合だけ規則を適用する。提供する GoalExpansion は証明済みではない。
5. R13R3 の Δ 画像と群表示の照合が閉じなければ未完成を維持する。
6. 公開接続後も `generic-complete-proof` を宣言しない。

## 対象テスト・完了条件

限定 pytest：R13R4 の 7 件に加え、R13R3 と R13R2 の関連テストのみ。全体 pytest は実施しない。

- H 零写像 Goal の公開候補が 1 件。
- H 零写像を経由する E 全射 Goal の候補が 1 件。
- 不正次数・不正前提・未証明前提を拒否。
- 差分は共有 Provider の登録箇所と新規パッケージのみ。

## 次 Phase との境界

Δ 単射候補が閉じるかの調査と実際の再帰的証明探索は次段階とする。零群 GIVEN や目標群 GIVEN を登録しない。

## R13R4R1 修正

R13R2 と R13R4 の同名 `test_rule.py` が pytest 収集中に衝突したため、`run.ps1` の限定 pytest に `--import-mode=importlib` を指定する。数学規則、Provider、テスト関数、公開接続は変更しない。DryRun・本実行の両方で、同じ限定 pytest を使用する。
