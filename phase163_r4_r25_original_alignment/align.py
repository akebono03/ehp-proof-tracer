"""Toda Chapter I R4-R25: one original-PDF-verified transcription correction."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "8a917454376246add722e5e5c95b5f5ea8a0cf37f77649ef8fec973582f459b0"
OLD = r"[W^{n+1}W,Z]"
NEW = r"[\Ex^{n+1}W,Z]"
REVIEW = (
    ("Proposition 1.3", 10, 6),
    ("Proposition 1.4", 11, 7),
    ("Proposition 1.5", 12, 8),
    ("Proposition 1.6: remaining statement and proof", 12, 8),
    ("Proposition 1.7: statement and proof", 13, 9),
    ("Proposition 1.8: statement and proof", 14, 10),
    ("Proposition 1.9: remaining statement and proof", 14, 10),
)


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def align(source: str) -> str:
    if source.count(OLD) != 1:
        raise ValueError("Proposition 1.6 の修正対象がちょうど1箇所ではありません")
    if source.count(NEW) != 0:
        raise ValueError("修正済みの式が存在します。二重修正を防止します")
    return source.replace(OLD, NEW, 1)


def run(source: Path, output: Path) -> dict:
    before = normalized_text(source)
    digest = hashlib.sha256(before.encode("utf-8")).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("R4-R24 の既知の修正版 TeX と SHA-256 が一致しません。変更しません")
    after = align(before)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r25.tex").write_text(before, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(after, encoding="utf-8")
    with (output / "alignment_review.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("status", "printed_page", "pdf_page", "item", "before", "after", "evidence"))
        writer.writerow(("CONFIRMED_CORRECTION", 12, 8, "Proposition 1.6 proof: abelian homotopy group", OLD, NEW,
                         "Original: group pi(E^{n+1}W -> Z); supplied TeX mistakenly types W^{n+1}W."))
        for name, printed, pdf in REVIEW:
            writer.writerow(("PENDING_FULL_TEXT_COMPARISON", printed, pdf, name, "", "", "Not certified as word-for-word identical"))
    summary = {
        "phase": "163 R4-R25",
        "input_sha256": digest,
        "confirmed_corrections": 1,
        "carried_forward_r21_to_r24_corrections": 6,
        "total_recorded_corrections": 7,
        "remaining_review_groups": len(REVIEW),
        "chapter_fully_verified": False,
        "formal_statement_ids_changed": 0,
        "production_code_changed": False,
        "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R25 — Toda 第1章原本照合\n\n"
        "印刷12頁（PDF 8頁）にある Proposition 1.6 の証明では、群 $\\pi(E^{n+1}W\\to Z)$ が abelian（可換）と述べられる。"
        "TeX の `$[W^{n+1}W,Z]$` を `$[\\Ex^{n+1}W,Z]$` に訂正した。"
        "これは記号の転記訂正であり、R4-R21〜R24 の6修正はそのまま維持した。\n\n"
        "Proposition 1.3〜1.9 の全文逐字照合は未完了であり、`alignment_review.csv` に保留7群を記録した。"
        "既存 Registry、証明探索、Statement ID は変更していない。全体 pytest は未実行。\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
