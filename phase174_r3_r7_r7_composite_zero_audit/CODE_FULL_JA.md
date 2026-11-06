# Phase 174 R3-R7-R7 — 完全コード

## 変更対象（すべて新規）

- `phase174_r3_r7_r7_composite_zero_audit/rule.py`: `expression_endpoints`, `composite_zero_generator_inputs`, `generator_zero_from_composite_rule`, `expand_generator_zero_from_composite` を新規追加。import は以下に全て掲載。
- `phase174_r3_r7_r7_composite_zero_audit/audit.py`: 出典・SHA・前工程・公開候補数の読み取り専用検査関数を新規追加。
- `phase174_r3_r7_r7_composite_zero_audit/tests/test_rule.py`, `tests/test_audit.py`: 全テスト関数と import を新規追加。
- `phase174_r3_r7_r7_composite_zero_audit/run.ps1`: 分割限定 pytest、DryRun、本実行。
- `__init__.py`, `README.md`, `AUDIT_PLAN_JA.md`: 新規追加。

既存のクラス・関数・import の変更はありません。以下の内容をディレクトリ直下へ完全コピーすることも可能です。省略コードはありません。

新規規則は群を特定する分岐を持たず、まだ共通公開探索に接続していません。全体 pytest は Phase 174 終了時のみ実行します。

## `__init__.py` — 全文

```python
"""Phase 174 R3-R7-R7 isolated audit package; no production wiring."""
```

## `rule.py` — 全文

```python
"""Generic composition-zero inference, isolated from public proof search.

A verified image f(g)=a∘b and an independently proved a=0 imply f(g)=0.
The source relation and mapped composite are separate typed proof obligations.
"""
from __future__ import annotations

from expression import Composition, Expression, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = "zero left composition factor implies zero generator image"


def expression_endpoints(value: object) -> tuple[int, int] | None:
    """Return (source sphere, target sphere) for explicitly typed composites."""
    if isinstance(value, HomotopyElement):
        if (not all(type(v) is int for v in
                    (value.dimension, value.source, value.target))
                or value.dimension != value.target
                or value.target < 2 or value.source <= value.target):
            return None
        return value.source, value.target
    if isinstance(value, Composition):
        left = expression_endpoints(value.left)
        right = expression_endpoints(value.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    return None


def composite_zero_generator_inputs(
    goal: object,
    composite_image: object,
) -> tuple[GeneratorImage, Relation] | None:
    """Demand a separately proved composite image and zero left-factor fact."""
    if (not isinstance(goal, GeneratorImage)
            or not isinstance(goal.map, TodaSuspensionMap)
            or not isinstance(goal.target_generator, Zero)
            or not isinstance(goal.source_generator, Expression)
            or isinstance(goal.source_generator, Zero)
            or not isinstance(composite_image, GeneratorImage)
            or composite_image.map != goal.map
            or composite_image.source_generator != goal.source_generator
            or not isinstance(composite_image.target_generator, Composition)):
        return None
    domain = goal.map.source_group
    target = goal.map.target_group
    if (not isinstance(domain, TodaPrimaryGroup)
            or not isinstance(target, TodaPrimaryGroup)):
        return None
    degree = domain.group_dimension
    sphere = domain.sphere_dimension
    if (type(degree) is not int or type(sphere) is not int
            or sphere < 2 or degree < sphere
            or target != TodaPrimaryGroup(degree + 1, sphere + 1)):
        return None
    composite = composite_image.target_generator
    if (expression_endpoints(composite) !=
            (degree + 1, sphere + 1)):
        return None
    left = composite.left
    right = composite.right
    if expression_endpoints(left) is None or expression_endpoints(right) is None:
        return None
    return composite_image, Relation(
        lhs=left, rhs=Zero(), relation_type=RelationType.EQUALITY,
    )


def generator_zero_from_composite_rule(
    goal: GeneratorImage, composite_image: GeneratorImage,
) -> InferenceRule:
    """Require both obligations as INFERENCE steps; never add a GIVEN."""
    required = composite_zero_generator_inputs(goal, composite_image)
    if required is None:
        raise ValueError("invalid composite-zero generator image")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and composite_zero_generator_inputs(goal, composite_image) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "If a separately proved generator image is a composition a∘b, "
            "and an independent typed proof establishes a=0, then "
            "the generator maps to zero. No source equation is admitted here."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=GeneratorImage,
                statement_pattern=required[0],
                proof_rule=ProofRule.INFERENCE,
            ),
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[1],
                proof_rule=ProofRule.INFERENCE,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_generator_zero_from_composite(
    goal: object,
    composite_image: object,
) -> tuple[GoalExpansion, ...]:
    """Offer one unproved generic candidate without modifying search providers."""
    required = composite_zero_generator_inputs(goal, composite_image)
    if required is None:
        return ()
    return (GoalExpansion(
        generator_zero_from_composite_rule(goal, composite_image),
        required,
    ),)
```

## `audit.py` — 全文

```python
"""Phase 174 R3-R7-R7: source-first audit of a composite zero generator.

Reads the previously certified R6 evidence, verifies the Toda transcription,
and checks only source-screened backward proposals. No proof is created.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R7"
BASE_HEAD = "cbe3b866b1e39f15fc1c6965004b705e31d61de5"
REVIEWED_R6_HEAD = "67c57fc9ae63ce783ffdf9b502d472900abad57f"
ALLOWED_SUCCESSOR_PREFIX = "phase174_r3_r7_r6_cyclic_generator_zero_image/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/audit.py": "8dff5c0a38558648b8894539c8b12929febd734a",
}
TODA_CLAUSES = {
    "annihilator_family": r"\nu_n\circ \eta_{n+3}=0\ (n\ge6)",
    "suspension_equals_composite_zero": (
        r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0"
    ),
    "zero_image_is_later_conclusion": r"E\pi_{10}^5=0",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def accepted_source_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(blob_sha(candidate) == expected for candidate in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def reviewed_head_lineage(
    local: str,
    remote: str,
    successors: tuple[str, ...],
    changed_paths: tuple[str, ...],
) -> str:
    if local != remote or len(local) != 40:
        raise RuntimeError("Local/remote develop HEAD mismatch")
    if local == BASE_HEAD and not successors and not changed_paths:
        return "REVIEWED_BASE"
    if (local == REVIEWED_R6_HEAD
            and successors == (REVIEWED_R6_HEAD,)
            and changed_paths
            and all(path.startswith(ALLOWED_SUCCESSOR_PREFIX)
                    for path in changed_paths)):
        return "REVIEWED_R6_ONLY_SUCCESSOR"
    raise RuntimeError("Unreviewed develop HEAD or changed sources")


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be under repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    if local == BASE_HEAD:
        successors: tuple[str, ...] = ()
        changed_paths: tuple[str, ...] = ()
    else:
        subprocess.run(
            ("git", "merge-base", "--is-ancestor", BASE_HEAD, local),
            cwd=root, check=True, capture_output=True,
        )
        successors = tuple(git(
            "rev-list", "--reverse", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
        changed_paths = tuple(git(
            "diff", "--name-only", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
    lineage = reviewed_head_lineage(local, remote, successors, changed_paths)
    for relative, expected in SOURCE_BLOBS.items():
        path = root / relative
        if (not path.is_file()
                or not accepted_source_blob(path.read_bytes(), expected)):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "head_lineage": lineage,
        "source_guard": "PASS",
        "reviewed_source_files": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_source(root: Path = ROOT) -> dict[str, Any]:
    body = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = body.index(r"\begin{proposition}\label{prop:5.9}")
    end = body.index(r"\qed", start)
    section = body[start:end]
    offsets = {key: section.find(value) for key, value in TODA_CLAUSES.items()}
    if (any(offset < 0 for offset in offsets.values())
            or not (offsets["annihilator_family"]
                    < offsets["suspension_equals_composite_zero"]
                    < offsets["zero_image_is_later_conclusion"])):
        raise RuntimeError("Toda (5.9) or Proposition 5.9 proof transcription differs")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "locator": "Toda Proposition 5.9 proof, equation (5.9)",
        "clause_offsets": offsets,
        "printed_edition_independently_verified": False,
        "typed_specialization_not_assumed_proved": True,
        "zero_image_conclusion_not_given": True,
    }


def prior_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r6" / "cyclic_generator_zero_image.json"


def validate_r6_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R6"
            or report.get("gate") != "PASS_ISOLATED_CYCLIC_ZERO_IMAGE_CHILDREN_UNPROVEN"):
        raise RuntimeError("Certified R6 full audit gate required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("completion_claimed") is not False
            or report.get("public_provider_changed") is not False):
        raise RuntimeError("R6 trust contract differs")
    live = report.get("live") or {}
    expected = {
        "isolated_zero_image_candidate_count": 1,
        "production_image_zero_frontier": 0,
        "production_presentation_frontier": 3,
        "production_generator_zero_frontier": 0,
    }
    if live.get("isolated_zero_image_candidate_count") != 1:
        raise RuntimeError("R6 generic candidate count differs")
    for key, count in expected.items():
        if key.startswith("production_") and (live.get(key) or {}).get("proposal_count") != count:
            raise RuntimeError("R6 observed child candidates differ: " + key)
    if (live.get("registered_presentation_is_not_proof") is not True
            or live.get("public_provider_unchanged") is not True):
        raise RuntimeError("R6 evidence screening differs")
    return {
        "gate": report["gate"],
        "production_generator_zero_proposals": 0,
        "completion_claimed": False,
    }


def inspect_composite_frontier() -> dict[str, Any]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from map_property_rules import ImageZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        cyclic_generator_zero_image_inputs,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        composite_zero_generator_inputs, expand_generator_zero_from_composite,
    )
    from phase174_r3_r7_source_first_audit.audit import is_exact_given, summarize_proposals
    from proof import ProofRule, Relation, RelationType
    from homotopy_groups import FiniteCyclicGroup

    target_zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target_zero)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=target_zero)
    presentation = exact_prior_database_result(5, 5)
    if (not isinstance(presentation, Relation)
            or presentation.relation_type is not RelationType.EQUALITY
            or presentation.lhs != TodaPrimaryGroup(10, 5)
            or not isinstance(presentation.rhs, FiniteCyclicGroup)
            or presentation.rhs.order != 2):
        raise RuntimeError("R6 source-screened finite cyclic presentation changed")
    suspension = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6))
    image_zero_goal = ImageZeroStatement(suspension)
    r6_children = cyclic_generator_zero_image_inputs(image_zero_goal, presentation)
    if r6_children is None:
        raise RuntimeError("R6 typed child construction changed")
    generator_zero = r6_children[1]
    nu6 = HomotopyElement(
        "nu_6", dimension=6, source=9, target=6,
        generator=GeneratorSymbol("nu", 6),
    )
    eta9 = HomotopyElement(
        "eta_9", dimension=9, source=10, target=9,
        generator=GeneratorSymbol("eta", 9),
    )
    eta10 = HomotopyElement(
        "eta_10", dimension=10, source=11, target=10,
        generator=GeneratorSymbol("eta", 10),
    )
    left = Composition(nu6, eta9)
    mapped_composite = Composition(left, eta10)
    image_candidate = GeneratorImage(
        suspension, generator_zero.source_generator, mapped_composite,
    )
    required = composite_zero_generator_inputs(generator_zero, image_candidate)
    options = expand_generator_zero_from_composite(generator_zero, image_candidate)
    if (required is None or len(options) != 1
            or options[0].subgoals != required
            or required[1].lhs != left
            or required[1].rhs != Zero()):
        raise RuntimeError("Typed source-factorization candidate invalid")
    if any(is_exact_given(item, admitted) for item in (
        target_zero, image_zero_goal, generator_zero, image_candidate, required[1],
    )):
        raise RuntimeError("Target, generator, or composed identity was GIVEN")
    return {
        "source_screening": "independent_source_screened",
        "candidate_from_toda_text_is_not_evidence": True,
        "registered_presentation_is_not_proof": True,
        "isolated_generator_zero_candidate_count": len(options),
        "typed_children": [
            {"type": type(item).__name__, "repr": repr(item)[:1500]}
            for item in required
        ],
        "public_composite_image_frontier": summarize_proposals(
            provider, required[0], admitted,
        ),
        "public_left_factor_zero_frontier": summarize_proposals(
            provider, required[1], admitted,
        ),
        "public_generator_zero_frontier": summarize_proposals(
            provider, generator_zero, admitted,
        ),
        "public_provider_unchanged": True,
        "new_verified_steps": 0,
    }


def output_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r7" / "composite_zero_audit.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    github = verify_git_and_sources(root)
    source = verify_toda_source(root)
    path = prior_report_path()
    if not path.is_file():
        raise RuntimeError("R6 full audit report is required")
    prior = validate_r6_evidence(json.loads(path.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_composite_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_ISOLATED_RULE",
        "git_state": github,
        "source_review": source,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": (
            "PASS_PREFLIGHT" if dry_run
            else "PASS_ISOLATED_COMPOSITE_ZERO_CHILDREN_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R7_"
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["head_lineage"])
    print(prefix + "TODA59_ANHILATOR=VERIFIED_TRANSCRIPTION")
    print(prefix + "R6_GENERATOR_ZERO_PROPOSALS=0")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "ISOLATED_COMPOSITE_ZERO_PROPOSALS=" + str(
            live["isolated_generator_zero_candidate_count"]
        ))
        for label, key in (
            ("PUBLIC_COMPOSITE_IMAGE", "public_composite_image_frontier"),
            ("PUBLIC_LEFT_FACTOR_ZERO", "public_left_factor_zero_frontier"),
            ("PUBLIC_GENERATOR_ZERO", "public_generator_zero_frontier"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(
                live[key]["proposal_count"]
            ))
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_rule.py` — 全文

```python
"""Source-independent generic composite-zero inference contracts."""
from __future__ import annotations

import pytest

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r7_r7_composite_zero_audit.rule import (
    RULE_NAME,
    composite_zero_generator_inputs,
    expand_generator_zero_from_composite,
    expression_endpoints,
    generator_zero_from_composite_rule,
)
from proof import (
    InferenceRule,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    find_inference_matches_for_rule,
)


def element(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(name, dimension=target, source=source, target=target)


def sample(degree: int = 10, sphere: int = 5):
    mapping = TodaSuspensionMap(
        TodaPrimaryGroup(degree, sphere),
        TodaPrimaryGroup(degree + 1, sphere + 1),
    )
    generator = element("g", degree, sphere)
    nu = element("a", sphere + 4, sphere + 1)
    eta = element("b", sphere + 5, sphere + 4)
    eta_second = element("c", degree + 1, sphere + 5)
    composite = Composition(Composition(nu, eta), eta_second)
    goal = GeneratorImage(mapping, generator, Zero())
    intermediate = GeneratorImage(mapping, generator, composite)
    return goal, intermediate


def inferred(statement: object) -> ProofStep:
    return ProofStep(
        conclusion=statement,
        premises=(),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only inferred fixture"),
    )


@pytest.mark.parametrize("degree,sphere", ((10, 5), (11, 6), (15, 10)))
def test_composite_zero_general_dimensions(degree: int, sphere: int) -> None:
    # In the generic fixture a has source sphere+4, so degree must be sphere+5.
    if degree != sphere + 5:
        return
    goal, intermediate = sample(degree, sphere)
    required = composite_zero_generator_inputs(goal, intermediate)
    assert required is not None
    assert required[0] == intermediate
    assert required[1] == Relation(
        intermediate.target_generator.left, Zero(), RelationType.EQUALITY,
    )
    candidates = expand_generator_zero_from_composite(goal, intermediate)
    assert len(candidates) == 1
    assert candidates[0].subgoals == required
    assert candidates[0].rule.name == RULE_NAME


def test_source_example_has_consistent_sphere_dimensions() -> None:
    goal, intermediate = sample(10, 5)
    assert expression_endpoints(intermediate.target_generator) == (11, 6)
    assert expression_endpoints(intermediate.target_generator.left) == (10, 6)
    assert expression_endpoints(intermediate.target_generator.right) == (11, 10)
    assert composite_zero_generator_inputs(goal, intermediate) is not None


def test_both_certified_ancestors_are_required() -> None:
    goal, intermediate = sample()
    required = composite_zero_generator_inputs(goal, intermediate)
    assert required is not None
    rule = generator_zero_from_composite_rule(goal, intermediate)
    proofs = tuple(inferred(item) for item in required)
    match = find_inference_matches_for_rule(rule, proofs)
    assert len(match) == 1
    derived = derive_inference_proof_step(match[0])
    assert derived.conclusion == goal
    assert derived.rule is ProofRule.INFERENCE
    assert derived.premises == proofs
    assert derived.inference_rule is rule
    assert find_inference_matches_for_rule(rule, proofs[:1]) == ()
    assert find_inference_matches_for_rule(rule, proofs[1:]) == ()


@pytest.mark.parametrize("index", (0, 1))
def test_direct_given_is_not_accepted(index: int) -> None:
    goal, intermediate = sample()
    required = composite_zero_generator_inputs(goal, intermediate)
    assert required is not None
    proofs = list(inferred(item) for item in required)
    proofs[index] = ProofStep(required[index], (), ProofRule.GIVEN)
    rule = generator_zero_from_composite_rule(goal, intermediate)
    assert find_inference_matches_for_rule(rule, tuple(proofs)) == ()


def test_wrong_generator_does_not_prove_target() -> None:
    goal, intermediate = sample()
    wrong = GeneratorImage(intermediate.map, element("other", 10, 5), intermediate.target_generator)
    assert composite_zero_generator_inputs(goal, wrong) is None
    assert expand_generator_zero_from_composite(goal, wrong) == ()


def test_mismatched_map_rejected() -> None:
    goal, intermediate = sample()
    wrong_map = TodaSuspensionMap(TodaPrimaryGroup(11, 6), TodaPrimaryGroup(12, 7))
    wrong = GeneratorImage(wrong_map, intermediate.source_generator, intermediate.target_generator)
    assert composite_zero_generator_inputs(goal, wrong) is None


def test_wrong_target_generator_shape_rejected() -> None:
    goal, intermediate = sample()
    for invalid in (Zero(), element("a", 11, 6), "some expression", 0):
        candidate = GeneratorImage(goal.map, goal.source_generator, invalid)
        assert expand_generator_zero_from_composite(goal, candidate) == ()


def test_wrong_composition_dimensions_rejected() -> None:
    goal, intermediate = sample()
    wrong = GeneratorImage(
        goal.map, goal.source_generator,
        Composition(Composition(element("a", 9, 6), element("b", 11, 10)),
                    element("c", 12, 11)),
    )
    assert composite_zero_generator_inputs(goal, wrong) is None


def test_wrong_domain_or_target_dimensions_rejected() -> None:
    goal, intermediate = sample()
    bad = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 9)),
        goal.source_generator, Zero(),
    )
    bad_image = GeneratorImage(bad.map, goal.source_generator, intermediate.target_generator)
    assert composite_zero_generator_inputs(bad, bad_image) is None
    assert composite_zero_generator_inputs(object(), intermediate) is None


def test_wrong_zero_type_or_untyped_source_rejected() -> None:
    goal, intermediate = sample()
    for wrong_zero in (0, "0", None, False):
        bad = GeneratorImage(goal.map, goal.source_generator, wrong_zero)
        assert composite_zero_generator_inputs(bad, intermediate) is None
    bad_source = GeneratorImage(goal.map, "g", Zero())
    matching = GeneratorImage(goal.map, "g", intermediate.target_generator)
    assert composite_zero_generator_inputs(bad_source, matching) is None


def test_wrong_annihilator_relation_cannot_close_proof() -> None:
    goal, intermediate = sample()
    required = composite_zero_generator_inputs(goal, intermediate)
    assert required is not None
    rule = generator_zero_from_composite_rule(goal, intermediate)
    wrong_left = Relation(element("x", 10, 6), Zero(), RelationType.EQUALITY)
    wrong_type = Relation(required[1].lhs, Zero(), RelationType.ZERO)
    wrong_right = Relation(required[1].lhs, 0, RelationType.EQUALITY)
    for bad_relation in (wrong_left, wrong_type, wrong_right):
        assert find_inference_matches_for_rule(
            rule, (inferred(required[0]), inferred(bad_relation)),
        ) == ()


def test_no_proof_step_or_target_given_constructed_by_expansion() -> None:
    goal, intermediate = sample()
    option, = expand_generator_zero_from_composite(goal, intermediate)
    assert len(option.subgoals) == 2
    assert all(not isinstance(child, ProofStep) for child in option.subgoals)
    assert goal not in option.subgoals
```

## `tests/test_audit.py` — 全文

```python
"""R7 read-only source, lineage and prior-R6 evidence contracts."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r7_composite_zero_audit.audit import (
    ALLOWED_SUCCESSOR_PREFIX,
    BASE_HEAD,
    REVIEWED_R6_HEAD,
    SOURCE_BLOBS,
    TODA_CLAUSES,
    accepted_source_blob,
    blob_sha,
    reviewed_head_lineage,
    validate_r6_evidence,
)


def sample_r6() -> dict:
    return {
        "phase": "174-R3-R7-R6",
        "gate": "PASS_ISOLATED_CYCLIC_ZERO_IMAGE_CHILDREN_UNPROVEN",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "isolated_zero_image_candidate_count": 1,
            "registered_presentation_is_not_proof": True,
            "public_provider_unchanged": True,
            "production_image_zero_frontier": {"proposal_count": 0},
            "production_presentation_frontier": {"proposal_count": 3},
            "production_generator_zero_frontier": {"proposal_count": 0},
        },
    }


def test_r6_certified_counts_are_not_promoted_to_proof() -> None:
    result = validate_r6_evidence(sample_r6())
    assert result["production_generator_zero_proposals"] == 0
    assert result["completion_claimed"] is False


@pytest.mark.parametrize("field", ("gate", "direct_given", "candidate", "presentation", "generator", "wiring"))
def test_r6_mismatch_fails_closed(field: str) -> None:
    report = sample_r6()
    if field == "gate":
        report["gate"] = "PASS_PREFLIGHT"
    elif field == "direct_given":
        report["new_group_given"] = 1
    elif field == "candidate":
        report["live"]["isolated_zero_image_candidate_count"] = 0
    elif field == "presentation":
        report["live"]["production_presentation_frontier"]["proposal_count"] = 4
    elif field == "generator":
        report["live"]["production_generator_zero_frontier"]["proposal_count"] = 1
    else:
        report["public_provider_changed"] = True
    with pytest.raises(RuntimeError):
        validate_r6_evidence(report)


def test_reviewed_base_and_successor_lineage_are_strict() -> None:
    assert reviewed_head_lineage(BASE_HEAD, BASE_HEAD, (), ()) == "REVIEWED_BASE"
    assert reviewed_head_lineage(
        REVIEWED_R6_HEAD, REVIEWED_R6_HEAD,
        (REVIEWED_R6_HEAD,),
        (ALLOWED_SUCCESSOR_PREFIX + "audit.py",),
    ) == "REVIEWED_R6_ONLY_SUCCESSOR"


@pytest.mark.parametrize("local,remote,successors,paths", (
    ("x" * 40, "x" * 40, (), ()),
    (BASE_HEAD, REVIEWED_R6_HEAD, (), ()),
    (REVIEWED_R6_HEAD, REVIEWED_R6_HEAD, (), ()),
    (REVIEWED_R6_HEAD, REVIEWED_R6_HEAD, (REVIEWED_R6_HEAD,), ("proof.py",)),
    (REVIEWED_R6_HEAD, REVIEWED_R6_HEAD, ("x" * 40,), (ALLOWED_SUCCESSOR_PREFIX + "a",)),
))
def test_unreviewed_or_mismatched_git_lineage_is_rejected(
    local: str, remote: str, successors: tuple[str, ...], paths: tuple[str, ...],
) -> None:
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(local, remote, successors, paths)


def test_transcription_general_annihilator_is_distinct_from_target_conclusion() -> None:
    assert r"\nu_n" in TODA_CLAUSES["annihilator_family"]
    assert r"n\ge6" in TODA_CLAUSES["annihilator_family"]
    assert r"\nu_6\circ\eta_9" in TODA_CLAUSES["suspension_equals_composite_zero"]
    assert TODA_CLAUSES["zero_image_is_later_conclusion"] == r"E\pi_{10}^5=0"
    assert len(SOURCE_BLOBS) >= 10
    assert len(REVIEWED_R6_HEAD) == 40


def test_source_blob_accepts_newline_normalization_only() -> None:
    value = b"alpha\nbeta\n"
    expected = blob_sha(value)
    assert accepted_source_blob(value, expected)
    assert accepted_source_blob(value.replace(b"\n", b"\r\n"), expected)
    assert not accepted_source_blob(b"alpha\ngamma\n", expected)


def test_isolated_audit_never_writes_production() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    funcs = {
        node.name for node in ast.parse(source.read_text(encoding="utf-8")).body
        if isinstance(node, ast.FunctionDef)
    }
    assert {"make_report", "verify_git_and_sources", "inspect_composite_frontier"} <= funcs
    assert not {"install", "apply_patch", "register_given", "change_public_provider"} & funcs
```

## `run.ps1` — 全文

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Each phase group runs in a separate pytest process: many legacy tests
    # share test_audit.py/test_rule.py basenames. Keep prepend import mode.
    $Groups = @(
        @{ Name = 'R7'; Paths = @(
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_rule.py',
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R6'; Paths = @(
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_rule.py',
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_audit.py'
        ) },
        @{ Name = 'R5'; Paths = @(
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py',
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_audit.py'
        ) },
        @{ Name = 'R4'; Paths = @(
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
        ) },
        @{ Name = 'R3'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py'
        ) },
        @{ Name = 'MATH_REGRESSION'; Paths = @(
            '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
            '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py',
            '.\phase165_r14_r9_ehp_exactness\test_phase165_r14_r9_ehp_exactness.py'
        ) }
    )

    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Focused test file missing: $TestPath"
            }
        }
    }

    Write-Output 'PHASE174_R3R7R7_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R7_PYTEST_GROUP=$($Group.Name)"
        $TestPaths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @TestPaths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R7 $($Group.Name) focused pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R7_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r7_composite_zero_audit.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r7_composite_zero_audit.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R7 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
```

## `README.md` — 全文

```markdown
# Phase 174 R3-R7-R7 — Composite Zero Generator Source Audit

This package examines a generic inference: if a homotopy generator has a separately proved image represented by `a ∘ b`, and `a = 0` has been independently proved, then the generator image is zero. The mathematical rule is isolated and **not** wired into production proof search, the public web route, the renderer, or the statement registry.

The source is the project's adopted transcription of Toda Proposition 5.9 and Equation (5.9), not an independently verified printed-edition scan. A transcription is not a proof leaf. The source-screened provider is used only to count available backward options.

Run on the `develop` branch in the EHP Proof Tracer repository. The previous R3-R7-R6 full audit report in `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r6\cyclic_generator_zero_image.json` is required.

```powershell
Expand-Archive -Path "$HOME\Downloads\R7.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r7_composite_zero_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r7_composite_zero_audit\run.ps1"
```

The script runs limited test groups in separate pytest processes to prevent collection conflicts. It validates the exact reviewed Git HEAD, pinned source files, the previous audit report, and the relative source and conclusion locations. The report is written outside the repository to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r7\composite_zero_audit.json`.

No full pytest suite is run. No production source file is modified.
```

## `AUDIT_PLAN_JA.md` — 全文

```markdown
# Phase 174 R3-R7-R7 監査計画

## 監査済みコード

GitHub `akebono03/ehp-proof-tracer` の `develop` HEAD `67c57fc9ae63ce783ffdf9b502d472900abad57f` を確認。前回の `cbe3b866b1e39f15fc1c6965004b705e31d61de5` からの差分は、R6 パッケージの追加ファイルだけ。`SOURCE_BLOBS` を個々に検査する。

## 数学的な推論

`GeneratorImage(E,g,a∘b)` と `Relation(a,Zero(),EQUALITY)` が、それぞれ独立した **INFERENCE** の証明を持つときのみ、`GeneratorImage(E,g,Zero())` を推論できる。合成の次元と懸垂写像の始域・終域は全て検査する。群や生成元に固有の規則分岐は置かない。

## 出典

Toda Proposition 5.9 の採用転写で、(5.9) の一般関係 `ν_n ∘ η_{n+3} = 0 (n >= 6)` と、生成元の懸垂像の合成表示を確認する。転写中にある結論そのものを GIVEN にしない。

## 変更対象と追加位置

既存プロダクションファイルの変更はなし。ルート直下の新規ディレクトリ `phase174_r3_r7_r7_composite_zero_audit/` に、`rule.py`（`expression_endpoints`, `composite_zero_generator_inputs`, `generator_zero_from_composite_rule`, `expand_generator_zero_from_composite`）、`audit.py`（Git・出典・前工程・候補数監査）、テスト、`run.ps1` を追加する。

## 検証

R7 の新規テストと R6/R5/R4/R3 の回帰、既存の限定数学テストを**別プロセス**で実行する。全体 pytest は実行しない。

## 完了条件

Source Guard、前工程 R6 の本実行記録、型付き候補の生成、子 Goal の探索候補数、公開 provider 非変更が確認できること。子 Goal が未完成なら目標も未完成を維持する。

## 次との境界

R7 は読み取り専用の監査と独立規則の検証まで。R8 以降で初めて、(5.9) の一般定義・生成元の像が出典付きに成立するか、プロダクションへの共通接続を検討する。専用 Narrative 追加は行わない。
```

