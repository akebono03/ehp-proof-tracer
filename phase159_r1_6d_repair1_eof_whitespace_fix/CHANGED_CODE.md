# Phase 159-R1-6d repair1

## 変更対象

- `tests/test_phase159_r1_6c_source_faithful_reference_linkage.py`
  - EOF の余分な空行のみ削除

Production code:
- 変更なし

import:
- 変更なし

test function:
- ロジック変更なし

## 修正理由

R1-6d の検証結果:

- R1-6d focused: 4 passed
- R1-6a/R1-6b/R1-6c: 9 passed
- Phase159 focused: 9 passed
- related regressions: 55 passed

失敗は `git diff --check` のみ。

```text
tests/test_phase159_r1_6c_source_faithful_reference_linkage.py:176:
new blank line at EOF.
```

そのためファイル末尾を

```text
exactly one newline
```

へ正規化するだけ。

## 実行する pytest

- R1-6d focused
- R1-6a/R1-6b/R1-6c
- Phase159 focused
- related regressions

その後 `git diff --check`。

## 完了条件

- 上記テスト PASS
- `git diff --check` PASS
- production diff 追加なし
- full pytest 未実行

## 次 Phase との境界

R1-6d の表示ロジックには触れない。
今回の repair は whitespace cleanup のみ。
