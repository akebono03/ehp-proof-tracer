"""Exact-source, minimal root-reachable citation scope patch for R10ET-R6C."""
from __future__ import annotations

import hashlib
from pathlib import Path

MODEL = "phase168_r3_3_proof_narrative_model.py"
RENDERER = "phase168_r3_5_model_renderer.py"
EXPECTED_GIT_BLOBS = {
    MODEL: "1080843a2a90bf60f0b8096d3c5542a24a9abb7c",
    RENDERER: "6694fa68205628d5bd870a08f38b1d4df2d45681",
}

ROOT_HELPER = '''def root_ancestor_step_indices(
    steps: tuple[ProofStep, ...], root_index: int,
) -> frozenset[int]:
    """Find exact ProofStep ancestors of the completed root, without inferring facts."""
    if type(root_index) is not int or not 0 <= root_index < len(steps):
        raise ValueError("complete proof requires a valid root index")
    identities = {id(step): index for index, step in enumerate(steps)}
    if len(identities) != len(steps):
        raise ValueError("duplicate ProofStep identities")
    visited: set[int] = set()
    pending = [root_index]
    while pending:
        index = pending.pop()
        if index in visited:
            continue
        visited.add(index)
        for premise in steps[index].premises:
            source = identities.get(id(premise))
            if source is None:
                matches = [i for i, step in enumerate(steps) if step == premise]
                if len(matches) != 1:
                    raise ValueError("missing or ambiguous ProofStep premise")
                source = matches[0]
            pending.append(source)
    return frozenset(visited)


'''


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def replace_once(source: str, needle: str, replacement: str, name: str) -> str:
    if source.count(needle) != 1:
        raise RuntimeError(f"{name}: expected one exact anchor, got {source.count(needle)}")
    return source.replace(needle, replacement, 1)


def patch_model(source: str) -> str:
    source = replace_once(source,
        "def build_proof_narrative_model(\n", ROOT_HELPER + "def build_proof_narrative_model(\n", "model helper")
    needle = '''    # Locator is the printed source position. Labels are presentation metadata,
'''
    replacement = '''    # Complete proofs cite only the actual final-root ancestry. Preserve all
    # steps and the full (including unrelated) verified search record.
    citation_scope = (
        root_ancestor_step_indices(steps, root_index)
        if result.status is ProofSearchStatus.COMPLETE
        else frozenset(range(len(steps)))
    )
    # Locator is the printed source position. Labels are presentation metadata,
'''
    source = replace_once(source, needle, replacement, "model citation scope")
    needle = '''    for step_index, step in enumerate(steps):
        linked: list[tuple[LiteratureReference, str | None, str | None]] = []
'''
    replacement = '''    for step_index, step in enumerate(steps):
        if step_index not in citation_scope:
            per_step.append(())
            continue
        linked: list[tuple[LiteratureReference, str | None, str | None]] = []
'''
    return replace_once(source, needle, replacement, "model unused citations")


def patch_renderer(source: str) -> str:
    needle = '''    from phase168_r3_29_order_projection import project_narrative_order
'''
    replacement = '''    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
'''
    source = replace_once(source, needle, replacement, "renderer function import")
    needle = '''    else:
        chains = project_exactness_chains(model)
        suppressed_exactness = {index for chain in chains for index in chain.step_indices}
        order = tuple(entry.step_index for entry in project_narrative_order(model, suppressed_exactness))
        lines = ["使用する結果", ""]
'''
    replacement = '''    else:
        root_scope = root_ancestor_step_indices(model.steps, model.root_index)
        chains = tuple(
            chain for chain in project_exactness_chains(model)
            if all(index in root_scope for index in chain.step_indices)
        )
        suppressed_exactness = {index for chain in chains for index in chain.step_indices}
        order = tuple(
            entry.step_index
            for entry in project_narrative_order(model, suppressed_exactness)
            if entry.step_index in root_scope
        )
        lines = ["使用する結果", ""]
'''
    return replace_once(source, needle, replacement, "renderer completed order")


def transform(path: str, original: bytes) -> bytes:
    expected = EXPECTED_GIT_BLOBS[path]
    observed = git_blob(original)
    if observed != expected:
        raise RuntimeError(f"source guard failed for {path}: {observed} != {expected}")
    newline = "\r\n" if b"\r\n" in original else "\n"
    source = original.decode("utf-8").replace("\r\n", "\n")
    changed = patch_model(source) if path == MODEL else patch_renderer(source)
    result = changed.replace("\n", newline).encode("utf-8")
    if result == original:
        raise RuntimeError(f"patch had no effect: {path}")
    compile(result.decode("utf-8"), path, "exec")
    return result


def extract_whole_function(raw: bytes, name: str) -> str:
    """Export a complete replacement-sized source function, never a diff."""
    lines = raw.decode("utf-8").splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if line.startswith(f"def {name}(")]
    if len(matches) != 1:
        raise RuntimeError(f"function {name}: expected exactly one definition")
    start = matches[0]
    after = next((i for i in range(start + 1, len(lines))
                  if lines[i].startswith("def ") or lines[i].startswith("class ")),
                 len(lines))
    return "".join(lines[start:after])
