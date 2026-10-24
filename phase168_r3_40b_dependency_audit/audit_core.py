"""Pure, non-mutating diagnostics for narrative proof-step ordering."""
from __future__ import annotations


def flattened_order(entries, step_count: int, suppressed=()):
    """Validate existing NarrativeOrderEntry projections without reordering."""
    if type(step_count) is not int or step_count < 0:
        raise ValueError("invalid step count")
    suppressed_set = set(suppressed)
    if any(type(index) is not int or not 0 <= index < step_count for index in suppressed_set):
        raise ValueError("invalid suppressed index")
    flat = []
    for entry in entries:
        flat.append(entry.step_index)
        flat.extend(entry.after_indices)
    if any(type(i) is not int or not 0 <= i < step_count for i in flat):
        raise ValueError("projection contains out-of-range step indices")
    if len(flat) != len(set(flat)):
        raise ValueError("projection duplicates proof-step indices")
    expected = set(range(step_count)) - suppressed_set
    if set(flat) != expected:
        raise ValueError("projection loses or adds proof-step indices")
    return tuple(flat)


def find_existing_step_index(steps, premise):
    """Resolve original ProofStep identity, with unambiguous value fallback."""
    identities = tuple(index for index, candidate in enumerate(steps) if candidate is premise)
    if len(identities) == 1:
        return identities[0], "identity"
    if len(identities) > 1:
        return None, "ambiguous_identity"
    equal = []
    for index, candidate in enumerate(steps):
        try:
            if candidate == premise:
                equal.append(index)
        except (TypeError, ValueError, RecursionError):
            continue
    if len(equal) == 1:
        return equal[0], "value"
    if len(equal) > 1:
        return None, "ambiguous_value"
    return None, "not_in_flattened_steps"


def proof_dependency_edges(steps):
    edges = []
    unresolved = []
    for child_index, step in enumerate(steps):
        for premise_index, premise in enumerate(step.premises):
            parent_index, resolution = find_existing_step_index(steps, premise)
            if parent_index is None:
                unresolved.append({
                    "child_step": child_index,
                    "premise_slot": premise_index,
                    "resolution": resolution,
                    "premise_type": type(premise.conclusion).__name__,
                })
            else:
                edges.append((parent_index, child_index))
    return tuple(dict.fromkeys(edges)), tuple(unresolved)


def dependency_inversions(edges, displayed):
    position = {index: pos for pos, index in enumerate(displayed)}
    return tuple(
        (parent, child)
        for parent, child in edges
        if parent in position and child in position and position[parent] >= position[child]
    )


def relative_order(before, after, displayed):
    positions = {index: pos for pos, index in enumerate(displayed)}
    if before not in positions or after not in positions:
        return "NOT_VISIBLE"
    return "PASS" if positions[before] < positions[after] else "FAIL"
