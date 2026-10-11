"""Phase 163 R4-R35: printed page 6 mathematical-content verification."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "ece0b13b9ce5c59508c24e1fe756dd6ab99c83e22e74ab495386768d7963b572"
EVIDENCE = (
    ("composition", "原本印刷6ページ冒頭: 合成の独立性・結合律・誘導写像とその合成則", "VERIFIED"),
    ("reduced_join_definition", "原本印刷6ページ中段: A#B=(A×B)/(A∨B), 基点、縮約写像と三重積", "VERIFIED"),
    ("equation_1_3", "原本(1.3): S^m×S^n→S^(m+n)、ψ による対応、球面積の結合性", "VERIFIED"),
    ("join_maps", "原本印刷6ページ下段: f,g の基点保存・積写像の誘導", "VERIFIED"),
    ("equation_1_4", "原本(1.4) 0), i), ii): 基点付きホモトピー、結合性、合成との両立", "VERIFIED"),
    ("homotopy_join", "原本末尾: α#β の代表写像非依存性・定義。続きの文は印刷7ページへ", "VERIFIED_WITH_CONTINUATION"),
)
REQUIRED = (
    r"\shrink_{m,n}:S^m\times S^n\longrightarrow S^{m+n}",
    r"\shrink_{m+n,p}\bigl(\shrink_{m,n}(a,b),c\bigr)",
    r"f(a_0)=a'_0",
    r"g(b_0)=b'_0",
    r"(f\wedge g)\wedge h = f\wedge (g\wedge h)",
    r"(f_2\circ f_1)\ \wedge\ (g_2\circ g_1)",
    r"f\simeq f':(A,a_0)\to(A',a'_0)",
    r"\alpha\wedge \beta\in[A\wedge B, A'\wedge B']",
)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_inputs(text: str, ledger: list[dict]) -> None:
    if sha256(text) != EXPECTED_SHA256:
        raise ValueError("R4-R34 source SHA-256 mismatch; output not written")
    if len(ledger) != 11 or [x.get("pdf_page") for x in ledger] != list(range(1, 12)):
        raise ValueError("Expected exactly eleven ordered PDF pages")
    if [x.get("status") for x in ledger] != ["VERIFIED"] + ["UNVERIFIED"] * 10:
        raise ValueError("Unexpected R4-R34 verification statuses")
    if any(x.get("source_sha256") != EXPECTED_SHA256 for x in ledger):
        raise ValueError("Ledger SHA-256 mismatch")
    missing = [fragment for fragment in REQUIRED if fragment not in text]
    if missing:
        raise ValueError("Missing expected corrected mathematical content: " + repr(missing))


def verify_page_six(text: str, ledger: list[dict]) -> list[dict]:
    validate_inputs(text, ledger)
    result = json.loads(json.dumps(ledger, ensure_ascii=False))
    page = result[1]
    page["status"] = "VERIFIED"
    page["verification_scope"] = "MATHEMATICAL_CONTENT_AND_CONDITIONS"
    page["verbatim_transcription_verified"] = False
    page["review"] = {"definitions": True, "equations": True, "named_statements": True,
                      "proofs_and_prose": True, "notation_and_conditions": True}
    page["reviewer"] = "R4-R35 original PDF page 2 visual mathematical comparison"
    page["notation_normalizations"] = [
        "原本の reduced join 記号 # を TeX では \\wedge と表示",
        "原本のホモトピー類 π(X→Y) を TeX では [X,Y] と表示",
        "原本の英語本文を日本語訳で記録",
    ]
    page["continuation_note"] = "原本の印刷6ページ末尾の It は印刷7ページへ続く。後続命題・式(1.5)の照合は印刷7ページで行う。"
    page["evidence_note"] = (page.get("evidence_note", "") + " R4-R35: 原本印刷6ページの数学的内容を全域照合。合成、reduced join、(1.3)、(1.4)、α#β の導入を確認。逐字照合ではない。末尾から印刷7ページへの継続は次ページに留保。").strip()
    return result


def run(source: Path, ledger_path: Path, output: Path) -> dict:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    updated = verify_page_six(text, ledger)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_corrected.tex").write_text(text, encoding="utf-8")
    (output / "page_ledger.json").write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "page_ledger.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["pdf_page", "printed_page", "status", "verification_scope", "evidence_note"])
        for row in updated:
            writer.writerow([row.get(k, "") for k in ("pdf_page", "printed_page", "status", "verification_scope", "evidence_note")])
    with (output / "page6_evidence.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["topic", "evidence", "status"])
        writer.writerows(EVIDENCE)
    summary = {
        "phase": "163 R4-R35", "input_sha256": sha256(text), "output_sha256": sha256(text),
        "reviewed_printed_page": 6, "page6_mathematical_content_verified": True,
        "page6_verbatim_transcription_verified": False, "new_confirmed_corrections": 0,
        "prior_confirmed_corrections": 18, "total_recorded_corrections": 18,
        "status_counts": {status: sum(x["status"] == status for x in updated)
                          for status in ("VERIFIED", "UNVERIFIED", "CORRECTION_REQUIRED")},
        "chapter_fully_verified": False, "statement_ids_changed": 0,
        "production_code_changed": False, "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R35 — 印刷6ページ原本照合\n\n"
        "- Toda 原本の印刷6ページ（PDF 2ページ目）を、数学的内容・適用条件について照合。\n"
        "- 合成、reduced join、(1.3)、(1.4)、α#β の導入を確認。\n"
        "- 印刷6ページ末尾の文は次ページへ続き、続きは未照合。\n"
        "- 原本の記号 # は TeX では $\\wedge$ としている。英語と日本語訳の逐字一致は認定しない。\n"
        "- 今回の新規修正は0箇所。過去の訂正18箇所は維持。\n"
        "- 印刷5・6ページを VERIFIED とし、残る9ページは UNVERIFIED。\n"
        "- Statement ID・本体 Registry・証明探索には変更なし。全体 pytest は未実施。\n",
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
