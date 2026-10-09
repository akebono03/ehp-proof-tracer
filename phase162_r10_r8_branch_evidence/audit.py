"""Phase 162 R10-R8: proof-branch relevance and duplicate provenance audit.
Read-only; each classification is evidence, not an instruction to drop a step.
"""
from __future__ import annotations
import argparse
import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text or "").replace(r"\left", "").replace(r"\right", "")


def shortest_root_branch(node_id: int, nodes: dict[int, dict], root_id: int) -> tuple[int, ...] | None:
    """Find a shortest premise-to-root path respecting directed parent edges."""
    if node_id not in nodes or root_id not in nodes:
        return None
    queue = deque([(node_id, (node_id,))])
    visited = {node_id}
    while queue:
        current, chain = queue.popleft()
        if current == root_id:
            return chain
        for parent in nodes[current].get("parent_node_ids", []):
            if parent in nodes and parent not in visited:
                queue.append((parent, chain + (parent,)))
                visited.add(parent)
    return None


def branches_of_root(nodes: dict[int, dict], root_id: int) -> dict[int, set[int]]:
    """Partition by direct root premises, allowing shared ancestors."""
    answer = {}
    for entry in nodes[root_id].get("premise_node_ids", []):
        visited = set()
        pending = [entry]
        while pending:
            nid = pending.pop()
            if nid in visited or nid not in nodes:
                continue
            visited.add(nid)
            pending.extend(nodes[nid].get("premise_node_ids", []))
        answer[entry] = visited
    return answer


def issue_labels(line: dict) -> tuple[str, ...]:
    text = normalize(line.get("text", ""))
    result = []
    if "H:" in text and (r"\pi_{3}^{2}" in text or r"\pi_3^2" in text) and (r"\pi_{3}^{3}" in text or r"\pi_3^3" in text):
        result.append("OFF_TARGET_H_MAP")
    if any(term in text for term in (r"\Delta(\iota_{5})",r"\Delta\left(\iota_{5}\right)",r"\Delta(\iota_5)")):
        result.append("DELTA_IOTA5")
    if any(term in text for term in (r"[\iota_{2},\iota_{2}]",r"[\iota_2,\iota_2]")):
        result.append("WHITEHEAD_SQUARE")
    if "証明木に記録された群構造の移送" in text or line.get("origin") == "TRANSPORT_APPENDIX":
        result.append("TRANSPORT_APPENDIX")
    return tuple(result)


def analyze(data: dict) -> dict:
    nodes = {n["id"]:n for n in data["steps"]}
    roots = sorted(nid for nid,n in nodes.items() if not n.get("parent_node_ids"))
    if len(roots)!=1:
        raise ValueError(f"Expected one root; got {roots}")
    root_id = roots[0]
    branches=branches_of_root(nodes,root_id)
    text_occurrences=defaultdict(list)
    for row in data["body_lines"]:
        text_occurrences[normalize(row.get("text", ""))].append(row["line"])
    latex_occurrences=defaultdict(list)
    for node in nodes.values():
        expression=normalize(node.get("statement_latex") or "")
        if expression:
            latex_occurrences[expression].append(node["id"])
    details=[]
    for row in data["body_lines"]:
        tags=issue_labels(row)
        if not tags:
            continue
        candidates=sorted(set(i for i in row.get("candidate_step_ids",[]) if i in nodes))
        matched=[]
        for nid in candidates:
            node=nodes[nid]
            matched.append({"id":nid,"statement_type":node.get("statement_type"),
                "rule":node.get("proof_rule"),"inference_rule":node.get("inference_rule"),
                "reference":node.get("reference_locator"),"parents":node.get("parent_node_ids",[]),
                "root_branches":[b for b,members in branches.items() if nid in members],
                "path_to_root":shortest_root_branch(nid,nodes,root_id),
                "equivalent_statement_nodes":latex_occurrences[normalize(node.get("statement_latex") or "")],
                "statement_latex":node.get("statement_latex")})
        duplicated=text_occurrences[normalize(row.get("text",""))]
        details.append({"line":row["line"],"tags":tags,"text":row.get("text",""),
            "origin":row.get("origin"),"direct_step_candidates":matched,
            "duplicate_rendered_lines":duplicated if len(duplicated)>1 else [],
            "assessment":("DIRECT_STEP_CANDIDATE" if matched else "NOT_DIRECTLY_ATTRIBUTED"),
            "safe_to_delete":False})
    return {"source":"phase162_r10_r5_prose_origin.json","root_node_id":root_id,
        "root_branches":[{"node_id":bid,"nodes":len(ids),"statement":nodes[bid].get("statement_latex"),
             "inference_rule":nodes[bid].get("inference_rule")} for bid,ids in branches.items()],
        "counts":{"nodes":len(nodes),"body_lines":len(data["body_lines"]),
            "flagged_lines":len(details),"by_tag":dict(Counter(tag for d in details for tag in d["tags"])),
            "flagged_with_direct_step":sum(bool(d["direct_step_candidates"]) for d in details)},
        "flagged_lines":details,"limitations":[
            "A path to the final conclusion does not prove the corresponding step should be shown in prose.",
            "Line-level exact LaTeX matching is not a rendering call trace.",
            "No ProofStep or source file has been modified; duplicate removal requires separate evidence."]}


def write_report(data:dict,repo:Path)->None:
    (repo/'phase162_r10_r8_branch_evidence.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    out=['# Phase 162 R10-R8：本文の根拠分岐監査','','## 集計','',
         f"- 証明木ノード：{data['counts']['nodes']}",
         f"- 本文行：{data['counts']['body_lines']}",
         f"- 問題候補行：{data['counts']['flagged_lines']}",
         f"- 直接一致のある問題行：{data['counts']['flagged_with_direct_step']}",
         f"- 分類：{data['counts']['by_tag']}",'','## 最終目標の直接前提分岐','']
    for branch in data['root_branches']:
        out.append(f"- ノード {branch['node_id']}、下位ノード {branch['nodes']}：`{branch['inference_rule']}` / `{branch['statement']}`")
    out.extend(['','## 各問題行と根拠ノード',''])
    for row in data['flagged_lines']:
        out += [f"### 行 {row['line']} — {', '.join(row['tags'])}",'',row['text'],'',
                f"- 本文重複行：{row['duplicate_rendered_lines']}",
                f"- 直接一致：{row['assessment']}"]
        if not row['direct_step_candidates']:
            out.append('- 根拠が見つからないため、不要と断定しない')
        for candidate in row['direct_step_candidates']:
            out.append(f"- ノード {candidate['id']}：規則 `{candidate['inference_rule']}`、親 {candidate['parents']}、根への経路 {candidate['path_to_root']}、属する直接前提分岐 {candidate['root_branches']}、同式ノード {candidate['equivalent_statement_nodes']}")
        out.append('')
    out.extend(['## 判定','','証明木のノードは変更していない。上記は「本文に残す数学的必要性」を自動判定するものではない。'])
    (repo/'phase162_r10_r8_branch_evidence.md').write_text('\n'.join(out)+'\n',encoding='utf-8')


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,default=Path.cwd())
    args=parser.parse_args()
    p=args.repo/'phase162_r10_r5_prose_origin.json'
    if not p.is_file():
        raise FileNotFoundError(f'R10-R5 JSON required: {p}')
    data=json.loads(p.read_text(encoding='utf-8-sig'))
    result=analyze(data)
    write_report(result,args.repo)
    print('R10-R8 read-only branch evidence audit')
    print('Nodes:',result['counts']['nodes'],'Body lines:',result['counts']['body_lines'])
    print('Flagged:',result['counts']['by_tag'])
    print('Direct step:',result['counts']['flagged_with_direct_step'])
    print('Reports:',args.repo/'phase162_r10_r8_branch_evidence.md',args.repo/'phase162_r10_r8_branch_evidence.json')

if __name__=='__main__':
    main()
