from __future__ import annotations

import shutil
from pathlib import Path

from install import BACKUP, PROJECT, REMOVAL


def restore() -> None:
    if not BACKUP.is_dir() or not all((BACKUP / path).is_file() for path in REMOVAL):
        raise RuntimeError('Complete backup does not exist; no restoration performed')
    for rel in REMOVAL:
        target = PROJECT / rel
        if target.exists():
            raise RuntimeError(f'Unexpected existing target prevents restore: {rel}')
    for rel in REMOVAL:
        destination = PROJECT / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BACKUP / rel, destination)
    print('R5-R17 removed files restored; backup preserved')


if __name__ == '__main__':
    restore()
