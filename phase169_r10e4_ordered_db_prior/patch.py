"""Guarded, reversible Phase 169 R10E4 patch; writes full functions and files."""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "output"
TARGETS = (
    "phase165_r3_recursive_search.py",
    "phase168_r3_41p13_trust_boundary/verification.py",
    "phase169_r10e1_general_group_transport/transport.py",
)


def _extract_function(text: str, name: str) -> tuple[int, int, str]:
    tree = ast.parse(text)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError(f"expected one full function {name}")
    rows = text.splitlines(keepends=True)
    node = matches[0]
    start = sum(len(line) for line in rows[:node.lineno - 1])
    end = sum(len(line) for line in rows[:node.end_lineno])
    return start, end, text[start:end]


def _one(original: str, old: str, new: str, context: str) -> str:
    if original.count(old) != 1 or new in original:
        raise RuntimeError("R10E4 guarded anchor mismatch: " + context)
    return original.replace(old, new, 1)


def transform(name: str, raw: bytes) -> tuple[bytes, dict[str, str]]:
    crlf = b"\r\n" in raw
    if raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R10E4 does not rewrite files with BOM")
    original = raw.decode("utf-8").replace("\r\n", "\n")
    if name == TARGETS[0]:
        start, end, body = _extract_function(original, "reconstruct_registered_goal")
        anchor = '            if (not bound and lookup_mode in ("typed_reference", "typed_reference_ordered", "typed_reference_publication")\n'
        injection = (
            '            # R10E4: DB results earlier in (stem, sphere dimension) are\n'
            '            # explicit adopted premises, not fabricated Toda citations.\n'
            '            # Prefer existing admitted literature leaves where present.\n'
            '            if (not bound and not options and lookup_mode in\n'
            '                    ("typed_reference", "typed_reference_ordered", "typed_reference_publication")):\n'
            '                from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step\n'
            '                db_step = admitted_db_step(actual, proof_target=goal, bridge=bridge)\n'
            '                if db_step is not None:\n'
            '                    options.append(db_step)\n'
        )
        newbody = _one(body, anchor, injection + anchor, name)
        functions = {"reconstruct_registered_goal": newbody}
    elif name == TARGETS[1]:
        start, end, body = _extract_function(original, "verify_proof_tree_for_narrative")
        anchor = '                accepted = False\n                for link in bridge.proof_links:\n'
        replacement = (
            '                # R10E4: the DB assumption is authenticated by a fresh\n'
            '                # exact-row read and the target-dependent lexicographic gate.\n'
            '                # It is NOT promoted to a Toda FIXED_STATEMENT.\n'
            '                from phase169_r10e4_ordered_db_prior.db_prior import verified_db_step\n'
            '                accepted = verified_db_step(\n'
            '                    step, proof_target=result.conclusion, bridge=bridge,\n'
            '                )\n'
            '                for link in bridge.proof_links:\n'
        )
        newbody = _one(body, anchor, replacement, name)
        functions = {"verify_proof_tree_for_narrative": newbody}
    elif name == TARGETS[2]:
        start, end, body = _extract_function(original, "expand_prior_general_group_transport")
        # Previously, having a cited target suppressed DB-prior fallback.
        # Citation registration now affects annotation, not DB order.
        body = _one(body, '        if citing_id is not None or legacy:\n            return legacy\n',
                    '        if legacy:\n            return legacy\n', name)
        anchor = '        if source is None:\n            continue\n        images = generator_images_for_group_transport(source, goal)\n'
        replacement = (
            '        if source is None:\n'
            '            # The root may cite no proposition. Adopt an explicitly\n'
            '            # stored earlier DB structure, never a synthetic stable fallback.\n'
            '            from phase169_r10e4_ordered_db_prior.db_prior import (\n'
            '                exact_prior_database_result, precedes_db_goal,\n'
            '            )\n'
            '            if precedes_db_goal(source_n, k, n, k):\n'
            '                source = exact_prior_database_result(source_n, k)\n'
            '        if source is None:\n'
            '            continue\n'
            '        images = generator_images_for_group_transport(source, goal)\n'
        )
        newbody = _one(body, anchor, replacement, name)
        functions = {"expand_prior_general_group_transport": newbody}
    else:
        raise RuntimeError("unknown source target: " + name)
    updated = original[:start] + newbody + original[end:]
    if updated == original:
        raise RuntimeError("no modification performed")
    ast.parse(updated)
    data = updated.encode("utf-8")
    if crlf:
        data = data.replace(b"\n", b"\r\n")
    return data, functions


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    stage = []
    for name in TARGETS:
        path = ROOT / name
        original = path.read_bytes()
        updated, functions = transform(name, original)
        stage.append((name, path, original, updated, functions))
    # Preflight every source BEFORE writing any production file.
    for name, path, original, updated, funcs in stage:
        filename = path.name
        (OUTPUT / (filename + ".before")).write_bytes(original)
        (OUTPUT / (filename + ".FULL")).write_bytes(updated)
        for fun, code in funcs.items():
            (OUTPUT / (fun + "_FULL.py")).write_text(code, encoding="utf-8")
            print("R10E4_FULL_FUNCTION=" + str(OUTPUT / (fun + "_FULL.py")))
        print("R10E4_FULL_FILE=" + str(OUTPUT / (filename + ".FULL")))
    for name, path, original, updated, funcs in stage:
        path.write_bytes(updated)
        print("R10E4_PATCHED=" + str(path))
    print("R10E4_PATCH_COUNT=" + str(len(stage)))


if __name__ == "__main__":
    main()
