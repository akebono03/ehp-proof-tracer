from phase167_r4_6_contribution_identity_audit.audit import describe_step


class _Rule:
    name = "example"


class _Step:
    conclusion = "value"
    rule = "given"
    inference_rule = _Rule()
    premises = ()


def test_describe_step_records_typed_provenance():
    result = describe_step(_Step())
    assert result["conclusion_type"] == "str"
    assert result["inference_rule"] == "example"
    assert result["premises"] == []


def test_describe_step_without_inference_rule():
    step = _Step()
    step.inference_rule = None
    result = describe_step(step)
    assert result["inference_rule"] is None
