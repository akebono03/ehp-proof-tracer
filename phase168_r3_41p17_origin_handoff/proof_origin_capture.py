"""Session-local observation of ProofStep factory outputs.

This is NOT a mathematical certificate: caller-supplied InferenceMatch objects
and caller-supplied source registries are not independently authenticated.
Only a canonical search scope plus its screened bridge is meaningful here.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator

from proof import ProofRule, ProofStep


class SearchOriginObservation:
    """Identity-based factory record for a single, live search invocation."""

    def __init__(self) -> None:
        self._factory_steps: dict[int, ProofStep] = {}
        self._accepted_steps: dict[int, ProofStep] = {}
        self._closed = False

    def contains_factory_step(self, step: ProofStep) -> bool:
        """Observe identity only; this does not independently validate a rule."""
        return self._factory_steps.get(id(step)) is step

    def contains_accepted_step(self, step: ProofStep) -> bool:
        return self._accepted_steps.get(id(step)) is step

    @property
    def factory_output_count(self) -> int:
        return len(self._factory_steps)

    @property
    def accepted_step_count(self) -> int:
        return len(self._accepted_steps)


_ACTIVE: ContextVar[SearchOriginObservation | None] = ContextVar(
    "ehp_search_origin_observation", default=None,
)


@contextmanager
def capture_search_origins() -> Iterator[SearchOriginObservation]:
    """Isolate factory observations per nested/thread-local search session."""
    observation = SearchOriginObservation()
    token = _ACTIVE.set(observation)
    try:
        yield observation
    finally:
        observation._closed = True
        _ACTIVE.reset(token)


def note_factory_inference(step: ProofStep) -> None:
    """Called by the existing checked factory, never by Renderer or Model."""
    observation = _ACTIVE.get()
    if observation is None:
        return
    if observation._closed:
        raise RuntimeError("search origin observation is closed")
    if type(step) is not ProofStep or step.rule is not ProofRule.INFERENCE:
        raise TypeError("only checked factory INFERENCE steps may be recorded")
    observation._factory_steps[id(step)] = step


def note_accepted_search_step(step: ProofStep) -> None:
    """Observe a `proved` callback from the existing search adapter.

    A candidate constructed but never accepted is not a proven search step.
    """
    observation = _ACTIVE.get()
    if observation is None:
        return
    if observation._closed:
        raise RuntimeError("search origin observation is closed")
    if type(step) is not ProofStep:
        raise TypeError("accepted origin must be a ProofStep")
    observation._accepted_steps[id(step)] = step


def require_active_observation(observation: SearchOriginObservation) -> None:
    """A historical or caller-supplied boolean is never a live search record."""
    if type(observation) is not SearchOriginObservation:
        raise TypeError("observation must be SearchOriginObservation")
    if observation._closed or _ACTIVE.get() is not observation:
        raise ValueError("origin observation must belong to the active search")
