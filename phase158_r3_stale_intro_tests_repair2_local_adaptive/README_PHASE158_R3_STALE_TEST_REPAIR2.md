# Phase 158-R3 stale intro tests repair2

## 原因

最初の test-only repair は GitHub 現行テストの文字列をそのまま前提にした。

local repository は GitHub より先に test contract が更新されているため、
`test_phase132_7_group_proof_cli_modes.py` では想定した旧 assertion が 0 件だった。

## 方針

local current test source を正として、存在する stale intro contract だけを検出して修正する。

Production code:
- 変更なし

対象 test files:
- `tests/test_phase132_7_group_proof_cli_modes.py`
- `tests/test_phase150_rc4_7a_cross_group_reference_normalization.py`
- `tests/test_phase153_r3_4_reference_statement_rendering_connection.py`
- `tests/test_phase144_6_r3_production_references.py`
- `tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py`
- `tests/test_phase153_r11_generic_reference_attribution_filtering.py`

## 変更規則

次の旧 contract が実際に存在するときだけ変更する。

1. `assert "使用する結果を先にまとめる." in ...`
   → `not in`

2. exact output の
   `"使用する結果を先にまとめる.\n\n"`
   → 削除

3. `startswith("使用する結果を先にまとめる.")`
   → `startswith("**[R1] ")`

すでに R3 contract に更新済みのテストは変更しない。

## pytest

apply 時に、intro 文を含んでいた test function の node id を local source から自動収集する。
その test function だけを focused pytest で実行する。

## 完了条件

- affected test functions: all passed
- remaining stale intro contracts: 0
- Phase 158-R3 112-group audit: pass
- production code changes: none

全体 pytest は Phase 158 の最後のみ。
