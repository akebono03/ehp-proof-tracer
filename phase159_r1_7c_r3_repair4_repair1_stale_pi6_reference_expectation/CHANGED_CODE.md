# Phase 159 R1-7c R3 repair4 repair1

## 変更対象

- `tests/test_phase157_r5_r6_53_bracket_definition_reference.py`
- production code の変更なし。

## 変更後 import 部分全文

```python
import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_components,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)
```

## 変更 test function 全文

```python
def test_phase157_r5_r6_pi6_reference_53_displays_bracket_definition():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi6_3_presentation()
    )
  )
  reference_part = (
    rendered.split(
      "---\n\n## 証明",
      1,
    )[
      0
    ]
  )

  assert (
    re.search(
      r"\*\*\[R\d+\] Equation 5\.3\.\*\*",
      reference_part,
    )
    is not None
  )
  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in reference_part
    or
    r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"
    in reference_part
  )
```

## Phase boundary

- Reference production rendering は変更しない。
- repair4 component pruning logic は変更しない。
- pi6_3 special case を追加しない。
- stale expectation のみ current public contract に合わせる。
