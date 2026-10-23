"""Pure proof-model projection: certified exactness windows to typed chains.

No rendering, source guessing, goal-specific content, or mutation of Proof Tree.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup
from map_facts import EHP_E_MAP, EHP_H_MAP, EHP_DELTA_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from toda_rules import TodaProp42ExactnessStatement


@dataclass(frozen=True)
class ExactnessChain:
    arrows: tuple[tuple[object, object, object], ...]
    step_indices: tuple[int, ...]


def project_exactness_chains(model: ProofNarrativeModel) -> tuple[ExactnessChain, ...]:
    """Merge overlapping certified 2-arrow windows into maximal unbranched chains.

    Shared endpoints alone do not suffice: edges must match source, map and
    target. Unsupported, disconnected, cyclic and branched components are not
    suppressed. Source-step identity is retained for provenance.
    """
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    windows = []
    for index, step in enumerate(model.steps):
        statement = step.conclusion
        if not isinstance(statement, TodaProp42ExactnessStatement):
            continue
        if prop42_exactness_indices(statement) is None:
            continue
        window = statement.window
        groups = (window.source_term, window.middle_term, window.target_term)
        if not all(isinstance(group, TodaPrimaryGroup)
                   and type(group.group_dimension) is int
                   and type(group.sphere_dimension) is int for group in groups):
            continue
        if window.first_map not in (EHP_E_MAP, EHP_H_MAP, EHP_DELTA_MAP) or window.second_map not in (EHP_E_MAP, EHP_H_MAP, EHP_DELTA_MAP):
            continue
        first = (window.source_term, window.first_map, window.middle_term)
        second = (window.middle_term, window.second_map, window.target_term)
        windows.append((index, first, second))

    successors: dict[tuple, set] = {}
    predecessors: dict[tuple, set] = {}
    for _, first, second in windows:
        successors.setdefault(first, set()).add(second)
        predecessors.setdefault(second, set()).add(first)
    seen = set()
    chains = []
    for _, first, second in windows:
        for arrow in (first, second):
            if arrow in seen:
                continue
            component = set()
            frontier = [arrow]
            while frontier:
                candidate = frontier.pop()
                if candidate in component:
                    continue
                component.add(candidate)
                frontier.extend(successors.get(candidate, ()))
                frontier.extend(predecessors.get(candidate, ()))
            seen.update(component)
            if len(component) < 3:
                continue
            if any(len(successors.get(edge, ())) > 1 or
                   len(predecessors.get(edge, ())) > 1 for edge in component):
                continue
            starts = [edge for edge in component if not predecessors.get(edge)]
            if len(starts) != 1:
                continue
            ordered = []
            current = starts[0]
            while current not in ordered:
                ordered.append(current)
                next_edges = successors.get(current, ())
                if not next_edges:
                    break
                current = next(iter(next_edges))
            if len(ordered) != len(component):
                continue
            steps = tuple(index for index, a, b in windows
                          if a in component and b in component)
            if len(steps) < 2:
                continue
            chains.append(ExactnessChain(tuple(ordered), steps))
    chains.sort(key=lambda chain: min(chain.step_indices))
    return tuple(chains)
