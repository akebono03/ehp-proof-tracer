from pathlib import Path
from tempfile import TemporaryDirectory
from phase165_r6_legacy_batch.cleanup import apply, plan


def test_direct_missing_legacy_module_can_be_retired():
    with TemporaryDirectory() as d:
        root = Path(d)
        t = root / 'tests'
        t.mkdir()
        (t / 'test_phase80_one.py').write_text('from repository_inference import old_api\n', encoding='utf-8')
        report = plan(root, {'records': [{'test_path': 'tests/test_phase80_one.py', 'detail': "No module named 'repository_inference'"}]})
        assert report['decisions'][0]['decision'] == 'REMOVE'
        apply(root, report, root / 'backup')
        assert not (t / 'test_phase80_one.py').exists()
        assert (root / 'backup/tests/test_phase80_one.py').exists()


def test_imported_test_is_preserved():
    with TemporaryDirectory() as d:
        root = Path(d)
        t = root / 'tests'
        t.mkdir()
        (t / 'test_phase80_one.py').write_text('from repository_inference import old_api\n', encoding='utf-8')
        (t / 'test_phase80_two.py').write_text('from test_phase80_one import something\n', encoding='utf-8')
        report = plan(root, {'records': [{'test_path': 'tests/test_phase80_one.py', 'detail': "No module named 'repository_inference'"}]})
        assert report['decisions'][0]['decision'] == 'KEEP'


def test_modern_tests_are_protected():
    with TemporaryDirectory() as d:
        root = Path(d)
        t = root / 'tests'
        t.mkdir()
        (t / 'test_phase162_one.py').write_text('from repository_inference import old_api\n', encoding='utf-8')
        report = plan(root, {'records': [{'test_path': 'tests/test_phase162_one.py', 'detail': "No module named 'repository_inference'"}]})
        assert report['decisions'] == []
