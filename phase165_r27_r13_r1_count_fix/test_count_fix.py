from pathlib import Path
from audit import collect


def test_distinct_file_scope_counts_ignore_multiple_references(tmp_path):
    from audit import REQUIRED
    for name in REQUIRED:
        (tmp_path / name).write_text('pass\n', encoding='utf-8')
    (tmp_path / 'main.py').write_text(
        'from standard_production_repository import build_standard_production_proof_repository\n'
        'build_standard_production_proof_repository()\n'
        'build_standard_production_proof_repository()\n',
        encoding='utf-8',
    )
    (tmp_path / 'proof_repository.py').write_text(
        'class ProofRepository:\n    pass\n', encoding='utf-8',
    )
    report = collect(tmp_path)
    assert report['event_counts_by_scope']['PUBLIC_ENTRY_OR_BRIDGE'] >= 2
    assert report['file_counts_by_scope']['PUBLIC_ENTRY_OR_BRIDGE'] == 1
    assert report['file_counts_by_scope']['ROOT_PRODUCTION_OR_UNCLASSIFIED'] == 1
    assert report['files_with_references'] == 2
    assert report['deletion_authorized'] is False
    assert report['production_files_modified'] is False
