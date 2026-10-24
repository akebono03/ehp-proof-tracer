"""Offline-only tests of R3-41P7 audit utilities; no proof changes."""
from __future__ import annotations

import json
from pathlib import Path

from phase168_r3_41p7_shape_boundary_audit.audit import (
    BASELINES, CASES, SOURCE_FILES, report_markdown, sha256_file, static_inventory,
)


def test_static_call_inventory_only_validator_calls():
    source = (
        "def one(value):\n"
        "    return _stable_eta_renaming_shape(value, value)\n"
        "def two(value):\n"
        "    return prop42_exactness_indices(value)\n"
        "def three():\n"
        "    return len('x')\n"
    )
    rows = static_inventory(source)
    assert [(r['function'], r['validator']) for r in rows] == [
        ('one', '_stable_eta_renaming_shape'),
        ('two', 'prop42_exactness_indices'),
    ]


def test_required_baselines_are_real_nonempty_fulltexts():
    for name, n, k, _, _ in CASES:
        assert n >= 2 and k == 1
        data = (BASELINES / f'{name}_current.md').read_text(encoding='utf-8')
        assert '使用する結果' in data
        assert '証明' in data
        assert '□' in data


def test_sha256_measures_real_bytes(tmp_path):
    p = tmp_path / 'source.py'
    p.write_bytes(b'proof\r\n')
    first = sha256_file(p)
    p.write_bytes(b'proof\n')
    second = sha256_file(p)
    assert first != second
    assert len(first) == len(second) == 64


def test_report_format_and_source_scope():
    report = {'cases': {'pi3_2': {
        'steps': 18, 'references': 4, 'fulltext_identical_to_p6': True,
        'frozen_requirements_pass': True,
        'provenance': {'citation_numbers_match': True, 'bidirectional_links_valid': True},
    }}}
    written = report_markdown(report)
    assert 'pi3_2 | 18 | 4 | PASS | PASS | PASS' in written
    assert '_stable_eta_renaming_shape' in written
    assert 'prop42_exactness_indices' in written
    assert len(SOURCE_FILES) == 6
