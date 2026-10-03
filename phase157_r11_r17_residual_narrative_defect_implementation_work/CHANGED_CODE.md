# Phase157 R11-R17 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

import 変更なし。

変更関数全体:
- `normalize_toda_group_proof_narrative_connectors()`
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`
  - pipeline 呼び出し部分に R11-R17 finalization を追加。

新規関数:
- `insert_toda_group_proof_narrative_hidden_zero_map_premises()`
- `trim_toda_group_proof_narrative_redundant_left_ehp_terms()`
- `normalize_toda_group_proof_narrative_repeated_numeric_equalities()`
- `link_toda_group_proof_narrative_unmarked_reference_consumers()`

新規関数の追加位置:
- `normalize_toda_group_proof_narrative_display_math_periods()` の直前。

### `tests/test_phase157_r11_r17_residual_narrative_defects.py`

新規ファイル。
import 全文:
```python
import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
```

## 実行 pytest

focused pytest のみ。
全体 pytest は Phase157 closure まで実行しない。

## 完了条件

- hidden zero-map statement が consumer/use より前に見える。
- pi6^3 の最初の Delta-E 列は保持し、後続の冗長左項だけ省略。
- 6代表群 standalone connector 0。
- `=N=N` 重複なし。
- 公開 Reference は本文 marker を持つ。
- ancestry-only Reference は公開されない。
- needed Reference は保持される。
- R11-R14 / Phase156 focused regressions を維持。

## 次 Phase との境界

R11-R17 は residual defect implementation のみ。
112-group re-audit は次 substep。
docs / full repository pytest は Phase157 closure まで行わない。
