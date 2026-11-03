# Complete revised production classes and function

### `CertifiedAbstractStructure`

```python
@dataclass(frozen=True)
class CertifiedAbstractStructure:
    """Verified abstract invariants, separate from a named group conclusion."""
    group: TodaPrimaryGroup
    invariant_summands: tuple[tuple[str, int], ...]
    proof_step: ProofStep

    def __post_init__(self) -> None:
        from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
            TodaProp44AbstractGroupResult,
        )
        if not isinstance(self.group, TodaPrimaryGroup):
            raise TypeError("abstract certificate must have a typed target group")
        expected = TodaProp44AbstractGroupResult(
            self.group, self.invariant_summands,
        )
        if (not isinstance(self.proof_step, ProofStep)
                or self.proof_step.rule is not ProofRule.INFERENCE
                or self.proof_step.conclusion != expected
                or self.proof_step.inference_rule is None
                or not callable(self.proof_step.inference_rule.match_guard)
                or not self.proof_step.inference_rule.match_guard(
                    self.proof_step.premises, (),
                )):
            raise ValueError("abstract certificate has no verified inference root")
```

### `PartialProofResult`

```python
@dataclass(frozen=True)
class PartialProofResult:
    target: TodaPrimaryGroup
    status: ProofSearchStatus
    structure_status: GroupStructureStatus = GroupStructureStatus.UNKNOWN
    references: tuple[str, ...] = ()
    proven_steps: tuple[ProofStep, ...] = ()
    open_goals: tuple[Any, ...] = ()
    diagnostics: tuple[str, ...] = ()
    conclusion: Any | None = None
    abstract_structure: CertifiedAbstractStructure | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.target, TodaPrimaryGroup):
            raise TypeError("target must be TodaPrimaryGroup")
        if not isinstance(self.status, ProofSearchStatus):
            raise TypeError("status must be ProofSearchStatus")
        if not isinstance(self.structure_status, GroupStructureStatus):
            raise TypeError("structure_status must be GroupStructureStatus")
        for name in ("references", "proven_steps", "open_goals", "diagnostics"):
            if not isinstance(getattr(self, name), tuple):
                raise TypeError(f"{name} must be a tuple")
        if not all(isinstance(s, ProofStep) for s in self.proven_steps):
            raise TypeError("proven_steps must contain only ProofStep")
        if not all(isinstance(s, str) and s for s in self.references + self.diagnostics):
            raise ValueError("references and diagnostics must contain nonempty strings")
        if self.status is ProofSearchStatus.COMPLETE:
            if self.conclusion is None or self.open_goals:
                raise ValueError("complete proof requires conclusion and no open goals")
            if not any(step.conclusion == self.conclusion for step in self.proven_steps):
                raise ValueError("completed conclusion requires a matching proven step")
        elif self.conclusion is not None:
            raise ValueError("incomplete result must not claim a final conclusion")
        if self.abstract_structure is not None:
            if (not isinstance(self.abstract_structure, CertifiedAbstractStructure)
                    or self.abstract_structure.group != self.target
                    or self.status not in (
                        ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED,
                    )
                    or self.conclusion is not None
                    or self.structure_status is GroupStructureStatus.KNOWN):
                raise ValueError(
                    "abstract-only evidence cannot certify a named group"
                )
        if self.status is ProofSearchStatus.NOT_SEARCHED and self.proven_steps:
            raise ValueError("not-searched result cannot contain derived steps")
        if self.status is ProofSearchStatus.SEARCH_FAILED and not self.diagnostics:
            raise ValueError("failed search requires a diagnostic")
```

### `search_group_from_registered_goal`

```python
def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None, goal=None, context_sink=None):
    """Search typed goals. Zero goals use the same evidenced backward engine."""
    from homotopy_groups import TodaPrimaryGroupZeroStatement

    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates

    target = TodaPrimaryGroup(n + k, n)
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)

    if goal is not None:
        valid_relation = (
            isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and goal.lhs == target
            and isinstance(goal.rhs, _GROUP_STRUCTURES)
        )
        valid_zero = (
            isinstance(goal, TodaPrimaryGroupZeroStatement)
            and goal.group == target
        )
        if not valid_relation and not valid_zero:
            raise ValueError("goal must be a typed group statement for the requested n,k")

    if goal is None:
        zeros = database_zero_group_goal_candidates(n=n, k=k)
        if len(zeros) == 1:
            candidate = zeros[0]
        else:
            if bridge is None:
                bridge = build_shared_typed_bridge()
            candidates = registered_group_goal_candidates(bridge, n=n, k=k)
            if len(candidates) != 1:
                explanation = (
                    "群構造・生成元の型付き証明目標を指定してください"
                    if not candidates else
                    "群構造の型付き候補が複数あり、証明目標を一意に選択できない"
                )
                return make_partial_proof_result(
                    n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                    open_goals=(target,), diagnostics=(explanation,),
                )
            candidate = candidates[0]
    else:
        candidate = goal

    if bridge is None:
        bridge = build_shared_typed_bridge()

    if isinstance(candidate, TodaPrimaryGroupZeroStatement):
        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        from phase165_r52_r2_search_adapter import search_registered_partial_proof

        from phase165_r52_r9_shared_math import shared_expansion_provider

        assertions = tuple(bridge.registry._assertions.values())
        if not assertions:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=("型付き命題台帳が空です",),
            )
        # The DB target has no publication position. Cite only independently
        # positioned fixed source statements; invent no target citation ID.
        context_id = assertions[0].assertion_id
        from phase173_r4_r11_zero_public_connection.route import (
            prepare_zero_toda56_public_connection,
        )
        zero_connection = prepare_zero_toda56_public_connection(
            bridge=bridge, goal=candidate,
        )
        if zero_connection is None:
            screened = screen_independent_sources_for_derived_goal(
                bridge, goal=candidate,
            )
            provider = shared_expansion_provider(
                screened, proof_target=candidate,
            )
        else:
            screened, provider = zero_connection
        if context_sink is not None:
            context_sink(screened)
        return search_registered_partial_proof(
            n=n, k=k, goal=candidate, bridge=screened,
            citing_assertion_id=context_id,
            expansion_provider=provider, lookup_mode="typed_reference",
        )

    if proof_order_catalog is None:
        from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog

        proof_order_catalog, order_diagnostic = resolve_reviewed_order_catalog(
            bridge, n=n, k=k,
        )
        if order_diagnostic is not None:
            pending = make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=(order_diagnostic,),
            )
            if n == 4 and k >= 3:
                from phase173_r4_r15r8_public_abstract_sidecar.attach import (
                    attach_certified_abstract_structure,
                )
                return attach_certified_abstract_structure(
                    pending, n=n, k=k, goal=candidate, bridge=bridge,
                )
            return pending
    citing_id = resolve_specialized_goal_citing_id(bridge, candidate)
    search_kwargs = dict(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
        context_sink=context_sink,
    )
    if citing_id is not None:
        search_kwargs["citing_assertion_id"] = citing_id
    result = search_shared_group_goal(**search_kwargs)
    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    if n == 4 and k >= 3:
        from phase173_r4_r15r8_public_abstract_sidecar.attach import (
            attach_certified_abstract_structure,
        )
        return attach_certified_abstract_structure(
            result, n=n, k=k, goal=candidate, bridge=bridge,
        )
    return result
```

