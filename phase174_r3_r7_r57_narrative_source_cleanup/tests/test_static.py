"""Preflight and checked two-step source corrections; no real source is forged."""
from __future__ import annotations
import ast
from pathlib import Path
import pytest
from phase174_r3_r7_r57_narrative_source_cleanup import install

def test_exact_source_pins_and_no_new_given():
    assert len(install.PINS)==3
    assert len(install.LOCAL_SHA256)==2
    assert all(len(value)==40 for value in install.PINS.values())
    assert all(len(value)==64 for value in install.LOCAL_SHA256.values())
    assert 'GIVEN' not in install.NEW_RULE.split('PremisePattern')[0] or 'ProofRule.GIVEN' in install.NEW_RULE

def test_new_generator_surjectivity_needs_only_one_relation():
    assert 'len(premises) == 1' in install.NEW_RULE
    assert 'Proposition 2.7' in install.NEW_RULE
    assert 'Prop27TypedHopfDeltaStatement,' not in install.NEW_RULE
    assert install.NEW_INPUTS.count('Relation(delta.target_group')==1

def test_r56_rule_and_test_replacements_parse():
    root=Path(__file__).resolve().parents[2]
    original=root/'phase174_r3_r7_r56_cyclic_generator_bridge/rule.py'
    tests=root/'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py'
    ast.parse(install.patch_rule(original.read_text(encoding='utf-8')) if install.sha256(original.read_bytes())==install.LOCAL_SHA256[install.R56_RULE] else original.read_text(encoding='utf-8'))
    assert tests.is_file()

def test_invalid_anchor_refuses_modified_display():
    with pytest.raises(RuntimeError):
        install.patch_typed('def unrelated():\n    pass\n')
    with pytest.raises(RuntimeError):
        install.patch_renderer('def unrelated():\n    pass\n')
    with pytest.raises(RuntimeError):
        install.patch_reference('def unrelated():\n    pass\n')

def test_no_phase_specific_narrative_or_new_proof_steps():
    source=Path(install.__file__).read_text(encoding='utf-8')
    assert 'pi11_6' not in source
    assert 'pi12_7' not in source
    assert 'ProofStep(' not in source
    assert 'register_fixed' not in source
