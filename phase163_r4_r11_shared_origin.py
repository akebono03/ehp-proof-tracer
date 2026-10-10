"""Read-only shared-ancestry identity inventory for Phase 163 R4-R11."""
from __future__ import annotations

from dataclasses import dataclass

from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class MissingOrigin:
    ordinal: int
    paths: tuple[str, ...]
    components: tuple[str, ...]
    conclusion_type: str
    conclusion_repr: str
    inference_rule_name: str | None
    proof_note: str | None
    has_inference_rule: bool
    premise_count: int
    issue: str


def find_missing_origins(witnesses: tuple[tuple[str, ProofStep], ...]) -> tuple[MissingOrigin, ...]:
    """Group missing inference ancestry by Python object identity across witnesses.

    Report paths per witness even if a DAG has repeated references. No steps,
    premises, trust boundaries or registry records are modified.
    """
    observations: dict[int, dict[str, object]] = {}
    for component, root in witnesses:
        if not isinstance(root, ProofStep):
            raise TypeError("witness root must be a ProofStep")
        active: set[int] = set()

        def walk(node: ProofStep, path: str) -> None:
            identity = id(node)
            if identity in active:
                return
            active.add(identity)
            try:
                if node.rule is ProofRule.INFERENCE and (
                    not node.premises or node.inference_rule is None
                ):
                    record = observations.setdefault(identity, {"node": node, "paths": [], "components": []})
                    record["paths"].append(f"{component}:{path}")
                    if component not in record["components"]:
                        record["components"].append(component)
                for index, child in enumerate(node.premises):
                    if isinstance(child, ProofStep):
                        walk(child, f"{path}/premise[{index}]")
            finally:
                active.remove(identity)

        walk(root, "root")

    result: list[MissingOrigin] = []
    for position, record in enumerate(observations.values(), start=1):
        node = record["node"]
        assert isinstance(node, ProofStep)
        rule = node.inference_rule
        reasons = []
        if not node.premises:
            reasons.append("INFERENCE_PREMISES_MISSING")
        if rule is None:
            reasons.append("INFERENCE_RULE_MISSING")
        result.append(MissingOrigin(
            ordinal=position,
            paths=tuple(record["paths"]),
            components=tuple(record["components"]),
            conclusion_type=type(node.conclusion).__name__,
            conclusion_repr=repr(node.conclusion),
            inference_rule_name=rule.name if rule is not None else None,
            proof_note=node.note,
            has_inference_rule=rule is not None,
            premise_count=len(node.premises),
            issue=" + ".join(reasons),
        ))
    return tuple(result)
