# Phase157 R11-R11 repair5

## 変更対象

### toda_group_proof_narrative_contribution_renderer.py

変更 import:
```python
from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)
```

変更関数:
- `_phase157_r5_r7_order_and_connect_fixed_definition_reference_lines()`
- `order_toda_group_proof_narrative_surjectivity_support()`
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`
  - 上記 ordering 呼び出しに `presentation` を渡す。

Reference formatting:
- definition statement: `とすると,`
- その他の独立 statement: `.`

Map-property ordering:
- direct equality premise と、その1段の equality premises を proof graph から取得。
- visible paragraph block を map-property の直前へ移動。
- 既存 target-group-before-surjectivity ordering は維持。

### tests/test_phase157_r11_reference_reason_punctuation.py

追加:
- Reference non-definition statements の period 終止。

## 完了条件

- `(5.3)` の double relation が `.` で Reference に表示。
- tag(4), tag(5), tag(6) が H-surjectivity より前。
- pi_6^5 group も H-surjectivity より前。
- focused pytest pass。
- full repository pytest はまだ実行しない。
