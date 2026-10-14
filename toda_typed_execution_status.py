"""Status of a typed generator execution request (not proof certification)."""
from enum import Enum


class TypedGeneratorExecutionStatus(str, Enum):
    NONE = "none"
    AMBIGUOUS = "ambiguous"
    EXECUTED = "executed"
