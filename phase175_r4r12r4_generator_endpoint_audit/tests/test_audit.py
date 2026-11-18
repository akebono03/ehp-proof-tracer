"""Unit tests of diagnostic classifier; they assert no proof results."""
from __future__ import annotations

import pytest

from phase175_r4r12r4_generator_endpoint_audit.audit import classify_endpoint


def test_matching_endpoint() -> None:
    assert classify_endpoint((8, 4), (8, 4)) == "MATCH"


def test_undefined_endpoint() -> None:
    assert classify_endpoint(None, (8, 4)) == "UNDEFINED_OR_NONCOMPOSABLE"


def test_other_endpoint() -> None:
    assert classify_endpoint((8, 5), (8, 4)) == "DIFFERENT_TYPED_ENDPOINTS"


def test_bad_type() -> None:
    assert classify_endpoint("(8, 4)", (8, 4)) == "UNEXPECTED_ENDPOINT_TYPE"


def test_reviewed_head_pin_is_current() -> None:
    from phase175_r4r12r4_generator_endpoint_audit.audit import EXPECTED_HEAD
    assert EXPECTED_HEAD == "6cdf40e089cb2950d2ae9a6aadb2a36188ca0e7d"
