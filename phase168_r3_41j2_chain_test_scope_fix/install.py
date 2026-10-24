"""Phase 168 R3-41J2: guarded renderer reapplication and focused test correction."""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
RENDERER = ROOT / "phase168_r3_5_model_renderer.py"
TEST_FILE = ROOT / "phase168_r3_26a_after_r3_25a" / "tests" / "test_phase168_r3_26_projection.py"
NEW_RENDERER_FUNCTION = PACKAGE / "modified_function_full.py"
OLD_TEST_FILE = PACKAGE / "original_projection_test.py"
NEW_TEST_FUNCTION = PACKAGE / "modified_test_function_full.py"
OUTPUT = PACKAGE / "output"
RENDERER_BACKUP = OUTPUT / "phase168_r3_5_model_renderer.py.before"
TEST_BACKUP = OUTPUT / "test_phase168_r3_26_projection.py.before"
EXPECTED_RENDERER_SHA256 = "068490ef45f2072d537dd674db04cf0704832c1a9832394c29f5c04e11fcc588"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_one_function(original_bytes: bytes, replacement: str, function_name: str) -> bytes:
    original = original_bytes.decode("utf-8-sig")
    nodes = [node for node in ast.parse(original).body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == function_name]
    if len(nodes) != 1:
        raise RuntimeError(f"exactly one {function_name}() definition required")
    replacement_nodes = ast.parse(replacement).body
    if (len(replacement_nodes) != 1
            or not isinstance(replacement_nodes[0], ast.FunctionDef)
            or replacement_nodes[0].name != function_name):
        raise RuntimeError(f"replacement must be the complete {function_name}() function")
    end_of_lines = "\r\n" if b"\r\n" in original_bytes else "\n"
    parts = original.splitlines(keepends=True)
    span = nodes[0]
    code = "".join(parts[:span.lineno - 1])
    code += replacement.replace("\r\n", "\n").replace("\n", end_of_lines)
    code += "".join(parts[span.end_lineno:])
    ast.parse(code)
    bom = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
    return bom + code.encode("utf-8")


def main() -> int:
    original_renderer = RENDERER.read_bytes()
    original_test = TEST_FILE.read_bytes()
    if sha256(original_renderer) != EXPECTED_RENDERER_SHA256:
        raise RuntimeError(
            "renderer changed since verified pre-R3-41J snapshot; no files patched. "
            f"current_sha256={sha256(original_renderer)}"
        )
    reference_test = OLD_TEST_FILE.read_text(encoding="utf-8")
    local_test = original_test.decode("utf-8-sig").replace("\r\n", "\n")
    if local_test != reference_test:
        raise RuntimeError("existing R3-26a test differs from verified develop snapshot; no files patched")
    renderer_source = original_renderer.decode("utf-8-sig")
    required = (
        "project_exactness_chains(model)",
        "project_narrative_order(model, suppressed_exactness)",
        "project_toda45_specialization_citation_numbers(",
        "model.step_citation_numbers[index]",
        "project_stable_eta_notation_transition(model, index)",
    )
    if not all(item in renderer_source for item in required):
        raise RuntimeError("current Renderer API contract not recognized; no files patched")
    new_renderer = replace_one_function(
        original_renderer, NEW_RENDERER_FUNCTION.read_text(encoding="utf-8"),
        "render_model_backed_narrative_markdown",
    )
    new_test = replace_one_function(
        original_test, NEW_TEST_FUNCTION.read_text(encoding="utf-8"),
        "test_pi32_three_windows_project_one_chain",
    )
    if new_renderer == original_renderer or new_test == original_test:
        raise RuntimeError("expected precisely two scoped changes")

    OUTPUT.mkdir(exist_ok=True)
    for backup, original in ((RENDERER_BACKUP, original_renderer), (TEST_BACKUP, original_test)):
        if backup.exists() and backup.read_bytes() != original:
            raise RuntimeError(f"old backup differs from current source: {backup}; no files patched")
    if not RENDERER_BACKUP.exists():
        RENDERER_BACKUP.write_bytes(original_renderer)
    if not TEST_BACKUP.exists():
        TEST_BACKUP.write_bytes(original_test)
    (OUTPUT / "renderer_full_file.py").write_bytes(new_renderer)
    (OUTPUT / "projection_test_full_file.py").write_bytes(new_test)

    try:
        RENDERER.write_bytes(new_renderer)
        TEST_FILE.write_bytes(new_test)
        if RENDERER.read_bytes() != new_renderer or TEST_FILE.read_bytes() != new_test:
            raise RuntimeError("post-write verification failed")
    except BaseException:
        RENDERER.write_bytes(original_renderer)
        TEST_FILE.write_bytes(original_test)
        raise
    payload = {
        "phase": "168 R3-41J2",
        "status": "PATCHED",
        "changed_files": [str(RENDERER), str(TEST_FILE)],
        "before_sha256": {"renderer": sha256(original_renderer), "test": sha256(original_test)},
        "after_sha256": {"renderer": sha256(new_renderer), "test": sha256(new_test)},
        "new_renderer_function": str(NEW_RENDERER_FUNCTION),
        "new_test_function": str(NEW_TEST_FUNCTION),
        "full_pytest_run": False,
    }
    (OUTPUT / "install.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("PATCHED", RENDERER)
    print("PATCHED_TEST", TEST_FILE)
    print("BACKUP", RENDERER_BACKUP)
    print("BACKUP_TEST", TEST_BACKUP)
    print("FULL_FUNCTION", NEW_RENDERER_FUNCTION)
    print("FULL_TEST_FUNCTION", NEW_TEST_FUNCTION)
    print("FULL_FILE", OUTPUT / "renderer_full_file.py")
    print("FULL_TEST_FILE", OUTPUT / "projection_test_full_file.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
