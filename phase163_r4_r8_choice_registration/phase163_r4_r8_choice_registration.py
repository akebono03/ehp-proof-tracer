"""Phase 163 R4-R8: retain typed literature choice without asserting proof.

The (5.3) nu-prime bracket membership is a source-claimed selection, not
an inference or a mathematically verified external statement.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from expression import HomotopyElement, Multiple, TodaBracket
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult, build_registry_bridge
from proof import ProofRule, ProofStep
from toda_rules import TodaBracketMembershipStatement


@dataclass(frozen=True)
class LiteratureChoice:
    """Typed selection with explicit, intentionally unverified provenance."""

    assertion_id: str
    reference_locator: str
    component_key: str
    defined_symbol: str
    statement: TodaBracketMembershipStatement
    source_step: ProofStep
    provenance: str = "source_claimed_not_independently_verified"

    def __post_init__(self) -> None:
        if self.provenance != "source_claimed_not_independently_verified":
            raise ValueError("unsupported provenance: verification must not be invented")
        if self.assertion_id != f"boundary:{self.reference_locator}:{self.component_key}":
            raise ValueError("assertion identity mismatch")
        if not isinstance(self.statement, TodaBracketMembershipStatement):
            raise TypeError("statement must be a TodaBracketMembershipStatement")
        if not isinstance(self.source_step, ProofStep):
            raise TypeError("source_step must be ProofStep")
        if self.source_step.rule is not ProofRule.GIVEN or self.source_step.premises:
            raise ValueError("choice must have a leaf GIVEN source; derived facts need R6/R7")
        if self.source_step.conclusion != self.statement:
            raise ValueError("choice statement differs from source step")
        if not self.defined_symbol:
            raise ValueError("defined_symbol required")


@dataclass(frozen=True)
class ChoiceSnapshot:
    """A parallel typed declaration catalog; no citation permission granted."""

    bridge: RegistryBridgeResult
    choices: tuple[LiteratureChoice, ...]

    def find(self, assertion_id: str) -> LiteratureChoice:
        return next(choice for choice in self.choices if choice.assertion_id == assertion_id)


def register_literature_choices(
    base: RegistryBridgeResult,
    choices: tuple[LiteratureChoice, ...],
) -> ChoiceSnapshot:
    """Validate identities and record typed choices without promoting bridge statuses."""
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    if not isinstance(choices, tuple):
        raise TypeError("choices must be a tuple")
    allowed = {
        record.assertion_id for record in base.records
        if record.source == "boundary" and record.status is MigrationStatus.METADATA_ONLY
    }
    seen: set[str] = set()
    for choice in choices:
        if not isinstance(choice, LiteratureChoice):
            raise TypeError("choices must contain LiteratureChoice")
        if choice.assertion_id not in allowed:
            raise ValueError(f"not an eligible boundary: {choice.assertion_id}")
        if choice.assertion_id in seen:
            raise ValueError(f"duplicate choice: {choice.assertion_id}")
        seen.add(choice.assertion_id)
        if base.registry.reference(f"toda:{choice.reference_locator}").locator != choice.reference_locator:
            raise ValueError("reference locator mismatch")
    return ChoiceSnapshot(bridge=base, choices=choices)


def nu_prime_bracket_matches(statement: TodaBracketMembershipStatement) -> bool:
    """Check structural fields; never infer truth of the mathematical relation."""
    if not isinstance(statement, TodaBracketMembershipStatement):
        return False
    element = statement.element
    bracket = statement.bracket
    if not isinstance(element, HomotopyElement) or not isinstance(bracket, TodaBracket):
        return False
    if not isinstance(bracket.first, HomotopyElement) or not isinstance(bracket.third, HomotopyElement):
        return False
    second = bracket.second
    if not isinstance(second, Multiple) or not isinstance(second.expression, HomotopyElement):
        return False
    elements = (element, bracket.first, second.expression, bracket.third)
    generators = tuple(x.generator for x in elements)
    return (
        element.name == "ν′"
        and element.source == 6 and element.target == 3
        and generators[0] is not None and generators[0].family == "ν" and generators[0].decoration == "′"
        and generators[1] is not None and generators[1].family == "η" and generators[1].index == 3
        and second.coefficient == 2
        and generators[2] is not None and generators[2].family == "ι" and generators[2].index == 4
        and generators[3] is not None and generators[3].family == "η" and generators[3].index == 4
        and bracket.index == 1
    )


def build_nu_prime_choice(base: RegistryBridgeResult, source_step: ProofStep) -> ChoiceSnapshot:
    """Use the existing bracket GIVEN directly, without replacing it with a proof."""
    if not isinstance(source_step, ProofStep):
        raise TypeError("source_step must be ProofStep")
    if not nu_prime_bracket_matches(source_step.conclusion):
        raise ValueError("source is not nu-prime in {eta_3, 2 iota_4, eta_4}_1")
    choice = LiteratureChoice(
        assertion_id="boundary:(5.3):nu_prime_bracket_definition",
        reference_locator="(5.3)",
        component_key="nu_prime_bracket_definition",
        defined_symbol="ν′",
        statement=source_step.conclusion,
        source_step=source_step,
    )
    return register_literature_choices(base, (choice,))


def run_audit(output_dir: Path) -> dict[str, object]:
    from probes.probe_phase58_capabilities import build_phase58_representative_result

    base = build_registry_bridge()
    representative = build_phase58_representative_result()
    snapshot = build_nu_prime_choice(base, representative["bracket_membership_step"])
    choice = snapshot.choices[0]
    record = next(record for record in base.records if record.assertion_id == choice.assertion_id)
    report = {
        "phase": "163 R4-R8",
        "reference_locator": choice.reference_locator,
        "component_key": choice.component_key,
        "defined_symbol": choice.defined_symbol,
        "expression": "nu_prime in {eta_3, 2 iota_4, eta_4}_1",
        "typed_bracket_index": choice.statement.bracket.index,
        "status": "CHOICE_RECORDED_SOURCE_UNVERIFIED",
        "bridge_status_unchanged": record.status.value,
        "source_rule": choice.source_step.rule.value,
        "choice_count": len(snapshot.choices),
        "notes": [
            "A GIVEN source is a source-claimed selection, not a derived proof.",
            "The typed choice catalog does not grant theorem availability or citation eligibility.",
            "The original bridge remains metadata-only for this component.",
            "No independent verification against the printed literature was performed.",
            "R7 derived Hopf/double relations remain separate assertions.",
        ],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 163 R4-R8 — (5.3) の元の選択の記録", "",
        r"- 数学的表記: $\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1$",
        "- 型付きの式の検査: 成功", "- 登録区分: CHOICE_RECORDED_SOURCE_UNVERIFIED",
        "- 元の Bridge の状態: metadata_only（変更なし）",
        "- 既存 ProofStep: GIVEN（変更なし）", "- 原典との独立照合: 未実施", "",
        r"この選択は $H(\nu')=\eta_5$ や $2\nu'=\eta_3\eta_4\eta_5$ と別々に扱う。",
        "探索への候補提供、推論規則の自動生成、Renderer 変更は行わない。",
        "全体 pytest は Phase 163 の最後まで実施しない。", "",
    ]
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    result = run_audit(Path("phase163_r4_r8_output"))
    print("Phase 163 R4-R8:", result["status"], result["bridge_status_unchanged"])
    print("Saved phase163_r4_r8_output/report.md")
    print("Full pytest not run.")
