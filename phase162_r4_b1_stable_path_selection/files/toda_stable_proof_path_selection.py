"""Select the stable proof strategy without fabricating proof evidence.

Phase 162 R4-B1 only: choice of path, not derivation or renderer wiring.
"""

from dataclasses import dataclass
from enum import Enum

from homotopy_groups import TodaPrimaryGroup
from stable_rules import (
    canonical_toda_stable_base,
    is_in_toda_stable_range,
    toda_stable_transport_exponent,
)
from toda_group_result import TodaGroupResult


class TodaStableProofPathKind(str, Enum):
    UNSTABLE_EXISTING = "unstable_existing"
    STABLE_BASE_EXISTING = "stable_base_existing"
    STABLE_TODA45_TRANSPORT = "stable_toda45_transport"


@dataclass(frozen=True)
class TodaStableProofPathSelection:
    kind: TodaStableProofPathKind
    target: TodaPrimaryGroup
    base: TodaPrimaryGroup | None
    suspension_count: int | None
    uses_existing_root: bool

    @property
    def requires_transport_proof(self) -> bool:
        return self.kind is TodaStableProofPathKind.STABLE_TODA45_TRANSPORT


def select_toda_stable_proof_path(
    group_result: TodaGroupResult,
) -> TodaStableProofPathSelection:
    """Select an intended strategy, without asserting any new ProofStep.

    For stable targets strictly above the canonical base, prefer (4.5).
    For base and unstable targets, keep the existing root ancestry.
    """
    if not isinstance(group_result, TodaGroupResult):
        raise TypeError("group_result must be a TodaGroupResult")

    target = group_result.target
    if not is_in_toda_stable_range(target):
        return TodaStableProofPathSelection(
            kind=TodaStableProofPathKind.UNSTABLE_EXISTING,
            target=target,
            base=None,
            suspension_count=None,
            uses_existing_root=True,
        )

    base = canonical_toda_stable_base(target)
    exponent = toda_stable_transport_exponent(target)
    if target == base:
        return TodaStableProofPathSelection(
            kind=TodaStableProofPathKind.STABLE_BASE_EXISTING,
            target=target,
            base=base,
            suspension_count=0,
            uses_existing_root=True,
        )

    if exponent <= 0:
        raise ValueError("stable non-base target needs positive suspension count")

    return TodaStableProofPathSelection(
        kind=TodaStableProofPathKind.STABLE_TODA45_TRANSPORT,
        target=target,
        base=base,
        suspension_count=exponent,
        uses_existing_root=False,
    )
