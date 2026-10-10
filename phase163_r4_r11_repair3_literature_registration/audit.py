"""Read-only Proposition 5.6 registration audit; no proof ancestry replay."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r11_literature_registration import (
    ALL_KEYS,
    existing_prop56_candidates,
    register_prop56_literature_statements,
)


def run_audit(directory: Path) -> dict[str, object]:
    base = build_registry_bridge()
    result = register_prop56_literature_statements(
        base, existing_prop56_candidates()
    )
    evidence = result.evidence
    output = {
        "phase": "163 R4-R11 repair3",
        "status": "TYPED_SOURCE_UNVERIFIED",
        "registered_count": len(evidence),
        "registered_keys": list(ALL_KEYS),
        "source_status": "SOURCE_UNVERIFIED",
        "proof_status": "PROOF_ANCESTRY_NOT_CHECKED",
        "proof_links_unchanged": result.snapshot.proof_links == base.proof_links,
        "original_metadata_unchanged": all(
            r.status.value == "metadata_only"
            for r in base.records
            if r.assertion_id in {e.assertion_id for e in evidence}
        ),
        "evidence": [
            {
                "assertion_id": e.assertion_id,
                "source_description": e.source_description,
                "verification_status": e.verification_status,
                "proof_status": e.proof_status,
            }
            for e in evidence
        ],
        "notes": [
            "All five typed components have verified structure and generators.",
            "This is a candidate literature assertion catalog, not literature authentication.",
            "No ProofStepLink generated and no backward search eligibility granted.",
            "Prior Phase 161 provenance failures are separate and unresolved.",
        ],
    }
    if len(evidence) != 5 or not output["proof_links_unchanged"]:
        raise RuntimeError("registration audit integrity failed")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "summary.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R11 repair3 — Proposition 5.6 型付き文献登録",
        "",
        "状態: TYPED_SOURCE_UNVERIFIED（型付き構造を登録、文献原本との独立照合は未実施）",
        "",
        "| 成分 | 型付き登録 | 文献照合 | 証明木検証 |",
        "|---|---|---|---|",
    ]
    for e in evidence:
        lines.append(
            f"| `{e.assertion_id.rsplit(':', 1)[-1]}` | STRUCTURED | {e.verification_status} | {e.proof_status} |"
        )
    lines.extend([
        "", "生成元・直和構造と `n >= 6` は既存の R10/R11 構造検査で確認。",
        "原典照合済み・証明済み・Phase 164 探索可能という意味ではありません。",
        "過去に検出された2個の前提なし推論ノードは未解決のままです。",
        "全体 pytest は実施していません。", "",
    ])
    (directory / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    output = run_audit(Path("phase163_r4_r11_repair3_output"))
    print("Phase 163 R4-R11 repair3:", output["status"], output["registered_count"])
    print("Saved phase163_r4_r11_repair3_output/report.md")
    print("Full pytest not run.")
