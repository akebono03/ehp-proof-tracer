"""Correct the R10EB file guard for Git blobs committed with CRLF bytes.

This adapter does not replace any mathematical rule or change the existing
R10EB display transformations. It uses the original reviewed transform().
"""
from __future__ import annotations

from pathlib import Path

from phase169_r10eb_typed_composition_power import patch as original

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "phase169_r10eb_typed_composition_power" / "output"
TARGETS = dict(original.TARGETS)


def prepare_patch(source_files: dict[str, bytes]) -> dict[str, tuple[bytes, str, str]]:
    """Verify the original Git bytes OR the LF-normalized working-tree form.

    Git objects may themselves contain CRLF. Comparing only an LF-converted
    string against such a Git blob is incorrect. The run script separately
    verifies that all tracked source paths match the reviewed HEAD.
    """
    if set(source_files) != set(TARGETS):
        raise RuntimeError("R10EBR1 requires both reviewed source files")
    prepared: dict[str, tuple[bytes, str, str]] = {}
    for path, expected in TARGETS.items():
        raw = source_files[path]
        source, style = original._style_and_source(raw)
        # The committed object can use CRLF (both current Renderer files do),
        # while the local checkout may use Git's supported LF conversion.
        raw_blob = original._git_blob(raw)
        normalized_blob = original._git_blob(source.encode("utf-8"))
        crlf_blob = original._git_blob(
            source.replace("\n", "\r\n").encode("utf-8")
        )
        if expected not in (raw_blob, normalized_blob, crlf_blob):
            raise RuntimeError("R10EBR1 source Git blob not reviewed: " + path)
        updated, function = original.transform(path, source)
        payload = updated.encode("utf-8")
        if style == "CRLF":
            payload = payload.replace(b"\n", b"\r\n")
        prepared[path] = (payload, function, style)
    return prepared


def main() -> None:
    """Apply the same R10EB display transformation after the corrected guard."""
    source_files = {path: (ROOT / path).read_bytes() for path in TARGETS}
    updated = prepare_patch(source_files)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path, (payload, function, style) in updated.items():
        target = ROOT / path
        target.write_bytes(payload)
        clean_name = path.replace("/", "__")
        (OUTPUT / (clean_name + ".FULL")).write_bytes(payload)
        (OUTPUT / (clean_name + ".FUNCTION_FULL.py")).write_text(
            function + "\n", encoding="utf-8",
        )
        print("R10EBR1_PATCHED=" + str(target))
        print("R10EBR1_NEWLINE=" + path + "=" + style)
        print("R10EBR1_FULL_FUNCTION=" + str(OUTPUT / (clean_name + ".FUNCTION_FULL.py")))
    print("R10EBR1_PROOF_OR_INFERENCE_ENGINE_CHANGED=False")


if __name__ == "__main__":
    main()
