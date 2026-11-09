"""Focused lineage policy: only reviewed phase directories and one cache file."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r26_prop27_source_premise_connection.audit import (
    ALLOWED_CACHE, classify_changes,
)


def test_reviewed_r24_r25_r26_and_cache_allowed():
    paths = (
        "phase174_r3_r7_r24_prop27_general_typed_design/audit.py",
        "phase174_r3_r7_r25_prop27_isolated_inference/rule.py",
        "phase174_r3_r7_r26_prop27_source_premise_connection/bridge.py",
        ALLOWED_CACHE,
    )
    assert classify_changes(paths) == paths


@pytest.mark.parametrize("path", [
    "proof.py", "sources/toda/Toda_02_2.tex",
    ".pytest_cache/v/cache/lastfailed", ".pytest_cache/v/cache/stepwise",
    "phase174_r3_r7_r18_delta_image_surjectivity/rule.py",
])
def test_unreviewed_changes_rejected(path):
    with pytest.raises(RuntimeError):
        classify_changes((path,))
