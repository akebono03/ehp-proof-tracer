from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

BASELINE = "11ea331f322883e2f2cf34b9e865dea2134f5058"
EXPECTED = "10f77860a5631d363d606e76b8c1f12ee6c500d5"
ALLOWED_CHANGES = {
    "phase173_r1_nge3_audit/AUDIT_PLAN_JA.md",
    "phase173_r1_nge3_audit/CODE_FULL_JA.md",
    "phase173_r1_nge3_audit/README.md",
    "phase173_r1_nge3_audit/__init__.py",
    "phase173_r1_nge3_audit/audit.py",
    "phase173_r1_nge3_audit/run.ps1",
    "phase173_r1_nge3_audit/tests/test_audit.py",
}
REVIEWED_BLOBS = {
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
ROOT = Path.cwd()

def git(*arguments: str) -> str:
    p = subprocess.run(["git", *arguments], cwd=ROOT, capture_output=True,
                       text=True, encoding="utf-8", check=True)
    return p.stdout.strip()

if git("branch", "--show-current") != "develop":
    raise RuntimeError("Branch must be develop")
if git("rev-parse", "HEAD") != EXPECTED:
    raise RuntimeError("Unknown HEAD; recheck current GitHub and local changes")
if git("merge-base", BASELINE, EXPECTED) != BASELINE:
    raise RuntimeError("Reviewed baseline is not an ancestor")
changes = set(git("diff", "--name-only", BASELINE, "HEAD").splitlines())
if changes != ALLOWED_CHANGES:
    raise RuntimeError("Unexpected changed paths: " + repr(sorted(changes)))
for filename, expected_sha in REVIEWED_BLOBS.items():
    actual_sha = git("rev-parse", "HEAD:" + filename)
    if actual_sha != expected_sha:
        raise RuntimeError("Reviewed source content changed: " + filename)
if git("status", "--porcelain", "--untracked-files=no"):
    raise RuntimeError("Tracked worktree has changes")
print("PHASE173_R3_HEAD_REVIEW=PASS")
print("PHASE173_R3_REVIEWED_SOURCE_BLOBS=PASS")

r1 = Path(os.environ["LOCALAPPDATA"]) / "EHPProofTracerRecovery" / "phase173_r1_20261031_225525_166058" / "audit.json"
report = json.loads(r1.read_text(encoding="utf-8-sig"))
observed = {(x.get("n"), x.get("k")): x for x in report["rows"]}
for target in ((4, 3), (5, 3)):
    if observed[target].get("audit_result") != "PROOF_UNFINISHED":
        raise RuntimeError("R1 baseline differs for " + str(target))

tex = (ROOT / "sources" / "toda" / "Toda_05_2.tex").read_text(encoding="utf-8-sig")
anchor = r"\begin{proposition}\label{prop:5.6}"
start = tex.index(anchor)
end = tex.index(r"\end{proposition}", start)
prop56 = tex[start:end]
for token in (r"\pi^{4}_{7}", r"\pi^{n}_{n+3}", r"\nu'"):
    if token not in prop56:
        raise RuntimeError("Prop 5.6 source is not as reviewed")

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from proof import ProofRule

bridge = build_shared_typed_bridge()
results = []
for n, k in ((4, 3), (5, 3)):
    row = {"n": n, "k": k, "stable_start_n": k + 2}
    goals = registered_group_goal_candidates(bridge, n=n, k=k)
    row["goal_candidates"] = len(goals)
    if len(goals) != 1:
        raise RuntimeError("Expected one typed goal for " + str((n, k)))
    goal = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    if citing is None:
        raise RuntimeError("Missing citing assertion for " + str((n, k)))
    assertion = bridge.registry.assertion(citing)
    row["source_assertion_id"] = citing
    row["source_locator"] = bridge.registry.reference(assertion.reference_id).locator
    row["component_position"] = assertion.component_position
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    given = tuple(x.step.conclusion for x in screened.proof_links
                  if x.step is not None and x.step.rule is ProofRule.GIVEN)
    row["screened_given_count"] = len(given)
    row["target_direct_given_count"] = sum(
        type(x) is type(goal) and x == goal for x in given
    )
    if row["target_direct_given_count"]:
        raise RuntimeError("Target was admitted as direct GIVEN")
    provider = shared_expansion_provider(screened, proof_target=goal)
    options = provider(goal)
    row["root_candidate_count"] = len(options)
    row["roots"] = []
    seen_children = []
    for option in options[:8]:
        children = []
        for child in option.subgoals[:8]:
            entry = {"type": type(child).__name__, "repr": repr(child)[:1600]}
            if len(seen_children) < 12 and not any(
                type(child) is type(old) and child == old for old in seen_children
            ):
                seen_children.append(child)
                try:
                    expansions = provider(child)
                    entry["child_proposal_count"] = len(expansions)
                    entry["child_proposal_rules"] = [x.rule.name for x in expansions[:12]]
                except Exception as exc:
                    entry["child_probe_error"] = "%s: %s" % (type(exc).__name__, exc)
                entry["exact_screened_given"] = any(
                    type(child) is type(x) and child == x for x in given
                )
            children.append(entry)
        row["roots"].append({"rule": option.rule.name, "children": children})
    row["prior_sources"] = []
    for source_n in range(3, n):
        prior = resolve_prior_group_result(
            screened, source_n=source_n, source_k=k,
            citing_assertion_id=citing,
        )
        row["prior_sources"].append({
            "n": source_n, "k": k, "eligible": prior.eligible,
            "reason": prior.reason,
            "stable_source": source_n >= k + 2,
        })
    results.append(row)
    print("R3 n=%d k=%d locator=%s GIVEN=%d roots=%d prior=%s" % (
        n, k, row["source_locator"], len(given), len(options),
        ",".join(p["reason"] for p in row["prior_sources"]) or "none"))

out = Path(os.environ["LOCALAPPDATA"]) / "EHPProofTracerRecovery" / "phase173_r3_manual"
out.mkdir(parents=True, exist_ok=True)
path = out / "audit.json"
path.write_text(json.dumps({
    "phase": "173 R3 manual", "mode": "AUDIT_ONLY",
    "head": EXPECTED, "source_prop56_present": True,
    "observations_are_not_proofs": True, "rows": results,
}, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print("PHASE173_R3_MANUAL_REPORT=" + str(path))
if git("status", "--porcelain", "--untracked-files=no"):
    raise RuntimeError("Tracked worktree changed during audit")
print("PHASE173_R3_TRACKED_UNCHANGED=True")
print("PHASE173_R3_MANUAL_AUDIT_ONLY=PASS")
