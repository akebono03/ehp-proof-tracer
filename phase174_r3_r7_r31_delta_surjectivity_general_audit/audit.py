"""R31: independent mathematical/typed audit of Delta surjectivity.

No production code, proof provider, database, GIVEN or verified ProofStep is
changed or fabricated. A valid *conditional* implication is not a proof of its
unverified hypotheses.
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
BASE_HEAD = "42025c9fb7198f766d3e09531e35bfe04142ceb7"
REVIEWED_HEAD = "25118e281445ca17b30c60c8fd02d00acaa25ea5"
R30_CHANGED = "phase165_r52_r9_shared_math.py"
SOURCE = "sources/toda/Toda_05_2.tex"
PINS = {
    SOURCE: "579661138928499ba04a51327f686d9b971b5314",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "phase165_r52_r9_shared_math.py": "742451ea67ede314f99246afbb470a5e8a7f008f",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase174_r3_r7_r30_prop27_public_provider_wiring/provider.py": "b54a73a5cb98803c9872973cbf194b0068ba6c8c",
    "phase174_r3_r7_r30_prop27_public_provider_wiring/tests/test_wiring.py": "b6a975dae81454e6984f3e695903a19a87f32bda",
    "phase174_r3_r7_r21_delta_hopf_chain_audit/audit.py": "3384e0856a466be1ed021d159f7092f1462b20b9",
    "phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py": "c6f5dd80bfc9278ad4b03bbac23566ea66ed6a3c",
    "phase174_r3_r7_r18_delta_image_surjectivity/rule.py": "f8da1f6fb7d5fb66feae33b4a4847fbad6891342",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r25_prop27_isolated_inference/rule.py": "e5ab7aa7a88f8ce49844ced057a81bd34c9a1e3b",
    "tests/test_phase50_prop27_theorem_semantics.py": "42961f363a31b01559391317a66815311e60c83a",
}
START = r"\begin{proposition}\label{prop:5.9}"
END = r"\begin{lemma}\label{lemma:5.10}"
DEPENDENCIES = (
    ("suspension_image_zero", r"E\pi_{10}^5=0"),
    ("hopf_delta_exact_sequence", r"0\to \pi^{6}_{11}\xrightarrow{H}\pi^{11}_{11}\xrightarrow{\ \Delta\ }\pi^{5}_{9}"),
    ("lower_delta_kernel", r"\(\ker\Delta=\gen{2\iota_{11}}\)"),
    ("prop27_typed_witness", r"H(\Delta(\iota_{13}))=\pm2\iota_{11}"),
    ("derived_cyclic_codomain", r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}"),
    ("derived_top_delta_isomorphism", r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}"),
    ("derived_root_zero", r"\pi_{12}^7=0"),
)
SUPPORTING = (
    r"\Delta(\eta_{11})=\nu_5\circ\eta_8^2",
    r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0",
    r"Prop5.8 と (5.10) により",
)


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_pinned_blob(data: bytes, sha: str) -> bool:
    """Allow exact reviewed bytes and whole-file CRLF/LF conversions only."""
    canonical = data.replace(b"\r\n", b"\n")
    candidates = (data, canonical, canonical.replace(b"\n", b"\r\n"))
    return len(sha) == 40 and any(git_blob_sha(candidate) == sha for candidate in candidates)


def verify_checkout() -> dict[str, object]:
    """Accept the reviewed R30 handoff without resetting its local edits."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R31 ZIP must be extracted in repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R31 requires develop branch")
    head = git("rev-parse", "HEAD")
    remote_text = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_text.split()[0] if remote_text else ""
    if remote != REVIEWED_HEAD or head not in (BASE_HEAD, REVIEWED_HEAD):
        raise RuntimeError("GitHub HEAD changed, or local HEAD needs a new review")
    staged = tuple(git("diff", "--cached", "--name-only").splitlines())
    if staged:
        raise RuntimeError("Staged changes require separate review: " + repr(staged))
    modified = tuple(git("diff", "--name-only").splitlines())
    if any(path != R30_CHANGED for path in modified):
        raise RuntimeError("Unexpected local tracked edits: " + repr(modified))
    for relative, sha in PINS.items():
        path = ROOT / relative
        if not path.is_file() or not matches_pinned_blob(path.read_bytes(), sha):
            raise RuntimeError("Reviewed GitHub source mismatch: " + relative)
    return {
        "local_head": head,
        "remote_head": remote,
        "handoff_mode": "R30_UNCOMMITTED_REVIEWED" if head == BASE_HEAD else "R30_MERGED_REVIEWED",
        "accepted_tracked_edits": list(modified),
        "pinned_source_count": len(PINS),
        "source_guard": "PASS",
    }


def inspect_toda_source(text: str) -> dict[str, object]:
    """Inspect the source *proof*, never register its final claim as GIVEN."""
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("Proposition 5.9 boundaries changed")
    a, b = text.index(START), text.index(END)
    if a >= b:
        raise ValueError("Reversed Proposition 5.9 boundaries")
    section = text[a:b]
    positions = []
    for name, token in DEPENDENCIES:
        if section.count(token) != 1:
            raise ValueError("Missing or ambiguous Toda proof dependency: " + name)
        positions.append(section.index(token))
    if positions != sorted(positions):
        raise ValueError("Toda proof dependency order changed")
    for token in SUPPORTING:
        if section.count(token) != 1:
            raise ValueError("Supporting proof clause missing: " + token)
    previous = text[:a]
    if previous.count(r"\Delta(\iota_{11})=\nu_5\circ\eta_8") < 1:
        raise ValueError("Earlier cited (5.10) Delta generator formula missing")
    return {
        "independent_source_verified": True,
        "preconclusion_dependencies": [name for name, _ in DEPENDENCIES[:4]],
        "printed_conclusions_not_treated_as_premises": True,
        "lower_delta_requires_independent_kernel_proof": True,
        "zero_suspension_image_requires_independent_proof": True,
    }


def inspect_typed_obligations() -> dict[str, object]:
    """Construct goals and validate existing rules; construct no ProofStep."""
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import (
        TodaDeltaMap, TodaEHPExactnessWindow, TodaHopfInvariantMap,
        TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
    )
    from map_facts import EHP_H_MAP, EHP_DELTA_MAP
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization
    from toda_rules import TodaProp42ExactnessStatement

    group = TodaPrimaryGroup
    upper = TodaDeltaMap(group(13, 13), group(11, 6))
    hopf = TodaHopfInvariantMap(group(11, 6), group(11, 11))
    lower = TodaDeltaMap(group(11, 11), group(9, 5))
    root = TodaPrimaryGroupZeroStatement(group(12, 7))
    root_premises = ehp_zero_inputs(root)
    if root_premises is None or root_premises[0] != MapSurjective(upper):
        raise RuntimeError("R3 EHP root map contract changed")
    prop27 = typed_specialization(6)
    if prop27.delta != upper or prop27.hopf != hopf or not prop27.sign_undetermined:
        raise RuntimeError("R30 Prop 2.7 typed map identity changed")
    injective = MapInjective(hopf)
    injective_premises = hopf_injectivity_from_zero_image_inputs(injective)
    if (injective_premises is None or
            not isinstance(injective_premises[0], ImageZeroStatement) or
            injective_premises[0].map.source_group != group(10, 5) or
            injective_premises[0].map.target_group != group(11, 6)):
        raise RuntimeError("R5 Hopf-injectivity antecedents changed")
    lower_exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=group(11, 6), middle_term=group(11, 11),
        target_term=group(9, 5), first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
    ))
    if prop42_exactness_indices(lower_exact) != (5, 11, "h_delta"):
        raise RuntimeError("Lower H-Delta exactness indices invalid")
    iota = HomotopyElement(
        name="iota_11", dimension=11, source=11, target=11,
        generator=GeneratorSymbol("iota", 11),
    )
    lower_kernel = KernelMultipleStatement(lower, group(11, 11), iota, 2)
    if lower_kernel.multiple != 2 or lower_kernel.map != lower:
        raise RuntimeError("Lower Delta kernel goal ill-typed")
    image_equals_kernel = EHPImageEqualsKernelStatement(lower_exact.window)
    if image_equals_kernel.window != lower_exact.window:
        raise RuntimeError("Lower exactness image-kernel bridge changed")
    return {
        "root_target": repr(root),
        "upper_delta_surjectivity_goal": repr(MapSurjective(upper)),
        "hopf_injectivity_goal": repr(injective),
        "zero_suspension_image_goal": repr(injective_premises[0]),
        "lower_h_delta_exactness_goal": repr(lower_exact),
        "lower_image_equals_kernel_goal": repr(image_equals_kernel),
        "lower_delta_kernel_goal": repr(lower_kernel),
        "prop27_n6_typed": True,
        "generic_lemma_conditionally_sound": True,
        "independent_lower_kernel_certified_in_r31": False,
        "independent_zero_image_certified_in_r31": False,
        "typed_generator_transport_rule_installed_in_r31": False,
    }


def report(dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    source = inspect_toda_source((ROOT / SOURCE).read_text(encoding="utf-8-sig"))
    typed = None if dry_run else inspect_typed_obligations()
    return {
        "phase": "174-R3-R7-R31",
        "git_state": state,
        "source": source,
        "typed": typed,
        "new_givens": 0,
        "new_math_rules": 0,
        "production_files_changed": 0,
        "web_http_tested": False,
        "full_pytest": False,
        "delta_surjectivity_proved": False,
        "root_complete": False,
        "gate": (
            "PASS_R31_SOURCE_PREFLIGHT_ONLY" if dry_run else
            "PASS_R31_GENERAL_BRIDGE_AUDITED_LOWER_KERNEL_AND_ZERO_IMAGE_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(dry_run=args.dry_run)
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r31"
    )
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("preflight.json" if args.dry_run else "general_inference_audit.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R31_"
    print(prefix + "LOCAL_HEAD=" + str(result["git_state"]["local_head"]))
    print(prefix + "REMOTE_HEAD=" + str(result["git_state"]["remote_head"]))
    print(prefix + "HANDOFF_MODE=" + str(result["git_state"]["handoff_mode"]))
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "MATH_BRIDGE_CONDITIONALLY_VALID=True")
    print(prefix + "NEW_GIVENS=0")
    print(prefix + "NEW_RULES=0")
    print(prefix + "DELTA_SURJECTIVITY_PROVED=False")
    print(prefix + "ROOT_COMPLETE=False")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(output))
    print(prefix + "GATE=" + str(result["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
