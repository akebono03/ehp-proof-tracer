# Phase 158-R3

## 目的

`## 使用する結果` の直後にある

`使用する結果を先にまとめる.`

を削除し、Reference section を `[R1]` から直接開始する形へ統一する。

## 変更対象

### Production

`toda_group_proof_narrative_references.py`

変更関数:

`render_toda_group_proof_narrative_reference_entries_markdown()`

import 変更なし。

変更は

`lines = ["使用する結果を先にまとめる.", ""]`

を

`lines = []`

へ置き換えるだけであり、Reference entry、statement、番号、帰属は変更しない。

### Tests

Phase 158-R3 専用 focused test を追加する。

確認対象:

- lower-level Reference renderer が `[R1]` から始まる
- pi6_3 に intro 文がない
- pi15_8 に intro 文がない
- pi15_8 の Reference 内容を維持
- Phase 158 public contract と terminal `□` を維持

## 112群 audit

depth=2 の 112群すべてについて:

- `使用する結果を先にまとめる.` が存在しない
- Reference body がある場合、最初の非空行は `**[R1] ...**`

を確認する。

## 既知の stale tests

過去 Phase の一部テストは intro 文の存在を固定している。
これは今回の仕様変更で stale になるため、Phase 158-R3 の実装確認後に test-only repair として更新する。

## Phase 境界

数学内容、Reference attribution、proof body、Reference numbering は変更しない。
全体 pytest は Phase 158 の最後のみ。
