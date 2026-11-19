"""Installer accepts one exact anchor, rejects ambiguous rewrites."""
from __future__ import annotations

import ast

import pytest

from phase175_r4r14r5_public_zero_transport.installer import (
    ANCHOR, INSERTION, expected_updated_source,
)


def test_guarded_insert_is_local_and_parseable():
    source = (
        "def shared_expansion_provider(bridge):\n"
        "    extra_providers = ()\n"
        + ANCHOR + "\n"
        "    return extra_providers\n"
    )
    revised = expected_updated_source(source)
    ast.parse(revised)
    assert revised.count(INSERTION) == 1
    assert revised.count(ANCHOR) == 1
    assert "return extra_providers" in revised


def test_repeated_or_ambiguous_insert_fails():
    source = (
        "def shared_expansion_provider(bridge):\n"
        "    extra_providers = ()\n" + ANCHOR + "\n"
        "    return extra_providers\n"
    )
    with pytest.raises(RuntimeError, match="ANCHOR_CHANGED"):
        expected_updated_source(expected_updated_source(source))
    with pytest.raises(RuntimeError, match="ANCHOR_CHANGED"):
        expected_updated_source(source.replace(ANCHOR, ""))
