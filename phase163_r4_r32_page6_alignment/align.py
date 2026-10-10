"""Phase 163 R4-R32: one source-verified omission on Toda printed page 6."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "521b481431b862b2c278069223c4990f36cf4fb6164987de78d75d1da47c7a82"
BEFORE = r"""\]
で定める.
写像
\[
f:A\to A',\quad g:B\to B'
"""
AFTER = r"""\]
で定める.
さらに原本の球面の reduced join の同一視に関して, 次の関係が成り立つ.
\[
\shrink_{m+n,p}\bigl(\shrink_{m,n}(a,b),c\bigr)
=\shrink_{m,n+p}\bigl(a,\shrink_{n,p}(b,c)\bigr),
\quad (a,b,c)\in S^m\times S^n\times S^p.
\]
写像
\[
f:A\to A',\quad g:B\to B'
"""


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def correct_page_six(text: str) -> str:
    if digest(text) != EXPECTED_SHA256:
        raise ValueError("R4-R31 source SHA-256 mismatch; no output written")
    if text.count(BEFORE) != 1:
        raise ValueError("Expected uncorrected source interval not unique")
    return text.replace(BEFORE, AFTER, 1)


def update_ledger(ledger: list[dict], source_sha: str) -> list[dict]:
    if len(ledger) != 11 or [row.get("pdf_page") for row in ledger] != list(range(1, 12)):
        raise ValueError("Invalid 11-page ledger")
    if ledger[0].get("status") != "VERIFIED" or any(row.get("status") != "UNVERIFIED" for row in ledger[1:]):
        raise ValueError("Unexpected previous verification status")
    if any(row.get("source_sha256") != EXPECTED_SHA256 for row in ledger):
        raise ValueError("Ledger SHA-256 mismatch")
    result = json.loads(json.dumps(ledger, ensure_ascii=False))
    for row in result:
        row["source_sha256"] = source_sha
    page = result[1]
    page["status"] = "UNVERIFIED"
    page["evidence_note"] = (page.get("evidence_note", "") + " R4-R32: original printed p.6 (PDF p.2), explicit sphere reduced-join associativity equation restored after (1.3); remaining mathematical text not fully checked.").strip()
    page["verification_scope"] = "PARTIAL_MATHEMATICAL_REVIEW"
    return result


def run(source: Path, ledger_file: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ledger = json.loads(ledger_file.read_text(encoding="utf-8-sig"))
    corrected = correct_page_six(text)
    new_sha = digest(corrected)
    new_ledger = update_ledger(ledger, new_sha)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r32.tex").write_text(text, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(corrected, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(new_ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["pdf_page", "printed_page", "status", "verification_scope", "evidence_note"])
        for row in new_ledger:
            writer.writerow([row.get(x, "") for x in ("pdf_page", "printed_page", "status", "verification_scope", "evidence_note")])
    with (output / "alignment_review.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["printed_page", "source", "subject", "status", "evidence"])
        writer.writerow([6, "Toda original PDF p.2", "Sphere reduced-join associativity equation after (1.3)", "CORRECTED", "Original explicitly has phi_(m+n,p)(phi_(m,n)(a,b),c)=phi_(m,n+p)(a,phi_(n,p)(b,c)); TeX omitted this displayed identity."])
        writer.writerow([6, "Toda original PDF p.2", "Composition and (1.4) details", "UNVERIFIED", "Full line-by-line comparison not completed in R4-R32."])
    counts = {s: sum(row["status"] == s for row in new_ledger) for s in ("VERIFIED", "UNVERIFIED", "CORRECTION_REQUIRED")}
    summary = {"phase": "163 R4-R32", "input_sha256": digest(text), "output_sha256": new_sha, "reviewed_printed_page": 6, "confirmed_corrections": 1, "prior_confirmed_corrections": 15, "total_recorded_corrections": 16, "status_counts": counts, "page_fully_verified": False, "chapter_fully_verified": False, "statement_ids_changed": 0, "production_code_changed": False, "full_suite_run": False}
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text("# Phase 163 R4-R32 — Toda 原本印刷6ページの部分照合\n\n- 原本 PDF 2ページの (1.3) 直後にある球面 reduced join の結合性の明示式を、TeX の省略箇所に追加した。\n- TeX の記号は原本の # に対応する \\wedge とし、既存の \\shrink マクロを再利用した。\n- (1.3) 自体と過去15箇所の訂正を維持した。\n- 式 (1.4) の細部を含む印刷6ページ全文照合は未完了。ページ状態は UNVERIFIED のまま。\n- 印刷5ページは VERIFIED を維持し、他9ページも UNVERIFIED とした。\n- Statement ID、Registry、Backward Search に変更なし。全体 pytest は実行しない。\n", encoding="utf-8")
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
