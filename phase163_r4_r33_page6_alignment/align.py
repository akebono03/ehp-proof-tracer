"""R4-R33: Toda printed p.6 basepoint hypotheses, with an evidence ledger."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "1a09fde523a9064ab4b73e9248a4565651385bf9ffeb4ae9724fb6ff17625eeb"
BEFORE = """f:A\\to A',\\quad g:B\\to B'
\\]
に対し, reduced join"""
AFTER = """f:A\\to A',\\quad g:B\\to B'
\\]
は基点を保存し, $f(a_0)=a'_0$, $g(b_0)=b'_0$ を満たすものとする.
このとき, reduced join"""


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def correct(text: str) -> str:
    if sha256(text) != EXPECTED_SHA256:
        raise ValueError("R4-R32 input SHA-256 mismatch; no output written")
    if text.count(BEFORE) != 1:
        raise ValueError("Basepoint-hypothesis location is not unique")
    return text.replace(BEFORE, AFTER, 1)


def update_ledger(ledger: list[dict], new_hash: str) -> list[dict]:
    if len(ledger) != 11 or [x.get("pdf_page") for x in ledger] != list(range(1, 12)):
        raise ValueError("Expected an 11-page ledger")
    if [x.get("status") for x in ledger] != ["VERIFIED"] + ["UNVERIFIED"] * 10:
        raise ValueError("Unexpected page statuses")
    if any(x.get("source_sha256") != EXPECTED_SHA256 for x in ledger):
        raise ValueError("Ledger source SHA-256 mismatch")
    result = json.loads(json.dumps(ledger, ensure_ascii=False))
    for item in result:
        item["source_sha256"] = new_hash
    entry = result[1]
    entry["status"] = "UNVERIFIED"
    entry["verification_scope"] = "PARTIAL_MATHEMATICAL_REVIEW"
    entry["evidence_note"] = (entry.get("evidence_note", "") + " R4-R33: printed p.6 (PDF p.2), f(a0)=a0' and g(b0)=b0' explicitly restored in the reduced join paragraph; equation (1.4) 0/i/ii visually checked, but full page not exhaustively verified.").strip()
    return result


def run(source: Path, ledger_path: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    updated = correct(text)
    new_hash = sha256(updated)
    new_ledger = update_ledger(ledger, new_hash)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r33.tex").write_text(text, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(updated, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(new_ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["pdf_page", "printed_page", "status", "verification_scope", "evidence_note"])
        for row in new_ledger:
            writer.writerow([row.get(k, "") for k in ("pdf_page", "printed_page", "status", "verification_scope", "evidence_note")])
    with (output / "alignment_review.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["printed_page", "pdf_page", "subject", "status", "evidence"])
        writer.writerow([6, 2, "Reduced join basepoint conditions", "CORRECTED", "Original printed p.6 explicitly states f(a0)=a0' and g(b0)=b0'; TeX relied on the global based-map convention. Restored explicit hypotheses."])
        writer.writerow([6, 2, "Equation (1.4) items 0/i/ii", "PARTIALLY_REVIEWED", "Items and composition order visually compared. Page-wide mathematical/content completion is not asserted."])
        writer.writerow([6, 2, "Whole page", "UNVERIFIED", "Unfinished verification of the rest of the prose, source notation, and page boundary."])
    counts = {status: sum(row["status"] == status for row in new_ledger) for status in ("VERIFIED", "UNVERIFIED", "CORRECTION_REQUIRED")}
    summary = {"phase": "163 R4-R33", "input_sha256": sha256(text), "output_sha256": new_hash, "reviewed_printed_page": 6, "confirmed_corrections": 1, "prior_confirmed_corrections": 16, "total_recorded_corrections": 17, "status_counts": counts, "page_fully_verified": False, "chapter_fully_verified": False, "statement_ids_changed": 0, "production_code_changed": False, "full_suite_run": False}
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text("# Phase 163 R4-R33 — 印刷6ページの部分原本照合\n\n- 原本印刷6ページ（PDF 2ページ）に明示される $f(a_0)=a'_0$, $g(b_0)=b'_0$ を reduced join の写像の説明に追加した。\n- (1.4) の 0), i), ii) の存在と合成順序を原本画像で部分照合した。\n- (1.3) と R4-R32 の結合性の明示式を維持した。\n- 印刷5ページは VERIFIED。印刷6ページおよび残る9ページは UNVERIFIED。\n- 第1章全文照合、逐語一致の検証、Statement 登録は未完了。\n- 元ファイルと既存 Registry・証明探索は変更しない。全体 pytest は実行しない。\n", encoding="utf-8")
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
