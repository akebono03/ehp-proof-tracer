"""R10ET-R3B: guard expansion is limited to inspected audit-only commits."""
from __future__ import annotations

from phase169_r10et_r3b_reviewed_head_guard.audit import (
    REVIEWED_HEADS,
    EXPECTED_SHARED_BLOB,
)


def test_reviewed_heads_are_only_three_inspected_commits():
    assert REVIEWED_HEADS == (
        "a5892721436effaf7be759ff17afd3bd427814ed",
        "085b58cfa1bdf0e0e3d164fbff0c4e95deb07367",
        "c63ca5d07904e7725cbfabc9db2d714845d9a8c7",
    )


def test_checked_provider_blob_is_unchanged():
    assert EXPECTED_SHARED_BLOB == "61cbadb06f770c51a9c1f5a3c8026acf9e3e14aa"
