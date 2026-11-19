# Phase 175 R4R12R13R6 監査計画

## 目的

R13R5 で確認された `TORSION_GENERATOR_EXACT_MATCH=False` の具体的原因を調べる。Toda (5.8) の有限巡回成分の式と、既存先行 DB 群の生成元を型・内部構造ごとに表示し、数学的同一性を推測で登録しない。

## 変更対象

- 新規 `phase175_r4r12r13r6_torsion_generator_audit/audit.py` — `git`, `shape`, `inspect`, `run`, `main`
- 新規 `tests/test_r13r6_audit.py` — 3件の限定テスト
- 新規 `run.ps1`、`__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`

既存ファイル・クラス・関数への変更なし。

## 検証

- `python -m pytest -q --import-mode=importlib phase175_r4r12r13r6_torsion_generator_audit/tests/test_r13r6_audit.py`
- DryRun・本実行の終了コード0
- 新規 GIVEN 0、数学規則 0、公開 Provider 改変 0
- 必要な比較情報が `output/report.json` に残ること

## 完了境界

この監査では生成元を正規化せず、Delta 単射性・H 零写像・E 全射性を証明済みにしない。次段階で現行の等式規則や構造的正規化が正当化できるか調べる。全体 pytest は Phase 175 最終時のみ。
