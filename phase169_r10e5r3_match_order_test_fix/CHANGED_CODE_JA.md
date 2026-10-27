# 変更対象の全体表示

変更ファイル：`phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py`

変更関数：`test_r10e5_two_inferred_images_are_required_to_prove_composition` のみ。

import の変更なし。既存の `from dataclasses import replace` と `from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule` をそのまま利用する。

## 変更後のテスト関数全文

```python
def test_r10e5_two_inferred_images_are_required_to_prove_composition():
    goal = _image(8, 6, _square(8), _square(9))
    obligations = component_image_obligations(goal)
    assert obligations is not None
    rule = composite_generator_image_rule(goal)
    steps = tuple(ProofStep(item, (), ProofRule.INFERENCE)
                  for item in obligations)
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    assert matches[0].premises == steps
    assert apply_inference_match(matches[0]).conclusion == goal
    assert find_inference_matches_for_rule(rule, steps[:1]) == ()
    assert find_inference_matches_for_rule(
        rule, (replace(steps[0], rule=ProofRule.GIVEN), steps[1]),
    ) == ()
    # The inference matcher accepts premises in arbitrary input order and
    # returns them in their typed premise-pattern order.
    reversed_matches = find_inference_matches_for_rule(rule, tuple(reversed(steps)))
    assert len(reversed_matches) == 1
    assert reversed_matches[0].premises == steps
    assert apply_inference_match(reversed_matches[0]).conclusion == goal
```

## 限定テスト・完了条件

実行：`powershell -ExecutionPolicy Bypass -File .\phase169_r10e5r3_match_order_test_fix\run.ps1`。

`R10E5_INTEGRITY_RESULT=PASS`、`R10E5_LIMITED_TESTS_AND_AUDIT=PASS`、`R10E5R3_INTEGRITY_RESULT=PASS` を完了条件とする。R10E5 の数学的な一般化のみを対象とし、未対応生成元の追加規則は次 Phase 以降の範囲とする。
