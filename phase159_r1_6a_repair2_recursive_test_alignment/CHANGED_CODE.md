# Phase 159-R1-6a repair2

## 変更対象

- `tests/test_phase159_r1_6a_foundational_reference_identity.py`
  - `test_phase159_r1_6a_pi3_2_foundational_premises_keep_identity()`

Production code:
- 変更なし

import:
- 変更なし

## 変更後テスト関数全体

```python
def test_phase159_r1_6a_pi3_2_foundational_premises_keep_identity():
  presentation = (
    _phase159_r1_6a_pi3_2_presentation()
  )

  expected = {
    pi_2_1_zero_fact():
      "sphere.circle.higher_zero",
    pi_3_3_free_cyclic_fact():
      "sphere.identity_group",
    e_pi_1_1_to_pi_2_2_isomorphism_fact():
      (
        "sphere.low_dimensional."
        "suspension_isomorphism"
      ),
  }

  found = {}
  seen_step_ids = set()

  def visit(
    proof_step,
  ):
    step_id = id(
      proof_step
    )

    if step_id in seen_step_ids:
      return

    seen_step_ids.add(
      step_id
    )

    if proof_step.conclusion in expected:
      identity = (
        proof_step.foundational_reference
      )

      assert identity is not None

      found[
        proof_step.conclusion
      ] = identity.key

    for premise in proof_step.premises:
      if hasattr(
        premise,
        "conclusion",
      ):
        visit(
          premise
        )

  visit(
    presentation.root_step
  )

  assert found == expected
```

## 修正理由

R1-6a repair1 で production の foundational collector は
`presentation.nodes` ではなく `presentation.root_step` から
`ProofStep.premises` を recursive traversal する仕様になった。

一方、focused test は旧仕様の `presentation.nodes` だけを観測していたため、
proof depth=2 より深い

- `pi_2^1 = 0`
- `E: pi_1^1 -> pi_2^2` isomorphism

を見つけられなかった。

## 完了条件

- R1-6a focused tests 4件 PASS。
- Phase 159 focused tests PASS。
- Phase 49 / Phase 157 related tests PASS。
- `git diff --check` PASS。
- public Narrative の `使用する結果` に3 foundational facts が表示される。
- target と Proposition 5.1 が foundational Reference に入らない。

## 次 Phase との境界

- production logic の追加変更なし。
- proof body の `[F1] より` linkage はまだ未実装。
- full pytest は Phase 159 最後のみ。
