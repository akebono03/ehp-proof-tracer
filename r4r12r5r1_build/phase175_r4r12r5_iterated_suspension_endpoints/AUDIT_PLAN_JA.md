# Phase 175 R4R12R5R1 — HEAD 固定値修正

- GitHub `develop` の `6cdf40e089cb2950d2ae9a6aadb2a36188ca0e7d` → `9203e1a8c077320a58214bda40d9bfeb17704f58` は1コミットの前進（ahead 1、behind 0）。
- 修正対象: `phase175_r4r12r5_iterated_suspension_endpoints/installer.py` の `EXPECTED_HEAD` 定数。
- 追加テスト: `tests/test_installer.py` の `test_reviewed_head_pin_matches_current_develop`。
- 既存 R4R3 `rule.py` の Git blob、追跡ファイルの許可リスト、branch、型検証、6つの証明義務の検査を保持。
- DryRun と本実行、限定 pytest を行い、全体 pytest は行わない。
- 新規 GIVEN 0、数学規則 0、群の完成証明は対象外。
