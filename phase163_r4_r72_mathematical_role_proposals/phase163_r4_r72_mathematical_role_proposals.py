"""Phase 163 R4-R72: source-grounded proposed mathematical roles, read-only."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

# These are editorial proposals about the TeX passages, NOT mathematically
# certified statements or permissions to use them as proof premises.
CHOICES = {73: ('EXISTING_REFERENCE_COMPONENT', 'coextension の代表写像に課した条件式。既存 Reference の本文に含める。'), 275: ('EXISTING_REFERENCE_COMPONENT', 'ν₄ の場合分けによる定義式。既存 Reference の本文に含める。'), 5: ('ADJACENT_DEFINITION_EXTENSION', 'f* と g* の定義。合成の定義の直後に連続し、出典境界の拡張を確認する。'), 21: ('SEPARATE_DEFINITION_CANDIDATE', '懸垂写像 Ef の作用式。次の加法・逆元の定義と混同しない。'), 40: ('SEPARATE_DEFINITION_CANDIDATE', '集合の合成 A∘B の記法の導入。secondary composition の定義とは別の概念。'), 63: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', '証明途中で使う自己同相 σ の具体式。恒久的定義としての独立登録は保留。'), 70: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', 'H と H′ から証明中に構成する H′′。一般 Definition にしない。'), 102: ('SEPARATE_DEFINITION_CANDIDATE', '(f)_t の点ごとの定義式。直前の写像の域・値域と合わせて扱う。'), 109: ('SEPARATE_DEFINITION_CANDIDATE', 'combinatorial extension h の定義式。写像と係数の条件を一体で扱う。'), 125: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', 'mapping track X の具体的構成。後続の Serre fibration の議論に依存する。'), 126: ('PROOF_LOCAL_CONSTRUCTION_CANDIDATE', 'mapping track の射影 p の具体的構成。後続の fibration 性質とは別。'), 7: ('UNNUMBERED_ASSERTION_CANDIDATE', '合成の結合律を述べる番号なしの一般的関係式。'), 8: ('UNNUMBERED_ASSERTION_CANDIDATE', '誘導写像の合成に関する関手性の関係式。'), 11: ('UNNUMBERED_ASSERTION_CANDIDATE', 'smash product の結合性を表す自然同相。'), 25: ('UNNUMBERED_ASSERTION_CANDIDATE', 'X が局所コンパクトなときの自然同型。適用条件の保持が必要。'), 30: ('UNNUMBERED_ASSERTION_CANDIDATE', 'ループ空間の操作が合成を保つという一般的関係。'), 41: ('SEPARATE_DEFINITION_CANDIDATE', '部分集合の和 A₁+A₂ の記法。A∘B と同一 Reference とするか出典文脈要確認。'), 52: ('PROOF_INTERNAL_CANDIDATE', '異なる null-homotopy による H と H′ の比較に現れる証明内関係式。'), 65: ('PROOF_INTERNAL_CANDIDATE', 'Prop1.4 の証明を閉じる包含式。既存命題の証明に属する。'), 94: ('UNNUMBERED_ASSERTION_CANDIDATE', '任意の整数 k に対する合成と倍数の関係式。'), 96: ('UNNUMBERED_ASSERTION_CANDIDATE', 'Eⁿα と reduced join の一般的な関係式。'), 110: ('DEPENDENCY_CONTEXT_CANDIDATE', 'Hopf 準同型の域と値域の表示。直前の定義と合わせる。'), 117: ('PROOF_INTERNAL_CANDIDATE', 'Prop1.7 の適用から得る証明内包含式。'), 118: ('PROOF_INTERNAL_CANDIDATE', '外部定理 [6] を引用する証明中での h* の表示。'), 119: ('UNNUMBERED_ASSERTION_CANDIDATE', 'm が奇数の場合のコホモロジー積の関係式。偶数の場合も別 Assertion として確認。'), 129: ('PROOF_INTERNAL_CANDIDATE', 'スペクトル列を用いる推論中の i₁* 同型性。'), 139: ('DEPENDENCY_CONTEXT_CANDIDATE', '直前の Theorem の帰結。既存 Reference への接続を優先確認する。'), 149: ('UNNUMBERED_ASSERTION_CANDIDATE', '偶数 n における Whitehead square の Hopf 不変量の既知事実。'), 255: ('PROOF_INTERNAL_CANDIDATE', 'EHP 完全列の証明で提示した列の一部。'), 257: ('EXTERNALLY_SOURCED_ASSERTION_CANDIDATE', 'n=2,4,8 と任意の i の Hopf fibration 由来の同型。Steenrod を出典とする。'), 274: ('PROOF_INTERNAL_CANDIDATE', '(5.4) の証明中に Prop1.3 と (1.15) を用いる包含計算。'), 280: ('PROOF_INTERNAL_CANDIDATE', '特定のホモトピー群に対する Prop の証明に現れる EHP 列。'), 287: ('PROOF_INTERNAL_CANDIDATE', 'Prop の証明中に Prop2.2 と (5.3) を適用する計算。'), 290: ('PROOF_INTERNAL_CANDIDATE', 'Prop の証明末尾の完全列と消滅の帰結。')}


def load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def propose_roles(source: dict) -> dict:
    if source.get("phase") != "163 R4-R71" or source.get("pending_candidate_count") != 237:
        raise ValueError("expected complete R71 input")
    records = source.get("records", [])
    if len(records) != 237:
        raise ValueError("R71 records are incomplete")
    by_id = {r["r48_index"]: r for r in records}
    if len(by_id) != 237 or set(CHOICES) - set(by_id):
        raise ValueError("R71 candidate IDs inconsistent")
    if Counter(r["review_tier"] for r in records) != {
        "T0_EXISTING_REFERENCE_SPAN": 2,
        "T1_ADJACENT_REFERENCE": 3,
        "T2_DEFINITION_NOTATION": 6,
        "T3_PROSE_CUE": 70,
        "T4_NO_PROSE_CUE": 156,
    }:
        raise ValueError("R71 review tiers changed")
    if any(r.get("mathematical_role_verified") or r.get("registration_action") != "NONE" for r in records):
        raise ValueError("upstream R71 is not read-only")
    for index, tier in [(73, "T0_EXISTING_REFERENCE_SPAN"), (275, "T0_EXISTING_REFERENCE_SPAN"),
                        (5, "T1_ADJACENT_REFERENCE"), (21, "T1_ADJACENT_REFERENCE"),
                        (40, "T1_ADJACENT_REFERENCE")]:
        if by_id[index]["review_tier"] != tier:
            raise ValueError("expected source context has changed")
    for index, (role, rationale) in CHOICES.items():
        row = by_id[index]
        if not row.get("excerpt") or not row.get("context"):
            raise ValueError("source excerpt/context missing")
        digest = hashlib.sha256(row["excerpt"].encode("utf-8")).hexdigest()
        if digest != row.get("excerpt_sha256"):
            raise ValueError(f"excerpt digest mismatch: {index}")
    out = []
    for row in records:
        index = row["r48_index"]
        selected = CHOICES.get(index)
        proposed_role, rationale = selected if selected else ("UNREVIEWED", "この段階では個別の数学的判定を行わない。")
        out.append({
            "r48_index": index,
            "chapter": row["chapter"],
            "source_file": row["source_file"],
            "source_line": row["source_line"],
            "review_tier": row["review_tier"],
            "proposed_role": proposed_role,
            "proposal_rationale": rationale,
            "excerpt_sha256": row["excerpt_sha256"],
            "excerpt": row["excerpt"],
            "context": row["context"],
            "existing_reference_overlap": row["overlapping_r69_keys"],
            "nearby_references": row["nearby_r69_keys_within_five_lines"],
            "mathematical_role_verified": False,
            "original_edition_verified": False,
            "semantic_registration_allowed": False,
            "production_reference_id": None,
            "production_assertion_ids": [],
        })
    counts = dict(sorted(Counter(r["proposed_role"] for r in out).items()))
    return {
        "phase": "163 R4-R72",
        "mode": "READ_ONLY_SOURCE_GROUNDED_ROLE_PROPOSALS",
        "source_phase": "163 R4-R71",
        "pending_candidate_count": 237,
        "editorial_proposal_count": len(CHOICES),
        "remaining_unreviewed_count": 237-len(CHOICES),
        "proposed_role_counts": counts,
        "mathematical_role_verified_count": 0,
        "semantic_registration_allowed_count": 0,
        "original_edition_verified": False,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": out,
    }


def write_reports(report: dict, output: str | Path) -> None:
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "role_proposals.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["r48_index", "chapter", "source_line", "review_tier", "proposed_role", "proposal_rationale", "excerpt_sha256"]
    with (output / "role_proposals.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(report["records"])
    lines = ["# Phase 163 R4-R72：数学的役割の個別判定案", "",
             "TeX 前後の文脈から作成した編集上の判定案。正式な数学的認定・Registry 登録ではない。", "",
             f"- 総候補：{report['pending_candidate_count']}件",
             f"- 個別判定案：{report['editorial_proposal_count']}件",
             f"- 未判定：{report['remaining_unreviewed_count']}件", "",
             "|候補種別|件数|", "|---|---:|"]
    for role, count in report["proposed_role_counts"].items():
        lines.append(f"|{role}|{count}|")
    lines.extend(["", "## 個別判定案（原文付き）", ""])
    for r in report["records"]:
        if r["proposed_role"] == "UNREVIEWED":
            continue
        lines.extend([f"### R48 #{r['r48_index']}（第{r['chapter']}章 {r['source_line']}行）",
                      "", f"候補：`{r['proposed_role']}`。{r['proposal_rationale']}",
                      "", "```tex", r["excerpt"], "```", "", "文脈：", "", "```text", r["context"], "```", ""])
    lines.extend(["## 登録境界", "", "Math role 認定、Original edition 照合、ID 採番、Registry 変更、proof search 接続はいずれも行っていない。", "全体 pytest は Phase 163 の最後に実施する。"])
    (output / "report.md").write_text("\n".join(lines)+"\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r71", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = propose_roles(load_json(args.r71))
    write_reports(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, ensure_ascii=False, indent=2))
    print("R72 source-grounded editorial proposals complete. Full pytest not run.")


if __name__ == "__main__":
    main()
