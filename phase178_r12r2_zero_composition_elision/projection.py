"""Elide duplicate verified zero-transport prose, never proof steps."""
from __future__ import annotations


def remove_owned_paragraphs(lines, boundary, positions):
    """Remove only certified body paragraphs and their single blank separator."""
    positions = tuple(positions)
    if (len(set(positions)) != len(positions)
            or any(type(p) is not int or not boundary < p < len(lines) - 1
                   or not lines[p].strip() or lines[p + 1] != '' for p in positions)):
        return lines
    output = list(lines)
    for p in sorted(positions, reverse=True):
        del output[p:p + 2]
    return output


def project_zero_composition_elision(before, lines, model, protected=frozenset()):
    """Use original unique line ownership and verified identical typed factors.

    Only the same cited premise, same zero-transport rule, same typed map and
    ordered factors qualify. The later duplicate must feed a visibly retained
    verified right transport. Absorb the common base only if its exact formula
    is already in its own cited reference block and all its uses are covered.
    """
    from expression import Zero
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase176_r3r10_right_zero_transport_isolated.rule import RULE_NAME, right_zero_transport_inputs
    from phase175_r3r9_lemma57_explicit_public import rule as lemma_rule, source as lemma_source
    from phase176_r3r56_cited_source_display_isolated.projection import source_citation
    from phase177_r17r4r1_prop25_suspension_elision.projection import replayed
    from phase178_r12r1_suspension_composition_display.projection import unique_body_anchor
    from proof import ProofRule
    from toda_human_readable_renderer import render_toda_public_group_generator_latex

    if (model.status is not ProofSearchStatus.COMPLETE or model.open_goals
            or type(model.root_index) is not int or before.count('証明') != 1
            or len(before) != len(lines)):
        return lines, {}
    boundary = before.index('証明')
    if before[:boundary + 1] != lines[:boundary + 1]:
        return lines, {}
    steps, numbers = model.steps, model.step_citation_numbers
    lookup = {id(s): i for i, s in enumerate(steps)}
    if len(lookup) != len(steps) or len(numbers) != len(steps):
        return lines, {}
    parents = tuple(tuple(lookup.get(id(p)) for p in s.premises) for s in steps)
    if any(type(p) is not int or not 0 <= p < i for i, ps in enumerate(parents) for p in ps):
        return lines, {}
    try:
        scope = root_ancestor_step_indices(steps, model.root_index)
    except ValueError:
        return lines, {}
    citations = {c.number: c for c in model.citations}
    if len(citations) != len(model.citations) or any(n not in citations for ns in numbers for n in ns):
        return lines, {}
    blocked = set(protected) | {model.root_index}
    ancestry = []
    for i, ps in enumerate(parents):
        nodes = {i}
        for p in ps:
            nodes.update(ancestry[p])
        ancestry.append(nodes)
    def users(i):
        return {j for j, ps in enumerate(parents) if i in ps}
    def refs(i):
        return tuple(sorted({n for j in ancestry[i] if steps[j].rule is ProofRule.GIVEN for n in numbers[j]}))
    def eligible(i):
        return i in scope and i not in blocked and not numbers[i]
    def transport(i):
        s = steps[i]
        if (not eligible(i) or s.rule is not ProofRule.INFERENCE
                or s.inference_rule is None or s.inference_rule.name != RULE_NAME
                or len(parents[i]) != 1):
            return False
        base = steps[parents[i][0]].conclusion
        return right_zero_transport_inputs(s.conclusion, base) == (base,) and replayed(s)
    def canonical(i):
        value = steps[i].conclusion
        if type(value) is not GeneratorImage or type(value.target_generator) is not Zero:
            return None
        factors = typed_composition_factors(value.source_generator)
        if factors is None:
            return None
        latex = render_toda_public_group_generator_latex(value.source_generator)
        if not latex or '\n' in latex or '\r' in latex:
            return None
        return '$E(' + latex + ')=0$.'
    owners = {}
    positions = {}
    for i, step in enumerate(steps):
        old = typed_sentence(step.conclusion, step)
        pos = unique_body_anchor(before, boundary, old, refs(i))
        if pos is not None:
            positions[i] = pos
            owners.setdefault(pos, set()).add(i)
    def owned(i):
        pos = positions.get(i)
        return pos if pos is not None and owners[pos] == {i} else None
    candidates = []
    for later in sorted(scope):
        if not transport(later) or len(refs(later)) != 1:
            continue
        base, = parents[later]
        lp = owned(later)
        if lp is None or before[lp] == lines[lp]:
            continue
        later_value = steps[later].conclusion
        tag = f'[R{refs(later)[0]}]より, '
        formula = canonical(later)
        if not formula or lines[lp] != tag + formula:
            continue
        consumers = users(later)
        if len(consumers) != 1:
            continue
        child, = consumers
        if not transport(child) or parents[child] != (later,) or refs(child) != refs(later):
            continue
        cp = owned(child)
        child_formula = canonical(child)
        if cp is None or cp <= lp or not child_formula or lines[cp] != tag + child_formula:
            continue
        for earlier in sorted(scope):
            if earlier >= later or parents[earlier] != (base,) or not transport(earlier):
                continue
            if refs(earlier) != refs(later) or steps[earlier].inference_rule.literature_reference != steps[later].inference_rule.literature_reference:
                continue
            value = steps[earlier].conclusion
            if (value.map != later_value.map or value.target_generator != later_value.target_generator
                    or value.source_generator == later_value.source_generator
                    or typed_composition_factors(value.source_generator) != typed_composition_factors(later_value.source_generator)):
                continue
            ep = owned(earlier)
            if (ep is None or ep >= lp or before[ep] == lines[ep]
                    or before[ep] == before[lp] or lines[ep] != tag + formula
                    or canonical(earlier) != formula):
                continue
            if [p for p in range(boundary + 1, len(lines)) if lines[p] == tag + formula] != [ep, lp]:
                continue
            if not users(earlier) or not users(earlier) <= scope:
                continue
            candidates.append((earlier, later, child, base, ep, lp, cp, tag))
    if len(candidates) != 1:
        return lines, {}
    earlier, later, child, base, ep, lp, cp, tag = candidates[0]
    remove = [lp]
    base_removed = False
    # The base can be represented by the actual reference clause instead of
    # repeating it in the body. This is not inferred from citation text alone.
    if eligible(base) and users(base) == {earlier, later} and len(parents[base]) == 1:
        leaf, = parents[base]
        n, = refs(later)
        cite = citations[n]
        source = steps[leaf]
        base_step = steps[base]
        if (source.rule is ProofRule.GIVEN and not source.premises and numbers[leaf] == (n,)
                and leaf in cite.step_indices and base_step.rule is ProofRule.INFERENCE
                and replayed(base_step) and refs(base) == (n,)):
            formula = canonical(base)
            starts = [j for j, line in enumerate(lines[:boundary]) if line.startswith(f'**[R{n}] ')]
            if formula and len(starts) == 1:
                start, = starts
                end = next((j for j in range(start + 1, boundary) if lines[j].startswith('**[R')), boundary)
                hits = [j for j in range(boundary + 1, ep) if before[j] == tag + formula and lines[j] == tag + formula]
                # Older layout code already normalizes this particular base
                # sentence; permit its canonical anchor, but never a shared one.
                ref_formulas = {formula}
                # The existing source projector quotes the original unbraced
                # eta index. Accept that spelling only via its typed source
                # and registered assertion/reference pair, not text matching.
                if (base_step.inference_rule is not None
                        and base_step.inference_rule.name == lemma_rule.RULE_NAME
                        and lemma_rule.exact_lemma57_zero_image_goal(base_step.conclusion)
                        and source_citation(model, scope, leaf, lemma_source.TodaLemma57ExplicitNuPrimeZero(),
                                            lemma_source.ASSERTION_ID, lemma_source.REFERENCE_ID, 'Lemma 5.7') == cite):
                    ref_formulas.add('$' + lemma_source.PARTICULAR_CLAUSE.replace(r'\circ', '') + '$.')
                if len(hits) == 1 and ref_formulas.intersection(lines[start + 1:end]):
                    bp, = hits
                    if (owners.get(bp, {base}) == {base} and owned(base) in (None, bp)
                            and all(j == base or canonical(j) != formula for j in scope)):
                        remove.append(bp)
                        base_removed = True
    output = remove_owned_paragraphs(lines, boundary, remove)
    if output == lines:
        return lines, {}
    return output, {'retained_index': earlier, 'duplicate_index': later,
                    'consumer_index': child, 'base_index': base,
                    'base_display_absorbed': base_removed,
                    'removed_positions': sorted(remove),
                    'removed_sentences': [lines[p] for p in sorted(remove)]}
