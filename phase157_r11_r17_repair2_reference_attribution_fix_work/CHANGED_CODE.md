# Phase157 R11-R17 repair2 changed code

## Production

### `toda_group_proof_narrative_contribution_renderer.py`

import 変更なし。

変更関数全体:
- `link_toda_group_proof_narrative_unmarked_reference_consumers()`

一般規則:
- consumer が `presentation.root_step` なら root candidate。
- non-root consumer が literature Reference を持つ場合は ancestry として除外。
- Reference 所有なしの visible non-root consumer を優先。
- それが無ければ unique visible root consumer を採用。
- ambiguous な場合は marker を付けない。

pipeline 変更:
- `_phase157_r3_restore_pi6_3_earlier_prop56_reference()` 後に
  `filter_toda_group_proof_narrative_reference_entries_by_body_usage()`
  を再実行。
- marker の無い ancestry-only restored Reference を最終公開 Reference から除外。

## Tests

テストファイル変更なし。
既存の R11-R17 focused tests および関連 regression tests を実行。

## 完了条件

- public Reference header の各 [R#] が body に存在。
- pi6 Proposition 5.3 非表示。
- pi12 (5.5) 非表示。
- pi16 Lemma 5.13 非表示。
- pi10 Lemma 5.4 保持＋marker。
- pi12 Lemma 5.13 保持＋marker。
- pi16 Lemma 5.14 保持＋marker。
- focused pytest pass。

## 次 Phase 境界

repair2 完了後に 112-group R11-R18 re-audit。
full pytest / docs は Phase157 closure まで実行しない。
