"""Installer preflight and change-unit tests that need no source rewrite."""
from __future__ import annotations

import pytest

from phase171_r20r6_order_four_connection.install import (
    APPEND,
    PROVIDER_ANCHOR,
    PROVIDER_FLAG,
    SOURCE_FLAG,
    patched_text,
)


def test_installer_adds_exactly_one_source_rule_and_provider_call() -> None:
    source = "def inferred_order_four_rule(\n    return None\n"
    provider = "def shared_expansion_provider():\n" + PROVIDER_ANCHOR + "    return ()\n"
    after_source, after_provider = patched_text(source, provider)
    assert after_source.count(SOURCE_FLAG) == 1
    assert after_provider.count(PROVIDER_FLAG) == 1
    assert APPEND.strip() in after_source
    assert patched_text(after_source, after_provider) == (after_source, after_provider)


def test_installer_refuses_partial_or_drifted_source() -> None:
    source = "def inferred_order_four_rule(\n    return None\n"
    provider = "def shared_expansion_provider():\n" + PROVIDER_ANCHOR + "    return ()\n"
    after_source, after_provider = patched_text(source, provider)
    with pytest.raises(RuntimeError, match="partial"):
        patched_text(after_source, provider)
    with pytest.raises(RuntimeError, match="partial"):
        patched_text(source, after_provider)
    with pytest.raises(RuntimeError, match="provider anchor"):
        patched_text(source, "def shared_expansion_provider():\n    return ()\n")


def test_installer_accepts_reviewed_crlf_provider() -> None:
    source = "def inferred_order_four_rule(\n    return None\n"
    provider = (
        "def shared_expansion_provider():\n"
        + PROVIDER_ANCHOR
        + "    return ()\n"
    ).replace("\n", "\r\n")
    after_source, after_provider = patched_text(source, provider)
    assert after_source.count(SOURCE_FLAG) == 1
    assert after_provider.count(PROVIDER_FLAG) == 1
    assert after_provider.count("\r\n") > provider.count("\r\n")
    assert after_provider.replace("\r\n", "").find("\n") == -1
    assert patched_text(after_source, after_provider) == (after_source, after_provider)


def test_installer_rejects_duplicate_crlf_provider_anchor() -> None:
    source = "def inferred_order_four_rule(\n    return None\n"
    provider = (
        "def shared_expansion_provider():\n"
        + PROVIDER_ANCHOR
        + PROVIDER_ANCHOR
        + "    return ()\n"
    ).replace("\n", "\r\n")
    with pytest.raises(RuntimeError, match="provider anchor"):
        patched_text(source, provider)
