"""Actual 112-target Web Narrative route audit; never modifies proof data."""
import json
from pathlib import Path

from web_group_proof import build_standard_web_group_proof_view
from web_group_query import build_standard_web_group_query_view


def main():
    output = Path("phase164_r5_r2_output")
    output.mkdir(exist_ok=True)
    results = []
    for n in range(2, 16):
        for k in range(8):
            item = {"n": n, "k": k}
            try:
                query = build_standard_web_group_query_view(n, k)
                if not query.proof_available:
                    item["status"] = "NO_PROOF_AVAILABLE"
                else:
                    view = build_standard_web_group_proof_view(n, k, 2, "narrative")
                    if not view.rendered_lines or view.mode != "narrative":
                        raise ValueError("common Narrative produced no lines")
                    if not view.conclusion_latex:
                        raise ValueError("missing proof conclusion")
                    item["status"] = "COMMON_VIEW_OK"
                    item["phase"] = view.phase
            except Exception as error:
                item["status"] = "ERROR"
                item["error"] = type(error).__name__ + ": " + str(error)
            results.append(item)
            print("pi", n + k, "^", n, item["status"], flush=True)
    counts = {name: sum(row["status"] == name for row in results)
              for name in ("COMMON_VIEW_OK", "NO_PROOF_AVAILABLE", "ERROR")}
    report = {"phase": "164 R5-R2", "targets": 112, "counts": counts,
              "all_available_proofs_use_common_view": counts["ERROR"] == 0,
              "full_pytest_run": False, "results": results}
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "results"}, ensure_ascii=False, indent=2))
    if counts["ERROR"]:
        raise SystemExit("112-target common display audit failed; see report.json")


if __name__ == "__main__":
    main()
