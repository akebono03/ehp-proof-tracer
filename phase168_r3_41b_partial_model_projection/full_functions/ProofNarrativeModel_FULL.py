@dataclass(frozen=True)
class ProofNarrativeModel:
    steps: tuple[ProofStep, ...]
    citations: tuple[NarrativeCitation, ...]
    step_citation_numbers: tuple[tuple[int, ...], ...]
    root_index: int | None
    status: ProofSearchStatus | None = None
    target: TodaPrimaryGroup | None = None
    open_goals: tuple[object, ...] = ()
    diagnostics: tuple[str, ...] = ()
