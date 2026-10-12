"""Unit tests for guarded R8-R7 source migration and residual classification."""
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import apply


def test_r8_r7_manifest_contains_original_66_sites():
    assert len(apply.ARCHIVE) == 66
    assert sum(site['r8_r6_classification'] == 'proofstep_reconstruction_migrate' for site in apply.ARCHIVE) == 1


def test_r8_r7_factory_migration_on_synthetic_project(tmp_path):
    factory = tmp_path / apply.FACTORY
    factory.write_text('def project_reference_component_step():\n    return None\n', encoding='utf-8')
    renderer = tmp_path / apply.RENDERER
    renderer.write_text('from phase164_r8_proofstep_factory import (\n    project_reference_component_step,\n)\n\n'
                        'def _phase157_r20_specialize_reference_value(value, changes):\n'
                        '  return replace(\n    value,\n    **changes,\n  )\n', encoding='utf-8')
    old, new = apply.prepare(tmp_path)
    assert set(old) == {apply.FACTORY, apply.RENDERER}
    assert b'replace_legacy_proof_step_fields' in new[apply.FACTORY]
    assert b'if isinstance(value, ProofStep)' in new[apply.RENDERER]


def test_r8_r7_precheck_rejects_changed_renderer(tmp_path):
    (tmp_path / apply.FACTORY).write_text('def project_reference_component_step():\n    return None\n', encoding='utf-8')
    (tmp_path / apply.RENDERER).write_text('from phase164_r8_proofstep_factory import (\n    project_reference_component_step,\n)\n', encoding='utf-8')
    with pytest.raises(ValueError, match='exactly one function'):
        apply.prepare(tmp_path)


def test_r8_r7_no_factory_double_application(tmp_path):
    (tmp_path / apply.FACTORY).write_text('def project_reference_component_step():\n    return None\n\ndef replace_legacy_proof_step_fields():\n    return None\n', encoding='utf-8')
    (tmp_path / apply.RENDERER).write_text('from phase164_r8_proofstep_factory import (\n    project_reference_component_step,\n)\n', encoding='utf-8')
    with pytest.raises(ValueError, match='already exists'):
        apply.prepare(tmp_path)


def test_r8_r7_only_generic_dataclass_replace_is_proofstep_possible():
    reviewed = [s for s in apply.ARCHIVE if s['r8_r6_classification'] != 'proofstep_reconstruction_migrate']
    assert len(reviewed) == 65
    generic = [s for s in reviewed if s['file'] == apply.RENDERER and s['function'] == apply.FUNCTION]
    assert {s['line'] for s in generic} == {1037, 1117}
