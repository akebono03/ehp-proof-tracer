# R32 — 変更・追加コード全文

既存ファイルの変更はありません。以下は新規ファイルの全内容です。

## `kernel_contract.py`

```python
"""R32 read-only contract for a conditional free-to-finite cyclic Delta kernel.

This is NOT a production InferenceRule or a provider. Nothing here certifies
its three independent mathematical premises or creates a ProofStep.
"""
from __future__ import annotations

from expression import HomotopyElement
from homotopy_groups import (
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
)
from map_facts import EHP_DELTA_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from proof import Relation, RelationType
from toda_rules import (
    TodaDeltaImageUpToSignStatement,
    TodaProp42ExactnessStatement,
)


def valid_ehp_lower_delta(delta: object) -> bool:
    """Reject map-shaped objects with invalid EHP H-Delta dimensions."""
    if type(delta) is not TodaDeltaMap:
        return False
    a, b = delta.source_group, delta.target_group
    if type(a) is not TodaPrimaryGroup or type(b) is not TodaPrimaryGroup:
        return False
    q, n = b.group_dimension, b.sphere_dimension
    if (type(q) is not int or type(n) is not int or n < 2 or q < n
            or a != TodaPrimaryGroup(q + 2, 2 * n + 1)):
        return False
    window = TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(q + 2, n + 1),
        middle_term=a,
        target_term=b,
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
    )
    return prop42_exactness_indices(TodaProp42ExactnessStatement(window)) == (
        n, q + 2, "h_delta",
    )


def generator_has_group_coordinates(element: object, group: TodaPrimaryGroup) -> bool:
    """Accept only typed homotopy elements of precisely the requested group."""
    return (
        type(element) is HomotopyElement
        and type(element.source) is int
        and type(element.target) is int
        and element.source == group.group_dimension
        and element.target == group.sphere_dimension
    )


def conditional_kernel_premises(
    goal: object,
    domain_presentation: object,
    codomain_presentation: object,
    signed_generator_image: object,
) -> tuple[Relation, Relation, TodaDeltaImageUpToSignStatement] | None:
    """Check the hypotheses of ker(Delta)=<m*g>; never prove them.

    A group homomorphism Z{g} -> Z/m{h} with Delta(g)=+/-h has kernel
    <m*g>. Signed generator equality is exact: no symbolic normalization,
    group identification, unverified database reuse, or dimension guessing.
    """
    if type(goal) is not KernelMultipleStatement:
        return None
    delta = goal.map
    if not valid_ehp_lower_delta(delta) or goal.domain != delta.source_group:
        return None
    if (type(domain_presentation) is not Relation
            or domain_presentation.relation_type is not RelationType.EQUALITY
            or domain_presentation.lhs != delta.source_group
            or type(domain_presentation.rhs) is not FreeCyclicGroup):
        return None
    generator = domain_presentation.rhs.generator
    if (not generator_has_group_coordinates(generator, delta.source_group)
            or generator != goal.source_generator):
        return None
    if (type(codomain_presentation) is not Relation
            or codomain_presentation.relation_type is not RelationType.EQUALITY
            or codomain_presentation.lhs != delta.target_group
            or type(codomain_presentation.rhs) is not FiniteCyclicGroup):
        return None
    target_group = codomain_presentation.rhs
    if (type(target_group.order) is not int or target_group.order < 1
            or goal.multiple != target_group.order
            or not generator_has_group_coordinates(
                target_group.generator, delta.target_group,
            )):
        return None
    if (type(signed_generator_image) is not TodaDeltaImageUpToSignStatement
            or signed_generator_image.map != delta
            or signed_generator_image.element != generator
            or signed_generator_image.positive_value != target_group.generator):
        return None
    return domain_presentation, codomain_presentation, signed_generator_image


def signed_cyclic_kernel_membership(
    order: int, coefficient: int, sign: int,
) -> bool:
    """Arithmetic check supporting the conditional lemma, not a proof step."""
    if (type(order) is not int or order < 1
            or type(coefficient) is not int or type(sign) is not int
            or sign not in (-1, 1)):
        raise ValueError("requires a positive order, integer coefficient, and sign +/-1")
    return (sign * coefficient) % order == 0
```

## `audit.py`

```python
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
    if head != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Local/remote develop advanced; review before running R32")
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
```

## `tests/test_kernel_contract.py`

```python
"""R32 isolated conditional kernel contract, no fabricated certified proof."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import (
    FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup,
)
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import (
    conditional_kernel_premises, generator_has_group_coordinates,
    signed_cyclic_kernel_membership, valid_ehp_lower_delta,
)
from proof import Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


def fixture(q: int = 9, n: int = 5, order: int = 2):
    delta = TodaDeltaMap(TodaPrimaryGroup(q + 2, 2 * n + 1), TodaPrimaryGroup(q, n))
    g = HomotopyElement("g", q + 2, q + 2, 2 * n + 1, GeneratorSymbol("g", n))
    h = HomotopyElement("h", q, q, n, GeneratorSymbol("h", n))
    goal = KernelMultipleStatement(delta, delta.source_group, g, order)
    domain = Relation(delta.source_group, FreeCyclicGroup(g), RelationType.EQUALITY)
    codomain = Relation(delta.target_group, FiniteCyclicGroup(order, h), RelationType.EQUALITY)
    signed = TodaDeltaImageUpToSignStatement(delta, g, h)
    return goal, domain, codomain, signed


@pytest.mark.parametrize("q,n,order", ((9, 5, 2), (11, 6, 4), (13, 7, 3), (17, 9, 8)))
def test_generic_well_typed_finite_cyclic_kernel_hypotheses(q: int, n: int, order: int):
    goal, source, target, signed = fixture(q, n, order)
    assert valid_ehp_lower_delta(goal.map)
    assert conditional_kernel_premises(goal, source, target, signed) == (
        source, target, signed,
    )


@pytest.mark.parametrize("order", (1, 2, 3, 4, 8, 13))
def test_cyclic_kernel_arithmetic_for_positive_and_negative_signs(order: int):
    for coefficient in range(-3 * order - 1, 3 * order + 2):
        for sign in (-1, 1):
            assert signed_cyclic_kernel_membership(order, coefficient, sign) == (
                coefficient % order == 0
            )


@pytest.mark.parametrize("bad", ((0, 0, 1), (-1, 2, 1), (2, True, 1),
                                      (2, 2, 0), (2, 2, 3), (2, 2, True),
                                      (2, 2.5, 1), (True, 2, 1)))
def test_arithmetic_rejects_untyped_inputs(bad):
    with pytest.raises(ValueError):
        signed_cyclic_kernel_membership(*bad)


def test_incorrect_map_dimensions_and_fake_map_rejected():
    goal, source, target, signed = fixture()
    assert not valid_ehp_lower_delta(TodaDeltaMap(
        TodaPrimaryGroup(12, 11), goal.map.target_group,
    ))
    assert not valid_ehp_lower_delta("Delta")
    assert not valid_ehp_lower_delta(TodaDeltaMap(
        TodaPrimaryGroup(5, 3), TodaPrimaryGroup(3, 1),
    ))
    wrong = replace(goal, map=TodaDeltaMap(
        TodaPrimaryGroup(12, 11), goal.map.target_group,
    ))
    assert conditional_kernel_premises(wrong, source, target, signed) is None


def test_wrong_kernel_multiple_is_rejected():
    goal, source, target, signed = fixture(order=4)
    assert conditional_kernel_premises(replace(goal, multiple=2), source, target, signed) is None


def test_source_generator_and_source_group_must_match_exactly():
    goal, source, target, signed = fixture()
    other = HomotopyElement("g-prime", 11, 11, 11)
    wrong = replace(source, rhs=FreeCyclicGroup(other))
    assert conditional_kernel_premises(goal, wrong, target, signed) is None
    assert conditional_kernel_premises(goal, replace(source, lhs=TodaPrimaryGroup(10, 10)),
                                       target, signed) is None
    assert conditional_kernel_premises(replace(goal, domain=TodaPrimaryGroup(10, 10)),
                                       source, target, signed) is None


def test_target_must_be_finite_cyclic_with_exact_generator():
    goal, source, target, signed = fixture()
    wrong_gen = HomotopyElement("h-other", 9, 9, 5)
    assert conditional_kernel_premises(goal, source, replace(target, rhs=FiniteCyclicGroup(2, wrong_gen)),
                                       signed) is None
    assert conditional_kernel_premises(goal, source, replace(target, rhs=FreeCyclicGroup(wrong_gen)),
                                       signed) is None
    assert conditional_kernel_premises(goal, source, replace(target, lhs=TodaPrimaryGroup(9, 6)),
                                       signed) is None
    assert conditional_kernel_premises(goal, source, replace(target, rhs=FiniteCyclicGroup(2, Zero())),
                                       signed) is None


def test_signed_generator_witness_must_be_exact_map_and_elements():
    goal, source, target, signed = fixture()
    wrong_source = HomotopyElement("g-other", 11, 11, 11)
    wrong_target = HomotopyElement("h-other", 9, 9, 5)
    for bad in (replace(signed, element=wrong_source),
                replace(signed, positive_value=wrong_target),
                replace(signed, map=TodaDeltaMap(TodaPrimaryGroup(13, 13), TodaPrimaryGroup(11, 6)))):
        assert conditional_kernel_premises(goal, source, target, bad) is None
    assert conditional_kernel_premises(goal, source, target, "(5.10)") is None


def test_wrong_relation_kind_and_untyped_element_rejected():
    goal, source, target, signed = fixture()
    assert conditional_kernel_premises(goal, replace(source, relation_type=RelationType.ORDER),
                                       target, signed) is None
    assert conditional_kernel_premises(goal, source, replace(target, relation_type=RelationType.ORDER),
                                       signed) is None
    assert not generator_has_group_coordinates(Zero(), goal.map.target_group)
    assert not generator_has_group_coordinates(
        HomotopyElement("wrong-degree", 9, 11, 5), goal.map.target_group,
    )


def test_no_raw_goal_is_accepted_as_source_evidence():
    goal, source, target, signed = fixture()
    assert conditional_kernel_premises(goal, goal, target, signed) is None
    assert conditional_kernel_premises(goal, source, goal, signed) is None
    assert conditional_kernel_premises(goal, source, target, goal) is None
```

## `tests/test_audit.py`

```python
"""R32 source-first audit and non-completion contract."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r32_lower_delta_kernel_audit.audit import (
    EQ510, EQ510_IMAGE, PINS, PROP58, PROP58_CODOMAIN, PROP59,
    R31_AUDIT, R31_SHA256, ROOT, SOURCE, git_blob_sha,
    inspect_toda_citations, inspect_typed_contract, matches_pin, report,
    verify_checkout,
)


def test_local_source_guard_respects_r30_and_r31():
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["r30_preserved"] is True
    assert state["r31_preserved"] is True
    assert state["tracked_changes"] == 0
    assert (ROOT / R31_AUDIT).exists()
    assert len(R31_SHA256) == 64


def test_source_pins_allow_whole_file_crlf_but_no_mutations():
    for file, sha in PINS.items():
        assert matches_pin((ROOT / file).read_bytes(), sha)
    original = b"a\nb\n"
    assert matches_pin(original.replace(b"\n", b"\r\n"), git_blob_sha(original))
    assert not matches_pin(b"different", git_blob_sha(original))


def test_toda_prior_statements_precede_proposition_59():
    source = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    info = inspect_toda_citations(source)
    assert info["prop58_codomain_precedes_prop59"] is True
    assert info["equation_510_precedes_prop59"] is True
    assert info["prop59_kernel_is_derived_not_given"] is True
    assert info["printed_claim_is_verified_proof_step"] is False
    assert source.index(PROP58) < source.index(EQ510) < source.index(PROP59)


def test_source_mutations_are_not_misread_as_proof():
    source = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    for marker in (PROP58_CODOMAIN, EQ510_IMAGE):
        altered = source.replace(marker, "NOT_CERTIFIED_SOURCE", 1)
        with pytest.raises(ValueError):
            inspect_toda_citations(altered)


def test_general_kernel_is_conditional_and_db_prior_not_literature():
    info = inspect_typed_contract()
    assert info["conditional_premise_types"] == [
        "Relation", "Relation", "TodaDeltaImageUpToSignStatement",
    ]
    assert info["hypothetical_premises_not_certified"] is True
    assert info["db_prior_is_independent_literature_reference"] is False
    assert info["general_rule_registered"] is False
    assert info["kernel_direct_given_inserted"] is False


def test_public_source_screen_cannot_insert_kernel_or_root_given():
    result = report(dry_run=False)
    assert result["screened"]["screened_direct_kernel_given"] == 0
    assert result["screened"]["screened_direct_root_given"] == 0
    assert result["new_givens"] == 0
    assert result["new_rules"] == 0
    assert result["production_files_changed"] == 0
    assert result["lower_delta_kernel_proved"] is False
    assert result["delta_surjectivity_proved"] is False
    assert result["root_complete"] is False
    assert result["full_pytest"] is False
    assert result["gate"].endswith("TYPED_PROOF_PENDING")


def test_r32_dry_run_keeps_proof_unfinished():
    r = report(dry_run=True)
    assert r["typed"] is None
    assert r["screened"] is None
    assert r["lower_delta_kernel_proved"] is False
    assert r["root_complete"] is False
    assert r["gate"] == "PASS_R32_SOURCE_PREFLIGHT_ONLY"
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r32_lower_delta_kernel_audit.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R32 Source Guard / DryRun failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R32_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m phase174_r3_r7_r32_lower_delta_kernel_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R32 conditional mathematical audit failed' }

$Groups = @(
    @{ Name='R32_CONTRACT'; Files=@('.\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_kernel_contract.py') },
    @{ Name='R32_AUDIT'; Files=@('.\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_audit.py') },
    @{ Name='R31_REGRESSION'; Files=@('.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_audit.py', '.\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_static_helpers.py') },
    @{ Name='R18_SURJECTIVITY'; Files=@('.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py') },
    @{ Name='R5_HOPF_INJECTIVITY'; Files=@('.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py') }
)
foreach ($Group in $Groups) {
    Write-Output ('PHASE174_R3R7R32_TEST_GROUP=' + $Group.Name)
    & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider @($Group.Files)
    if ($LASTEXITCODE -ne 0) { throw ('R32 focused pytest failed: ' + $Group.Name) }
}

Write-Output 'PHASE174_R3R7R32_RUN=PASS'
Write-Output 'PHASE174_R3R7R32_FULL_PYTEST=False'
Write-Output '(END)'
```

## `README.md`

```markdown
# Phase 174 R3-R7-R32 — Lower Delta Kernel General Audit

This package performs a **read-only, source-first audit** of the conditional
free-to-finite cyclic kernel computation for the lower EHP Delta map. It does
not modify the production search, registry, renderer, database, or source files.
It creates no GIVEN, verified ProofStep, or registered mathematical rule.

## Reviewed baseline

- Repository: `akebono03/ehp-proof-tracer`, branch `develop`.
- Reviewed GitHub HEAD: `25118e281445ca17b30c60c8fd02d00acaa25ea5`.
- R30's ten-line shared-provider change is already merged at this HEAD.
- The R31 audit package must be retained unchanged, whether untracked or
  otherwise locally available. No reset, checkout, or write to R31 occurs.

## Mathematical contract

For a genuine homomorphism of abelian groups

`Delta: Z{g} -> (Z/m){h}`, with `m >= 1` and `Delta(g) = +/- h`, the kernel
is `<m*g>`. All three mathematical premises require independent proof. The
reviewed source states the finite codomain in Toda Proposition 5.8 and the
image of the diagonal generator in equation (5.10); the kernel mentioned in
Proposition 5.9 is a **consequence**, never a new premise.

R32 does not claim that these textual statements are certified typed proof
steps in the public search. A database prior, if found, is reported as such
and is not silently treated as a literature citation.

## Install and run

Extract the ZIP directly into the existing repository root. In Windows
PowerShell, run the following commands from the root directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r32_lower_delta_kernel_audit\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r32_lower_delta_kernel_audit\run.ps1'
```

The complete PowerShell command including exit-code checks is included in
`AUDIT_PLAN_JA.md`. The normal run performs Source Guard, a report-only
source/proof-frontier audit, and five groups of **focused** pytest runs.
The full test suite is intentionally not run.

Reports are written outside the Git working tree to
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r32\`.

## Success and non-claims

A successful R32 audit establishes only the validity of the **conditional**
cyclic-kernel reasoning and the integrity of the inspected source evidence.
It leaves the lower Delta kernel, upper Delta surjectivity, and target group
zero statement **unproved**. A changed GitHub HEAD or modified pinned source
must halt the audit for review rather than be reset or overwritten.
```

