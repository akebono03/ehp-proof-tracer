# Phase 159 R1-7c R3 repair3

## 変更対象

- `phase159_r1_7c_r3_known_result_direct_premise_specialization/audit_phase159_r1_7c_r3.py`
- production code の変更なし。
- test code の変更なし。

## 変更後 import 部分全文

```python
from pathlib import Path
import sys


REPOSITORY_ROOT = (
  Path(__file__).resolve().parents[1]
)

if str(
  REPOSITORY_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )


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

## audit main function

`main()` 自体の変更はない。
