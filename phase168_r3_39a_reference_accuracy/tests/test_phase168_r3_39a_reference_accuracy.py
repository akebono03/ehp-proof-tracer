from dataclasses import dataclass

from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
from phase168_r3_37c_reference_projection import project_reference_bodies


@dataclass(frozen=True)
class _Assertion:
    content: object


class _Registry:
    def __init__(self, contents):
        self.contents = contents

    def assertion(self, identifier):
        return _Assertion(self.contents[identifier])


def test_reference_prop42_uses_all_five_verified_adopted_tex_terms():
    registry = _Registry({"prop42": TodaProp42GeneralExactnessStatement()})
    bodies = project_reference_bodies(registry, ("prop42",))
    assert len(bodies) == 1
    assert (r"\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}"
            r"\xrightarrow{H}\pi_{i+1}^{2n+1}"
            r"\xrightarrow{\Delta}\pi_{i-1}^{n}"
            r"\xrightarrow{E}\pi_i^{n+1}") in bodies[0]


def test_reference_toda51_general_zero_only_when_assertion_used():
    registry = _Registry({"toda51": Toda51BelowDiagonalZeroStatement(),
                          "prop42": TodaProp42GeneralExactnessStatement()})
    assert project_reference_bodies(registry, ("toda51",)) == (
        r"$\pi_i^n=0\quad(i<n)$.",
    )
    assert all(r"\pi_i^n=0" not in body
               for body in project_reference_bodies(registry, ("prop42",)))


def test_reference_projection_does_not_include_unused_general_assertions():
    registry = _Registry({"prop42": TodaProp42GeneralExactnessStatement(),
                          "toda51": Toda51BelowDiagonalZeroStatement()})
    assert project_reference_bodies(registry, ()) == ()
    assert project_reference_bodies(None, ("prop42",)) == ()
