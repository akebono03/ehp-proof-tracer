"""Read-only audit of R2/R7 citation bodies and the upper-Delta proof chain.

No proof candidate, registered GIVEN, mathematical inference, or public source
is modified.  The audit reads the real production (n,k)=(7,5) search and the
same screened bridge that the web route uses.  A missing display remains a
reported defect rather than becoming a synthetic proof step.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
REPORT_FOLDER = "phase174_r3_r7_r55r2"
REVIEWED_BASE = "2dc8ac9faacc0630a18ecc5591c6951bf4e2f7a9"
REVIEWED_LATEST = "7224260731ca5e61fffc4ee047cf31b6cc5ce6c5"
# Git object SHAs of files reviewed on GitHub develop, not line-ending hashes.
PINNED_BLOBS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_4_link_bridge.py": "c3a6233a57c41e61e6649ee33c7a336d7aa1c664",
    "phase168_r3_5_model_renderer.py": "913a7030e209a689f58a5215013d3708140052e7",
    "phase168_r3_27_typed_statement_projection.py": "26ce3632fe1b32bab7e822e8f701409b26f4f04a",
    "phase168_r3_37c_reference_projection.py": "0a7800b3bd9d140fc22c1b92ab74bcdf48740546",
    "phase174_r3_r7_r12_toda59_annihilator_source/source.py": "10b03ec879cb6f5ad1ae01f3e8ffa1dd0af6c01f",
    "phase174_r3_r7_r13_cited_annihilator_bridge/registry.py": "489380d974d9e3a2869743325d21b15b4d64f808",
    "phase174_r3_r7_r28_prop27_typed_literature_registration/registration.py": "16d7caff9303f4f1da450175fe1fea00e7821c6c",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
}


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "git " + " ".join(args) + " failed: " + result.stderr.strip()
        )
    return result.stdout.strip()


def verify_checkout() -> dict[str, object]:
    """Fail closed on unknown ancestry, source blobs or edited target files."""
    if git("rev-parse", "--show-toplevel").replace("\\", "/").lower() != str(ROOT).replace("\\", "/").lower():
        raise RuntimeError("ZIP must be unpacked in the repository root")
    branch = git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("Expected local develop branch, got " + branch)
    head = git("rev-parse", "HEAD")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", REVIEWED_BASE, "HEAD"],
        cwd=ROOT, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("HEAD does not descend from the reviewed R55R1 base")
    checked = []
    for path, expected in PINNED_BLOBS.items():
        current = git("rev-parse", "HEAD:" + path)
        if current != expected:
            raise RuntimeError("Reviewed Git blob changed: " + path)
        changed = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", path],
            cwd=ROOT, check=False,
        )
        if changed.returncode != 0:
            raise RuntimeError("Local tracked target differs from HEAD: " + path)
        checked.append(path)
    return {
        "branch": branch,
        "local_head": head,
        "reviewed_base": REVIEWED_BASE,
        "reviewed_latest_at_audit_authoring": REVIEWED_LATEST,
        "pinned_blob_count": len(checked),
        "checked_files": checked,
        "source_guard": "PASS",
    }


def reference_snapshot(model: object, locator: str) -> dict[str, object]:
    """Identify a cited source by its exact printed locator, not a label guess."""
    candidates = [
        citation for citation in model.citations
        if (citation.reference.locator or citation.reference.label) == locator
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"Expected one cited {locator}, got {len(candidates)}")
    citation = candidates[0]
    return {
        "number": citation.number,
        "locator": locator,
        "assertion_ids": list(citation.assertion_ids),
        "reference_ids": list(citation.reference_ids),
        "step_indices": list(citation.step_indices),
        "statement_bodies": list(citation.statement_bodies),
        "reference_body_present": bool(citation.statement_bodies),
    }


def ancestor_contains(step: object, target_step: object) -> bool:
    """Membership in the real, identity-preserved Proof Tree."""
    visited: set[int] = set()
    pending = [step]
    while pending:
        current = pending.pop()
        if id(current) in visited:
            continue
        visited.add(id(current))
        if current is target_step:
            return True
        pending.extend(current.premises)
    return False


def lines_containing(text: str, terms: tuple[str, ...]) -> list[str]:
    """Expose relevant displayed prose without inventing unprinted formulas."""
    return [line for line in text.splitlines()
            if line.strip() and any(term in line for term in terms)]


def inspect_public_proof() -> dict[str, object]:
    """Run the real root search and inspect source, type, proof and prose separately."""
    from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import canonical_annihilator_instance
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
        Prop27GeneralTheoremPremise, Prop27TypedHopfDeltaStatement,
        typed_specialization,
    )
    from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
        Prop27UniversalLiteratureStatement,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        upper_delta_surjectivity_inputs,
    )
    from proof import ProofRule, Relation, RelationType

    bridge = build_shared_typed_bridge()
    contexts: list[object] = []
    proof = search_group_from_registered_goal(
        n=7, k=5, bridge=bridge, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("Public search did not retain a unique screened context")
    # Match the Web path: verify the real COMPLETE proof before citing anything.
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    verify_proof_tree_for_narrative(
        proof, contexts[0], citing_assertion_id=None,
        derived_target_without_citing_id=True,
    )
    model = build_linked_proof_narrative_model(proof, contexts[0])
    markdown = render_model_backed_narrative_markdown(proof, model)
    if proof.status is not ProofSearchStatus.COMPLETE or proof.open_goals:
        raise RuntimeError("Expected completed public Group proof")
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    scoped = [model.steps[i] for i in sorted(scope)]
    if len(scoped) != 28:
        raise RuntimeError("Public proof-ancestor count changed: " + str(len(scoped)))

    r2 = reference_snapshot(model, "(5.9)")
    r7 = reference_snapshot(model, "Proposition 2.7")
    general_annihilators = [
        step for step in scoped
        if step.rule is ProofRule.GIVEN
        and type(step.conclusion) is CitedFamilyAnnihilator
    ]
    general_prop27 = [
        step for step in scoped
        if step.rule is ProofRule.GIVEN
        and type(step.conclusion) is Prop27UniversalLiteratureStatement
    ]
    if len(general_annihilators) != 1 or len(general_prop27) != 1:
        raise RuntimeError("Expected one cited general GIVEN for both R2 and R7")
    annihilator_given = general_annihilators[0]
    prop_given = general_prop27[0]
    n6_relation = canonical_annihilator_instance(annihilator_given.conclusion, 6)
    if n6_relation is None:
        raise RuntimeError("(5.9) n=6 canonical specialization unavailable")
    n6_steps = [step for step in scoped
                if step.rule is ProofRule.INFERENCE
                and step.conclusion == n6_relation
                and len(step.premises) == 1
                and step.premises[0] is annihilator_given]

    typed_prop = typed_specialization(6)
    specialized = [step for step in scoped
                   if step.rule is ProofRule.INFERENCE
                   and type(step.conclusion) is Prop27TypedHopfDeltaStatement
                   and step.conclusion == typed_prop]
    prop_chain = []
    for step in specialized:
        if len(step.premises) != 1:
            continue
        middle = step.premises[0]
        if (middle.rule is ProofRule.INFERENCE
                and type(middle.conclusion) is Prop27GeneralTheoremPremise
                and len(middle.premises) == 1
                and middle.premises[0] is prop_given):
            prop_chain.append(step)

    upper_map = TodaDeltaMap(TodaPrimaryGroup(13, 13), TodaPrimaryGroup(11, 6))
    upper_goal = MapSurjective(upper_map)
    required = upper_delta_surjectivity_inputs(upper_goal)
    if required is None:
        raise RuntimeError("R37 typed upper Delta premise contract missing")
    certified_upper = [
        step for step in scoped
        if step.rule is ProofRule.INFERENCE
        and step.conclusion == upper_goal
        and len(step.premises) == 4
        and tuple(parent.conclusion for parent in step.premises) == required
        and all(parent.rule is ProofRule.INFERENCE for parent in step.premises)
    ]
    if len(certified_upper) != 1:
        raise RuntimeError("Upper Delta lacks its four checked distinct premises")
    upper = certified_upper[0]
    # The order-two codomain and signed lower-Delta image must be the actual
    # two independently cited GIVEN premises of the certified kernel step.
    kernel_step = upper.premises[2]
    if len(kernel_step.premises) != 3:
        raise RuntimeError("Cited lower Delta kernel must have three antecedents")
    domain_step, codomain_step, signed_step = kernel_step.premises
    codomain = codomain_step.conclusion
    order_two = (
        codomain_step.rule is ProofRule.GIVEN
        and type(codomain) is Relation
        and codomain.relation_type is RelationType.EQUALITY
        and codomain.lhs == TodaPrimaryGroup(9, 5)
        and type(codomain.rhs) is FiniteCyclicGroup
        and codomain.rhs.order == 2
    )
    if not order_two or signed_step.rule is not ProofRule.GIVEN:
        raise RuntimeError("Order-two R5 and cited signed R6 are not proved")
    proof_has_n6 = bool(n6_steps) and any(ancestor_contains(upper, node) for node in n6_steps)
    proof_has_prop27 = bool(prop_chain) and any(ancestor_contains(upper, node) for node in prop_chain)
    if not proof_has_n6 or not proof_has_prop27:
        raise RuntimeError("The upper Delta root lost a certified R2 or R7 ancestor")
    for item, source in ((r2, annihilator_given), (r7, prop_given)):
        if not any(model.steps[index] is source for index in item["step_indices"]):
            raise RuntimeError("Citation not attached to the actual typed GIVEN: " + item["locator"])

    # The renderer is not modified; the HTML/Markdown defect is an observation.
    proof_region = markdown.partition("\n証明\n")[2]
    if not proof_region:
        raise RuntimeError("Unable to identify complete narrative proof section")
    significant = lines_containing(
        proof_region,
        (r"\Delta", r"\nu", r"\eta", "全射", "単射", "完全性", "Proposition"),
    )
    lower_signed_lines = [
        line for line in significant
        if r"\Delta" in line and r"\pm" in line
        and (r"\nu_5" in line or r"\nu_{5}" in line)
        and (r"\eta_8" in line or r"\eta_{8}" in line)
    ]
    r2_body = r2["reference_body_present"] and "\\nu" in " ".join(r2["statement_bodies"])
    r7_body = r7["reference_body_present"] and "\\Delta" in " ".join(r7["statement_bodies"])
    prop_formula_in_body = any(
        "\\Delta" in line and "\\iota_{13}" in line and "2\\iota_{11}" in line
        for line in proof_region.splitlines()
    )
    n6_in_body = any(
        "\\nu_{6}" in line and "\\eta_{9}" in line and "=0" in line
        for line in proof_region.splitlines()
    )
    return {
        "target": "pi_12^7 = 0",
        "status": proof.status.value,
        "model_steps": len(model.steps),
        "root_ancestor_steps": len(scoped),
        "open_goals": len(proof.open_goals),
        "citation_count": len(model.citations),
        "r2": r2,
        "r7": r7,
        "source_proof": {
            "r2_general_given": True,
            "r2_n6_relation_inferred_and_used": proof_has_n6,
            "r7_general_given": True,
            "r7_n6_typed_instance_inferred_and_used": proof_has_prop27,
            "upper_delta_four_distinct_inference_premises": True,
            "lower_delta_codomain_order_two_given": order_two,
            "signed_lower_delta_image_given": True,
            "four_premise_types": [type(item).__name__ for item in required],
        },
        "narrative": {
            "r2_general_formula_in_reference": bool(r2_body),
            "r7_general_formula_in_reference": bool(r7_body),
            "r7_hopf_delta_specialization_in_proof": prop_formula_in_body,
            "r2_n6_zero_relation_in_proof": n6_in_body,
            "unnecessary_lower_delta_plusminus_in_proof": bool(lower_signed_lines),
            "signed_lower_delta_lines": lower_signed_lines,
            "relevant_proof_lines": significant,
        },
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_files_changed": 0,
        "full_pytest": False,
        "gate": "PASS_CERTIFIED_TREE_DISPLAY_AUDIT_ONLY",
    }


def report_path(dry_run: bool) -> Path:
    home = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return home / "EHPProofTracerAudit" / REPORT_FOLDER / (
        "preflight.json" if dry_run else "reference_tree_audit.json"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    state = verify_checkout()
    observations = None if opts.dry_run else inspect_public_proof()
    report = {
        "phase": "174-R3-R7-R55R2",
        "state": state,
        "observations": observations,
        "gate": "PASS_SOURCE_GUARD_ONLY" if opts.dry_run else observations["gate"],
    }
    destination = report_path(opts.dry_run)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("PHASE174_R55R2_LOCAL_HEAD=" + str(state["local_head"]))
    print("PHASE174_R55R2_SOURCE_GUARD=" + str(state["source_guard"]))
    if observations is not None:
        for locator, key in (("R2", "r2"), ("R7", "r7")):
            info = observations[key]
            print(f"PHASE174_R55R2_{locator}_NUMBER=" + str(info["number"]))
            print(f"PHASE174_R55R2_{locator}_REFERENCE_BODY_PRESENT="
                  + str(info["reference_body_present"]))
        for name, value in observations["source_proof"].items():
            print("PHASE174_R55R2_TREE_" + name.upper() + "=" + str(value))
        for name, value in observations["narrative"].items():
            if name not in ("relevant_proof_lines", "signed_lower_delta_lines"):
                print("PHASE174_R55R2_NARRATIVE_" + name.upper() + "=" + str(value))
    print("PHASE174_R55R2_REPORT=" + str(destination))
    print("PHASE174_R55R2_GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
