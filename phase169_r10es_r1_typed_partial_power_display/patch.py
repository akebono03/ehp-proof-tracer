"""SHA-guarded replacement of one complete public rendering function."""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "toda_human_readable_renderer.py"
FUNCTION = HERE / "full_functions" / "render_toda_expression_latex.py"
EXPECTED_GIT_BLOB = "90b78bdac961392790e6057bcc4d9e5fb2826085"


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def full_function_span(source: str) -> tuple[int, int]:
    pattern = r"(?m)^def render_toda_expression_latex\(\n"
    starts = list(re.finditer(pattern, source))
    if len(starts) != 1:
        raise RuntimeError("expected exactly one rendering function")
    start = starts[0].start()
    following = re.search(r"(?m)^def [a-zA-Z_]\w*\(", source[start + 1:])
    if following is None:
        raise RuntimeError("next top-level function not found")
    end = start + 1 + following.start()
    return start, end


def replacement_content(raw: bytes) -> tuple[bytes, str]:
    if git_blob_sha1(raw) != EXPECTED_GIT_BLOB:
        raise RuntimeError("working source Git blob SHA1 differs; no edit allowed")
    source = raw.decode("utf-8")
    if "\r\n" in source and "\n" in source.replace("\r\n", ""):
        raise RuntimeError("mixed newlines in source")
    style = "\r\n" if "\r\n" in source else "\n"
    normalized = source.replace("\r\n", "\n")
    replacement = FUNCTION.read_text(encoding="utf-8")
    if not replacement.endswith("\n"):
        raise RuntimeError("replacement function must end in newline")
    compile(replacement, str(FUNCTION), "exec")
    start, end = full_function_span(normalized)
    after = normalized[:start] + replacement + "\n\n" + normalized[end:]
    if after == normalized:
        raise RuntimeError("source unchanged unexpectedly")
    compile(after, str(TARGET), "exec")
    return after.replace("\n", style).encode("utf-8"), replacement


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m phase169_r10es_r1_typed_partial_power_display.patch OUTPUT_DIR")
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    before = TARGET.read_bytes()
    modified, function = replacement_content(before)
    backup = output / "toda_human_readable_renderer.py.before"
    full_file = output / "toda_human_readable_renderer.py.FULL"
    full_function = output / "render_toda_expression_latex_FULL.py"
    backup.write_bytes(before)
    full_file.write_bytes(modified)
    full_function.write_text(function, encoding="utf-8")
    TARGET.write_bytes(modified)
    print("R10ES_PATCHED=toda_human_readable_renderer.py", flush=True)
    print("R10ES_BACKUP=" + str(backup), flush=True)
    print("R10ES_FULL_FUNCTION=" + str(full_function), flush=True)
    print("R10ES_FULL_FILE=" + str(full_file), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
