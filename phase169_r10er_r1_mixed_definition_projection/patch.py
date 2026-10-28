"""Guarded, exact full-function replacement with saved full sources."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "phase169_r10ec_direct_sum_narrative_projection" / "projection.py"
GIT_BLOB_SHA1 = "977797156cecf3b948016f690bbb72f34e22d636"
OLD = '''    # R10EN: each direct-sum image needs its own registered GIVEN ancestor.
    from phase169_r10en_shared_citation_provenance.core import (
        verified_generator_image_citation_numbers,
    )
    numbers = verified_generator_image_citation_numbers(
        model, order, image_steps, require_each=True,
    )
    if numbers is None:
        return None
'''
NEW = '''    # R10ER: a typed stable Definition inference has no literature GIVEN.
    # All other image paths retain R10EN's every-image citation requirement.
    from phase169_r10eq_r1_universal_stable_definition.definition import (
        expand_defined_stable_element_image,
    )
    from phase169_r10en_shared_citation_provenance.core import (
        verified_generator_image_citation_numbers,
    )
    from proof import InferenceRule, find_inference_matches_for_rule

    def is_certified_definition_image(step):
        if (step.rule is not ProofRule.INFERENCE or step.premises
                or not isinstance(step.inference_rule, InferenceRule)):
            return False
        proposals = expand_defined_stable_element_image(step.conclusion)
        if len(proposals) != 1 or proposals[0].subgoals:
            return False
        actual = step.inference_rule
        canonical = proposals[0].rule
        return (
            actual.name == canonical.name
            and actual.description == canonical.description
            and actual.premise_patterns == canonical.premise_patterns == ()
            and actual.conclusion_pattern == canonical.conclusion_pattern
            and actual.conclusion_builder is None
            and actual.literature_reference is None
            and len(find_inference_matches_for_rule(actual, ())) == 1
        )

    cited_image_steps = tuple(
        step for step in image_steps if not is_certified_definition_image(step)
    )
    if cited_image_steps:
        numbers = verified_generator_image_citation_numbers(
            model, order, cited_image_steps, require_each=True,
        )
        if numbers is None:
            return None
    else:
        # The root's independently cited source and (4.5) remain mandatory.
        # Never manufacture a citation for a definition-only image chain.
        if not getattr(model, "citations", ()):
            return None
        numbers = ()
'''
OLD_STATEMENT = '''    labels = ", ".join(f"[R{number}]" for number in numbers)
    statement = f"{labels}より, " + "、".join(formulae) + "."
'''
NEW_STATEMENT = '''    labels = ", ".join(f"[R{number}]" for number in numbers)
    if len(cited_image_steps) == len(image_steps):
        # Unchanged output for all earlier fully cited direct-sum proofs.
        prefix = f"{labels}より, "
    elif labels:
        prefix = f"Definition と {labels} より, "
    else:
        prefix = "Definition より, "
    statement = prefix + "、".join(formulae) + "."
'''


def git_blob_hash(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def function_span(source: str, name: str) -> tuple[int, int]:
    marker = f"def {name}("
    if source.count(marker) != 1:
        raise RuntimeError(f"function not unique: {name}")
    start = source.index(marker)
    next_def = source.find("\ndef ", start + len(marker))
    return start, len(source) if next_def == -1 else next_def + 1


def replacement_content(original: bytes) -> tuple[bytes, str]:
    if git_blob_hash(original) != GIT_BLOB_SHA1:
        raise RuntimeError("inspected projection Git blob SHA1 differs")
    text = original.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    normalized = text.replace("\r\n", "\n")
    begin, end = function_span(normalized, "project_verified_direct_sum_transport")
    old_func = normalized[begin:end]
    if (old_func.count(OLD) != 1 or old_func.count(OLD_STATEMENT) != 1):
        raise RuntimeError("reviewed projection anchors changed")
    new_func = old_func.replace(OLD, NEW).replace(OLD_STATEMENT, NEW_STATEMENT)
    patched = (normalized[:begin] + new_func + normalized[end:]).replace("\n", newline)
    return patched.encode("utf-8"), new_func


def apply_patch(out: Path) -> None:
    original = TARGET.read_bytes()
    modified, function = replacement_content(original)
    out.mkdir(parents=True, exist_ok=True)
    backup = out / "projection.py.before"
    backup.write_bytes(original)
    (out / "project_verified_direct_sum_transport_FULL.py").write_text(function, encoding="utf-8")
    (out / "projection.py.FULL").write_bytes(modified)
    TARGET.write_bytes(modified)
    print("R10ER_PATCHED=phase169_r10ec_direct_sum_narrative_projection/projection.py", flush=True)
    print("R10ER_BACKUP=" + str(backup), flush=True)
    print("R10ER_FULL_FUNCTION=" + str(out / "project_verified_direct_sum_transport_FULL.py"), flush=True)
    print("R10ER_FULL_FILE=" + str(out / "projection.py.FULL"), flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m phase169_r10er_r1_mixed_definition_projection.patch OUTPUT")
    apply_patch(Path(sys.argv[1]))
