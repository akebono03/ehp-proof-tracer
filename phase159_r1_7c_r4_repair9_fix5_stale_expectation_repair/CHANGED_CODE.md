# 変更対象

## Production

変更なし。

## Test

`tests/test_phase157_r20_repair30_final_reflexive_suppression.py`

### import 部分

変更なし。現在の import 全文:

```python
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

### 変更後テスト関数全文

```python
def test_phase157_r20_repair30_eta_bridge_and_hopf_support_remain():
  rendered = _render_pi6_3_repair30()
  body = rendered.split(
    "---",
    1,
  )[1]

  required = (
    r"$\eta_{6}=E\eta_{5}$.",
    r"$H\left(\nu'\right) = \eta_{5}",
    r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}",
  )

  for text in required:
    assert text in body

  assert (
    r"$2\nu' = \eta_{3}^{3}"
    in body
    or (
      r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}"
      r" = \eta_{3}^{3}$"
      in body
    )
  )
```

## 実行 pytest

- `tests/test_phase157_r20_repair30_final_reflexive_suppression.py`
- `tests/test_phase158_r5_5b_public_generic_order_route.py`
- `tests/test_phase157_r20_repair12_map_property_reference_support.py`
- `phase159_r1_7c_r4_repair9_fix5_stale_expectation_repair/test_phase159_r1_7c_r4_repair9_fix5.py`

repository-wide pytest は実行しない。
