"""R3-41P3 narrow, guarded source-function replacement and backup."""
from __future__ import annotations

import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .replacements import RENDERER_HELPER, TODA45_EVIDENCE

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
BACKUP = OUTPUT / "backups"
RENDERER = "phase168_r3_5_model_renderer.py"
PROJECTION = "phase168_r3_27_typed_statement_projection.py"
# SHA-256 fingerprints were read from the user's completed R3-41P2 audit.
EXPECTED_ORIGINAL_SHA256 = {
    RENDERER: "ed248f02f3229d979ac88180fe7690e45778916c18da2d8b2221a3417cbf86cb",
    PROJECTION: "9f51d795c7dc871edeadda2fc9c67e31920d08a88684c52b8a000be9cfe06419",
}


def replaced_function(source: str, name: str, new_text: str) -> str:
    tree = ast.parse(source)
    found = [node for node in ast.walk(tree)
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == name]
    if len(found) != 1:
        raise ValueError(f"Expected exactly one function {name}: found {len(found)}")
    node = found[0]
    lines = source.splitlines(keepends=True)
    before = "".join(lines[:node.lineno - 1])
    after = "".join(lines[node.end_lineno:])
    if not new_text.endswith("\n"):
        raise ValueError("Replacement must end with a newline")
    replaced = before + new_text + after
    ast.parse(replaced)
    return replaced


def compute_patches(current: dict[str, str]) -> dict[str, str]:
    renderer = current[RENDERER]
    projection = current[PROJECTION]
    if "def validated_specialization_citation_numbers(step):" not in renderer:
        raise ValueError("Renderer specialization helper changed: refusing unknown source")
    if renderer.count("sources = validated_specialization_citation_numbers(step)") != 1:
        raise ValueError("Renderer caller changed: refusing unknown source")
    if "def toda45_specialization_evidence(step):" not in projection:
        raise ValueError("Toda45 evidence function changed: refusing unknown source")
    if "bindings = specialize_typed_statement(parent.conclusion, step.conclusion)" not in projection:
        raise ValueError("Toda45 validator call not in expected source: refusing unknown source")
    renderer = replaced_function(renderer, "validated_specialization_citation_numbers", RENDERER_HELPER)
    renderer = renderer.replace(
        "sources = validated_specialization_citation_numbers(step)",
        "sources = direct_given_premise_citation_numbers(step)", 1,
    )
    projection = replaced_function(projection, "toda45_specialization_evidence", TODA45_EVIDENCE)
    ast.parse(renderer)
    ast.parse(projection)
    if "specialize_typed_statement" in renderer:
        raise AssertionError("Renderer still imports mathematical specialization")
    if "specialize_typed_statement" in projection:
        raise AssertionError("Typed statement projection still imports mathematical specialization")
    return {RENDERER: renderer, PROJECTION: projection}


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    raw = {}
    normalized = {}
    for filename in (RENDERER, PROJECTION):
        data = (PROJECT / filename).read_bytes()
        raw[filename] = data
        digest = hashlib.sha256(data).hexdigest()
        if digest != EXPECTED_ORIGINAL_SHA256[filename]:
            raise ValueError(
                "Current source differs from the verified R3-41P2 audit: "
                + filename + ". Refusing to patch unknown code."
            )
        normalized[filename] = data.decode("utf-8-sig").replace("\r\n", "\n")
    updated = compute_patches(normalized)

    BACKUP.mkdir(parents=True, exist_ok=True)
    manifest = {"files": [], "created_at": datetime.now(timezone.utc).isoformat()}
    for filename in (RENDERER, PROJECTION):
        destination = BACKUP / filename
        if destination.exists() and destination.read_bytes() != raw[filename]:
            raise ValueError("Backup collision, refusing to overwrite " + str(destination))
        manifest["files"].append({
            "name": filename,
            "sha256_before": hashlib.sha256(raw[filename]).hexdigest(),
        })

    for filename in (RENDERER, PROJECTION):
        (BACKUP / filename).write_bytes(raw[filename])
    # Preserve original newline convention and BOM, if present.
    replacements = {}
    for filename in (RENDERER, PROJECTION):
        new_source = updated[filename]
        if b"\r\n" in raw[filename]:
            new_source = new_source.replace("\n", "\r\n")
        data = new_source.encode("utf-8-sig" if raw[filename].startswith(b"\xef\xbb\xbf") else "utf-8")
        replacements[filename] = data
        manifest["files"][[x["name"] for x in manifest["files"]].index(filename)][
            "sha256_after"
        ] = hashlib.sha256(data).hexdigest()

    written = []
    try:
        for filename, data in replacements.items():
            (PROJECT / filename).write_bytes(data)
            written.append(filename)
        full = OUTPUT / "full_files"
        full.mkdir(exist_ok=True)
        for filename in (RENDERER, PROJECTION):
            (full / filename).write_bytes(replacements[filename])
        (OUTPUT / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except Exception:
        for filename in written:
            (PROJECT / filename).write_bytes(raw[filename])
        raise
    for filename in (RENDERER, PROJECTION):
        print("PATCHED", PROJECT / filename)
        print("BACKUP", BACKUP / filename)
        print("FULL_FILE", OUTPUT / "full_files" / filename)
    print("APPLICATION_PATCH_ONLY_TWO_FUNCTIONS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
