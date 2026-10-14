"""R52-R2: observe the canonical search without converting goals into proof."""

from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_partial_proof import (
    GroupStructureStatus,
    ProofSearchStatus,
    make_partial_proof_result,
)
from proof import ProofStep


def search_registered_partial_proof(
    *,
    n: int,
    k: int,
    goal: object | None = None,
    bridge: object | None = None,
    citing_assertion_id: str | None = None,
    expansion_provider: object | None = None,
    verified_assertion_ids: tuple[str, ...] = (),
    lookup_mode: str = "legacy",
    structure_status: GroupStructureStatus = GroupStructureStatus.UNKNOWN,
    references: tuple[str, ...] = (),
    completed_internal_proofs: tuple = (),
):
    """Return observed results; never replay or manufacture missing premises."""
    # Validate the public domain even for a not-searched result.
    base = dict(
        n=n, k=k, structure_status=structure_status, references=references,
    )
    if any(item is None for item in (goal, bridge, citing_assertion_id, expansion_provider)):
        return make_partial_proof_result(
            **base, status=ProofSearchStatus.NOT_SEARCHED,
            open_goals=(goal,) if goal is not None else (),
            diagnostics=("登録済み探索入力が不足しているため未探索",),
        )

    target_group = TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n)
    observed_steps: list[ProofStep] = []
    observed_unresolved: list[object] = []

    def same(a: object, b: object) -> bool:
        return type(a) is type(b) and a == b

    def observer(kind: str, observed_goal: object, step: ProofStep | None) -> None:
        if kind == "proved":
            if step is None or not isinstance(step, ProofStep):
                raise TypeError("proved observation must contain a ProofStep")
            if not any(existing is step for existing in observed_steps):
                observed_steps.append(step)
        elif kind == "unresolved":
            if not any(same(item, observed_goal) for item in observed_unresolved):
                observed_unresolved.append(observed_goal)
        else:
            raise ValueError("unknown search observation")

    error = None
    try:
        root_step = reconstruct_registered_goal(
            goal, bridge, citing_assertion_id, expansion_provider,
            verified_assertion_ids=verified_assertion_ids,
            lookup_mode=lookup_mode,
            progress_observer=observer,
            completed_internal_proofs=completed_internal_proofs,
        )
    except RegisteredGoalUnresolved as exc:
        root_step = None
        error = str(exc)

    unsolved = tuple(
        item for item in observed_unresolved
        if not any(same(item, step.conclusion) for step in observed_steps)
    )
    if root_step is None:
        if not any(same(item, goal) for item in unsolved):
            unsolved += (goal,)
        return make_partial_proof_result(
            **base,
            status=ProofSearchStatus.PARTIAL if observed_steps else ProofSearchStatus.SEARCH_FAILED,
            proven_steps=tuple(observed_steps),
            open_goals=unsolved,
            diagnostics=(error or "探索が未解決のまま終了",),
        )

    # The canonical prover's root success alone does not certify that the
    # claimed group is the requested group.
    if getattr(root_step.conclusion, "lhs", None) != target_group:
        return make_partial_proof_result(
            **base, status=ProofSearchStatus.PARTIAL,
            proven_steps=tuple(observed_steps), open_goals=(goal,),
            diagnostics=("導出された結論の群が要求された群と一致しない",),
        )
    return make_partial_proof_result(
        **base, status=ProofSearchStatus.COMPLETE,
        proven_steps=tuple(observed_steps), conclusion=root_step.conclusion,
    )
