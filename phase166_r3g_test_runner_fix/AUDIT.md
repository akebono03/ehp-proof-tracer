# Phase 166 R3-G テスト実行修正

- 修正対象: `phase166_r3g_test_runner_fix/run.ps1`（新規）。
- 問題: 退避済みの `tests/test_phase49_probe.py` を旧 `run.ps1` が直接指定し、pytest の収集時に終了した。
- 対処: 当該2テストを除き、現在の R3-G、文献登録、Toda (4.5)、共通探索の限定テストを指定する。
- 本番コード変更: なし。`install.py` 再実行: なし。
- 完了条件: 対象テストが PASS。全体 pytest は Phase 166 終了まで実行しない。
- 次 Phase との境界: R3-G テスト通過後に π₅⁴ の証明探索を別途再実行する。
