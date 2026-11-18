# Phase 175 R4R12R1R1 — 監査計画

- 直前の R4R12R1 は限定テスト4件成功後、追跡ファイル許可集合の不一致で停止。
- 既存 R4R12 の `audit.py` で認められている `.pytest_cache/v/cache/nodeids` を R4R12R1 の補正検査にも反映する。
- `phase165_r52_r9_shared_math.py` 以外のソース変更は引き続き拒否する。
- 未承認の追跡ファイルの具体的なパスをエラーに出力する。
- HEAD と祖先関係、過去レポートの旧 HEAD の検証は維持する。
- 変更対象：`phase175_r4r12r1r1_tracked_cache_guard_fix/patch.py` の `reviewed_tracked_changes`（新規）、`replacement_paths`（全文）、および追加した限定テスト。
- 修正適用後、既存 R4R12 DryRun → 本実行を続ける。全体 pytest は実施しない。
- R4R12 の Gate が PASS しても、群の完成証明は次 Phase の対象とする。
