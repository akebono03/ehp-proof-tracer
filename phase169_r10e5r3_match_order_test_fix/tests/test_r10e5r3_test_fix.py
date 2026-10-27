"""R10E5-R3 guarded repair does not change the matcher or other tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase169_r10e5r3_match_order_test_fix.patch_test import (
    OLD_TEST,
    NEW_TEST,
    TARGET,
    TEST_NAME,
    transform,
    _extract_test,
)


def test_r10e5r3_exactly_one_test_is_replaced() -> None:
    before = (Path(__file__).resolve().parents[1] / "output" /
              "test_r10e5_composite_generator_image.py.before").read_bytes()
    updated, function = transform(before)
    assert updated == TARGET.read_bytes()
    assert function == NEW_TEST
    assert "assert reversed_matches[0].premises == steps" in function
    assert "assert find_inference_matches_for_rule(rule, steps[:1]) == ()" in function
    assert "replace(steps[0], rule=ProofRule.GIVEN)" in function
    with pytest.raises(RuntimeError, match="already applied"):
        transform(updated)


def test_r10e5r3_reversed_matching_uses_typed_premise_order() -> None:
    current, _, _ = _extract_test(TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n"))
    assert current == NEW_TEST
    assert NEW_TEST != OLD_TEST
    assert TEST_NAME in current
