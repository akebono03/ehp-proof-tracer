class RegisteredGoalUnresolved(ValueError):
    """The requested proof is not established under the active search gates."""


@dataclass(frozen=True)
class SourceBoundGoal:
    """Require an inferred conclusion derived from this specific cited source.

    This is a search obligation, not a mathematical assertion or a GIVEN leaf.
    The returned ProofStep has the ordinary conclusion type, not this wrapper.
    """
    conclusion: object
    source: object
