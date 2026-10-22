import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / 'audit.py'
spec = importlib.util.spec_from_file_location('phase168_r2_11_audit', MODULE_PATH)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class FakeReference:
    def __init__(self, locator):
        self.locator = locator
        self.label = 'Toda ' + locator


class FakeEntry:
    def __init__(self, number, locator):
        self.number = number
        self.reference = FakeReference(locator)
        self.proof_steps = ()


def test_entry_records_preserves_reference_identity():
    result = audit.entry_records((FakeEntry(1, 'Proposition 5.1'), FakeEntry(2, '(5.2)')))
    assert [x['locator'] for x in result] == ['Proposition 5.1', '(5.2)']
    assert [x['number'] for x in result] == [1, 2]


def test_stage_output_extraction_keeps_empty_reference_set():
    assert audit.entries_from_result('exclude_toda_group_proof_narrative_root_reference', ((), {})) == []
    assert audit.entries_from_result('render_toda_group_proof_narrative_reference_entries_markdown', 'text') is None
