"""Phase 163 R4-R27: fail-closed page-by-page original alignment ledger.

This tool does not modify Toda's TeX or certify an unchecked PDF page.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_R26_SHA256 = "c36eaa063d86ae92d813ee83ad54c3c92f9b8a36f0f0f067a5b746e96b1c1da3"
PDF_PAGE_COUNT = 11
REVIEW_FIELDS = ("definitions", "equations", "named_statements", "proofs_and_prose", "notation_and_conditions")
PAGE_TOPICS = (
    "章冒頭、球面・写像・ホモトピー集合の導入",
    "写像の合成、reduced join、(1.3)〜(1.4)",
    "懸垂・ループ空間、(1.5)〜(1.8)",
    "ループ写像、随伴、(1.9)〜(1.13)",
    "二次合成の定義、Lemma 1.1",
    "Proposition 1.2 と証明",
    "Proposition 1.2 証明の続き、Proposition 1.3",
    "Proposition 1.4〜1.6 の周辺",
    "Proposition 1.6 の証明、Proposition 1.7",
    "Proposition 1.8〜1.9 と証明",
    "Proposition 1.9 の証明の続き",
)
# 修正位置の過去記録。ページの全文照合済みを意味しない。
CORRECTION_HISTORY = (
    ("R4-R21", 2, "(1.3) の次元・写像の修正", 1),
    ("R4-R22", 3, "suspension d_X の定義", 1),
    ("R4-R22", 3, "(1.7) の写像記述", 1),
    ("R4-R23", 6, "Proposition 1.2 iii) の括弧", 1),
    ("R4-R24", 8, "Proposition 1.6 の懸垂条件", 1),
    ("R4-R24", 10, "Proposition 1.9 の extension 定義域", 1),
    ("R4-R25", 8, "Proposition 1.6 証明の懸垂記号", 1),
    ("R4-R26", 10, "Proposition 1.9 証明の beta 上線 (2箇所)", 2),
)


def read_tex(source: Path) -> str:
    return source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def validate_source(source: Path) -> tuple[str, str]:
    content = read_tex(source)
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    if digest != EXPECTED_R26_SHA256:
        raise ValueError("R4-R26 の修正版 TeX SHA-256 が一致しません。出力は変更しません")
    return content, digest


def make_ledger(digest: str) -> list[dict[str, object]]:
    pages: list[dict[str, object]] = []
    for i, topic in enumerate(PAGE_TOPICS, start=1):
        corrections = sum(count for _phase, page, _item, count in CORRECTION_HISTORY if page == i)
        pages.append({
            "pdf_page": i,
            "printed_page": i + 4,
            "scope_hint": topic,
            "status": "UNVERIFIED",
            "source_sha256": digest,
            "prior_corrections": corrections,
            "review": {key: False for key in REVIEW_FIELDS},
            "reviewer": "",
            "evidence_note": "",
        })
    return pages


def validate_ledger(pages: list[dict[str, object]], digest: str) -> None:
    if len(pages) != PDF_PAGE_COUNT or [page.get("pdf_page") for page in pages] != list(range(1, 12)):
        raise ValueError("PDF 11ページの網羅が必要です")
    for page in pages:
        if page.get("source_sha256") != digest:
            raise ValueError("照合時の TeX SHA-256 が一致しません")
        status = page.get("status")
        if status not in ("UNVERIFIED", "CORRECTION_REQUIRED", "VERIFIED"):
            raise ValueError("不正なページ状態です")
        if status == "VERIFIED":
            review = page.get("review")
            if not isinstance(review, dict) or set(review) != set(REVIEW_FIELDS):
                raise ValueError("全文照合チェック欄が不足しています")
            if not all(review[key] is True for key in REVIEW_FIELDS):
                raise ValueError("全文照合が未完了です")
            if not str(page.get("reviewer", "")).strip() or not str(page.get("evidence_note", "")).strip():
                raise ValueError("照合者・原本と TeX を比較した証跡が必要です")


def build_summary(pages: list[dict[str, object]], digest: str) -> dict[str, object]:
    validate_ledger(pages, digest)
    counts = {s: sum(p["status"] == s for p in pages) for s in ("UNVERIFIED", "CORRECTION_REQUIRED", "VERIFIED")}
    return {
        "phase": "163 R4-R27",
        "source_sha256": digest,
        "pdf_pages": len(pages),
        "printed_pages": "5-15",
        "status_counts": counts,
        "prior_confirmed_corrections": sum(x[3] for x in CORRECTION_HISTORY),
        "new_confirmed_corrections": 0,
        "chapter_fully_verified": counts["VERIFIED"] == PDF_PAGE_COUNT,
        "statement_ids_changed": 0,
        "production_code_changed": False,
        "full_suite_run": False,
    }


def run(source: Path, output: Path) -> dict[str, object]:
    _content, digest = validate_source(source)
    pages = make_ledger(digest)
    summary = build_summary(pages, digest)
    output.mkdir(parents=True, exist_ok=True)
    (output / "page_ledger.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("pdf_page", "printed_page", "status", "scope_hint", "prior_corrections", "evidence_note"))
        for page in pages:
            writer.writerow(tuple(page[key] for key in ("pdf_page", "printed_page", "status", "scope_hint", "prior_corrections", "evidence_note")))
    with (output / "correction_history.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("phase", "pdf_page", "printed_page", "item", "count"))
        for phase, pdf_page, item, count in CORRECTION_HISTORY:
            writer.writerow((phase, pdf_page, pdf_page + 4, item, count))
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = [
        "# Phase 163 R4-R27 — Toda 第1章 原本照合ページ台帳", "",
        "基準資料：利用者提供の Toda 第1章 PDF（全11ページ、印刷5〜15ページ）。", "",
        "本 Phase はページ単位の照合記録を整備する。原本と TeX の全文逐字比較はまだ終わっていない。",
        "既存の9箇所の修正履歴は引き継ぐが、修正済み箇所があるだけでページ全体を照合済みとはしない。", "",
        "## 照合の完了条件", "",
        "- Definitions（定義）、Equations（式）、Named statements（名前付き主張）、Proofs/prose（証明・本文）、Notation/conditions（記号・条件）の5領域を原本画像と照合する。",
        "- 各領域について確認後、review を true にし、reviewer と evidence_note に具体的な証跡を記録する。",
        "- 相違が残る場合は CORRECTION_REQUIRED、未照合は UNVERIFIED。すべて満たした場合のみ VERIFIED。",
        "- 全11ページが VERIFIED になった場合に限り章全体の照合完了とする。", "",
        "## 現在の結果", "",
        "- VERIFIED: 0ページ", "- CORRECTION_REQUIRED: 0ページ（既知の修正9箇所は過去 Phase で適用済み）", "- UNVERIFIED: 11ページ", "- 新しい TeX 修正: 0件", "",
        "この台帳は実際の原本読解を代替しない。印刷原典との一致を自動的に認定しない。", "既存 Registry、Statement ID、Proof Search を変更せず、全体 pytest は実施しない。", "",
    ]
    (output / "report.md").write_text("\n".join(report), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
