# Phase 174 R3-R7-R2 監査計画

## 判明している事実

前工程 R3-R7-R1 の PowerShell 実測は、限定 pytest 36 PASS、GitHub／ローカル HEAD `992975395195a0e49955617ba1ae772127036dde` 一致、Source Guard PASS。`π_12^7=0` に対する source-first Root 候補は 0 件で、`π_11^6` は search_failed だった。

## 今回の目的

Toda Proposition 5.9 の転写には、`π_13^13 →Δ π_11^6 →E π_12^7 →H π_12^13` の EHP 完全列と、その出典中での `Δ` 同型の主張がある。しかし、出典中の主張を target の直接 GIVEN として登録してはならない。普遍的な Toda Proposition 4.2 の特殊化、`π_12^13=0` の Toda (5.1)、`Δ` の全射性／同型性、`π_11^6` の巡回群構造を別々の型付き Goal として検査する。

## 監査時の禁止事項

1. 直接 `π_12^7=0` という GIVEN を追加しない。
2. `π_11^6=Z{Δι_13}` を直接 GIVEN にしない。
3. 証明していない `MapIsomorphism(Δ)` を証明済みとして扱わない。
4. 対象群の専用検索・専用 Narrative を作らない。
5. 既存の本体・テスト・5文書を変更しない。
6. Phase の終わりまで全体 pytest を実行しない。

## 変更対象（新規のみ）

- `phase174_r3_r7_r2_ehp_chain_audit/__init__.py`
- `phase174_r3_r7_r2_ehp_chain_audit/audit.py`：すべての新規関数は同ファイル内に全定義。
- `phase174_r3_r7_r2_ehp_chain_audit/tests/test_contract.py`
- `phase174_r3_r7_r2_ehp_chain_audit/tests/test_repo.py`
- `phase174_r3_r7_r2_ehp_chain_audit/run.ps1`
- `phase174_r3_r7_r2_ehp_chain_audit/README.md`
- `phase174_r3_r7_r2_ehp_chain_audit/AUDIT_PLAN_JA.md`
- `phase174_r3_r7_r2_ehp_chain_audit/CODE_FULL_JA.md`

## 完了条件

DryRun で現行ソースと R1 の証跡が検証でき、本実行で EHP の隣接2ウィンドウが型付きで適合する。全ての推論候補数と `π_11^6` の未解決 Goal を JSON に保存する。既存の 16 ステップ完成証明を変更しない。候補が生成できたとしても、それを証明完成とは宣言しない。

## 次 Phase の境界

R3-R7-R3 では監査された個別の未解決前提と出典を再確認し、数学的に成立する一般推論のみを検討する。本 Phase は inference rule（推論規則）を実装しない。
