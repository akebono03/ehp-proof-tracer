from pathlib import Path
import importlib.util

SCRIPT = Path(__file__).with_name('audit.py')
spec = importlib.util.spec_from_file_location('phase166_r2_generator_audit', SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_parse_ids():
    assert module.parse_ids('2 2 2') == (2, 2, 2)
    assert module.parse_ids('') == ()
    assert module.parse_ids('bad') is None


def test_existing_ids_are_only_candidates():
    gens = [{'id':'2', 'display':'η', 'n':'2', 'k':'1'}]
    sphere = [{'n':'3','k':'1','id':'0','generator':'η3','Element':'2'}]
    summary, rows = module.inspect(gens, sphere)
    assert rows[0]['status'] == 'GENERATOR_IDS_RESOLVED_NOT_CERTIFIED'
    assert summary['proof_permission_granted'] == 0
    assert not rows[0]['mathematical_identity_confirmed']


def test_unknown_id_fails_closed():
    summary, rows = module.inspect([{'id':'2','display':'η'}], [{'Element':'99'}])
    assert rows[0]['status'] == 'UNKNOWN_GENERATOR_ID'
    assert summary['mathematical_identity_confirmed'] == 0


def test_duplicate_id_fails_closed():
    gens = [{'id':'2','display':'η'},{'id':'2','display':'η_alt'}]
    _, rows = module.inspect(gens,[{'Element':'2'}])
    assert rows[0]['status'] == 'DUPLICATE_GENERATOR_ID'
