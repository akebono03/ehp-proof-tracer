"""Read-only audit of Toda Proposition 4.4 and equation (5.2) registry wiring."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LOCATORS = ("Proposition 4.4", "(5.2)")
EXPECTED_IDS = {
    "Proposition 4.4": "toda:tex:ch4:0010",
    "(5.2)": "toda:tex:ch5:0003",
}


def _display(value: object) -> str:
    return repr(value)[:1000]


def _matches(value: object, locator: str) -> bool:
    text = str(value)
    return locator in text or EXPECTED_IDS[locator] in text


def _inspect_bridge(name: str, bridge: object) -> dict:
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    registry = bridge.registry
    refs = tuple(registry._references.values())
    assertions = tuple(registry._assertions.values())
    links = tuple(bridge.proof_links)
    output = {"source": name, "reference_count": len(refs), "assertion_count": len(assertions), "proof_link_count": len(links), "locators": {}}
    for locator in LOCATORS:
        matching_refs = [r for r in refs if _matches(getattr(r, "locator", ""), locator) or _matches(getattr(r, "reference_id", ""), locator)]
        refids = {r.reference_id for r in matching_refs}
        matching_assertions = [a for a in assertions if a.reference_id in refids or _matches(a.assertion_id, locator)]
        ids = {a.assertion_id for a in matching_assertions}
        matching_links = [l for l in links if l.assertion_id in ids]
        certified = []
        for link in matching_links:
            step = link.step
            if step is None:
                continue
            assertion = registry.assertion(link.assertion_id)
            if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                    and step.rule is ProofRule.GIVEN
                    and step.conclusion == assertion.content):
                certified.append({"assertion_id": link.assertion_id, "type": type(step.conclusion).__name__, "conclusion": _display(step.conclusion)})
        output["locators"][locator] = {
            "reference_ids": sorted(refids),
            "assertions": [{"assertion_id": a.assertion_id, "origin": str(a.origin), "content_type": type(a.content).__name__, "content": _display(a.content)} for a in matching_assertions],
            "link_count": len(matching_links),
            "fixed_given_links": certified,
            "typed_reference_usable": bool(certified),
        }
    return output


def audit() -> dict:
    from phase165_r9_production_wiring import discover_goal_search_inputs
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry

    production = discover_goal_search_inputs().bridge
    source = ROOT / "phase165_r14_r39_toda51.tex"
    adopted = build_adopted_typed_reference_registry(source)
    shared = build_shared_typed_bridge(sources=(production, adopted))
    results = [
        _inspect_bridge("production", production),
        _inspect_bridge("adopted_tex", adopted),
        _inspect_bridge("shared", shared),
    ]
    # An eligible leaf does not imply a forward/backward expansion can use it.
    # Report source reachability separately without attempting an unsupported theorem specialization.
    conclusions = []
    for link in shared.proof_links:
        if link.step is not None:
            conclusions.append(type(link.step.conclusion).__name__)
    # No arbitrary candidate goal is fabricated: only report whether these types occur in linked leaves.
    result = {
        "phase": "165 R52-R27-R4",
        "mode": "READ_ONLY_REFERENCE_TO_TYPED_GIVEN_AUDIT",
        "results": results,
        "shared_linked_conclusion_types": sorted(set(conclusions)),
        "proposition44_linked_typed": any("Prop44" in t for t in conclusions),
        "equation52_linked_typed": "Toda52CompositionIsomorphismStatement" in conclusions,
        "actual_backward_expansion_verified": False,
        "reference_identity_semantically_verified": False,
        "production_modified": False,
        "full_pytest_run": False,
    }
    out = Path(__file__).resolve().parent / "audit_output"
    out.mkdir(exist_ok=True)
    (out / "registry_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# R27-R4 文献命題接続監査", "", "本監査は型付き GIVEN の利用可能性を確認するもので、数学的同値性の証明や命題の自動登録は行いません。", ""]
    for record in results:
        lines.append("## " + record["source"])
        for locator, values in record["locators"].items():
            lines.append(f"- {locator}: 参照 {len(values['reference_ids'])} 件 / 主張 {len(values['assertions'])} 件 / 検証可能な GIVEN 接続 {len(values['fixed_given_links'])} 件")
        lines.append("")
    lines.append("共通 Backward Search の当該命題への特殊化・適用は未検証です。")
    (out / "review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = audit()
    print(json.dumps({
        "phase": result["phase"], "mode": result["mode"],
        "shared": result["results"][2]["locators"],
        "backward_expansion_verified": False, "production_modified": False,
        "full_pytest_run": False,
    }, ensure_ascii=False, indent=2))
