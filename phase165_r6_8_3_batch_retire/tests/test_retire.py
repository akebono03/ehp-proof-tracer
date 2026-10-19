from pathlib import Path
from tempfile import TemporaryDirectory
from phase165_r6_8_3_batch_retire.retire import consumers, plan

def test_imported_probe_is_not_retired():
    with TemporaryDirectory() as folder:
        root=Path(folder)
        (root/'probes').mkdir()
        (root/'tests').mkdir()
        (root/'probes/probe_phase53_capabilities.py').write_text('x=1\n',encoding='utf-8')
        (root/'tests/test_keep.py').write_text('from probes.probe_phase53_capabilities import x\n',encoding='utf-8')
        assert 'probes/probe_phase53_capabilities.py' not in plan(root)['retirable']

def test_orphaned_probe_is_retirable():
    with TemporaryDirectory() as folder:
        root=Path(folder)
        (root/'probes').mkdir()
        (root/'probes/probe_phase53_capabilities.py').write_text('x=1\n',encoding='utf-8')
        assert 'probes/probe_phase53_capabilities.py' in plan(root)['retirable']

def test_parse_error_blocks_all_removal():
    with TemporaryDirectory() as folder:
        root=Path(folder)
        (root/'probes').mkdir()
        (root/'probes/probe_phase53_capabilities.py').write_text('x=1\n',encoding='utf-8')
        (root/'broken.py').write_text('def broken(\n',encoding='utf-8')
        assert not plan(root)['retirable']
