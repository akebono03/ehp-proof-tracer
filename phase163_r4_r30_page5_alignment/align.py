"""Phase 163 R4-R30: conservative Toda printed page 5 correction."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "d742543864fbfc77b79a683e95e322a33b18ee1bfaf102ea730533a95945847d"
OLD = r"\psi_n(t) = (\cos 2\pi t,\ \sin 2\pi t)."
NEW = r"\psi_1(t) = (\cos 2\pi t,\ \sin 2\pi t)."


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def correct_page5(text: str) -> str:
    if digest(text) != EXPECTED_SHA256:
        raise ValueError("R4-R29 corrected TeX SHA-256 mismatch; no changes applied")
    if text.count(OLD) != 1 or NEW in text:
        raise ValueError("Unexpected formula occurrence or correction already applied")
    return text.replace(OLD, NEW, 1)


def update_ledger(ledger: list[dict], before_hash: str, after_hash: str) -> list[dict]:
    if len(ledger) != 11 or [p.get("pdf_page") for p in ledger] != list(range(1, 12)):
        raise ValueError("Expected eleven ordered PDF pages")
    if any(p.get("source_sha256") != before_hash or p.get("status") != "UNVERIFIED" for p in ledger):
        raise ValueError("Unexpected ledger hash or status")
    result = json.loads(json.dumps(ledger, ensure_ascii=False))
    for row in result:
        row["source_sha256"] = after_hash
    row = result[0]
    row["prior_corrections"] = int(row["prior_corrections"]) + 1
    row["evidence_note"] = (str(row.get("evidence_note", "")) + " R4-R30: printed p.5 after (1.2) gives psi_1(t), not psi_n(t). Equation (1.1)/(1.2) and basepoint notation compared in part only; page remains UNVERIFIED.").strip()
    return result


def run(source: Path, ledger_path: Path, output: Path) -> dict:
    original = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    corrected = correct_page5(original)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    pages = update_ledger(ledger, digest(original), digest(corrected))
    counts = {s: sum(p["status"] == s for p in pages) for s in ("UNVERIFIED", "CORRECTION_REQUIRED", "VERIFIED")}
    summary = {
        "phase": "163 R4-R30",
        "input_sha256": digest(original),
        "output_sha256": digest(corrected),
        "confirmed_corrections": 1,
        "prior_confirmed_corrections": 14,
        "total_recorded_corrections": 15,
        "printed_page_reviewed": 5,
        "status_counts": counts,
        "page_fully_verified": False,
        "chapter_fully_verified": False,
        "statement_ids_changed": 0,
        "production_code_changed": False,
        "full_suite_run": False,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r30.tex").write_text(original, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(corrected, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("pdf_page", "printed_page", "status", "scope_hint", "prior_corrections", "evidence_note"))
        for row in pages:
            writer.writerow(tuple(row.get(k, "") for k in ("pdf_page", "printed_page", "status", "scope_hint", "prior_corrections", "evidence_note")))
    with (output / "alignment_review.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("pdf_page", "printed_page", "item", "before_tex", "after_tex", "original_pdf_evidence", "status"))
        writer.writerow((1, 5, "circle_parameterization", OLD, NEW, "Printed p.5 following (1.2): psi_1(t)=(cos 2pi t, sin 2pi t)", "CORRECTED"))
        writer.writerow((1, 5, "equation_1_1", r"\psi_n:I^n\to S^n", "", "Printed p.5 (1.1) identifies the continuous map; no confirmed numerical discrepancy", "PARTIALLY_REVIEWED"))
        writer.writerow((1, 5, "equation_1_2", "boundary and homeomorphism clauses", "", "Printed p.5 (1.2): boundary collapses to e0; map restricts to homeomorphism on complements", "PARTIALLY_REVIEWED"))
        writer.writerow((1, 5, "homotopy_set_notation", "[X,Y]", "", "Printed p.5 uses pi(X -> Y); notation normalization is not established as a transcription correction", "UNRESOLVED_NOTATION"))
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R30 — 印刷5ページ原本照合（部分）\n\n"
        "原本 PDF の印刷5ページ（PDF 1ページ目）を基準に照合。\n\n"
        "- **修正1件**：式 (1.2) の次の円周パラメータ表示を $\\psi_n(t)$ から $\\psi_1(t)$ へ訂正。原本では $\\psi_1(t)=(\\cos 2\\pi t,\\sin 2\\pi t)$。\n"
        "- (1.1) は $\\psi_n:I^n\\to S^n$ を表示していることを確認。ただし周辺の文章を含む逐字照合は未完了。\n"
        "- (1.2) は境界の像と補集合上の同相に言及することを確認。ただし逐字照合は未完了。\n"
        "- 原本の $\\pi(X\\to Y)$ と TeX の $[X,Y]$ は記法上の差異。原本表記への置換を今回の自動修正に含めない。\n\n"
        "**印刷5ページは UNVERIFIED のまま**。修正累計15件。既存 Registry・Statement ID・証明探索を変更しない。全体 pytest は未実行。\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.ledger, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
