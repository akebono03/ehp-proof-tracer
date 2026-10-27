"""Read proof-backed Web narrative after R4E; never create proof evidence."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from web_group_proof import build_standard_web_group_proof_view

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def main() -> None:
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE
            or len(result.proven_steps) != 18 or result.open_goals
            or len(contexts) != 1):
        raise RuntimeError("R4E lost complete pi6_4 proof")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise RuntimeError("R4E lacks positioned pi6_4 citation target")
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    if "\n証明\n" not in markdown:
        raise RuntimeError("R4E cannot separate Reference from proof body")
    reference, body = markdown.split("\n証明\n", 1)
    reference_numbers = tuple(int(x) for x in re.findall(r"\*\*\[R(\d+)\]", reference))
    body_numbers = tuple(int(x) for x in re.findall(r"\[R(\d+)\]", body))
    citations = tuple(
        {"number": entry.number,
         "locator": entry.reference.locator or entry.reference.label,
         "assertion_ids": list(entry.assertion_ids),
         "body": list(entry.statement_bodies)}
        for entry in model.citations
    )
    if (len(citations) != 5
            or len(reference_numbers) != 5
            or set(reference_numbers) != set(body_numbers)
            or set(body_numbers) != {entry["number"] for entry in citations}):
        raise RuntimeError("R4E references are missing, repeated, or unbound in body")
    citation_by_locator = {entry["locator"]: entry for entry in citations}
    r2 = citation_by_locator["Proposition 4.4"]
    r3 = citation_by_locator["Proposition 4.2 (4.4)"]
    if (len(r2["body"]) != 1
            or r"H(\alpha)=\pm\iota_{2n-1}" not in r2["body"][0]
            or not re.search(rf"\[R{r2['number']}\]より, \$E:.*は単射", body)
            or not re.search(rf"\[R{r3['number']}\]より, \$\\pi_\{{5\}}\^\{{3\}}.*は完全", body)):
        raise RuntimeError("R4E Proposition 4.4 / 4.2 text or ancestry tag missing")
    if not body.rstrip().endswith("□"):
        raise RuntimeError("R4E lost completed proof terminator")
    web = build_standard_web_group_proof_view(4, 2, mode="narrative")
    if (web.key != "generic-complete-proof" or web.partial_result
            or len(web.steps) != 18):
        raise RuntimeError("R4E Web result no longer complete")
    web_text = ["".join(segment.value for segment in line.segments)
                for line in web.rendered_lines]
    if not any(f"[R{r2['number']}]より" in text for text in web_text):
        raise RuntimeError("R4E Web lost Proposition 4.4 citation")
    if not any(f"[R{r3['number']}]より" in text for text in web_text):
        raise RuntimeError("R4E Web lost Proposition 4.2 citation")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
        check=True, text=True,
    ).stdout.strip()
    report = {
        "phase": "169-R4E", "git_head": head,
        "proof_status": result.status.value, "proof_steps": len(result.proven_steps),
        "open_goals": len(result.open_goals), "proof_tree_verified": True,
        "web_key": web.key, "web_partial": web.partial_result,
        "web_steps": len(web.steps), "citations": citations,
        "reference_numbers": list(reference_numbers),
        "proof_body_numbers": list(body_numbers),
        "all_references_used": True,
        "prop44_reference_body_present": True,
        "prop44_body_tagged": True, "prop42_body_tagged": True,
        "full_pytest_run": False,
    }
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    (output / "web_narrative.md").write_text(markdown, encoding="utf-8")
    (output / "audit.md").write_text(
        "# Phase 169 R4E — π₆⁴ Reference と本文の引用対応\n\n"
        f"- Git HEAD: `{head}`\n"
        "- 検証済み Proof Tree: 完成（18ステップ、未解決0件）\n"
        "- Reference: 5件（すべて証明本文に対応）\n"
        "- Proposition 4.4: 命題本文と[R2]の本文引用を確認\n"
        "- Proposition 4.2 (4.4): 完全列と[R3]の本文引用を確認\n"
        "- Web: `generic-complete-proof`\n"
        "- 全体 pytest: 未実施\n",
        encoding="utf-8",
    )
    print("R4E_GIT_HEAD=" + head)
    print("R4E_PI64_STATUS=" + result.status.value)
    print("R4E_PI64_STEPS=" + str(len(result.proven_steps)))
    print("R4E_PI64_OPEN_GOALS=" + str(len(result.open_goals)))
    print("R4E_WEB_KEY=" + web.key)
    print("R4E_REFERENCES=" + str(len(citations)))
    print("R4E_ALL_REFERENCES_TAGGED=True")
    print("R4E_PROP44_REFERENCE_BODY=True")
    print("R4E_FULL_PYTEST_RUN=False")
    print("R4E_REPORT=" + str(output / "audit.md"))
    print("R4E_WEB_NARRATIVE=" + str(output / "web_narrative.md"))


if __name__ == "__main__":
    main()
