"""R79: exact TeX bounded fixed-claim previews beside R78 internal claims."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin,
    LiteratureEntry, ReferenceKind, UnifiedStatementRegistry,
)

SOURCES = {
    "Toda_01_corrected.tex": "92cbfbb9b3ea9ba59a07450a5a8f16ec6b80715bb8b7d8f6eab442dd1a402605",
    "Toda_02_2(2).tex": "13d03c1e5767c64fb7da8fc9293bbb47f202884d304bfb06f4c7a6f0f8fdbe72",
    "Toda_04_2(2).tex": "4aef8ef8716bebf4f83e7ebafbaffe58a874fc0efb3b18a8acce24dad9c506aa",
}
# Inclusive source line spans, captured from the numbered statement, NOT the proof.
CLAIMS = (
    ("prop:1-6", "Toda_01_corrected.tex", 967, 977, "last_argument_additivity"),
    ("prop:1-6", "Toda_01_corrected.tex", 978, 985, "middle_argument_additivity"),
    ("prop:1-6", "Toda_01_corrected.tex", 986, 994, "first_argument_additivity"),
    ("thm:2.4", "Toda_02_2(2).tex", 492, 496, "odd_dimension_case"),
    ("thm:2.4", "Toda_02_2(2).tex", 497, 502, "even_dimension_case"),
    ("prop:2.5", "Toda_02_2(2).tex", 962, 965, "delta_composition"),
    ("prop:2.5", "Toda_02_2(2).tex", 966, 974, "whitehead_product_case"),
    ("prop:4.2", "Toda_04_2(2).tex", 258, 266, "ehp_exact_sequence"),
)
OWNERS = {
    "prop:1-6": (ReferenceKind.PROPOSITION, "Proposition 1.6", "Toda_01_corrected.tex", 965, 995),
    "thm:2.4": (ReferenceKind.THEOREM, "Theorem 2.4", "Toda_02_2(2).tex", 483, 504),
    "prop:2.5": (ReferenceKind.PROPOSITION, "Proposition 2.5", "Toda_02_2(2).tex", 960, 975),
    "prop:4.2": (ReferenceKind.PROPOSITION, "Proposition 4.2", "Toda_04_2(2).tex", 256, 267),
}


def load_sources(source_dir: Path, *, expected_hashes=None):
    expected = SOURCES if expected_hashes is None else expected_hashes
    result = {}
    for name, digest in expected.items():
        raw = (source_dir / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError(f"TeX SHA256 mismatch: {name}")
        result[name] = raw.decode("utf-8-sig").splitlines()
    return result


def build_preview(r78: dict, sources: dict):
    if r78.get("phase") != "163 R4-R78" or r78.get("preview_proof_internal_count") != 10:
        raise ValueError("R78 input is missing or mismatched")
    internal = [r for r in r78["records"] if r["preview_status"] == "PROOF_INTERNAL_PREVIEW"]
    if len(internal) != 10 or len({r["preview_assertion_id"] for r in internal}) != 10:
        raise ValueError("R78 internal claims are not unique")
    if set(r["source_owner_label"] for r in internal) != set(OWNERS):
        raise ValueError("R78 owners mismatch")
    registry = UnifiedStatementRegistry()
    for owner, (kind, locator, fname, begin, end) in OWNERS.items():
        lines = sources[fname]
        head = "\n".join(lines[begin-1:end])
        if f"\\label{{{owner}}}" not in head or f"\\end{{{kind.value}}}" not in head:
            raise ValueError(f"numbered statement boundary changed: {owner}")
        registry.add_reference(LiteratureEntry(f"preview:{owner}",kind,locator,source_id=fname))
    records = []
    counts = Counter()
    for owner, fname, begin, end, slug in CLAIMS:
        meta = OWNERS[owner]
        if fname != meta[2] or not(meta[3] <= begin <= end <= meta[4]):
            raise ValueError(f"claim escaped statement: {slug}")
        text = "\n".join(sources[fname][begin - 1:end])
        if not text.strip() or not any(marker in text for marker in ("\\[", "\\begin{equation}")):
            raise ValueError(f"invalid bounded claim: {slug}")
        counts[owner] += 1
        aid = f"preview:fixed:{owner}:{slug}"
        registry.add_assertion(AssertionEntry(aid, f"preview:{owner}", AssertionKind.STATEMENT,
                                              text, AssertionOrigin.FIXED_STATEMENT,
                                              component_position=counts[owner]))
        records.append({"owner": owner, "assertion_id": aid, "source_file": fname,
                        "start_line": begin, "end_line": end, "claim_text": text,
                        "full_statement_text": "\n".join(sources[fname][meta[3]-1:meta[4]]),
                        "claim_sha256": hashlib.sha256(text.encode()).hexdigest(),
                        "registration_allowed": False, "original_edition_verified": False})
    for r in internal:
        owner = r["source_owner_label"]
        registry.add_assertion(AssertionEntry(r["preview_assertion_id"], f"preview:{owner}",
                                              AssertionKind.STATEMENT, r["original_excerpt_sha256"],
                                              AssertionOrigin.PROOF_INTERNAL))
    for owner in OWNERS:
        actual = registry.assertions_for(f"preview:{owner}")
        if sum(a.origin is AssertionOrigin.FIXED_STATEMENT for a in actual) != counts[owner]:
            raise AssertionError("fixed assertion count changed")
    if len(records) != 8 or sum(counts.values()) != 8:
        raise AssertionError("fixed candidate count mismatch")
    return {"phase":"163 R4-R79", "mode":"TRANSIENT_EXACT_TEX_FIXED_AND_INTERNAL_PREVIEW",
            "source_phase":"163 R4-R78", "preview_reference_count":len(OWNERS),
            "preview_fixed_statement_count":len(records), "preview_proof_internal_count":len(internal),
            "fixed_counts_by_owner":dict(counts), "paraphrase_hold_count":1,
            "tex_boundary_checked":True, "original_edition_verified":False,
            "formal_source_boundary_verified_count":0, "mathematical_role_verified_count":0,
            "semantic_registration_allowed_count":0, "production_registry_modified":False,
            "production_ids_allocated":False, "proof_search_connected":False, "full_suite_run":False,
            "fixed_statement_previews":records}


def write_results(result: dict, output: Path):
    output.mkdir(parents=True,exist_ok=True)
    (output/"fixed_statement_preview.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Phase 163 R4-R79：番号付き命題本文の登録案", "",
           "日本語 TeX の所定の命題本文範囲のみ抽出。番号付き証明内の式とは分離。",
           "", f"- 一時 Reference：{result['preview_reference_count']}",
           f"- Fixed-statement 一時 Assertion：{result['preview_fixed_statement_count']}",
           f"- 既存 Proof-internal 一時 Assertion：{result['preview_proof_internal_count']}",
           "- 原本照合・数学的認定・正式 ID 採番：未実施", "",
           "| 命題 | 出典行 | 仮 Assertion |", "|---|---|---|"]
    for r in result["fixed_statement_previews"]:
        lines.append(f"| {r['owner']} | {r['source_file']}:{r['start_line']}-{r['end_line']} | `{r['assertion_id']}` |")
    (output/"report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--r78",type=Path,required=True)
    parser.add_argument("--sources",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    data=json.loads(args.r78.read_text(encoding="utf-8"))
    result=build_preview(data,load_sources(args.sources))
    write_results(result,args.output)
    print(json.dumps({k:v for k,v in result.items() if k!="fixed_statement_previews"},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
