# Phase 173 R4-R1 — 確認済み HEAD `c352f7d2` 対応（監査のみ）

## 変更対象（開始時に確認済み）

- `phase173_r4_r1_typed_premise_probe/audit.py` の `REVIEWED_HEADS` 定数のみ更新。`guard_source_files()` の本体や `REVIEWED_BLOBS` は変更しない。
- `phase173_r4_r1_typed_premise_probe/tests/test_audit.py` の `test_reviewed_head_is_strictly_pinned()` 全体更新、新規 `test_reviewed_c352_head_accepts_only_unchanged_source_blobs()` と `test_unknown_new_head_still_rejected()` を末尾に追加。
- `README.md` と本監査計画、`CODE_FULL_JA.md` を最新状況に更新。

## 実施前の実コード・テスト確認

2026-11-02 の GitHub `akebono03/ehp-proof-tracer` `develop` を確認。現在の HEAD は `c352f7d24d3156ba7cde26ebb0933c4680a8c813`。`6f5adde0` との差分は、`phase173_r4_r1_frontier_readout/` 内の監査・読み出しファイル7件の追加のみ。`phase165_r52_r9_shared_math.py`、`toda_rules.py`、Toda 出典などの数学的なコードは変更なし。関連する `phase173_r4_r1_frontier_readout/tests/test_readout.py` と、修正元の `tests/test_audit.py` を確認。

## 安全装置と Phase 境界

- 今回の変更は **確認済み HEAD の集合に1件追加するだけ**。任意の将来 HEAD、未知のブランチ、ピン留めしたソース blob の改変、追跡済みソースのステージ・作業ツリー変更は従来どおり拒否。
- `GIVEN`、ProofStep、DB Goal、ProofSearch の本体、出典を一切変更しない。
- DryRun は読み取りのみ。本実行は `%LOCALAPPDATA%` 配下に監査レポート JSON を出力する。Git や本体ファイルは変更せず、コミットやファイル整理も実施しない。
- Phase 173 の全体 pytest は Phase 終了時まで実行しない。
- 対象群は $\pi_7^4$ のみ。$\pi_8^5$ は次の Phase 下位段階まで対象外。

## 完了条件

DryRun が `PHASE173_R4_R1_TYPED_PREMISE_DRY_RUN=PASS`、本実行が `PHASE173_R4_R1_TYPED_PREMISE_AUDIT=PASS` を記録し、`audit.json` に `PI77_COMPLETE`、既存 Rule Factory、通常/仮定的 Root 候補の結果を記録する。数学的な完成証明を自動的に認定しない。
