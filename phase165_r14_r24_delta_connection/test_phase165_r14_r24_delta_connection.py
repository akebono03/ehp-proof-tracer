from pathlib import Path
import pytest

from homotopy_groups import (
    TodaEHPExactnessWindow, TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from phase165_r14_r11_delta_zero import expand_delta_zero_from_suspension_iso
from phase165_r14_r24_delta_connection import (
    pi32_delta_goal, derive_delta_zero_from_steps, reviewed_r23_isomorphism,
)
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement

TEX = Path(__file__).with_name('toda_51_complete.tex')


def _parts():
    iso, _ = reviewed_r23_isomorphism(TEX)
    exactness = expand_delta_zero_from_suspension_iso(pi32_delta_goal())[0].subgoals[1]
    return iso, ProofStep(exactness, (), ProofRule.GIVEN)


def test_r23_real_inference_step_is_reused():
    iso, _ = _parts()
    assert iso.rule is ProofRule.INFERENCE
    assert iso.conclusion == expand_delta_zero_from_suspension_iso(pi32_delta_goal())[0].subgoals[0]


def test_exactness_fixture_completes_delta_inference():
    iso, fixture = _parts()
    step = derive_delta_zero_from_steps(iso, fixture)
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == pi32_delta_goal()
    assert len(step.premises) == 2


def test_missing_exactness_is_rejected():
    iso, fixture = _parts()
    with pytest.raises(TypeError):
        derive_delta_zero_from_steps(iso, None)


def test_untyped_exactness_rejected():
    iso, fixture = _parts()
    with pytest.raises(ValueError):
        derive_delta_zero_from_steps(iso, ProofStep('exactness', (), ProofRule.GIVEN))


def test_wrong_exactness_window_rejected():
    iso, fixture = _parts()
    old = fixture.conclusion.window
    invalid = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        old.source_term, old.middle_term, old.target_term, EHP_E_MAP, EHP_DELTA_MAP))
    with pytest.raises(ValueError):
        derive_delta_zero_from_steps(iso, ProofStep(invalid, (), ProofRule.GIVEN))


def test_wrong_suspension_rejected():
    iso, fixture = _parts()
    bad = TodaSuspensionIsomorphismStatement(TodaSuspensionMap(
        TodaPrimaryGroup(2, 2), TodaPrimaryGroup(3, 3)))
    with pytest.raises(ValueError):
        derive_delta_zero_from_steps(ProofStep(bad, (), ProofRule.GIVEN), fixture)
