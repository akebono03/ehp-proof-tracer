def project_narrative_order(
    model: ProofNarrativeModel,
    suppressed_exactness: frozenset[int] | set[int] = frozenset(),
) -> tuple[NarrativeOrderEntry, ...]:
    """Order proven steps without reversing a ProofStep premise dependency.

    Real proof dependencies are mandatory. Two presentation preferences are
    permitted only when their witness statements already occur in the model:
    the source-group presentation precedes its quotient, and a suspension
    generator is described after the relevant certified transport evidence.
    A stable topological order keeps unrelated steps in their original order.
    """
    from heapq import heappop, heappush

    from expression import IteratedSuspension
    from homotopy_groups import (
        FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaSuspensionMap,
    )
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase165_r14_r6_generic_iso import GeneratorImage
    from toda_rules import Toda45IsomorphismStatement

    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    total = len(model.steps)
    if any(type(i) is not int or not 0 <= i < total
           for i in suppressed_exactness):
        raise ValueError("invalid suppressed proof-step index")

    # Keep all nodes (including non-rendered and suppressed ones) in the
    # dependency graph. Suppressing their prose does not erase their proofs.
    successors = [set() for _ in range(total)]
    predecessors = [set() for _ in range(total)]

    def locate(premise):
        for candidate_index, candidate in enumerate(model.steps):
            if candidate is premise:
                return candidate_index
        for candidate_index, candidate in enumerate(model.steps):
            if candidate == premise:
                return candidate_index
        raise ValueError("Proof Tree premise is missing from narrative model")

    def precedes_or_equals(start, destination):
        pending = [start]
        visited = set()
        while pending:
            current = pending.pop()
            if current == destination:
                return True
            if current in visited:
                continue
            visited.add(current)
            pending.extend(successors[current])
        return False

    def add_dependency(before, after, *, editorial=False):
        if before == after or before in predecessors[after]:
            return before != after
        if precedes_or_equals(after, before):
            if editorial:
                return False
            raise ValueError("Proof Tree contains a premise cycle")
        successors[before].add(after)
        predecessors[after].add(before)
        return True

    for index, step in enumerate(model.steps):
        for premise in step.premises:
            add_dependency(locate(premise), index)

    # Present a quotient only after an existing equality for its domain.
    for index, step in enumerate(model.steps):
        quotient = step.conclusion
        if not isinstance(quotient, QuotientIsomorphismStatement):
            continue
        for later in range(index + 1, total):
            candidate = model.steps[later].conclusion
            if (later not in suppressed_exactness
                    and isinstance(candidate, Relation)
                    and candidate.relation_type is RelationType.EQUALITY
                    and candidate.lhs == quotient.domain):
                add_dependency(later, index, editorial=True)
                break

    # A single E step and an iterated E^r step use the same witness search:
    # match an existing Toda isomorphism to the existing generator's target,
    # then inspect an actual cyclic-transport inference using that theorem.
    for index, step in enumerate(model.steps):
        generator = step.conclusion
        if not isinstance(generator, (GeneratorSuspension, GeneratorImage)):
            continue
        if not isinstance(generator.map, TodaSuspensionMap):
            continue
        for iso_index, iso_step in enumerate(model.steps):
            iso = iso_step.conclusion
            if not (isinstance(iso, Toda45IsomorphismStatement)
                    and isinstance(iso.map, TodaIteratedSuspensionMap)
                    and iso.map.target_group == generator.map.target_group):
                continue
            transported_index = next((relation_index
                for relation_index, relation_step in enumerate(model.steps)
                if isinstance(relation_step.conclusion, Relation)
                and relation_step.conclusion.relation_type is RelationType.EQUALITY
                and relation_step.conclusion.lhs == iso.map.target_group
                and isinstance(relation_step.conclusion.rhs, FiniteCyclicGroup)
                and isinstance(relation_step.conclusion.rhs.generator, IteratedSuspension)
                and any(parent is iso_step or parent == iso_step
                        for parent in relation_step.premises)
                and any(isinstance(parent.conclusion, Relation)
                        and parent.conclusion.lhs == iso.map.source_group
                        for parent in relation_step.premises)
            ), None)
            if transported_index is None:
                continue
            source_indices = [locate(parent)
                for parent in model.steps[transported_index].premises
                if isinstance(parent.conclusion, Relation)
                and parent.conclusion.lhs == iso.map.source_group]
            if not source_indices:
                continue
            # When E itself is the transport, the generator image may be
            # explained after the isomorphism. If it is only the final link
            # of E^r, explain it after the transported group is established.
            anchor = (iso_index if generator.map.source_group == iso.map.source_group
                      else transported_index)
            # A single extension to the generator is valid only if all its
            # editorial prerequisites can be imposed without a proof cycle.
            if (not precedes_or_equals(index, anchor)
                    and all(not precedes_or_equals(index, source)
                            for source in source_indices)):
                for source in source_indices:
                    add_dependency(source, index, editorial=True)
                add_dependency(anchor, index, editorial=True)
            break

    indegree = [len(items) for items in predecessors]
    ready = []
    for index, degree in enumerate(indegree):
        if degree == 0:
            heappush(ready, index)
    ordered = []
    while ready:
        index = heappop(ready)
        ordered.append(index)
        for after in sorted(successors[index]):
            indegree[after] -= 1
            if indegree[after] == 0:
                heappush(ready, after)
    if len(ordered) != total:
        raise ValueError("Proof Tree has a cyclic dependency")

    # Keep the NarrativeOrderEntry API; no post-hoc deferred child rendering.
    return tuple(
        NarrativeOrderEntry(index)
        for index in ordered
        if index not in suppressed_exactness
    )
