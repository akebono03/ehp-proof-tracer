"""R4-R40: original PDF printed page 8 mathematical-content verification.

The source is retained byte-for-byte in mathematical meaning; the original
mapping-space topology claim is transcribed, not independently proven.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "ece0b13b9ce5c59508c24e1fe756dd6ab99c83e22e74ab495386768d7963b572"
EVIDENCE = (
    ("p8-01", "group-operation continuation", "MATCH", "Printed p.8 opening continues the p.7 assertion: operations on pi(EX->Y) and pi_(n+1)(Y) coincide."),
    ("p8-02", "loop-space definition", "MATCH", "Omega Y is based loops (I^1, boundary I^1)->(Y,y0); Omega f acts by composition."),
    ("p8-03", "loop functor composition", "MATCH", "Original Omega(g o f)=Omega g o Omega f and class-level composition, corresponding to TeX."),
    ("p8-04", "canonical injection (1.9)", "MATCH", "i(x)(t)=d_X(x,t); commuting square X->Y / Omega EX->Omega EY checked by domains and arrows."),
    ("p8-05", "adjunction (1.10)", "MATCH", "Omega_0 F=Omega F o i, Omega_0 F(x)(t)=F(d_X(x,t)); induced bijection of homotopy classes."),
    ("p8-06", "mapping-space compact subsets", "MATCH_WITH_SOURCE_CAVEAT", "Both original and TeX assert a homeomorphism between compact subsets of mapping spaces. Claim is transcribed, not independently validated or strengthened to a homeomorphism of full mapping spaces."),
    ("p8-07", "isomorphism and diagram (1.11)", "MATCH", "Loop multiplication gives group isomorphism; if X is a suspension EX', multiplication matches +; E, i_*, Omega_0 triangle matches."),
    ("p8-08", "naturality (1.12)", "MATCH", "Mappings f:X->Y, g:EY->Z, h:Z->W and four relations, including two homotopy-class equations, checked."),
    ("p8-09", "zero map and (1.13)", "MATCH", "Zero homotopy class and conditions alpha o E^n beta=0, beta o gamma=0 with n>=0 correspond."),
    ("p8-10", "representatives and page boundary", "MATCH_WITH_BOUNDARY", "Printed p.8 defines a:E^nY->Z, b:X->Y, c:W->X as representatives; null homotopies begin on p.9 and are outside page-8 certification."),
)
ANCHORS = (
    r"\Ox Y=", r"\Ox f:", r"\Ox(g\circ f)=", r"i(x)(t) = d_X(x,t)",
    r"\label{eq:loop-susp-comm}", r"\Omega_0F(x)(t) = F(d_X(x,t))",
    r"\Omega_0:\ [EX,Y]", r"\Omega_0(g\circ Ef)",
    r"\alpha\circ \Ex^n\beta=0", r"\beta\circ \gamma=0",
    r"コンパクト部分集合", r"$X$ が suspension $EX'$", r"c:(W,w_0)\to (X,x_0)",
)

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_inputs(text: str, ledger: list[dict]) -> None:
    if sha256(text) != EXPECTED_SHA256:
        raise ValueError("R4-R39 corrected TeX SHA-256 mismatch")
    if len(ledger) != 11 or [r.get("printed_page") for r in ledger] != list(range(5, 16)):
        raise ValueError("Expected ledger for printed pages 5-15")
    if [r.get("status") for r in ledger] != ["VERIFIED"] * 3 + ["UNVERIFIED"] * 8:
        raise ValueError("Unexpected preceding status")
    if any(r.get("source_sha256") != EXPECTED_SHA256 for r in ledger):
        raise ValueError("Ledger source mismatch")
    if any(anchor not in text for anchor in ANCHORS):
        raise ValueError("Original-comparison anchor missing")


def verify_page_eight(text: str, ledger: list[dict]) -> list[dict]:
    validate_inputs(text, ledger)
    updated = json.loads(json.dumps(ledger, ensure_ascii=False))
    page = updated[3]
    page["status"] = "VERIFIED"
    page["verification_scope"] = "MATHEMATICAL_CONTENT_SOURCE_COMPARISON"
    page["verbatim_transcription_verified"] = False
    page["reviewer"] = "R4-R40 original PDF printed p.8 visual comparison"
    page["evidence_note"] = (page.get("evidence_note", "") + " R4-R40: all p.8 mathematical content matched to supplied original, with mapping-space compact-subset assertion retained as source claim (not independently proven); p.9 null-homotopies are outside p.8 scope.").strip()
    page["unresolved_review_topics"] = []
    page["source_claim_independently_proven"] = False
    return updated


def run(source: Path, ledger_path: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    updated = verify_page_eight(text, ledger)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_corrected.tex").write_text(text, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["pdf_page", "printed_page", "status", "verification_scope"], extrasaction="ignore")
        writer.writeheader()
        writer.writerows(updated)
    with (output / "page8_evidence.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["evidence_id", "subject", "assessment", "original_pdf_basis"])
        writer.writerows(EVIDENCE)
    counts = {status: sum(item["status"] == status for item in updated) for status in ("VERIFIED", "UNVERIFIED", "CORRECTION_REQUIRED")}
    summary = {
        "phase": "163 R4-R40", "input_sha256": sha256(text), "output_sha256": sha256(text),
        "reviewed_printed_page": 8, "page8_mathematical_content_verified": True,
        "page8_verbatim_transcription_verified": False, "original_claim_independently_proven": False,
        "evidence_entries": len(EVIDENCE), "new_confirmed_corrections": 0,
        "total_recorded_corrections": 18, "status_counts": counts,
        "chapter_fully_verified": False, "statement_ids_changed": 0,
        "production_code_changed": False, "search_connected": False, "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = """# Phase 163 R4-R40 — 印刷8ページの数学的内容照合

Toda 原本 PDF の4ページ目（印刷8ページ）と修正版 TeX を比較し、10項目の根拠を記録した。

(1.9)〜(1.13)、ループ空間、随伴写像、コンパクト部分集合に関する原典の記述、(1.11) の可換図式と仮定、代表写像 a,b,c を照合した。原典の『compact subsets の間の homeomorphism』という主張は原文のまま保持した。数学的正しさを独立に証明したわけではない。

印刷9ページから始まる null homotopy の説明は次ページの照合対象であり、印刷8ページの VERIFIED 判定には含まない。原本と日本語 TeX の逐語的な一致は認定しない。

今回 TeX 変更0、累計修正18箇所。印刷5〜8ページ VERIFIED、9〜15ページ UNVERIFIED。Statement ID、Registry、証明探索に変更なし。全体 pytest 未実行。
"""
    (output / "report.md").write_text(report, encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.ledger, args.output), ensure_ascii=False, indent=2))
    print("R4-R40 page-eight mathematical content review complete. Full suite not run.")


if __name__ == "__main__":
    main()
