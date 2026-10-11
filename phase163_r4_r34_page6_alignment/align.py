"""Phase 163 R4-R34: source-guarded correction of (1.4) 0) hypotheses."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "52c7b24fa4523107050b26137c2ef3f6fae3fb396565e3a2f95706ce4b7d4c17"
BEFORE = r"""\text{0).}\ & f\simeq f',\ g\simeq g' \ \Rightarrow\ 
f\ \wedge\ g\simeq f'\ \wedge\ g': A\wedge B\to A'\wedge B',"""
AFTER = r"""\text{0).}\ & f\simeq f':(A,a_0)\to(A',a'_0),\quad
 g\simeq g':(B,b_0)\to(B',b'_0)\ \Rightarrow\\
& f\wedge g\simeq f'\wedge g':
(A\wedge B,a_0\wedge b_0)\to(A'\wedge B',a'_0\wedge b'_0),"""


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def correct(text: str) -> str:
    if sha256(text) != EXPECTED_SHA256:
        raise ValueError("R4-R33 source SHA-256 mismatch; no output written")
    if text.count(BEFORE) != 1:
        raise ValueError("Equation (1.4) 0) target not unique")
    return text.replace(BEFORE, AFTER, 1)


def update_ledger(ledger: list[dict], new_sha: str) -> list[dict]:
    if len(ledger) != 11 or [x.get("pdf_page") for x in ledger] != list(range(1, 12)):
        raise ValueError("Expected 11 original PDF pages")
    if [x.get("status") for x in ledger] != ["VERIFIED"] + ["UNVERIFIED"] * 10:
        raise ValueError("Unexpected page verification statuses")
    if any(x.get("source_sha256") != EXPECTED_SHA256 for x in ledger):
        raise ValueError("Ledger SHA-256 does not match source")
    result = json.loads(json.dumps(ledger, ensure_ascii=False))
    for row in result:
        row["source_sha256"] = new_sha
    page = result[1]
    page["status"] = "UNVERIFIED"
    page["verification_scope"] = "PARTIAL_MATHEMATICAL_REVIEW"
    page["evidence_note"] = (page.get("evidence_note", "") + " R4-R34: printed p.6/PDF p.2 equation (1.4) 0) based-map domains, codomains, and the induced based reduced-join homotopy explicitly restored. Remaining page boundary and full mathematical-content verification pending.").strip()
    return result


def run(source: Path, ledger_path: Path, output: Path) -> dict:
    original = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    prior = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    corrected = correct(original)
    new_sha = sha256(corrected)
    updated_ledger = update_ledger(prior, new_sha)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r34.tex").write_text(original, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(corrected, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(updated_ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["pdf_page", "printed_page", "status", "verification_scope", "evidence_note"])
        for row in updated_ledger:
            writer.writerow([row.get(k, "") for k in ("pdf_page", "printed_page", "status", "verification_scope", "evidence_note")])
    with (output / "alignment_review.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["printed_page", "pdf_page", "subject", "status", "evidence"])
        writer.writerow([6, 2, "Equation (1.4) 0): based maps", "CORRECTED", "Original specifies pointed domain and codomain of f~f', g~g' and f#g~f'#g'. These are explicit in the updated TeX; wedge is the retained modern notation for original #."])
        writer.writerow([6, 2, "Printed p.6 full mathematical content", "UNVERIFIED", "Not all prose, notation, hypotheses and page-boundary continuation have been conclusively verified. No full-page VERIFIED claim."])
    statuses = ("VERIFIED", "UNVERIFIED", "CORRECTION_REQUIRED")
    summary = {
        "phase": "163 R4-R34", "input_sha256": sha256(original),
        "output_sha256": new_sha, "reviewed_printed_page": 6,
        "confirmed_corrections": 1, "prior_confirmed_corrections": 17,
        "total_recorded_corrections": 18,
        "status_counts": {status: sum(row["status"] == status for row in updated_ledger) for status in statuses},
        "page_fully_verified": False, "chapter_fully_verified": False,
        "statement_ids_changed": 0, "production_code_changed": False, "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R34 — 印刷6ページの原本照合\n\n"
        "- 原本印刷6ページの式 (1.4) 0) の基点付き写像の定義域・値域を TeX に明記した。\n"
        "- 記号 $\\wedge$ は原本の reduced join の記号 # を表す現行 TeX の慣行に従った。\n"
        "- 17箇所の過去修正を維持し、累計18箇所。\n"
        "- 印刷5ページ VERIFIED、印刷6ページは UNVERIFIED。原本全文の数学的照合未完了。\n"
        "- 既存 Registry、Statement ID、Backward Search は変更せず、全体 pytest は実行しない。\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.ledger, args.output), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
