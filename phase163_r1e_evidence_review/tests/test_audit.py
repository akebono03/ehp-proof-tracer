import csv
from pathlib import Path

from audit import inspect_assignments, read_csv


def test_read_csv_handles_utf8_bom(tmp_path: Path) -> None:
    source = tmp_path / 'items.csv'
    with source.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['file', 'line'])
        writer.writeheader()
        writer.writerow({'file': 'example.py', 'line': '3'})
    assert read_csv(source) == [{'file': 'example.py', 'line': '3'}]


def test_inspect_assignments_tracks_entry_name(tmp_path: Path) -> None:
    source = tmp_path / 'example.py'
    source.write_text('ENTRY = ProofRepositoryEntry(\n    key="item",\n    step=step,\n)\n', encoding='utf-8')
    assert inspect_assignments(source, {1}) == {1: 'ENTRY'}
