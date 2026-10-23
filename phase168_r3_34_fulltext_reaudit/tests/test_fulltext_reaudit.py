from pathlib import Path
import importlib.util

path=Path(__file__).resolve().parents[1]/'audit.py'
spec=importlib.util.spec_from_file_location('r3_34_audit',path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_all_three_reference_and_proof_sections_are_compared():
    report=module.generate()
    assert len(report['results']) == 3
    for group in report['results'].values():
        assert group['comparison']['reference']['identical_normalized'] is False
        assert group['comparison']['proof']['identical_normalized'] is False


def test_pi54_reports_missing_toda45_proof_application():
    report=module.generate()
    findings=report['results']['pi_5^4']['findings']
    assert any('(n,m,k)=(3,4,1)' in f['description'] for f in findings)
    assert any('証明本文に [R3] が現れない' in f['description'] for f in findings)
