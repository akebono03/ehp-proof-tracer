class NarrativeCitation:
    number: int
    reference: LiteratureReference
    step_indices: tuple[int, ...]
    assertion_ids: tuple[str, ...] = ()
    reference_ids: tuple[str, ...] = ()
    statement_bodies: tuple[str, ...] = ()
