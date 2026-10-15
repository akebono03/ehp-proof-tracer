from pathlib import Path

import install


def test_verified_existing_backup_accepts_exact_restoration(tmp_path, monkeypatch):
    monkeypatch.setattr(install, 'PROJECT', tmp_path)
    monkeypatch.setattr(install, 'BACKUP', tmp_path / 'backup')
    for rel in install.REMOVAL:
        current = tmp_path / rel
        backup = tmp_path / 'backup' / rel
        current.parent.mkdir(parents=True, exist_ok=True)
        backup.parent.mkdir(parents=True, exist_ok=True)
        current.write_bytes(rel.encode('utf-8'))
        backup.write_bytes(rel.encode('utf-8'))
    assert install._verified_existing_backup()


def test_verified_existing_backup_rejects_changed_restoration(tmp_path, monkeypatch):
    monkeypatch.setattr(install, 'PROJECT', tmp_path)
    monkeypatch.setattr(install, 'BACKUP', tmp_path / 'backup')
    for rel in install.REMOVAL:
        current = tmp_path / rel
        backup = tmp_path / 'backup' / rel
        current.parent.mkdir(parents=True, exist_ok=True)
        backup.parent.mkdir(parents=True, exist_ok=True)
        current.write_bytes(b'original')
        backup.write_bytes(b'original')
    (tmp_path / install.REMOVAL[0]).write_bytes(b'changed')
    assert not install._verified_existing_backup()


def test_verified_existing_backup_requires_full_backup(tmp_path, monkeypatch):
    monkeypatch.setattr(install, 'PROJECT', tmp_path)
    monkeypatch.setattr(install, 'BACKUP', tmp_path / 'backup')
    (tmp_path / 'backup').mkdir()
    assert not install._verified_existing_backup()
