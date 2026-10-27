"""R10E8-R2: newline handling must preserve working bytes and fail closed."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase169_r10e8r2_crlf_safe_patch.newline_support import (
    decode_working_source,
    encode_working_source,
)


def test_r10e8r2_uniform_lf_round_trip():
    path = Path("module.py")
    original = b"def value():\n    return 1\n"
    text, style = decode_working_source(path, original)
    assert style == "\n"
    assert text == original.decode("utf-8")
    assert encode_working_source(text, style) == original
    assert encode_working_source(text.replace("return 1", "return 2"), style) == (
        b"def value():\n    return 2\n"
    )


def test_r10e8r2_uniform_crlf_round_trip():
    path = Path("module.py")
    original = b"def value():\r\n    return 1\r\n"
    text, style = decode_working_source(path, original)
    assert style == "\r\n"
    assert text == "def value():\n    return 1\n"
    assert encode_working_source(text, style) == original
    assert encode_working_source(text.replace("return 1", "return 2"), style) == (
        b"def value():\r\n    return 2\r\n"
    )


@pytest.mark.parametrize("invalid", [
    b"a\r\nb\nc\r\n",
    b"a\r\nb\rc\r\n",
    b"a\rb\r",
])
def test_r10e8r2_mixed_or_bare_cr_refused(invalid):
    with pytest.raises(RuntimeError, match="line endings"):
        decode_working_source(Path("module.py"), invalid)


def test_r10e8r2_bom_and_non_utf8_refused():
    with pytest.raises(RuntimeError, match="BOM"):
        decode_working_source(Path("module.py"), b"\xef\xbb\xbfprint(1)\n")
    with pytest.raises(RuntimeError, match="not valid UTF-8"):
        decode_working_source(Path("module.py"), b"\xff")


def test_r10e8r2_invalid_output_newline_refused():
    with pytest.raises(RuntimeError, match="LF-normalized"):
        encode_working_source("a\r\nb\r\n", "\r\n")
    with pytest.raises(ValueError, match="newline style"):
        encode_working_source("a\nb\n", "\r")


def _guarded_source_fixtures() -> tuple[str, str]:
    family = (
        'from __future__ import annotations\n'
        'from proof import (\n'
        '    ProofRule,\n'
        ')\n'
        '\nROOT = "test"\n'
        'def canonical_member(source):\n'
        '    return source.family_id not in {record.family_id for record in SOURCE_RECORDS}\n'
        'def cited_family_reference_sentence(source):\n'
        '    return source.family_id not in {record.family_id for record in SOURCE_RECORDS}\n'
    )
    shared = (
        'from __future__ import annotations\n'
        'def build_shared_typed_bridge():\n'
        '        sources = sources + (build_cited_stable_family_definitions(),)\n'
    )
    return family, shared


def test_r10e8r2_adapter_applies_original_transform_to_crlf(tmp_path, monkeypatch):
    from phase169_r10e8_hyoujigen_generic_suspension import patch as original
    from phase169_r10e8r2_crlf_safe_patch.patch import apply_guarded_crlf_patch

    family, shared = _guarded_source_fixtures()
    family_path = tmp_path / 'family.py'
    shared_path = tmp_path / 'shared.py'
    output_dir = tmp_path / 'output'
    family_path.write_bytes(family.replace('\n', '\r\n').encode('utf-8'))
    shared_path.write_bytes(shared.replace('\n', '\r\n').encode('utf-8'))
    monkeypatch.setattr(original, 'FAMILY', family_path)
    monkeypatch.setattr(original, 'SHARED', shared_path)
    monkeypatch.setattr(original, 'OUTPUT', output_dir)

    apply_guarded_crlf_patch()
    updated_a = family_path.read_bytes()
    updated_b = shared_path.read_bytes()
    assert b'CHAPTER_VI_SOURCE_RECORDS' in updated_a
    assert b'build_cited_chapter_vi_family_definitions' in updated_b
    assert b'\r\n' in updated_a and b'\n' not in updated_a.replace(b'\r\n', b'')
    assert b'\r\n' in updated_b and b'\n' not in updated_b.replace(b'\r\n', b'')
    assert (output_dir / 'family_citation_IMPORTS_FULL.py').is_file()
    assert (output_dir / 'canonical_member_FULL.py').is_file()
    assert (output_dir / 'build_shared_typed_bridge_FULL.py').is_file()


def test_r10e8r2_adapter_rejects_mixed_newlines_without_writing(tmp_path, monkeypatch):
    from phase169_r10e8_hyoujigen_generic_suspension import patch as original
    from phase169_r10e8r2_crlf_safe_patch.patch import apply_guarded_crlf_patch

    family, shared = _guarded_source_fixtures()
    family_path = tmp_path / 'family.py'
    shared_path = tmp_path / 'shared.py'
    original_bytes = family.replace('\n', '\r\n').encode('utf-8') + b'\n'
    family_path.write_bytes(original_bytes)
    shared_path.write_text(shared, encoding='utf-8')
    monkeypatch.setattr(original, 'FAMILY', family_path)
    monkeypatch.setattr(original, 'SHARED', shared_path)
    monkeypatch.setattr(original, 'OUTPUT', tmp_path / 'output')
    with pytest.raises(RuntimeError, match='mixed source line endings'):
        apply_guarded_crlf_patch()
    assert family_path.read_bytes() == original_bytes
    assert shared_path.read_text(encoding='utf-8') == shared
