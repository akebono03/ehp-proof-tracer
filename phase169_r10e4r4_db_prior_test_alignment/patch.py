"""R10E4R4: stage one parser payload and four historical test replacements.

No production files are mutated by this module. R10E4R2's guarded runner
later installs the single _has_explicit_row function and runs focused tests.
"""
from __future__ import annotations

import ast
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "output"
TARGETS = {
    "phase169_r10e2_unpositioned_citation/tests/test_r10e2_unpositioned_citation.py": {
        "test_r10e2_missing_publication_position_is_not_a_proof_source": "r10e2_FULL.py",
    },
    "phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py": {
        "test_r10e1_prior_citation_and_iso_required_for_direct_sum": "r10e1a_FULL.py",
        "test_r10e1_zero_citation_absence_not_inferred_from_db": "r10e1b_FULL.py",
        "test_r10e1_existing_finite_cyclic_route_keeps_compatibility": "r10e1c_FULL.py",
    },
}
R2_FN = "phase169_r10e4r2_explicit_db_row_parser/_has_explicit_row_FULL.py"


def function_bounds(text: str, fn: str) -> tuple[int, int, str]:
    tree = ast.parse(text)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == fn]
    if len(matches) != 1:
        raise RuntimeError("R10E4R4 unexpected test function count: " + fn)
    node = matches[0]
    lines = text.splitlines(keepends=True)
    start = sum(len(x) for x in lines[:node.lineno - 1])
    end = sum(len(x) for x in lines[:node.end_lineno])
    return start, end, text[start:end]


def transform(name: str, raw: bytes) -> tuple[bytes, dict[str, str]]:
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    replacements = TARGETS[name]
    originals = {}
    for fn, source in replacements.items():
        start, end, old = function_bounds(text, fn)
        new = (HERE / "full_functions" / source).read_text(encoding="utf-8")
        if new == old or "assert universal.expand_prior_general_group_transport(" not in old and "assert expand_prior_general_group_transport(" not in old:
            raise RuntimeError("R10E4R4 expected unmodified historical test: " + fn)
        originals[fn] = old
        text = text[:start] + new + text[end:]
    ast.parse(text)
    data = text.encode("utf-8")
    return (data.replace(b"\n", b"\r\n") if crlf else data), originals


def stage() -> None:
    specs = []
    for name in TARGETS:
        path = ROOT / name
        if not path.is_file():
            raise RuntimeError("R10E4R4 missing test: " + name)
        before = path.read_bytes()
        after, originals = transform(name, before)
        specs.append((name, path, before, after, originals))
    payload = ROOT / R2_FN
    if not payload.is_file():
        raise RuntimeError("R10E4R4 missing R10E4R2 function payload")
    old_payload = payload.read_bytes()
    expected = b"if int(raw_n) == n and int(raw_k) == k:"
    if expected not in old_payload:
        raise RuntimeError("R10E4R4 unrecognized R10E4R2 payload")
    new_payload = (HERE / "full_functions/_has_explicit_row_FULL.py").read_bytes()
    ast.parse(new_payload.decode("utf-8"))
    if new_payload == old_payload:
        raise RuntimeError("R10E4R4 parser payload is already updated")
    specs.append((R2_FN, payload, old_payload, new_payload, {}))
    OUT.mkdir(exist_ok=True)
    # Preflight all inputs before writing anything.
    for name, path, before, after, originals in specs:
        prefix = name.replace("/", "__")
        (OUT / (prefix + ".before")).write_bytes(before)
        (OUT / (prefix + ".FULL")).write_bytes(after)
        for fn, old in originals.items():
            (OUT / (fn + "_BEFORE.py")).write_text(old, encoding="utf-8")
            print("R10E4R4_FULL_TEST_FUNCTION=" + str(HERE / "full_functions" / TARGETS[name][fn]))
        print("R10E4R4_PATCH_TARGET=" + str(path))
    for name, path, before, after, originals in specs:
        path.write_bytes(after)
    print("R10E4R4_STAGE_COUNT=" + str(len(specs)))


if __name__ == "__main__":
    stage()
