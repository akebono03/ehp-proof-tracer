from phase168_r2_8_6_reference_trace.audit import describe_entries, describe_step
from proof import ProofStep


def test_describe_entries_empty():
    assert describe_entries(()) == []


def test_describe_step_requires_proof_step():
    try:
        describe_step(None)
    except (AttributeError, TypeError):
        pass
    else:
        raise AssertionError("An invalid step must not be interpreted as a proof")


def test_proofstep_class_is_available():
    assert ProofStep.__name__ == "ProofStep"
