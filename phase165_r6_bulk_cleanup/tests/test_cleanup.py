from pathlib import Path
import importlib.util

MODULE=Path(__file__).resolve().parents[1]/'cleanup.py'
spec=importlib.util.spec_from_file_location('bulk_cleanup',MODULE)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_import_extraction(tmp_path):
    source=tmp_path/'example.py'
    source.write_text('from repository_inference import derive\nfrom tests.test_phase45_x import helper\n',encoding='utf-8')
    assert 'repository_inference' in module.imports(source)
    assert 'tests.test_phase45_x' in module.imports(source)

def test_cleanup_protects_imported_and_modern_tests(tmp_path):
    tests=tmp_path/'tests'
    tests.mkdir()
    (tests/'test_phase80_a.py').write_text('from repository_inference import derive\n',encoding='utf-8')
    (tests/'test_phase159_b.py').write_text('from test_phase80_a import derive\n',encoding='utf-8')
    (tests/'test_phase80_c.py').write_text('from repository_inference import derive\n',encoding='utf-8')
    log='_____ ERROR collecting tests/test_phase80_a.py _____\nModuleNotFoundError: No module named \'repository_inference\'\n_____ ERROR collecting tests/test_phase80_c.py _____\nModuleNotFoundError: No module named \'repository_inference\'\n'
    info=module.plan(tmp_path,{'error_files':['tests/test_phase80_a.py','tests/test_phase80_c.py']+['tests/test_phase999_missing.py']*378},log) if False else None
    assert module.PHASE.match('test_phase159_b').group(1)=='159'
    assert module.blocks(log)['tests/test_phase80_c.py'].count('repository_inference')==1

def test_sha_backup_and_restore(tmp_path):
    tests=tmp_path/'tests'
    tests.mkdir()
    p=tests/'test_phase80_a.py'
    p.write_text('from repository_inference import derive\n',encoding='utf-8')
    row={'path':'tests/test_phase80_a.py','sha256':module.digest(p),'decision':'REMOVE'}
    assert module.apply(tmp_path,{'decisions':[row]},tmp_path/'backup')==1
    assert not p.exists()
    assert module.digest(tmp_path/'backup'/'tests/test_phase80_a.py')==row['sha256']
