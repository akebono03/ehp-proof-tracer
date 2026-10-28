"""R10EO-R1 read-only audit: metadata, literal definitions, provenance, goals.

A textual match is a review candidate, NEVER a licensed GIVEN or inference.
No application source or pre-existing tests are modified by this module.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "HyoujiGen.csv"
TEX_PATHS = {
    "chapter_v": ROOT / "sources" / "toda" / "Toda_05_2.tex",
    "chapter_vi": ROOT / "sources" / "toda" / "Toda_06_2.tex",
}


def read_metadata(path: Path) -> list[dict[str, Any]]:
    """Read the entire database, including non-series rows, without trust uplift."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"id", "display", "kinds", "k", "n", "orders", "latex", "stable", "stable_orders"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("HyoujiGen.csv required columns missing")
        entries = []
        seen = set()
        for row in reader:
            identity = int(row["id"])
            if identity in seen:
                raise ValueError("duplicate generator ID")
            seen.add(identity)
            entry = dict(row)
            for key in ("id", "kinds", "k", "n"):
                entry[key] = int(row[key])
            entries.append(entry)
        return entries


def normalize_tex(source: str) -> str:
    """Conservative surface normalization for finding review candidates only."""
    text = re.sub(r"\s+", "", source)
    for token in (r"\,", r"\;", r"\!", r"\quad", r"\qquad"):
        text = text.replace(token, "")
    text = re.sub(r"_\{(n|\d+)\}", r"_\1", text)
    text = text.replace(r"\overline{\nu}", r"\bar{\nu}")
    text = text.replace(r"\overline\nu", r"\bar{\nu}")
    return text


def literal_definition_candidates(
    row: dict[str, Any], text: str, *, source_id: str,
) -> list[dict[str, Any]]:
    """Locate α_n := E^(n-n0) α_n0 text; do not create a citation or proof."""
    if row["kinds"] != 0 or row["id"] == 0:
        return []
    symbol = normalize_tex(str(row["latex"]).strip())
    n0 = row["n"]
    if not symbol or n0 < 1:
        return []
    target = normalize_tex(f"{symbol}_n:=E^{{n-{n0}}}{symbol}_{n0}")
    found = []
    for match in re.finditer(r":=", text):
        start = max(0, match.start() - 130)
        end = min(len(text), match.end() + 190)
        snippet = text[start:end]
        if target not in normalize_tex(snippet):
            continue
        preceding = text.rfind(r"\paragraph{", 0, match.start())
        paragraph = ""
        if preceding >= 0:
            paragraph = text[preceding:preceding + 115].split("\n", 1)[0]
        found.append({
            "source_id": source_id,
            "line": text.count("\n", 0, match.start()) + 1,
            "paragraph": paragraph,
            "normalized_match": target,
            "classification": "TEXT_MATCH_CANDIDATE_NOT_AUTHORIZED",
        })
    return found


def classify_source(row: dict[str, Any], source_ids: set[int], matches: list[dict]) -> str:
    """Never promote a database row or literal match into mathematical evidence."""
    if row["id"] == 2:
        return "LEGACY_ETA_CITATION_PATH"
    if row["id"] in source_ids:
        return "REGISTERED_CITED_DEFINITION"
    if matches:
        return "TEXT_MATCH_REQUIRES_INDEPENDENT_REVIEW"
    return "NO_REGISTERED_CITED_DEFINITION"


def inspect_metadata_and_sources(root: Path = ROOT) -> dict[str, Any]:
    from phase169_r10b_registered_stable_family_binding.family_registry import (
        read_registered_stable_families,
    )
    from phase169_r10d2_general_family_definition.family_citation import (
        SOURCE_RECORDS, verified_source_positions,
    )
    from phase169_r10e8_hyoujigen_generic_suspension.source_records import (
        CHAPTER_VI_SOURCE_RECORDS,
    )
    from phase169_r10e8_hyoujigen_generic_suspension.chapter_vi_reference import (
        verified_chapter_vi_source_positions,
    )
    rows = read_metadata(root / "data" / "HyoujiGen.csv")
    source_texts = {
        name: (root / "sources" / "toda" / filename).read_text(encoding="utf-8-sig")
        for name, filename in (("chapter_v", "Toda_05_2.tex"),
                               ("chapter_vi", "Toda_06_2.tex"))
    }
    registered = read_registered_stable_families(root / "data" / "HyoujiGen.csv")
    ids = {int(r.family_id) for r in SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS}
    if len(ids) != len(SOURCE_RECORDS) + len(CHAPTER_VI_SOURCE_RECORDS):
        raise ValueError("duplicate registered cited definitions")
    positions = {
        "chapter_v": list(verified_source_positions()),
        "chapter_vi": list(verified_chapter_vi_source_positions()),
    }
    reports = []
    for row in rows:
        if row["kinds"] != 0 or row["id"] == 0:
            continue
        candidates = []
        for name, content in source_texts.items():
            candidates += literal_definition_candidates(row, content, source_id=name)
        reports.append({
            "id": row["id"], "display": row["display"],
            "stem": row["k"], "minimum_n": row["n"],
            "latex": row["latex"],
            "stable": row["stable"], "stable_orders": row["stable_orders"],
            "freudenthal_threshold_n": max(2, row["k"] + 2),
            "initial_n_in_stable_range": row["n"] >= max(2, row["k"] + 2),
            "citation_status": classify_source(row, ids, candidates),
            "literal_candidates": candidates,
        })
    # This report is diagnostic. Existing source checks retain authority.
    return {
        "mode": "AUDIT_ONLY", "all_rows": len(rows),
        "series_count": len(reports),
        "registered_identifier_count": len(registered),
        "registered_definition_ids": sorted(ids),
        "source_publication_positions": positions,
        "series_with_nonempty_stable": sum(bool(r["stable"]) for r in reports),
        "series_with_nonempty_stable_orders": sum(bool(r["stable_orders"]) for r in reports),
        "candidate_count": sum(len(r["literal_candidates"]) for r in reports),
        "families": reports,
        "metadata_proves_suspension": False,
        "literal_match_proves_suspension": False,
        "production_files_changed": False,
    }


def inspect_live_goal(n: int = 30, k: int = 11) -> dict[str, Any]:
    """Run the existing search, exposing all open goals without adding facts."""
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates, search_group_from_registered_goal,
    )
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    contexts: list[object] = []
    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    report: dict[str, Any] = {
        "target": f"pi_{n+k}^{n}",
        "status": result.status.value,
        "typed_goal_candidates": len(candidates),
        "goal_candidate_reprs": [repr(item)[:2000] for item in candidates],
        "open_goal_count": len(result.open_goals),
        "open_goal_types": [type(item).__name__ for item in result.open_goals],
        "open_goals": [repr(item)[:2500] for item in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "given_steps": sum(s.rule is ProofRule.GIVEN for s in result.proven_steps),
        "inference_steps": sum(s.rule is ProofRule.INFERENCE for s in result.proven_steps),
        "trust": "NOT_APPLICABLE_INCOMPLETE",
    }
    if result.status is ProofSearchStatus.COMPLETE:
        if not contexts or result.conclusion is None:
            report["trust"] = "MISSING_CONTEXT"
        else:
            citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
            try:
                inf, giv = verify_proof_tree_for_narrative(
                    result, contexts[-1], citing_assertion_id=citing_id,
                    derived_target_without_citing_id=citing_id is None,
                )
            except (ValueError, TypeError) as exc:
                report["trust"] = f"FAIL: {type(exc).__name__}: {exc}"
            else:
                report["trust"] = "PASS"
                report["verified_inferences"] = inf
                report["verified_givens"] = giv
    return report


def render_markdown(report: dict[str, Any]) -> str:
    rows = report["metadata"]["families"]
    lines = [
        "# Phase 169 R10EO-R1 — Definition 一般化の監査結果", "",
        "本報告は AUDIT_ONLY。CSV の名前一致や TeX の字面一致を証明には昇格しない。", "",
        "| ID | 生成元 | k | n0 | 安定範囲始点 | 引用登録 | 転写定義候補 |",
        "|---:|---|---:|---:|---:|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['display']} | {row['stem']} | "
            f"{row['minimum_n']} | {row['freudenthal_threshold_n']} | "
            f"{row['citation_status']} | {len(row['literal_candidates'])} |"
        )
    lines.extend(["", "## 11-stem の未解決 Goal", ""])
    live = report.get("runtime")
    if live is None:
        lines.append("未実行。`run.ps1` で現行の型付き探索を実行する。")
    else:
        lines.append(f"- 探索: `{live['target']}` / `{live['status']}`")
        lines.append(f"- 信頼境界: `{live['trust']}`")
        for i, goal in enumerate(live["open_goals"], 1):
            lines.append(f"- Open Goal {i}: `{goal.replace('`', chr(39))}`")
        for diag in live["diagnostics"]:
            lines.append(f"- Diagnosis: `{str(diag).replace('`', chr(39))}`")
    lines.extend([
        "", "## 設計判断", "",
        "CSV は ID・型・添字の候補集合を生成する。Definition の採用は別の信頼済み出典と publication position の検証を要する。",
        "テキスト候補の自動検出と、FIXED_STATEMENT / GIVEN の承認は別工程とする。",
        "証明済み Definition から各添字の定義と GeneratorImage を既存の INFERENCE で導く。",
        "Toda (4.5) による同型と各 GeneratorImage を独立の前提として維持する。",
        "合成元・直和群・群構造 Relation は既存の共通処理を変更しない。",
        "", "## 範囲", "",
        "R10EO-R1 は監査専用。既存本番ファイル・既存テスト・既存ドキュメントは更新しない。",
        "全体 pytest は実施しない。", "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--search", action="store_true")
    args = parser.parse_args()
    destination = args.output.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    report: dict[str, Any] = {"phase": "169 R10EO-R1", "mode": "AUDIT_ONLY"}
    report["metadata"] = inspect_metadata_and_sources()
    if args.search:
        report["runtime"] = inspect_live_goal(n=30, k=11)
    (destination / "audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    (destination / "audit.md").write_text(render_markdown(report), encoding="utf-8")
    zeta = next(row for row in report["metadata"]["families"] if row["id"] == 16)
    print("R10EO_SERIES=" + str(report["metadata"]["series_count"]))
    print("R10EO_SOURCE_REGISTERED=" + str(report["metadata"]["registered_definition_ids"]))
    print("R10EO_ZETA_STATUS=" + zeta["citation_status"])
    print("R10EO_ZETA_SOURCE_CANDIDATES=" + str(len(zeta["literal_candidates"])))
    if "runtime" in report:
        live = report["runtime"]
        print("R10EO_PI41_30_STATUS=" + live["status"])
        print("R10EO_PI41_30_OPEN_GOALS=" + str(live["open_goal_types"]))
        print("R10EO_PI41_30_TRUST=" + live["trust"])
    print("R10EO_REPORT=" + str(destination / "audit.json"))
    print("R10EO_MODE=AUDIT_ONLY")


if __name__ == "__main__":
    main()
