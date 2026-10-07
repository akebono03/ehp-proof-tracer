# Phase 159 R1-7c R3 repair1

## 変更対象

- `tests/test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py`
- Production file の変更なし。

## 変更する test function 全文

```python
def test_phase159_r1_7c_r3_pi11_4_renders_i11_decomposition_specialization():
  body = (
    _phase159_r1_7c_r3_proof_body(
      _phase159_r1_7c_r3_render(
        4,
        7,
      )
    )
  )
  specialized = (
    r"\pi_{10}^{3} \oplus "
    r"\pi_{11}^{7} "
    r"\xrightarrow{\cong} "
    r"\pi_{11}^{4}"
  )

  assert specialized in body
  assert (
    r"$\nu_{4}$ の分解写像は同型写像である."
    not in body
  )
  assert (
    r"\pi_{11}^{4} = 0"
    in body
  )
  assert body.rstrip().endswith(
    "□"
  )
```

必要 import の変更はない。
