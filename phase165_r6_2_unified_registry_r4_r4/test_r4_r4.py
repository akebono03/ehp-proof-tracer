from dataclasses import dataclass

import pytest

from r4_r4_patch import replace_function


SOURCE = """from proof import (
  InferenceRule,
  PremisePattern,
)

def isomorphism_implies_injective_inference_rule():
  def build_conclusion(premises):
    return premises[0].conclusion
  return InferenceRule(name='x', conclusion_builder=build_conclusion)
"""


def test_patch_adds_typed_patterns():
    result = replace_function(SOURCE)
    assert "conclusion_pattern=InjectiveMapStatement(" in result
    assert "statement_pattern=IsomorphismStatement(" in result
    assert "PatternVariable," in result


def test_patch_preserves_forward_builder():
    result = replace_function(SOURCE)
    assert "def build_conclusion(" in result
    assert "conclusion_builder=(" in result


def test_idempotent():
    patched = replace_function(SOURCE)
    assert replace_function(patched) == patched


def test_missing_function_rejected():
    with pytest.raises(ValueError):
        replace_function("x = 1\n")


def test_duplicate_function_rejected():
    with pytest.raises(ValueError):
        replace_function(SOURCE + SOURCE)


def test_legacy_adapter_guard():
    with pytest.raises(ValueError):
        replace_function(SOURCE + "from phase165_r52_r23_existing_rule_adapter import x\n")
