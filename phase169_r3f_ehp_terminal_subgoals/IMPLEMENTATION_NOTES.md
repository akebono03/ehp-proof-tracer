# Phase 169 R3F — 実装と監査の範囲

## 変更ファイル・関数

1. `phase165_r14_r5_ehp_connection.py`：`audit_ehp_connection()` の直前に新規関数 `expand_registered_ehp_terminal_goal()` を追加。既存関数は不変更。既存の import 節は不変更で、新関数の局所 import を全文収録。
2. `phase165_r52_r9_shared_math.py`：関数 `shared_expansion_provider()` 全体を置換。既存 API は維持。モジュール先頭の import 節は不変更。
3. `tests/test_phase169_r3f_ehp_terminal_subgoals.py`：新規テスト関数8件を追加。import 節を含めた全文を同梱。

## 数学的な境界

- 既存の型付き `TodaDeltaInjectiveStatement` には Proposition 5.1 の複合命題を下位 Goal として要求する。
- `TodaHopfInvariantSurjectiveStatement` には $H(\nu')=\eta_5$ の関係式と Proposition 5.1 の複合命題を下位 Goal として要求する。
- 既存の終端推論規則に設定された `ProofRule.INFERENCE` の前提条件は変更しない。
- 両下位 Goal に文献順で適格な `ProofStep` が実際に構成されない限り、EHP 同型性・$\pi_5^3$ の完成を主張しない。
- Proposition 5.3 の対象群構造を直接 GIVEN として追加しない。旧専用証明の再生もしない。

## 検証

`run.ps1` は限定 pytest と、実際の引用済み Proof Context を使った terminal proposal 監査を行う。検証失敗時は両ファイルを安全に復元する。全体 pytest は Phase 169 の最終段階まで実施しない。

## 次の工程

次工程では、未証明の `INFERENCE` 前提を文献成分および既存の一般規則から導く経路の有無を確認する。群構造・写像性質を新たな GIVEN として追加しない。
