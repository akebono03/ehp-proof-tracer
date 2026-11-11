"""R67: fix only the extra escape in the common ImageZeroStatement TeX arrow.

Source-first guard pins the entire reviewed production file, irrespective of
whole-file LF or CRLF. A repeated installation is recognized from the same
pinned original, not from an unchecked substring. The proof tree is untouched.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
import json
import os
from pathlib import Path
import tempfile


PACKAGE = "phase174_r3_r7_r67_zero_map_tex_arrow_fix"
TARGET = "phase168_r3_27_typed_statement_projection.py"
REVIEWED_BLOB = "5b7bf647a7f7f427e2790cbe915709f014480d11"
OLD_LINE = r'            return rf"${symbol}:{source}\\to {target}$ は零写像."'
NEW_LINE = r'            return rf"${symbol}:{source}\to {target}$ は零写像."'


def git_blob_sha(content: bytes) -> str:
    """Compute the Git object SHA-1 of bytes, without Git working-tree filters."""
    return sha1(b"blob " + str(len(content)).encode("ascii") + b"\x00" + content).hexdigest()


def reviewed_bytes(content: str, raw: bytes) -> bool:
    """Accept only exact reviewed bytes or whole-file EOL equivalents."""
    lf = content.encode("utf-8")
    candidates = (raw, lf, lf.replace(b"\n", b"\r\n"))
    return REVIEWED_BLOB in {git_blob_sha(candidate) for candidate in candidates}


def normalized_contents(raw: bytes) -> tuple[str, str]:
    """Preserve CRLF/LF; reject BOM, CR-only and mixed line endings."""
    if raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R67_UNEXPECTED_UTF8_BOM")
    text = raw.decode("utf-8")
    if "\r" in text.replace("\r\n", ""):
        raise RuntimeError("R67_UNEXPECTED_CR_ONLY")
    if "\r\n" in text and text.count("\r\n") != text.count("\n"):
        raise RuntimeError("R67_MIXED_LINE_ENDINGS")
    eol = "\r\n" if "\r\n" in text else "\n"
    return text.replace("\r\n", "\n"), eol


def review_patch(original: bytes) -> tuple[str, bytes]:
    """Verify the entire reviewed source, then change exactly one string line."""
    normalized, eol = normalized_contents(original)
    before = normalized.count(OLD_LINE)
    after = normalized.count(NEW_LINE)
    if before == 1 and after == 0:
        if not reviewed_bytes(normalized, original):
            raise RuntimeError("R67_SOURCE_GUARD_FAILED: reviewed production blob changed")
        altered = normalized.replace(OLD_LINE, NEW_LINE, 1)
        status = "PATCH_REQUIRED"
    elif before == 0 and after == 1:
        reconstructed = normalized.replace(NEW_LINE, OLD_LINE, 1)
        reconstructed_raw = reconstructed.replace("\n", eol).encode("utf-8")
        if not reviewed_bytes(reconstructed, reconstructed_raw):
            raise RuntimeError("R67_SOURCE_GUARD_FAILED: already-patched source is unreviewed")
        altered = normalized
        status = "ALREADY_APPLIED"
    else:
        raise RuntimeError("R67_SOURCE_GUARD_FAILED: ambiguous or missing arrow anchor")
    ast.parse(altered, filename=TARGET)
    if altered.count(NEW_LINE) != 1 or OLD_LINE in altered:
        raise RuntimeError("R67_UNEXPECTED_POST_PATCH_ARROW")
    return status, altered.replace("\n", eol).encode("utf-8")


def verified_function(source: bytes) -> str:
    """Extract full modified function for audit; never use excerpts as replacement."""
    text, _ = normalized_contents(source)
    tree = ast.parse(text)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == "typed_sentence"]
    if len(nodes) != 1:
        raise RuntimeError("R67_TYPED_SENTENCE_FUNCTION_NOT_UNIQUE")
    lines = text.splitlines(keepends=True)
    node = nodes[0]
    return "".join(lines[node.lineno - 1:node.end_lineno]).rstrip() + "\n"


def run(root: Path, *, dry_run: bool = False) -> str:
    """Run review and optionally install atomically, backing up exact old bytes."""
    target = root / TARGET
    if not target.is_file():
        raise RuntimeError("R67_SOURCE_GUARD_FAILED: target missing")
    original = target.read_bytes()
    status, patched = review_patch(original)
    if dry_run:
        return status
    if status == "ALREADY_APPLIED":
        return status
    backup_dir = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    backup_dir = backup_dir / "EHPProofTracerAudit" / PACKAGE
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / "phase168_r3_27_typed_statement_projection.py.before"
    if backup.exists() and backup.read_bytes() != original:
        raise RuntimeError("R67_DIFFERENT_PREVIOUS_BACKUP")
    if target.read_bytes() != original:
        raise RuntimeError("R67_SOURCE_CHANGED_DURING_REVIEW")
    if not backup.exists():
        backup.write_bytes(original)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".r67_", suffix=".tmp", delete=False) as file:
        staged = Path(file.name)
        file.write(patched)
    try:
        if target.read_bytes() != original:
            raise RuntimeError("R67_SOURCE_CHANGED_BEFORE_INSTALL")
        os.replace(staged, target)
    finally:
        if staged.exists():
            staged.unlink()
    if target.read_bytes() != patched:
        raise RuntimeError("R67_POST_INSTALL_BYTES_MISMATCH")
    return "PATCH_APPLIED"


def public_arrow_audit() -> dict[str, object]:
    """Check the real verified proof and its displayed arrow, not a mock root."""
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase174_r3_r7_r57_narrative_source_cleanup.audit import inspect_public

    source = TodaPrimaryGroup(10, 5)
    target = TodaPrimaryGroup(11, 6)
    sentence = typed_sentence(ImageZeroStatement(TodaSuspensionMap(source, target)), None)
    expected = r"$E:\pi_{10}^{5}\to \pi_{11}^{6}$ は零写像."
    if sentence != expected or r"\\to" in sentence:
        raise RuntimeError("R67_TYPED_ZERO_MAP_ARROW_WRONG")
    prior = inspect_public()
    if not (prior["pi11_6_complete"] and prior["pi12_7_complete"]
            and prior["pi11_reference_count"] == 7
            and prior["pi12_reference_count"] == 3):
        raise RuntimeError("R67_R57_PROOF_REGRESSION")
    bridge = build_shared_typed_bridge()
    first, model = _search_with_model(6, 5, bridge)
    markdown = render_model_backed_narrative_markdown(first, model)
    matches = [line.strip() for line in markdown.splitlines() if "は零写像" in line and line.startswith("$E:")]
    if len(matches) != 1 or matches[0] != expected:
        raise RuntimeError("R67_PUBLIC_ZERO_MAP_LINE_CHANGED: " + repr(matches))
    if r"\\to" in markdown:
        raise RuntimeError("R67_PUBLIC_DOUBLE_ESCAPE_REMAINS")
    return {"typed_arrow": sentence, "public_arrow": matches[0],
            "pi11_6_references": len(model.citations), "pi12_7_references": prior["pi12_reference_count"],
            "proofs_complete": True, "math_rules_added": 0, "given_added": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--audit-only", action="store_true")
    options = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if options.audit_only:
        status, _ = review_patch((root / TARGET).read_bytes())
        if status != "ALREADY_APPLIED":
            raise RuntimeError("R67_PUBLIC_AUDIT_REQUIRES_APPLIED_PATCH")
        data = public_arrow_audit()
        output = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
        output = output / "EHPProofTracerAudit" / PACKAGE / "report.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE174_R67_PUBLIC_ZERO_MAP_ARROW=PASS")
        print("PHASE174_R67_PI11_REFERENCES=" + str(data["pi11_6_references"]))
        print("PHASE174_R67_PI12_REFERENCES=" + str(data["pi12_7_references"]))
        print("PHASE174_R67_REPORT=" + str(output))
        print("PHASE174_R67_GATE=PASS_R67_PUBLIC_TYPED_ARROW_AND_R57_PROOFS")
        print("(END)")
        return 0
    status = run(root, dry_run=options.dry_run)
    print("PHASE174_R67_SOURCE_GUARD=PASS")
    print("PHASE174_R67_REVIEWED_BLOB=" + REVIEWED_BLOB)
    print("PHASE174_R67_PATCH_STATUS=" + status)
    print("PHASE174_R67_PRODUCTION_FILES_CHANGED=" + str(0 if options.dry_run or status == "ALREADY_APPLIED" else 1))
    print("PHASE174_R67_NEW_GIVEN=0")
    print("PHASE174_R67_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R67_GATE=" + ("PASS_R67_DRYRUN" if options.dry_run else "PASS_R67_ARROW_PATCH_APPLIED_OR_PRESENT"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
