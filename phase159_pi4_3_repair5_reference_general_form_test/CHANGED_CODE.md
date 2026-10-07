# Phase 159 pi4^3 repair5

## 変更対象

- `tests/test_phase159_pi4_3_repair2g_reference_policy.py`
  - `test_phase159_repair2g_pi4_public_reference_policy_is_51_then_prop51`

production code の変更はありません。
import の変更もありません。

## 修正理由

現行 public Reference の `(5.1)` は一般形

$$
\pi_i^n = 0 \quad (i<n),
$$

$$
\pi_n^n = \mathbb{Z}\{\iota_n\}
$$

を表示する契約になっている。

旧テストは Reference に

$$
\pi_5^5=\mathbb{Z}\{\iota_5\},
\qquad
\pi_4^5=0
$$

という個別 specialization を要求していたため stale expectation となっていた。

## 変更後のテスト関数全文

```python
def test_phase159_repair2g_pi4_public_reference_policy_is_51_then_prop51():
  _, _, rendered = _group_data(
    3,
    1,
  )
  reference = _reference_section(
    rendered
  )

  assert "**[R1] (5.1).**" in reference
  assert (
    "**[R2] Proposition 5.1.**"
    in reference
  )

  assert (
    r"\pi_{i}^{n} = 0\ (i < n)"
    in reference
  )
  assert (
    r"\pi_{n}^{n} = "
    r"\mathbb{Z}\{\iota_{n}\}"
    in reference
  )

  assert (
    r"\pi_{5}^{5}"
    not in reference
  )
  assert (
    r"\pi_{4}^{5} = 0"
    not in reference
  )

  assert (
    r"\pi_{3}^{2}"
    in reference
  )
  assert (
    r"\mathbb{Z}\{\eta_{2}\}"
    in reference
  )
  assert (
    r"\Delta"
    in reference
  )
  assert (
    r"\iota_{5}"
    in reference
  )
  assert (
    r"2\eta_{2}"
    in reference
  )

  assert "Proposition 4.2" not in reference
  assert r"\xrightarrow" not in reference

```

## Phase 境界

- production renderer は変更しない。
- `pi_4^3` の証明本文は変更しない。
- `pi_(n+1)^n`, `n>=4` stable transport も変更しない。
- Reference は一般形、proof body は specialization という現在の方針を維持する。
- 全体テストは Phase 最後まで実行しない。
