"""R70 audited, idempotent patch of one shared completed-narrative formatter."""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess


PACKAGE = "phase174_r3_r7_r70_verified_narrative_projection"
TARGET = "phase171_r20r13_eta_sentence_layout/projection.py"
REVIEWED_BLOB = "4c1ef57ed0a20d551ae24c80d4b7ddbbb7df9c31"
REVIEWED_DEPENDENCIES = {
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_27_typed_statement_projection.py": "9ce32b5db34a3981649b9b9f2c5ff897eb8de831",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r56_cyclic_generator_bridge/rule.py": "e6bbeb8efa47a46f7326b8711b6de9e79ff60319",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py": "6031f6a1b396d040181f04b792bc5c5caf2c5530",
}

BEFORE = '''def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    return split_completed_proof_sentences(
        combine_adjacent_verified_eta_sentences(lines, model)
    )
'''

AFTER = '''def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    from phase174_r3_r7_r70_verified_narrative_projection.projection import (
        project_verified_general_narrative,
    )
    return split_completed_proof_sentences(
        project_verified_general_narrative(
            combine_adjacent_verified_eta_sentences(lines, model), model,
        )
    )
'''


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def normalize(raw: bytes) -> tuple[str, bytes, str]:
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    body = raw[len(bom):]
    if b"\r" in body.replace(b"\r\n", b""):
        raise RuntimeError("R70_UNEXPECTED_CR_OR_MIXED_EOL")
    if b"\r\n" in body and b"\n" in body.replace(b"\r\n", b""):
        raise RuntimeError("R70_MIXED_EOL")
    eol = "\r\n" if b"\r\n" in body else "\n"
    return body.decode("utf-8").replace("\r\n", "\n"), bom, eol


def accepts_sha(raw: bytes, sha: str) -> bool:
    content, bom, _ = normalize(raw)
    lf = bom + content.encode("utf-8")
    crlf = bom + content.replace("\n", "\r\n").encode("utf-8")
    return sha in {git_blob_sha(raw), git_blob_sha(lf), git_blob_sha(crlf)}


def replace_formatter(original: bytes) -> tuple[str, bytes]:
    content, bom, eol = normalize(original)
    sha_valid = accepts_sha(original, REVIEWED_BLOB)
    if content.count(BEFORE) == 1 and AFTER not in content:
        if not sha_valid:
            raise RuntimeError("R70_SOURCE_GUARD_FAILED")
        rewritten = content.replace(BEFORE, AFTER, 1)
        state = "PATCH_REQUIRED"
    elif content.count(AFTER) == 1 and BEFORE not in content:
        rewritten = content.replace(AFTER, BEFORE, 1)
        baseline = bom + rewritten.replace("\n", eol).encode("utf-8")
        if not accepts_sha(baseline, REVIEWED_BLOB):
            raise RuntimeError("R70_POST_PATCH_SOURCE_MISMATCH")
        rewritten = content
        state = "ALREADY_APPLIED"
    else:
        raise RuntimeError("R70_UNREVIEWED_FORMATTER_BODY")
    ast.parse(rewritten)
    result = bom + rewritten.replace("\n", eol).encode("utf-8")
    return state, result


def source_guard(root: Path) -> tuple[str, ...]:
    checked = []
    for relative, sha in REVIEWED_DEPENDENCIES.items():
        if not accepts_sha((root / relative).read_bytes(), sha):
            raise RuntimeError("R70_REVIEWED_DEPENDENCY_CHANGED: " + relative)
        checked.append(relative)
    return tuple(checked)


def write_full_formatter(root: Path) -> None:
    target = (root / TARGET).read_text(encoding="utf-8-sig")
    parsed = ast.parse(target)
    matches = [x for x in parsed.body
               if isinstance(x, ast.FunctionDef) and x.name == "format_complete_proof_sentences"]
    if len(matches) != 1:
        raise RuntimeError("R70_FORMATTER_NOT_UNIQUE")
    full = ast.get_source_segment(target, matches[0])
    if full is None or "project_verified_general_narrative" not in full:
        raise RuntimeError("R70_FULL_FUNCTION_MISSING")
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    (output / "format_complete_proof_sentences_FULL_AFTER.py").write_text(
        full + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=root,
                            text=True, capture_output=True, check=False)
    if branch.returncode != 0 or branch.stdout.strip() != "develop":
        raise RuntimeError("R70_DEVELOP_BRANCH_REQUIRED")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          text=True, capture_output=True, check=True).stdout.strip()
    checked = source_guard(root)
    target = root / TARGET
    before = target.read_bytes()
    state, after = replace_formatter(before)
    print("PHASE174_R70_SOURCE_GUARD=PASS")
    print("PHASE174_R70_SOURCE_PINS=" + str(len(checked) + 1))
    print("PHASE174_R70_LOCAL_HEAD=" + head)
    print("PHASE174_R70_PATCH_STATUS=" + state)
    print("PHASE174_R70_NEW_GIVEN=0")
    print("PHASE174_R70_NEW_MATHEMATICAL_RULES=0")
    if args.dry_run:
        print("PHASE174_R70_PRODUCTION_CHANGES=0")
        print("PHASE174_R70_GATE=PASS_R70_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    if state == "PATCH_REQUIRED":
        target.write_bytes(after)
    write_full_formatter(root)
    print("PHASE174_R70_PRODUCTION_CHANGES=" + str(state == "PATCH_REQUIRED"))
    print("PHASE174_R70_GATE=PASS_R70_GENERAL_FORMATTER_PATCH_APPLIED_OR_PRESENT")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
