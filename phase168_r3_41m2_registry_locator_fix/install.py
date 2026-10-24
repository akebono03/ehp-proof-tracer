"""R3-41M2 guarded transaction including source registry locator."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
OUTPUT = PACKAGE / "output"
SOURCES = (
    ("phase168_r3_5_model_renderer.py", "modified_renderer_full.py", "render_model_backed_narrative_markdown"),
    ("phase168_r3_37c_reference_projection.py", "modified_reference_full.py", "project_reference_bodies"),
)
TEST_NAME = "phase168_r3_41l_reasoned_prose/tests/test_phase168_r3_41l_reasoned_prose.py"
ASSESS_NAME = "phase168_r3_39f_frozen_comparison/audit.py"
ASSESS_OLD = r'{"key": "diagonal_general_in_proof", "present": bool(re.search(r"\\pi_\{?n\}?\^\{?n\}?", flat)), "why": "基準にも存在する対角群の一般式"}'
ASSESS_NEW = r'{"key": "diagonal_general_only_in_reference", "present": not bool(re.search(r"\\pi_\{?n\}?\^\{?n\}?", flat)), "why": "一般の対角群構造は Reference に置き本文には重複させない"}'
ETA_SOURCE = "phase165_r12_r20_eta_definition.py"
J2_TEST_NAME = "phase168_r3_41j2_chain_test_scope_fix/tests/test_phase168_r3_41j2_citation_provenance.py"
ETA_LOCATOR_OLD = 'locator="Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation"'
ETA_LOCATOR_NEW = 'locator="Chapter V, i)"'
EXPECTED_RENDERER_SHA = "d2e3876b97d13b0bc417844b5736b1d072aa184bc4cf1d1ae4cca0e1d08af440"
REFERENCE_OLD_LEAD = 'r"Proposition 4.2 により, EHP の列 "'
REFERENCE_OLD_TAIL = 'r"\\xrightarrow{E}\\pi_i^{n+1}$ は完全である."'


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def extract_function(text: str, name: str) -> str:
    tree = ast.parse(text)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError("Expected one function " + name)
    node = matches[0]
    return "".join(text.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def replace_function(original: bytes, target_text: str, fn: str) -> bytes:
    text = original.decode("utf-8-sig")
    old_body = extract_function(text, fn)
    new_body = extract_function(target_text, fn)
    assert old_body != new_body, "Expected function change"
    lines = text.splitlines(keepends=True)
    node = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == fn)
    newline = "\r\n" if b"\r\n" in original else "\n"
    new_text = "".join(lines[:node.lineno - 1]) + new_body.rstrip("\r\n").replace("\r\n", "\n").replace("\n", newline) + newline + "".join(lines[node.end_lineno:])
    ast.parse(new_text)
    return (b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b"") + new_text.encode("utf-8")


def create_patches() -> dict[Path, tuple[bytes, bytes]]:
    patches = {}
    renderer_path = REPO / SOURCES[0][0]
    old_renderer = renderer_path.read_bytes()
    if sha256(old_renderer) != EXPECTED_RENDERER_SHA:
        raise RuntimeError("R3-41L source mismatch, no files patched: " + sha256(old_renderer))
    for path, payload, func in SOURCES:
        destination = REPO / path
        original = destination.read_bytes()
        if path == "phase168_r3_37c_reference_projection.py":
            # The real repository reference source is not rewritten as a registry entity.
            ref_text = original.decode("utf-8-sig")
            if ref_text.count(REFERENCE_OLD_LEAD) != 1 or ref_text.count(REFERENCE_OLD_TAIL) != 1:
                raise RuntimeError("Reference baseline unexpected; no files patched")
        patched = replace_function(original, (PACKAGE / payload).read_text("utf-8"), func)
        patches[destination] = (original, patched)
    # Correct the source registry, not merely its Web display alias.
    eta_path = REPO / ETA_SOURCE
    eta_original = eta_path.read_bytes()
    eta_text = eta_original.decode("utf-8-sig")
    if eta_text.count(ETA_LOCATOR_OLD) != 1:
        raise RuntimeError("Eta registry locator unexpected; no files patched")
    eta_updated = eta_text.replace(ETA_LOCATOR_OLD, ETA_LOCATOR_NEW)
    ast.parse(eta_updated)
    newline = "\r\n" if b"\r\n" in eta_original else "\n"
    eta_patched = (b"\xef\xbb\xbf" if eta_original.startswith(b"\xef\xbb\xbf") else b"") + eta_updated.replace("\r\n", "\n").replace("\n", newline).encode("utf-8")
    patches[eta_path] = (eta_original, eta_patched)

    # This earlier citation test must search the registered short locator.
    j2_path = REPO / J2_TEST_NAME
    j2_original = j2_path.read_bytes()
    j2_text = j2_original.decode("utf-8-sig")
    old_test_search = "_reference_number(model, 'eta-family notation')"
    new_test_search = "_reference_number(model, 'Chapter V, i)')"
    if j2_text.count(old_test_search) != 1:
        raise RuntimeError("R3-41J2 locator test unexpected; no files patched")
    j2_updated = j2_text.replace(old_test_search, new_test_search)
    ast.parse(j2_updated)
    newline = "\r\n" if b"\r\n" in j2_original else "\n"
    j2_patched = (b"\xef\xbb\xbf" if j2_original.startswith(b"\xef\xbb\xbf") else b"") + j2_updated.replace("\r\n", "\n").replace("\n", newline).encode("utf-8")
    patches[j2_path] = (j2_original, j2_patched)
    test_path = REPO / TEST_NAME
    original = test_path.read_bytes()
    source = original.decode("utf-8-sig")
    required = (
        'assert f"{expected}より, ${statement_latex}$ を得る." in body',
        'assert "導出により" in proof',
    )
    if not all(x in source for x in required):
        raise RuntimeError("R3-41L test baseline unexpected; no files patched")
    test_text = (PACKAGE / "updated_r341l_test_full.py").read_text("utf-8")
    ast.parse(test_text)
    newline = "\r\n" if b"\r\n" in original else "\n"
    test_bytes = (b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b"") + test_text.replace("\n", newline).encode("utf-8")
    patches[test_path] = (original, test_bytes)
    # User-approved presentation rule differs from the historical frozen
    # pi4_3 text. Update only the narrow prose benchmark, never its original.
    assess_path = REPO / ASSESS_NAME
    original = assess_path.read_bytes()
    old_text = original.decode("utf-8-sig")
    if old_text.count(ASSESS_OLD) != 1:
        raise RuntimeError("R3-39F benchmark baseline unexpected; no files patched")
    new_text = old_text.replace(ASSESS_OLD, ASSESS_NEW)
    ast.parse(new_text)
    newline = "\r\n" if b"\r\n" in original else "\n"
    patched = (b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b"") + new_text.replace("\r\n", "\n").replace("\n", newline).encode("utf-8")
    patches[assess_path] = (original, patched)
    return patches


def main() -> int:
    patches = create_patches()  # Verify everything before any repository write.
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path, (old, _) in patches.items():
        backup = OUTPUT / (path.name + ".before")
        if backup.exists() and backup.read_bytes() != old:
            raise RuntimeError("Existing backup has different contents; no files patched: " + str(backup))
    for path, (old, _) in patches.items():
        backup = OUTPUT / (path.name + ".before")
        if not backup.exists():
            backup.write_bytes(old)
    written = []
    try:
        for path, (old, new) in patches.items():
            path.write_bytes(new)
            if path.read_bytes() != new:
                raise RuntimeError("File write verification failed: " + str(path))
            written.append(path)
            (OUTPUT / (path.name + ".full.py")).write_bytes(new)
    except BaseException:
        for path in reversed(written):
            path.write_bytes(patches[path][0])
        raise
    report = {
        "phase": "168 R3-41M2", "full_pytest_run": False,
        "changes": [{"file": str(path), "old_sha256": sha256(old), "new_sha256": sha256(new)}
                    for path, (old, new) in patches.items()],
    }
    (OUTPUT / "install.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for path in patches:
        print("PATCHED",path)
        print("BACKUP",OUTPUT/(path.name+".before"))
    print("FULL_FUNCTION",PACKAGE/"renderer_function_full.py")
    print("FULL_REFERENCE_FUNCTION",PACKAGE/"reference_function_full.py")
    print("FULL_TEST_FILE",PACKAGE/"updated_r341l_test_full.py")
    print("FULL_ETA_REGISTRATION",PACKAGE/"eta_definition_function_full.py")
    print("FULL_J2_TEST_FILE",OUTPUT/"test_phase168_r3_41j2_citation_provenance.py.full.py")
    print("FULL_BENCHMARK_FUNCTION",PACKAGE/"assess_function_full.py")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
