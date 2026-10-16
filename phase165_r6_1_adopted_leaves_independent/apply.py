from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r14_r36_adopted_backward.py"
NEW_FUNCTION = 'def adopted_leaf_steps(tex_path: Path) -> tuple[ProofStep, ...]:\n    """Register cited source steps independently of a selected proof goal.\n\n    The adopted source bundle has two reviewed diagonal statements,\n    six explicitly typed source statements, and the foundational identity\n    E(iota_2)=iota_3. This inventory is not derived from a search frontier.\n    """\n    from phase165_r14_r16_foundational_suspension import (\n        instantiate_foundational_identity_suspension,\n    )\n    path = Path(tex_path)\n    candidates = known_source_candidates(path)\n    source_text = path.read_text(encoding="utf-8")\n    completed = complete_toda51_source(source_text)\n    bridge, _ = build_phase165_r5_manifest_bridge()\n    integration = integrate_toda51_into_existing_reference(bridge, source_text)\n    review = AdoptedTextReview(\n        complete_source_sha256=completed.source_sha256,\n        diagonal_clause_checked=True,\n        reviewer_note="Adopted TeX (5.1) diagonal clause reviewed; original edition unverified",\n    )\n    reviewed, ids = promote_diagonal_from_existing_reference(integration.bridge, review)\n    diagonal_steps = []\n    for assertion_id in ids:\n        matches = [link.step for link in reviewed.proof_links\n                   if link.assertion_id == assertion_id and link.step is not None]\n        if len(matches) != 1:\n            raise ValueError("ambiguous adopted diagonal source link")\n        if matches[0].conclusion != reviewed.registry.assertion(assertion_id).content:\n            raise ValueError("diagonal source linkage mismatch")\n        diagonal_steps.append(matches[0])\n    if len(diagonal_steps) != 2:\n        raise ValueError("adopted diagonal source inventory changed")\n\n    for candidate in candidates:\n        if candidate.certification != "unverified_source_claim":\n            raise ValueError("unexpected source candidate certification")\n    if len(candidates) != 6:\n        raise ValueError("adopted source candidate inventory changed")\n\n    foundation_goal = instantiate_foundational_identity_suspension(2).statement\n    foundation = derive_foundational_suspension_step(foundation_goal)\n    if foundation is None or foundation.rule is not ProofRule.GIVEN:\n        raise ValueError("foundational suspension source unavailable")\n\n    from phase165_r14_r33_final_group import pi33_cyclic_step, hopf_eta2_image_step\n    from phase165_r14_r31_hopf_injective import toda51_pi21_zero_step, prop42_e_h_exactness_step\n    from phase165_r14_r30_hopf_surjective import prop42_h_delta_exactness_step\n    from phase165_r14_r26_prop42_typed import adopted_tex_proofstep, bind_proposition42\n    from phase165_r14_r29_delta_derived import Prop42ApplicationPolicy\n\n    policy = Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)\n    step_list = [*diagonal_steps, foundation,\n                 pi33_cyclic_step(path), hopf_eta2_image_step(),\n                 toda51_pi21_zero_step(path),\n                 prop42_e_h_exactness_step(policy),\n                 prop42_h_delta_exactness_step(policy),\n                 adopted_tex_proofstep(bind_proposition42(\n                     bridge, n=1, i=2, index_scope_confirmed=True,\n                 ))]\n    if len(step_list) != 9:\n        raise ValueError("adopted source inventory changed")\n    for step in step_list:\n        if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN:\n            raise ValueError("adopted source leaf must be a GIVEN ProofStep")\n        if sum(other.conclusion == step.conclusion for other in step_list) != 1:\n            raise ValueError("duplicate adopted source conclusion")\n    if {candidate.goal for candidate in candidates} - {step.conclusion for step in step_list}:\n        raise ValueError("source candidates are not represented by typed steps")\n    return tuple(step_list)\n'

def main():
    original = TARGET.read_text(encoding="utf-8-sig")
    tree = ast.parse(original)
    functions = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "adopted_leaf_steps"]
    if len(functions) != 1:
        raise RuntimeError("expected one adopted_leaf_steps")
    node = functions[0]
    lines = original.splitlines(keepends=True)
    old = "".join(lines[node.lineno-1:node.end_lineno])
    if "goals = backward_leaf_goals(pi32_goal())" not in old:
        if 'instantiate_foundational_identity_suspension(2).statement' in old:
            print(json.dumps({"status":"ALREADY_INSTALLED","full_pytest_run":False}))
            return
        raise RuntimeError("unrecognized adopted_leaf_steps; no changes made")
    revised = "".join(lines[:node.lineno-1]) + NEW_FUNCTION + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(revised)
    backup = TARGET.with_name(TARGET.name + ".r6_1_adopted_leaves.bak")
    if not backup.exists():
        shutil.copy2(TARGET, backup)
    TARGET.write_text(revised, encoding="utf-8")
    print(json.dumps({"status":"CHANGED","file":str(TARGET.relative_to(ROOT)),
                      "legacy_goal_dependency_removed_from_adopted_leaf_steps":True,
                      "full_pytest_run":False},indent=2))

if __name__ == "__main__":
    main()
