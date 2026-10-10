"""Audit the actual Phase 65 representative through the Phase 163 R7 binding."""
from __future__ import annotations

import json
from pathlib import Path

from phase163_r4_r10_generator_integrity import (
    ASSERTION_ID,
    verify_prop56_pi5_2_generator,
)
from phase163_r4_r7_representative_bindings import (
    bind_representative_witnesses,
    representative_candidates,
)
from phase163_r4_registry_bridge import build_registry_bridge


def run_audit(output_dir: Path) -> dict[str, object]:
    base = build_registry_bridge()
    candidates = tuple(
        candidate for candidate in representative_candidates()
        if (candidate.reference_locator, candidate.component_key)
        == ("Proposition 5.6", "pi5_2_group_relation")
    )
    if len(candidates) != 1:
        raise ValueError("Expected exactly one real Phase 65 proposition witness")
    snapshot, attempts = bind_representative_witnesses(base, candidates)
    if len(attempts) != 1 or attempts[0].status != "STRUCTURED":
        raise ValueError(f"Actual witness failed verification: {attempts}")
    integrity = verify_prop56_pi5_2_generator(snapshot)
    payload = {
        "phase": "163 R4-R10",
        "assertion_id": ASSERTION_ID,
        "status": integrity.status,
        "registration": attempts[0].status,
        "order": integrity.order,
        "generator_structure": "Composition(eta_2, Composition(eta_3, eta_4))",
        "canonical_latex": integrity.canonical_latex,
        "note": "Existing registered mathematical content is preserved; no production renderer or registration rewrite.",
        "literature_source_independently_verified": False,
        "full_pytest_run": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "report.md").write_text(
        "# Phase 163 R4-R10 — Proposition 5.6 生成元保持監査\n\n"
        f"- Assertion: `{ASSERTION_ID}`\n"
        f"- 結果: `{integrity.status}`\n"
        f"- 登録状態: `{attempts[0].status}`\n"
        f"- 位数: {integrity.order}\n"
        f"- 生成元内部構造: `Composition(eta_2, Composition(eta_3, eta_4))`\n"
        f"- 標準表示: `${integrity.canonical_latex}$`\n"
        "- 既存の登録内容・Renderer は変更していません\n"
        "- 文献原本との独立照合は未完了\n"
        "- 全体 pytest は未実施\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    result = run_audit(Path("phase163_r4_r10_output"))
    print(f"Phase 163 R4-R10: {result['status']}")
    print("Saved phase163_r4_r10_output/report.md")
    print("Full pytest not run.")
