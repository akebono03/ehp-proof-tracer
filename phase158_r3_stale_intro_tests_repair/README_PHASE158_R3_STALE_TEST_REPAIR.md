# Phase 158-R3 stale intro tests repair

## 変更対象

Production code:
- 変更なし

Test files:
- `tests/test_phase132_7_group_proof_cli_modes.py`
- `tests/test_phase150_rc4_7a_cross_group_reference_normalization.py`
- `tests/test_phase153_r3_4_reference_statement_rendering_connection.py`
- `tests/test_phase144_6_r3_production_references.py`
- `tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py`
- `tests/test_phase153_r11_generic_reference_attribution_filtering.py`

## 変更する test functions

- `test_phase132_7_group_proof_default_mode_is_narrative`
- `test_phase132_7_group_proof_narrative_mode_uses_narrative_renderer`
- `test_phase150_rc4_7a_pi10_4_numbers_normalized_references`
- `test_phase150_rc4_7a_pi12_5_numbers_normalized_references`
- `test_phase150_rc4_7a_pi16_9_numbers_normalized_references`
- `test_phase153_r3_4_reference_renderer_accepts_statement_lines_without_breaking_old_api`
- `test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section`
- `test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary`
- `test_phase153_r11_pi6_3_generic_section_excludes_root_self_reference`

## 修正内容

R3 以前:
- `使用する結果を先にまとめる.` が存在することを期待

R3 以後:
- public renderer では `## 使用する結果` を確認
- intro 文が存在しないことを確認
- lower-level Reference renderer では `**[R1] ...**` から直接始まることを確認

Reference numbering、Reference attribution、statement、proof body の期待値は変更しない。

## import

変更なし。

## 実行する pytest

変更した test function だけを node id 指定で実行する。
同じ test file に存在する Phase 157 後の別 stale expectation は今回の scope 外。

## 完了条件

- focused repaired tests: all passed
- remaining positive intro expectations: 0
- Phase 158-R3 112-group audit: pass
- production code changes: none

## 次 Phase との境界

これは Phase 158-R3 の test-only cleanup。
prose / formatting の横断改善は Phase 158-R4 以降で扱う。
全体 pytest は Phase 158 の最後のみ。
