"""Chapter VI family definitions: source/text/metadata only, never a proof leaf.

This audit deliberately does not edit a source registry or invent publication
positions.  Full citation eligibility and Trust Boundary replay are later steps.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "sources" / "toda" / "Toda_06_2.tex"
GENERATOR_CSV = ROOT / "data" / "HyoujiGen.csv"
MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"

# The source form is checked literally. The symbol in HyoujiGen is only
# identity metadata, and its spelling need not match the source's LaTeX form.
FAMILIES = (
    {
        "label": "epsilon",
        "id": 10,
        "name": "ε",
        "latex": r"\varepsilon",
        "stem": 8,
        "minimum_n": 3,
        "section": r"\paragraph{i). The Elements \(\varepsilon_n\).}",
        "clause": r"\varepsilon_n:=E^{\,n-3}\varepsilon_3\quad (n\ge3)",
        "next_section": r"\paragraph{ii). The elements \(\,\overline{\nu}_n\).}",
    },
    {
        "label": "bar_nu",
        "id": 11,
        "name": "ν̅",
        "latex": r"\bar{\nu}",
        "stem": 8,
        "minimum_n": 6,
        "section": r"\paragraph{ii). The elements \(\,\overline{\nu}_n\).}",
        "clause": r"\overline{\nu}_n:=E^{\,n-6}\overline{\nu}_6\ (n\ge6)",
        "next_section": r"\paragraph{iii). The elements \(\mu_n\).}",
    },
    {
        "label": "mu",
        "id": 12,
        "name": "μ",
        "latex": r"\mu",
        "stem": 9,
        "minimum_n": 3,
        "section": r"\paragraph{iii). The elements \(\mu_n\).}",
        "clause": r"\mu_{n}:=E^{\,n-3}\mu_{3}",
        "next_section": r"\paragraph{iv). The element \(\varepsilon'\).}",
    },
)


def inspect_source_clause(text: str, spec: dict) -> dict:
    """Require one literal defining clause inside one matching source section."""
    section, following, clause = (
        spec["section"], spec["next_section"], spec["clause"]
    )
    if text.count(section) != 1 or text.count(following) != 1:
        raise ValueError(f"ambiguous Chapter VI section: {spec['label']}")
    first = text.index(section)
    last = text.index(following)
    if first >= last:
        raise ValueError(f"incorrect Chapter VI section order: {spec['label']}")
    if text.count(clause) != 1:
        raise ValueError(f"missing/repeated literal source clause: {spec['label']}")
    location = text.index(clause)
    if not first < location < last:
        raise ValueError(f"source clause is outside reviewed section: {spec['label']}")
    # The source is a transcription in this repository.  A checked location
    # does NOT independently authenticate Toda's original printed edition.
    return {
        "label": spec["label"],
        "section_line": text.count("\n", 0, first) + 1,
        "clause_line": text.count("\n", 0, location) + 1,
        "following_section_line": text.count("\n", 0, last) + 1,
        "unique_source_clause": True,
        "defining_clause": clause,
        "original_edition_verified": False,
    }


def inspect_generator_metadata(csv_text: str, spec: dict) -> dict:
    """Check one genuine kinds=0 series ID without promoting DB data to fact."""
    rows = tuple(csv.DictReader(csv_text.lstrip("\ufeff").splitlines()))
    matching = [r for r in rows if r.get("id") == str(spec["id"])]
    if len(matching) != 1:
        raise ValueError(f"missing/duplicate HyoujiGen ID: {spec['id']}")
    record = matching[0]
    expected = {
        "display": spec["name"],
        "latex": spec["latex"],
        "kinds": "0",
        "k": str(spec["stem"]),
        "n": str(spec["minimum_n"]),
    }
    if any(record.get(key, "").strip() != val for key, val in expected.items()):
        raise ValueError(f"typed HyoujiGen metadata mismatch: {spec['label']}")
    return {
        "family_id": spec["id"],
        "stem": spec["stem"],
        "minimum_n": spec["minimum_n"],
        "metadata_only": True,
    }


def inspect_manifest(text: str) -> dict:
    """Observe existing chapter coverage; do not synthesize Chapter VI positions."""
    data = json.loads(text)
    if (data.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or data.get("publication_order_scope")
            != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise ValueError("unreviewed reference manifest provenance")
    entries = data.get("assertions")
    if not isinstance(entries, list):
        raise ValueError("manifest assertion list missing")
    chapters = sorted({item.get("chapter") for item in entries
                       if isinstance(item, dict)
                       and type(item.get("chapter")) is int})
    chapter6 = [item for item in entries if isinstance(item, dict)
                and (item.get("chapter") == 6
                     or item.get("source_file") == "Toda_06_2.tex")]
    return {
        "chapters": chapters,
        "chapter6_entries": len(chapter6),
        "chapter6_position_covered": bool(chapter6),
        "publication_position_invented": False,
    }


def build_report(source_text: str, csv_text: str, manifest_text: str,
                 registered_family_ids: tuple[int, ...]) -> dict:
    """Combine independent observations without constructing any proof object."""
    definitions = []
    for spec in FAMILIES:
        definitions.append({
            **inspect_source_clause(source_text, spec),
            **inspect_generator_metadata(csv_text, spec),
            "already_cited_by_r10d2": spec["id"] in registered_family_ids,
        })
    coverage = inspect_manifest(manifest_text)
    return {
        "phase": "169 R10E7",
        "mode": "AUDIT_ONLY",
        "source": "sources/toda/Toda_06_2.tex (adopted transcription)",
        "definitions": definitions,
        "manifest": coverage,
        "currently_registered_source_ids": list(registered_family_ids),
        "citation_registration_ready": False,
        "next_requirement": (
            "Review Chapter VI publication-position anchors and extend the "
            "existing cited stable-family registry without fabricating GIVENs"
        ),
        "production_files_modified": [],
        "full_pytest_run": False,
    }


def main() -> None:
    from phase169_r10d2_general_family_definition.family_citation import (
        SOURCE_RECORDS,
    )
    registered = tuple(x.family_id for x in SOURCE_RECORDS)
    if registered != (4, 9):
        raise ValueError("R10D2 cited-family baseline changed; review required")
    report = build_report(
        SOURCE.read_text(encoding="utf-8-sig"),
        GENERATOR_CSV.read_text(encoding="utf-8-sig"),
        MANIFEST.read_text(encoding="utf-8-sig"),
        registered,
    )
    folder = HERE / "output"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 169 R10E7 — Chapter VI 系列定義の引用境界監査", "",
        "AUDIT_ONLY。原典の採用転写から定義式の存在・位置を確認した。", "",
        "| 系列 | HyoujiGen ID | 懸垂定義の行 | stem | 最小 n | R10D2登録 |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for item in report["definitions"]:
        lines.append(
            f"| {item['label']} | {item['family_id']} | {item['clause_line']} | "
            f"{item['stem']} | {item['minimum_n']} | "
            f"{item['already_cited_by_r10d2']} |"
        )
        print("R10E7_" + item["label"].upper() + "_SOURCE=PASS")
    covered = report["manifest"]["chapter6_position_covered"]
    lines.extend([
        "", f"既存 manifest の Chapter VI 掲載位置: {'あり' if covered else 'なし'}。",
        "採用転写の行番号は原著の出版順序を認証するものではない。",
        "名前・型の一致は GeneratorImage を証明しない。",
        "独立に検証した文献登録と Trust Boundary の審査までは未完成のまま。",
        "全体 pytest は実行しない。", "",
    ])
    (folder / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("R10E7_CH6_MANIFEST_ENTRIES=" + str(report["manifest"]["chapter6_entries"]))
    print("R10E7_PRODUCTION_FILES_CHANGED=none")
    print("R10E7_FULL_PYTEST_RUN=False")
    print("R10E7_AUDIT_JSON=" + str(folder / "audit.json"))
    print("R10E7_AUDIT_MD=" + str(folder / "audit.md"))


if __name__ == "__main__":
    main()
