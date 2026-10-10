"""Read-only Phase 163 R4-R9 catalog demonstration using actual R8 choice."""
from __future__ import annotations

import json
from pathlib import Path
import sys

# The audit is executed from this package directory, whereas project modules
# are installed in the current project root by run.ps1.
PROJECT_ROOT = Path.cwd().resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r8_choice_registration import build_nu_prime_choice
from phase163_r4_r9_declaration_catalog import adapt_r8_snapshot
from probes.probe_phase58_capabilities import build_phase58_representative_result


def main() -> None:
    base = build_registry_bridge()
    selection = build_phase58_representative_result()["bracket_membership_step"]
    catalog = adapt_r8_snapshot(build_nu_prime_choice(base, selection))
    choice = catalog.declarations[0]
    record = next(x for x in base.records if x.assertion_id == choice.assertion_id)
    summary = {
        "phase": "163 R4-R9",
        "declarations": len(catalog.declarations),
        "kind": choice.kind.value,
        "reference_id": choice.reference_id,
        "assertion_id": choice.assertion_id,
        "defined_symbol": choice.defined_symbol,
        "index": choice.content.bracket.index,
        "coefficient": choice.content.bracket.second.coefficient,
        "source_verification": choice.provenance.value,
        "original_bridge_status": record.status.value,
        "definition_fixture_only": True,
        "citation_eligibility_granted": False,
        "full_pytest": "not_run",
    }
    destination = Path("phase163_r4_r9_output")
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = "\n".join((
        "# Phase 163 R4-R9 — Definition / Choice 共通登録モデル", "",
        r"- Choice: $\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1$", 
        "- (5.3) の Choice を既存の R8 から型付きで移送: 1件",
        "- 登録状態: source_unverified（引用許可なし）",
        "- 元の Bridge: metadata_only（変更なし）",
        "- Definition の独立した登録 API: 軽量テストの架空出典だけで確認",
        "- 他の文献 Definition の実登録: 未実施",
        "- 数学的同一性、原典の検証、Proof Search / Renderer 接続: 未実施",
        "- 全体 pytest: 未実施", "",
    ))
    (destination / "report.md").write_text(report, encoding="utf-8")
    print("Phase 163 R4-R9:", summary["declarations"], "choice declaration; bridge:", record.status.value)
    print("Saved phase163_r4_r9_output/report.md; full pytest not run.")


if __name__ == "__main__":
    main()
