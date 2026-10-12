"""Phase 163 R4-R67: read-only contextual excerpts for unresolved TeX spans."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

WINDOW = 14


def load_decisions(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data.get("phase") != "163 R4-R66" or data.get("reference_policy") != "ONE_REFERENCE_MULTIPLE_ASSERTIONS_ALLOWED":
        raise ValueError("Expected R4-R66 multi-assertion decisions")
    if len(data.get("records", [])) != 16 or data.get("assertion_proposal_count") != 21:
        raise ValueError("Expected 16 references and 21 assertions")
    if data.get("production_registry_modified") is not False or data.get("production_ids_allocated") is not False:
        raise ValueError("Input unexpectedly changed the production registry")
    if len({r["editorial_key"] for r in data["records"]}) != 16:
        raise ValueError("Duplicate editorial keys")
    return data


def build_context(data: dict, tex_root: Path, window: int = WINDOW) -> dict:
    if window < 1 or window > 80:
        raise ValueError("Context window must be between 1 and 80")
    output = []
    cache = {}
    for record in data["records"]:
        if record["boundary_status"] != "REQUIRES_CONTEXT_OR_SPAN_REVIEW":
            continue
        name = record["source_file"]
        if Path(name).name != name:
            raise ValueError("Unsafe TeX filename")
        if name not in cache:
            path = tex_root / name
            if not path.is_file():
                raise FileNotFoundError(path)
            cache[name] = path.read_text(encoding="utf-8-sig").splitlines()
        lines = cache[name]
        start, end = record["start_line"], record["end_line"]
        if not (1 <= start <= end <= len(lines)):
            raise ValueError(f"Invalid TeX span: {name}:{start}-{end}")
        span = "\n".join(lines[start-1:end])
        digest = hashlib.sha256(span.encode("utf-8")).hexdigest()
        if digest != record["source_text_sha256"]:
            raise ValueError(f"TeX source changed since R4-R66: {record['editorial_key']}")
        for assertion in record["assertions"]:
            if assertion["source_marker"] not in span:
                raise ValueError(f"Missing assertion marker: {record['editorial_key']}")
        lo, hi = max(1,start-window), min(len(lines),end+window)
        excerpt = [{"line":i, "region":"BEFORE" if i < start else "AFTER" if i > end else "ORIGINAL", "text":lines[i-1]} for i in range(lo,hi+1)]
        output.append({
            "editorial_key":record["editorial_key"],"chapter":record["chapter"],"source_file":name,
            "original_start_line":start,"original_end_line":end,"display_start_line":lo,"display_end_line":hi,
            "review_flags":record["review_flags"],"assertions":record["assertions"],
            "source_span_sha256_verified":True,"surrounding_lines":excerpt,
            "proposed_new_reference_start_line":None,"proposed_new_reference_end_line":None,
            "context_adequacy":"REQUIRES_HUMAN_REVIEW","mathematical_boundary_verified":False,
            "registration_action":"NONE",
        })
    if len(output) != 10 or sum(len(x["assertions"]) for x in output) != 13:
        raise ValueError("Expected ten flagged references and thirteen assertions")
    return {"phase":"163 R4-R67","mode":"READ_ONLY_CONTEXT_EXPANSION",
        "reference_policy":"ONE_REFERENCE_MULTIPLE_ASSERTIONS_ALLOWED",
        "reviewed_reference_count":len(output),"reviewed_assertion_count":sum(len(x["assertions"]) for x in output),
        "mathematical_boundary_verified_count":0,"semantic_registration_allowed_count":0,
        "production_registry_modified":False,"production_ids_allocated":False,"full_suite_run":False,
        "records":output}


def write_reports(result: dict, dest: Path) -> None:
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"context_review.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Phase 163 R4-R67：出典前後の確認資料","", "10件の暫定範囲について前後の TeX を示す。太字等による自動承認は行わない。", ""]
    for r in result["records"]:
        lines.extend([f"## {r['editorial_key']}（第{r['chapter']}章）", "",f"出典: `{r['source_file']}`、元の範囲: {r['original_start_line']}–{r['original_end_line']}、確認表示: {r['display_start_line']}–{r['display_end_line']}", "",f"保留理由: {', '.join(r['review_flags'])}", "", "```text"])
        for line in r["surrounding_lines"]:
            lines.append(f"{line['line']:>5} [{line['region']:<8}] {line['text']}")
        lines.extend(["```", "", "判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査", ""])
    lines.extend(["正式 ID、数学的承認、Registry 変更、証明探索への接続は行わない。", "全体 pytest は実施しない。", ""])
    (dest/"context_review.md").write_text("\n".join(lines),encoding="utf-8")


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--decisions",type=Path,required=True)
    parser.add_argument("--tex-root",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=build_context(load_decisions(args.decisions),args.tex_root)
    write_reports(result,args.output)
    print(json.dumps({k:v for k,v in result.items() if k!="records"},ensure_ascii=False,indent=2))
    print("R4-R67 context expansion complete. Full pytest not run.")


if __name__ == "__main__":
    main()
