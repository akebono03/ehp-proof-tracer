"""R3Z: guarded in-place whole-function update, with byte-preserving rollback."""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parent
TARGET = Path("phase168_r3_5_model_renderer.py")
OUTPUT = PACKAGE / "output"
META = OUTPUT / "installed.json"
OLD_ANCHOR = "        # Only verbalize the certified stable-eta normalization already\n"
PATCH_TAG = "        # R3Z: general higher-eta clauses belong to Reference, not the proof body.\n"

ADDITION = """        # R3Z: general higher-eta clauses belong to Reference, not the proof body.
        # Hide one only when a directly dependent certified specialization is
        # retained in this display. The citation and both ProofSteps survive.
        if (step.rule is ProofRule.GIVEN
                and isinstance(statement, Relation)
                and model.step_citation_numbers[index]):
            from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
            from phase165_r57_r20_general_specialization import specialize_typed_statement
            if (_is_generic_eta_group_relation(statement)
                    and any(
                        derived_index not in suppressed_body_indices
                        and derived_index != index
                        and derived.rule is ProofRule.INFERENCE
                        and isinstance(derived.conclusion, Relation)
                        and any(parent is step or parent == step
                                for parent in derived.premises)
                        and specialize_typed_statement(
                            statement, derived.conclusion
                        ) is not None
                        for derived_index in order
                        for derived in (model.steps[derived_index],)
                    )):
                continue
"""


def function_span(source: str, name: str):
    tree = ast.parse(source)
    candidates = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                  and node.name == name]
    if len(candidates) != 1:
        raise ValueError("Missing unique renderer function: " + name)
    node = candidates[0]
    return node.lineno, node.end_lineno


def transform(source: str) -> tuple[str, str]:
    name = "render_model_backed_narrative_markdown"
    start, end = function_span(source, name)
    rows = source.splitlines(keepends=True)
    whole = "".join(rows[start - 1:end])
    if PATCH_TAG not in whole:
        if whole.count(OLD_ANCHOR) != 1:
            raise RuntimeError("Renderer expected insertion anchor missing or ambiguous")
        if ("step.rule is ProofRule.GIVEN" not in whole
                or "# A cited symbolic diagonal GIVEN" not in whole
                or "direct_given_premise_citation_numbers" not in whole):
            raise RuntimeError("Renderer narrative contract changed; refusing patch")
        whole = whole.replace(OLD_ANCHOR, ADDITION + OLD_ANCHOR, 1)
    elif whole.count(PATCH_TAG) != 1:
        raise RuntimeError("Renderer patch marker duplicated")
    ast.parse(whole)
    rows[start - 1:end] = [whole]
    changed = "".join(rows)
    ast.parse(changed)
    return changed, whole


def encode_with_style(original: bytes, changed_normal: str) -> bytes:
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    content = original.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in content else "\n"
    return bom + changed_normal.replace("\n", newline).encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def install() -> None:
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=REPOSITORY,
        text=True, encoding="utf8"
    ).strip()
    print("R3Z_GIT_BRANCH=" + branch)
    if branch != "develop":
        raise RuntimeError("R3Z requires develop branch")
    location = REPOSITORY / TARGET
    if not location.is_file():
        raise FileNotFoundError(location)
    before_bytes = location.read_bytes()
    before_text = before_bytes.decode("utf-8-sig")
    original_normal = before_text.replace("\r\n", "\n")
    new_normal, full_function = transform(original_normal)
    new_bytes = encode_with_style(before_bytes, new_normal)
    if META.is_file():
        previous = json.loads(META.read_text(encoding="utf8"))
        if digest(before_bytes) == previous["after"]:
            print("R3Z_ALREADY_INSTALLED=True")
            return
        raise RuntimeError("Prior R3Z installation or different working tree detected")
    if new_bytes == before_bytes:
        raise RuntimeError("R3Z code already patched without installation record")
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / (TARGET.name + ".before")).write_bytes(before_bytes)
    (OUTPUT / (TARGET.name + ".FULL.py")).write_bytes(new_bytes)
    full_path = OUTPUT / "render_model_backed_narrative_markdown_FULL.py"
    full_path.write_text(full_function, encoding="utf8")
    META.write_text(json.dumps({
        "target":str(TARGET), "before":digest(before_bytes),"after":digest(new_bytes)
    },indent=2)+"\n",encoding="utf8")
    location.write_bytes(new_bytes)
    print("R3Z_PATCHED=" + str(TARGET))
    print("R3Z_FULL_FUNCTION=" + str(full_path))
    print("R3Z_FULL_FILE=" + str(OUTPUT / (TARGET.name + ".FULL.py")))
    print("R3Z_BACKUP=" + str(OUTPUT / (TARGET.name + ".before")))


def restore() -> None:
    if not META.is_file():
        raise RuntimeError("No R3Z installation recorded")
    meta = json.loads(META.read_text(encoding="utf8"))
    location = REPOSITORY / meta["target"]
    if digest(location.read_bytes()) != meta["after"]:
        raise RuntimeError("Refusing rollback: file modified after R3Z installation")
    original = OUTPUT / (TARGET.name + ".before")
    old = original.read_bytes()
    if digest(old) != meta["before"]:
        raise RuntimeError("Rollback backup damaged")
    location.write_bytes(old)
    META.unlink()
    print("R3Z_RESTORED=" + meta["target"])


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("install", "restore"):
        raise SystemExit("Usage: install.py install|restore")
    globals()[sys.argv[1]]()
