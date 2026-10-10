"""Phase 163 R4-R23: original-page-10 verified correction and conservative ledger."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = "6a1284e00f95b2b255ce02dab6560b4e09f5b2455f17bd4dadab1b1c7ad9e322"
OLD = r'\{\alpha\circ\Ex^n\beta,\ \Ex^n\gamma,\ \Ex^n\delta)\}_n'
NEW = r'\{\alpha\circ\Ex^n\beta,\ \Ex^n\gamma,\ \Ex^n\delta\}_n'

REVIEW = (
    ("CONFIRMED_CORRECTION", 10, 6, "Proposition 1.2 iii)", "TeX の第三引数末尾に余分な閉じ括弧がある。原本では E^n delta に続いて bracket が閉じる。"),
    ("VISUAL_SPOT_CHECK", 8, 4, "(1.9)-(1.13)", "図式と対応関係を参照。全文・全文字の一致は未確認。"),
    ("VISUAL_SPOT_CHECK", 9, 5, "(1.14), Lemma 1.1", "H の場合分けと double coset の構造が存在することを確認。精密比較は未完了。"),
    ("VISUAL_SPOT_CHECK", 10, 6, "(1.15), Proposition 1.2", "命題 i)-iv) と 0) の構造、(1.15) の存在を確認。括弧以外の一致は未確定。"),
    ("PENDING_EXACT", 10, 6, "Proposition 1.3", "添字・符号・型および量化範囲の逐字照合が必要。"),
    ("PENDING_EXACT", 11, 7, "Proposition 1.3 proof, Proposition 1.4", "証明の等式と条件を原本と比較する必要がある。"),
    ("PENDING_EXACT", 12, 8, "Proposition 1.4 proof, Proposition 1.5", "添字、符号、式の条件の照合待ち。"),
    ("PENDING_EXACT", 13, 9, "Proposition 1.6, cone, extension/coextension", "定義の向きと式 (1.16) の照合待ち。"),
    ("PENDING_EXACT", 14, 10, "Proposition 1.7, 1.8, (1.17), (1.18)", "原典との量化条件、coset と式の向きを照合待ち。"),
    ("PENDING_EXACT", 15, 11, "Proposition 1.9 proof", "最後の証明と H_s の場合分けの照合待ち。"),
)


def align(text: str) -> str:
    if text.count(OLD) != 1:
        raise ValueError("原本照合済みの対象が一意に見つからないため変更しません")
    return text.replace(OLD, NEW, 1)


def run(source: Path, output: Path) -> dict:
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != SOURCE_SHA256:
        raise ValueError("R4-R22 修正版 TeX と一致しません。変更を中止します")
    revised = align(text)
    output.mkdir(parents=True, exist_ok=True)
    (output / "Toda_01_before_r23.tex").write_text(text, encoding="utf-8")
    (output / "Toda_01_corrected.tex").write_text(revised, encoding="utf-8")
    with (output / "alignment_review.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(("status", "printed_page", "pdf_page", "item", "finding"))
        writer.writerows(REVIEW)
    summary = {
        "phase": "163 R4-R23",
        "input_sha256": digest,
        "confirmed_corrections": 1,
        "carried_forward_r21_r22_corrections": 3,
        "review_ledger_entries": len(REVIEW),
        "full_chapter_verified": False,
        "formal_statement_ids_changed": 0,
        "production_code_changed": False,
        "full_suite_run": False,
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 163 R4-R23 原本照合記録\n\n"
        "## 原本と修正\n\n"
        "Toda Chapter I 印刷10頁（添付 PDF の6頁）にある Proposition 1.2 iii) を画像で確認。"
        "原本にはない余分な閉じ括弧を TeX の第三引数から削除した。"
        "R4-R21 と R4-R22 による修正3件は維持した。\n\n"
        "## 監査対象と制限\n\n"
        "印刷8〜15頁の式・命題について照合台帳を生成した。"
        "台帳の VISUAL_SPOT_CHECK は完全一致を意味しない。"
        "PENDING_EXACT は逐字照合未完了であり、修正すべきと断定していない。"
        "第1章全体の原本照合・登録済み Statement の照合完了は宣言しない。\n\n"
        "## 既存プログラム\n\n"
        "ProofRepository、文献境界、証明探索は変更していない。全体 pytest 未実施。\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
