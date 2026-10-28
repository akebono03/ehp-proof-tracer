"""Fail-closed, full-function patch of the existing shared provider."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
EXPECTED_HEAD = "3e102f43b5d378d511391e0b3eb5a175f07ac2dc"
OLD = (
    "        options.extend(expand_cited_stable_family(goal, tuple(available)))\n"
    "        if not eta_generator_options:\n"
    "            from phase169_r10e5_composite_generator_image.rule import (\n"
    "                expand_composite_generator_image,\n"
    "            )\n"
    "            options.extend(expand_composite_generator_image(goal))\n"
)
NEW = (
    "        cited_stable_options = expand_cited_stable_family(\n"
    "            goal, tuple(available),\n"
    "        )\n"
    "        options.extend(cited_stable_options)\n"
    "        composite_image_options = ()\n"
    "        if not eta_generator_options:\n"
    "            from phase169_r10e5_composite_generator_image.rule import (\n"
    "                expand_composite_generator_image,\n"
    "            )\n"
    "            composite_image_options = expand_composite_generator_image(goal)\n"
    "            options.extend(composite_image_options)\n"
    "        if not (eta_generator_options or cited_stable_options\n"
    "                or composite_image_options):\n"
    "            from phase169_r10eq_r1_universal_stable_definition.definition import (\n"
    "                expand_defined_stable_element_image,\n"
    "            )\n"
    "            options.extend(expand_defined_stable_element_image(goal))\n"
)


def full_function_span(text: str) -> tuple[int, int]:
    start_marker = "def shared_expansion_provider("
    start = text.find(start_marker)
    if start < 0 or text.count(start_marker) != 1:
        raise RuntimeError("shared provider not uniquely found")
    next_def = text.find("\ndef ", start + len(start_marker))
    end = len(text) if next_def < 0 else next_def + 1
    return start, end


def replacement_content(original: bytes) -> tuple[bytes, str]:
    # Preserve existing CRLF if present.
    if original.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("unexpected BOM")
    raw = original.decode("utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    normalized = raw.replace("\r\n", "\n")
    begin, end = full_function_span(normalized)
    old_func = normalized[begin:end]
    if old_func.count(OLD) != 1 or NEW in old_func:
        raise RuntimeError("expected full function anchor changed")
    new_func = old_func.replace(OLD, NEW)
    result = (normalized[:begin] + new_func + normalized[end:]).replace("\n", newline)
    return result.encode("utf-8"), new_func


def apply_patch(output: Path) -> None:
    original = TARGET.read_bytes()
    changed, function = replacement_content(original)
    output.mkdir(parents=True, exist_ok=True)
    before = output / "shared_math.py.before"
    before.write_bytes(original)
    (output / "shared_expansion_provider_FULL.py").write_text(function, encoding="utf-8")
    (output / "phase165_r52_r9_shared_math.py.FULL").write_bytes(changed)
    TARGET.write_bytes(changed)
    print("R10EQ_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    print("R10EQ_BACKUP=" + str(before), flush=True)
    print("R10EQ_FULL_FUNCTION=" + str(output / "shared_expansion_provider_FULL.py"), flush=True)
    print("R10EQ_FULL_FILE=" + str(output / "phase165_r52_r9_shared_math.py.FULL"), flush=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m phase169_r10eq_r1_universal_stable_definition.patch OUTPUT_DIR")
    apply_patch(Path(sys.argv[1]))
