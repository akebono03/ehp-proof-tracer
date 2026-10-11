"""Phase 163 R4-R29: conservative comparison of Toda printed page 5."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "db046e212b9fcef0c8500dbf563d7bf74792c6ea92f98b493f43fca152896226"
CHANGES = (
    (
        "tangent_direction",
        "での接ベクトルは,\n\\((0,t_{1},\\cdots,t_{n})\\)\nに平行になるものとする.",
        "での接ベクトルは,\n\\(\\{-1\\}\\times\\overrightarrow{c_{0}x}\\)\nに平行になるものとする.",
        "印刷5ページ：接ベクトルは (-1) × (c_0 から x へのベクトル) に平行",
    ),
    (
        "coordinate_interchange",
        "\\(t_{i}\\)\nを\n\\(t_{j}\\)\nに置き換えたとき,",
        "\\(t_{i}\\)\nと\n\\(t_{j}\\)\nを互いに交換したとき,",
        "印刷5ページ：If t_i and t_j are interchanged",
    ),
)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def align(text: str) -> str:
    if digest(text) != EXPECTED_SHA256:
        raise ValueError("R4-R28 corrected TeX SHA-256 mismatch; no changes applied")
    for key, old, new, evidence in CHANGES:
        if text.count(old) != 1 or new in text:
            raise ValueError(f"Non-unique or repeated correction: {key}")
        text = text.replace(old, new, 1)
    return text


def update_ledger(ledger: list[dict], old_hash: str, new_hash: str) -> list[dict]:
    if len(ledger) != 11 or [row.get("pdf_page") for row in ledger] != list(range(1, 12)):
        raise ValueError("Expected eleven ordered pages")
    if any(row.get("source_sha256") != old_hash for row in ledger):
        raise ValueError("Ledger source hash mismatch")
    pages = json.loads(json.dumps(ledger, ensure_ascii=False))
    for page in pages:
        if page["status"] != "UNVERIFIED":
            raise ValueError("Cannot implicitly overwrite completed page status")
        page["source_sha256"] = new_hash
    page5 = pages[0]
    page5["prior_corrections"] = int(page5["prior_corrections"]) + len(CHANGES)
    page5["evidence_note"] = (
        str(page5.get("evidence_note", "")) + " R4-R29: tangent vector direction and "
        "interchanging t_i/t_j aligned with printed p.5. All fields not fully compared."
    ).strip()
    return pages


def run(source: Path, ledger_path: Path, output: Path) -> dict:
    original = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    corrected = align(original)
    pages = update_ledger(
        json.loads(ledger_path.read_text(encoding="utf-8-sig")),
        digest(original), digest(corrected)
    )
    counts = {name: sum(row["status"] == name for row in pages)
              for name in ("UNVERIFIED", "CORRECTION_REQUIRED", "VERIFIED")}
    summary = {
        "phase": "163 R4-R29",
        "input_sha256": digest(original),
        "output_sha256": digest(corrected),
        "confirmed_corrections": len(CHANGES),
        "prior_confirmed_corrections": 12,
        "total_recorded_corrections": 12 + len(CHANGES),
        "printed_page_reviewed": 5,
        "status_counts": counts,
        "page_fully_verified": False,
        "chapter_fully_verified": False,
        "statement_ids_changed": 0,
        "production_code_changed": False,
        "full_suite_run": False,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r29.tex").write_text(original, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(corrected, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(("pdf_page", "printed_page", "status", "scope_hint", "prior_corrections", "evidence_note"))
        for row in pages:
            writer.writerow(tuple(row.get(key, "") for key in ("pdf_page", "printed_page", "status", "scope_hint", "prior_corrections", "evidence_note")))
    with (output / "alignment_review.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(("pdf_page", "printed_page", "item", "before_tex", "after_tex", "original_pdf_evidence", "status"))
        for key, old, new, evidence in CHANGES:
            writer.writerow((1, 5, key, old, new, evidence, "CORRECTED"))
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R29 — 原本印刷5ページの部分照合\n\n"
        "原本 PDF 第1ページ（印刷5ページ）の目視比較に基づく修正。\n\n"
        "- 標準写像の中心からの線分に沿う接ベクトルの向きを、原本の $(-1)\\times\\overrightarrow{c_0x}$ に合わせた。\n"
        "- $t_i,t_j$ の同時交換を、片方の置換と誤読しない日本語に訂正した。\n\n"
        "(1.1)、(1.2)、基点付き写像、ホモトピー集合の説明は今後も逐字照合を要する。"
        "原本の記号 $\\pi(X\\to Y)$ と現代化された $[X,Y]$ の表記差も、確認を残す。\n\n"
        "印刷5ページは引き続き UNVERIFIED。既存 Statement ID、Registry、証明探索は変更しない。"
        "全体 pytest は行わない。\n", encoding="utf-8"
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
