"""R4-R37: retain the original printed formula separately from editorial normalization."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "ece0b13b9ce5c59508c24e1fe756dd6ab99c83e22e74ab495386768d7963b572"
ORIGINAL_FORMULA = r"d_X = \phi_{X,S^n}\circ(1_X\times\psi_1)"
NORMALIZED_FORMULA = r"d_X = \phi_{X,S^1}\circ(1_X\times\psi_1)"
TE_X_ANCHOR = r"d_X = \phi_{X,S^1}\circ (1_X\times \psi_1)"


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate(text: str, ledger: list[dict]) -> None:
    if sha256(text) != EXPECTED_SHA256:
        raise ValueError("R4-R36 input SHA-256 mismatch")
    if TE_X_ANCHOR not in text:
        raise ValueError("Expected d_X anchor missing")
    if len(ledger) != 11 or [x.get("pdf_page") for x in ledger] != list(range(1, 12)):
        raise ValueError("Expected ordered eleven-page ledger")
    if [x.get("status") for x in ledger] != ["VERIFIED"] * 2 + ["UNVERIFIED"] * 9:
        raise ValueError("Unexpected page status")
    if any(x.get("source_sha256") != EXPECTED_SHA256 for x in ledger):
        raise ValueError("Ledger source SHA-256 mismatch")
    if len(ledger[2].get("unresolved_original_discrepancies", [])) != 1:
        raise ValueError("R4-R36 source discrepancy evidence missing")


def source_record() -> dict:
    return {
        "record_key": "toda_ch1_p7_dx_formula",
        "printed_page": 7,
        "pdf_page": 3,
        "subject": "suspension canonical map d_X",
        "source_formula_tex": ORIGINAL_FORMULA,
        "editorial_normalization_tex": NORMALIZED_FORMULA,
        "original_witness": "Supplied Toda_01.pdf, printed p.7, d_X definition",
        "mathematical_basis": [
            "d_X is specified on X × I^1",
            "psi_1 maps I^1 to S^1",
            "EX = X wedge S^1",
        ],
        "source_transcription_status": "VISUALLY_CONFIRMED",
        "normalization_status": "MATHEMATICALLY_MOTIVATED_NOT_ORIGINAL_PRINT",
        "source_typo_status": "POSSIBLE_NOT_ESTABLISHED",
        "proof_search_eligible": False,
        "printed_source_overwritten": False,
        "editorial_tex_modified": False,
    }


def reconcile(text: str, ledger: list[dict]) -> tuple[list[dict], dict]:
    validate(text, ledger)
    updated = json.loads(json.dumps(ledger, ensure_ascii=False))
    page = updated[2]
    page["status"] = "UNVERIFIED"
    page["verification_scope"] = "PARTIAL_MATHEMATICAL_REVIEW_SOURCE_NORMALIZATION_SEPARATED"
    page["verbatim_transcription_verified"] = False
    page["source_normalization_record_key"] = "toda_ch1_p7_dx_formula"
    page["unresolved_original_discrepancies"] = [{
        "reference": "printed p.7 d_X",
        "original_printed": ORIGINAL_FORMULA,
        "current_tex": NORMALIZED_FORMULA,
        "status": "SOURCE_RETAINED_NORMALIZATION_DOCUMENTED_TYPO_UNDECIDED",
        "auto_corrected": False,
    }]
    page["evidence_note"] = (page.get("evidence_note", "") +
        " R4-R37: PDF source S^n and mathematically motivated TeX S^1 retained separately;"
        " no assertion that the original is a confirmed typo; page still unverified.")
    return updated, source_record()


def run(source: Path, ledger_path: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    updated, record = reconcile(text, ledger)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_corrected.tex").write_text(text, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "source_normalization.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        columns = ("pdf_page", "printed_page", "status", "verification_scope")
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(updated)
    summary = {
        "phase": "163 R4-R37",
        "input_sha256": sha256(text),
        "output_sha256": sha256(text),
        "reviewed_printed_page": 7,
        "original_and_normalization_recorded": True,
        "original_typo_confirmed": False,
        "pending_page7_review": True,
        "new_confirmed_corrections": 0,
        "total_recorded_corrections": 18,
        "status_counts": {key: sum(x["status"] == key for x in updated) for key in ("VERIFIED", "UNVERIFIED", "CORRECTION_REQUIRED")},
        "chapter_fully_verified": False,
        "statement_ids_changed": 0,
        "production_code_changed": False,
        "search_connected": False,
        "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R37 — 原本表記と数学的正規化の分離\n\n"
        "印刷7ページの $d_X$ について、原本の $\\phi_{X,S^n}$ と数学的に自然な $\\phi_{X,S^1}$ を別個に記録した。\n\n"
        "原本の誤植と断定しない。$d_X:X\\times I^1\\to EX$、$\\psi_1:I^1\\to S^1$、$EX=X\\wedge S^1$ から正規化の根拠を記録。\n\n"
        "TeX 変更0、累計修正18。印刷5・6ページのみ VERIFIED。印刷7ページは UNVERIFIED。\n\n"
        "印刷7ページの残りの文章・記号について、この監査だけでは全文照合を完了していない。原典 PDF と逐字一致は保証しない。\n\n"
        "既存 Registry・Statement ID・証明探索を変更せず、全体 pytest は実施しない。\n",
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
    print("R4-R37 source notation audit complete. Full suite not run.")


if __name__ == "__main__":
    main()
