from pathlib import Path
from prune import BACKUP_CANDIDATES, prune


def test_prune_removes_unreferenced_backup_with_verified_copy(tmp_path: Path) -> None:
    target = tmp_path / BACKUP_CANDIDATES[0]
    target.write_text('OLD BACKUP = True\n', encoding='utf-8')
    result = prune(tmp_path, apply=True, output=tmp_path / 'r20')
    assert result['removed_files'] == 1
    assert not target.exists()
    assert (tmp_path / 'r20' / 'removed_files_backup' / target.name).read_text(encoding='utf-8') == 'OLD BACKUP = True\n'


def test_prune_protects_referenced_backup(tmp_path: Path) -> None:
    target = tmp_path / BACKUP_CANDIDATES[0]
    target.write_text('old = 1\n', encoding='utf-8')
    (tmp_path / 'active.py').write_text(f'path = "{target.name}"\n', encoding='utf-8')
    result = prune(tmp_path, apply=True, output=tmp_path / 'r20')
    assert result['removed_files'] == 0
    assert result['blocked_files'] == 1
    assert target.exists()


def test_prune_is_idempotent_and_keeps_production(tmp_path: Path) -> None:
    target = tmp_path / BACKUP_CANDIDATES[0]
    target.write_text('old = 1\n', encoding='utf-8')
    production = tmp_path / 'standard_production_repository.py'
    production.write_text('keep = True\n', encoding='utf-8')
    prune(tmp_path, apply=True, output=tmp_path / 'r20')
    result = prune(tmp_path, apply=True, output=tmp_path / 'r20')
    assert result['removed_files'] == 0
    assert production.read_text(encoding='utf-8') == 'keep = True\n'
