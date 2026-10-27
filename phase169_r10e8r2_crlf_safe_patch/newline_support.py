"""Strict LF/CRLF source round trip for guarded Python source changes.

The text handed to the existing R10E8 transform is always LF-normalized.
Working-tree bytes preserve their original newline convention after patching.
Mixed or bare-CR files are rejected rather than silently reformatted.
"""
from __future__ import annotations

from pathlib import Path


def decode_working_source(path: Path, data: bytes) -> tuple[str, str]:
    """Decode UTF-8 source as LF text, retaining its uniform newline style."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError(f"unexpected UTF-8 BOM in guarded source: {path}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"source is not valid UTF-8: {path}") from exc
    if "\r\n" in text:
        remainder = text.replace("\r\n", "")
        if "\r" in remainder or "\n" in remainder:
            raise RuntimeError(f"mixed source line endings: {path}")
        return text.replace("\r\n", "\n"), "\r\n"
    if "\r" in text:
        raise RuntimeError(f"bare CR source line endings: {path}")
    return text, "\n"


def encode_working_source(text: str, style: str) -> bytes:
    """Restore the exact newline style selected from the input file."""
    if style not in ("\n", "\r\n"):
        raise ValueError("unsupported newline style")
    if "\r" in text:
        raise RuntimeError("patch output must be LF-normalized")
    return text.replace("\n", style).encode("utf-8")
