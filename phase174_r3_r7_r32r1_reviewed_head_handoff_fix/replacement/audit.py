"""R32 source-first, read-only audit of the lower EHP Delta cyclic kernel.

No application source, renderer, registry, GIVEN or proof provider is changed.
The conditional contract is NOT a proof of the source, target, or image facts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_HEAD = "25118e281445ca17b30c60c8fd02d00acaa25ea5"
REVIEWED_R31_MERGE_HEAD = "02f694b27a4239052bfa9d27a116fca6bbbff6b5"
SOURCE = "sources/toda/Toda_05_2.tex"
R31_AUDIT = "phase174_r3_r7_r31_delta_surjectivity_general_audit/audit.py"
R31_SHA256 = "ab6f81dbbb32c6fd46dfb85c639534f7eff15062e2cc42c58b32f44efc0bc191"
PINS = {
    SOURCE: "579661138928499ba04a51327f686d9b971b5314",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r12_r2_quotient_rules.py": "2b3e8e0449382e9245ee22f08501e9cede0a5b59",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r52_r9_shared_math.py": "742451ea67ede314f99246afbb470a5e8a7f008f",
    "phase165_r57_r19_delta_image_backward.py": "c5b3447258f41e15219ead8daeeb17cbb5605b6d",
    "phase174_r3_r7_r18_delta_image_surjectivity/rule.py": "f8da1f6fb7d5fb66feae33b4a4847fbad6891342",
    "phase174_r3_r7_r18_delta_image_surjectivity/tests/test_rule.py": "603dc4c687cbb445fc8909d53ff66fede8e01169",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "toda_delta_image_rules.py": "f0ccdc2d3b8545986caaaba51a213c86cc08b781",
    "phase174_r3_r7_r30_prop27_public_provider_wiring/provider.py": "b54a73a5cb98803c9872973cbf194b0068ba6c8c",
}
PROP58 = r"\begin{proposition}\label{prop:5.8}"
PROP59 = r"\begin{proposition}\label{prop:5.9}"
EQ510 = r"\begin{equation}\label{eq:5.10}"
PROP58_CODOMAIN = r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}"
EQ510_IMAGE = r"\Delta(\iota_{11})=\nu_5\circ\eta_8"
PROP59_KERNEL = r"\ker\Delta=\gen{2\iota_{11}}"
DIAGONAL = r"\pis{n}{S^n} = \z\gen{\iota_n}"


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_pin(data: bytes, sha: str) -> bool:
    canonical = data.replace(b"\r\n", b"\n")
    return len(sha) == 40 and any(
        git_blob_sha(candidate) == sha
        for candidate in (data, canonical, canonical.replace(b"\n", b"\r\n"))
    )


def verify_checkout() -> dict[str, object]:
    """Fail closed on new GitHub code, preserving the untracked R31 package."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R32 ZIP must be extracted at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R32 requires develop")
    head = git("rev-parse", "HEAD")
    remote_result = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_result.split()[0] if remote_result else ""
    # GitHub reviewed R31 as one successor commit containing only the R31 audit
    # package. The checkout may still be at R30 while R31 is locally untracked.
    # The R31 file is checked below against its original exact SHA256 in both
    # handoff modes; never fetch, pull, reset, or overwrite it here.
    if (remote != REVIEWED_R31_MERGE_HEAD
            or head not in (REVIEWED_HEAD, REVIEWED_R31_MERGE_HEAD)):
        raise RuntimeError("Unreviewed local/remote develop handoff; review before R32")
    staged = git("diff", "--cached", "--name-only").splitlines()
    changed = git("diff", "--name-only").splitlines()
    if staged or changed:
        raise RuntimeError("Tracked edits require review; no reset performed")
    for relative, sha in PINS.items():
        file = ROOT / relative
        if not file.is_file() or not matches_pin(file.read_bytes(), sha):
            raise RuntimeError("R32 reviewed file differs: " + relative)
    prior = ROOT / R31_AUDIT
    if not prior.is_file():
        raise RuntimeError("R31 audited package is not present; do not overwrite it")
    text = prior.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != R31_SHA256:
        raise RuntimeError("R31 audit file changed; previous work needs review")
    return {
        "local_head": head,
        "remote_head": remote,
        "handoff_mode": (
            "R31_LOCAL_UNMERGED_REVIEWED" if head == REVIEWED_HEAD
            else "R31_MERGED_REVIEWED"
        ),
        "source_guard": "PASS",
        "r30_preserved": True,
        "r31_preserved": True,
        "git_pins_checked": len(PINS),
        "tracked_changes": 0,
    }


def inspect_toda_citations(text: str) -> dict[str, object]:
    """Separate prior source premises from Prop 5.9's printed conclusion."""
    if any(text.count(t) != 1 for t in (PROP58, PROP59, EQ510)):
        raise ValueError("Toda source proposition/equation boundaries changed")
    p58, e510, p59 = (text.index(t) for t in (PROP58, EQ510, PROP59))
    if not (p58 < e510 < p59):
        raise ValueError("Toda Prop 5.8 -> (5.10) -> Prop 5.9 order invalid")
    prop58_section = text[p58:text.index(r"\end{proposition}", p58)]
    eq510_section = text[e510:text.index(r"\end{equation}", e510)]
    next_lemma = text.index(r"\begin{lemma}\label{lemma:5.10}", p59)
    prop59_section = text[p59:next_lemma]
    if prop58_section.count(PROP58_CODOMAIN) != 1:
        raise ValueError("Prior Prop 5.8 finite cyclic codomain missing")
    if eq510_section.count(EQ510_IMAGE) != 1:
        raise ValueError("Prior equation (5.10) signed generator image missing")
    if prop59_section.count(PROP59_KERNEL) != 1:
        raise ValueError("Prop 5.9 lower kernel conclusion missing")
    if DIAGONAL not in text[:p58]:
        raise ValueError("Earlier general diagonal free group statement missing")
    return {
        "prop58_codomain_precedes_prop59": True,
        "equation_510_precedes_prop59": True,
        "diagonal_free_group_in_source": True,
        "prop59_kernel_is_derived_not_given": True,
        "printed_claim_is_verified_proof_step": False,
        "original_print_edition_verified": False,
    }


def inspect_typed_contract() -> dict[str, object]:
    """Construct only hypothetical premises, never GIVENs or ProofSteps."""
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import (
        FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap,
        TodaPrimaryGroup,
    )
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import (
        conditional_kernel_premises, signed_cyclic_kernel_membership,
        valid_ehp_lower_delta,
    )
    from proof import Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement

    group = TodaPrimaryGroup
    lower = TodaDeltaMap(group(11, 11), group(9, 5))
    source_generator = HomotopyElement("iota_11", 11, 11, 11, GeneratorSymbol("iota", 11))
    target_generator = HomotopyElement(
        "nu_5_eta_8", 9, 9, 5, GeneratorSymbol("nu_eta", 5),
    )
    domain = Relation(group(11, 11), FreeCyclicGroup(source_generator), RelationType.EQUALITY)
    codomain = Relation(group(9, 5), FiniteCyclicGroup(2, target_generator), RelationType.EQUALITY)
    signed = TodaDeltaImageUpToSignStatement(lower, source_generator, target_generator)
    goal = KernelMultipleStatement(lower, group(11, 11), source_generator, 2)
    required = conditional_kernel_premises(goal, domain, codomain, signed)
    if required != (domain, codomain, signed) or not valid_ehp_lower_delta(lower):
        raise RuntimeError("R32 isolated conditional kernel contract invalid")
    if not all(signed_cyclic_kernel_membership(2, k, sign) == (k % 2 == 0)
               for sign in (-1, 1) for k in range(-10, 11)):
        raise RuntimeError("R32 signed cyclic coefficient calculation invalid")
    db_prior = exact_prior_database_result(5, 4)
    if db_prior is not None:
        db_group_is_target = (
            type(db_prior) is Relation
            and db_prior.lhs == lower.target_group
            and type(db_prior.rhs) is FiniteCyclicGroup
            and db_prior.rhs.order == 2
        )
    else:
        db_group_is_target = False
    return {
        "lower_delta_map": repr(lower),
        "kernel_goal": repr(goal),
        "conditional_premise_types": [type(x).__name__ for x in required],
        "isolate_only": True,
        "hypothetical_premises_not_certified": True,
        "db_prior_present": db_prior is not None,
        "db_prior_has_expected_cyclic_shape": db_group_is_target,
        "db_prior_is_independent_literature_reference": False,
        "kernel_direct_given_inserted": False,
        "general_rule_registered": False,
        "public_proof_step_created": False,
    }


def inspect_screened_frontier() -> dict[str, object]:
    """Inspect admitted source leaves but never infer a proof from their counts."""
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from proof import ProofRule, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    lower = TodaDeltaMap(TodaPrimaryGroup(11, 11), TodaPrimaryGroup(9, 5))
    generator = HomotopyElement("iota_11", 11, 11, 11, GeneratorSymbol("iota", 11))
    kernel = KernelMultipleStatement(lower, lower.source_group, generator, 2)
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    leaves = tuple(link.step for link in screened.proof_links
                   if link.step is not None and link.step.rule is ProofRule.GIVEN)
    direct_kernel = tuple(step for step in leaves if step.conclusion == kernel)
    direct_root = tuple(step for step in leaves if step.conclusion == goal)
    if direct_kernel or direct_root:
        raise RuntimeError("Forbidden kernel/root direct GIVEN exposed after screening")
    lower_map_signed = tuple(
        step for step in leaves
        if type(step.conclusion) is TodaDeltaImageUpToSignStatement
        and step.conclusion.map == lower
    )
    signed = tuple(step for step in lower_map_signed
                   if step.conclusion.element == generator)
    source_group = tuple(step for step in leaves if type(step.conclusion) is Relation
                         and step.conclusion.relation_type is RelationType.EQUALITY
                         and step.conclusion.lhs == lower.source_group)
    target_group = tuple(step for step in leaves if type(step.conclusion) is Relation
                         and step.conclusion.relation_type is RelationType.EQUALITY
                         and step.conclusion.lhs == lower.target_group)
    return {
        "screened_signed_lower_map_leaves": len(lower_map_signed),
        "screened_signed_exact_generator_leaves": len(signed),
        "screened_domain_relation_leaves": len(source_group),
        "screened_codomain_relation_leaves": len(target_group),
        "screened_direct_kernel_given": 0,
        "screened_direct_root_given": 0,
        "screened_counts_are_not_certified_inference": True,
        "exact_generator_count_uses_synthetic_representation": True,
    }


def report(dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    cited = inspect_toda_citations((ROOT / SOURCE).read_text(encoding="utf-8-sig"))
    typed = None if dry_run else inspect_typed_contract()
    screened = None if dry_run else inspect_screened_frontier()
    return {
        "phase": "174-R3-R7-R32",
        "git_state": state,
        "source": cited,
        "typed": typed,
        "screened": screened,
        "new_givens": 0,
        "new_rules": 0,
        "production_files_changed": 0,
        "web_http_tested": False,
        "full_pytest": False,
        "delta_surjectivity_proved": False,
        "lower_delta_kernel_proved": False,
        "root_complete": False,
        "gate": (
            "PASS_R32_SOURCE_PREFLIGHT_ONLY" if dry_run else
            "PASS_R32_LOWER_DELTA_KERNEL_CONDITIONAL_AUDITED_TYPED_PROOF_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(dry_run=args.dry_run)
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r32"
    )
    folder.mkdir(parents=True, exist_ok=True)
    file = folder / ("preflight.json" if args.dry_run else "lower_delta_kernel_audit.json")
    file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pre = "PHASE174_R3R7R32_"
    for key in ("local_head", "remote_head", "source_guard", "r30_preserved", "r31_preserved"):
        print(pre + key.upper() + "=" + str(result["git_state"][key]))
    print(pre + "SOURCE_CITATIONS_IN_DEPENDENCY_ORDER=True")
    if result["typed"] is not None:
        print(pre + "DB_PRIOR_EXPECTED_SHAPE=" + str(result["typed"]["db_prior_has_expected_cyclic_shape"]))
        for key, value in result["screened"].items():
            if key.startswith("screened_") and isinstance(value, int):
                print(pre + key.upper() + "=" + str(value))
    print(pre + "NEW_GIVENS=0")
    print(pre + "NEW_RULES=0")
    print(pre + "LOWER_DELTA_KERNEL_PROVED=False")
    print(pre + "DELTA_SURJECTIVITY_PROVED=False")
    print(pre + "ROOT_COMPLETE=False")
    print(pre + "FULL_PYTEST=False")
    print(pre + "REPORT=" + str(file))
    print(pre + "GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
