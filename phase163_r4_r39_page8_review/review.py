"""R4-R39: read-only, source-grounded audit of Toda printed page 8."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "ece0b13b9ce5c59508c24e1fe756dd6ab99c83e22e74ab495386768d7963b572"
EVIDENCE = (
    ("p8-01", "group law continuation", "PARTIAL_MATCH", "Printed page 8 begins with agreement of the two group laws; compare preceding page 7."),
    ("p8-02", "loop space and induced Omega f", "MATHEMATICAL_MATCH", "Original defines loops (I^1, boundary I^1) -> (Y,y0), (Omega f(l))(t)=f(l(t))."),
    ("p8-03", "loop homotopy and composition", "MATHEMATICAL_MATCH", "Original gives Omega(g compose f)=Omega g compose Omega f, with class relation."),
    ("p8-04", "canonical injection and (1.9)", "MATHEMATICAL_MATCH", "Original i(x)(t)=d_X(x,t), commutative square X,Y,Omega EX,Omega EY."),
    ("p8-05", "adjunction (1.10)", "MATHEMATICAL_MATCH", "Original Omega_0 F=Omega F compose i; bijection pi(EX->Y) and pi(X->Omega Y)."),
    ("p8-06", "mapping-space compact-subset topology", "REQUIRES_CONTEXT_REVIEW", "Original explicitly says homeomorphism between compact subsets of mapping spaces; precise topology/translation not fully resolved."),
    ("p8-07", "group isomorphism and (1.11)", "PARTIAL_MATCH", "Original commutative diagram and group multiplication; diagram domains and suspension premise need final proofread."),
    ("p8-08", "naturality (1.12)", "MATHEMATICAL_MATCH", "Original lists two mapping equations and two homotopy class equations for f, g, h."),
    ("p8-09", "zero class and (1.13)", "MATHEMATICAL_MATCH", "Original defines zero class then imposes alpha compose E^n beta=0, beta compose gamma=0."),
    ("p8-10", "representative maps and page boundary", "REQUIRES_CONTEXT_REVIEW", "Original at end of printed page 8 introduces a,b,c; null-homotopies start on printed page 9."),
)
ANCHORS = (
    r"\Ox Y=", r"\Ox f:", r"\Ox(g\circ f)=", r"i(x)(t) = d_X(x,t)",
    r"\label{eq:loop-susp-comm}", r"\Omega_0F(x)(t) = F(d_X(x,t))",
    r"\Omega_0:\ [EX,Y]", r"\Omega_0(g\circ Ef)",
    r"\alpha\circ \Ex^n\beta=0", r"\beta\circ \gamma=0",
)

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def validate_inputs(text: str, ledger: list[dict]) -> None:
    if sha256(text) != EXPECTED_SHA256:
        raise ValueError("R4-R38 corrected TeX SHA-256 mismatch")
    if len(ledger) != 11 or [row.get("printed_page") for row in ledger] != list(range(5,16)):
        raise ValueError("Expected 11 printed pages 5-15")
    if [row.get("status") for row in ledger] != ["VERIFIED"] * 3 + ["UNVERIFIED"] * 8:
        raise ValueError("Unexpected preceding verification states")
    if any(row.get("source_sha256") != EXPECTED_SHA256 for row in ledger):
        raise ValueError("Ledger does not match input TeX")
    if any(anchor not in text for anchor in ANCHORS):
        raise ValueError("Required original comparison anchor missing")

def review_page_eight(text: str, ledger: list[dict]) -> list[dict]:
    validate_inputs(text, ledger)
    updated = json.loads(json.dumps(ledger, ensure_ascii=False))
    page = updated[3]
    page["status"] = "UNVERIFIED"
    page["verification_scope"] = "PARTIAL_MATHEMATICAL_COMPARISON"
    page["verbatim_transcription_verified"] = False
    page["reviewer"] = "R4-R39 visual comparison against supplied original PDF page 4"
    page["evidence_note"] = page.get("evidence_note", "") + " R4-R39: original printed p.8 compared in ten sections; mapping-space topology and page-boundary continuation require final review. Not certified as VERIFIED."
    page["unresolved_review_topics"] = ["mapping-space compact subset topology", "equation (1.11) diagram and premise final proofread", "representative map boundary to printed p.9"]
    return updated

def run(source: Path, ledger_path: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    updated = review_page_eight(text, ledger)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_corrected.tex").write_text(text, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(updated, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    with (output / "page_ledger.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["pdf_page","printed_page","status","verification_scope"],extrasaction="ignore")
        w.writeheader();w.writerows(updated)
    with (output / "page8_evidence.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(["evidence_id","subject","assessment","source_basis"]);w.writerows(EVIDENCE)
    status={key:sum(p["status"]==key for p in updated) for key in ("VERIFIED","UNVERIFIED","CORRECTION_REQUIRED")}
    summary={"phase":"163 R4-R39","input_sha256":sha256(text),"output_sha256":sha256(text),"reviewed_printed_page":8,"evidence_entries":len(EVIDENCE),"new_confirmed_corrections":0,"total_recorded_corrections":18,"page8_mathematical_content_verified":False,"status_counts":status,"chapter_fully_verified":False,"statement_ids_changed":0,"production_code_changed":False,"search_connected":False,"full_suite_run":False}
    (output / "summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (output / "report.md").write_text("# Phase 163 R4-R39 — 印刷8ページの原本照合\n\nToda 原本 PDF の4ページ目（印刷8ページ）と R4-R38 の修正版 TeX を照合した。\n\n(1.9)〜(1.13)、ループ空間、写像の合成、随伴の数式は対応位置を確認。写像空間の compact subsets に関する位相的主張、(1.11) の図式および9ページへ続く境界を追加確認する。\n\n照合記録は10項目。新規 TeX 修正は0、累計18箇所。印刷8ページは UNVERIFIED を維持する。原本と数学的に同値な記法の違いを自動修正しない。\n\n既存 Registry、Statement ID、Backward Search は変更していない。全体 pytest は未実行。\n",encoding="utf-8")
    return summary

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--ledger",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(run(a.source,a.ledger,a.output),ensure_ascii=False,indent=2))
    print("R4-R39 partial page 8 comparison complete. Full suite not run.")

if __name__ == "__main__":
    main()
