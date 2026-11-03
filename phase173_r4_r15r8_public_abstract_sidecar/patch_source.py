"""Small, source-guarded changes to the canonical public result model and selector."""
from __future__ import annotations

import ast


ABSTRACT_CLASS = '''@dataclass(frozen=True)
class CertifiedAbstractStructure:
    """Verified abstract invariants, separate from a named group conclusion."""
    group: TodaPrimaryGroup
    invariant_summands: tuple[tuple[str, int], ...]
    proof_step: ProofStep

    def __post_init__(self) -> None:
        from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
            TodaProp44AbstractGroupResult,
        )
        if not isinstance(self.group, TodaPrimaryGroup):
            raise TypeError("abstract certificate must have a typed target group")
        expected = TodaProp44AbstractGroupResult(
            self.group, self.invariant_summands,
        )
        if (not isinstance(self.proof_step, ProofStep)
                or self.proof_step.rule is not ProofRule.INFERENCE
                or self.proof_step.conclusion != expected
                or self.proof_step.inference_rule is None
                or not callable(self.proof_step.inference_rule.match_guard)
                or not self.proof_step.inference_rule.match_guard(
                    self.proof_step.premises, (),
                )):
            raise ValueError("abstract certificate has no verified inference root")


'''

MODEL_FIELD = '    abstract_structure: CertifiedAbstractStructure | None = None\n'
MODEL_GUARD = '''        if self.abstract_structure is not None:
            if (not isinstance(self.abstract_structure, CertifiedAbstractStructure)
                    or self.abstract_structure.group != self.target
                    or self.status not in (
                        ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED,
                    )
                    or self.conclusion is not None
                    or self.structure_status is GroupStructureStatus.KNOWN):
                raise ValueError(
                    "abstract-only evidence cannot certify a named group"
                )
'''

ORDER_BRANCH = '''        if order_diagnostic is not None:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=(order_diagnostic,),
            )
'''
ORDER_REPLACEMENT = '''        if order_diagnostic is not None:
            pending = make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=(order_diagnostic,),
            )
            if n == 4 and k >= 3:
                from phase173_r4_r15r8_public_abstract_sidecar.attach import (
                    attach_certified_abstract_structure,
                )
                return attach_certified_abstract_structure(
                    pending, n=n, k=k, goal=candidate, bridge=bridge,
                )
            return pending
'''
END_BRANCH = '''    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result
'''
END_REPLACEMENT = '''    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    if n == 4 and k >= 3:
        from phase173_r4_r15r8_public_abstract_sidecar.attach import (
            attach_certified_abstract_structure,
        )
        return attach_certified_abstract_structure(
            result, n=n, k=k, goal=candidate, bridge=bridge,
        )
    return result
'''


def _eol(source: bytes) -> str:
    text = source.decode("utf-8-sig")
    if "\r\n" in text and text.count("\r\n") == text.count("\n"):
        return "\r\n"
    if "\r\n" in text:
        raise RuntimeError("Mixed source line endings require review")
    return "\n"


def _replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise RuntimeError("Reviewed production anchor absent or ambiguous: " + repr(old[:80]))
    return source.replace(old, new, 1)


def transform_model(source: bytes) -> bytes:
    eol = _eol(source)
    text = source.decode("utf-8-sig").replace("\r\n", "\n")
    if text.count("@dataclass(frozen=True)\nclass PartialProofResult:") != 1:
        raise RuntimeError("Reviewed result class not found")
    if "class CertifiedAbstractStructure:" in text or "abstract_structure:" in text:
        raise RuntimeError("Result model already contains an abstract sidecar")
    text = _replace_once(text, "from proof import ProofStep\n",
                         "from proof import ProofRule, ProofStep\n")
    text = _replace_once(text, "@dataclass(frozen=True)\nclass PartialProofResult:",
                         ABSTRACT_CLASS + "@dataclass(frozen=True)\nclass PartialProofResult:")
    text = _replace_once(text, "    conclusion: Any | None = None\n",
                         "    conclusion: Any | None = None\n" + MODEL_FIELD)
    anchor = '        if self.status is ProofSearchStatus.NOT_SEARCHED and self.proven_steps:\n'
    text = _replace_once(text, anchor, MODEL_GUARD + anchor)
    ast.parse(text)
    return text.replace("\n", eol).encode("utf-8")


def transform_selector(source: bytes) -> bytes:
    eol = _eol(source)
    text = source.decode("utf-8-sig").replace("\r\n", "\n")
    if "attach_certified_abstract_structure" in text:
        raise RuntimeError("Selector already has abstract attachment logic")
    text = _replace_once(text, ORDER_BRANCH, ORDER_REPLACEMENT)
    text = _replace_once(text, END_BRANCH, END_REPLACEMENT)
    ast.parse(text)
    return text.replace("\n", eol).encode("utf-8")


def full_replacement_units(original_model: bytes, original_selector: bytes) -> str:
    """Emit complete reviewed classes and complete changed selector function."""
    model = ast.parse(transform_model(original_model).decode("utf-8-sig"))
    selector = ast.parse(transform_selector(original_selector).decode("utf-8-sig"))
    model_text = transform_model(original_model).decode("utf-8-sig").replace("\r\n", "\n")
    selector_text = transform_selector(original_selector).decode("utf-8-sig").replace("\r\n", "\n")
    chunks = []
    for node in model.body:
        if isinstance(node, ast.ClassDef) and node.name in ("CertifiedAbstractStructure", "PartialProofResult"):
            # Include the entire decorated class, including class-level import annotations.
            lines = model_text.splitlines(keepends=True)
            start = min((d.lineno for d in node.decorator_list), default=node.lineno)
            chunks.append((node.name, "".join(lines[start-1:node.end_lineno])))
    for node in selector.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "search_group_from_registered_goal":
            lines = selector_text.splitlines(keepends=True)
            chunks.append((node.name, "".join(lines[node.lineno-1:node.end_lineno])))
    if len(chunks) != 3:
        raise RuntimeError("Could not extract all three complete replacement units")
    return "".join("### `" + name + "`\n\n```python\n" + body + "```\n\n" for name,body in chunks)
