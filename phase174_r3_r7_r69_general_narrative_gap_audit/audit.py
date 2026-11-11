"""R69: read-only audit of general EHP narrative proof-step boundaries.

It never modifies the proof tree, reference registry, renderer, source facts, or
math rules. A proposed prose rewrite is NOT a verified ProofStep.
"""
from __future__ import annotations

import argparse
from hashlib import sha1
import json
import os
from pathlib import Path
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r69_general_narrative_gap_audit"
PINS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_27_typed_statement_projection.py": "9ce32b5db34a3981649b9b9f2c5ff897eb8de831",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r56_cyclic_generator_bridge/rule.py": "e6bbeb8efa47a46f7326b8711b6de9e79ff60319",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase174_r3_r7_r68_ehp_premise_semantics_audit/audit.py": "ab3506e1d7163546d1966b0187b0b583aa72d22f",
}


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Guard the reviewed source, preserving whole-file LF or CRLF."""
    checked = []
    for relative, expected in PINS.items():
        raw = (root / relative).read_bytes()
        normalized = raw.replace(b"\r\n", b"\n")
        if b"\r" in normalized:
            raise RuntimeError("R69_MIXED_OR_CR_ONLY_EOL: " + relative)
        candidates = (raw, normalized, normalized.replace(b"\n", b"\r\n"))
        if expected not in {git_blob_sha(item) for item in candidates}:
            raise RuntimeError("R69_REVIEWED_SOURCE_MISMATCH: " + relative)
        checked.append(relative)
    return tuple(checked)


def local_head(root: Path) -> str:
    p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                       text=True, capture_output=True, check=False)
    if p.returncode != 0:
        raise RuntimeError("R69_GIT_HEAD_UNAVAILABLE")
    return p.stdout.strip()


def decide_presentation_boundary(*, root_verified: bool,
                                  explicit_zero_e: bool,
                                  explicit_h_injective: bool) -> str:
    """Separate an already-verified root from independently proved substeps."""
    if not all(type(value) is bool for value in
               (root_verified, explicit_zero_e, explicit_h_injective)):
        raise TypeError("boolean proof-state flags required")
    if not root_verified:
        return "ROOT_NOT_VERIFIED"
    if explicit_zero_e and explicit_h_injective:
        return "EXPLICIT_INTERMEDIATE_PROOFSTEPS_PRESENT"
    return "FOUR_PREMISE_ROOT_VERIFIED_INTERMEDIATE_STEPS_NOT_ALL_EXPLICIT"


def decide_composite_display(*, generator_zero_step: bool,
                             r2_cited_given_ancestor: bool,
                             component_images_verified: bool) -> str:
    """A complete display chain needs distinct evidence, never text resemblance."""
    if not all(type(value) is bool for value in
               (generator_zero_step, r2_cited_given_ancestor,
                component_images_verified)):
        raise TypeError("boolean witness flags required")
    if all((generator_zero_step, r2_cited_given_ancestor,
            component_images_verified)):
        return "CANDIDATE_CHAIN_NEEDS_GENERIC_RENDERING_REVIEW"
    return "INCOMPLETE_WITNESS_FOR_PROPOSED_CONDENSED_SENTENCE"


def step_index(model, target) -> int:
    """Locate exactly one actual ProofStep identity, else fail closed."""
    by_identity = tuple(i for i, item in enumerate(model.steps) if item is target)
    if len(by_identity) == 1:
        return by_identity[0]
    if by_identity:
        raise RuntimeError("R69_DUPLICATE_PREMISE_IDENTITIES")
    by_value = tuple(i for i, item in enumerate(model.steps) if item == target)
    if len(by_value) != 1:
        raise RuntimeError("R69_MISSING_OR_AMBIGUOUS_PREMISE")
    return by_value[0]


def inspect_public() -> dict[str, object]:
    """Audit two existing COMPLETE public searches without adding any fact."""
    from expression import Zero
    from homotopy_groups import (
        TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup,
        TodaPrimaryGroupZeroStatement, TodaSuspensionMap,
    )
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective, MapSurjective
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME as ZERO_RULE, ehp_zero_inputs
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import SURJECTIVE_RULE_NAME
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase174_r3_r7_r68_ehp_premise_semantics_audit.audit import (
        inspect_public as inspect_r68, unique_inference_index,
        check_direct_premises,
    )
    from phase174_r3_r7_r63_sentence_witness_audit.audit import (
        verified_ancestor_indices,
    )
    from proof import ProofRule

    old = inspect_r68()
    if (old["pi11_6"]["reference_count"] != 7
            or old["pi12_7"]["reference_count"] != 3):
        raise RuntimeError("R69_PREVIOUS_PROOF_CONTRACT_CHANGED")
    bridge = build_shared_typed_bridge()
    result1, model1 = _search_with_model(6, 5, bridge)
    result2, model2 = _search_with_model(7, 5, bridge)
    scope1 = root_ancestor_step_indices(model1.steps, model1.root_index)
    scope2 = root_ancestor_step_indices(model2.steps, model2.root_index)
    md1 = render_model_backed_narrative_markdown(result1, model1)
    md2 = render_model_backed_narrative_markdown(result2, model2)
    if r"\\to" in md1 or r"\\to" in md2:
        raise RuntimeError("R69_OLD_TEX_ARROW_REAPPEARED")

    zero_map1 = ImageZeroStatement(TodaSuspensionMap(
        TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6),
    ))
    map1 = zero_map1.map
    zero_index = tuple(i for i in sorted(scope1)
                       if model1.steps[i].conclusion == zero_map1
                       and model1.steps[i].rule is ProofRule.INFERENCE)
    if len(zero_index) != 1:
        raise RuntimeError("R69_PI11_VERIFIED_ZERO_IMAGE_MISSING_OR_AMBIGUOUS")
    image_indices = tuple(i for i in sorted(scope1)
                          if model1.steps[i].rule is ProofRule.INFERENCE
                          and isinstance(model1.steps[i].conclusion, GeneratorImage)
                          and model1.steps[i].conclusion.map == map1
                          and isinstance(model1.steps[i].conclusion.target_generator, Zero))
    component_images = tuple(i for i in sorted(scope1)
                             if isinstance(model1.steps[i].conclusion, GeneratorImage)
                             and model1.steps[i].conclusion.map == map1
                             and not isinstance(model1.steps[i].conclusion.target_generator, Zero))
    r2_sources = []
    for idx in image_indices:
        ancestors = verified_ancestor_indices(model1, idx)
        refs = tuple(sorted(i for i in ancestors
                            if model1.steps[i].rule is ProofRule.GIVEN
                            and 2 in model1.step_citation_numbers[i]))
        r2_sources.append({"zero_image_generator_step": idx,
                           "r2_given_ancestor_steps": list(refs)})
    has_r2 = any(entry["r2_given_ancestor_steps"] for entry in r2_sources)
    image_zero_step = bool(image_indices)
    # An η/ν decomposition requires the existing typed component image steps;
    # merely seeing the strings nu and eta is not an acceptable witness.
    has_components = len(component_images) >= 2
    pi11 = {
        "reference_count": 7,
        "certified_zero_map_step": zero_index[0],
        "zero_generator_image_steps": list(image_indices),
        "nonzero_component_image_steps": list(component_images),
        "zero_generator_r2_ancestry": r2_sources,
        "composite_display_state": decide_composite_display(
            generator_zero_step=image_zero_step,
            r2_cited_given_ancestor=has_r2,
            component_images_verified=has_components,
        ),
        "rewriting_applied": False,
    }

    goal2 = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    required = ehp_zero_inputs(goal2)
    if required is None or len(required) != 4:
        raise RuntimeError("R69_PI12_ZERO_RULE_PREMISES_CHANGED")
    root = unique_inference_index(model2, scope2, goal2, ZERO_RULE)
    if root != model2.root_index:
        raise RuntimeError("R69_PI12_ROOT_CHANGED")
    root_parents = check_direct_premises(
        model2, scope2, root, required, ("INFERENCE",) * 4,
    )
    delta = required[0]
    delta_index = unique_inference_index(model2, scope2, delta, SURJECTIVE_RULE_NAME)
    if delta_index != root_parents[0]:
        raise RuntimeError("R69_DELTA_IS_NOT_ZERO_ROOT_PREMISE")
    parent = model2.steps[delta_index].premises
    if len(parent) != 1 or parent[0].rule is not ProofRule.GIVEN:
        raise RuntimeError("R69_DELTA_PRIOR_DIRECT_SOURCE_CHANGED")
    parent_index = step_index(model2, parent[0])
    if (model2.step_citation_numbers[parent_index] != (1,)
            or "ADOPTED_DATABASE_PRIOR" not in (parent[0].note or "")):
        raise RuntimeError("R69_DELTA_PRIOR_SOURCE_NOT_R1")

    e_map = TodaSuspensionMap(TodaPrimaryGroup(11, 6), TodaPrimaryGroup(12, 7))
    h_map = TodaHopfInvariantMap(TodaPrimaryGroup(12, 7), TodaPrimaryGroup(12, 13))
    e_steps = tuple(i for i in sorted(scope2)
                    if model2.steps[i].rule is ProofRule.INFERENCE
                    and model2.steps[i].conclusion == ImageZeroStatement(e_map))
    h_steps = tuple(i for i in sorted(scope2)
                    if model2.steps[i].rule is ProofRule.INFERENCE
                    and model2.steps[i].conclusion == MapInjective(h_map))
    pi12 = {
        "reference_count": 3,
        "zero_root_step_index": root,
        "zero_root_four_premises": list(root_parents),
        "delta_surj_step_index": delta_index,
        "delta_surj_prior_given_index": parent_index,
        "delta_surj_only_one_given_premise": True,
        "derived_zero_suspension_step_indices": list(e_steps),
        "derived_hopf_injective_step_indices": list(h_steps),
        "hopf_display_state": decide_presentation_boundary(
            root_verified=True, explicit_zero_e=bool(e_steps),
            explicit_h_injective=bool(h_steps),
        ),
        "rewriting_applied": False,
    }
    return {
        "pi11_6": pi11,
        "pi12_7": pi12,
        "explicit_hopf_argument_mathematically_inside_existing_four_premise_rule": True,
        "full_sentence_semantics_audited": False,
        "recommendation": (
            "Keep general math rules intact. Reuse verified typed steps for "
            "composite E-image projection; present one-premise Delta surjectivity "
            "with a connective; distinguish an explanation of the verified "
            "four-premise zero rule from a new independently verified Hopf step."
        ),
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": 0,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    checked = source_guard(root)
    head = local_head(root)
    print("PHASE174_R69_SOURCE_GUARD=PASS")
    print("PHASE174_R69_SOURCE_PINS=" + str(len(checked)))
    print("PHASE174_R69_LOCAL_HEAD=" + head)
    print("PHASE174_R69_PRODUCTION_CHANGES=0")
    if opts.dry_run:
        print("PHASE174_R69_GATE=PASS_R69_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    report = inspect_public()
    directory = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
                 / "EHPProofTracerAudit" / PACKAGE)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "report.json"
    path.write_text(json.dumps({"phase": "174-R69", "head": head,
                                "source_pins": list(checked), "audit": report},
                               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pi11 = report["pi11_6"]
    pi12 = report["pi12_7"]
    print("PHASE174_R69_PI11_ZERO_GENERATOR_IMAGE_STEPS=" + str(len(pi11["zero_generator_image_steps"])))
    print("PHASE174_R69_PI11_COMPONENT_IMAGE_STEPS=" + str(len(pi11["nonzero_component_image_steps"])))
    print("PHASE174_R69_PI11_COMPOSITE_DISPLAY_STATE=" + pi11["composite_display_state"])
    print("PHASE174_R69_PI12_DELTA_SURJ_ONLY_R1_GIVEN=PASS")
    print("PHASE174_R69_PI12_ZERO_ROOT_FOUR_PREMISES=PASS")
    print("PHASE174_R69_PI12_EXPLICIT_ZERO_E_STEPS=" + str(len(pi12["derived_zero_suspension_step_indices"])))
    print("PHASE174_R69_PI12_EXPLICIT_H_INJECTIVE_STEPS=" + str(len(pi12["derived_hopf_injective_step_indices"])))
    print("PHASE174_R69_PI12_HOPF_DISPLAY_STATE=" + pi12["hopf_display_state"])
    print("PHASE174_R69_FULL_SENTENCE_SEMANTICS_AUDITED=False")
    print("PHASE174_R69_PRODUCTION_CHANGES=0")
    print("PHASE174_R69_REPORT=" + str(path))
    print("PHASE174_R69_GATE=PASS_R69_GENERAL_NARRATIVE_PROOFSTEP_BOUNDARY_AUDIT_ONLY")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
