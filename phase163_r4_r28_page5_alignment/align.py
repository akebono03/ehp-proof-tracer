"""R4-R28: verified page-5 coordinate-index corrections, fail closed."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "c36eaa063d86ae92d813ee83ad54c3c92f9b8a36f0f0f067a5b746e96b1c1da3"
CHANGES = (
    ("coordinate_sign", r"\(s_{i}\geq0\ (s_{i}\leq0)\)", r"\(s_{i+1}\geq0\ (s_{i+1}\leq0)\)"),
    ("coordinate_reflection", "\\(s_{i}\\)\nは\n\\(-s_{i}\\)", "\\(s_{i+1}\\)\nは\n\\(-s_{i+1}\\)"),
    ("coordinate_exchange", "\\(s_{i}\\)\nと\n\\(s_{j}\\)", "\\(s_{i+1}\\)\nと\n\\(s_{j+1}\\)"),
)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def correct_page5(text: str) -> str:
    if digest(text) != EXPECTED_SHA256:
        raise ValueError("R4-R26 canonical TeX SHA-256 mismatch; no changes applied")
    for label, before, after in CHANGES:
        if text.count(before) != 1 or after in text:
            raise ValueError(f"Ambiguous or already-applied correction: {label}")
        text = text.replace(before, after, 1)
    return text


def update_ledger(pages: list[dict], source_hash: str, new_hash: str) -> list[dict]:
    if len(pages) != 11 or [p.get("pdf_page") for p in pages] != list(range(1, 12)):
        raise ValueError("Expected eleven pages in existing ledger")
    if any(p.get("source_sha256") != source_hash for p in pages):
        raise ValueError("Existing ledger is not associated with baseline TeX")
    updated = json.loads(json.dumps(pages, ensure_ascii=False))
    for page in updated:
        page["source_sha256"] = new_hash
    first = updated[0]
    if first["status"] != "UNVERIFIED":
        raise ValueError("Page 1 has unexpected status")
    first["prior_corrections"] = int(first["prior_corrections"]) + 3
    first["evidence_note"] = (
        "Printed p.5/PDF p.1: t_i relates to s_{i+1}; "
        "sign, reflection, and coordinate exchange corrected. "
        "Remaining content not exhaustively verified."
    )
    first["status"] = "UNVERIFIED"
    return updated


def run(source: Path, ledger_path: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    corrected = correct_page5(text)
    previous = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    new_hash = digest(corrected)
    updated = update_ledger(previous, digest(text), new_hash)
    summary = {
        "phase": "163 R4-R28", "input_sha256": digest(text),
        "output_sha256": new_hash, "confirmed_corrections": len(CHANGES),
        "prior_confirmed_corrections": 9, "total_recorded_corrections": 12,
        "status_counts": {s: sum(row["status"] == s for row in updated)
                          for s in ("UNVERIFIED", "CORRECTION_REQUIRED", "VERIFIED")},
        "printed_page_reviewed": 5, "page_fully_verified": False,
        "chapter_fully_verified": False, "statement_ids_changed": 0,
        "production_code_changed": False, "full_suite_run": False,
    }
    # All validation above finishes before making output directory.
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r28.tex").write_text(text, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(corrected, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("pdf_page", "printed_page", "status", "scope_hint", "prior_corrections", "evidence_note"))
        for p in updated:
            writer.writerow([p[k] for k in ("pdf_page", "printed_page", "status", "scope_hint", "prior_corrections", "evidence_note")])
    with (output / "alignment_review.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("pdf_page", "printed_page", "item", "before_tex", "after_tex", "source_evidence", "status"))
        for label, before, after in CHANGES:
            writer.writerow((1, 5, label, before, after, "Original PDF p.1, printed p.5, after (1.2)", "CORRECTED"))
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R28 — 原本印刷5ページの照合\n\n"
        "Toda 原本 PDF 1ページ（印刷5ページ）の標準写像 $\\psi_n$ の座標添字を照合した。\n\n"
        "- 符号条件：$s_i$ から $s_{i+1}$ に訂正。\n"
        "- $t_i \\mapsto 1-t_i$ による反転：$s_{i+1} \\mapsto -s_{i+1}$ に訂正。\n"
        "- $t_i,t_j$ の交換：$s_{i+1},s_{j+1}$ の交換に訂正。\n\n"
        "今回の訂正は3箇所。過去9箇所を保持。\n"
        "印刷5ページの全要素の逐字照合は未完了なのでページ状態は UNVERIFIED のまま。\n"
        "印刷原本を正とし、TeX 本体や Registry を上書きしない。\n"
        "既存の Statement ID と証明探索は変更せず、全体 pytest は実施しない。\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.ledger, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
