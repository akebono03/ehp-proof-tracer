# Phase 176 R3R17 監査計画

## 目的

R3R16 で共有再帰探索に接続した零像の2段階推論と、群構造の根 Goal の証明義務を区別する。新規の数学的推論規則・GIVEN を追加しない。

## 監査前に確認した既存コード・テスト

- `phase165_r52_r9_shared_math.py`: `build_shared_typed_bridge`, `shared_expansion_provider`, `search_shared_group_goal`
- `phase165_r55_nk_only_goal.py`: `search_group_from_registered_goal`
- `phase165_r52_r2_search_adapter.py`: `search_registered_partial_proof`
- `phase165_r3_recursive_search.py`: `reconstruct_registered_goal`
- `phase176_r3r16_public_connection/audit.py`, `run.ps1`（前工程の実装・限定テスト構成）

## 変更対象と追加位置

- 新規 `phase176_r3r17_root_frontier_audit/audit.py`: `preflight`, `observe`, `classify_frontier`, `describe_options`, `execute`, `main` などの読み取り専用関数
- 新規 `phase176_r3r17_root_frontier_audit/tests/test_audit.py`: テスト4件
- 新規 `phase176_r3r17_root_frontier_audit/run.ps1`, `__init__.py`, `README.md`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`
- 既存プロダクションファイル変更：なし

## 検証・完了条件

DryRun、限定 pytest 4件、本監査が成功し、出典付き零像推論と根 Goal の候補数・未解決状態が別々に報告されること。候補は証明済みとはみなさない。探索の異常時は FAIL とする。

## 次 Phase との境界

R3R17 では根構造の推論規則は実装しない。R3R18 以降で報告された不足義務の出典と一般化可能性を検討する。全体 pytest は Phase 終了時のみ実施する。
