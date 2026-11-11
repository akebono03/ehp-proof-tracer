"""R68: read-only typed premise audit of two public EHP inference transitions.

Checks *actual verified ProofStep* direct premises and the unchanged general
rules, not similarity of source labels. Does not certify all narrative sentences
or re-prove EHP exactness independently of the sourced proof tree.
"""
from __future__ import annotations

import argparse
from hashlib import sha1
import json
import os
from pathlib import Path
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r68_ehp_premise_semantics_audit"
PINS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_27_typed_statement_projection.py": "9ce32b5db34a3981649b9b9f2c5ff897eb8de831",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r56_cyclic_generator_bridge/rule.py": "e6bbeb8efa47a46f7326b8711b6de9e79ff60319",
    "phase174_r3_r7_r56_cyclic_generator_bridge/audit.py": "868e4dfad4d97bb3e5d5da462260bab3759d4af8",
    "phase174_r3_r7_r57_narrative_source_cleanup/audit.py": "7cc7e7ac7f63c4bf28142c1d84c5d8ddd249cc8a",
    "phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py": "54ae4d4430c99895e0687ea8c56fd711284465f1",
    "phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py": "a819eaebf33870443a8a0df9db2c8da78d1c4a5c",
    "phase174_r3_r7_r67_zero_map_tex_arrow_fix/install.py": "223db1c260cb568a031ede0064fcc361c6f15f82",
}


def git_blob_sha(raw: bytes) -> str:
    """Compute a Git blob identity on exact supplied bytes."""
    return sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Verify all reviewed source/test blobs; HEAD itself is not a gate."""
    checked: list[str] = []
    for name, sha in PINS.items():
        original = (root / name).read_bytes()
        lf = original.replace(b"\r\n", b"\n")
        if b"\r" in lf:
            raise RuntimeError("R68_MIXED_OR_CR_ONLY_EOL: " + name)
        variants = (original, lf, lf.replace(b"\n", b"\r\n"))
        if sha not in {git_blob_sha(data) for data in variants}:
            raise RuntimeError("R68_SOURCE_GUARD_FAILED: " + name)
        checked.append(name)
    return tuple(checked)


def local_head(root: Path) -> str:
    """Record the exact local source commit without rejecting benign descendants."""
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          text=True, capture_output=True, check=False)
    if proc.returncode:
        raise RuntimeError("R68_GIT_HEAD_UNAVAILABLE")
    return proc.stdout.strip()


def unique_inference_index(model, scope: frozenset[int], conclusion: object,
                           rule_name: str) -> int:
    """Select a unique *verified* inference by its typed goal and rule name."""
    if not rule_name or not isinstance(rule_name, str):
        raise ValueError("rule name is required")
    matches = tuple(i for i in sorted(scope)
                    if model.steps[i].conclusion == conclusion
                    and getattr(model.steps[i].rule, "name", None) == "INFERENCE"
                    and getattr(model.steps[i].inference_rule, "name", None) == rule_name)
    if len(matches) != 1:
        raise RuntimeError("R68_INFERENCE_NOT_UNIQUE: " + repr(matches))
    return matches[0]


def check_direct_premises(model, scope: frozenset[int], index: int,
                          required: tuple[object, ...],
                          required_roles: tuple[str, ...]) -> tuple[int, ...]:
    """Check the actual premises, identities, ordered types and certified scope.

    An equal-valued but detached premise must have one unique step witness;
    ambiguous or missing antecedents are rejected rather than silently linked.
    """
    if (type(index) is not int or index not in scope
            or index < 0 or index >= len(model.steps)):
        raise ValueError("R68_INVALID_VERIFIED_STEP_INDEX")
    if (not isinstance(required, tuple) or not isinstance(required_roles, tuple)
            or len(required) != len(required_roles)):
        raise ValueError("R68_INVALID_REQUIRED_PREMISE_CONTRACT")
    parent_step = model.steps[index]
    if getattr(parent_step.rule, "name", None) != "INFERENCE":
        raise RuntimeError("R68_TARGET_NOT_INFERENCE")
    actual = parent_step.premises
    if len(actual) != len(required):
        raise RuntimeError("R68_PREMISE_COUNT_CHANGED")
    witnesses = []
    for actual_parent, expected, role in zip(actual, required, required_roles):
        if (actual_parent.conclusion != expected
                or getattr(actual_parent.rule, "name", None) != role):
            raise RuntimeError("R68_PREMISE_GOAL_OR_ROLE_MISMATCH")
        matching_identity = tuple(i for i in sorted(scope)
                                  if model.steps[i] is actual_parent)
        matching_value = (matching_identity if matching_identity
                          else tuple(i for i in sorted(scope)
                                     if model.steps[i] == actual_parent))
        if len(matching_value) != 1:
            raise RuntimeError("R68_MISSING_OR_AMBIGUOUS_PREMISE")
        witnesses.append(matching_value[0])
    return tuple(witnesses)


def inspect_public() -> dict[str, object]:
    """Verify two existing complete roots and their previously sourced rules.

    The returned result is a *typed inference-premise* certificate, not a
    blanket review of 20 Japanese narrative paragraphs.
    """
    from homotopy_groups import (TodaHopfInvariantMap, TodaPrimaryGroup,
                                 TodaPrimaryGroupZeroStatement)
    from phase165_r14_r6_generic_iso import MapInjective
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import SURJECTIVE_RULE_NAME
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        RULE_NAME as ZERO_RULE_NAME, ehp_zero_inputs,
    )
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        RULE_NAME as HOPF_RULE_NAME, hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r67_zero_map_tex_arrow_fix.install import public_arrow_audit
    from proof import ProofRule

    public_arrow = public_arrow_audit()
    if (not public_arrow["proofs_complete"]
            or public_arrow["pi11_6_references"] != 7
            or public_arrow["pi12_7_references"] != 3):
        raise RuntimeError("R68_R67_PUBLIC_PROOF_REGRESSION")

    bridge = build_shared_typed_bridge()
    first, model1 = _search_with_model(6, 5, bridge)
    second, model2 = _search_with_model(7, 5, bridge)
    scope1 = root_ancestor_step_indices(model1.steps, model1.root_index)
    scope2 = root_ancestor_step_indices(model2.steps, model2.root_index)

    hopf_goal = MapInjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(11, 6), TodaPrimaryGroup(11, 11),
    ))
    hopf_premises = hopf_injectivity_from_zero_image_inputs(hopf_goal)
    if hopf_premises is None or len(hopf_premises) != 2:
        raise RuntimeError("R68_HOPF_TYPED_PREMISES_CHANGED")
    hopf_index = unique_inference_index(model1, scope1, hopf_goal, HOPF_RULE_NAME)
    hopf_indices = check_direct_premises(
        model1, scope1, hopf_index, hopf_premises, ("INFERENCE", "INFERENCE"),
    )
    if first.status.name != "COMPLETE":
        raise RuntimeError("R68_PI11_NOT_COMPLETE")
    if not any(i in scope1 and model1.steps[i].rule is ProofRule.GIVEN
               for i in range(len(model1.steps))):
        raise RuntimeError("R68_PI11_HAS_NO_SOURCED_GIVEN")
    sentence1 = render_model_backed_narrative_markdown(first, model1)
    if (r"$E:\pi_{10}^{5}\to \pi_{11}^{6}$ は零写像." not in sentence1
            or r"\\to" in sentence1):
        raise RuntimeError("R68_PI11_ZERO_IMAGE_PROSE_REGRESSION")

    zero_goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    zero_premises = ehp_zero_inputs(zero_goal)
    if zero_premises is None or len(zero_premises) != 4:
        raise RuntimeError("R68_ZERO_TYPED_PREMISES_CHANGED")
    zero_index = unique_inference_index(model2, scope2, zero_goal, ZERO_RULE_NAME)
    if zero_index != model2.root_index or second.status.name != "COMPLETE":
        raise RuntimeError("R68_PI12_ROOT_NOT_VERIFIED_ZERO_INFERENCE")
    zero_indices = check_direct_premises(
        model2, scope2, zero_index, zero_premises,
        ("INFERENCE", "INFERENCE", "INFERENCE", "INFERENCE"),
    )
    delta_index = unique_inference_index(
        model2, scope2, zero_premises[0], SURJECTIVE_RULE_NAME,
    )
    if delta_index != zero_indices[0]:
        raise RuntimeError("R68_ZERO_DELTA_SURJ_NOT_ACTUAL_PARENT")
    if len(model2.steps[delta_index].premises) != 1:
        raise RuntimeError("R68_DELTA_SURJ_PREMISE_COUNT_CHANGED")
    prior = model2.steps[delta_index].premises[0]
    if (prior.rule is not ProofRule.GIVEN
            or "ADOPTED_DATABASE_PRIOR" not in (prior.note or "")):
        raise RuntimeError("R68_DELTA_SURJ_DID_NOT_USE_ADMITTED_PRIOR")
    check_direct_premises(model2, scope2, delta_index,
                          (prior.conclusion,), ("GIVEN",))
    if any("Proposition 2.7" in (c.reference.locator or "")
           for c in model2.citations):
        raise RuntimeError("R68_UNNECESSARY_PROP27_REINTRODUCED")
    return {
        "pi11_6": {"complete": True, "reference_count": len(model1.citations),
                    "hopf_injectivity_rule": HOPF_RULE_NAME,
                    "hopf_step_index": hopf_index,
                    "direct_premise_indices": list(hopf_indices),
                    "zero_suspension_image_and_exactness": True,
                    "rendered_single_tex_arrow": True},
        "pi12_7": {"complete": True, "reference_count": len(model2.citations),
                    "zero_root_rule": ZERO_RULE_NAME,
                    "zero_root_step_index": zero_index,
                    "zero_root_premise_indices": list(zero_indices),
                    "delta_surjectivity_rule": SURJECTIVE_RULE_NAME,
                    "delta_surjectivity_step_index": delta_index,
                    "prior_db_step_rule": prior.rule.name,
                    "prior_db_single_premise": True,
                    "proposition_2_7_not_reused": True},
        "sentence_level_semantics_fully_audited": False,
        "mathematical_rules_added": 0,
        "new_given": 0,
        "production_changes": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    pins = source_guard(root)
    head = local_head(root)
    print("PHASE174_R68_SOURCE_GUARD=PASS")
    print("PHASE174_R68_SOURCE_PINS=" + str(len(pins)))
    print("PHASE174_R68_LOCAL_HEAD=" + head)
    print("PHASE174_R68_PRODUCTION_CHANGES=0")
    if args.dry_run:
        print("PHASE174_R68_GATE=PASS_R68_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    proof = inspect_public()
    target = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit" / PACKAGE / "report.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"phase": "174-R68", "local_head": head,
                                  "source_pins": list(pins),
                                  "proof": proof, "full_pytest": False},
                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R68_PI11_6_HOPF_INJECTIVE_TWO_PREMISES=PASS")
    print("PHASE174_R68_PI11_6_REFERENCE_COUNT=" + str(proof["pi11_6"]["reference_count"]))
    print("PHASE174_R68_PI12_7_ZERO_ROOT_FOUR_PREMISES=PASS")
    print("PHASE174_R68_PI12_7_DELTA_SURJ_PRIOR_ONLY=PASS")
    print("PHASE174_R68_PI12_7_REFERENCE_COUNT=" + str(proof["pi12_7"]["reference_count"]))
    print("PHASE174_R68_FULL_SENTENCE_SEMANTICS_AUDITED=False")
    print("PHASE174_R68_NEW_GIVEN=0")
    print("PHASE174_R68_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R68_REPORT=" + str(target))
    print("PHASE174_R68_GATE=PASS_R68_VERIFIED_EHP_PREMISE_AUDIT_ONLY")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
