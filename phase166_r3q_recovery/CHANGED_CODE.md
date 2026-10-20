# Phase 166 R3-Q 復旧

## 変更対象

- `phase165_r55_nk_only_goal.py` の `search_group_from_registered_goal()` 全体のみ。R3-Q 適用直前の `phase166_r3q_web_publication_order_backups/20261020T103615Z/phase165_r55_nk_only_goal.py` に格納された関数全体で復元する。
- 新規 `phase166_r3q_recovery/recover.py`: `function_bounds()` と `main()` を追加。対象の構文と変更箇所を検査してから復元。
- 新規 `phase166_r3q_recovery/run.ps1`: 復元後に限定テストを実行。
- 新規 `phase166_r3q_recovery/README.md`、本書。

## 変更しないもの

- import、他のクラス・関数、命題台帳、`publication_position`、`component_position`、`ProofStepLink`、Renderer、テスト本体は変更しない。
- 完成 Proof の再利用、π₅⁴専用処理、代替の資格ルールは追加しない。

## pytest

`python -m pytest -q phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py`

## 完了条件

6件 PASS および Web の π₃² 表示復旧。R3-Q は未完了のまま、目標 Relation と参照順境界の別管理を再調査する。Phase 166 の全体 pytest は実施しない。
