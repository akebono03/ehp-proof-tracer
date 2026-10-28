"""Verify full/Trust, projection and visible Definition text after the R4 patch."""
from __future__ import annotations

import json
import re
from pathlib import Path

CASES = ((22, 6), (22, 10), (15, 8), (24, 9),
         (43, 26), (30, 26), (30, 11), (30, 14), (30, 16), (30, 9))


def audit(root: Path, output: Path, *, cases: str = "all") -> bool:
    from phase165_r52_partial_proof import ProofSearchStatus
    import phase165_r52_r9_shared_math as shared
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
    from phase169_r10et_r2_shadow_common_definition_comparison.audit import (
        shadow_provider_factory,
    )

    selected = CASES if cases == "all" else CASES[:4]
    bridge = shared.build_shared_typed_bridge()
    prior = shared.shared_expansion_provider
    rows = []
    report_dir = output / "audit"
    report_dir.mkdir()
    try:
        shared.shared_expansion_provider = shadow_provider_factory(prior)
        for n, k in selected:
            label = f"pi_{n+k}^{n}"
            print(f"R10ET_R4_START={label}", flush=True)
            contexts = []
            result = search_group_from_registered_goal(
                n=n, k=k, bridge=bridge, context_sink=contexts.append,
            )
            if (result.status is not ProofSearchStatus.COMPLETE
                    or result.open_goals or len(contexts) != 1):
                raise RuntimeError(f"{label} incomplete or missing proof context")
            citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
            inferred, given = verify_proof_tree_for_narrative(
                result, contexts[0], citing_assertion_id=citing,
                derived_target_without_citing_id=citing is None,
            )
            model = build_linked_proof_narrative_model(result, contexts[0])
            order = tuple(item.step_index for item in project_narrative_order(model))
            before = (tuple(map(id, model.steps)), model.step_citation_numbers)
            cyclic = project_verified_stable_image_chain(model, order)
            direct_sum = project_verified_direct_sum_transport(model, order)
            markdown = render_model_backed_narrative_markdown(result, model)
            if (before != (tuple(map(id, model.steps)), model.step_citation_numbers)
                    or not markdown.rstrip().endswith("□")
                    or re.search(r"(?m)^より, \$E\^", markdown)):
                raise RuntimeError(f"{label} renderer changed model or has orphan prefix")
            refs = [item.reference.locator or item.reference.label
                    for item in model.citations]
            if (n, k) in ((22, 6), (22, 10)):
                if (cyclic is None or cyclic.citation_numbers
                        or "Definition より, $E^" not in markdown):
                    raise RuntimeError(f"{label} common Definition cyclic projection failed")
            if (n, k) in ((15, 8), (24, 9), (43, 26), (30, 26),
                          (30, 14), (30, 16), (30, 9)):
                if direct_sum is None or direct_sum.statement not in markdown:
                    raise RuntimeError(f"{label} direct sum projection regressed")
            if "(4.5)" not in refs or not any("DB prior:" in ref for ref in refs):
                raise RuntimeError(f"{label} lost independent root source or (4.5)")
            if any("family definition" in ref for ref in refs):
                raise RuntimeError(f"{label} unexpected family Definition after shadow")
            path = report_dir / f"pi{n+k}_{n}.md"
            path.write_text(markdown, encoding="utf-8")
            row = {"n": n, "k": k, "group": label, "status": "complete",
                   "trust": "PASS", "inferences": inferred, "givens": given,
                   "cyclic": cyclic is not None,
                   "cyclic_citations": None if cyclic is None else list(cyclic.citation_numbers),
                   "direct_sum": direct_sum is not None,
                   "references": refs, "renderer_model_unchanged": True,
                   "orphan_prefix": False, "narrative": str(path)}
            rows.append(row)
            print(f"R10ET_R4_{label}_TRUST=PASS", flush=True)
            print(f"R10ET_R4_{label}_CYCLIC={row['cyclic']}", flush=True)
            print(f"R10ET_R4_{label}_DIRECT_SUM={row['direct_sum']}", flush=True)
    finally:
        shared.shared_expansion_provider = prior
    report = {"phase": "169 R10ET-R4", "mode": "FOCUSED_IMPLEMENTATION_AUDIT",
              "cases": rows, "provider_restored": shared.shared_expansion_provider is prior,
              "full_suite_ran": False}
    (report_dir / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    return len(rows) == len(selected) and shared.shared_expansion_provider is prior
