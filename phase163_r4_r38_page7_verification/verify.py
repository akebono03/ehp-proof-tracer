"""R4-R38: evidence-based mathematical comparison for Toda printed page 7."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "ece0b13b9ce5c59508c24e1fe756dd6ab99c83e22e74ab495386768d7963b572"
NORMALIZATION_KEY = "toda_ch1_p7_dx_formula"

EVIDENCE = (
    ("p7-01", "(1.5) reduced join relations", "MATHEMATICAL_MATCH", "Original p.7 equations i), ii); editorial wedge replaces original #."),
    ("p7-02", "n-fold suspension space and associativity", "MATHEMATICAL_MATCH", "Original p.7 E^n X = X # S^n and E^n E^m X = E^(m+n) X."),
    ("p7-03", "suspension of maps and (1.6)", "MATHEMATICAL_MATCH", "Original p.7 equations 0), i), ii) and source/target."),
    ("p7-04", "d_X domain and exceptional original typography", "NORMALIZED_EXCEPTION", "Original p.7 phi_(X,S^n) versus editorial phi_(X,S^1), recorded separately by R4-R37. Original typo not established."),
    ("p7-05", "d_X quotient and Ef", "MATHEMATICAL_MATCH", "Original p.7 collapse of X x boundary I and basepoint x0 x I, Ef formula."),
    ("p7-06", "addition and inverse on [EX,Y]", "MATHEMATICAL_MATCH", "Original p.7 two-branch + formula and reversal for -f."),
    ("p7-07", "group structure and mapping space", "MATHEMATICAL_MATCH", "Original p.7 group and locally compact X comparison with pi_1 mapping space."),
    ("p7-08", "(1.7) homomorphism and abelian n-fold case", "MATHEMATICAL_MATCH", "Original p.7 f_* and (Eg)^*, homomorphism relations, n >= 2."),
    ("p7-09", "(1.8) sphere d_n and boundary text", "MATHEMATICAL_MATCH", "Original p.7 domain S^n x I^1, formula via psi_(n+1); the sentence at top continues from p.6."),
)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_inputs(text: str, ledger: list[dict], normalization: dict) -> None:
    if sha256(text) != EXPECTED_SHA256:
        raise ValueError("R4-R37 corrected TeX SHA-256 mismatch")
    if len(ledger) != 11 or [x.get("printed_page") for x in ledger] != list(range(5, 16)):
        raise ValueError("Eleven-page ledger in printed order required")
    if [x.get("status") for x in ledger] != ["VERIFIED"] * 2 + ["UNVERIFIED"] * 9:
        raise ValueError("Unexpected prior ledger statuses")
    if any(x.get("source_sha256") != EXPECTED_SHA256 for x in ledger):
        raise ValueError("Ledger source SHA-256 mismatch")
    if normalization.get("record_key") != NORMALIZATION_KEY:
        raise ValueError("R4-R37 normalization evidence missing")
    if normalization.get("source_typo_status") != "POSSIBLE_NOT_ESTABLISHED":
        raise ValueError("Original typo status must remain undecided")
    if normalization.get("proof_search_eligible") is not False:
        raise ValueError("Normalization must not enable proof search")
    if normalization.get("source_formula_tex") == normalization.get("editorial_normalization_tex"):
        raise ValueError("Original and editorial normalization not separated")
    anchors = (r"\Ex^n X\ :=\ X\ \wedge\ S^n", r"d_X = \phi_{X,S^1}\circ (1_X\times \psi_1)",
               r"\label{eq:toda-1-7}", r"d_n:S^n\times I\longrightarrow S^{n+1}")
    if any(anchor not in text for anchor in anchors):
        raise ValueError("Expected page-seven mathematical anchors missing")


def verify_page_seven(text: str, ledger: list[dict], normalization: dict) -> list[dict]:
    validate_inputs(text, ledger, normalization)
    updated = json.loads(json.dumps(ledger, ensure_ascii=False))
    page = updated[2]
    page["status"] = "VERIFIED"
    page["verification_scope"] = "MATHEMATICAL_CONTENT_VERIFIED_WITH_DOCUMENTED_SOURCE_NORMALIZATION"
    page["verbatim_transcription_verified"] = False
    page["original_typo_confirmed"] = False
    page["source_normalization_record_key"] = NORMALIZATION_KEY
    page["review"] = {k: True for k in ("definitions", "equations", "named_statements", "proofs_and_prose", "notation_and_conditions")}
    page["reviewer"] = "R4-R38 visual mathematical comparison of supplied original PDF page 3"
    page["unresolved_original_discrepancies"] = [{
        "reference": "printed p.7 d_X",
        "original_printed": normalization["source_formula_tex"],
        "current_tex": normalization["editorial_normalization_tex"],
        "status": "DOCUMENTED_SOURCE_NORMALIZATION_EXCEPTION_ORIGINAL_TYPO_UNDECIDED",
        "auto_corrected": False,
        "proof_search_eligible": False,
    }]
    page["evidence_note"] = page.get("evidence_note", "") + " R4-R38: mathematical content of original printed p.7 reviewed; (1.5)-(1.8), suspension, group operations and page-boundary prose compared; original d_X S^n kept as explicit exception against S^1 editorial normalization; this is not verbatim verification or proof of original typo."
    assert sum(x["status"] == "VERIFIED" for x in updated) == 3
    return updated


def run(source: Path, ledger_path: Path, normalization_path: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    normalization = json.loads(normalization_path.read_text(encoding="utf-8-sig"))
    updated = verify_page_seven(text, ledger, normalization)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_corrected.tex").write_text(text, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "source_normalization.json").write_text(json.dumps(normalization, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["pdf_page", "printed_page", "status", "verification_scope"], extrasaction="ignore")
        writer.writeheader(); writer.writerows(updated)
    with (output / "page7_evidence.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream); writer.writerow(["evidence_id", "subject", "assessment", "source_basis"]); writer.writerows(EVIDENCE)
    summary = {
        "phase": "163 R4-R38", "input_sha256": sha256(text), "output_sha256": sha256(text),
        "reviewed_printed_page": 7, "page7_mathematical_content_verified": True,
        "page7_verbatim_transcription_verified": False, "source_normalization_exception_count": 1,
        "original_typo_confirmed": False, "evidence_entries": len(EVIDENCE),
        "new_confirmed_corrections": 0, "total_recorded_corrections": 18,
        "status_counts": {k: sum(x["status"] == k for x in updated) for k in ("VERIFIED", "UNVERIFIED", "CORRECTION_REQUIRED")},
        "chapter_fully_verified": False, "statement_ids_changed": 0,
        "production_code_changed": False, "search_connected": False, "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = ("# Phase 163 R4-R38 — Toda 原本印刷7ページの数学的照合\n\n"
              "原本 PDF の印刷7ページについて、(1.5)〜(1.8)、懸垂、群演算、ページ境界の説明を照合した。\n\n"
              "原本の $d_X=\\phi_{X,S^n}\\circ(1_X\\times\\psi_1)$ と編集上の正規化 $d_X=\\phi_{X,S^1}\\circ(1_X\\times\\psi_1)$ は引き続き分離する。原本の誤植と断定せず、例外を保存する。\n\n"
              "印刷7ページの数学的内容を VERIFIED とするが、逐字一致ではない。原本の文字列との差異は登録時にも表示し、証明探索には自動接続しない。\n\n"
              "新規 TeX 修正0、累計18。VERIFIED は印刷5〜7ページの3ページ。未確認は8〜15ページの8ページ。\n\n"
              "既存 API・Statement ID を変更しない。全体 pytest は実行しない。\n")
    (output / "report.md").write_text(report.replace("\n", "\n"), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.ledger, args.normalization, args.output), ensure_ascii=False, indent=2))
    print("R4-R38 page-seven mathematical comparison complete. Full suite not run.")


if __name__ == "__main__":
    main()
