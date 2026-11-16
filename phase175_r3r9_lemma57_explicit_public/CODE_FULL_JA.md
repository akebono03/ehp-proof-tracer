# Phase 175 R3R9 — 変更コード全文

GitHub の現行 `develop` と関連テストを実装前に確認した。既存コードの差し替え対象は `phase165_r52_r9_shared_math.py` の `search_shared_group_goal()` 全体のみ。トップレベル import の変更なし。新規クラス・関数・テストは以下に列挙する各**新規ファイル内**に配置する。

新規パッケージのコードは全ファイル全文を掲載する。既存のトップレベル `README.md`・`design.md`・`development_log.md`・`roadmap.md`・`proof_records.md` は今回変更しない。

## 既存関数全文（置き換え用）: search_shared_group_goal_FULL.py.txt

```python
def search_shared_group_goal(*, n: int, k: int, group_structure: object,
                              bridge: RegistryBridgeResult | None = None,
                              expansion_provider=None,
                              citing_assertion_id: str | None = None,
                              verified_assertion_ids: tuple[str, ...] = (), completed_internal_proofs: tuple = (), proof_use_order=None,
                              ordered_completed_proofs: tuple = (), target_order: int | None = None,
                              proof_order_catalog=None, recursive_proof_order_catalog=None, context_sink=None):
    """Run canonical search under a screened Reference context.

    Older calls retain their signature. R15 ordering is applied to sources
    outside the explicitly adopted-Tex policy; no IDs are auto-verified.
    """
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r57_r12_ordered_proofs import validate_prior_internal_proofs

    goal = Relation(TodaPrimaryGroup(n + k, n), group_structure)
    if proof_order_catalog is not None and recursive_proof_order_catalog is None:
        from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
        if not isinstance(proof_order_catalog, ProofOrderCatalog):
            raise TypeError("proof_order_catalog must be ProofOrderCatalog")
        if ordered_completed_proofs or completed_internal_proofs or target_order is not None:
            raise ValueError("catalog proof order cannot mix with caller-supplied proofs")
        if any(record.completed is not None for record in proof_order_catalog._records):
            raise ValueError("on-demand mode forbids registered completed proofs")
        recursive_proof_order_catalog = proof_order_catalog
        proof_order_catalog = None
    if recursive_proof_order_catalog is not None:
        from phase165_r57_r14_recursive_search import search_recursively_in_proof_order
        if (proof_order_catalog is not None or ordered_completed_proofs
                or completed_internal_proofs or target_order is not None):
            raise ValueError("recursive proof order cannot mix with saved or caller-supplied proofs")

        def search_one(statement, earlier, order):
            if (not isinstance(statement, Relation)
                    or not isinstance(statement.lhs, TodaPrimaryGroup)
                    or statement.relation_type is not RelationType.EQUALITY):
                raise TypeError("recursive catalog targets must be typed group relations")
            target = statement.lhs
            if (not isinstance(target.group_dimension, int)
                    or not isinstance(target.sphere_dimension, int)
                    or target.sphere_dimension < 2
                    or target.group_dimension < target.sphere_dimension):
                raise ValueError("recursive target must have concrete dimensions")
            return search_shared_group_goal(
                n=target.sphere_dimension,
                k=target.group_dimension - target.sphere_dimension,
                group_structure=statement.rhs,
                bridge=bridge,
                expansion_provider=expansion_provider,
                citing_assertion_id=citing_assertion_id,
                verified_assertion_ids=verified_assertion_ids,
                completed_internal_proofs=(),
                proof_use_order=proof_use_order,
                ordered_completed_proofs=earlier,
                target_order=order,
                context_sink=context_sink if statement == goal else None,
            )

        return search_recursively_in_proof_order(
            recursive_proof_order_catalog, goal, search_one,
        )
    if proof_order_catalog is not None:
        from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
        if not isinstance(proof_order_catalog, ProofOrderCatalog):
            raise TypeError("proof_order_catalog must be ProofOrderCatalog")
        if ordered_completed_proofs or completed_internal_proofs or target_order is not None:
            raise ValueError("catalog proof order cannot be mixed with caller order")
        prior, target_order = proof_order_catalog.select_prior(goal)
    else:
        prior = validate_prior_internal_proofs(
            ordered_completed_proofs, target_order, completed_internal_proofs
        )
    if bridge is None:
        bridge = build_shared_typed_bridge()
    if n == 4 and k == 3 and expansion_provider is None:
        from phase173_r4_r1_public_connection.route import (
            prepare_pi74_public_connection,
        )
        pi74_connection = prepare_pi74_public_connection(
            bridge=bridge, goal=goal, citing_assertion_id=citing_assertion_id,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        if pi74_connection is not None:
            bridge, citing_assertion_id, expansion_provider = pi74_connection
    # R3R9: cite the explicit nu-prime consequence of Lemma 5.7.
    if n == 3 and k == 4 and expansion_provider is None:
        from phase175_r3r9_lemma57_explicit_public.route import (
            prepare_pi73_public_connection,
        )
        pi73_connection = prepare_pi73_public_connection(
            bridge=bridge, goal=goal, citing_assertion_id=citing_assertion_id,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        if pi73_connection is not None:
            bridge, citing_assertion_id, expansion_provider = pi73_connection
    if citing_assertion_id is not None and expansion_provider is None:
        from phase174_r3_r6_r2_prop44_lemma54.source import (
            attach_earlier_verified_lemma54,
        )
        bridge = attach_earlier_verified_lemma54(bridge, citing_assertion_id)
    assertions = tuple(bridge.registry._assertions.values())
    if not assertions:
        raise ValueError("shared typed registry is empty")
    context_id = citing_assertion_id or assertions[0].assertion_id
    if citing_assertion_id is None:
        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        proof_context = screen_independent_sources_for_derived_goal(
            bridge, goal=goal,
        )
    else:
        proof_context = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=context_id,
            verified_assertion_ids=verified_assertion_ids,
            explicit_publication_target=True,
        )
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    proof_context = prefer_universal_prop42_derivation(proof_context)
    # Phase 173 R4-R8: reuse only the three isolated, source-verified Toda (5.6) roots.
    if n == 4 and k in (4, 5, 6) and expansion_provider is None and citing_assertion_id is None:
        from phase173_r4_r8_public_connection.route import (
            prepare_pi4_higher_public_connection,
        )
        pi4_higher_connection = prepare_pi4_higher_public_connection(
            bridge=bridge, goal=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        if pi4_higher_connection is not None:
            proof_context, expansion_provider = pi4_higher_connection
    if context_sink is not None:
        context_sink(proof_context)
    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        # Every ordinary (nonzero) group search needs the same cited R53
        # source-bound kernel candidate already used by the zero-group route.
        # This is a candidate ordering wrapper, not a new premise or GIVEN.
        from phase174_r3_r7_r53_public_source_bound_kernel.provider import (
            build_public_source_bound_kernel_provider,
        )
        expansion_provider = build_public_source_bound_kernel_provider(
            expansion_provider, proof_context,
        )
    return search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=proof_context,
        citing_assertion_id=context_id,
        expansion_provider=expansion_provider,
        lookup_mode="typed_reference_publication" if citing_assertion_id is not None else "typed_reference",
        structure_status=GroupStructureStatus.UNKNOWN,
        completed_internal_proofs=prior,
    )
```

## 新規: source.py

```python
"""Quote the independently explicit nu-prime clause of Toda Lemma 5.7.

The cited source is a FIXED_STATEMENT, but it is not the generator-image
ProofStep or a group-structure theorem. A separately guarded extraction
inference must convert the cited clause to an ordinary GeneratorImage.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from phase175_r3r6_lemma57_general.source import (
    MANIFEST,
    SOURCE_ID,
    SOURCE_SHA256,
    verify_lemma57_manifest,
)

REFERENCE_ID = "toda:175:r3r9:Lemma 5.7 explicit particular clause"
ASSERTION_ID = "toda:175:r3r9:lemma57:explicit_nu_prime_zero"
SOURCE_POSITION = 9100
PARTICULAR_CLAUSE = r"E(\eta_2\circ\nu')=0"


@dataclass(frozen=True)
class TodaLemma57ExplicitNuPrimeZero:
    """The source explicitly says 'in particular, E(eta_2 o nu') = 0'."""


def verify_explicit_lemma57_source(root: Path) -> dict[str, object]:
    """Check the reviewed source SHA, whole lemma and exact particular text.

    This verifies the project's adopted Japanese transcription, not an
    independently compared printed first edition of Toda's book.
    """
    root = Path(root)
    predecessor = verify_lemma57_manifest(root)
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8-sig"))
    rows = [
        row for row in manifest["assertions"]
        if row.get("reference_id") == "toda:Lemma 5.7"
    ]
    if len(rows) != 1:
        raise ValueError("R3R9_LEMMA57_SOURCE_NOT_UNIQUE")
    lemma = rows[0]
    source_text = lemma.get("source_text", "")
    if (
        lemma.get("statement_id") != SOURCE_ID
        or lemma.get("source_sha256") != SOURCE_SHA256
        or lemma.get("publication_position") != SOURCE_POSITION
        or lemma.get("review_needed") is not False
        or not isinstance(source_text, str)
        or "特に," not in source_text
        or source_text.count(PARTICULAR_CLAUSE) != 1
        or r"\Delta(\nu_5)=\pm(\eta_2\circ\nu')" not in source_text
    ):
        raise ValueError("R3R9_LEMMA57_PARTICULAR_CLAUSE_NOT_SOURCE_VERIFIED")
    return {
        "source": predecessor,
        "source_id": SOURCE_ID,
        "source_sha256": SOURCE_SHA256,
        "publication_position": SOURCE_POSITION,
        "particular_clause": PARTICULAR_CLAUSE,
        "new_group_given": 0,
        "particular_cited_source_count": 1,
    }


def build_explicit_lemma57_source(root: Path):
    """Create one verifiable source leaf, never a direct zero-image GIVEN."""
    from phase163_r4_registry_bridge import (
        MigrationRecord,
        MigrationStatus,
        RegistryBridgeResult,
    )
    from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
    from unified_statement_registry import (
        AssertionEntry,
        AssertionKind,
        AssertionOrigin,
        LiteratureEntry,
        ProofStepLink,
        ReferenceKind,
        UnifiedStatementRegistry,
    )

    verify_explicit_lemma57_source(root)
    claim = TodaLemma57ExplicitNuPrimeZero()
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.LEMMA,
        locator="Lemma 5.7",
        source_id=(
            "sources/toda/Toda_05_2.tex "
            "(adopted transcription; original printed edition not verified)"
        ),
        publication_position=SOURCE_POSITION,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=claim,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=(
            "explicit in-particular clause of Lemma 5.7 only",
            "no group-structure GIVEN, no direct GeneratorImage GIVEN",
        ),
    ))
    step = ProofStep(
        conclusion=claim,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Cited explicit nu-prime clause of Toda Lemma 5.7",
            literature_reference=LiteratureReference(
                label="Toda Lemma 5.7", locator="Lemma 5.7",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry=registry,
        records=(MigrationRecord(
            "phase175_r3r9", SOURCE_ID, ASSERTION_ID,
            MigrationStatus.STRUCTURED,
            "Source-verified explicit particular clause; image requires inference",
        ),),
        proof_links=(ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )
```

## 新規: rule.py

```python
"""Extract the explicit cited Lemma 5.7 consequence via an inference.

Unlike the conditional generalization of Lemma 5.7, this clause is stated
separately in the lemma itself. No Lemma 5.4 hypothesis is needed to quote it.
The two spellings of nu-prime are reconciled only by checked registered IDs.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = "extract explicit nu-prime zero-suspension clause of Toda Lemma 5.7"


def exact_lemma57_zero_image_goal(goal: object) -> bool:
    """Check the full map, zero, eta_2 and uniquely registered nu-prime ID."""
    if not isinstance(goal, GeneratorImage):
        return False
    expected_map = TodaSuspensionMap(
        TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3),
    )
    if goal.map != expected_map or not isinstance(goal.target_generator, Zero):
        return False
    if not isinstance(goal.source_generator, Composition):
        return False
    eta, nu_prime = goal.source_generator.left, goal.source_generator.right
    if typed_element_span(eta) != (3, 2) or typed_element_span(nu_prime) != (6, 3):
        return False
    eta_cited = HomotopyElement(
        "η₂", 2, source=3, target=2,
        generator=GeneratorSymbol("η", 2),
    )
    nu_cited = HomotopyElement(
        "ν′", 3, source=6, target=3,
        generator=GeneratorSymbol("ν", decoration="′"),
    )
    eta_match = eta == eta_cited or same_registered_group_presentation(
        FiniteCyclicGroup(2, eta), FiniteCyclicGroup(2, eta_cited),
    )
    nu_match = nu_prime == nu_cited or same_registered_group_presentation(
        FiniteCyclicGroup(4, nu_prime), FiniteCyclicGroup(4, nu_cited),
    )
    return bool(eta_match and nu_match)


def lemma57_explicit_zero_rule(goal: GeneratorImage) -> InferenceRule:
    """Require exactly the screened GIVEN for the lemma's explicit clause."""
    if not exact_lemma57_zero_image_goal(goal):
        raise ValueError("R3R9_GOAL_NOT_EXACT_LEMMA57_SPECIAL_CLAUSE")
    source = TodaLemma57ExplicitNuPrimeZero()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and not premises[0].premises
            and premises[0].conclusion == source
            and exact_lemma57_zero_image_goal(goal)
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "Read the independently explicit 'in particular' clause "
            "E(eta_2 o nu-prime)=0 from cited Toda Lemma 5.7. "
            "No Lemma 5.4 condition is needed at this citation boundary."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaLemma57ExplicitNuPrimeZero,
            statement_pattern=source,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_cited_lemma57_explicit_zero(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Offer one backward proposal; do not fabricate a completed ProofStep."""
    if (
        not isinstance(available, tuple)
        or available.count(TodaLemma57ExplicitNuPrimeZero()) != 1
        or not exact_lemma57_zero_image_goal(goal)
    ):
        return ()
    return (GoalExpansion(
        rule=lemma57_explicit_zero_rule(goal),
        subgoals=(TodaLemma57ExplicitNuPrimeZero(),),
    ),)
```

## 新規: route.py

```python
"""Public Group query route citing Lemma 5.7's explicit nu-prime clause.

Only the already registered pi_7^3 goal selects this routing module. All
mathematical rules for zero image, EHP exactness and Hopf lift remain the
shared generic rules. No direct goal GIVEN or specialized narrative is added.
"""
from __future__ import annotations

from pathlib import Path

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
    expand_hopf_injective_from_zero_image,
    hopf_injectivity_from_zero_image_inputs,
)
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
from phase175_r3r6_lemma57_general.source import merge_isolated_cited_source
from phase175_r3r8r1_verified_prior_public.rule import (
    expand_verified_prior_hopf_lift,
    expand_verified_prior_zero_image,
)
from phase175_r3r9_lemma57_explicit_public.rule import (
    exact_lemma57_zero_image_goal,
    expand_cited_lemma57_explicit_zero,
)
from phase175_r3r9_lemma57_explicit_public.source import (
    ASSERTION_ID,
    TodaLemma57ExplicitNuPrimeZero,
    build_explicit_lemma57_source,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def public_cited_ehp_extensions(
    available: tuple[object, ...], *, proof_target: object = None, bridge: object = None,
):
    """Place the citation extraction before generic EHP and Hopf proposals."""
    if available.count(TodaLemma57ExplicitNuPrimeZero()) != 1:
        raise ValueError("R3R9_REQUIRES_EXACTLY_ONE_CITED_LEMMA57_CLAUSE")

    def expand(statement: object):
        options = []
        options.extend(expand_cited_lemma57_explicit_zero(statement, available))
        if isinstance(statement, ImageZeroStatement):
            suspension = statement.map
            if isinstance(suspension, TodaSuspensionMap):
                domain, codomain = suspension.source_group, suspension.target_group
                if (
                    isinstance(domain, TodaPrimaryGroup)
                    and isinstance(codomain, TodaPrimaryGroup)
                    and type(domain.group_dimension) is int
                    and type(domain.sphere_dimension) is int
                    and codomain == TodaPrimaryGroup(
                        domain.group_dimension + 1, domain.sphere_dimension + 1,
                    )
                ):
                    n = domain.sphere_dimension
                    k = domain.group_dimension - n
                    prior = exact_prior_database_result(n, k)
                    if isinstance(prior, Relation) and prior.relation_type is RelationType.EQUALITY:
                        if proof_target is not None and bridge is not None:
                            options.extend(expand_verified_prior_zero_image(
                                statement, prior,
                                proof_target=proof_target, bridge=bridge,
                            ))
                        options.extend(expand_zero_image_from_cyclic_generator(
                            statement, prior,
                        ))
        options.extend(expand_hopf_injective_from_zero_image(statement))
        lifts = expand_cited_hopf_lift(statement, available)
        if proof_target is not None and bridge is not None:
            for lift in lifts:
                if len(lift.subgoals) != 3:
                    continue
                options.extend(expand_verified_prior_hopf_lift(
                    statement, lift.subgoals[1], lift.subgoals[2],
                    proof_target=proof_target, bridge=bridge,
                ))
        options.extend(lifts)
        return tuple(options)

    return expand


def prepare_pi73_public_connection(
    *, bridge, goal, citing_assertion_id, prior_conclusions: tuple,
):
    """Select the published clause; retain the ordinary typed proof resolver."""
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be tuple")
    if (
        not isinstance(goal, Relation)
        or goal.relation_type is not RelationType.EQUALITY
        or goal.lhs != TodaPrimaryGroup(7, 3)
    ):
        return None
    candidates = registered_group_goal_candidates(bridge, n=3, k=4)
    if len(candidates) != 1 or candidates[0] != goal:
        return None
    exact_id = resolve_specialized_goal_citing_id(bridge, goal)
    if not isinstance(exact_id, str) or not exact_id:
        return None
    if citing_assertion_id is not None and citing_assertion_id != exact_id:
        return None
    if ASSERTION_ID in bridge.registry._assertions:
        return None

    root = Path(__file__).resolve().parents[1]
    supplemental = build_explicit_lemma57_source(root)
    augmented = merge_isolated_cited_source(bridge, supplemental)
    if (
        ASSERTION_ID not in augmented.registry._assertions
        or not precedes_citing_assertion(augmented, ASSERTION_ID, exact_id)
    ):
        return None
    screened = prefer_universal_prop42_derivation(
        screen_shared_proof_context(
            augmented, goal=goal, citing_assertion_id=exact_id,
            explicit_publication_target=True,
        )
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    if (
        available.count(TodaLemma57ExplicitNuPrimeZero()) != 1
        or goal in available
    ):
        return None

    prior = exact_prior_database_result(2, 4)
    if (
        not isinstance(prior, Relation)
        or prior.lhs != TodaPrimaryGroup(6, 2)
    ):
        return None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    zero = GeneratorImage(e, prior.rhs.generator, Zero())
    if (
        not exact_lemma57_zero_image_goal(zero)
        or len(expand_cited_lemma57_explicit_zero(zero, available)) != 1
    ):
        return None
    structure = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    lifts = expand_cited_hopf_lift(structure, available)
    if len(lifts) != 1 or lifts[0].subgoals[0] is None:
        return None
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(lifts[0].subgoals[0])
    if hopf_inputs is None or hopf_inputs[0] != ImageZeroStatement(e):
        return None
    if len(expand_zero_image_from_cyclic_generator(hopf_inputs[0], prior)) != 1:
        return None
    if len(expand_verified_prior_zero_image(
        hopf_inputs[0], prior, proof_target=goal, bridge=screened,
    )) != 1:
        return None

    from phase165_r52_r9_shared_math import shared_expansion_provider

    ordinary = shared_expansion_provider(
        screened, proof_target=goal, prior_conclusions=prior_conclusions,
    )
    extensions = public_cited_ehp_extensions(
        available, proof_target=goal, bridge=screened,
    )

    def provider(statement: object):
        # First successful, cited proof wins. No proof step is imported.
        return extensions(statement) + ordinary(statement)

    return augmented, exact_id, provider
```

## 新規: install.py

```python
"""Replace exactly one reviewed public routing function with bytewise rollback.

The input is the audited R3R8R1R2 public-route function already committed to
develop; the only change is its Phase 175 pi73 route import and comment.
No top-level imports, mathematical rules or unrelated functions are modified.
"""
from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path
import subprocess

from phase175_r3r8r1_verified_prior_public.worktree_guard import (
    reviewed_tracked_snapshot,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = Path("phase165_r52_r9_shared_math.py")
PINNED_GIT_BLOB = "3426b223f94e839e77972801977d58a4ca182767"
PINNED_HEAD_ANCESTOR = "7171af968ba510291f87b8bb484d8718a3cef204"
OLD_ROUTE = (
    "    # R3R8R1: connect the R3R7 cited general EHP proof chain, not a saved result.\n"
    "    if n == 3 and k == 4 and expansion_provider is None:\n"
    "        from phase175_r3r8r1_verified_prior_public.route import (\n"
)
NEW_ROUTE = (
    "    # R3R9: cite the explicit nu-prime consequence of Lemma 5.7.\n"
    "    if n == 3 and k == 4 and expansion_provider is None:\n"
    "        from phase175_r3r9_lemma57_explicit_public.route import (\n"
)


def git(root: Path, *args: str) -> str:
    """Read Git metadata; never stage, reset, check out or commit."""
    if not args or args[0] not in {"rev-parse", "branch"}:
        raise ValueError("R3R9_GIT_READ_ONLY_OPERATION_REQUIRED")
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R3R9_GIT_READ_FAILED: " + " ".join(args))
    return result.stdout.strip()


def find_function(text: str) -> tuple[int, int]:
    """Get exact offsets for the sole top-level public search function."""
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        raise RuntimeError("R3R9_INVALID_REVIEWED_CODE_AST") from exc
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "search_shared_group_goal"]
    if len(matches) != 1:
        raise RuntimeError("R3R9_SEARCH_FUNCTION_NOT_UNIQUE")
    lines = text.splitlines(keepends=True)
    node = matches[0]
    return (
        sum(len(line) for line in lines[:node.lineno - 1]),
        sum(len(line) for line in lines[:node.end_lineno]),
    )


def replace_function_bytes(before: bytes, *, require_exact_template: bool = True) -> bytes:
    """Preserve all bytes outside one AST-reviewed function, including CRLF."""
    if before.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R9_UNEXPECTED_UTF8_BOM")
    original = before.decode("utf-8")
    newline = "\r\n" if "\r\n" in original else "\n"
    if "\r\n" in original and "\n" in original.replace("\r\n", ""):
        raise RuntimeError("R3R9_MIXED_NEWLINES")
    normalized = original.replace("\r\n", "\n")
    start, end = find_function(normalized)
    function = normalized[start:end]
    old_template = (PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    new_template = (PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    if (
        old_template.count(OLD_ROUTE) != 1
        or old_template.replace(OLD_ROUTE, NEW_ROUTE, 1) != new_template
        or new_template.count(NEW_ROUTE) != 1
    ):
        raise RuntimeError("R3R9_TEMPLATE_HAS_UNREVIEWED_EDIT")
    if require_exact_template and ast.dump(
        ast.parse(function), include_attributes=False,
    ) != ast.dump(ast.parse(old_template), include_attributes=False):
        raise RuntimeError("R3R9_SOURCE_FUNCTION_CHANGED_SINCE_REVIEW")
    if function.count(OLD_ROUTE) != 1:
        raise RuntimeError("R3R9_OLD_ROUTE_NOT_UNIQUE")
    candidate = normalized[:start] + new_template + normalized[end:]
    compile(candidate, str(TARGET), "exec")
    actual_old = OLD_ROUTE.replace("\n", newline)
    actual_new = NEW_ROUTE.replace("\n", newline)
    if original.count(actual_old) != 1:
        raise RuntimeError("R3R9_EOL_ANCHOR_CHANGED")
    return original.replace(actual_old, actual_new, 1).encode("utf-8")


def preflight(root: Path = ROOT) -> dict[str, object]:
    """Require committed reviewed baseline and no unrelated tracked edits."""
    root = Path(root).resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R3R9_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3R9_WRONG_BRANCH")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != PINNED_GIT_BLOB:
        raise RuntimeError("R3R9_BASE_PRODUCTION_BLOB_NOT_COMMITTED")
    # Prior package's guard allows its own known docs but NOT the production
    # target. This also rejects staging, unknown edits and dirty core files.
    prior_snapshot = reviewed_tracked_snapshot(root, allow_public_target=False)
    before = (root / TARGET).read_bytes()
    candidate = replace_function_bytes(before)
    return {
        "head": git(root, "rev-parse", "HEAD"),
        "pinned_blob": PINNED_GIT_BLOB,
        "before_sha256": sha256(before).hexdigest(),
        "candidate_sha256": sha256(candidate).hexdigest(),
        "reviewed_tracked_before": prior_snapshot,
        "function_name": "search_shared_group_goal",
        "new_group_given": 0,
        "full_pytest": False,
    }


def apply(root: Path, backup_folder: Path) -> dict[str, object]:
    """Install one whole function after backing up the complete original file."""
    evidence = preflight(root)
    path = Path(root) / TARGET
    before = path.read_bytes()
    if sha256(before).hexdigest() != evidence["before_sha256"]:
        raise RuntimeError("R3R9_INPUT_CHANGED_BETWEEN_PREFLIGHT_AND_APPLY")
    after = replace_function_bytes(before)
    if sha256(after).hexdigest() != evidence["candidate_sha256"]:
        raise RuntimeError("R3R9_REWRITTEN_HASH_MISMATCH")
    backup_folder.mkdir(parents=True, exist_ok=True)
    (backup_folder / "phase165_r52_r9_shared_math.py.before").write_bytes(before)
    try:
        path.write_bytes(after)
        if path.read_bytes() != after:
            raise RuntimeError("R3R9_POST_WRITE_MISMATCH")
    except Exception:
        # If the installer fails after writing but before returning, the
        # caller has not yet set its installed flag. Restore locally here.
        path.write_bytes(before)
        if path.read_bytes() != before:
            raise RuntimeError("R3R9_INSTALLER_LOCAL_ROLLBACK_FAILED")
        raise
    return {**evidence, "installed_sha256": sha256(after).hexdigest()}


def verify_postflight(root: Path, evidence: dict[str, object]) -> None:
    """Allow exactly the installed production patch, not any other drift."""
    if sha256((Path(root) / TARGET).read_bytes()).hexdigest() != evidence["installed_sha256"]:
        raise RuntimeError("R3R9_INSTALL_MUTATED")
    status = reviewed_tracked_snapshot(root, allow_public_target=True)
    public = status.pop(TARGET.as_posix(), None)
    if public != evidence["installed_sha256"]:
        raise RuntimeError("R3R9_PUBLIC_PATCH_NOT_TRACKED")
    if status != evidence["reviewed_tracked_before"]:
        raise RuntimeError("R3R9_UNRELATED_TRACKED_CHANGE_AFTER_INSTALL")


def rollback(root: Path, backup_folder: Path) -> None:
    """Restore exact bytes, without invoking Git commands."""
    path = Path(root) / TARGET
    old = (backup_folder / "phase165_r52_r9_shared_math.py.before").read_bytes()
    path.write_bytes(old)
    if path.read_bytes() != old:
        raise RuntimeError("R3R9_ROLLBACK_FAILED")
```

## 新規: audit.py

```python
"""Phase 175 R3R9: guarded direct Lemma 5.7 citation and public proof audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r9_lemma57_explicit_public import install, source

PACKAGE = "phase175_r3r9_lemma57_explicit_public"
MARKER = "__PHASE175_R3R9_WORKER__="
FOCUSED_TESTS = (
    PACKAGE + "/tests",
    "phase175_r3r8r1_verified_prior_public/tests/test_verified_prior.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_public_search.py",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py",
    "phase175_r3_pi73_hopf_lift/tests/test_rule.py",
    "phase173_r4_r1_public_connection/tests",
)
GATE = "PASS_R3R9_DIRECT_LEMMA57_PI73_PUBLIC_COMPLETE"


def git(root: Path, *args: str) -> str:
    """Run approved read-only Git queries; no mutating subcommands."""
    if not args or args[0] not in {"rev-parse", "branch", "merge-base"}:
        raise ValueError("R3R9_GIT_READ_ONLY_REQUIRED")
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if proc.returncode:
        raise RuntimeError("R3R9_GIT_QUERY_FAILED: " + " ".join(args))
    return proc.stdout.strip()


def source_guard(root: Path) -> dict[str, object]:
    """Pin all earlier reviewed sources, updating only the former public-route pin.

    The original Phase 175 R1 guard required the pre-R3R8 production blob.
    That blob is intentionally superseded by the successful R3R8R1R2 commit;
    all other R1/R2/R3 anchors retain their original expected SHAs.
    """
    from phase175_r1_k4_audit import audit as r1
    from phase175_r2_k4_frontier_audit import audit as r2
    from phase175_r3_pi73_hopf_lift import audit as r3

    if (
        git(root, "branch", "--show-current") != "develop"
        or Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root
    ):
        raise RuntimeError("R3R9_NOT_REVIEWED_DEVELOP_ROOT")
    head = git(root, "rev-parse", "HEAD")
    git(root, "merge-base", "--is-ancestor", install.PINNED_HEAD_ANCESTOR, head)
    checked = {}
    for relative, expected in (
        dict(r1.SOURCE_BLOBS)
        | r2.EXTRA_PINS
        | r3.EXTRA_PINS
    ).items():
        if relative == install.TARGET.as_posix():
            expected = install.PINNED_GIT_BLOB
        if not (root / relative).is_file():
            raise RuntimeError("R3R9_REQUIRED_SOURCE_MISSING: " + relative)
        observed = git(root, "rev-parse", "HEAD:" + relative)
        if observed != expected:
            raise RuntimeError("R3R9_PINNED_SOURCE_BLOB_CHANGED: " + relative)
        checked[relative] = expected
    if len(r1.registered_k4_rows(root / "data/sphere.csv")) != 6:
        raise RuntimeError("R3R9_REGISTERED_K4_TARGETS_CHANGED")
    citation = source.verify_explicit_lemma57_source(root)
    patch = install.preflight(root)
    return {
        "head": head, "pinned_blobs": checked,
        "explicit_source": citation,
        "patch": patch,
    }


def latest_successful_r3r8r1() -> Path:
    """Require the actual earlier user-run public PASS, not a claimed success."""
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / "phase175_r3r8r1_verified_prior_public"
    for file in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            row = json.loads(file.read_text(encoding="utf-8"))
            worker = row.get("worker")
            data = worker.get("data") if isinstance(worker, dict) else None
            if (
                row.get("phase") == "175-R3R8R1"
                and row.get("dry_run") is False
                and row.get("result") == "PASS_R3R8R1_PUBLIC_PI73_COMPLETE_AND_WEB_VERIFIED"
                and isinstance(data, dict)
                and data.get("audit_result") == "COMPLETE_AND_WEB_VERIFIED"
                and data.get("search_status") == "complete"
                and data.get("trust_verified") is True
                and data.get("web_key") == "generic-complete-proof"
            ):
                return file
        except (OSError, UnicodeError, TypeError, ValueError, KeyError):
            continue
    raise RuntimeError("R3R9_PRIOR_R3R8R1_PUBLIC_PASS_NOT_FOUND")


def worker() -> int:
    """Observe real registered backward search, trust boundary and Web view."""
    try:
        from phase175_r1_k4_audit.audit import inspect_one_group
        report = {"status": "INSPECTED", "data": inspect_one_group(3, 4)}
    except Exception as exc:
        report = {
            "status": "ERROR", "error": type(exc).__name__ + ": " + str(exc),
            "traceback": traceback.format_exc()[-6000:],
        }
    print(MARKER + json.dumps(report, ensure_ascii=False), flush=True)
    return 0


def run_worker(root: Path, folder: Path, seconds: int) -> dict:
    """Run public audit in an isolated subprocess with a bounded timeout."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        done = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"],
            cwd=root, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "seconds": seconds}
    (folder / "worker.log").write_text(
        done.stdout + "\nSTDERR:\n" + done.stderr, encoding="utf-8",
    )
    candidates = [line[len(MARKER):] for line in done.stdout.splitlines()
                  if line.startswith(MARKER)]
    if done.returncode or len(candidates) != 1:
        return {"status": "INVALID_WORKER", "exit_code": done.returncode,
                "marker_count": len(candidates)}
    try:
        decoded = json.loads(candidates[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_JSON"}
    return decoded if isinstance(decoded, dict) else {"status": "INVALID_PAYLOAD"}


def focused_pytest(root: Path, folder: Path, seconds: int) -> None:
    """Run only this Phase's relevant tests; full pytest is deferred."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        done = subprocess.run(
            [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
             *FOCUSED_TESTS],
            cwd=root, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=seconds, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("R3R9_FOCUSED_PYTEST_TIMEOUT") from exc
    output = done.stdout + "\nSTDERR:\n" + done.stderr
    (folder / "focused_pytest.log").write_text(output, encoding="utf-8")
    for line in done.stdout.strip().splitlines()[-3:]:
        print("PHASE175_R3R9_PYTEST_OUTPUT=" + line[:500], flush=True)
    if done.returncode:
        raise RuntimeError("R3R9_FOCUSED_PYTEST_FAILED: " + output[-2000:])
    print("PHASE175_R3R9_FOCUSED_PYTEST=PASS", flush=True)


def verify_public_result(data: dict[str, object]) -> dict[str, object]:
    """Trust completed tree and explicitly exclude the former Lemma 5.4 route."""
    if not isinstance(data, dict):
        raise RuntimeError("R3R9_PUBLIC_RESULT_NOT_TYPED_DATA")
    steps = data.get("proof_steps")
    refs = data.get("references")
    if not isinstance(steps, list) or not isinstance(refs, list):
        raise RuntimeError("R3R9_PROOF_ANCESTRY_NOT_PRESENT")
    from phase175_r3r9_lemma57_explicit_public.rule import RULE_NAME

    extracted = [step for step in steps if step.get("inference_rule") == RULE_NAME]
    rejected_names = (
        "Toda Lemma 5.4 verified double-suspension clause extraction",
        "even double-suspension factor implies Lemma 5.7 membership",
        "Toda Lemma 5.7 general double-suspension criterion",
    )
    old = [step for step in steps if step.get("inference_rule") in rejected_names]
    cited_54 = [ref for ref in refs if ref.get("locator") == "Lemma 5.4"]
    if not (
        data.get("audit_result") == "COMPLETE_AND_WEB_VERIFIED"
        and data.get("search_status") == "complete"
        and data.get("search_open_count") == 0
        and data.get("search_conclusion_matches_db") is True
        and data.get("trust_verified") is True
        and data.get("model_root_verified") is True
        and data.get("web_key") == "generic-complete-proof"
        and data.get("web_partial") is False
        and len(extracted) == 1
        and extracted[0].get("rule") == "INFERENCE"
        and extracted[0].get("premise_count") == 1
        and not old
        and not cited_54
        and any(ref.get("locator") == "Lemma 5.7" for ref in refs)
        and all(not (step.get("rule") == "GIVEN"
                     and "GeneratorImage(" in str(step.get("conclusion")))
                for step in steps)
    ):
        raise RuntimeError("R3R9_PUBLIC_DIRECT_LEMMA57_NOT_VERIFIED: " + str({
            key: data.get(key) for key in (
                "audit_result", "search_status", "search_open_count",
                "search_proven_count", "trust_verified", "model_error",
                "web_key", "web_error", "exception",
            )
        }) + f"; extract={len(extracted)}, old={len(old)}, lemma54_refs={len(cited_54)}")
    return {
        "search_status": "complete", "web": "generic-complete-proof",
        "source": "Lemma 5.7 explicit special clause", "lemma54_used": False,
        "reference_count": data.get("reference_count"),
        "proof_steps": len(steps),
    }


def write_report(folder: Path, report: dict[str, object]) -> None:
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 175 R3R9 — Lemma 5.7 特別結論の直接引用", "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- 対象: $\\pi_7^3=\\mathbb{Z}/2\\{\\nu'\\eta_6\\}$",
        "- Lemma 5.7 の明記された特別結論を出典付きで利用",
        "- Lemma 5.4 の依存を公開証明木に含めない",
        "- 最終群構造の直接 GIVEN: なし",
        "- 全体 pytest: 未実施", "",
        "## 実測", "",
    ]
    checked = report.get("public_evidence")
    if isinstance(checked, dict):
        for key, value in checked.items():
            lines.append("- " + key + ": `" + str(value) + "`")
    if report.get("error"):
        lines += ["", "## 失敗", "", "`" + str(report["error"]) + "`"]
    (folder / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, seconds: int) -> int:
    root = Path(root).resolve()
    local = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = local / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S_%fZ"
    )
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3R9", "dry_run": dry_run, "result": "NOT_STARTED",
        "new_group_given": 0, "new_specific_cited_clause": 1,
        "new_mathematical_inference_theorems": 0, "full_pytest": False,
        "modified_file": str(install.TARGET),
    }
    installed = False
    exit_code = 2
    print("PHASE175_R3R9_OUTPUT=" + str(folder), flush=True)
    try:
        report["source_guard"] = source_guard(root)
        report["previous_success"] = str(latest_successful_r3r8r1())
        print("PHASE175_R3R9_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R9_PRIOR_PUBLIC_PASS=PASS", flush=True)
        if dry_run:
            report["result"] = "PASS_R3R9_READ_ONLY_DRYRUN"
            exit_code = 0
        else:
            report["installation"] = install.apply(root, folder)
            installed = True
            print("PHASE175_R3R9_PUBLIC_ROUTE_PATCH=ONE_FUNCTION", flush=True)
            focused_pytest(root, folder, seconds)
            tested = run_worker(root, folder, seconds)
            report["worker"] = tested
            if tested.get("status") != "INSPECTED":
                raise RuntimeError("R3R9_PUBLIC_WORKER_FAILED: " + str(tested))
            observed = tested.get("data", {})
            print("PHASE175_R3R9_SEARCH=" + str(observed.get("search_status")), flush=True)
            print("PHASE175_R3R9_TRUST=" + str(observed.get("trust_verified")), flush=True)
            print("PHASE175_R3R9_WEB=" + str(observed.get("web_key")), flush=True)
            report["public_evidence"] = verify_public_result(observed)
            install.verify_postflight(root, report["installation"])
            report["result"] = GATE
            exit_code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
        report["result"] = "R3R9_REFUSED_OR_PUBLIC_VERIFICATION_FAILED"
        print("PHASE175_R3R9_ERROR=" + report["error"], flush=True)
    finally:
        if installed and exit_code != 0:
            try:
                install.rollback(root, folder)
                report["rolled_back"] = True
                print("PHASE175_R3R9_ROLLBACK=PASS", flush=True)
            except Exception as exc:
                report["rolled_back"] = False
                report["rollback_error"] = str(exc)
                report["result"] = "R3R9_ROLLBACK_FAILED"
        write_report(folder, report)
        print("PHASE175_R3R9_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R9_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=install.ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("timeout-seconds must be positive")
    if args.worker:
        return worker()
    return run(args.root, args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規: run.ps1

```powershell
param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

if ($DryRun) {
    Write-Output 'PHASE175_R3R9_DRYRUN_START'
    & python -B -m phase175_r3r9_lemma57_explicit_public.audit `
        --root $root --dry-run --timeout-seconds $TimeoutSeconds
    $code = $LASTEXITCODE
    Write-Output "PHASE175_R3R9_EXIT_CODE=$code"
    exit $code
}

Write-Output 'PHASE175_R3R9_PUBLIC_INTEGRATION_START'
& python -B -m phase175_r3r9_lemma57_explicit_public.audit `
    --root $root --timeout-seconds $TimeoutSeconds
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R9_EXIT_CODE=$code"
exit $code
```

## 新規: tests/test_source.py

```python
"""Source pinning and explicit-clause provenance tests."""
from __future__ import annotations

import json

import pytest

from phase175_r3r9_lemma57_explicit_public import source
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def manuscript(clause: str = source.PARTICULAR_CLAUSE) -> dict:
    """Only mock the immutable manifest shape, not the actual production source."""
    return {
        "assertions": [
            {
                "reference_id": "toda:Lemma 5.7",
                "statement_id": source.SOURCE_ID,
                "source_sha256": source.SOURCE_SHA256,
                "publication_position": source.SOURCE_POSITION,
                "review_needed": False,
                "source_text": (
                    r"\alpha\in\pi_i(S^3) "
                    r"E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5) "
                    r"E(\eta_2\circ\alpha)=0 特に, "
                    + clause + " "
                    + r"\Delta(\nu_5)=\pm(\eta_2\circ\nu')"
                ),
            },
        ],
    }


def write_manifest(root, record):
    location = root / source.MANIFEST
    location.parent.mkdir(parents=True, exist_ok=True)
    location.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")


def test_exact_explicit_source_and_order(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(source, "verify_lemma57_manifest", lambda root: {"original_pin": "verified"})
    write_manifest(tmp_path, manuscript())
    verified = source.verify_explicit_lemma57_source(tmp_path)
    assert verified["particular_clause"] == source.PARTICULAR_CLAUSE
    assert verified["new_group_given"] == 0
    assert verified["publication_position"] == 9100


@pytest.mark.parametrize("mutation", [
    "missing", "twice", "wrong_sha", "wrong_order", "needs_review", "without_specific",
])
def test_missing_or_changed_specific_clause_rejected(monkeypatch, tmp_path, mutation) -> None:
    monkeypatch.setattr(source, "verify_lemma57_manifest", lambda root: {"verified": True})
    row = manuscript()
    original = row["assertions"][0]
    if mutation == "missing":
        row["assertions"] = []
    elif mutation == "twice":
        original["source_text"] += " " + source.PARTICULAR_CLAUSE
    elif mutation == "wrong_sha":
        original["source_sha256"] = "0" * 64
    elif mutation == "wrong_order":
        original["publication_position"] = 9500
    elif mutation == "needs_review":
        original["review_needed"] = True
    elif mutation == "without_specific":
        original["source_text"] = original["source_text"].replace(
            source.PARTICULAR_CLAUSE, "E(eta_2 something)=0",
        )
    write_manifest(tmp_path, row)
    with pytest.raises(ValueError, match="R3R9_LEMMA57"):
        source.verify_explicit_lemma57_source(tmp_path)


def test_source_is_not_given_generator_image_or_group(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(source, "verify_explicit_lemma57_source", lambda root: {"verified": True})
    bridge = source.build_explicit_lemma57_source(tmp_path)
    assert len(bridge.proof_links) == 1
    link = bridge.proof_links[0]
    assert link.assertion_id == source.ASSERTION_ID
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.conclusion == source.TodaLemma57ExplicitNuPrimeZero()
    assertion = bridge.registry.assertion(source.ASSERTION_ID)
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert bridge.registry.reference(source.REFERENCE_ID).publication_position == 9100
    assert type(link.step.conclusion).__name__ != "GeneratorImage"
    assert type(link.step.conclusion).__name__ != "Relation"
```

## 新規: tests/test_rule.py

```python
"""Extract only the actually cited particular nu-prime zero-image clause."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r3r9_lemma57_explicit_public.rule import (
    RULE_NAME,
    exact_lemma57_zero_image_goal,
    expand_cited_lemma57_explicit_zero,
)
from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
from proof import (
    ProofRule,
    ProofStep,
    find_inference_matches_for_rule,
)


def fixture_goal():
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    return GeneratorImage(e, prior.rhs.generator, Zero())


def test_registered_db_nu_prime_alias_matches_explicit_toda_clause() -> None:
    goal = fixture_goal()
    assert exact_lemma57_zero_image_goal(goal)
    offered = expand_cited_lemma57_explicit_zero(goal, (TodaLemma57ExplicitNuPrimeZero(),))
    assert len(offered) == 1
    assert offered[0].rule.name == RULE_NAME
    assert offered[0].subgoals == (TodaLemma57ExplicitNuPrimeZero(),)
    given = ProofStep(TodaLemma57ExplicitNuPrimeZero(), (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(offered[0].rule, (given,))
    assert len(matches) == 1
    inferred = derive_inference_proof_step(matches[0])
    assert inferred.conclusion == goal
    assert inferred.rule is ProofRule.INFERENCE
    assert inferred.premises == (given,)


def test_no_source_means_no_candidate() -> None:
    goal = fixture_goal()
    assert expand_cited_lemma57_explicit_zero(goal, ()) == ()
    assert expand_cited_lemma57_explicit_zero(
        goal, (TodaLemma57ExplicitNuPrimeZero(), TodaLemma57ExplicitNuPrimeZero()),
    ) == ()


def test_spoofed_given_or_missing_premise_is_rejected() -> None:
    goal = fixture_goal()
    option, = expand_cited_lemma57_explicit_zero(
        goal, (TodaLemma57ExplicitNuPrimeZero(),),
    )
    assert find_inference_matches_for_rule(option.rule, ()) == ()
    assert find_inference_matches_for_rule(
        option.rule, (ProofStep("not a source", (), ProofRule.GIVEN),),
    ) == ()
    assert find_inference_matches_for_rule(
        option.rule, (ProofStep(TodaLemma57ExplicitNuPrimeZero(), (), ProofRule.INFERENCE),),
    ) == ()


def test_wrong_nu_prime_and_wrong_suspension_are_rejected() -> None:
    goal = fixture_goal()
    for wrong in (
        replace(goal, map=TodaSuspensionMap(
            TodaPrimaryGroup(7, 3), TodaPrimaryGroup(8, 4),
        )),
        replace(goal, target_generator=HomotopyElement(
            "b", 3, source=7, target=3,
        )),
        replace(goal, source_generator=Composition(
            goal.source_generator.left,
            HomotopyElement(
                "ν′", 3, source=6, target=3,
                generator=GeneratorSymbol("not-registered", 3),
            ),
        )),
    ):
        assert not exact_lemma57_zero_image_goal(wrong)
        assert expand_cited_lemma57_explicit_zero(
            wrong, (TodaLemma57ExplicitNuPrimeZero(),),
        ) == ()
```

## 新規: tests/test_route.py

```python
"""The public provider must use the specific cited clause, not Lemma 5.4."""
from __future__ import annotations

from dataclasses import replace

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r3r9_lemma57_explicit_public.route import (
    prepare_pi73_public_connection,
)
from phase175_r3r9_lemma57_explicit_public.rule import RULE_NAME
from phase175_r3r9_lemma57_explicit_public.source import (
    ASSERTION_ID,
    TodaLemma57ExplicitNuPrimeZero,
)
from proof import ProofRule


def test_prepared_route_uses_explicit_lemma_without_lemma54() -> None:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=4)
    assert len(goals) == 1
    goal = goals[0]
    prepared = prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id=None,
        prior_conclusions=(),
    )
    assert prepared is not None
    augmented, citing, provider = prepared
    assert citing == resolve_specialized_goal_citing_id(bridge, goal)
    assert ASSERTION_ID in augmented.registry._assertions
    assert ASSERTION_ID not in bridge.registry._assertions
    assert not any(link.step is not None and link.step.conclusion == goal
                   for link in augmented.proof_links)
    links = [link for link in augmented.proof_links
             if link.step is not None
             and link.step.conclusion == TodaLemma57ExplicitNuPrimeZero()]
    assert len(links) == 1
    assert links[0].step.rule is ProofRule.GIVEN
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    image = GeneratorImage(e, prior.rhs.generator, Zero())
    options = provider(image)
    assert options[0].rule.name == RULE_NAME
    assert not any("Lemma 5.4" in option.rule.name for option in options)


def test_wrong_registered_target_cannot_trigger_route() -> None:
    bridge = build_shared_typed_bridge()
    goal, = registered_group_goal_candidates(bridge, n=3, k=4)
    assert prepare_pi73_public_connection(
        bridge=bridge, goal=replace(goal, lhs=TodaPrimaryGroup(9, 3)),
        citing_assertion_id=None, prior_conclusions=(),
    ) is None
    assert prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id="fabricated-citation",
        prior_conclusions=(),
    ) is None
```

## 新規: tests/test_public_search.py

```python
"""Focused actual public search and trust/citation boundary regression."""
from __future__ import annotations

from phase175_r1_k4_audit.audit import inspect_one_group
from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result


def test_real_group_query_has_direct_lemma57_proof_and_no_lemma54_reference() -> None:
    observed = inspect_one_group(3, 4)
    certified = verify_public_result(observed)
    assert certified["search_status"] == "complete"
    assert certified["web"] == "generic-complete-proof"
    assert certified["lemma54_used"] is False
    assert certified["reference_count"] >= 2
```

## 新規: tests/test_install.py

```python
"""Review the whole-function replacement and its exact EOL handling."""
from __future__ import annotations

import ast

import pytest

from phase175_r3r9_lemma57_explicit_public import install


def test_only_one_routing_import_changes_in_complete_function() -> None:
    old = (install.PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    new = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    assert old.count(install.OLD_ROUTE) == 1
    assert new == old.replace(install.OLD_ROUTE, install.NEW_ROUTE, 1)
    before = ast.parse(old)
    after = ast.parse(new)
    assert len(before.body) == len(after.body) == 1
    assert isinstance(before.body[0], ast.FunctionDef)
    assert isinstance(after.body[0], ast.FunctionDef)
    assert ast.dump(before.body[0].args) == ast.dump(after.body[0].args)
    assert not any(isinstance(x, (ast.Global, ast.Nonlocal)) for x in after.body[0].body)


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_rewrite_full_function_and_preserve_newlines(newline: str) -> None:
    old = (install.PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    new = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    wrapped = "# untouched prefix\n" + old + "\n# untouched suffix\n"
    replaced = install.replace_function_bytes(
        wrapped.replace("\n", newline).encode("utf-8"),
    )
    expected = ("# untouched prefix\n" + new + "\n# untouched suffix\n")
    assert replaced == expected.replace("\n", newline).encode("utf-8")


def test_unreviewed_function_rejected() -> None:
    function = (install.PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    modified = function.replace("    if n == 4 and k == 3", "    if n == 5 and k == 3", 1)
    with pytest.raises(RuntimeError, match="SOURCE_FUNCTION_CHANGED_SINCE_REVIEW"):
        install.replace_function_bytes(modified.encode("utf-8"))


def test_missing_route_rejected() -> None:
    function = (install.PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    modified = function.replace(install.OLD_ROUTE, "", 1)
    with pytest.raises(RuntimeError):
        install.replace_function_bytes(modified.encode("utf-8"))
```

## 新規: tests/test_audit.py

```python
"""Ensure a claimed completion without the specific cited inference fails closed."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result
from phase175_r3r9_lemma57_explicit_public.rule import RULE_NAME


def successful_minimum():
    return {
        "audit_result": "COMPLETE_AND_WEB_VERIFIED",
        "search_status": "complete",
        "search_open_count": 0,
        "search_conclusion_matches_db": True,
        "trust_verified": True,
        "model_root_verified": True,
        "web_key": "generic-complete-proof",
        "web_partial": False,
        "proof_steps": [
            {"rule": "GIVEN", "inference_rule": "Cited explicit nu-prime clause of Toda Lemma 5.7",
             "conclusion": "TodaLemma57ExplicitNuPrimeZero()", "premise_count": 0},
            {"rule": "INFERENCE", "inference_rule": RULE_NAME,
             "conclusion": "GeneratorImage(map=E, target=Zero())", "premise_count": 1},
        ],
        "references": [{"locator": "Lemma 5.7"}],
        "reference_count": 1,
    }


def test_direct_lemma57_gate_accepts_exact_provenance_shape() -> None:
    assert verify_public_result(successful_minimum())["lemma54_used"] is False


@pytest.mark.parametrize("mutation", ["not_complete", "given_image", "no_lemma57",
                                      "old_lemma54", "missing_extraction"])
def test_public_gate_fails_without_exact_cited_extraction(mutation: str) -> None:
    item = deepcopy(successful_minimum())
    if mutation == "not_complete":
        item["search_status"] = "partial"
    elif mutation == "given_image":
        item["proof_steps"][1]["rule"] = "GIVEN"
    elif mutation == "no_lemma57":
        item["references"] = []
    elif mutation == "old_lemma54":
        item["references"].append({"locator": "Lemma 5.4"})
    elif mutation == "missing_extraction":
        item["proof_steps"][1]["inference_rule"] = "another rule"
    with pytest.raises(RuntimeError, match="R3R9_PUBLIC_DIRECT_LEMMA57_NOT_VERIFIED"):
        verify_public_result(item)
```

## 新規: README.md

```markdown
# Phase 175 R3R9 — Direct citation of Toda Lemma 5.7

This package replaces the unnecessary Lemma 5.4 dependency in the **public proof of** `pi_7^3` with the explicit “in particular” conclusion of Toda's Lemma 5.7:

`E(eta_2 o nu-prime) = 0`.

The project's **adopted Japanese Chapter V transcription** states this conclusion directly in the lemma text. The original printed edition has not been independently verified. The general conditional portion of Lemma 5.7 is not used to re-derive this particular conclusion.

The new cited source is a typed `FIXED_STATEMENT` for the text of the explicit clause, **not** a `GeneratorImage` or group result supplied as a `GIVEN`. An ordinary guarded inference extracts the typed generator-image conclusion from this exact citation. The existing verified-prior finite-cyclic zero-image rule, EHP exactness, and finite-cyclic Hopf-lift rules are reused unchanged. No source or mathematical fact is inferred from a target group answer.

Only the already reviewed `search_shared_group_goal` function in `phase165_r52_r9_shared_math.py` is changed: the previous `(n,k)=(3,4)` route import is replaced with this package's route import. All other code, API signatures, and renderer paths are preserved. On verification failure, the installer restores the exact original file bytes.

## Requirements

- Checked-out `develop` branch descended from commit `7171af968ba510291f87b8bb484d8718a3cef204`.
- The previously completed and committed Phase 175 R3R8R1R2 public route.
- The previously successful **normal** R3R8R1R2 report in `%LOCALAPPDATA%\EHPProofTracerAudit`.
- Python and pytest available on PATH.

## Running on Windows

Extract `R3R9.zip` into the repository root.

```powershell
$script = ".\phase175_r3r9_lemma57_explicit_public\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
Write-Output "DRYRUN_EXIT_CODE=$LASTEXITCODE"
```

Only if the DryRun exit code is zero, execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $script
Write-Output "R3R9_EXIT_CODE=$LASTEXITCODE"
git status -sb
```

The full test suite is deliberately **not** run during this intermediate Phase step. The bundled audit runs only focused tests and an actual registered Group query and Web verification.

## Success gate

`PASS_R3R9_DIRECT_LEMMA57_PI73_PUBLIC_COMPLETE`

This requires a complete typed proof, trust verification, the `generic-complete-proof` Web result, exactly one inference extracting the cited explicit Lemma 5.7 clause, and **no** dependency on Lemma 5.4 in the accepted proof tree or citations.
```

## 新規: AUDIT_PLAN_JA.md

```markdown
# Phase 175 R3R9 — Lemma 5.7 特別結論の直接引用と公開証明監査

## 目的

現行の $\pi_7^3$ の公開 Proof Tree は Lemma 5.4 を経由して $E(\eta_2\circ\nu')=0$ を導く。しかしプロジェクト採用 Toda Chapter V 転記の Lemma 5.7 自体に「特に、$E(\eta_2\circ\nu')=0$」と明記されている。したがって、後続の証明でこの結論を引用するために Lemma 5.4 の証明を再実行する必要はない。

一般の $\alpha$ に対する Lemma 5.7 の仮定 $E^2\alpha\in2\iota_5\circ\pi_{i+2}^5$ を不要にするわけではない。今回採用するのは明記された特別な結論そのものである。

## 監査した既存コード・テスト

- `phase165_r52_r9_shared_math.py`：現行 `search_shared_group_goal()` および公開接続
- `phase175_r3r8r1_verified_prior_public/route.py`・`rule.py`・`install.py`
- `phase175_r3r8r1_verified_prior_public/tests/test_public_search.py`・`tests/test_verified_prior.py`
- `phase175_r3r6_lemma57_general/source.py`・`rule.py`・`tests/test_source.py`
- `phase175_r3r7_lemma54_membership/rule.py`
- `phase169_r10e4_ordered_db_prior/db_prior.py`：実際の先行 DB 検証
- `phase175_r1_k4_audit/audit.py`：通常 Group query・Trust・共通 Renderer・Web の実監査
- `phase168_r3_5_model_renderer.py`：共通 Narrative
- `phase163_r4_r94_output/manifest.json` の Lemma 5.7：出典 ID `toda:tex:ch5:0015`、SHA256 `01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c`、出版順 9100。Proposition 5.8 は順 9200。

**出典上の留保**：検証対象はプロジェクト採用の日本語転記とその署名済みマニフェストであり、原著の印刷版との独立照合は未実施。

## 変更対象一覧

1. **既存ファイル** `phase165_r52_r9_shared_math.py`
   - **関数** `search_shared_group_goal()` の全体：$(n,k)=(3,4)$ の import 接続先のみ `phase175_r3r9_lemma57_explicit_public.route` に変更。既存の import 部と他の関数は変更しない。
2. **新規ファイル** `phase175_r3r9_lemma57_explicit_public/source.py`
   - **クラス** `TodaLemma57ExplicitNuPrimeZero`、**関数** `verify_explicit_lemma57_source()`、`build_explicit_lemma57_source()` を新規追加。
3. **新規ファイル** `phase175_r3r9_lemma57_explicit_public/rule.py`
   - **関数** `exact_lemma57_zero_image_goal()`、`lemma57_explicit_zero_rule()`、`expand_cited_lemma57_explicit_zero()` を新規追加。
4. **新規ファイル** `phase175_r3r9_lemma57_explicit_public/route.py`
   - **関数** `public_cited_ehp_extensions()`、`prepare_pi73_public_connection()` を新規追加。
5. **新規ファイル** `phase175_r3r9_lemma57_explicit_public/install.py`・`audit.py`・`run.ps1`・`tests/`・`README.md`・本監査文書・全文コード・テスト記録。

新規関数／クラスはいずれも記載した新規ファイル内に配置する。既存のクラス・数学的規則・公開 Renderer・他のテストを修正しない。

## 数学的推論の境界

1. Lemma 5.7 の出典を厳格に検証し、明記された特別結論の引用自体を一つの `GIVEN` ソース型で表す。
2. その型から $E(\eta_2\circ\nu')=0$ に対応する `GeneratorImage` を **INFERENCE** として抽出する。この段階で登録済み HyoujiGen ID による同一生成元検証を要求する。
3. $\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}$ の先行 DB `ProofStep` を `verified_db_step()` で再検証して零写像性を導く。
4. EHP 完全性から $H$ の単射性を導く。
5. 出典付き Hopf 像と先行 $\pi_7^5$ の検証済み群構造から $\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}$ を導く。

**禁止事項**：最終群構造の直接 GIVEN、条件付き一般命題からの無条件特殊化、未登録の名前同一視、専用証明・専用 Narrative、証明の保存済み再生。

## DryRun／本実行・テスト

- DryRun：Git HEAD と既存コード・出典 SHA・先行正常報告・差分の検査だけを実施し、追跡済みファイルを変更しない。
- 本実行：既存の `search_shared_group_goal()` 関数全体のみに限定した変更を適用し、限定 pytest と通常 Group query の公開検証を実施。
- 成功条件：`complete`、未解決 Goal 0、Trust `True`、Web `generic-complete-proof`、Lemma 5.7 の引用出典、該当抽出推論1件、Lemma 5.4 の使用0件。
- 失敗時：検証開始前の `phase165_r52_r9_shared_math.py` を**バイト単位で復元**。
- **全体 pytest は Phase 175 終了時にのみ行う。**

## 次 Phase との境界

R3R9 は $\pi_7^3$ の出典依存関係を短くすることだけに集中し、$\pi_9^5$ や $\pi_{10}^6$ の新しい証明規則・文献登録や一般 Narrative の追加変更を先取りしない。共通 Renderer の表示簡略化は証明の出典が安定した後に独立した監査として行う。
```

## 新規: TEST_RESULTS_JA.md

```markdown
# Phase 175 R3R9 — テスト記録

## 現時点の作成環境での確認

- すべての新規 `.py` と `search_shared_group_goal_FULL.py.txt` の構文検査：**15対象 PASS**。
- 既存の関数全体と変更後関数の AST（抽象構文木）、API 引数、置換範囲の監査：実施。
- インストーラーの純粋関数による LF／CRLF 置換・未知の差分拒否：**限定テスト5件 PASS**（旧ガードへの import をテスト用スタブに置き換えた独立環境）。
- GitHub `develop` の公開接続対象ファイルを確認：`phase165_r52_r9_shared_math.py` Git blob `3426b223f94e839e77972801977d58a4ca182767`。
- Toda Chapter V の Lemma 5.7 原文と出典順序を確認：特別な零写像結論が明記されている。追加の単独 Source Guard テストで正規テキストを受理し、特別結論を改変したテキストを拒否。

## Windows 実リポジトリでは未実施

以下は同梱 `run.ps1` の本実行時に**限定して実行**する。

```text
python -B -m pytest -q -p no:cacheprovider \
  phase175_r3r9_lemma57_explicit_public/tests \
  phase175_r3r8r1_verified_prior_public/tests/test_verified_prior.py \
  phase175_r3r8r1_verified_prior_public/tests/test_public_search.py \
  phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py \
  phase175_r3_pi73_hopf_lift/tests/test_rule.py \
  phase173_r4_r1_public_connection/tests
```

同時に、`inspect_one_group(3,4)` を子プロセスで実行し、通常 Proof Search、Proof Tree Trust、共通 Narrative、Web `generic-complete-proof` を検証する。

**実リポジトリでの PASS 件数はまだ主張しない。**

## 完了条件

`PASS_R3R9_DIRECT_LEMMA57_PI73_PUBLIC_COMPLETE`

失敗時は `R3R9_REFUSED_OR_PUBLIC_VERIFICATION_FAILED` として本体の接続関数を自動復元する。

全体 pytest：Phase 175 完了時のみ実施。
```

## 新規: HANDOFF_JA.md

```markdown
# EHP Proof Tracer — Phase 175 R3R9 引継ぎ（2026-11-16）

## 数学的な訂正（確定）

Toda Chapter V、Lemma 5.7 の採用転記には、一般条件のあとに「特に、$E(\eta_2\circ\nu')=0$」と明記されている。この特別結論を**定理の引用として**使う場合、Lemma 5.4 の $E^2\nu'=2E\nu_4$ を後続証明で再度示す必要はない。一般の $\alpha$ に関する Lemma 5.7 の仮定は別であり、無条件の一般化は禁止。

## 実証済みの到達点

Phase 175 R3R8R1R2 は user Windows 実行で限定 pytest 85 PASS、$\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}$ の Group query `complete`、Trust `True`、Web `generic-complete-proof`、Reference 8件となった。ただし当時の Proof Tree は Lemma 5.4 を経由している。

## R3R9 の目標・変更

R3R9 は、Lemma 5.7 の明示的結論を出典付き `GIVEN` ソース型から `GeneratorImage` へ抽出する推論として表現し、Lemma 5.4 に依存しない新しい公開経路を選ぶ。その他の EHP 群構造推論、Hopf lift、検証済み DB 先行結果、共通 Narrative は変更しない。

- 新規 `phase175_r3r9_lemma57_explicit_public/` 以下に出典検証、抽出推論、公開接続、インストーラー、限定テスト、監査を追加。
- 唯一の既存コード変更：`phase165_r52_r9_shared_math.py` の `search_shared_group_goal()` にある `(n,k)=(3,4)` の import 接続先を旧 R3R8R1 route から R3R9 route へ変更。
- ベースライン GitHub `develop` の production blob：`3426b223f94e839e77972801977d58a4ca182767`、確認 HEAD：`7171af968ba510291f87b8bb484d8718a3cef204`。
- プロジェクト採用出典 Manifest は Lemma 5.7 の ID `toda:tex:ch5:0015`、SHA256 `01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c`、順序9100を要求。原著印刷本は未照合。

## 実行と報告

まず `R3R9.zip` をリポジトリ root に解凍し、`phase175_r3r9_lemma57_explicit_public/run.ps1 -DryRun`、成功後に通常実行。先行 R3R8R1 の正常レポートを要求。実際の公開探索が失敗すれば単一ファイルをバイト単位でロールバックする。

成功 Gate：`PASS_R3R9_DIRECT_LEMMA57_PI73_PUBLIC_COMPLETE`。単に完成しているだけではなく、Lemma 5.7 特別結論の抽出推論、Lemma 5.4 の非使用、Trust と Web 完成表示を要求する。

## 境界とユーザー要望

- $\pi_9^5$ / $\pi_{10}^6$ は次回以降。今回は未着手。
- 全体 pytest は Phase 175 の最後のみ。
- 変更対象の関数・クラス・import・テストは省略せず全文。ZIP と PowerShell コマンドを必ず用意。
- 専用 Narrative や直接の最終結論 GIVEN を作らない。
- 回答は日本語、数式は短く、先に結論。PowerShell への貼り付けで `{` が壊れた事例があるため、貼り付け例は可能なら `if` 不使用。
- 他チャットでの完全自動引継ぎは保証されないため、この文書や実行ログを参照して再開。
```
