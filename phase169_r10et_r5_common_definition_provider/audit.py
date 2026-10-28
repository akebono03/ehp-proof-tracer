"""R10ET-R5 real production-provider proof, trust, provenance and display audit."""
from __future__ import annotations

import json
import re
from pathlib import Path

CORE_CASES = ((43, 26), (30, 26), (30, 11), (30, 14), (30, 16), (30, 9))
LOW_CASES = ((2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2))
PROJECTION_CASES = ((22, 6), (22, 10), (15, 8), (24, 9))
CASES = CORE_CASES + LOW_CASES + PROJECTION_CASES
CYCLIC = ((22, 6), (22, 10))
DIRECT_SUM = ((43, 26), (30, 26), (30, 14), (30, 16), (30, 9),
              (15, 8), (24, 9))
BASELINE = (
    "phase169_r10et_r2_shadow_common_definition_comparison/output/"
    "20261028_151843_654/audit.json"
)


def audit(root: Path, output: Path, *, cases: str = "all") -> dict:
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r14_r6_generic_iso import GeneratorImage
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
    from phase169_r10et_r4_cyclic_definition_projection.policy import (
        canonical_definition_image,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import (
        is_defined_stable_image,
    )
    from proof import ProofRule

    baseline_path = root / BASELINE
    if not baseline_path.is_file():
        raise RuntimeError("reviewed R10ET-R2 shadow baseline not available")
    baseline_data = json.loads(baseline_path.read_text(encoding="utf-8"))
    if (baseline_data.get("mode") != "AUDIT_ONLY_SHADOW"
            or not baseline_data.get("all_complete_trusted")):
        raise RuntimeError("R10ET-R2 baseline is not verified")
    baseline = {row["group"]: row for row in baseline_data["cases"]}
    selected = CASES if cases == "all" else CORE_CASES + PROJECTION_CASES
    bridge = build_shared_typed_bridge()
    rows = []
    narratives = output / "narratives"
    narratives.mkdir(parents=True, exist_ok=True)
    for n, k in selected:
        label = f"pi_{n+k}^{n}"
        print(f"R10ET_R5_START={label}", flush=True)
        contexts = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        if (result.status is not ProofSearchStatus.COMPLETE
                or result.open_goals or len(contexts) != 1):
            raise RuntimeError(f"{label} is not a completed, context-bound proof")
        citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        inferred, given = verify_proof_tree_for_narrative(
            result, contexts[0], citing_assertion_id=citing_id,
            derived_target_without_citing_id=citing_id is None,
        )
        model = build_linked_proof_narrative_model(result, contexts[0])
        order = tuple(row.step_index for row in project_narrative_order(model))
        before = (tuple(map(id, model.steps)), model.step_citation_numbers)
        display_cyclic = project_verified_stable_image_chain(model, order)
        display_direct = project_verified_direct_sum_transport(model, order)
        narrative = render_model_backed_narrative_markdown(result, model)
        if (before != (tuple(map(id, model.steps)), model.step_citation_numbers)
                or not narrative.rstrip().endswith("□")
                or re.search(r"(?m)^より,\s*\$E\^", narrative)):
            raise RuntimeError(f"{label} renderer corruption or orphan prefix")
        locators = [item.reference.locator or item.reference.label
                    for item in model.citations]
        canonical = sum(
            bool(canonical_definition_image(step)) for step in model.steps
            if isinstance(step.conclusion, GeneratorImage)
        )
        remaining = sum(
            bool(is_defined_stable_image(step.conclusion))
            and not bool(canonical_definition_image(step))
            for step in model.steps
            if isinstance(step.conclusion, GeneratorImage)
        )
        original = baseline.get(label)
        if original is None:
            raise RuntimeError(f"{label} absent in reviewed R2 shadow output")
        expected_locators = [item["locator"] for item in original["references"]]
        if (canonical != original["image_actual_common"]
                or remaining != 0
                or locators != expected_locators):
            raise RuntimeError(f"{label} differs from trusted R2 shadow Proof Tree: "
                               f"{canonical=} {remaining=} {locators=}, "
                               f"expected {original['image_actual_common']} and {expected_locators}")
        if (n, k) in CORE_CASES + PROJECTION_CASES:
            if (len(locators) != 2 or not locators[0].startswith("DB prior:")
                    or locators[1] != "(4.5)"):
                raise RuntimeError(f"{label} lost DB prior or Toda (4.5)")
            root = model.steps[model.root_index]
            if root.rule is not ProofRule.INFERENCE or len(root.premises) < 3:
                raise RuntimeError(f"{label} invalid root evidence structure")
            by_id = {id(step): idx for idx, step in enumerate(model.steps)}
            def ancestors(step):
                pending = [step]
                visited = set()
                seen = set()
                while pending:
                    current = pending.pop()
                    key = id(current)
                    if key in visited:
                        continue
                    visited.add(key)
                    idx = by_id.get(key)
                    if idx is None:
                        raise RuntimeError(f"{label} external premise")
                    if current.rule is ProofRule.GIVEN:
                        seen.update(model.step_citation_numbers[idx])
                    pending.extend(current.premises)
                return seen
            first_support = ancestors(root.premises[0])
            second_support = ancestors(root.premises[1])
            if 1 not in first_support or 2 not in second_support:
                raise RuntimeError(f"{label} root source or isomorphism detached from citations")
        if (n, k) in CYCLIC:
            if (display_cyclic is None or display_cyclic.citation_numbers != ()
                    or f"Definition より, $E^{{{display_cyclic.exponent}}}" not in narrative):
                raise RuntimeError(f"{label} cyclic Definition compression not active")
        if (n, k) in DIRECT_SUM:
            if (display_direct is None or display_direct.statement not in narrative
                    or "Definition より, " not in display_direct.statement):
                raise RuntimeError(f"{label} direct sum Definition compression regressed")
        file = narratives / f"pi{n+k}_{n}.md"
        file.write_text(narrative, encoding="utf-8")
        row = {"n": n, "k": k, "group": label, "complete": True, "trust": "PASS",
               "inferences": inferred, "givens": given, "canonical_images": canonical,
               "eligible_noncanonical_images": remaining, "references": locators,
               "cyclic_projection": display_cyclic is not None,
               "direct_sum_projection": display_direct is not None,
               "narrative": str(file)}
        rows.append(row)
        print(f"R10ET_R5_{label}_TRUST=PASS", flush=True)
        print(f"R10ET_R5_{label}_COMMON_IMAGES={canonical}", flush=True)
        print(f"R10ET_R5_{label}_CITED_COMMON_ELIGIBLE={remaining}", flush=True)
        print(f"R10ET_R5_{label}_CYCLIC={display_cyclic is not None}", flush=True)
        print(f"R10ET_R5_{label}_DIRECT_SUM={display_direct is not None}", flush=True)
    report = {"phase": "169 R10ET-R5", "mode": "REAL_PROVIDER",
              "baseline": BASELINE, "full_suite_run": False, "cases": rows,
              "all_complete_trusted": len(rows) == len(selected)}
    (output / "audit.json").write_text(json.dumps(
        report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 169 R10ET-R5 本番探索の比較監査", "",
             "| 対象 | 完成/Trust | 共通Definition | 残存する置換可能推論 | 巡回圧縮 | 直和圧縮 |",
             "|---|---|---:|---:|---|---|"]
    for row in rows:
        lines.append("| `{group}` | complete / PASS | {canonical_images} | "
                     "{eligible_noncanonical_images} | {cyclic_projection} | "
                     "{direct_sum_projection} |".format(**row))
    lines.extend(("", "R2 の検証済み Shadow Proof Tree と群・引用・Definition 数を照合。",
                  "Reference の削除は表示フィルタではなく Proof Tree の依存変更の結果。",
                  "DB prior と Toda (4.5) の GIVEN 祖先は独立して検証。",
                  "全体 pytest は Phase 末まで実行しない。", ""))
    (output / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    return report
