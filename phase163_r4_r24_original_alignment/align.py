"""R4-R24: two PDF-confirmed Chapter I transcription corrections."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_CANONICAL_SHA256 = "c498c52fba9a770a3b6deddcbed111dfb3badeb835a64afe0a914cadda58f6f2"
CORRECTIONS = (
    (
        "Proposition 1.6, second condition",
        12,
        8,
        r"\gamma=\Ex\gamma' \ (X=\Ex X,\ W=\Ex W')",
        r"\gamma=\Ex\gamma' \ (X=\Ex X',\ W=\Ex W')",
        "原本では X=EX'。転記中の X=EX を訂正する。",
    ),
    (
        "Proposition 1.9, extension domain",
        14,
        10,
        r"\overline\beta\in[X\cup_f CW, Y]",
        r"\overline\beta\in[X\cup_\gamma CW, Y]",
        "原本では X∪_γ CW。添字 f を γ に訂正する。",
    ),
)
PENDING = (
    ("Proposition 1.3", 10, 6),
    ("Proposition 1.4", 11, 7),
    ("Proposition 1.5", 12, 8),
    ("Proposition 1.6: remaining conditions and proof", 12, 8),
    ("Proposition 1.7: statement and proof", 13, 9),
    ("Proposition 1.8: statement and proof", 14, 10),
    ("Proposition 1.9: remaining conditions and proof", 14, 10),
)


def align(source: str) -> str:
    result = source
    for item, printed, pdf, old, new, finding in CORRECTIONS:
        if result.count(old) != 1:
            raise ValueError(f"修正対象が1箇所ではありません: {item}")
        result = result.replace(old, new, 1)
    return result


def run(source: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    actual_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if actual_sha != EXPECTED_CANONICAL_SHA256:
        raise ValueError("R4-R23 の既知の修正版 TeX と異なります。変更を中止します")
    corrected = align(text)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r24.tex").write_text(text, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(corrected, encoding="utf-8")
    with (output / "alignment_review.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("status", "printed_page", "pdf_page", "item", "old_tex", "new_tex", "finding"))
        for item, printed, pdf, old, new, finding in CORRECTIONS:
            writer.writerow(("CONFIRMED_CORRECTION", printed, pdf, item, old, new, finding))
        for item, printed, pdf in PENDING:
            writer.writerow(("PENDING_FULL_COMPARISON", printed, pdf, item, "", "", "全文・全添字・証明の原典照合は未完了"))
    summary = {
        "phase": "163 R4-R24",
        "input_canonical_sha256": actual_sha,
        "confirmed_corrections": len(CORRECTIONS),
        "carried_forward_r21_to_r23_corrections": 4,
        "total_recorded_corrections": 6,
        "remaining_review_groups": len(PENDING),
        "chapter_fully_verified": False,
        "statement_ids_changed": 0,
        "production_code_changed": False,
        "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R24 原本照合記録\n\n"
        "Toda 原本 PDF の印刷12頁（PDF 8頁）と印刷14頁（PDF 10頁）を目視で確認。\n\n"
        "- Proposition 1.6: $X=EX$ を原本の $X=EX'$ に訂正。\n"
        "- Proposition 1.9: extension の定義域 $X\\cup_f CW$ を $X\\cup_\\gamma CW$ に訂正。\n\n"
        "R4-R21〜R23 の修正4箇所は維持。その他の命題の逐字照合は未完了。"
        "既存 Registry・証明探索は未変更。全体 pytest は未実行。\n", encoding="utf-8"
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
