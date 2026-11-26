"""Display-only absorption of exclusive, verified factor suspension witnesses."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition, StableFamilyMemberDefinition,
    expand_cited_stable_family, cited_family_reference_sentence,
)
from phase169_r10e5_composite_generator_image.rule import component_image_obligations
from phase169_r10eq_r1_universal_stable_definition.definition import is_defined_stable_image
from phase177_r17r3_rank_two_quotient_display.projection import project_rank_two_quotient_reason
from phase177_r17r4r1_prop25_suspension_elision.projection import replayed
from proof import ProofRule

COMPOSITE = 'suspension preserves composition of separately proved maps'
FAMILY = 'consecutive cited stable-family instances imply generator image'
MEMBER = 'specialize cited stable-family definition'
STABLE = 'stable representative definitional suspension'


def named(step, name):
    return (step.rule is ProofRule.INFERENCE and step.inference_rule is not None
            and step.inference_rule.name == name and replayed(step))


def match_composition_branch(model, index):
    """Return the actual typed factor witnesses, source leaves and all branch nodes.

    Only two proved factor images of the existing composite inference are
    supported. Each factor is a cited consecutive-family image or a guarded
    stable definitional image. Unknown proof paths are left unchanged.
    """
    steps = model.steps
    numbers = model.step_citation_numbers
    if type(index) is not int or not 0 <= index < len(steps) or len(numbers) != len(steps):
        return None
    lookup = {id(s): i for i, s in enumerate(steps)}
    if len(lookup) != len(steps):
        return None
    parent_indices = {i: tuple(lookup.get(id(p)) for p in s.premises) for i, s in enumerate(steps)}
    if any(p is None for ps in parent_indices.values() for p in ps):
        return None
    step = steps[index]
    required = component_image_obligations(step.conclusion)
    if (required is None or not named(step, COMPOSITE) or numbers[index]
            or tuple(p.conclusion for p in step.premises) != required):
        return None
    factors = parent_indices[index]
    if len(set(factors)) != 2:
        return None
    nodes = {index, *factors}
    leaves = set()
    displays = []
    from phase168_r3_27_typed_statement_projection import typed_sentence
    for f in factors:
        factor = steps[f]
        if numbers[f]:
            return None
        text = typed_sentence(factor.conclusion, factor)
        if not text or not text.startswith('$E(') or not text.endswith('$.'):
            return None
        if named(factor, STABLE):
            if factor.premises or not is_defined_stable_image(factor.conclusion):
                return None
            displays.append(text)
            continue
        if not named(factor, FAMILY) or len(factor.premises) != 2:
            return None
        a, b = parent_indices[f]
        if a == b:
            return None
        for j in (a, b):
            member = steps[j]
            if (not named(member, MEMBER) or numbers[j] or len(member.premises) != 1
                    or type(member.conclusion) is not StableFamilyMemberDefinition):
                return None
        if parent_indices[a] != parent_indices[b]:
            return None
        leaf, = parent_indices[a]
        source = steps[leaf]
        if (source.rule is not ProofRule.GIVEN or source.premises
                or type(source.conclusion) is not CitedStableFamilyDefinition
                or len(numbers[leaf]) != 1
                or type(numbers[leaf][0]) is not int or numbers[leaf][0] <= 0
                or cited_family_reference_sentence(source.conclusion) is None):
            return None
        c, = numbers[leaf]
        cites = [x for x in model.citations if x.number == c and leaf in x.step_indices]
        if len(cites) != 1:
            return None
        # The already registered rule must propose these exact premises, not
        # merely share the rule's name or produce matching TeX.
        for j in (a, b, f):
            child = steps[j]
            options = expand_cited_stable_family(child.conclusion, (source.conclusion,))
            if not any(o.rule.name == child.inference_rule.name
                       and o.subgoals == tuple(p.conclusion for p in child.premises)
                       for o in options):
                return None
        nodes.update((a, b, leaf))
        leaves.add(leaf)
        displays.append(f'[R{c}]より, '+text)
    if not leaves or len(set(displays)) != len(displays):
        return None
    try:
        if root_ancestor_step_indices(steps, index) != nodes:
            return None
    except ValueError:
        return None
    if any(p >= i for i in nodes for p in parent_indices[i]):
        return None
    return frozenset(nodes), frozenset(leaves), tuple(displays)


def project_suspension_composition_display(lines, model, protected=frozenset()):
    """Edit only exact emitted body lines, keeping every proof node and citation."""
    if (model.status is not ProofSearchStatus.COMPLETE or model.open_goals
            or type(model.root_index) is not int
            or len(model.steps) != len(model.step_citation_numbers)
            or lines.count('証明') != 1):
        return lines, {}
    steps = model.steps
    try:
        scope = root_ancestor_step_indices(steps, model.root_index)
    except ValueError:
        return lines, {}
    lookup = {id(s): i for i, s in enumerate(steps)}
    if len(lookup) != len(steps):
        return lines, {}
    parents = {i: tuple(lookup.get(id(p)) for p in s.premises) for i, s in enumerate(steps)}
    if any(p is None for ps in parents.values() for p in ps):
        return lines, {}
    boundary = lines.index('証明')
    def unique(text):
        hits = [i for i in range(boundary+1,len(lines)) if lines[i] == text]
        return hits[0] if len(hits) == 1 else None
    candidates = []
    for q in sorted(scope):
        quotient = steps[q]
        if q in protected or q == model.root_index or model.step_citation_numbers[q]:
            continue
        reason = project_rank_two_quotient_reason(quotient.conclusion, quotient)
        if reason is None or not replayed(quotient):
            continue
        image = parents[q][-1]
        match = match_composition_branch(model, image)
        if match is None:
            continue
        branch, leaves, old = match
        if not branch <= scope or branch & (set(protected) | {q, model.root_index}):
            continue
        if any(i >= q for i in branch):
            continue
        # Exclusivity covers even hidden users outside the root ancestry.
        if any(i not in branch | {q} and branch.intersection(ps) for i, ps in parents.items()):
            continue
        if set(parents[q]).intersection(branch) != {image}:
            continue
        refs = sorted({n for i in leaves for n in model.step_citation_numbers[i]})
        # Require every transferred source to remain in the reference section
        # with its actual definition text, even after previous layout passes.
        valid_refs = True
        for i in leaves:
            n, = model.step_citation_numbers[i]
            ref_text = cited_family_reference_sentence(steps[i].conclusion)
            starts = [j for j,s in enumerate(lines[:boundary]) if s.startswith(f'**[R{n}] ')]
            if len(starts) != 1:
                valid_refs = False
                break
            start, = starts
            end = next((j for j in range(start+1,boundary) if lines[j].startswith('**[R')), boundary)
            if ref_text not in lines[start+1:end]:
                valid_refs = False
                break
        if not valid_refs:
            continue
        pieces = reason.split('. ')
        if len(pieces) != 3 or not pieces[1].startswith('また, $E('):
            continue
        first, middle, last = [p if p.endswith('.') else p+'.' for p in pieces]
        new = ', '.join(f'[R{n}]' for n in refs)+'を用いて, '+middle.removeprefix('また, ')
        positions = [unique(s) for s in (*old, first, middle, last)]
        if any(i is None for i in positions) or positions != sorted(set(positions)) or unique(new) is not None:
            continue
        # All visible factor witnesses must have the exact expected lines.
        # No intervening substantive sentence before the kernel is removed.
        a,b,k,m,l = positions
        if any(lines[j].strip() for j in range(a+1,k) if j != b):
            continue
        candidates.append((q, branch, refs, old, middle, new, (a,b), m))
    if len(candidates) != 1:
        return lines, {}
    q,branch,refs,old,middle,new,remove,replace_index = candidates[0]
    output = list(lines)
    output[replace_index] = new
    for i in sorted(remove, reverse=True):
        del output[i]
        if i < len(output) and not output[i]:
            del output[i]
    return output, {'quotient_index':q, 'branch_indices':sorted(branch),
                    'citation_numbers':refs, 'removed_sentences':list(old),
                    'replacement':new, 'previous_sentence':middle}
