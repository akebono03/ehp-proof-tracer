"""Phase 166 R2: read-only, explicitly typed witness for Toda (5.3)."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple
from proof import Relation, RelationType
from phase165_r4_production_connection import discover_production_registry


def typed_witness() -> tuple[Relation, dict]:
    """Build a typed candidate, never a proof step or source authorization."""
    eta3 = HomotopyElement("η₃", 3, source=4, target=3,
                           generator=GeneratorSymbol("η", index=3))
    eta4 = HomotopyElement("η₄", 4, source=5, target=4,
                           generator=GeneratorSymbol("η", index=4))
    eta5 = HomotopyElement("η₅", 5, source=6, target=5,
                           generator=GeneratorSymbol("η", index=5))
    nu_prime = HomotopyElement("ν′", 3, source=6, target=3,
                               generator=GeneratorSymbol("ν", decoration="′"))
    inner = Composition(eta4, eta5)
    outer = Composition(eta3, inner)
    compatible = inner.is_type_compatible() and eta3.source == eta4.target
    lhs_source, lhs_target = eta5.source, eta3.target
    rhs_source, rhs_target = nu_prime.source, nu_prime.target
    if not compatible or (lhs_source, lhs_target) != (rhs_source, rhs_target):
        raise ValueError("The (5.3) candidate has incompatible source/target")
    relation = Relation(lhs=outer, rhs=Multiple(2, nu_prime),
                        relation_type=RelationType.EQUALITY)
    info = {
        "lhs_source": lhs_source,
        "lhs_target": lhs_target,
        "rhs_source": rhs_source,
        "rhs_target": rhs_target,
        "homotopy_group": "pi_6^3",
        "inner_composition_compatible": inner.is_type_compatible(),
        "outer_composition_compatible_by_boundary": eta3.source == eta4.target,
        "typed_relation_constructed": True,
        "registry_content_equal_to_relation": False,
        "mathematical_identity_confirmed": False,
        "proof_permission_granted": False,
    }
    return relation, info


def inspect(source: Path, registry) -> dict:
    if not source.is_file():
        raise FileNotFoundError(source)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 687:
        raise ValueError(f"Expected 687 source rows, found {len(rows)}")
    assert_id = "boundary:(5.3):nu_prime_double_relation"
    assertion = registry.assertion(assert_id)
    if getattr(assertion.content, "component_key", None) != "nu_prime_double_relation":
        raise ValueError("The registered component has changed")
    if getattr(getattr(assertion.content, "statement_role", None), "value", None) != "relation":
        raise ValueError("The registered component is not a relation")
    relation, typing = typed_witness()
    selected = []
    for line, row in enumerate(rows, start=2):
        reference = row.get("reference", "")
        if not reference.startswith("(5.3),"):
            continue
        left = row.get("composition", "").strip()
        right = row.get("rep_linear", "").strip()
        exact = left == r"\eta3^3" and right == r"2\nu'"
        selected.append({
            "csv_line": line, "n": row.get("n", ""), "k": row.get("k", ""),
            "composition": left, "rep_linear": right,
            "display_pair_matches_witness": exact,
            "candidate_component_id": assert_id if exact else None,
            "status": "DISPLAY_MATCH_TYPED_WITNESS_NOT_CERTIFIED" if exact else "OTHER_OR_INCOMPLETE_DISPLAY",
            "mathematical_identity_confirmed": False,
            "proof_permission_granted": False,
        })
    if len(selected) != 4 or sum(r["display_pair_matches_witness"] for r in selected) != 2:
        raise ValueError("(5.3) CSV baseline changed; refusing silent mapping")
    result = {
        "phase": "166 R2 typed (5.3) witness",
        "read_only": True,
        "rows_total": len(rows),
        "equation53_rows": len(selected),
        "display_match_rows": 2,
        "candidate_assertion_id": assert_id,
        "assertion_content_type": type(assertion.content).__name__,
        "typed_expression_type": type(relation).__name__,
        "typing": typing,
        "mathematical_identity_confirmed": 0,
        "proof_permission_granted": 0,
        "production_code_modified": False,
        "full_pytest_run": False,
        "rows": selected,
    }
    return result


def main() -> int:
    registry = discover_production_registry().bridge.registry
    candidates = (ROOT / "sphere_relation2.csv",
                  ROOT / "phase166_r1_source_registry_audit" / "sphere_relation2.csv")
    source = next((candidate for candidate in candidates if candidate.is_file()), None)
    if source is None:
        raise FileNotFoundError("sphere_relation2.csv")
    result = inspect(source, registry)
    destination = HERE / "results"
    destination.mkdir(exist_ok=True)
    (destination / "audit_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    with (destination / "typed53_candidates.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result["rows"][0]))
        writer.writeheader()
        writer.writerows(result["rows"])
    print(json.dumps({key: value for key, value in result.items() if key != "rows"},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
