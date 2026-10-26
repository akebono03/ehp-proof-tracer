# Phase 169 R4A — Proposition 4.4 と EHP の接続監査

## 現状

Phase 169 R4 の実行では、π₅³ は complete（28ステップ・Reference 6件）、π₆⁴ は partial（2ステップ・未解決4件）だった。Toda (4.5) の安定範囲は、n=3, k=2 では満たされない。

## 原文に沿った証明方針

Toda『Proposition 5.3』の証明では、π₅³→π₆⁴→π₆⁷ という EHP の部分を使用する。

(5.1) より $\pi_6^7=0$ なので $E$ は全射である。また、Proposition 4.4 より $E$ は単射である。従って $E:\pi_5^3\xrightarrow{\cong}\pi_6^4$ を示せる。η² の生成元の懸垂も別途証明する必要がある。

## 監査対象の既存ファイル

- `phase165_r52_r27_r5_literature.py`: Proposition 4.4 の一般型付き命題
- `phase165_r52_r9_shared_math.py`: 共通 Backward Search の候補生成
- `phase165_r12_r12_ehp_consequences.py`: EHP と零群から全射を導く規則
- `phase165_r12_r15_toda51.py`: (5.1) の零群特殊化
- `phase165_r12_r21_eta_generator_chain.py`: η² の生成元の懸垂
- `phase169_r3o_stable_composite_rule.py`: Toda (4.5) の安定範囲制約
- `sources/toda/Toda_04_2.tex`, `sources/toda/Toda_05_2.tex`: 文献原文

## 今回の追加ファイル

- `phase169_r4a_prop44_ehp_route_audit/audit.py` — `git_value`, `source_excerpt`, `expansion_summaries`, `describe_assertion`, `run_audit`, `render_markdown`, `main` を新規追加。
- `phase169_r4a_prop44_ehp_route_audit/tests/test_r4a.py` — 4つの読み取り専用限定テストを新規追加。
- `phase169_r4a_prop44_ehp_route_audit/run.ps1` — 実行スクリプト。
- `README.md` — 英語の実行手順。
- `AUDIT_JA.md` — 日本語の監査方針。

既存ソースと既存テストの変更対象はない。したがって import の置換、既存クラス・関数の差し替え、バックアップによる復元は不要である。

## 完了条件

1. 限定 pytest が PASS。
2. Proposition 4.4 と (5.1) の引用された型付き命題および候補を監査。
3. π₆⁴ の未解決 Goal を記録。
4. Git 追跡ファイルの状態を維持。
5. 全体 pytest を実行しない。

## 後続工程との境界

R4A は出典の存在と候補の接続状態だけを監査する。R5 で適法な一般規則が必要と判明したときのみ、関数単位で最小限の実装変更を検討する。原文の Proposition 4.4 を根拠なく無条件の GIVEN に変換しない。
