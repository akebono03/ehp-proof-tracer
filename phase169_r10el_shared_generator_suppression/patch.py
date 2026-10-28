"""Exact-byte guarded R10EL patch for two existing presentation functions."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = (
    (
        "phase169_r10a_verified_stable_chain_projection/projection.py",
        "r10a_baseline.py", "r10a_projection.py.FULL",
    ),
    (
        "phase169_r10ec_direct_sum_narrative_projection/projection.py",
        "r10ec_baseline.py", "r10ec_projection.py.FULL",
    ),
)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _transform_cyclic(source: str) -> str:
    start = source.index("    hidden = set(image_indices)\n")
    end = source.index("    # Citations are copied from actual linked GIVEN ancestors", start)
    replacement = '''    # R10EL: use the shared, proof-preserving suppression contract.
    # The cyclic-specific root and single-generator chain checks above stay.
    from phase169_r10el_shared_generator_suppression.core import (
        exclusive_generator_inference_indices,
    )
    hidden = exclusive_generator_inference_indices(
        model, order, images, root_index, require_all=False,
    )
    if hidden is None:
        return None

'''
    return source[:start] + replacement + source[end:]


def _transform_direct_sum(source: str) -> str:
    start = source.index("    # Suppress ONLY inference equations consumed exclusively")
    end = source.index("    formulae: list[str] = []", start)
    replacement = '''    # R10EL: the shared strict contract preserves all-or-nothing direct-sum
    # suppression, including external-consumer and individual-citation checks.
    from phase169_r10el_shared_generator_suppression.core import (
        exclusive_generator_inference_indices,
    )
    hidden = exclusive_generator_inference_indices(
        model, order, image_steps, root_index, require_all=True,
    )
    if hidden is None:
        return None

'''
    # The existing given-source/citation walk remains above this section.
    result = source[:start] + replacement + source[end:]
    result = result.replace("hidden_indices=tuple(sorted(eligible)),",
                            "hidden_indices=tuple(sorted(hidden)),")
    result = result.replace("    ancestor_ids: set[int] = set()\n", "")
    result = result.replace("            ancestor_ids.add(index)\n", "")
    return result


def replace_checked(relative: str, payload: bytes) -> bytes:
    matched = [row for row in FILES if row[0] == relative]
    if len(matched) != 1:
        raise ValueError("not a reviewed R10EL patch target")
    _, old_name, full_name = matched[0]
    before = (ROOT / old_name).read_bytes()
    if payload != before:
        raise ValueError(f"unreviewed source bytes: {relative}")
    source = payload.decode("utf-8")
    if "r10a_" in relative:
        edited = _transform_cyclic(source)
    else:
        edited = _transform_direct_sum(source)
    ast.parse(edited)
    after = edited.encode("utf-8")
    if after != (ROOT / full_name).read_bytes():
        raise ValueError("full-file export differs from reviewed patch")
    return after


def apply(repo: Path, output: Path) -> list[tuple[Path, bytes]]:
    output.mkdir(parents=True, exist_ok=True)
    validated = []
    for relative, _, _ in FILES:
        target = repo / relative
        before = target.read_bytes()
        after = replace_checked(relative, before)
        validated.append((target, before, after))
    originals = []
    try:
        for target, before, after in validated:
            backup = output / (target.parent.name + "_" + target.name + ".before")
            backup.write_bytes(before)
            target.write_bytes(after)
            originals.append((target, before))
            print(f"R10EL_PATCHED={target}", flush=True)
        return originals
    except BaseException:
        for target, before in reversed(originals):
            target.write_bytes(before)
        raise
