from pathlib import Path

from audit import audit


def write(root, file, content):
    (root / file).write_text(content, encoding='utf-8')


def fixture_root(tmp_path):
    from audit import ENTRYPOINTS, SITES
    for path in set(SITES) | {entry[0] for entry in ENTRYPOINTS.values()}:
        write(tmp_path, path, 'def placeholder():\n    pass\n')
    for label, (path, function, guard) in ENTRYPOINTS.items():
        write(tmp_path, path, f'def {function}():\n    repo = build_standard_production_proof_repository()\n    {guard}(repo)\n')
    write(tmp_path, 'phase164_r4_r8_registry_reconstruction.py', 'def reconstruct_phase164_r4_r8_pi5_3():\n    resolve_registered_statement(bridge, assertion_id)\n')
    write(tmp_path, 'phase164_r7_statement_resolution.py', 'STRUCTURED = 1\nFIXED_STATEMENT = 1\n')
    write(tmp_path, 'phase164_r2_citation_eligibility.py', 'SOURCE_ARCHIVE = 1\nPROOF_INTERNAL = 1\nverified_assertion_ids = ()\n')
    return tmp_path


def test_expected_layout_is_scoped_clear(tmp_path):
    root = fixture_root(tmp_path)
    result = audit(root)
    assert result['status'] == 'STATIC_SCOPE_CLEAR_PENDING_TARGETED_PYTEST'
    assert result['scope_closed']
    assert len(result['entrypoints']) == 3


def test_direct_registry_access_blocks_closure(tmp_path):
    root = fixture_root(tmp_path)
    write(root, 'phase164_r4_r8_registry_reconstruction.py', 'def reconstruct_phase164_r4_r8_pi5_3():\n    resolve_registered_statement(bridge, assertion_id)\n    bridge.registry.assertion(assertion_id)\n')
    assert 'pi53_direct_registry_getter_remains' in audit(root)['blockers']


def test_no_shared_resolver_blocks_closure(tmp_path):
    root = fixture_root(tmp_path)
    write(root, 'phase164_r4_r8_registry_reconstruction.py', 'def reconstruct_phase164_r4_r8_pi5_3():\n    pass\n')
    assert 'pi53_no_shared_resolver_call' in audit(root)['blockers']


def test_missing_standard_guard_blocks_closure(tmp_path):
    root = fixture_root(tmp_path)
    write(root, 'toda_calculation_facade.py', 'def build_standard_toda_report():\n    repo = build_standard_production_proof_repository()\n')
    assert 'group_unguarded' in audit(root)['blockers']


def test_missing_citation_policy_blocks_closure(tmp_path):
    root = fixture_root(tmp_path)
    write(root, 'phase164_r2_citation_eligibility.py', 'verified_assertion_ids = ()\n')
    assert 'citation_policy_keeps_archive_denial_missing' in audit(root)['blockers']
