"""Normalize verified zero suspension composition notation without elision."""
from __future__ import annotations


def unique_body_anchor(lines, boundary, sentence, numbers):
    if not sentence:
        return None
    candidates = {sentence}
    if len(numbers) == 1:
        candidates.add(f'[R{numbers[0]}]より, ' + sentence)
    matches = [i for i in range(boundary + 1, len(lines)) if lines[i] in candidates]
    return matches[0] if len(matches) == 1 else None


def project_owned_lines(lines, boundary, rows):
    """Replace only a uniquely owned body line, preserving its exact source tag."""
    output = list(lines)
    owners = {}
    for index, pos, old, new, numbers in rows:
        if pos is not None:
            owners.setdefault(pos, []).append(index)
    for index, pos, old, new, numbers in rows:
        if (pos is None or not boundary < pos < len(lines)
                or len(owners[pos]) != 1 or not old or not new or old == new):
            continue
        if lines[pos] == old:
            output[pos] = new
        elif len(numbers) == 1 and lines[pos] == f'[R{numbers[0]}]より, ' + old:
            output[pos] = f'[R{numbers[0]}]より, ' + new
    return output


def project_zero_suspension_composition(lines, model, protected=frozenset()):
    """Use typed proof ancestry; do not remove any sentence, step or reference."""
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase177_r17r4r1_prop25_suspension_elision.projection import replayed
    from proof import ProofRule
    from toda_human_readable_renderer import render_toda_public_group_generator_latex

    if (model.status is not ProofSearchStatus.COMPLETE or model.open_goals
            or type(model.root_index) is not int or lines.count('証明') != 1):
        return lines
    steps, numbers = model.steps, model.step_citation_numbers
    if len(steps) != len(numbers):
        return lines
    lookup = {id(s): i for i, s in enumerate(steps)}
    if len(lookup) != len(steps):
        return lines
    parents = tuple(tuple(lookup.get(id(p)) for p in s.premises) for s in steps)
    if any(type(p) is not int or not 0 <= p < i for i, ps in enumerate(parents) for p in ps):
        return lines
    try:
        scope = root_ancestor_step_indices(steps, model.root_index)
    except ValueError:
        return lines
    citations = {c.number for c in model.citations}
    if len(citations) != len(model.citations) or any(n not in citations for ns in numbers for n in ns):
        return lines
    ancestry = []
    for i, ps in enumerate(parents):
        nodes = {i}
        for p in ps:
            nodes.update(ancestry[p])
        ancestry.append(nodes)
    boundary = lines.index('証明')
    rows = []
    for i, step in enumerate(steps):
        value = step.conclusion
        refs = sorted({n for j in ancestry[i] if steps[j].rule is ProofRule.GIVEN for n in numbers[j]})
        old = typed_sentence(value, step)
        pos = unique_body_anchor(lines, boundary, old, refs)
        new = None
        if (pos is not None and i in scope and i != model.root_index and i not in protected
                and not numbers[i] and step.rule is ProofRule.INFERENCE
                and type(value) is GeneratorImage and type(value.map) is TodaSuspensionMap
                and type(value.target_generator) is Zero and type(value.source_generator) is Composition
                and old and old.startswith('$E(') and old.endswith(')=0$.')):
            domain, target = value.map.source_group, value.map.target_group
            factors = typed_composition_factors(value.source_generator)
            if (type(domain) is TodaPrimaryGroup and type(target) is TodaPrimaryGroup
                    and type(domain.group_dimension) is int and type(domain.sphere_dimension) is int
                    and factors is not None and len(factors) >= 2
                    and expression_endpoints(value.source_generator) == (domain.group_dimension, domain.sphere_dimension)
                    and target == TodaPrimaryGroup(domain.group_dimension + 1, domain.sphere_dimension + 1)
                    and replayed(step)):
                latex = render_toda_public_group_generator_latex(value.source_generator)
                if latex and '\n' not in latex and '\r' not in latex:
                    new = '$E(' + latex + ')=0$.'
        rows.append((i, pos, old, new, refs))
    return project_owned_lines(lines, boundary, rows)
