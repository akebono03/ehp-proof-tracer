"""Guarded replacement tests; no production imports or public proof claims."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r16_public_ehp_zero_root.patch import (
    BASE_BLOB, NEW, OLD, blob_sha, normalize_and_style, transform_source,
)


def sample_source() -> str:
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        + OLD
        + "        options.append(expand_hopf_image_relation(goal, ()))\n"
        + "        return tuple(options)\n"
        + "    return expand\n"
    )


def test_single_whole_function_preserves_existing_api_and_old_rule() -> None:
    text = transform_source(sample_source())
    assert text.count(NEW) == 1
    assert OLD not in text
    assert "def shared_expansion_provider():" in text
    assert "        options.append(expand_hopf_image_relation(goal, ()))" in text
    assert "expand_ehp_zero_from_delta_surjectivity(goal)" in text


def test_no_second_apply_and_no_nonmatching_anchor() -> None:
    updated = transform_source(sample_source())
    with pytest.raises(RuntimeError):
        transform_source(updated)
    with pytest.raises(RuntimeError):
        transform_source("def shared_expansion_provider():\n    return None\n")


def test_unique_function_and_anchor_required() -> None:
    with pytest.raises(RuntimeError):
        transform_source(sample_source().replace("def shared_expansion_provider():", "def unrelated():"))
    with pytest.raises(RuntimeError):
        transform_source(sample_source().replace("    return expand", OLD + "    return expand"))


@pytest.mark.parametrize("content", (
    b"a\r\nb\n", b"a\rb\r", b"\xef\xbb\xbfa\n",
))
def test_mixed_eol_or_bom_is_rejected(content: bytes) -> None:
    with pytest.raises(RuntimeError):
        normalize_and_style(content)


def test_uniform_line_endings_are_preserved() -> None:
    assert normalize_and_style(b"a\nb\n") == ("a\nb\n", b"\n")
    assert normalize_and_style(b"a\r\nb\r\n") == ("a\nb\n", b"\r\n")
    assert blob_sha(b"a\nb\n") != blob_sha(b"a\r\nb\r\n")
    assert len(BASE_BLOB) == 40


def test_full_function_export_is_not_an_abbreviated_diff(tmp_path) -> None:
    from phase174_r3_r7_r16_public_ehp_zero_root.patch import export_complete_function

    path = tmp_path / "MODIFIED_FUNCTION_FULL_JA.md"
    export_complete_function(transform_source(sample_source()), path)
    result = path.read_text(encoding="utf-8")
    assert "def shared_expansion_provider():" in result
    assert "    def expand(goal):" in result
    assert "        return tuple(options)" in result
    assert "    return expand" in result
    assert "expand_ehp_zero_from_delta_surjectivity(goal)" in result


def test_patched_bytes_require_exact_sha_and_retain_crlf(monkeypatch) -> None:
    import phase174_r3_r7_r16_public_ehp_zero_root.patch as target

    original = sample_source().encode("utf-8")
    monkeypatch.setattr(target, "BASE_BLOB", blob_sha(original))
    expected = transform_source(sample_source()).encode("utf-8")
    assert target.patched_bytes(original) == expected
    assert target.patched_bytes(original.replace(b"\n", b"\r\n")) == expected.replace(b"\n", b"\r\n")
    with pytest.raises(RuntimeError):
        target.patched_bytes(original + b"# unexpected edit\n")
