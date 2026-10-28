"""R10ET-R3B: reviewed HEADs, R3 shadow cyclic projection comparison.

Application, tests, documents and Git index are never modified. Existing
provider and citation checker are restored even when an exception is raised.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True

REVIEWED_HEADS = (
    "a5892721436effaf7be759ff17afd3bd427814ed",
    "085b58cfa1bdf0e0e3d164fbff0c4e95deb07367",
    "c63ca5d07904e7725cbfabc9db2d714845d9a8c7",
)
EXPECTED_SHARED_BLOB = "61cbadb06f770c51a9c1f5a3c8026acf9e3e14aa"
PROJECTION_CASES = ((22, 6), (22, 10), (15, 8), (24, 9))
CORE_CASES = ((43, 26), (30, 26), (30, 11), (30, 14), (30, 16), (30, 9))


def git_output(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout.strip()


def git_tracked_status(root: Path) -> tuple[str, str]:
    return (git_output(root, "diff", "--name-status"),
            git_output(root, "diff", "--cached", "--name-status"))


def inspect_group(bridge: object, n: int, k: int, directory: Path) -> dict:
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase169_r10a_verified_stable_chain_projection.projection import (
        project_verified_stable_image_chain,
    )
    from phase169_r10ec_direct_sum_narrative_projection.projection import (
        project_verified_direct_sum_transport,
    )
    from phase169_r10et_r1_definition_reference_dependency_audit.audit import (
        canonical_definition_inference,
    )
    from phase169_r10et_r3_cyclic_definition_projection_audit.policy import (
        _given_ancestor_numbers, _indices,
    )
    import phase169_r10en_shared_citation_provenance.core as provenance
    from proof import ProofRule

    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or len(contexts) != 1):
        return {"group": f"pi_{n+k}^{n}", "status": result.status.value,
                "trust": "NOT_COMPLETE", "open_goals": list(map(repr, result.open_goals))}
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(item.step_index for item in project_narrative_order(model))
    before = (tuple(map(id, model.steps)), model.step_citation_numbers)
    original_citations = provenance.verified_generator_image_citation_numbers

    cyclic_original = project_verified_stable_image_chain(model, order)
    direct_sum_original = project_verified_direct_sum_transport(model, order)
    from phase169_r10et_r3_cyclic_definition_projection_audit.policy import (
        proposed_cyclic_image_citations,
    )
    observed = {"candidate_calls": 0, "candidate_rejections": 0}

    def candidate(model_arg, order_arg, image_steps, *, require_each):
        if require_each:
            return original_citations(model_arg, order_arg, image_steps, require_each=True)
        observed["candidate_calls"] += 1
        found = proposed_cyclic_image_citations(
            model_arg, order_arg, image_steps,
            legacy_checker=original_citations,
            canonical_definition_checker=canonical_definition_inference,
            given_rule=ProofRule.GIVEN, inference_rule=ProofRule.INFERENCE,
        )
        if found is None:
            observed["candidate_rejections"] += 1
        return found

    try:
        provenance.verified_generator_image_citation_numbers = candidate
        cyclic_candidate = project_verified_stable_image_chain(model, order)
        direct_sum_candidate = project_verified_direct_sum_transport(model, order)
        markdown = render_model_backed_narrative_markdown(result, model)
    finally:
        provenance.verified_generator_image_citation_numbers = original_citations
    after = (tuple(map(id, model.steps)), model.step_citation_numbers)
    if before != after:
        raise RuntimeError("shadow projection modified ProofSteps or citations")
    if not markdown.rstrip().endswith("□"):
        raise RuntimeError("shadow proof narrative lost completion marker")
    directory.mkdir(parents=True, exist_ok=False)
    (directory / "candidate_narrative.md").write_text(markdown, encoding="utf-8")
    root = model.steps[model.root_index]
    by_id = _indices(model, order)
    prior_citations = _given_ancestor_numbers(
        model, order, by_id, root.premises[0], ProofRule.GIVEN,
    ) if by_id is not None and len(root.premises) >= 2 else None
    iso_citations = _given_ancestor_numbers(
        model, order, by_id, root.premises[1], ProofRule.GIVEN,
    ) if by_id is not None and len(root.premises) >= 2 else None
    refs = {cite.number: cite.reference.locator or cite.reference.label
            for cite in model.citations}
    canonical = sum(canonical_definition_inference(step) for step in model.steps)
    orphan_prefix = bool(re.search(r"(?m)^より, \$E\^", markdown))
    no_individual = all(
        "family definition" not in locator and "The elements" not in locator
        and "Definition of indexed elements" not in locator and "Chapter V, i)" != locator
        for locator in refs.values()
    )
    return {
        "group": f"pi_{n+k}^{n}", "n": n, "k": k,
        "status": "complete", "trust": "PASS", "inferences": inferred, "givens": given,
        "canonical_definition_images": canonical,
        "references": refs,
        "source_citation_numbers": sorted(prior_citations or ()),
        "iso_citation_numbers": sorted(iso_citations or ()),
        "baseline_cyclic": cyclic_original is not None,
        "candidate_cyclic": cyclic_candidate is not None,
        "baseline_direct_sum": direct_sum_original is not None,
        "candidate_direct_sum": direct_sum_candidate is not None,
        "candidate_cyclic_citations": None if cyclic_candidate is None else list(cyclic_candidate.citation_numbers),
        "candidate_cyclic_hidden": None if cyclic_candidate is None else len(cyclic_candidate.hidden_indices),
        "candidate_direct_sum_citations": None if direct_sum_candidate is None else list(direct_sum_candidate.citation_numbers),
        "candidate_calls": observed["candidate_calls"],
        "candidate_rejections": observed["candidate_rejections"],
        "has_orphan_cyclic_reference_prefix": orphan_prefix,
        "no_individual_definition_reference": no_individual,
        "markdown_length": len(markdown),
        "narrative_path": str(directory / "candidate_narrative.md"),
        "proof_steps_and_citations_unchanged": before == after,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cases", choices=("focus", "all"), default="all")
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    if git_output(root, "branch", "--show-current") != "develop":
        raise SystemExit("R10ET-R3B REFUSED: branch is not develop")
    head = git_output(root, "rev-parse", "HEAD")
    if head not in REVIEWED_HEADS:
        raise SystemExit(f"R10ET-R3B REFUSED: unreviewed HEAD {head}")
    blob = git_output(root, "hash-object", "phase165_r52_r9_shared_math.py")
    if blob != EXPECTED_SHARED_BLOB:
        raise SystemExit("R10ET-R3B REFUSED: provider source differs")
    original_status = git_tracked_status(root)
    if any(original_status):
        raise SystemExit("R10ET-R3B REFUSED: tracked changes present")
    sys.path.insert(0, str(root))
    import phase165_r52_r9_shared_math as shared
    from phase169_r10et_r2_shadow_common_definition_comparison.audit import (
        shadow_provider_factory,
    )
    original_factory = shared.shared_expansion_provider
    rows: list[dict] = []
    output.mkdir(parents=True, exist_ok=False)
    scenario = PROJECTION_CASES + CORE_CASES if args.cases == "all" else PROJECTION_CASES
    try:
        bridge = shared.build_shared_typed_bridge()
        shared.shared_expansion_provider = shadow_provider_factory(original_factory)
        for n, k in scenario:
            name = f"pi_{n+k}^{n}"
            print(f"R10ET_R3B_START={name}", flush=True)
            try:
                row = inspect_group(bridge, n, k, output / f"pi{n+k}_{n}")
            except Exception as exc:
                row = {"group": name, "status": "ERROR", "trust": "ERROR",
                       "error": f"{type(exc).__name__}: {exc}",
                       "traceback": traceback.format_exc()}
            rows.append(row)
            for field in ("status", "trust", "baseline_cyclic", "candidate_cyclic",
                          "baseline_direct_sum", "candidate_direct_sum",
                          "has_orphan_cyclic_reference_prefix"):
                if field in row:
                    print(f"R10ET_R3B_{name}_{field.upper()}={row[field]}", flush=True)
    finally:
        shared.shared_expansion_provider = original_factory
    tracked_unchanged = git_tracked_status(root) == original_status
    provider_restored = shared.shared_expansion_provider is original_factory
    all_trusted = all(row.get("status") == "complete" and row.get("trust") == "PASS"
                      for row in rows)
    focus_cyclic_recovered = all(
        row.get("candidate_cyclic") is True for row in rows
        if (row.get("n"), row.get("k")) in ((22, 6), (22, 10))
    )
    no_direct_sum_regression = all(
        not row.get("baseline_direct_sum") or row.get("candidate_direct_sum")
        for row in rows
    )
    report = {
        "phase": "169 R10ET-R3B", "mode": "AUDIT_ONLY_IN_MEMORY_PROJECTION",
        "head": head, "provider_source_blob": blob, "cases": rows,
        "all_complete_trusted": all_trusted,
        "focus_cyclic_recovered": focus_cyclic_recovered,
        "no_direct_sum_regression": no_direct_sum_regression,
        "tracked_unchanged": tracked_unchanged,
        "provider_restored": provider_restored,
        "full_pytest_run": False, "application_changed": [],
        "requires_renderer_prefix_review": any(
            row.get("has_orphan_cyclic_reference_prefix") for row in rows
        ),
    }
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = ["# Phase 169 R10ET-R3B — 巡回群表示の共通 Definition 監査", "",
             "**AUDIT_ONLY。製品コード・既存テスト・文書は変更していない。**", "",
             f"- HEAD: `{head}`", f"- 完成・Trust 全件: `{all_trusted}`",
             f"- 巡回群の候補 Projection 復旧: `{focus_cyclic_recovered}`",
             f"- 直和群の既存 Projection 維持: `{no_direct_sum_regression}`",
             f"- 本文の引用なし『より』: `{report['requires_renderer_prefix_review']}`",
             f"- tracked 不変: `{tracked_unchanged}`", "", "| 対象 | cyclic 現行→候補 | 直和 現行→候補 | 引用 | 結果 |",
             "|---|---|---|---|---|"]
    for row in rows:
        lines.append(
            f"| `{row['group']}` | {row.get('baseline_cyclic')} → {row.get('candidate_cyclic')} | "
            f"{row.get('baseline_direct_sum')} → {row.get('candidate_direct_sum')} | "
            f"{row.get('references')} | {row.get('trust')} |"
        )
    lines += ["", "## 次段階", "", "候補が成立しても実装は未実施。巡回群の引用なし前置詞と、",
              "既存の引用付き経路を保護するテストを先に準備する。", "",
              "Reference の削除だけで Proof Tree を変更しない。", ""]
    (output / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"R10ET_R3B_REPORT={output / 'audit.md'}", flush=True)
    print(f"R10ET_R3B_CYCLIC_RECOVERED={focus_cyclic_recovered}", flush=True)
    print(f"R10ET_R3B_DIRECT_SUM_PRESERVED={no_direct_sum_regression}", flush=True)
    print(f"R10ET_R3B_ORPHAN_PREFIX={report['requires_renderer_prefix_review']}", flush=True)
    print(f"R10ET_R3B_TRACKED_UNCHANGED={tracked_unchanged}", flush=True)
    print(f"R10ET_R3B_PROVIDER_RESTORED={provider_restored}", flush=True)
    return 0 if tracked_unchanged and provider_restored and all_trusted else 1


if __name__ == "__main__":
    raise SystemExit(main())
