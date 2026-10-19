"""Read-only candidate binding for Toda (5.3); no certification or ProofStep."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase166_r2_typed53.audit import typed_witness
from phase165_r4_production_connection import discover_production_registry
from unified_statement_registry import AssertionInstantiation

ASSERTION_ID = "boundary:(5.3):nu_prime_double_relation"


def candidate_binding(registry):
    """Return a typed *candidate*, never a certified statement or proof link."""
    assertion = registry.assertion(ASSERTION_ID)
    content = assertion.content
    if (getattr(content, "component_key", None) != "nu_prime_double_relation"
            or getattr(content, "reference_locator", None) != "(5.3)"
            or getattr(getattr(content, "statement_role", None), "value", None) != "relation"):
        raise ValueError("Toda (5.3) component metadata mismatch")
    relation, typing = typed_witness()
    instantiation = AssertionInstantiation(
        assertion_id=ASSERTION_ID,
        concrete_content=relation,
        substitutions=(),
    )
    return instantiation, typing, content


def inspect(source: Path, registry):
    if not source.is_file():
        raise FileNotFoundError(source)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 687:
        raise ValueError(f"Unexpected relation baseline: {len(rows)} rows")
    instantiation, typing, component = candidate_binding(registry)
    matching = []
    selected_count = 0
    for csv_line, row in enumerate(rows, 2):
        if not str(row.get("reference", "")).startswith("(5.3),"):
            continue
        selected_count += 1
        if (str(row.get("composition", "")).strip() == r"\eta3^3"
                and str(row.get("rep_linear", "")).strip() == r"2\nu'"):
            matching.append({
                "csv_line": csv_line,
                "assertion_id": instantiation.assertion_id,
                "status": "CANDIDATE_DISPLAY_AND_TYPE_ONLY",
                "mathematical_identity_confirmed": False,
                "proof_permission_granted": False,
            })
    if selected_count != 4 or len(matching) != 2:
        raise ValueError("The 5.3 row/display baseline changed")
    return {
        "phase": "166 R2 assertion binding",
        "read_only": True,
        "selected_rows": selected_count,
        "binding_candidates": matching,
        "candidate_count": len(matching),
        "assertion_id": instantiation.assertion_id,
        "assertion_content_type": type(registry.assertion(ASSERTION_ID).content).__name__,
        "candidate_content_type": type(instantiation.concrete_content).__name__,
        "component_key": component.component_key,
        "homotopy_group": typing["homotopy_group"],
        "registry_content_equal_to_relation": registry.assertion(ASSERTION_ID).content == instantiation.concrete_content,
        "mathematical_identity_confirmed": 0,
        "proof_permission_granted": 0,
        "proof_step_links_created": 0,
        "production_code_modified": False,
        "full_pytest_run": False,
    }


def main():
    candidates = (
        ROOT / "sphere_relation2.csv",
        ROOT / "phase166_r1_source_registry_audit" / "sphere_relation2.csv",
    )
    source = next((p for p in candidates if p.is_file()), None)
    if source is None:
        raise FileNotFoundError("sphere_relation2.csv was not found")
    registry = discover_production_registry().bridge.registry
    result = inspect(source, registry)
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    (out / "audit_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (out / "binding_candidates.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=(
            "csv_line", "assertion_id", "status", "mathematical_identity_confirmed", "proof_permission_granted"
        ))
        writer.writeheader()
        writer.writerows(result["binding_candidates"])
    print(json.dumps({k: v for k, v in result.items() if k != "binding_candidates"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
