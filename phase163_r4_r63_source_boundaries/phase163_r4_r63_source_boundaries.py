"""R4-R63: source-span proposals only; no approved literature registration."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

# Hand-reviewed text spans in the supplied TeX edition, never formal proof boundaries.
# A span can be larger than one definition and should not imply that its full contents
# constitute one Assertion.
SPAN_PROPOSALS = {
    "unit_sphere": (80,83,"LOCAL_DISPLAY","S^n"),
    "pointed_homotopy_classes": (155,159,"LOCAL_DISPLAY_WITH_SENTENCE","[X,Y]"),
    "composition_homotopy_classes": (163,170,"PRECEDING_SETUP_AND_NAMING","composition"),
    "iterated_suspension": (283,288,"DISPLAY_AND_NAMING","E^n X"),
    "addition_inverse_suspension": (341,354,"TWO_DISPLAY_DEFINITIONS","f+g; -f"),
    "secondary_composition": (535,540,"CONSTRUCTION_DEPENDS_ON_PRIOR_TEXT","secondary composition"),
    "reduced_cone": (1084,1087,"LOCAL_DISPLAY","CX"),
    "extension": (1099,1103,"PRECEDING_CONDITION","extension"),
    "coextension": (1105,1117,"PRECEDING_CONDITION_AND_DISPLAY","coextension"),
    "stable_homotopy_group": (1199,1206,"ADJACENT_DEFINITIONS","G_k; E^infty"),
    "stable_composition": (1214,1221,"MAP_AND_NAMING","composition on G"),
    "stable_toda_bracket": (1236,1266,"EXTENDED_CONSTRUCTION","stable Toda bracket"),
    "nu4_generator_notation": (567,579,"PIECEWISE_DEFINITION","nu_4"),
    "nu_n_notation": (605,607,"MULTIPLE_SYMBOLS_IN_DISPLAY","nu_n; nu"),
    "eta_n_cubed_notation": (608,612,"MULTIPLE_SYMBOLS_IN_DISPLAY","eta_n^3; eta^3"),
    "nu_n_squared_notation": (1320,1323,"MULTIPLE_SYMBOLS_IN_DISPLAY","nu_n^2; nu^2"),
}
MULTIPLE = {"addition_inverse_suspension","stable_homotopy_group","nu_n_notation","eta_n_cubed_notation","nu_n_squared_notation"}
OPEN_CONTEXT = {"composition_homotopy_classes","secondary_composition","extension","coextension","stable_toda_bracket"}


def load_inputs(inventory_path, tex_root):
    inventory_path=Path(inventory_path)
    data=json.loads(inventory_path.read_text(encoding="utf-8"))
    if data.get("phase") != "163 R4-R62" or data.get("remaining_definition_candidate_count") != 16:
        raise ValueError("expected R4-R62 inventory with 16 candidates")
    if data.get("semantic_registration_approved_count") != 0 or data.get("production_registry_modified"):
        raise ValueError("source inventory was already promoted")
    sources={}
    for item in data["records"]:
        name=item["source_file"]
        path=Path(tex_root)/name
        if not path.is_file():
            raise FileNotFoundError(str(path))
        if name not in sources:
            raw=path.read_bytes()
            sources[name]={"lines":raw.decode("utf-8-sig").splitlines(),"sha256":hashlib.sha256(raw).hexdigest()}
    return data,sources


def audit_boundaries(data,sources):
    records=data["records"]
    if len(records)!=16 or len({x["editorial_key"] for x in records}) != 16:
        raise ValueError("candidate identity count differs")
    if set(x["editorial_key"] for x in records)!=set(SPAN_PROPOSALS):
        raise ValueError("reviewed span set differs from inventory")
    output=[]
    for r in records:
        key=r["editorial_key"]
        start,end,kind,subjects=SPAN_PROPOSALS[key]
        lines=sources[r["source_file"]]["lines"]
        anchor=r["source_line"]
        if not (1<=start<=anchor<=end<=len(lines)):
            raise ValueError(f"invalid source boundaries for {key}")
        excerpt=r["source_excerpt"].replace("\r\n","\n").strip()
        full="\n".join(lines)
        if excerpt not in full:
            raise ValueError(f"source excerpt changed: {key}")
        if excerpt not in "\n".join(lines[start-1:end]):
            # Naming lines with an excerpt in another logical block must be enlarged,
            # rather than silently losing exact quoted source evidence.
            raise ValueError(f"excerpt is not covered by span: {key}")
        if not lines[anchor-1].strip():
            raise ValueError(f"empty anchor: {key}")
        warnings=[]
        if key in MULTIPLE:
            warnings.append("POTENTIAL_MULTIPLE_ASSERTIONS")
        if key in OPEN_CONTEXT:
            warnings.append("MATHEMATICAL_CONTEXT_OUTSIDE_SPAN")
        if key in {"nu_n_notation","eta_n_cubed_notation"}:
            warnings.append("SHARED_ADJACENT_NOTATION_BLOCK")
        output.append({
            "editorial_key":key,"chapter":r["chapter"],"source_file":r["source_file"],
            "source_line":anchor,"proposed_start_line":start,"proposed_end_line":end,
            "span_kind":kind,"editorial_subjects_unverified":subjects,
            "source_span_text":"\n".join(lines[start-1:end]),
            "source_file_sha256":sources[r["source_file"]]["sha256"],
            "excerpt_exactly_contained":True,"source_anchor_in_span":True,
            "warning_codes":warnings,
            "span_review_status":"PROVISIONAL_SOURCE_ANCHOR_NOT_COMPLETE_MATHEMATICAL_BOUNDARY",
            "publication_position":None,"defined_symbol_verified":None,
            "formal_assertion_count_verified":0,"production_reference_id":None,
            "production_assertion_id":None,"semantic_registration_allowed":False,
        })
    output.sort(key=lambda r:(r["chapter"],r["source_line"],r["editorial_key"]))
    return {
        "phase":"163 R4-R63","mode":"READ_ONLY_PROVISIONAL_TEX_DEFINITION_SPANS",
        "candidate_count":len(output),"source_excerpt_verified_count":len(output),
        "source_span_proposed_count":len(output),
        "multi_assertion_review_count":sum("POTENTIAL_MULTIPLE_ASSERTIONS" in r["warning_codes"] for r in output),
        "external_context_review_count":sum("MATHEMATICAL_CONTEXT_OUTSIDE_SPAN" in r["warning_codes"] for r in output),
        "mathematical_boundary_verified_count":0,
        "publication_position_verified_count":0,
        "definition_symbol_verified_count":0,
        "pending_other_candidates_count":data["pending_other_candidates_count"],
        "production_registry_modified":False,"production_ids_allocated":False,
        "proof_search_connected":False,"original_edition_verified":False,
        "records":output,
    }


def write_reports(data, output_dir):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    (out/"source_boundaries.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    fields=["chapter","source_file","editorial_key","source_line","proposed_start_line","proposed_end_line","span_kind","editorial_subjects_unverified","span_review_status"]
    with (out/"source_boundaries.csv").open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");writer.writeheader();writer.writerows(data["records"])
    report=["# Phase 163 R4-R63：未番号 Definition 候補の TeX 範囲監査","",
            "出典の開始・終了行は**監査用の暫定候補**であり、定義全体の数学的範囲を確定したものではない。","",
            "|章|候補|暫定出典範囲|要注意|","|---:|---|---|---|"]
    for r in data["records"]:
        report.append(f'|{r["chapter"]}|`{r["editorial_key"]}`|{r["proposed_start_line"]}–{r["proposed_end_line"]}|{", ".join(r["warning_codes"]) or "—"}|')
    report.extend(["","特記事項：第5章の ν 記法と η³ 記法は隣接した二つの数式に分かれる。各数式内にも複数記号がある。",
                   "第3章の stable Toda bracket は 1236–1266 行を確認したが、前後の仮定や既出の構成は別途照合が必要。",
                   "掲載順、定義対象の確定、数学的同値性、原本照合は未完了。本番 Registry と ID、証明探索は未変更。",
                   "全体 pytest は実施しない。"])
    (out/"report.md").write_text("\n".join(report)+"\n",encoding="utf-8")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--inventory",required=True)
    parser.add_argument("--tex-root",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    inventory,sources=load_inputs(args.inventory,args.tex_root)
    result=audit_boundaries(inventory,sources)
    write_reports(result,args.output)
    print(json.dumps({k:v for k,v in result.items() if k!="records"},ensure_ascii=False,indent=2))
    print("R4-R63 provisional source span audit complete. Full pytest not run.")

if __name__=="__main__":
    main()
