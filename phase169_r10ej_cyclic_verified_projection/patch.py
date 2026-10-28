"""R10EJ: narrowly edit the existing R10A display projection, never the proof engine."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

TARGET = Path("phase169_r10a_verified_stable_chain_projection/projection.py")
REVIEWED_GIT_BLOB = "c387b6a46d71561f8ecc2f2dc1d78158145dd883"
REVIEWED_SHA256 = "87cf6b32baccd15ed050181fd61ffb22c9461a87cd951526d71c644fe8a94117"

OLD_TEX = '''    source_tex, target_tex = element_tex(src.rhs.generator), element_tex(dst.rhs.generator)
    if not source_tex or not target_tex:
        return None
'''
NEW_TEX = '''    # A public LaTeX spelling is permitted only for the already-typed,
    # independently proven generator.  The public printer supplies notation,
    # never a missing GeneratorImage or a new mathematical inference.
    def display_generator_tex(generator):
        value = element_tex(generator)
        if value:
            return value
        from expression import Composition
        if not isinstance(generator, Composition):
            return None
        from toda_human_readable_renderer import render_toda_public_group_generator_latex
        return render_toda_public_group_generator_latex(generator)

    source_tex = display_generator_tex(src.rhs.generator)
    target_tex = display_generator_tex(dst.rhs.generator)
    if not source_tex or not target_tex:
        return None
'''
OLD_HIDDEN = '''    hidden = set(image_indices)
    # An eta-family suspension step can be shared by adjacent composite images.
    # Hide it only when ALL of its actual consumers are the collapsed images,
    # and the individual step has no direct citation to preserve.
    for index, candidate in enumerate(steps):
        if (index not in order or index == root_index
                or candidate.rule is not ProofRule.INFERENCE
                or not isinstance(candidate.conclusion, GeneratorSuspension)
                or model.step_citation_numbers[index]):
            continue
        consumers = {
            consumer_index
            for consumer_index, consumer in enumerate(steps)
            if any(parent is candidate for parent in consumer.premises)
        }
        if consumers and consumers.issubset(hidden):
            hidden.add(index)
'''
NEW_HIDDEN = '''    hidden = set(image_indices)
    # The image chain may use intermediate GeneratorImages and
    # GeneratorSuspensions for its factors (e.g. nu^2 or eta o mu).
    # Inspect ONLY ancestors of the root's independently proved images.
    # Hide a typed inference only when it has no own citation and every
    # consumer is already hidden (or the compressed root).  This fixed point
    # keeps shared or separately cited evidence visible, and never edits the
    # model or its actual dependencies.
    eligible_ancestors = set()
    pending = [premise for image_step in images for premise in image_step.premises]
    visited = set()
    while pending:
        ancestor = pending.pop()
        identity = id(ancestor)
        if identity in visited:
            continue
        visited.add(identity)
        index = by_identity.get(identity)
        if index is None or index not in order:
            return None
        if (index != root_index
                and ancestor.rule is ProofRule.INFERENCE
                and isinstance(ancestor.conclusion, (GeneratorImage, GeneratorSuspension))
                and not model.step_citation_numbers[index]):
            eligible_ancestors.add(index)
        pending.extend(ancestor.premises)

    changed = True
    while changed:
        changed = False
        for index in sorted(eligible_ancestors - hidden):
            ancestor = steps[index]
            consumers = {
                consumer_index
                for consumer_index, consumer in enumerate(steps)
                if any(parent is ancestor for parent in consumer.premises)
            }
            if consumers and consumers.issubset(hidden | {root_index}):
                hidden.add(index)
                changed = True
'''


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _full_function(source: str) -> str:
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "project_verified_stable_image_chain"]
    if len(functions) != 1:
        raise ValueError("Expected exactly one complete R10A projection function")
    node = functions[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def transform(data: bytes, *, require_reviewed: bool = True) -> tuple[bytes, str]:
    if not data or (b"\r\n" in data and b"\n" in data.replace(b"\r\n", b"")):
        raise ValueError("R10EJ refuses empty input or mixed line endings")
    newline = "\r\n" if b"\r\n" in data else "\n"
    canonical_bytes = data.replace(b"\r\n", b"\n")
    if require_reviewed and (
        _git_blob(canonical_bytes) != REVIEWED_GIT_BLOB
        or hashlib.sha256(canonical_bytes).hexdigest() != REVIEWED_SHA256
    ):
        raise RuntimeError("R10EJ requires the reviewed, unchanged GitHub R10A blob")
    canonical = canonical_bytes.decode("utf-8")
    if canonical.count(OLD_TEX) != 1 or canonical.count(OLD_HIDDEN) != 1:
        raise RuntimeError("R10EJ exact projection anchors changed: refusing patch")
    before_function = _full_function(canonical)
    modified = canonical.replace(OLD_TEX, NEW_TEX).replace(OLD_HIDDEN, NEW_HIDDEN)
    after_function = _full_function(modified)
    if before_function == after_function:
        raise AssertionError("R10EJ did not modify the target function")
    before_ast = ast.parse(canonical)
    after_ast = ast.parse(modified)
    def without_projection(tree):
        return [ast.dump(node, include_attributes=False)
                for node in tree.body
                if not (isinstance(node, ast.FunctionDef)
                        and node.name == "project_verified_stable_image_chain")]
    if without_projection(before_ast) != without_projection(after_ast):
        raise AssertionError("R10EJ changed code outside the one function")
    return modified.replace("\n", newline).encode("utf-8"), after_function
