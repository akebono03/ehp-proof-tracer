# Phase 176 R3R29 監査仕様

## 目的

R3R28R1 で共有探索が証明可能になった Toda (5.5) の $4\nu_5=\eta_5^3$ を、Toda Proposition 2.2 の右合成公式と結び付ける際の候補生成と型の境界を監査する。

## 検証事項

- Source-first で (5.5) 第2関係、Prop 2.2、(5.3) Hopf 関係が何件採用されるか
- 合成左因子を含む右 Hopf 公式が `_formula_parts` に認識されるか
- `shared_expansion_provider` の式別候補数・規則名
- 根の生成元に用いられる右結合の合成と、公式用の左結合の合成が異なること
- `_combined_premises` が合成左因子を持つ場合に返す候補数

## 変更対象

新規 `phase176_r3r29_hopf_right_connection_audit/` のみ。

- `audit.py`：`source_guard`, `git`, `preflight`, `equation`, `probe`, `report_file`, `run`, `main` を新規追加
- `tests/test_audit.py`：4テストの新規追加
- `run.ps1`：監査と限定 pytest
- `README.md`：英語
- `AUDIT_PLAN_JA.md` と `CODE_FULL_JA.md`：日本語
- `__init__.py`：パッケージ登録

既存 API、クラス、関数、import は変更なし。実装済みの四倍関係の推論規則にも変更なし。

## 完了条件

DryRun、本実行、限定 pytest が PASS し、候補規則名と型の差異が監査 JSON に記録されること。候補が存在するだけでは証明完成としない。

## 次の R3R30 との境界

監査で確認された一般的な結合性・Hopf 値代入の欠落のみを対象にする。根の群構造の直接 GIVEN は追加しない。全体 pytest は Phase 終了時だけ実施する。
