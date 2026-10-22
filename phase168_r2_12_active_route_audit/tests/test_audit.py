import importlib.util
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'audit.py'
spec = importlib.util.spec_from_file_location('phase168_r2_12_audit', PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_safe_repr():
    assert mod.safe(42) == '42'


def test_step_record_minimal():
    class Step:
        rule = 'GIVEN'
        conclusion = 7
        inference_rule = None
        premises = ()
    record = mod.step_record(Step())
    assert record['reference'] is None
    assert record['premise_ids'] == []
    assert record['conclusion'] == '7'
