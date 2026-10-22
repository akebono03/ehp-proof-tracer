from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
from typing import Iterable

from phase165_r9_production_wiring import discover_goal_search_inputs
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


LITERATURE_RE = re.compile(
    r"(Proposition\s+\d+(?:\.\d+)?|Lemma\s+\d+(?:\.\d+)?|Equation\s*\(?\d+(?:\.\d+)?\)?|\(\d+\.\d+\))",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class AuditRow:
    source: str
    assertion_id: str
    locator: str
    typed: bool
    fixed_statement: bool
    in_shared_bridge: bool
    has_reference: bool
    publication_position: int | None
    component_position: int | None
    has_proof_step_link: bool
    has_given_link: bool
    duplicate_count: int
    content_type: str
    content_repr: str


def strip_shared_prefix(assertion_id: str) -> str:
    return re.sub(r"^shared:\d+:", "", assertion_id)


def literature_locator(reference: object) -> str | None:
    values = (
        getattr(reference, "locator", None),
        getattr(reference, "title", None),
        getattr(reference, "label", None),
        getattr(reference, "source", None),
    )
    for value in values:
        if not isinstance(value, str):
            continue
        match = LITERATURE_RE.search(value)
        if match is not None:
            return match.group(1)
    return None


def is_typed_content(content: object) -> bool:
    return content is not None and not isinstance(content, (str, bytes, int, float, bool))


def semantic_key(assertion: object) -> tuple[str, str]:
    return (type(assertion.content).__name__, repr(assertion.content))


def collect_rows(source_name: str, bridge: object, shared_keys: set[tuple[str, str]]) -> list[AuditRow]:
    assertions = tuple(bridge.registry._assertions.values())
    key_counts = Counter(semantic_key(assertion) for assertion in assertions)
    links_by_id = defaultdict(list)
    for link in bridge.proof_links:
        links_by_id[link.assertion_id].append(link)

    rows: list[AuditRow] = []
    for assertion in assertions:
        reference = bridge.registry.reference(assertion.reference_id)
        locator = literature_locator(reference)
        if locator is None:
            continue
        links = links_by_id.get(assertion.assertion_id, [])
        rows.append(AuditRow(
            source=source_name,
            assertion_id=assertion.assertion_id,
            locator=locator,
            typed=is_typed_content(assertion.content),
            fixed_statement=assertion.origin is AssertionOrigin.FIXED_STATEMENT,
            in_shared_bridge=semantic_key(assertion) in shared_keys,
            has_reference=reference is not None,
            publication_position=getattr(assertion, "publication_position", None),
            component_position=getattr(assertion, "component_position", None),
            has_proof_step_link=bool(links),
            has_given_link=any(
                link.step is not None and link.step.rule is ProofRule.GIVEN
                for link in links
            ),
            duplicate_count=key_counts[semantic_key(assertion)],
            content_type=type(assertion.content).__name__,
            content_repr=repr(assertion.content),
        ))
    return rows


def summarize(rows: Iterable[AuditRow]) -> dict[str, object]:
    rows = tuple(rows)
    typed = tuple(row for row in rows if row.typed)
    disconnected = tuple(row for row in typed if not row.in_shared_bridge)
    missing_order = tuple(
        row for row in typed
        if row.publication_position is None or row.component_position is None
    )
    missing_link = tuple(row for row in typed if not row.has_proof_step_link)
    duplicate = tuple(row for row in typed if row.duplicate_count > 1)
    by_locator = Counter(row.locator for row in typed)
    return {
        "literature_rows": len(rows),
        "typed_rows": len(typed),
        "typed_not_in_shared_bridge": len(disconnected),
        "typed_missing_publication_or_component_position": len(missing_order),
        "typed_missing_proof_step_link": len(missing_link),
        "typed_duplicate_rows": len(duplicate),
        "typed_by_locator": dict(sorted(by_locator.items())),
    }


def main() -> int:
    production = discover_goal_search_inputs().bridge
    shared = build_shared_typed_bridge()
    shared_assertions = tuple(shared.registry._assertions.values())
    shared_keys = {semantic_key(assertion) for assertion in shared_assertions}

    production_rows = collect_rows("production", production, shared_keys)
    shared_rows = collect_rows("shared", shared, shared_keys)

    report = {
        "audit": "phase168-r2-6-registry-bridge",
        "production_code_modified": False,
        "definitions": {
            "typed": "content is a non-scalar Python object rather than metadata text",
            "in_shared_bridge": "same content type and repr occur in build_shared_typed_bridge() output",
            "proof_step_link": "RegistryBridgeResult.proof_links contains the assertion_id",
            "given_link": "a ProofStepLink exists whose step rule is GIVEN",
            "duplicate": "same content type and repr appears more than once in the same snapshot",
        },
        "production": summarize(production_rows),
        "shared": summarize(shared_rows),
        "production_rows": [asdict(row) for row in production_rows],
        "shared_rows": [asdict(row) for row in shared_rows],
    }

    out_dir = Path(__file__).resolve().parent / "output"
    out_dir.mkdir(exist_ok=True)
    json_path = out_dir / "registry_bridge_audit.json"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )

    csv_path = out_dir / "registry_bridge_audit.csv"
    headers = tuple(AuditRow.__dataclass_fields__)
    lines = [",".join(headers)]
    import csv
    import io
    for row in production_rows + shared_rows:
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="")
        writer.writerow([getattr(row, header) for header in headers])
        lines.append(buffer.getvalue())
    csv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(report["production"], ensure_ascii=False, indent=2))
    print("SHARED:")
    print(json.dumps(report["shared"], ensure_ascii=False, indent=2))
    print(f"JSON: {json_path}")
    print(f"CSV:  {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
