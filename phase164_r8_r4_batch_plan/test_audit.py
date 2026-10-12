"""Self-contained targeted tests for R8-R4 inventory."""
import json
from pathlib import Path

from audit import inventory, write_report


def test_classifies_given_and_inference(tmp_path):
    (tmp_path / 'domain.py').write_text('from proof import ProofStep\na=ProofStep(conclusion=1,premises=(),rule=ProofRule.GIVEN)\nb=apply_inference_match(match)\n', encoding='utf-8')
    result = inventory(tmp_path)
    assert result['category_counts']['given_source_boundary_review'] == 1
    assert result['category_counts']['inference_factory_migrate'] == 1


def test_core_is_kept_separate(tmp_path):
    (tmp_path / 'proof.py').write_text('x=ProofStep(conclusion=1,premises=(),rule=ProofRule.INFERENCE)\n', encoding='utf-8')
    assert inventory(tmp_path)['category_counts']['core_engine_keep_or_internal_refactor'] == 1


def test_does_not_count_nested_archive_or_backup(tmp_path):
    (tmp_path / 'archive').mkdir()
    (tmp_path / 'archive' / 'noise.py').write_text('ProofStep()\n', encoding='utf-8')
    (tmp_path / 'old_backup.py').write_text('ProofStep()\n', encoding='utf-8')
    (tmp_path / 'domain.py').write_text('ProofStep()\n', encoding='utf-8')
    result = inventory(tmp_path)
    assert result['scanned_files'] == 1
    assert len(result['sites']) == 1


def test_replace_not_treated_as_proof_step(tmp_path):
    (tmp_path / 'domain.py').write_text('replace(document, title="new")\n', encoding='utf-8')
    result = inventory(tmp_path)
    assert result['category_counts']['dataclass_replace_type_review'] == 1
    assert 'domain.py' not in result['migration_candidate_files']


def test_report_utf8_on_windows(tmp_path):
    (tmp_path / 'domain.py').write_text('ProofStep()\n', encoding='utf-8')
    result = inventory(tmp_path)
    write_report(result, tmp_path / 'out')
    assert 'ProofStep' in (tmp_path / 'out' / 'report.md').read_text(encoding='utf-8')
    assert json.loads((tmp_path / 'out' / 'audit.json').read_text(encoding='utf-8'))['production_modified'] is False


def test_parse_errors_fail_closed(tmp_path):
    (tmp_path / 'domain.py').write_text('def broken(\n', encoding='utf-8')
    assert len(inventory(tmp_path)['parse_errors']) == 1
