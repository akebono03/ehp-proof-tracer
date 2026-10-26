@dataclass(frozen=True)
class SourceBoundGoal:
    """Require a uniquely proved conclusion derived from this cited source.

    This is a search obligation, not a mathematical assertion or a GIVEN leaf.
    The returned ProofStep has the ordinary conclusion type, not this wrapper.
    """
    conclusion: object
    source: object
