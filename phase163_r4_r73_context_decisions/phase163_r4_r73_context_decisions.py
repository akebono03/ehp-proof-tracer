from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

DECISIONS = {2: ('DEFINITION_COMPONENT', 'Chapter 1 sphere parametrization'), 3: ('DEFINITION_COMPONENT', 'Chapter 1 sphere parametrization'), 6: ('DEPENDENCY_CONTEXT_CANDIDATE', ''), 9: ('DEFINITION_COMPONENT', 'smash product definition'), 10: ('DEFINITION_COMPONENT', 'smash product definition'), 12: ('DEPENDENCY_CONTEXT_CANDIDATE', ''), 13: ('DEFINITION_COMPONENT', 'sphere smash identification'), 14: ('UNNUMBERED_ASSERTION_CANDIDATE', 'smash identification associativity'), 15: ('DEPENDENCY_CONTEXT_CANDIDATE', ''), 16: ('DEFINITION_COMPONENT', 'smash product on maps'), 17: ('DEFINITION_COMPONENT', 'smash product on maps'), 19: ('DEFINITION_COMPONENT', 'iterated suspension of a map'), 20: ('DEPENDENCY_CONTEXT_CANDIDATE', ''), 26: ('UNNUMBERED_ASSERTION_CANDIDATE', 'homomorphism property of composition'), 27: ('UNNUMBERED_ASSERTION_CANDIDATE', 'homomorphism property of composition'), 28: ('DEFINITION_COMPONENT', 'loop space induced map'), 29: ('DEFINITION_COMPONENT', 'loop space induced map'), 31: ('DEFINITION_COMPONENT', 'canonical inclusion'), 32: ('DEFINITION_COMPONENT', 'canonical inclusion'), 33: ('DEFINITION_COMPONENT', 'loop-suspension adjunction'), 34: ('DEFINITION_COMPONENT', 'loop-suspension adjunction'), 35: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 36: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 37: ('PROOF_INTERNAL_CANDIDATE', ''), 42: ('PROOF_INTERNAL_CANDIDATE', ''), 43: ('PROOF_INTERNAL_CANDIDATE', ''), 44: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 46: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 47: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 49: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 50: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 51: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 53: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 55: ('PROOF_INTERNAL_CANDIDATE', ''), 56: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 57: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 61: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 62: ('PROOF_INTERNAL_CANDIDATE', ''), 64: ('PROOF_INTERNAL_CANDIDATE', ''), 71: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 74: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 75: ('PROOF_INTERNAL_CANDIDATE', ''), 76: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 77: ('PROOF_INTERNAL_CANDIDATE', ''), 78: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 79: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 80: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 93: ('DEPENDENCY_CONTEXT_CANDIDATE', ''), 95: ('DEFINITION_COMPONENT', 'reduced join definition'), 97: ('DEPENDENCY_CONTEXT_CANDIDATE', ''), 98: ('DEPENDENCY_CONTEXT_CANDIDATE', ''), 100: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 101: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 103: ('DEFINITION_COMPONENT', 'canonical embedding'), 106: ('DEFINITION_COMPONENT', 'James-Hopf map'), 124: ('UNNUMBERED_ASSERTION_CANDIDATE', 'cohomology decomposition'), 127: ('UNNUMBERED_ASSERTION_CANDIDATE', 'Serre spectral sequence E2'), 136: ('UNNUMBERED_ASSERTION_CANDIDATE', 'Whitehead theorem application'), 137: ('UNNUMBERED_ASSERTION_CANDIDATE', 'five lemma application'), 141: ('PROOF_INTERNAL_CANDIDATE', ''), 148: ('PROOF_INTERNAL_CANDIDATE', ''), 155: ('UNNUMBERED_ASSERTION_CANDIDATE', 'permutation sign of suspension'), 160: ('PROOF_INTERNAL_CANDIDATE', ''), 162: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 165: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 171: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 174: ('PROOF_INTERNAL_CANDIDATE', ''), 175: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 176: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 178: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 180: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 182: ('PROOF_INTERNAL_CANDIDATE', ''), 185: ('DEFINITION_COMPONENT', 'mapping cone K'), 186: ('DEFINITION_COMPONENT', 'mapping cone K'), 187: ('DEFINITION_COMPONENT', 'mapping cone K'), 188: ('DEFINITION_COMPONENT', 'mapping cone quotient'), 189: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 190: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 191: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 192: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 193: ('PROOF_INTERNAL_CANDIDATE', ''), 194: ('UNNUMBERED_ASSERTION_CANDIDATE', 'suspension sign relation'), 195: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 196: ('PROOF_INTERNAL_CANDIDATE', ''), 198: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 200: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 201: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 202: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 205: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 207: ('DEFINITION_COMPONENT', 'proof-local self-homeomorphism'), 208: ('PROOF_INTERNAL_CANDIDATE', ''), 212: ('PROOF_INTERNAL_CANDIDATE', ''), 213: ('PROOF_INTERNAL_CANDIDATE', ''), 214: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 216: ('DEFINITION_COMPONENT', 'proof-local self-homeomorphism'), 217: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', ''), 232: ('PROOF_INTERNAL_CANDIDATE', ''), 235: ('PROOF_INTERNAL_CANDIDATE', ''), 250: ('UNNUMBERED_ASSERTION_CANDIDATE', 'Chapter 4 homotopy group calculation'), 251: ('UNNUMBERED_ASSERTION_CANDIDATE', 'Chapter 4 homotopy group calculation'), 252: ('UNNUMBERED_ASSERTION_CANDIDATE', 'Chapter 4 homotopy group calculation'), 254: ('UNNUMBERED_ASSERTION_CANDIDATE', 'Chapter 4 homotopy group calculation'), 258: ('DEPENDENCY_CONTEXT_CANDIDATE', ''), 259: ('UNNUMBERED_ASSERTION_CANDIDATE', 'multiplication order relation'), 262: ('UNNUMBERED_ASSERTION_CANDIDATE', 'Delta iota5 special case'), 269: ('UNNUMBERED_ASSERTION_CANDIDATE', 'eta square suspension'), 270: ('PROOF_INTERNAL_CANDIDATE', ''), 271: ('PROOF_INTERNAL_CANDIDATE', ''), 272: ('PROOF_INTERNAL_CANDIDATE', ''), 273: ('PROOF_INTERNAL_CANDIDATE', ''), 279: ('PROOF_INTERNAL_CANDIDATE', ''), 281: ('PROOF_INTERNAL_CANDIDATE', ''), 283: ('PROOF_INTERNAL_CANDIDATE', ''), 284: ('PROOF_INTERNAL_CANDIDATE', ''), 286: ('PROOF_INTERNAL_CANDIDATE', ''), 288: ('PROOF_INTERNAL_CANDIDATE', ''), 289: ('PROOF_INTERNAL_CANDIDATE', ''), 291: ('PROOF_INTERNAL_CANDIDATE', ''), 292: ('PROOF_INTERNAL_CANDIDATE', ''), 294: ('PROOF_INTERNAL_CANDIDATE', ''), 295: ('PROOF_INTERNAL_CANDIDATE', ''), 296: ('PROOF_INTERNAL_CANDIDATE', ''), 297: ('PROOF_INTERNAL_CANDIDATE', ''), 299: ('PROOF_INTERNAL_CANDIDATE', ''), 301: ('PROOF_INTERNAL_CANDIDATE', ''), 302: ('PROOF_INTERNAL_CANDIDATE', ''), 303: ('PROOF_INTERNAL_CANDIDATE', ''), 304: ('PROOF_INTERNAL_CANDIDATE', ''), 305: ('PROOF_INTERNAL_CANDIDATE', ''), 306: ('PROOF_INTERNAL_CANDIDATE', ''), 307: ('PROOF_INTERNAL_CANDIDATE', ''), 308: ('PROOF_INTERNAL_CANDIDATE', ''), 309: ('PROOF_INTERNAL_CANDIDATE', ''), 310: ('PROOF_INTERNAL_CANDIDATE', ''), 311: ('PROOF_INTERNAL_CANDIDATE', ''), 312: ('PROOF_INTERNAL_CANDIDATE', ''), 313: ('PROOF_INTERNAL_CANDIDATE', ''), 314: ('PROOF_INTERNAL_CANDIDATE', '')}
ROLE_RATIONALES = {'DEFINITION_COMPONENT': '周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。', 'UNNUMBERED_ASSERTION_CANDIDATE': '表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。', 'PROOF_INTERNAL_CANDIDATE': '証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。', 'PROOF_LOCAL_CONSTRUCTION_CANDIDATE': '証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。', 'DEPENDENCY_CONTEXT_CANDIDATE': '周辺の定義・前提・同一視の文脈。隣接した Reference と一体で再確認。'}


def build_review(source: dict) -> dict:
    if source.get("phase") != "163 R4-R72" or source.get("pending_candidate_count") != 237:
        raise ValueError("R72 input contract mismatch")
    if source.get("editorial_proposal_count") != 34 or source.get("remaining_unreviewed_count") != 203:
        raise ValueError("R72 status mismatch")
    if source.get("production_registry_modified") is not False or source.get("production_ids_allocated") is not False:
        raise ValueError("R72 must not have production modifications")
    records = source.get("records", [])
    if len(records) != 237 or len(set(r["r48_index"] for r in records)) != 237:
        raise ValueError("R72 records are not unique and complete")
    available = {r["r48_index"] for r in records if r["proposed_role"] == "UNREVIEWED"}
    if not set(DECISIONS).issubset(available):
        raise ValueError("Explicit R73 decisions cannot overwrite existing R72 judgments")
    out = []
    for record in records:
        row = dict(record)
        index = row["r48_index"]
        if index in DECISIONS:
            role, owner = DECISIONS[index]
            if not row.get("excerpt_sha256") or hashlib.sha256(row["excerpt"].encode("utf-8")).hexdigest() != row["excerpt_sha256"]:
                raise ValueError(f"Excerpt hash mismatch for R48 #{index}")
            row["proposed_role"] = role
            row["proposal_rationale"] = ROLE_RATIONALES[role]
            row["proposed_owner_context"] = owner
            row["r73_individually_reviewed"] = True
        else:
            row["proposed_owner_context"] = None
            row["r73_individually_reviewed"] = False
        if row["mathematical_role_verified"] or row["semantic_registration_allowed"]:
            raise ValueError("Unverified data must remain unapproved")
        out.append(row)
    counts = dict(sorted(Counter(r["proposed_role"] for r in out).items()))
    return {
        "phase": "163 R4-R73", "mode": "READ_ONLY_EXPLICIT_CONTEXT_ROLE_DECISIONS",
        "source_phase": "163 R4-R72", "pending_candidate_count": 237,
        "previous_editorial_proposal_count": 34,
        "new_editorial_proposal_count": len(DECISIONS),
        "editorial_proposal_count": 237 - counts.get("UNREVIEWED", 0),
        "remaining_unreviewed_count": counts.get("UNREVIEWED", 0),
        "role_counts": counts, "mathematical_role_verified_count": 0,
        "semantic_registration_allowed_count": 0, "original_edition_verified": False,
        "production_registry_modified": False, "production_ids_allocated": False,
        "proof_search_connected": False, "full_suite_run": False,
        "records": out,
    }


def write_reports(result: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "role_decisions.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "role_decisions.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["r48_index", "chapter", "source_file", "source_line", "proposed_role", "r73_individually_reviewed", "proposed_owner_context", "proposal_rationale", "excerpt_sha256", "excerpt", "context"])
        writer.writeheader()
        for record in result["records"]:
            writer.writerow({key: record.get(key) for key in writer.fieldnames})
    lines = ["# Phase 163 R4-R73：文脈に基づく追加個別判定案", "", "出典 TeX と既存 R72 提案に基づく編集上の提案。原本照合・数学的検証・Registry 登録は未実施。", "",
             f"- 追加で個別判定した候補: {result['new_editorial_proposal_count']}",
             f"- 判定案の累計: {result['editorial_proposal_count']}",
             f"- 未判定: {result['remaining_unreviewed_count']}", "", "|Role|Count|", "|---|---:|"]
    lines.extend(f"|{key}|{count}|" for key, count in result["role_counts"].items())
    lines.extend(["", "## 追加判断（出典と根拠）", ""])
    for rec in result["records"]:
        if not rec["r73_individually_reviewed"]:
            continue
        lines.extend([f"### R48 #{rec['r48_index']}（第{rec['chapter']}章 {rec['source_line']}行）", "",
                      f"- 判定案：`{rec['proposed_role']}`", f"- 帰属：{rec['proposed_owner_context'] or '原文文脈に基づく暫定判断'}", f"- 理由：{rec['proposal_rationale']}", "",
                      "```tex", rec["excerpt"], "```", "", "```text", rec["context"], "```", ""])
    lines.extend(["", "追加判断はいずれも未承認。既存番号付き命題への所属確認と原本照合後に登録判断する。", "全体 pytest は Phase 最終段階のみ。", ""])
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("phase163_r4_r72_output/role_proposals.json"))
    parser.add_argument("--output", type=Path, default=Path("phase163_r4_r73_output"))
    args = parser.parse_args()
    result = build_review(json.loads(args.input.read_text(encoding="utf-8")))
    write_reports(result, args.output)
    print(json.dumps({key: value for key, value in result.items() if key != "records"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
