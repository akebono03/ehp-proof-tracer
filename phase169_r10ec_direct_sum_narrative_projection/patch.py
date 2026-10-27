"""Fail-closed, single-function R10EC renderer patch; preserves source newlines."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
TARGET = "phase168_r3_5_model_renderer.py"
REVIEWED_BLOB = "d4d0aa6b3973d5c3d6fe88861cf11948c419cd6b"
ANCHOR = (
    "    for index in order:\n"
    "        if stable_chain_display is not None and index == stable_chain_display.root_index:\n"
)
REPLACEMENT = (
    "    # R10EC: a complete, verified direct-sum proof may present the actual\n"
    "    # E^r endpoints, while retaining all certified ProofSteps and citations.\n"
    "    from phase169_r10ec_direct_sum_narrative_projection.projection import (\n"
    "        project_verified_direct_sum_transport,\n"
    "    )\n"
    "    direct_sum_display = (\n"
    "        project_verified_direct_sum_transport(model, order)\n"
    "        if not incomplete else None\n"
    "    )\n"
    "    if direct_sum_display is not None:\n"
    "        suppressed_body_indices.update(direct_sum_display.hidden_indices)\n"
    "    for index in order:\n"
    "        if direct_sum_display is not None and index == direct_sum_display.root_index:\n"
    "            lines.extend((direct_sum_display.statement, \"\"))\n"
    "        if stable_chain_display is not None and index == stable_chain_display.root_index:\n"
)


def _git_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _decode_and_style(data: bytes) -> tuple[str, str]:
    if not data:
        raise RuntimeError("R10EC empty source")
    if b"\r\n" in data:
        residue = data.replace(b"\r\n", b"")
        if b"\r" in residue or b"\n" in residue:
            raise RuntimeError("R10EC mixed newline source refused")
        return data.replace(b"\r\n", b"\n").decode("utf-8"), "CRLF"
    if b"\r" in data:
        raise RuntimeError("R10EC CR-only source refused")
    return data.decode("utf-8"), "LF"


def _function(source: str, name: str) -> str:
    tree = ast.parse(source)
    candidates = [node for node in tree.body
                  if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(candidates) != 1:
        raise RuntimeError("R10EC function anchor not unique")
    return ast.get_source_segment(source, candidates[0]) or ""


def transform(source: str) -> tuple[str, str]:
    original = _function(source, "render_model_backed_narrative_markdown")
    if original.count(ANCHOR) != 1 or source.count(ANCHOR) != 1:
        raise RuntimeError("R10EC reviewed renderer anchor changed")
    updated = source.replace(ANCHOR, REPLACEMENT, 1)
    final = _function(updated, "render_model_backed_narrative_markdown")
    if final != original.replace(ANCHOR, REPLACEMENT, 1):
        raise RuntimeError("R10EC renderer changed outside reviewed function")
    if final.count(REPLACEMENT) != 1:
        raise RuntimeError("R10EC renderer output postcondition failed")
    return updated, final


def prepare_patch(data: bytes) -> tuple[bytes, str, str]:
    """Accept only verified Git content, with LF/CRLF checkout conversion."""
    source, style = _decode_and_style(data)
    raw = source.encode("utf-8")
    crlf = raw.replace(b"\n", b"\r\n")
    if _git_sha(data) != REVIEWED_BLOB and _git_sha(raw) != REVIEWED_BLOB and _git_sha(crlf) != REVIEWED_BLOB:
        raise RuntimeError("R10EC reviewed renderer Git blob mismatch")
    updated, function = transform(source)
    payload = updated.encode("utf-8")
    if style == "CRLF":
        payload = payload.replace(b"\n", b"\r\n")
    return payload, function, style


def main() -> None:
    target = ROOT / TARGET
    payload, function, style = prepare_patch(target.read_bytes())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    full = OUTPUT / "phase168_r3_5_model_renderer.py.FULL"
    fn = OUTPUT / "render_model_backed_narrative_markdown_FULL.py"
    full.write_bytes(payload)
    fn.write_text(function + "\n", encoding="utf-8")
    print("R10EC_PATCHED=" + str(target))
    print("R10EC_NEWLINE=" + style)
    print("R10EC_FULL_FILE=" + str(full))
    print("R10EC_FULL_FUNCTION=" + str(fn))
    print("R10EC_PROOF_AND_INFERENCE_ENGINE_CHANGED=False")


if __name__ == "__main__":
    main()
