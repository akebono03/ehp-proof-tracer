"""Replace only the public Web entry function, preserving unrelated source."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "web_group_proof.py"
REPLACEMENT = PACKAGE / "full_functions" / "build_standard_web_group_proof_view_FULL.py"
OUTPUT = PACKAGE / "output"
BACKUP = OUTPUT / "web_group_proof.py.before"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    original = TARGET.read_bytes()
    text = original.decode("utf-8-sig")
    if "phase168_r3_41p13_trust_boundary" in text:
        raise RuntimeError("R3-41P13 already installed; refusing to overwrite backup")
    reuse_backup = False
    if BACKUP.exists():
        manifest = OUTPUT / "manifest.json"
        if not manifest.is_file():
            raise RuntimeError("Previous backup has no manifest")
        saved = json.loads(manifest.read_text(encoding="utf-8"))
        if (BACKUP.read_bytes() != original
                or saved.get("before_sha256") != sha256(original)):
            raise RuntimeError("Existing backup does not match current source")
        reuse_backup = True
    if "model = build_linked_proof_narrative_model(result, model_bridge)" not in text:
        raise RuntimeError("Existing public model route differs from reviewed develop")
    if "def build_web_partial_group_proof_view(" not in text:
        raise RuntimeError("The existing partial Web compatibility entry is missing")
    tree = ast.parse(text)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == "build_standard_web_group_proof_view"]
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one public standard Web function")
    node = matches[0]
    lines = text.splitlines(keepends=True)
    replacement = REPLACEMENT.read_text(encoding="utf-8")
    ast.parse(replacement)
    if "def build_standard_web_group_proof_view(" not in replacement:
        raise RuntimeError("Full replacement function not found")
    newline = "\r\n" if b"\r\n" in original else "\n"
    replacement = replacement.replace("\n", newline).rstrip("\r\n") + newline
    rewritten = "".join(lines[:node.lineno - 1]) + replacement + "".join(lines[node.end_lineno:])
    if "phase168_r3_41p13_trust_boundary" not in rewritten:
        raise RuntimeError("Trust boundary is absent in replacement")
    ast.parse(rewritten)
    if not reuse_backup:
        BACKUP.write_bytes(original)
    encoded = rewritten.encode("utf-8")
    if original.startswith(b"\xef\xbb\xbf"):
        encoded = b"\xef\xbb\xbf" + encoded
    TARGET.write_bytes(encoded)
    (OUTPUT / "web_group_proof.py.FULL.py").write_bytes(TARGET.read_bytes())
    (OUTPUT / "manifest.json").write_text(json.dumps({
        "target": str(TARGET),
        "before_sha256": sha256(original),
        "after_sha256": sha256(TARGET.read_bytes()),
        "modified_functions": ["build_standard_web_group_proof_view"],
        "new_module": "phase168_r3_41p13_trust_boundary/verification.py",
        "full_pytest_run": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PATCHED", TARGET)
    print("BACKUP", BACKUP)
    print("FULL_FILE", OUTPUT / "web_group_proof.py.FULL.py")


if __name__ == "__main__":
    main()
