"""Read-only literature statement registration audit for Proposition 5.1/5.3."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) in sys.path:
    sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r12_literature_registration import (
    COMPONENTS, existing_prop51_prop53_candidates,
    register_prop51_prop53_literature_statements,
)


def run_audit(directory: Path) -> dict[str, object]:
    base = build_registry_bridge()
    result = register_prop51_prop53_literature_statements(
        base, existing_prop51_prop53_candidates()
    )
    targets = {e.assertion_id for e in result.evidence}
    unchanged_original = all(
        r.status.value == "metadata_only" for r in base.records if r.assertion_id in targets
    )
    output = {
        "phase": "163 R4-R12",
        "status": "TYPED_SOURCE_UNVERIFIED",
        "registered_count": len(result.evidence),
        "counts_by_reference": {
            locator: len(keys) for locator, keys in COMPONENTS.items()
        },
        "proof_status": "PROOF_ANCESTRY_NOT_CHECKED",
        "proof_links_unchanged": result.snapshot.proof_links == base.proof_links,
        "base_metadata_unchanged": unchanged_original,
        "evidence": [
            {
                "assertion_id": e.assertion_id,
                "source_description": e.source_description,
                "verification_status": e.verification_status,
                "proof_status": e.proof_status,
            }
            for e in result.evidence
        ],
    }
    if len(result.evidence) != 8 or not output["proof_links_unchanged"] or not unchanged_original:
        raise RuntimeError("Proposition 5.1/5.3 registration audit failed")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "summary.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R12 — Proposition 5.1 / 5.3 の型付き登録",
        "", "状態: TYPED_SOURCE_UNVERIFIED（原典照合は未実施）", "",
        "| 文献 | 成分 | 登録 | 出典検証 | 証明木検証 |",
        "|---|---|---|---|---|",
    ]
    for entry in result.evidence:
        locator, component = entry.assertion_id.removeprefix("boundary:").rsplit(":", 1)
        lines.append(
            f"| {locator} | `{component}` | STRUCTURED | {entry.verification_status} | {entry.proof_status} |"
        )
    lines.extend([
        "", "生成元・型付き範囲は R4-R12 の検証で確認。",
        "Proposition 5.1 の高次部分は境界 metadata の n >= 3 を型付き宣言として保持。",
        "Proposition 5.3 の高次部分は n >= 5 を型付き宣言として保持。",
        "出典の数学的正しさや証明成立を示すものではありません。",
        "全体 pytest は実施していません。", "",
    ])
    (directory / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    output = run_audit(Path("phase163_r4_r12_output"))
    print(f"Phase 163 R4-R12: {output['status']} {output['registered_count']}")
    print("Saved phase163_r4_r12_output/report.md")
    print("Full pytest not run.")
