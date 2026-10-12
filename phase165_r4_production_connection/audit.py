"""Produce a reproducible report using only live production registration."""
import json
from pathlib import Path

from phase165_r4_production_connection import (
    describe_production_blockers,
    discover_production_registry,
)


def main():
    discovery = discover_production_registry()
    info = {
        "phase": "165 R4",
        "mode": "LIVE_PRODUCTION_REGISTRY_DISCOVERY",
        "fixed_assertions": discovery.fixed_assertion_count,
        "internal_assertions": discovery.internal_assertion_count,
        "source_archive_assertions": discovery.archive_assertion_count,
        "fixed_with_both_order_fields": discovery.ordered_fixed_count,
        "proof_links": discovery.proof_link_count,
        "automatically_verified_assertions": len(discovery.verified_fixed_ids),
        "blockers": list(describe_production_blockers(discovery)),
        "pi5_3_goal_only_proved": False,
        "full_pytest_run": False,
    }
    out = Path("phase165_r4_output")
    out.mkdir(exist_ok=True)
    (out / "report.json").write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    content = ["# Phase 165 R4 本番登録接続監査", "", "| 項目 | 件数 |", "|---|---:|",]
    for name in ("fixed_assertions", "internal_assertions", "source_archive_assertions", "fixed_with_both_order_fields", "proof_links", "automatically_verified_assertions"):
        content.append(f"| {name} | {info[name]} |")
    content += ["", "## 未解決", ""] + [f"- `{item}`" for item in info["blockers"]]
    content += ["", "この結果は Goal-only の成功を示さない。旧経路への代替処理は追加していない。", ""]
    (out / "report.md").write_text("\n".join(content), encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
