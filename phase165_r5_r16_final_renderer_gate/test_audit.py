from pathlib import Path

from audit import audit


def _fixture(tmp_path: Path, legacy: bool = True) -> Path:
    files = {
        'phase162_ehp_leaf_inputs.py': 'def _phase162_ehp_leaves():\n    return ()\n',
        'phase162_pi5_3_web_replay.py': 'from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n',
        'phase162_web_narrative_integration.py': 'from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n',
        'phase162_r3_narrative_connection.py': '',
        'toda_group_proof_narrative_proof_chain_renderer.py': '',
        'toda_group_proof_narrative_concrete_transport.py': '',
        'web_group_proof.py': 'def build_web_partial_group_proof_view():\n    return render_partial_proof_markdown\n',
        'cli.py': 'render_partial_proof_markdown = object()\n',
        'main.py': 'render_partial_proof_markdown = object()\n',
    }
    if legacy:
        files['phase162_web_narrative_integration.py'] += 'def build_phase162_web_validated_isomorphism_markdown():\n    return "old"\n'
    for path, content in files.items():
        (tmp_path / path).write_text(content, encoding='utf-8')
    return tmp_path


def test_present_old_renderer_must_not_claim_retired(tmp_path):
    result = audit(_fixture(tmp_path))
    assert result['status'] == 'PUBLIC_PATH_UNIFIED_LEGACY_REMAINS'
    assert result['legacy_definitions_present'] == 1


def test_no_old_renderer_only_static_candidate(tmp_path):
    result = audit(_fixture(tmp_path, legacy=False))
    assert result['status'] == 'STATIC_RETIREMENT_CANDIDATE_NEEDS_RUNTIME_VERIFICATION'


def test_missing_shared_leaf_is_precondition_failure(tmp_path):
    root = _fixture(tmp_path)
    (root / 'phase162_ehp_leaf_inputs.py').unlink()
    assert audit(root)['status'] == 'PRECONDITION_FAILED'


def test_missing_compat_reexport_is_precondition_failure(tmp_path):
    root = _fixture(tmp_path)
    (root / 'phase162_web_narrative_integration.py').write_text('def build_phase162_web_validated_isomorphism_markdown():\n    pass\n', encoding='utf-8')
    assert audit(root)['status'] == 'PRECONDITION_FAILED'


def test_no_false_positive_for_nonexistent_symbols(tmp_path):
    result = audit(_fixture(tmp_path))
    assert result['legacy_symbols']['phase162_r3_narrative_connection.py:render_phase162_r3_narrative'] == 'ABSENT'


def test_direct_test_import_is_recorded(tmp_path):
    root = _fixture(tmp_path)
    tests = root / 'tests'
    tests.mkdir()
    (tests / 'test_old.py').write_text('from phase162_web_narrative_integration import build_phase162_web_validated_isomorphism_markdown\n', encoding='utf-8')
    result = audit(root)
    assert result['direct_imports']['phase162_web_narrative_integration.build_phase162_web_validated_isomorphism_markdown'] == ['tests/test_old.py']
