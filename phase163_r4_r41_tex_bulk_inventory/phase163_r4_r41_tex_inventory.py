"""Phase 163 R4-R41: read-only inventory, no registry writes."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


LABEL = re.compile(r"\\(?:label)\s*\{([^{}]+)\}")
HEADING = re.compile(r"\\(?:chapter|section|subsection|begin\{(?:theorem|proposition|lemma|corollary|definition|remark)\})\b", re.I)


def inspect_sources(root: Path) -> list[dict[str, object]]:
    """Fingerprint Toda_01..05; report labels without assuming theorem boundaries."""
    result = []
    for chapter in range(1, 6):
        name = f"Toda_{chapter:02d}.tex"
        path = root / name
        if not path.is_file():
            result.append({"chapter": chapter, "file": name, "status": "MISSING"})
            continue
        raw = path.read_bytes()
        try:
            source = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            result.append({"chapter": chapter, "file": name, "status": "ENCODING_UNRESOLVED", "sha256": hashlib.sha256(raw).hexdigest()})
            continue
        labels = LABEL.findall(source)
        result.append({"chapter": chapter, "file": name, "status": "READABLE",
                       "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                       "label_count": len(labels), "labels": labels,
                       "duplicate_labels": sorted({x for x in labels if labels.count(x) > 1}),
                       "heading_candidates": len(HEADING.findall(source))})
    return result


def inspect_registry() -> dict[str, object]:
    from phase163_r4_registry_bridge import build_registry_bridge

    bridge = build_registry_bridge()
    references = bridge.registry._references
    assertions = bridge.registry._assertions
    return {"reference_count": len(references), "assertion_count": len(assertions),
            "reference_ids": sorted(references), "assertion_ids": sorted(assertions),
            "migration_counts": {status: sum(r.status.value == status for r in bridge.records)
                                 for status in sorted({r.status.value for r in bridge.records})},
            "unresolved_sources": [r.source_key for r in bridge.unresolved],
            "existing_ids_preserved": True}


def build_report(root: Path) -> dict[str, object]:
    sources = inspect_sources(root)
    registry = inspect_registry()
    return {"phase": "163 R4-R41", "mode": "READ_ONLY_INVENTORY",
            "sources": sources, "registry": registry,
            "registration_applied": False, "proof_search_connected": False,
            "next_step": "Review TeX structure and existing-id mapping before introducing a bulk registration writer."}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path.cwd() / "phase163_r4_r41_output")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    result = build_report(args.root)
    target = args.output / "inventory.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"R4-R41 read-only inventory: {target}")
    print("No TeX or registry modified; no bulk registration executed.")


if __name__ == "__main__":
    main()
