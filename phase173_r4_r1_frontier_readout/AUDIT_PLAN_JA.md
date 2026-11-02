# Phase 173 R4-R1 — 既存監査結果の読み取り

## 目的

既存の `phase173_r4_r1_committed_cache_resume/audit.json` から、Toda (5.6) による $\pi_7^4$ の直和分解の証明境界を表示する。新しい GIVEN、ProofStep、規則、推測による数学的結論を追加しない。

## 変更対象

新規 `phase173_r4_r1_frontier_readout/` 配下の `readout.py`、`run.ps1`、`tests/test_readout.py`、`__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md` の7ファイルだけ。既存クラス、import、関数、公式5文書は変更しない。

## 検証項目

- AUDIT_ONLY という範囲と `OBSERVATION_ONLY_NOT_A_PROOF` の確認。
- ソース改変なし・$i=7$ の (5.6) 特殊化の確認。
- Proposition 4.4 の引用済み GIVEN 数。
- $\pi_6^3$ の先行結果資格（完成証明そのものとは区別）。
- $\pi_7^7$ の DB Goal 数（完成証明そのものとは区別）。
- Root Candidate と Subgoal の規則候補。

## 完了条件と境界

限定 pytest の PASS と、監査レポートの読み取り・整合性検証を完了条件とする。R4-R1 で必要な推論経路を判断するための観測であり、直和分解の完成を意味しない。$\pi_8^5$ の位数8、Web 表示、全体 pytest は対象外。
