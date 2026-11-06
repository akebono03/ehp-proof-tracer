# Phase 174 R3-R7-R9 — 変更コード全文

## 変更対象

新規ディレクトリ `phase174_r3_r7_r9_composition_associativity/` にだけ追加する。既存ファイル、クラス、関数は変更しない。

- `rule.py`：新規関数 `typed_composition_factors`、`right_associated_composition`、`generator_image_associativity_inputs`、`generator_image_associativity_rule`、`expand_generator_image_associativity`。記載順に新規追加。
- `audit.py`：新規関数 `git`、`git_blob_sha`、`accepted_source_blob`、`verify_git_and_sources`、`verify_toda_source`、`previous_report_path`、`validate_r8_evidence`、`inspect_rebracketing_frontier`、`report_path`、`make_report`、`main`。記載順に新規追加。
- `tests/test_rule.py`、`tests/test_audit.py`：新規テストファイル。import とテスト関数全文。
- `run.ps1`：新規。PowerShell 全文。
- `__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`：新規。

## 数学的な境界

`GeneratorImage(E, g, a ◦ (b ◦ c))` が独立した `INFERENCE` として証明された場合に限り、`GeneratorImage(E, g, (a ◦ b) ◦ c)` を結合律で導出する。公開 provider は未変更。`ν₆ ◦ η₉ = 0` は未証明。

## 完全な新規ファイル

### `rule.py`

```python
"""Generic reassociation of a proved composition-valued generator image.

A typed proof that E(g) is a right-associated composite implies that it
is the equivalent left-associated composite. This isolated rule does not
prove E(g), the cited Toda annihilator, or any group presentation.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = "composition associativity transports a verified generator image"


def typed_composition_factors(value: object) -> tuple[HomotopyElement, ...] | None:
    """Flatten only well-typed compositions of actual typed sphere maps."""
    if isinstance(value, HomotopyElement):
        if expression_endpoints(value) is None:
            return None
        return (value,)
    if not isinstance(value, Composition) or expression_endpoints(value) is None:
        return None
    left = typed_composition_factors(value.left)
    right = typed_composition_factors(value.right)
    if left is None or right is None:
        return None
    return left + right


def right_associated_composition(value: object) -> Composition | None:
    """Keep every factor and its order; alter parentheses only."""
    factors = typed_composition_factors(value)
    if factors is None or len(factors) < 3:
        return None
    result: object = factors[-1]
    for factor in reversed(factors[:-1]):
        result = Composition(factor, result)
    if not isinstance(result, Composition):
        return None
    if expression_endpoints(result) != expression_endpoints(value):
        return None
    return result


def generator_image_associativity_inputs(
    goal: object,
) -> tuple[GeneratorImage] | None:
    """Demand a proved right-associated image for the original same g and E."""
    if not isinstance(goal, GeneratorImage):
        return None
    mapping = goal.map
    if not isinstance(mapping, TodaSuspensionMap):
        return None
    domain, target = mapping.source_group, mapping.target_group
    if not isinstance(domain, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return None
    degree, sphere = domain.group_dimension, domain.sphere_dimension
    if (type(degree) is not int or type(sphere) is not int
            or sphere < 2 or degree < sphere
            or target != TodaPrimaryGroup(degree + 1, sphere + 1)):
        return None
    if (expression_endpoints(goal.source_generator) != (degree, sphere)
            or expression_endpoints(goal.target_generator) != (degree + 1, sphere + 1)):
        return None
    normalized = right_associated_composition(goal.target_generator)
    if normalized is None or normalized == goal.target_generator:
        return None
    return (GeneratorImage(mapping, goal.source_generator, normalized),)


def generator_image_associativity_rule(goal: GeneratorImage) -> InferenceRule:
    """Allow only one independently inferred and identically typed premise."""
    required = generator_image_associativity_inputs(goal)
    if required is None:
        raise ValueError("goal has no valid nontrivial composition reassociation")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == required[0]
            and generator_image_associativity_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "Composition is associative in the homotopy category. A separately "
            "proved image of precisely the same generator under precisely "
            "the same map may be rebracketed without adding any source fact."
        ),
        premise_patterns=(PremisePattern(
            statement_type=GeneratorImage,
            statement_pattern=required[0],
            proof_rule=ProofRule.INFERENCE,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_generator_image_associativity(goal: object) -> tuple[GoalExpansion, ...]:
    """Create an unproved backward branch without changing public providers."""
    inputs = generator_image_associativity_inputs(goal)
    if inputs is None:
        return ()
    return (GoalExpansion(generator_image_associativity_rule(goal), inputs),)
```

### `audit.py`

```python
"""R3-R7-R9: source-first audit of composition parenthesis mismatch.

No proof is created, and the public expansion provider is not modified.
The Toda annihilator is source text, not an authenticated proof premise.
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
PHASE = "174-R3-R7-R9"
REVIEWED_HEAD = "15785b921c15a19810b2b067715832ee20c61280"
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
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase174_r3_r7_r8_composite_image_gap/audit.py": "87e8558e63c014e4e9ae9d16576e594752f2bf66",
}
TODA_CLAUSES = {
    "general_annihilator": r"\nu_n\circ \eta_{n+3}=0\ (n\ge6)",
    "generator_suspension": r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0",
    "zero_image_conclusion": r"E\pi_{10}^5=0",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, check=True,
        text=True, capture_output=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def accepted_source_blob(data: bytes, expected_sha: str) -> bool:
    if len(expected_sha) != 40 or any(x not in "0123456789abcdef" for x in expected_sha):
        return False
    normalized = data.replace(b"\r\n", b"\n")
    return any(git_blob_sha(candidate) == expected_sha for candidate in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Expected repository root with this package as direct child")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if local != remote or local != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed develop HEAD: review current GitHub and tests")
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    for relative, sha in SOURCE_BLOBS.items():
        path = root / relative
        if not path.is_file() or not accepted_source_blob(path.read_bytes(), sha):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "reviewed_files": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_source(root: Path = ROOT) -> dict[str, Any]:
    body = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = body.index(r"\begin{proposition}\label{prop:5.9}")
    end = body.index(r"\qed", start)
    section = body[start:end]
    positions = {name: section.find(text) for name, text in TODA_CLAUSES.items()}
    if any(offset < 0 for offset in positions.values()):
        raise RuntimeError("Toda Proposition 5.9 adopted transcription differs")
    if not (positions["general_annihilator"] < positions["generator_suspension"]
            < positions["zero_image_conclusion"]):
        raise RuntimeError("Toda source premise/conclusion sequence changed")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "reference": "Toda (5.9) in Proposition 5.9 proof",
        "positions": positions,
        "printed_edition_verified": False,
        "annihilator_specialization_is_unproved": True,
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r8" / "composite_image_gap.json"


def validate_r8_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R8"
            or report.get("gate") != "PASS_READ_ONLY_COMPOSITE_IMAGE_GAP_DIAGNOSIS"):
        raise RuntimeError("Certified R8 read-only audit is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R8 source and proof trust contract changed")
    live = report.get("live") or {}
    for key, expected in (
        ("public_composite_image_frontier", 0),
        ("public_left_factor_zero_frontier", 1),
        ("public_generator_zero_frontier", 0),
    ):
        if (live.get(key) or {}).get("proposal_count") != expected:
            raise RuntimeError("R8 observed frontier changed: " + key)
    if (live.get("existing_composite_image_rule_candidate_count") != 0
            or live.get("left_factor_rule_name") != "equality symmetry"
            or live.get("source_generator_type") != "Composition"
            or live.get("public_provider_unchanged") is not True
            or live.get("source_claim_promoted_to_given") is not False):
        raise RuntimeError("R8 structural gap or proof contract changed")
    return {
        "r8_gate": report["gate"],
        "previous_composite_options": 0,
        "previous_left_factor_rule_is_symmetry_only": True,
        "prior_completion_claimed": False,
    }


def inspect_rebracketing_frontier() -> dict[str, Any]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        cyclic_generator_zero_image_inputs,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        composite_zero_generator_inputs,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import (
        expand_generator_image_associativity, generator_image_associativity_inputs,
        right_associated_composition,
    )
    from phase174_r3_r7_source_first_audit.audit import is_exact_given, summarize_proposals
    from proof import ProofRule, Relation, RelationType

    zero_target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=zero_target)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=zero_target)
    prior = exact_prior_database_result(5, 5)
    if (not isinstance(prior, Relation) or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != TodaPrimaryGroup(10, 5)):
        raise RuntimeError("Prior finite cyclic presentation changed")
    e = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6))
    image_zero = ImageZeroStatement(e)
    r6 = cyclic_generator_zero_image_inputs(image_zero, prior)
    if r6 is None:
        raise RuntimeError("R6 generator child not available")
    original_generator_zero = r6[1]
    nu6 = HomotopyElement("nu_6", dimension=6, source=9, target=6,
                          generator=GeneratorSymbol("nu", 6))
    eta9 = HomotopyElement("eta_9", dimension=9, source=10, target=9,
                           generator=GeneratorSymbol("eta", 9))
    eta10 = HomotopyElement("eta_10", dimension=10, source=11, target=10,
                            generator=GeneratorSymbol("eta", 10))
    left = Composition(Composition(nu6, eta9), eta10)
    original_image = GeneratorImage(e, original_generator_zero.source_generator, left)
    r7 = composite_zero_generator_inputs(original_generator_zero, original_image)
    if r7 is None or r7[0] != original_image or r7[1] != Relation(
        Composition(nu6, eta9), Zero(), RelationType.EQUALITY,
    ):
        raise RuntimeError("R7 composite/annihilator obligations changed")
    r9 = generator_image_associativity_inputs(original_image)
    proposals = expand_generator_image_associativity(original_image)
    if r9 is None or len(proposals) != 1 or proposals[0].subgoals != r9:
        raise RuntimeError("Generic rebracketing failed to offer one unproved Goal")
    right_image = r9[0]
    if right_image.target_generator != right_associated_composition(left):
        raise RuntimeError("Rebracketed target does not preserve composition factors")
    old_options = expand_composite_generator_image(original_image)
    new_options = expand_composite_generator_image(right_image)
    original_children = component_image_obligations(original_image)
    new_children = component_image_obligations(right_image)
    if old_options or original_children is not None:
        raise RuntimeError("R8 original unbracketed gap unexpectedly disappeared")
    if new_options and (len(new_options) != 1 or new_options[0].subgoals != new_children):
        raise RuntimeError("Existing right-associated rule changed")
    if any(is_exact_given(item, admitted) for item in (
        zero_target, image_zero, original_generator_zero, original_image,
        right_image, r7[1],
    )):
        raise RuntimeError("Source-screened goal was improperly admitted as GIVEN")
    left_proposals = tuple(provider(r7[1]))
    if len(left_proposals) != 1 or getattr(left_proposals[0].rule, "name", None) != "equality symmetry":
        raise RuntimeError("R8 left factor is no longer symmetry-only")
    return {
        "source_screening": "independent_source_screened",
        "source_generator_shape": repr(original_generator_zero.source_generator)[:1500],
        "left_associated_image": repr(left)[:1500],
        "right_associated_image": repr(right_image.target_generator)[:1500],
        "isolated_rebracket_candidate_count": len(proposals),
        "old_composite_candidate_count": len(old_options),
        "right_associated_composite_candidate_count": len(new_options),
        "right_associated_component_goals": (
            [{"type": type(c).__name__, "repr": repr(c)[:1500]} for c in new_children]
            if new_children is not None else []
        ),
        "source_generator_is_not_evidence": True,
        "public_right_associated_image_frontier": summarize_proposals(
            provider, right_image, admitted,
        ),
        "public_left_associated_image_frontier": summarize_proposals(
            provider, original_image, admitted,
        ),
        "left_factor_root_rule": getattr(left_proposals[0].rule, "name", None),
        "left_factor_symmetry_is_not_proof": True,
        "new_verified_steps": 0,
        "public_provider_unchanged": True,
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r9" / "composition_associativity.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    source = verify_toda_source(root)
    previous = previous_report_path()
    if not previous.is_file():
        raise RuntimeError("Certified R8 report is required")
    prior = validate_r8_evidence(json.loads(previous.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_rebracketing_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "ISOLATED_TYPED_ASSOCIATIVITY_AUDIT",
        "git_state": git_state,
        "source_review": source,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "production_files_changed": False,
        "public_provider_changed": False,
        "full_pytest_run": False,
        "completion_claimed": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_ISOLATED_ASSOCIATIVITY_CHILDREN_PENDING",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = report_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R9_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "SOURCE_ANNIHILATOR=VERIFIED_TRANSCRIPTION_NOT_GIVEN")
    if report["live"] is not None:
        live = report["live"]
        for label, key in (
            ("ISOLATED_REBRACKET", "isolated_rebracket_candidate_count"),
            ("ORIGINAL_COMPOSITE_RULE", "old_composite_candidate_count"),
            ("REASSOCIATED_COMPOSITE_RULE", "right_associated_composite_candidate_count"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(live[key]))
        for label, key in (
            ("PUBLIC_RIGHT_IMAGE", "public_right_associated_image_frontier"),
            ("PUBLIC_LEFT_IMAGE", "public_left_associated_image_frontier"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(live[key]["proposal_count"]))
        print(prefix + "LEFT_FACTOR_RULE=" + live["left_factor_root_rule"])
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

### `tests/test_rule.py`

```python
"""Focused proof contracts for generic composition reassociation."""
from __future__ import annotations

import pytest

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase169_r10e5_composite_generator_image.rule import expand_composite_generator_image
from phase174_r3_r7_r9_composition_associativity.rule import (
    RULE_NAME,
    expand_generator_image_associativity,
    generator_image_associativity_inputs,
    generator_image_associativity_rule,
    right_associated_composition,
    typed_composition_factors,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule,
)


def element(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(name, target, source=source, target=target)


def sample(sphere: int = 5) -> tuple[GeneratorImage, GeneratorImage]:
    source_f = element("f", sphere + 3, sphere)
    source_g = element("g", sphere + 4, sphere + 3)
    source_h = element("h", sphere + 5, sphere + 4)
    target_f = element("Ef", sphere + 4, sphere + 1)
    target_g = element("Eg", sphere + 5, sphere + 4)
    target_h = element("Eh", sphere + 6, sphere + 5)
    source = Composition(source_f, Composition(source_g, source_h))
    target_left = Composition(Composition(target_f, target_g), target_h)
    target_right = Composition(target_f, Composition(target_g, target_h))
    mapping = TodaSuspensionMap(
        TodaPrimaryGroup(sphere + 5, sphere),
        TodaPrimaryGroup(sphere + 6, sphere + 1),
    )
    return (
        GeneratorImage(mapping, source, target_left),
        GeneratorImage(mapping, source, target_right),
    )


@pytest.mark.parametrize("sphere", (3, 5, 9, 17))
def test_generic_reassociation_preserves_factors_and_map(sphere: int) -> None:
    left, right = sample(sphere)
    normalized = right_associated_composition(left.target_generator)
    assert normalized == right.target_generator
    assert typed_composition_factors(normalized) == typed_composition_factors(left.target_generator)
    assert generator_image_associativity_inputs(left) == (right,)
    choices = expand_generator_image_associativity(left)
    assert len(choices) == 1
    assert isinstance(choices[0], GoalExpansion)
    assert choices[0].subgoals == (right,)
    assert choices[0].rule.name == RULE_NAME


def test_prior_composite_rule_requires_matching_parentheses() -> None:
    left, right = sample()
    assert expand_composite_generator_image(left) == ()
    options = expand_composite_generator_image(right)
    assert len(options) == 1
    assert len(options[0].subgoals) == 2
    assert all(isinstance(child, GeneratorImage) for child in options[0].subgoals)


def test_inferred_premise_derives_exact_original_goal_and_preserves_tree() -> None:
    left, right = sample()
    rule = generator_image_associativity_rule(left)
    inferred = ProofStep(
        conclusion=right,
        premises=(),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only independently proved image"),
    )
    matches = find_inference_matches_for_rule(rule, (inferred,))
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.conclusion == left
    assert result.premises == (inferred,)
    assert result.inference_rule is rule
    assert result.rule is ProofRule.INFERENCE


def test_given_and_unproved_image_do_not_close_goal() -> None:
    left, right = sample()
    rule = generator_image_associativity_rule(left)
    given = ProofStep(right, (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (given,)) == ()
    assert find_inference_matches_for_rule(rule, ()) == ()


def test_unrelated_or_wrong_map_does_not_close_goal() -> None:
    left, right = sample()
    rule = generator_image_associativity_rule(left)
    unrelated = sample(6)[1]
    premise = ProofStep(
        unrelated, (), ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only unrelated evidence"),
    )
    assert find_inference_matches_for_rule(rule, (premise,)) == ()
    wrong_source = GeneratorImage(right.map, unrelated.source_generator, right.target_generator)
    proof = ProofStep(
        wrong_source, (), ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only wrong source"),
    )
    assert find_inference_matches_for_rule(rule, (proof,)) == ()


def test_right_associated_goal_is_not_reexpanded_into_itself() -> None:
    left, right = sample()
    assert generator_image_associativity_inputs(right) is None
    assert expand_generator_image_associativity(right) == ()
    assert right_associated_composition(left.target_generator) == right.target_generator


def test_wrong_suspension_dimensions_are_rejected() -> None:
    left, right = sample()
    wrong = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 8)),
        left.source_generator, left.target_generator,
    )
    assert expand_generator_image_associativity(wrong) == ()
    assert expand_generator_image_associativity(object()) == ()
    assert expand_generator_image_associativity(GeneratorImage(
        "E", left.source_generator, left.target_generator,
    )) == ()


def test_composition_with_bad_endpoint_is_rejected() -> None:
    a = element("a", 9, 6)
    b = element("b", 12, 10)
    c = element("c", 13, 12)
    bad = Composition(Composition(a, b), c)
    assert typed_composition_factors(bad) is None
    assert right_associated_composition(bad) is None
    assert right_associated_composition(a) is None
    assert right_associated_composition(Composition(a, b)) is None


def test_zero_and_non_map_factors_are_rejected() -> None:
    left, right = sample()
    assert typed_composition_factors(Zero()) is None
    bad = GeneratorImage(
        left.map, left.source_generator,
        Composition(Composition(Zero(), right.target_generator.left),
                    right.target_generator.right),
    )
    assert expand_generator_image_associativity(bad) == ()


def test_isolated_rule_does_not_fabricate_any_proof_step() -> None:
    left, right = sample()
    choices = expand_generator_image_associativity(left)
    assert len(choices) == 1
    assert not any(isinstance(child, ProofStep) for child in choices[0].subgoals)
    assert left not in choices[0].subgoals
    assert choices[0].subgoals == (right,)
```

### `tests/test_audit.py`

```python
"""Source-first, prior-evidence and SHA guards for the R9 audit."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r9_composition_associativity.audit import (
    REVIEWED_HEAD, SOURCE_BLOBS, TODA_CLAUSES,
    accepted_source_blob, git_blob_sha, validate_r8_evidence,
    verify_git_and_sources,
)


def sample_r8() -> dict:
    return {
        "phase": "174-R3-R7-R8",
        "gate": "PASS_READ_ONLY_COMPOSITE_IMAGE_GAP_DIAGNOSIS",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "public_composite_image_frontier": {"proposal_count": 0},
            "public_left_factor_zero_frontier": {"proposal_count": 1},
            "public_generator_zero_frontier": {"proposal_count": 0},
            "existing_composite_image_rule_candidate_count": 0,
            "left_factor_rule_name": "equality symmetry",
            "source_generator_type": "Composition",
            "public_provider_unchanged": True,
            "source_claim_promoted_to_given": False,
        },
    }


def test_r8_observed_evidence_is_not_promoted_to_proof() -> None:
    verified = validate_r8_evidence(sample_r8())
    assert verified["previous_composite_options"] == 0
    assert verified["previous_left_factor_rule_is_symmetry_only"]
    assert verified["prior_completion_claimed"] is False


@pytest.mark.parametrize("change", (
    "gate", "given", "production", "unproved", "left_factor_rule", "generator_type",
))
def test_r8_contract_fails_closed(change: str) -> None:
    report = sample_r8()
    if change == "gate":
        report["gate"] = "PASS_PREFLIGHT"
    elif change == "given":
        report["new_group_given"] = 1
    elif change == "production":
        report["new_production_inference_rules"] = 1
    elif change == "unproved":
        report["live"]["source_claim_promoted_to_given"] = True
    elif change == "left_factor_rule":
        report["live"]["left_factor_rule_name"] = "unverified source direct GIVEN"
    else:
        report["live"]["source_generator_type"] = "Other"
    with pytest.raises(RuntimeError):
        validate_r8_evidence(report)


@pytest.mark.parametrize("key,count", (
    ("public_composite_image_frontier", 1),
    ("public_left_factor_zero_frontier", 0),
    ("public_generator_zero_frontier", 1),
))
def test_prior_candidate_counts_are_not_guessed(key: str, count: int) -> None:
    report = sample_r8()
    report["live"][key]["proposal_count"] = count
    with pytest.raises(RuntimeError, match="observed frontier changed"):
        validate_r8_evidence(report)


def test_full_sha_guard_accepts_crlf_only_and_rejects_truncation() -> None:
    source = b"A\nB\n"
    sha = git_blob_sha(source)
    assert accepted_source_blob(source, sha)
    assert accepted_source_blob(b"A\r\nB\r\n", sha)
    assert not accepted_source_blob(b"A\nC\n", sha)
    assert not accepted_source_blob(source, sha[:-1])
    assert all(len(value) == 40 for value in SOURCE_BLOBS.values())
    assert len(REVIEWED_HEAD) == 40


def test_toda_annihilator_and_generator_suspension_are_separate_claims() -> None:
    assert "n\\ge6" in TODA_CLAUSES["general_annihilator"]
    assert "nu_6" in TODA_CLAUSES["generator_suspension"]
    assert TODA_CLAUSES["zero_image_conclusion"] == r"E\pi_{10}^5=0"


def test_audit_has_no_production_mutation_methods() -> None:
    path = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "verify_git_and_sources" in names
    assert "inspect_rebracketing_frontier" in names
    assert not {"patch", "install", "register_given", "change_public_provider"} & names


def test_source_guard_rejects_any_unreviewed_head_before_reading_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import phase174_r3_r7_r9_composition_associativity.audit as mod

    def fake_git(*args: str, cwd: Path = tmp_path) -> str:
        answers = {
            ("rev-parse", "--show-toplevel"): str(tmp_path),
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): "a" * 40,
            ("ls-remote", "origin", "refs/heads/develop"):
                "a" * 40 + "\trefs/heads/develop",
        }
        if args not in answers:
            raise AssertionError("Unexpected call to git " + repr(args))
        return answers[args]

    monkeypatch.setattr(mod, "git", fake_git)
    with pytest.raises(RuntimeError, match="Unreviewed develop HEAD"):
        verify_git_and_sources(tmp_path)
```

### `__init__.py`

```python
"""Phase 174 R3-R7-R9: isolated composition-associativity proof obligation."""
```

### `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PriorPythonPath = $env:PYTHONPATH
$PriorNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # A separate pytest process per Phase avoids test_audit.py basename collisions.
    # Prepend mode avoids the repository's file/directory import-name collisions.
    $Groups = @(
        @{ Name = 'R9'; Paths = @(
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py',
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_audit.py'
        ) },
        @{ Name = 'R8'; Paths = @(
            '.\phase174_r3_r7_r8_composite_image_gap\tests\test_audit.py'
        ) },
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
                throw "Missing focused test file: $TestPath"
            }
        }
    }

    Write-Output 'PHASE174_R3R7R9_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R9_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R9 $($Group.Name) pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R9_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r9_composition_associativity.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r9_composition_associativity.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R9 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PriorPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PriorNoBytecode
    Pop-Location
}
```

### `README.md`

```markdown
# Phase 174 R3-R7-R9 — Typed Composition Associativity Preflight

This package audits a structural mismatch between a right-associated database generator and a left-associated Toda composition. The new, isolated inference rule transports **only a separately proved generator image** through reassociation of composition; it does not supply any new reference fact, group result, or proof tree leaf.

## Files

- `rule.py`: generic, source-independent reassociation rule with one certified child obligation.
- `audit.py`: source-first GitHub HEAD and pinned-blob checks, certified R8 evidence, and live provider diagnostics.
- `tests/test_rule.py`: algebraic and negative-case checks.
- `tests/test_audit.py`: source, prior-report, and fail-closed SHA checks.
- `run.ps1`: dry run and full read-only audit, each with focused tests in independent pytest processes.
- `AUDIT_PLAN_JA.md`: Japanese review plan.
- `CODE_FULL_JA.md`: complete code and test listings.

## Running

Extract `R9.zip` into the root of a checked-out `develop` branch of `akebono03/ehp-proof-tracer`. The exact audited HEAD is `15785b921c15a19810b2b067715832ee20c61280`. Previously generated R8 evidence must exist at `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r8\composite_image_gap.json`.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r9_composition_associativity\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r9_composition_associativity\run.ps1"
```

The report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r9\composition_associativity.json`. Production inference providers, the database, the web renderer and existing tests are not modified. A candidate is not a proof. Full pytest is deferred until the end of Phase 174.
```

### `AUDIT_PLAN_JA.md`

```markdown
# Phase 174 R3-R7-R9 — 合成の結合律と型付き証明義務

## 監査済み現行状態

2026-11-06、GitHub `akebono03/ehp-proof-tracer` の `develop` HEAD `15785b921c15a19810b2b067715832ee20c61280` を確認。R8R1 は限定 pytest 175 PASS、Source Guard PASS、本監査 PASS。既存の合成懸垂推論は0候補、左因子零関係の公開候補は `equality symmetry` のみ。

## 変更対象と実装位置

新規ディレクトリ `phase174_r3_r7_r9_composition_associativity/` のみ。既存の Python ファイル・テスト・共通5文書は変更しない。

- `rule.py`：`typed_composition_factors()`、`right_associated_composition()`、`generator_image_associativity_inputs()`、`generator_image_associativity_rule()`、`expand_generator_image_associativity()` をこの順で追加。
- `audit.py`：GitHub HEAD / SHA 検査、Toda 転写確認、R8 JSON 検証、Source-first 公開候補の監査を新規追加。
- `tests/test_rule.py`、`tests/test_audit.py`：全テスト関数を新規追加。
- `run.ps1`：別プロセス pytest で同名テストの収集衝突を回避する。
- `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`：新規追加。README は英語。

## 数学的推論と未証明部分

結合律により `(a∘b)∘c = a∘(b∘c)`。この恒等式は合成の括弧付けだけを変え、因子・順序・次元は保持する。`GeneratorImage(E, g, a∘(b∘c))` を独立して証明できた場合に限り、`GeneratorImage(E, g, (a∘b)∘c)` を推論する。

Toda Proposition 5.9 の採用転写には一般関係式 `(5.9)` と生成元の懸垂像が含まれるが、転写確認は引用の証明木を完成させない。`ν₆∘η₉=0` は、等式の対称性を1回適用しただけでは証明されない。

## Gate と次段階

- GitHub の検査済みコミット以外を拒否。全文 SHA-1 の桁不足を拒否し、LF / CRLF のみ正規化する。
- R8 完了 JSON を厳密に照合し、Source-first の既存公開 provider を変更しない。
- 結合律候補の数、括弧整合化後の既存合成規則候補、未解決の因子画像 Goal を記録する。
- 新規 GIVEN 0、production ルール追加 0、全体 pytest 不実施。

次段階 R10 は、R9 の実測値から独立した `GeneratorImage` 子 Goal と Toda (5.9) の引用付き零関係を監査する。`π₁₂⁷=0` の complete は宣言しない。
```

## 変更一覧と完了条件

- 新規独立一般規則と監査のみ。既存 API・テスト・本番 provider・Web・共通5文書は変更しない。
- 実行する pytest：`run.ps1` に記載した R9/R8/R7/R6/R5/R4/R3/数学的回帰の8グループ。
- 完了条件：Source Guard、限定 pytest、DryRun・本監査が PASS し、再結合前後の候補数が JSON に残る。
- 次段階 R10：合成の各因子の懸垂像および Toda (5.9) に基づく零関係の出典接続。R9 では先取りしない。
- 全体 pytest は Phase 174 終了時のみ。
