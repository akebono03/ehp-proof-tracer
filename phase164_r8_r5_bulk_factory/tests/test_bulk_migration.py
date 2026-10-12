from collections import Counter
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from apply import AUDIT, BASELINE, expected_sites, migrate


def fixture_project(tmp_path):
    (tmp_path / 'phase164_r8_proofstep_factory.py').write_bytes(BASELINE)
    for relative, sites in expected_sites().items():
        lines = ['from proof import ProofStep, ProofRule, apply_inference_match\n', '\n', 'def build():\n']
        for site in sites:
            if site['category'] == 'given_source_boundary_review':
                text = 'ProofStep(conclusion=object(), premises=(), rule=ProofRule.GIVEN)'
            elif site['category'] == 'inference_constructor_provenance_review':
                text = 'ProofStep(conclusion=object(), premises=(object(),), rule=ProofRule.INFERENCE)'
            else:
                text = 'apply_inference_match(object())'
            lines.append('    x = ' + text + '\n')
        (tmp_path / relative).write_text(''.join(lines), encoding='utf-8')


def test_every_expected_site_is_preflighted(tmp_path):
    fixture_project(tmp_path)
    report = migrate(tmp_path, dry_run=True)
    assert report['dry_run'] is True
    assert report['counts']['given_source_boundary_review'] == 128
    assert report['counts']['inference_constructor_provenance_review'] == 18
    assert report['counts']['inference_factory_migrate'] == 22


def test_migrates_all_preserving_rule_selection(tmp_path):
    fixture_project(tmp_path)
    report = migrate(tmp_path)
    assert report['status'] == 'MIGRATED_LEGACY_STATUS_PRESERVED'
    assert report['files_modified'] == len(expected_sites()) + 1
    text = (tmp_path / 'hopf_rules.py').read_text(encoding='utf-8')
    assert 'create_legacy_given_proof_step(' in text
    assert 'ProofStep(' not in text
    assert 'from phase164_r8_proofstep_factory import (' in text
    assert (tmp_path / 'phase164_r8_r5_output/CHANGED_CODE.md').is_file()
    assert 'create_legacy_specialization_proof_step' in (tmp_path / 'phase164_r8_proofstep_factory.py').read_text()


def test_preflight_prevents_partial_mutation(tmp_path):
    fixture_project(tmp_path)
    (tmp_path / 'hopf_rules.py').write_text('invalid = 1\n', encoding='utf-8')
    previous = (tmp_path / 'phase164_r8_proofstep_factory.py').read_bytes()
    with pytest.raises(ValueError, match='PRECHECK FAILED'):
        migrate(tmp_path)
    assert (tmp_path / 'phase164_r8_proofstep_factory.py').read_bytes() == previous


def test_factory_revision_guard(tmp_path):
    fixture_project(tmp_path)
    factory = tmp_path / 'phase164_r8_proofstep_factory.py'
    factory.write_bytes(BASELINE + b'\n# local changes\n')
    with pytest.raises(ValueError, match='differs from verified baseline'):
        migrate(tmp_path)
    assert factory.read_bytes().endswith(b'# local changes\n')


def test_manifest_excludes_engine_and_own_factory():
    sites = [s for values in expected_sites().values() for s in values]
    assert all(s['file'] != 'proof.py' for s in sites)
    assert all(s['file'] != 'phase164_r8_proofstep_factory.py' for s in sites)
    assert Counter(s['category'] for s in sites) == {
        'given_source_boundary_review': 128,
        'inference_constructor_provenance_review': 18,
        'inference_factory_migrate': 22,
    }
