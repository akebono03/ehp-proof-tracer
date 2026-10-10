"""Phase 163 R4-R31: source-grounded mathematical review of printed page 5.

This is a review ledger update, not a transformation of the TeX source.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "521b481431b862b2c278069223c4990f36cf4fb6164987de78d75d1da47c7a82"
REVIEW_FIELDS = (
    "definitions", "equations", "named_statements", "proofs_and_prose", "notation_and_conditions"
)
EVIDENCE = (
    ("definitions", "Printed p.5: I^n, S^n, psi_n and designated basepoints", "TeX lines 75-106, 145-146", "MATCH_SEMANTIC"),
    ("equations", "Printed p.5 (1.1), (1.2), psi_1 and psi_{n+1} restrictions", "TeX lines 86-143; R4-R28 through R4-R30 corrections", "MATCH_SEMANTIC"),
    ("named_statements", "No named Lemma/Proposition/Theorem on printed p.5", "TeX heading through homotopy groups", "NOT_APPLICABLE"),
    ("proofs_and_prose", "Center and boundary map, great semicircle, basepoint-preserving homotopy", "TeX lines 91-106, 145-160", "MATCH_SEMANTIC"),
    ("notation_and_conditions", "Original pi(X -> Y), TeX [X,Y]; original f: (X,x0) -> (Y,y0); H(x0,t)=y0", "TeX lines 147-160", "MATCH_WITH_NOTATION_NORMALIZATION"),
)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_inputs(tex: str, ledger: list[dict]) -> None:
    if sha256(tex) != EXPECTED_SHA256:
        raise ValueError("R4-R30 TeX SHA-256 mismatch; nothing updated")
    if len(ledger) != 11 or [p.get("pdf_page") for p in ledger] != list(range(1, 12)):
        raise ValueError("Expected ordered PDF pages 1 through 11")
    if any(row.get("source_sha256") != EXPECTED_SHA256 for row in ledger):
        raise ValueError("Page ledger does not match R4-R30 TeX")
    if any(row.get("status") != "UNVERIFIED" for row in ledger):
        raise ValueError("Unexpected prior verification status")
    required = (
        r"\psi_n:I^n\longrightarrow S^n",
        r"\psi_1(t) = (\cos 2\pi t,\ \sin 2\pi t).",
        r"[X,Y]=\{\, [f]\ \mid\ f:(X,x_0)\to (Y,y_0)\,\}",
        r"H(x_0, t) = y_0",
    )
    for token in required:
        if token not in tex:
            raise ValueError(f"Expected page-five material absent: {token}")


def verify_page_five(ledger: list[dict]) -> list[dict]:
    result = json.loads(json.dumps(ledger, ensure_ascii=False))
    page = result[0]
    for field in REVIEW_FIELDS:
        page["review"][field] = True
    page["status"] = "VERIFIED"
    page["reviewer"] = "R4-R31 original PDF page 1 visual mathematical comparison"
    page["verification_scope"] = "MATHEMATICAL_CONTENT_AND_CONDITIONS"
    page["verbatim_transcription_verified"] = False
    page["notation_normalizations"] = [
        "Original pi(X -> Y) represented in Japanese TeX by [X,Y]",
        "Original English prose translated into Japanese",
    ]
    page["evidence_note"] = (
        str(page.get("evidence_note", ""))
        + " R4-R31: all printed p.5 mathematical definitions, displayed equations, "
        + "coordinate properties, prose conditions and the absence of named statements "
        + "reviewed against original PDF p.1. Mathematical semantic verification "
        + "complete. Not a verbatim transcription certification; notation and language "
        + "normalization retained."
    ).strip()
    return result


def run(source: Path, ledger_path: Path, output: Path) -> dict:
    tex = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    validate_inputs(tex, ledger)
    updated = verify_page_five(ledger)
    counts = {status: sum(p["status"] == status for p in updated) for status in (
        "UNVERIFIED", "CORRECTION_REQUIRED", "VERIFIED"
    )}
    summary = {
        "phase": "163 R4-R31",
        "input_sha256": sha256(tex),
        "output_sha256": sha256(tex),
        "reviewed_printed_page": 5,
        "page5_mathematical_content_verified": True,
        "page5_verbatim_transcription_verified": False,
        "new_confirmed_corrections": 0,
        "prior_confirmed_corrections": 15,
        "total_recorded_corrections": 15,
        "status_counts": counts,
        "chapter_fully_verified": all(p["status"] == "VERIFIED" for p in updated),
        "statement_ids_changed": 0,
        "production_code_changed": False,
        "full_suite_run": False,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_corrected.tex").write_text(tex, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("pdf_page", "printed_page", "status", "verification_scope", "prior_corrections", "evidence_note"))
        for row in updated:
            writer.writerow([row.get(k, "") for k in ("pdf_page", "printed_page", "status", "verification_scope", "prior_corrections", "evidence_note")])
    with (output / "page5_evidence.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("review_field", "original_pdf_evidence", "tex_evidence", "review_result"))
        writer.writerows(EVIDENCE)
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R31 — 原本印刷5ページの数学的内容照合\n\n"
        "- 原本 PDF 1ページ（印刷5ページ）と R4-R30 修正版 TeX を対比。\n"
        "- 定義、式 (1.1)、(1.2)、$\\psi_1$、座標性質、基点保存条件、ホモトピー類の対応を点検。\n"
        "- 原本の $\\pi(X\\to Y)$ は TeX で $[X,Y]$ と記す。数学的内容の一致として扱い、原本と逐字同一とは判定しない。\n"
        "- 日本語訳や記号置換を明記した上で、印刷5ページの数学的内容を `VERIFIED` とする。\n"
        "- 今回の新規 TeX 修正は0件。R4-R21〜R4-R30 の15箇所を維持。\n"
        "- 他の10ページは `UNVERIFIED`。第1章全体の原本照合は未完了。\n"
        "- Statement ID、Registry、Backward Search は変更しない。全体 pytest は実施しない。\n",
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
