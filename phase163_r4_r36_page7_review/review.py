"""R4-R36: conservative original-PDF page-seven mathematical review.

The original visibly prints S^n in the d_X formula while the prior Japanese
TeX uses S^1. The audit must not silently resolve this conflict.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "ece0b13b9ce5c59508c24e1fe756dd6ab99c83e22e74ab495386768d7963b572"
EVIDENCE = (
    ("boundary_p6_p7", "printed p.7 top", "(1.4) gives (1.5)", "MATCHED_MATHEMATICAL_CONTENT", "Connection to preceding page is retained"),
    ("equation_1_5", "printed p.7 (1.5)", "Associativity and composition laws for reduced join", "MATCHED_MATHEMATICAL_CONTENT", "Original # represented as wedge"),
    ("suspension_objects", "printed p.7 after (1.5)", "E^n X = X # S^n and iterated suspension", "MATCHED_MATHEMATICAL_CONTENT", "Original # represented as wedge"),
    ("equation_1_6", "printed p.7 (1.6)", "Homotopy, iterated suspension, composition", "MATCHED_MATHEMATICAL_CONTENT", "Check boundaries and conditions before final certification"),
    ("d_x_source_conflict", "printed p.7 d_X definition", "PDF prints phi_{X,S^n} with psi_1, whereas corrected TeX uses phi_{X,S^1}", "ORIGINAL_MATH_CONFLICT", "Printed n may itself be a source typo: no silent replacement"),
    ("suspension_map", "printed p.7 after d_X", "Ef(d_X(x,t))=d_Y(f(x),t)", "MATCHED_MATHEMATICAL_CONTENT", "Page not fully certified"),
    ("addition_negation", "printed p.7 below d_X", "Two-piece f+g and reversal -f", "MATCHED_MATHEMATICAL_CONTENT", "Original t interval notation retained semantically"),
    ("equation_1_7", "printed p.7 (1.7)", "Induced homomorphisms and abelian n-fold suspension for n>=2", "MATCHED_MATHEMATICAL_CONTENT", "Original pi(X->Y) represented as [X,Y]"),
    ("equation_1_8", "printed p.7 (1.8)", "d_n:S^n x I^1 -> S^(n+1) and psi_(n+1) formula", "MATCHED_MATHEMATICAL_CONTENT", "Original I^1 represented by I in TeX"),
)
REQUIRED = (
    r"(\alpha\wedge\beta)\wedge\gamma",
    r"\Ex^n X\ :=\ X\ \wedge\ S^n",
    r"E^n(E^m\alpha)",
    r"d_X = \phi_{X,S^1}\circ (1_X\times \psi_1)",
    r"\Ex f(d_X(x, t))",
    r"(-f)(d_X(x, t))",
    r"\label{eq:toda-1-7}",
    r"d_n:S^n\times I\longrightarrow S^{n+1}",
)

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def validate_inputs(text: str, ledger: list[dict]) -> None:
    if sha256(text) != EXPECTED_SHA256:
        raise ValueError("R4-R35 source SHA-256 mismatch; output not written")
    if len(ledger) != 11 or [row.get("pdf_page") for row in ledger] != list(range(1, 12)):
        raise ValueError("Expected eleven ordered original PDF pages")
    if [row.get("status") for row in ledger] != ["VERIFIED", "VERIFIED"] + ["UNVERIFIED"] * 9:
        raise ValueError("Unexpected prior page verification statuses")
    if any(row.get("source_sha256") != EXPECTED_SHA256 for row in ledger):
        raise ValueError("Page ledger SHA-256 differs from source")
    missing = [item for item in REQUIRED if item not in text]
    if missing:
        raise ValueError("Expected original comparison anchors missing: " + repr(missing))

def review_page_seven(text: str, ledger: list[dict]) -> list[dict]:
    validate_inputs(text, ledger)
    updated = json.loads(json.dumps(ledger, ensure_ascii=False))
    page = updated[2]
    page["status"] = "UNVERIFIED"
    page["verification_scope"] = "PARTIAL_ORIGINAL_COMPARISON_WITH_CONFLICT"
    page["verbatim_transcription_verified"] = False
    page["reviewer"] = "R4-R36 visual comparison of supplied Toda PDF page 3"
    page["evidence_note"] = (page.get("evidence_note", "") + " R4-R36: (1.5)-(1.8) and suspension operations compared to original printed p.7; the original d_X formula prints S^n, but TeX corrected in R4-R22 says S^1. Not resolved or declared verified.").strip()
    page["unresolved_original_discrepancies"] = [
        {"reference": "printed p.7 d_X", "original_printed": "phi_{X,S^n} (1_X x psi_1)",
         "current_tex": "phi_{X,S^1} (1_X x psi_1)",
         "status": "REQUIRES_EXPLICIT_SOURCE_TYPO_POLICY", "auto_corrected": False}
    ]
    return updated

def run(source: Path, ledger_path: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    updated = review_page_seven(text, ledger)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_corrected.tex").write_text(text, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("pdf_page", "printed_page", "status", "verification_scope", "evidence_note"))
        for row in updated:
            writer.writerow([row.get(k, "") for k in ("pdf_page", "printed_page", "status", "verification_scope", "evidence_note")])
    with (output / "page7_evidence.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("topic", "original_position", "comparison", "status", "notes"))
        writer.writerows(EVIDENCE)
    summary = {
        "phase": "163 R4-R36", "input_sha256": sha256(text), "output_sha256": sha256(text),
        "reviewed_printed_page": 7, "comparison_entries": len(EVIDENCE),
        "unresolved_original_math_discrepancies": 1,
        "page7_mathematical_content_verified": False,
        "page7_verbatim_transcription_verified": False,
        "new_confirmed_corrections": 0, "prior_confirmed_corrections": 18,
        "total_recorded_corrections": 18,
        "status_counts": {s: sum(row["status"] == s for row in updated)
                          for s in ("VERIFIED", "UNVERIFIED", "CORRECTION_REQUIRED")},
        "chapter_fully_verified": False, "statement_ids_changed": 0,
        "production_code_changed": False, "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R36 — 印刷7ページの原本照合（部分監査）\n\n"
        "- 印刷7ページ（PDF 3ページ目）の式 (1.5)〜(1.8) と本文を照合した。\n"
        "- 原本の $d_X$ の式では $\\phi_{X,S^n}$ と印刷される一方、"
        "R4-R22 以来の修正済み TeX は $\\phi_{X,S^1}$ である。\n"
        "- 定義域 $X\\times I^1$ と $\\psi_1$ を考えると $S^1$ は数学的に自然だが、"
        "原本忠実転記との相違を勝手に消さない。原本自体の誤植の可能性は未確定。\n"
        "- TeX の修正は0件、累計18件。ページ7は UNVERIFIED。\n"
        "- 原本の # と TeX の $\\wedge$、原本の $\\pi(X\\to Y)$ と TeX の $[X,Y]$ は記法の対応として保持。\n"
        "- ページ5・6は VERIFIED、ページ7〜15は UNVERIFIED。\n"
        "- Statement ID、既存 Registry、Proof Search の変更なし。全体 pytest は未実施。\n",
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
