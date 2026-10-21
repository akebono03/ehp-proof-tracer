# Phase 166 R3-AA — 掲載順による実動作監査

## 対象ファイル・関数

- 新規 `phase166_r3aa_publication_runtime_audit/audit.py`：`assert_legacy_gates_absent()`、`given_records()`、`run()`、内部 `observer()` の全文
- 新規 `phase166_r3aa_publication_runtime_audit/tests/test_r3aa_guards.py`：限定テスト2件の全文
- 新規 `phase166_r3aa_publication_runtime_audit/run.ps1`：PowerShell 実行コード
- 既存の本体コード、import、既存クラス・関数・テスト：**変更なし**

## 監査内容

1. 共通探索から旧制限の呼び出しが撤去されていることを AST で検査する。
2. 命題台帳の掲載順で Proposition 5.1 の $\pi_4^3$ が使用可能であることを検査する。
3. 文献固定 `GIVEN` に現れる $\pi_4^3$ 群構造と Toda (4.5) を採取する。
4. 実際の expansion provider で生成元正規化・transport の候補を調べる。
5. `reconstruct_registered_goal()` による実探索と Web と同じ `search_group_from_registered_goal()` による探索を実行する。
6. 証明成功・失敗にかかわらず `report.json` に記録し、成功条件を満たさなければ明示的に失敗終了する。

## 限定 pytest

`python -m pytest -q phase166_r3aa_publication_runtime_audit/tests/test_r3aa_guards.py`

## 完了条件

- 先行する $\pi_4^3$ と Toda (4.5) が選別される。
- 推論規則から transport 候補が生成される。
- 直接探索と Web 入口の両方が COMPLETE になる。
- 旧使用順制限を復活させない。

## 次 Phase との境界

本 Phase では証明を修正せず、不足があれば原因を report に記録する。全体 pytest は実行しない。
