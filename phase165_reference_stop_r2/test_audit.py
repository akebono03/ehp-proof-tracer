from dataclasses import dataclass
from audit import matches_step, graph_report

@dataclass(frozen=True)
class DummyStep:
    conclusion: object
    rule: object = None
    premises: tuple = ()

@dataclass(frozen=True)
class DummyResult:
    proven_steps: tuple
    conclusion: object

def test_matching_requires_type_and_equality():
    assert matches_step(DummyStep("x"), "x")
    assert not matches_step(DummyStep(1), True)

def test_graph_report_empty_prior():
    root = DummyStep("result")
    report = graph_report(DummyResult((root,), "result"), "prior")
    assert report["pi32_steps_in_result"] == 0
    assert report["generator_suspension_steps_in_result"] == 0
