"""Phase 163 R4-R26: verified Proposition 1.9 proof transcription repair.

Only the two occurrences in the Proposition 1.9 proof are changed.
The user-supplied Toda PDF, printed p.14 (PDF p.10), is authoritative.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "600b2d38fbf3589bd250b1adbe32c56bdfa566aeab15b6fce174041a447c64d5"
OLD = r"(E^n p)^*\lambda = \alpha\circ E^n\beta"
NEW = r"(E^n p)^*\lambda = \alpha\circ E^n\overline\beta"
START_MARKER = r"\begin{proposition}\label{prop:1-9}"
PROOF_MARKER = "Proof.\\\n"
REVIEW = (
    ("Proposition 1.3", 10, 6),
    ("Proposition 1.4", 11, 7),
    ("Proposition 1.5", 12, 8),
    ("Proposition 1.6: remaining statement and proof", 12, 8),
    ("Proposition 1.7: remaining statement and proof", 13, 9),
    ("Proposition 1.8: remaining statement and proof", 14, 10),
    ("Proposition 1.9: remaining statement and proof", 14, 10),
)


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def align(source: str) -> str:
    if source.count(START_MARKER) != 1:
        raise ValueError("Proposition 1.9 の開始位置を一意に特定できません")
    head, proposition = source.split(START_MARKER, 1)
    if proposition.count(PROOF_MARKER) != 1:
        raise ValueError("Proposition 1.9 の証明開始位置を一意に特定できません")
    statement, proof = proposition.split(PROOF_MARKER, 1)
    if proof.count(OLD) != 2 or proof.count(NEW) != 0:
        raise ValueError("Proposition 1.9 の上線欠落が想定の2箇所ではありません")
    if source.count(OLD) != 2:
        raise ValueError("命題外にも対象の式があり、安全に修正できません")
    return head + START_MARKER + statement + PROOF_MARKER + proof.replace(OLD, NEW)


def run(source: Path, output: Path) -> dict:
    before = normalized_text(source)
    digest = hashlib.sha256(before.encode("utf-8")).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("R4-R25 の入力 SHA-256 が不一致です。出力は変更しません")
    after = align(before)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r26.tex").write_text(before, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(after, encoding="utf-8")
    with (output / "alignment_review.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("status", "printed_page", "pdf_page", "item", "before", "after", "evidence"))
        writer.writerow(("CONFIRMED_CORRECTION", 14, 10, "Proposition 1.9 proof: first pullback equation", OLD, NEW, "Original printed p.14: (E^n p)^* lambda = alpha o E^n bar(beta)"))
        writer.writerow(("CONFIRMED_CORRECTION", 14, 10, "Proposition 1.9 proof: repeated pullback equation", OLD, NEW, "Original printed p.14: repeated condition refers to extension bar(beta)"))
        for name, printed, pdf in REVIEW:
            writer.writerow(("PENDING_FULL_TEXT_COMPARISON", printed, pdf, name, "", "", "Full statement/proof parity not certified"))
    summary = {
        "phase": "163 R4-R26",
        "input_sha256": digest,
        "confirmed_corrections": 2,
        "carried_forward_r21_to_r25_corrections": 7,
        "total_recorded_corrections": 9,
        "remaining_review_groups": len(REVIEW),
        "chapter_fully_verified": False,
        "formal_statement_ids_changed": 0,
        "production_code_changed": False,
        "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = (
        "# Phase 163 R4-R26 — Toda 第1章の原本照合\n\n"
        "原本印刷14頁（PDF 10頁）の Proposition 1.9 証明を照合した。"
        "原本では $(E^n p)^*\\lambda=\\alpha\\circ E^n\\overline{\\beta}$ であるが、"
        "TeX では同じ関係式を述べる2箇所で $\\overline{\\beta}$ の上線が欠落していた。"
        "原本に合わせて2箇所とも修正した。\n\n"
        "これまでの7箇所の修正を維持した。Proposition 1.3〜1.9 の全文逐字照合は"
        "未完了であるため、残り7群は未確認とする。\n\n"
        "既存 Registry・証明探索・Statement ID に変更はない。全体 pytest は実施しない。\n"
    )
    (output / "report.md").write_text(report, encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
