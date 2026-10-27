"""Phase 169 R9: read-only stable-family metadata and narrative audit.

No EHP application modules are imported. No production files are modified.
"""
from __future__ import annotations

import ast
import csv
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
CSV_PATH = ROOT / "data" / "HyoujiGen.csv"

SOURCES = {
    "phase166_r3aj_structured_generator.py": ("_base_element", "structured_generator_from_ids"),
    "phase169_r7_general_stable_transport/rule.py": (
        "_intermediate_typed_generator",
        "_consecutive_generator_image_goals",
        "general_stable_cyclic_transport_rule",
    ),
    "phase168_r3_5_model_renderer.py": ("render_model_backed_narrative_markdown",),
    "phase165_r12_r21_eta_generator_chain.py": (
        "_composition_eta_suspensions", "expand_cited_eta_generator",
    ),
    "phase165_r52_r9_shared_math.py": ("shared_expansion_provider",),
}


def git(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=12,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def read_family_rows(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"id", "display", "kinds", "k", "n", "latex"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("HyoujiGen.csv lacks required columns")
        rows: list[dict[str, object]] = []
        for row in reader:
            parsed = {
                "id": int(row["id"]),
                "display": row["display"],
                "kinds": int(row["kinds"]),
                "k": int(row["k"]),
                "n_min": int(row["n"]),
                "latex": row["latex"],
                "stable": row.get("stable", ""),
                "stable_orders": row.get("stable_orders", ""),
            }
            parsed["freudenthal_start"] = max(2, parsed["k"] + 2)
            parsed["at_minimum_in_stable_range"] = (
                parsed["n_min"] >= parsed["freudenthal_start"]
            )
            rows.append(parsed)
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("HyoujiGen has duplicate generator IDs")
    return rows


def inspect_source(relative: str, functions: tuple[str, ...]) -> dict[str, object]:
    path = ROOT / relative
    if not path.is_file():
        return {"present": False, "functions_missing": list(functions)}
    contents = path.read_bytes()
    parsed = ast.parse(contents.decode("utf-8-sig"), filename=str(path))
    declarations = {n.name: n for n in parsed.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    return {
        "present": True,
        "sha256": hashlib.sha256(contents).hexdigest(),
        "functions_missing": [name for name in functions if name not in declarations],
        "functions": {
            name: {"line": declarations[name].lineno, "end_line": declarations[name].end_lineno}
            for name in functions if name in declarations
        },
    }


def family_name(row: dict[str, object], dimension: int) -> tuple[int, int, int] | None:
    """Return structural (family-id, target degree, sphere degree), NOT a proof."""
    if row["kinds"] != 0 or dimension < row["n_min"] or dimension < 2:
        return None
    return row["id"], dimension + row["k"], dimension


def family_transport_shape(row: dict[str, object], n: int, r: int) -> bool:
    """Check the names' candidate dimensions; not a generator-image certificate."""
    return (
        type(n) is int and type(r) is int and r >= 0
        and family_name(row, n) is not None
        and family_name(row, n + r) is not None
    )


def stable_group_transport_allowed(row: dict[str, object], n: int, r: int) -> bool:
    return family_transport_shape(row, n, r) and n >= row["k"] + 2


def main() -> int:
    rows = read_family_rows(CSV_PATH)
    stable = [row for row in rows if row["kinds"] == 0]
    below = [row for row in stable if not row["at_minimum_in_stable_range"]]
    source_checks = {path: inspect_source(path, names) for path, names in SOURCES.items()}
    examples = []
    for id_, n, r in ((2, 2, 1), (2, 3, 5), (4, 4, 1), (4, 5, 2),
                       (9, 8, 1), (9, 9, 3), (10, 3, 7), (10, 10, 2)):
        row = next(item for item in rows if item["id"] == id_)
        examples.append({
            "id": id_, "display": row["display"], "k": row["k"],
            "n": n, "r": r,
            "family_notation_candidate": family_transport_shape(row, n, r),
            "stable_group_isomorphism_range": stable_group_transport_allowed(row, n, r),
        })
    audit = {
        "phase": "169-R9", "kind": "AUDIT_ONLY",
        "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "local_head": git("rev-parse", "HEAD"),
        "local_branch": git("branch", "--show-current"),
        "git_status": git("status", "--porcelain"),
        "remote_develop": git("ls-remote", "origin", "refs/heads/develop"),
        "hyoujigen_sha256": hashlib.sha256(CSV_PATH.read_bytes()).hexdigest(),
        "all_rows": len(rows), "kinds_zero_count": len(stable),
        "kinds_zero_below_stable_range": len(below),
        "family_records": stable,
        "examples": examples,
        "source_checks": source_checks,
        "proof_or_renderer_modified": False,
        "whole_pytest_run": False,
        "interpretation": [
            "kinds=0 identifies DB suspension-family notation, not a group isomorphism at its minimum n.",
            "The stable group range is n >= k+2, independently of HyoujiGen n_min.",
            "DB family identity is metadata; proof of a named suspension requires cited definition/evidence.",
            "Eta-square composition can be compressed in narrative only after proving all image premises.",
            "No unproved base group, including pi_8^5, is promoted to a GIVEN.",
        ],
    }
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    example_table = "\n".join(
        f"| {x['display']} | {x['n']} | {x['r']} | {x['family_notation_candidate']} | {x['stable_group_isomorphism_range']} |"
        for x in examples
    )
    src_table = "\n".join(
        f"| `{k}` | {v['present']} | {', '.join(v['functions_missing']) or '-'} |"
        for k, v in source_checks.items()
    )
    note = "\n".join([
        "# Phase 169 R9 — HyoujiGen stable-family 設計監査", "",
        f"- Git local HEAD: `{audit['local_head']}`",
        f"- Git local branch: `{audit['local_branch']}`",
        f"- DB rows: {len(rows)}", f"- kinds=0: {len(stable)}",
        f"- kinds=0 かつ最小次元が安定範囲外: {len(below)}", "",
        "## 次元境界", "",
        "| 系列 | 元の次元 n | 回数 r | 系列表記の候補 | 懸垂同型の安定範囲 |",
        "|---|---:|---:|---|---|", example_table, "",
        "系列表記の候補は数学的な等式を証明しない。",
        "DB の family ID と `n_min` は命名のための情報であり、", 
        "群同型には Freudenthal の `n >= k+2` と Toda (4.5) の先行出典が必要。", "",
        "## 関連コード", "", "| ファイル | 有り | 関数欠落 |", "|---|---|---|", src_table, "",
        "## 目標となる表示", "",
        "`[R3]より, $E^4(\\eta_4^2)=\\eta_8^2$.`", "",
        "これは実際の Proof Tree に全ての中間 GeneratorImage が証明済みのときのみ表示可能。", "",
        "## 実装後の責務境界", "",
        "1. 型付き家族の同定: DB ID/kinds/k/n_min による候補生成。",
        "2. 命名の数学的根拠: 登録済みの定義・文献に結合。DB 行自体は GIVEN としない。",
        "3. 群同型: Toda (4.5) に基づく stable-range 検査を独立に維持。",
        "4. 合成元: 懸垂と合成の関係を型付き再帰規則から証明。",
        "5. Narrative: Proof Tree は完全保存し、証明済み連鎖のみ一式に圧縮。",
        "6. 基点 π_8^5 の incomplete は別問題として残す。", "",
        "本 ZIP は監査専用。本番変更なし。全体 pytest なし。",
    ]) + "\n"
    (OUTPUT / "audit.md").write_text(note, encoding="utf-8")
    missing = [path for path, checked in source_checks.items() if not checked["present"] or checked["functions_missing"]]
    print("R9_AUDIT_ONLY=True")
    print("R9_GIT_HEAD=" + str(audit["local_head"]))
    print("R9_HYOUJIGEN_ROWS=" + str(len(rows)))
    print("R9_KINDS_ZERO=" + str(len(stable)))
    print("R9_KIND0_MINIMUM_NOT_STABLE=" + str(len(below)))
    print("R9_RELATED_FILES=" + str(len(source_checks)))
    print("R9_MISSING_APIS=" + str(len(missing)))
    print("R9_PRODUCTION_PATCHED=False")
    print("R9_WHOLE_PYTEST_RUN=False")
    print("R9_REPORT=" + str(OUTPUT / 'audit.md'))
    if missing:
        print("R9_CHANGED_OR_MISSING=" + str(missing))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
