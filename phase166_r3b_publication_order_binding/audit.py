from __future__ import annotations

import json

from phase163_r4_registry_bridge import build_registry_bridge
from phase166_r3b_publication_order_binding import connect_phase163_publication_order


def main() -> None:
    before = build_registry_bridge()
    after, summary = connect_phase163_publication_order(before)
    report = {
        "phase": "166 R3-B",
        "status": "EXISTING_PUBLICATION_ORDER_CONNECTED_BY_REFERENCE_ID",
        "manifest_reference_count": summary.manifest_reference_count,
        "manifest_assertion_count": summary.manifest_assertion_count,
        "typed_reference_count": summary.typed_reference_count,
        "connected_reference_count": summary.connected_reference_count,
        "connected_assertion_count": summary.connected_assertion_count,
        "unchanged_reference_count": summary.unchanged_reference_count,
        "proof_link_count": summary.proof_link_count,
        "records_unchanged": after.records is before.records,
        "proof_links_unchanged": after.proof_links is before.proof_links,
        "tex_reparsed": False,
        "publication_order_recomputed": False,
        "locator_fallback_used": False,
        "component_positions_rewritten": False,
        "dependencies_rewritten": False,
        "proof_search_connected": False,
        "sqlite_added": False,
        "full_pytest_run": False,
        "bindings": [
            {
                "reference_id": item.reference_id,
                "publication_position": item.publication_position,
                "typed_assertion_ids": list(item.typed_assertion_ids),
                "source_statement_ids": list(item.source_statement_ids),
            }
            for item in summary.bindings
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
