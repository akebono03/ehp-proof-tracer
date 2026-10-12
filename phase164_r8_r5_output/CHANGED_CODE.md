# R8-R5 変更コード全文

新規 Factory 関数は以下。各ファイルの変更後 import と変更関数全文も続く。

```python
"""R8-R5 compatibility constructors, preserving legacy proof status.

These entry points centralize creation but do not certify the mathematical
truth, statement-registry enrollment or provenance of their inputs.
"""


def create_legacy_given_proof_step(
    *, conclusion, premises, rule, note=None,
    inference_rule=None, foundational_reference=None,
):
    """Construct a legacy GIVEN without promoting its trust or source status."""
    if rule is not ProofRule.GIVEN:
        raise ValueError("legacy GIVEN requires ProofRule.GIVEN")
    return ProofStep(
        conclusion=conclusion,
        premises=premises,
        rule=rule,
        note=note,
        inference_rule=inference_rule,
        foundational_reference=foundational_reference,
    )


def create_legacy_specialization_proof_step(
    *, conclusion, premises, rule, note=None,
    inference_rule=None, foundational_reference=None,
):
    """Preserve an already-checked legacy specialization; no new certification."""
    if rule is not ProofRule.INFERENCE:
        raise ValueError("legacy specialization requires ProofRule.INFERENCE")
    return ProofStep(
        conclusion=conclusion,
        premises=premises,
        rule=rule,
        note=note,
        inference_rule=inference_rule,
        foundational_reference=foundational_reference,
    )

```

## hopf_rules.py

### 変更後の import 全文

```python
from dataclasses import dataclass
from ehp_rules import (
  EHPZeroCompositionStatement,
)
from expression import (
  Composition,
  Expression,
  MapApplication,
  SmashProduct,
  Suspension,
  Zero,
)
from homomorphism_rules import (
  HomomorphismStatement,
)
from map_facts import EHP_H_MAP
from proof import (
  InferenceRule,
  LiteratureReference,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
)
```

### 変更クラス・関数全文

```python
def ehp_h_homomorphism_proof_step():
  return create_legacy_given_proof_step(
    conclusion=HomomorphismStatement(
      map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )
```

```python
def hopf_invariant_proof_step(
  statement,
):
  if not isinstance(
    statement,
    HopfInvariantStatement,
  ):
    raise TypeError(
      "statement must be a "
      "HopfInvariantStatement"
    )

  return create_legacy_given_proof_step(
    conclusion=statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )
```

## map_facts.py

### 変更後の import 全文

```python
from dataclasses import dataclass
from expression import MapSymbol
from map_property_rules import IsomorphismStatement
from proof import (
  ProofRule,
  ProofStep,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
)
```

### 変更クラス・関数全文

```python
class MapIsomorphismFact:
  typing: MapTypingFact

  def to_proof_step(
    self,
  ) -> ProofStep:
    return create_legacy_given_proof_step(
      conclusion=IsomorphismStatement(
        map=self.typing.map,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    )
```

## phase161_r7_premise_provenance_validation.py

### 変更後の import 全文

```python
from dataclasses import dataclass
from phase161_r5_backward_proof_reconstruction import (
    BackwardReconstructionResult,
    reconstruct_phase161_r5_goal,
)
from proof import (
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from phase164_r8_proofstep_factory import (
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def validate_phase161_r7_provenance(
    steps: tuple[ProofStep, ...],
    trusted_given_roots: tuple[ProofStep, ...],
) -> PremiseProvenanceReport:
    """Check reachable proof ancestry using exact premise identities and rules.

    A trusted root must be the same ProofStep object, not merely an equal
    dataclass value. No inference with missing premises is accepted.
    """
    if not isinstance(steps, tuple) or any(not isinstance(s, ProofStep) for s in steps):
        raise TypeError("steps must be a tuple of ProofStep")
    if not isinstance(trusted_given_roots, tuple) or any(
        not isinstance(s, ProofStep) for s in trusted_given_roots
    ):
        raise TypeError("trusted_given_roots must be a tuple of ProofStep")
    if any(s.rule is not ProofRule.GIVEN or s.premises for s in trusted_given_roots):
        raise ValueError("Trusted roots must be premise-free GIVEN steps")

    trusted_ids = {id(s) for s in trusted_given_roots}
    visiting = set()
    verified = set()
    inferences = set()
    roots = {}

    def visit(step: ProofStep) -> None:
        identity = id(step)
        if identity in verified:
            return
        if identity in visiting:
            raise ValueError("Cyclic proof ancestry")
        visiting.add(identity)
        try:
            if step.rule is ProofRule.GIVEN:
                if step.premises or identity not in trusted_ids:
                    raise ValueError("Untrusted GIVEN provenance root")
                roots[identity] = step
            elif step.rule is ProofRule.INFERENCE:
                if step.inference_rule is None or not step.premises:
                    raise ValueError("Unjustified INFERENCE ancestry")
                if any(not isinstance(p, ProofStep) for p in step.premises):
                    raise ValueError("Inference contains non-ProofStep premises")
                for premise in step.premises:
                    visit(premise)
                matches = (
                    candidate
                    for candidate in find_inference_matches_for_rule(
                        step.inference_rule, step.premises
                    )
                    if len(candidate.premises) == len(step.premises)
                    and all(a is b for a, b in zip(candidate.premises, step.premises))
                )
                if not any(
                    derive_inference_proof_step(match).conclusion == step.conclusion
                    for match in matches
                ):
                    raise ValueError("Inference does not follow from recorded premises")
                inferences.add(identity)
            else:
                raise ValueError("Unsupported proof-rule provenance")
            verified.add(identity)
        finally:
            visiting.remove(identity)

    for step in steps:
        visit(step)
    return PremiseProvenanceReport(
        verified_steps=len(verified),
        verified_inferences=len(inferences),
        trusted_roots_used=tuple(roots.values()),
    )
```

## phase162_group_structure_backward.py

### 変更後の import 全文

```python
from dataclasses import dataclass
from expression import MapApplication, MapSymbol, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from phase161_backward_goal_schema import BackwardGoalExpansion
from phase161_r5_backward_proof_reconstruction import reconstruct_phase161_r5_goal
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from phase164_r8_proofstep_factory import (
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def reconstruct_group_structure_goal(
    goal: Relation,
    suspension_map: TodaSuspensionMap,
    source_generator: object,
    ehp_leaf_steps: tuple[ProofStep, ...],
    group_leaf_steps: tuple[ProofStep, ...],
) -> GroupStructureBackwardResult:
    """Resolve goal-derived children and execute the registered transport rule.

    The two group leaves must already exist as supplied ProofSteps. Their
    provenance should be validated at the calling boundary; none is fabricated.
    """
    plan = expand_group_structure_goal(goal, suspension_map, source_generator)
    if not isinstance(group_leaf_steps, tuple) or any(not isinstance(s, ProofStep) for s in group_leaf_steps):
        raise TypeError("group_leaf_steps must be tuple[ProofStep, ...]")
    resolved = []
    for subgoal in plan.expansion.subgoals:
        if isinstance(subgoal, TodaSuspensionIsomorphismStatement):
            reconstructed = reconstruct_phase161_r5_goal(subgoal, ehp_leaf_steps)
            resolved.append(reconstructed.final_step)
        else:
            candidates = tuple(s for s in group_leaf_steps if s.conclusion == subgoal)
            if len(candidates) != 1:
                raise ValueError(f"Missing or ambiguous independent group premise: {subgoal!r}")
            resolved.append(candidates[0])
    matches = tuple(m for m in find_inference_matches_for_rule(plan.expansion.inference_rule, tuple(resolved)) if all(a is b for a, b in zip(m.premises, resolved)))
    if len(matches) != 1:
        raise ValueError("Group structure transport inference rejected its premises")
    final = derive_inference_proof_step(matches[0])
    if final.conclusion != goal or final.rule is not ProofRule.INFERENCE:
        raise ValueError("Group structure transport did not prove requested goal")
    return GroupStructureBackwardResult(
        goal=goal,
        final_step=final,
        derived_steps=reconstructed.derived_steps + (final,),
        leaf_steps=reconstructed.leaf_steps + tuple(resolved[1:]),
        plan=plan,
    )
```

## phase162_pi5_3_backward_selection.py

### 変更後の import 全文

```python
from dataclasses import dataclass, replace
from expression import Composition
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaPrimaryGroup,
)
from phase161_backward_goal_schema import BackwardGoalExpansion
from phase161_r5_backward_proof_reconstruction import (
    phase161_r5_target_goal,
    reconstruct_phase161_r5_goal,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_rules import (
    toda_eta_family_definition_statement,
    toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
    toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def _canonical_goals():
    eta2 = toda_eta_family_definition_statement(2).element
    eta3 = toda_eta_family_definition_statement(3).element
    # Match the name used by the existing n=3 transport production.
    # The eta-family definition currently represents this element as "η_4".
    eta4 = replace(toda_eta_family_definition_statement(4).element, name="η₄")
    pi4_2 = Relation(
        lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
        rhs=FiniteCyclicGroup(order=2, generator=Composition(left=eta2, right=eta3)),
        relation_type=RelationType.EQUALITY,
    )
    pi5_3 = Relation(
        lhs=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        rhs=FiniteCyclicGroup(order=2, generator=Composition(left=eta3, right=eta4)),
        relation_type=RelationType.EQUALITY,
    )
    # Derive the intermediate goal using the existing production, not a
    # separately assembled expression that might use different normalization.
    definition_steps = tuple(
        create_legacy_given_proof_step(
            conclusion=toda_eta_family_definition_statement(i),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for i in (3, 4)
    )
    rule = toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
    candidates = tuple(find_inference_matches_for_rule(rule, definition_steps))
    if len(candidates) != 1:
        raise ValueError("Unable to derive unique canonical eta-square bridge")
    bridge_step = derive_inference_proof_step(candidates[0])
    bridge = bridge_step.conclusion
    if bridge_step.rule is not ProofRule.INFERENCE or not isinstance(bridge, Relation):
        raise ValueError("Canonical bridge production returned an invalid conclusion")
    return pi4_2, pi5_3, bridge
```

```python
def _apply_unique(rule, premises, goal):
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, premises)
        if len(match.premises) == len(premises)
        and all(a is b for a, b in zip(match.premises, premises))
    )
    if len(matches) != 1:
        raise ValueError(f"Exactly one inference match required for {goal!r}: {len(matches)}")
    step = derive_inference_proof_step(matches[0])
    if step.rule is not ProofRule.INFERENCE or step.conclusion != goal:
        raise ValueError("Existing production did not prove the requested goal")
    return step
```

## phase162_pi5_3_web_replay.py

### 変更後の import 全文

```python
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase162_pi5_3_backward_selection import (
    _canonical_goals,
    reconstruct_phase162_pi5_3_group_goal,
)
from phase162_web_narrative_integration import _phase162_ehp_leaves
from probes.probe_phase50_capabilities import build_phase50_representative_result
from probes.probe_phase56_capabilities import build_phase56_representative_result
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_match
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_rules import (
    toda_52_pi4_2_finite_cyclic_transport_inference_rule,
    toda_eta_family_definition_statement,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_phase162_pi5_3_web_replay(max_depth: int = 40):
    """Construct a new, inference-backed root, then reuse the standard replay API."""
    phase50 = build_phase50_representative_result()
    phase56 = build_phase56_representative_result()
    pi4_3_steps = phase50["final_group_steps"]
    toda52_steps = phase56["composition_isomorphism_steps"]
    if len(pi4_3_steps) != 1 or len(toda52_steps) != 1:
        raise ValueError("Expected unique independently proved Toda (5.2) premises")

    match = find_inference_match(
        toda_52_pi4_2_finite_cyclic_transport_inference_rule(),
        (pi4_3_steps[0], toda52_steps[0]),
    )
    if match is None:
        raise ValueError("Could not prove source pi_4^2 group structure")
    source_step = derive_inference_proof_step(match)
    eta_steps = tuple(
        create_legacy_given_proof_step(
            conclusion=toda_eta_family_definition_statement(index),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for index in (3, 4)
    )
    prop51, hopf_eta5, exactness = _phase162_ehp_leaves()
    ehp_leaves = (prop51, hopf_eta5) + exactness
    _, goal, _ = _canonical_goals()
    reconstruction = reconstruct_phase162_pi5_3_group_goal(
        goal, source_step, eta_steps, ehp_leaves
    )
    root = reconstruction.final_step
    if root.conclusion != goal or root.rule is not ProofRule.INFERENCE:
        raise ValueError("The reconstructed root does not prove pi_5^3")
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        raise ValueError("The reconstructed goal is not a finite cyclic group")
    entry = ProofRepositoryEntry(
        key="phase162-pi5-3-reconstructed-web",
        step=root,
        theorem="Toda Proposition 5.3",
        phase="162",
    )
    group_result = TodaGroupResult(
        target=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        group_structure=goal.rhs,
        generators=(goal.rhs.generator,),
        generator_orders=(goal.rhs.order,),
        source_entry=entry,
        proof_step=root,
    )
    replay = build_toda_group_result_proof_replay(group_result, max_depth=max_depth)
    if replay.root_step is not root:
        raise ValueError("Web replay replaced the newly constructed root")
    return replay
```

## phase162_r2_existing_proof_connection.py

### 変更後の import 全文

```python
from dataclasses import dataclass
from homotopy_groups import FiniteCyclicGroup, TodaSuspensionMap
from phase161_r7_premise_provenance_validation import (
    PremiseProvenanceReport,
    validate_phase161_r7_provenance,
)
from phase162_group_structure_backward import (
    GroupStructureBackwardResult,
    expand_group_structure_goal,
    reconstruct_group_structure_goal,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_rules import toda_prop53_n3_eta_square_suspension_bridge_inference_rule
from phase164_r8_proofstep_factory import (
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def reconstruct_phase162_r2_from_existing_proofs(
    goal: Relation,
    suspension_map: TodaSuspensionMap,
    source_structure_steps: tuple[ProofStep, ...],
    eta_definition_steps: tuple[ProofStep, ...],
    ehp_leaf_steps: tuple[ProofStep, ...],
    trusted_given_roots: tuple[ProofStep, ...],
) -> ExistingProofConnectionResult:
    """Resolve the root group goal using real source and eta-family evidence.

    The caller supplies existing proof steps, not a final pi_5^3 proof.
    Only a matching independently derived source-group relation is accepted.
    The eta-square bridge is executed from its original definition premises.
    All reachable inference ancestry is checked against explicit GIVEN roots.
    """
    if not isinstance(source_structure_steps, tuple) or any(
        not isinstance(step, ProofStep) for step in source_structure_steps
    ):
        raise TypeError("source_structure_steps must be tuple[ProofStep, ...]")
    if not isinstance(eta_definition_steps, tuple) or any(
        not isinstance(step, ProofStep) for step in eta_definition_steps
    ):
        raise TypeError("eta_definition_steps must be tuple[ProofStep, ...]")
    if not isinstance(ehp_leaf_steps, tuple) or any(
        not isinstance(step, ProofStep) for step in ehp_leaf_steps
    ):
        raise TypeError("ehp_leaf_steps must be tuple[ProofStep, ...]")

    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        raise ValueError("Expected target group equality goal")
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        raise ValueError("Expected finite cyclic target group")

    candidates = tuple(
        step for step in source_structure_steps
        if step.rule is ProofRule.INFERENCE
        and isinstance(step.conclusion, Relation)
        and step.conclusion.relation_type is RelationType.EQUALITY
        and step.conclusion.lhs == suspension_map.source_group
        and isinstance(step.conclusion.rhs, FiniteCyclicGroup)
        and step.conclusion.rhs.order == goal.rhs.order
    )
    if len(candidates) != 1:
        raise ValueError("Missing or ambiguous derived source-group structure")
    source_step = candidates[0]
    source_generator = source_step.conclusion.rhs.generator
    plan = expand_group_structure_goal(goal, suspension_map, source_generator)
    if source_step.conclusion != plan.source_structure_goal:
        raise ValueError("Source structure does not match backward goal")

    bridge_rule = toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
    bridge_matches = tuple(
        match for match in find_inference_matches_for_rule(
            bridge_rule, eta_definition_steps
        )
        if len(match.premises) == len(eta_definition_steps)
        and all(a is b for a, b in zip(match.premises, eta_definition_steps))
    )
    if len(bridge_matches) != 1:
        raise ValueError("Missing or ambiguous eta-family definition bridge")
    bridge_step = derive_inference_proof_step(bridge_matches[0])
    if bridge_step.conclusion != plan.generator_image_goal:
        raise ValueError("Derived generator image does not match backward goal")

    result = reconstruct_group_structure_goal(
        goal=goal,
        suspension_map=suspension_map,
        source_generator=source_generator,
        ehp_leaf_steps=ehp_leaf_steps,
        group_leaf_steps=(source_step, bridge_step),
    )
    provenance = validate_phase161_r7_provenance(
        (result.final_step,), trusted_given_roots
    )
    return ExistingProofConnectionResult(
        reconstruction=result,
        source_structure_step=source_step,
        generator_image_step=bridge_step,
        provenance=provenance,
    )
```

## phase162_r3j_inference_rule_audit.py

### 変更後の import 全文

```python
from collections import Counter
from dataclasses import dataclass
from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace
from phase162_r3i_semantic_sidecar_audit import build_phase162_r3i_sidecar_audit
from proof import (
    InferenceRule,
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_group_proof_presentation import TodaGroupProofPresentation
from phase164_r8_proofstep_factory import (
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def classify_r3j_inference_rule(record) -> R3JRuleEntry:
    """Replay a single existing inference with its original direct premises.

    This reports metadata and replayability; it does not infer any prose reason.
    """
    step = record.step
    if not isinstance(step, ProofStep) or step.rule is not ProofRule.INFERENCE:
        raise TypeError('R3-J requires an INFERENCE ProofStep')
    rule = step.inference_rule
    if rule is not None and not isinstance(rule, InferenceRule):
        raise TypeError('inference_rule must be InferenceRule or None')

    description = rule.description if rule is not None else None
    patterns = tuple(rule.premise_patterns) if rule is not None else ()
    exact_count = 0
    conclusion_count = 0
    details = []
    if rule is None:
        category = 'INFERENCE_RULE_MISSING'
    elif not step.premises:
        category = 'INFERENCE_PREMISES_MISSING'
    else:
        try:
            for match in find_inference_matches_for_rule(rule, step.premises):
                if len(match.premises) != len(step.premises):
                    continue
                if not all(actual is expected for actual, expected in zip(match.premises, step.premises)):
                    continue
                exact_count += 1
                try:
                    derived = derive_inference_proof_step(match)
                except (TypeError, ValueError, AttributeError) as exc:
                    details.append('apply_error:' + type(exc).__name__ + ':' + str(exc))
                    continue
                if derived.conclusion == step.conclusion:
                    conclusion_count += 1
        except (TypeError, ValueError, AttributeError) as exc:
            details.append('match_error:' + type(exc).__name__ + ':' + str(exc))
        if conclusion_count > 0:
            category = 'RULE_REPLAY_VERIFIED_PROSE_UNAUDITED'
        elif details:
            category = 'RULE_REPLAY_ERROR_REVIEW'
        elif exact_count:
            category = 'RULE_CONCLUSION_MISMATCH'
        else:
            category = 'RULE_NO_EXACT_PREMISE_MATCH'

    return R3JRuleEntry(
        index=record.index,
        statement_type=type(step.conclusion).__name__,
        inference_rule_name=rule.name if rule is not None else None,
        description=description,
        premise_indices=record.premise_indices,
        premise_types=tuple(type(p.conclusion).__name__ for p in step.premises),
        premise_pattern_count=len(patterns),
        premise_pattern_types=tuple(
            pattern.statement_type.__name__ if pattern.statement_type is not None else None
            for pattern in patterns
        ),
        has_conclusion_builder=rule.conclusion_builder is not None if rule is not None else False,
        has_conclusion_pattern=rule.conclusion_pattern is not None if rule is not None else False,
        has_match_guard=rule.match_guard is not None if rule is not None else False,
        has_literature_reference=rule.literature_reference is not None if rule is not None else False,
        classification=category,
        exact_identity_match_count=exact_count,
        matching_conclusion_count=conclusion_count,
        details=tuple(details),
    )
```

## phase162_reference_boundary.py

### 変更後の import 全文

```python
from __future__ import annotations
from dataclasses import replace
from proof import (
    FoundationalReferenceIdentity, InferenceRule, LiteratureReference,
    PremisePattern, ProofRule, ProofStep, apply_inference_match,
    find_inference_match,
)
from phase161_r7_premise_provenance_validation import validate_phase161_r7_provenance
from toda_literature_statement_boundary import get_toda_fixed_statement_component
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def cite_verified_fixed_statement(
    witness: ProofStep,
    reference_locator: str,
    component_key: str,
    expected_conclusion: object,
) -> ProofStep:
    """Collapse verified ancestry at a registered citation boundary.

    The caller must identify the exact fixed statement and pass the mathematical
    conclusion it claims. A registered component is necessary, not sufficient,
    to establish the external truth of that mathematical citation.
    """
    if not isinstance(witness, ProofStep):
        raise TypeError("witness must be a ProofStep")
    if witness.rule is not ProofRule.INFERENCE or not witness.premises:
        raise ValueError("Citation witness must be a derived inference")
    if witness.conclusion != expected_conclusion:
        raise ValueError("Citation statement does not match verified witness")
    component = get_toda_fixed_statement_component(reference_locator, component_key)
    if component.reference_locator != reference_locator or component.component_key != component_key:
        raise ValueError("Registered component mismatch")
    validate_phase161_r7_provenance((witness,), _trusted_given_ancestors(witness))
    citation_identity = FoundationalReferenceIdentity(
        key=f"literature:{reference_locator}:{component_key}",
        label=reference_locator,
    )
    citation_leaf = create_legacy_given_proof_step(
        conclusion=witness.conclusion,
        premises=(),
        rule=ProofRule.GIVEN,
        foundational_reference=citation_identity,
    )
    citation_rule = InferenceRule(
        name="phase162_verified_literature_citation",
        description="Use a verified fixed literature statement",
        premise_patterns=(PremisePattern(proof_rule=ProofRule.GIVEN),),
        match_guard=lambda premises, bindings=(): (
            len(premises) == 1
            and premises[0].foundational_reference == citation_identity
            and premises[0].conclusion == expected_conclusion
        ),
        conclusion_builder=lambda premises: premises[0].conclusion,
        literature_reference=LiteratureReference(
            label="Toda " + reference_locator,
            locator=reference_locator,
        ),
    )
    match = find_inference_match(citation_rule, (citation_leaf,))
    if match is None:
        raise ValueError("Citation inference failed to match the trusted leaf")
    result = derive_inference_proof_step(match)
    return replace(result, foundational_reference=citation_identity)
```

## phase162_web_narrative_integration.py

### 変更後の import 全文

```python
from phase162_reference_boundary import cite_verified_fixed_statement
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    derive_inference_proof_step,
)
from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    reconstruct_phase161_r7_validated_goal,
)
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from probes.probe_phase55_capabilities import build_phase55_representative_result
from probes.probe_phase58_capabilities import build_phase58_representative_result
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from homotopy_groups import FiniteCyclicGroup, TodaSuspensionMap
from phase162_r2_existing_proof_connection import (
    reconstruct_phase162_r2_from_existing_proofs,
)
from phase162_r3_narrative_connection import render_phase162_r3_narrative
from probes.probe_phase50_capabilities import build_phase50_representative_result
from probes.probe_phase56_capabilities import build_phase56_representative_result
from proof import Relation, RelationType, apply_inference_match, find_inference_match
from toda_rules import (
    toda_52_pi4_2_finite_cyclic_transport_inference_rule,
    toda_eta_family_definition_statement,
    toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
)
```

### 変更クラス・関数全文

```python
def _build_phase162_legacy_validated_isomorphism_markdown() -> str:
    """Render only after the exact provenance roots pass R7 validation."""
    prop51 = build_phase55_representative_result()["prop51_steps"][0]
    hopf_eta5 = cite_verified_fixed_statement(
        build_phase58_representative_result()["final_hopf_step"],
        reference_locator="(5.3)",
        component_key="nu_prime_hopf_relation",
        expected_conclusion=build_phase58_representative_result()["expected_final_hopf"],
    )

    pi_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    pi_4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi_5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    pi_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    pi_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
    pi_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)

    windows = (
        (pi_5_3, pi_5_5, pi_3_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_4_2, pi_5_3, pi_5_5, EHP_E_MAP, EHP_H_MAP),
        (pi_6_3, pi_6_5, pi_4_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_6_5, pi_4_2, pi_5_3, EHP_DELTA_MAP, EHP_E_MAP),
    )
    exactness = tuple(
        create_legacy_given_proof_step(
            conclusion=TodaProp42ExactnessStatement(
                window=TodaEHPExactnessWindow(
                    source_term=source,
                    middle_term=middle,
                    target_term=target,
                    first_map=first,
                    second_map=second,
                )
            ),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for source, middle, target, first, second in windows
    )
    leaves = (prop51, hopf_eta5) + exactness
    trusted = {}
    visited = set()

    def collect(step: ProofStep) -> None:
        key = id(step)
        if key in visited:
            return
        visited.add(key)
        if step.rule is ProofRule.GIVEN:
            trusted[key] = step
        for premise in step.premises:
            collect(premise)

    for leaf in leaves:
        collect(leaf)

    validated = reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), leaves, tuple(trusted.values())
    )
    presentation = build_validated_backward_proof_presentation(validated)
    markdown = render_validated_backward_proof_markdown(presentation)
    return _format_phase162_proof_sentences(
        _compose_phase162_group_conclusion(markdown)
    )
```

```python
def _build_phase162_existing_group_connection():
    """Build the group-root proof from independently derived existing evidence."""
    phase50 = build_phase50_representative_result()
    phase56 = build_phase56_representative_result()
    pi4_3_steps = phase50["final_group_steps"]
    toda52_steps = phase56["composition_isomorphism_steps"]
    if len(pi4_3_steps) != 1 or len(toda52_steps) != 1:
        raise ValueError("Expected one independently derived source premise of each kind")
    transport = toda_52_pi4_2_finite_cyclic_transport_inference_rule()
    match = find_inference_match(transport, (pi4_3_steps[0], toda52_steps[0]))
    if match is None:
        raise ValueError("Could not derive pi_4^2 from the existing Toda (5.2) evidence")
    source_step = derive_inference_proof_step(match)
    if source_step.rule is not ProofRule.INFERENCE:
        raise ValueError("Source group must be derived")

    pi4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    if source_step.conclusion.lhs != pi4_2 or not isinstance(source_step.conclusion.rhs, FiniteCyclicGroup):
        raise ValueError("Existing source proof does not establish expected cyclic group")
    eta_definitions = tuple(
        create_legacy_given_proof_step(
            conclusion=toda_eta_family_definition_statement(index),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for index in (3, 4)
    )
    source_generator = source_step.conclusion.rhs.generator
    bridge_rule = toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
    bridge_match = find_inference_match(bridge_rule, eta_definitions)
    if bridge_match is None:
        raise ValueError("Existing eta-family definitions do not derive the image")
    bridge_step = derive_inference_proof_step(bridge_match)
    from expression import Composition, Suspension
    if (
        not isinstance(bridge_step.conclusion, Relation)
        or bridge_step.conclusion.relation_type is not RelationType.EQUALITY
        or bridge_step.conclusion.lhs != Suspension(expression=source_generator)
        or not isinstance(bridge_step.conclusion.rhs, Composition)
        or bridge_step.conclusion.rhs.left.generator.family != "η"
        or bridge_step.conclusion.rhs.left.generator.index != 3
        or bridge_step.conclusion.rhs.right.generator.family != "η"
        or bridge_step.conclusion.rhs.right.generator.index != 4
    ):
        raise ValueError("Eta-family bridge does not match the source and target generators")
    goal = Relation(
        lhs=pi5_3,
        rhs=FiniteCyclicGroup(
            order=source_step.conclusion.rhs.order,
            generator=bridge_step.conclusion.rhs,
        ),
        relation_type=RelationType.EQUALITY,
    )
    suspension_map = TodaSuspensionMap(source_group=pi4_2, target_group=pi5_3)
    prop51, hopf_eta5, exactness = _phase162_ehp_leaves()
    ehp_leaves = (prop51, hopf_eta5) + exactness
    roots = {}
    seen = set()

    def collect(step: ProofStep) -> None:
        identity = id(step)
        if identity in seen:
            return
        seen.add(identity)
        if step.rule is ProofRule.GIVEN:
            roots[identity] = step
        for premise in step.premises:
            collect(premise)

    for step in (source_step,) + eta_definitions + ehp_leaves:
        collect(step)
    return reconstruct_phase162_r2_from_existing_proofs(
        goal=goal,
        suspension_map=suspension_map,
        source_structure_steps=(source_step,),
        eta_definition_steps=eta_definitions,
        ehp_leaf_steps=ehp_leaves,
        trusted_given_roots=tuple(roots.values()),
    )
```

```python
def _phase162_ehp_leaves():
    """Reuse the original independent EHP input leaves, not an iso conclusion."""
    prop51 = build_phase55_representative_result()["prop51_steps"][0]
    hopf_eta5 = cite_verified_fixed_statement(
        build_phase58_representative_result()["final_hopf_step"],
        reference_locator="(5.3)",
        component_key="nu_prime_hopf_relation",
        expected_conclusion=build_phase58_representative_result()["expected_final_hopf"],
    )
    pi_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    pi_4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi_5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    pi_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    pi_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
    pi_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)
    windows = (
        (pi_5_3, pi_5_5, pi_3_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_4_2, pi_5_3, pi_5_5, EHP_E_MAP, EHP_H_MAP),
        (pi_6_3, pi_6_5, pi_4_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_6_5, pi_4_2, pi_5_3, EHP_DELTA_MAP, EHP_E_MAP),
    )
    exactness = tuple(
        create_legacy_given_proof_step(
            conclusion=TodaProp42ExactnessStatement(
                window=TodaEHPExactnessWindow(
                    source_term=source,
                    middle_term=middle,
                    target_term=target,
                    first_map=first,
                    second_map=second,
                )
            ),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for source, middle, target, first, second in windows
    )
    return prop51, hopf_eta5, exactness
```

## phase164_r5_web_registry_connection.py

### 変更後の import 全文

```python
from __future__ import annotations
from pathlib import Path
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from phase162_web_narrative_integration import _phase162_ehp_leaves
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r8_registry_reconstruction import (
    _known_trusted_roots,
    reconstruct_phase164_r4_r8_pi5_3,
)
from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_rules import toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule
from phase164_r8_proofstep_factory import (
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_phase164_r5_web_pi5_3_proof(*, max_depth: int = 2):
    """Build the group root using an R4-R8-validated, registry-backed map proof.

    The original group/source and generator-bridge subproofs stay INFERENCE.
    R4-R8 supplies the *same* typed literature-connected isomorphism step,
    not a display-only replacement. No test fixture is imported.
    """
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an integer")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    manifest = Path("phase163_r4_r94_output/manifest.json")
    if not manifest.is_file():
        raise ValueError("R4-R8 source manifest missing; Web proof cannot be certified")

    prop51, hopf, exactness = _phase162_ehp_leaves()
    ehp_leaves = (prop51, hopf) + exactness
    fixed = reconstruct_phase164_r4_r8_pi5_3(
        audit_current_repository(manifest),
        ehp_leaves,
        _known_trusted_roots(ehp_leaves),
        user_confirmed_original=True,
    )
    isomorphism_step = fixed.validated.reconstruction.final_step
    if isomorphism_step.rule is not ProofRule.INFERENCE:
        raise ValueError("R4-R8 did not derive an isomorphism")

    previous_replay = build_phase162_pi5_3_web_replay(max_depth=2)
    previous_root = previous_replay.root_step
    if previous_root.rule is not ProofRule.INFERENCE or len(previous_root.premises) != 3:
        raise ValueError("Phase 162 group root structure changed")
    source_step, prior_isomorphism, generator_bridge = previous_root.premises
    if prior_isomorphism.conclusion != isomorphism_step.conclusion:
        raise ValueError("registry-backed isomorphism differs from group requirement")
    if source_step.rule is not ProofRule.INFERENCE or generator_bridge.rule is not ProofRule.INFERENCE:
        raise ValueError("group source or generator bridge is not inferred")

    rule = toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule()
    premises = (source_step, isomorphism_step, generator_bridge)
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, premises)
        if len(match.premises) == len(premises)
        and all(actual is expected for actual, expected in zip(match.premises, premises))
    )
    if len(matches) != 1:
        raise ValueError("registry-backed group transport has no unique match")
    group_step = derive_inference_proof_step(matches[0])
    if group_step.rule is not ProofRule.INFERENCE or group_step.conclusion != previous_root.conclusion:
        raise ValueError("group conclusion did not match the original group result")
    if tuple(group_step.premises) != premises:
        raise ValueError("group proof lost the registry-backed isomorphism")

    goal = group_step.conclusion
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        raise ValueError("unexpected target group structure")
    entry = ProofRepositoryEntry(
        key="phase164-r5-registry-backed-pi5-3-web",
        step=group_step,
        theorem="Toda Proposition 5.3",
        phase="164 R5",
    )
    result = TodaGroupResult(
        target=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        group_structure=goal.rhs,
        generators=(goal.rhs.generator,),
        generator_orders=(goal.rhs.order,),
        source_entry=entry,
        proof_step=group_step,
    )
    replay = build_toda_group_result_proof_replay(result, max_depth=max_depth)
    if replay.root_step is not group_step:
        raise ValueError("replay did not preserve the registry-backed group root")

    # Render the actual group-root proof through the shared pipeline.
    # No pi_5^3-specific sentences or concatenated markdown are permitted.
    presentation = build_toda_group_proof_presentation(replay)
    narrative = render_toda_group_proof_narrative_markdown(presentation)
    if not narrative or "## 証明" not in narrative:
        raise ValueError("common group narrative unavailable")
    return replay, narrative
```

## repository_foundational_group_specialization.py

### 変更後の import 全文

```python
from expression import (
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_proof_scope import (
  build_repository_proof_scope,
)
from toda_group_query import TodaGroupQuery
from toda_group_result import (
  normalize_toda_group_result,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    create_legacy_specialization_proof_step,
)
```

### 変更クラス・関数全文

```python
def _build_identity_group_step(
  n: int,
) -> ProofStep:
  iota_n = HomotopyElement(
    name=f"ι_{n}",
    dimension=n,
    generator=GeneratorSymbol(
      family="ι",
      index=n,
    ),
  )

  return create_legacy_given_proof_step(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=n,
        sphere_dimension=n,
      ),
      rhs=FreeCyclicGroup(
        generator=iota_n,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
    note=(
      "Phase 130-10 foundational identity group "
      "pi_n(S^n) = Z{iota_n}"
    ),
  )
```

```python
def _build_connectivity_zero_step(
  query: TodaGroupQuery,
) -> ProofStep:
  return create_legacy_given_proof_step(
    conclusion=TodaPrimaryGroupZeroStatement(
      group=query.target,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
    note=(
      "Phase 130-10 foundational sphere "
      "connectivity: pi_m(S^n)=0 for 1 <= m < n"
    ),
  )
```

```python
def _specialize_circle_higher_zero_step(
  symbolic_step: ProofStep,
  query: TodaGroupQuery,
) -> ProofStep:
  if query.n != 1 or query.k < 1:
    raise ValueError(
      "query must have n=1 and k>=1"
    )

  if not _is_symbolic_circle_higher_zero_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the Phase 56 "
      "symbolic circle higher-homotopy zero"
    )

  return create_legacy_specialization_proof_step(
    conclusion=TodaPrimaryGroupZeroStatement(
      group=query.target,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-10 concrete specialization of "
      "Phase 56 pi_(i-1)^1 zero"
    ),
  )
```

## repository_nu5_eta8_suspension_zero_specialization.py

### 変更後の import 全文

```python
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import ProofRepository
from repository_operation_query import (
  RepositoryCompositionQuery,
  RepositoryMapOperationQuery,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatch,
  RepositoryOperationQueryMatchKind,
  RepositoryOperationQueryResult,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  build_repository_proof_scope,
)
from phase164_r8_proofstep_factory import (
    create_legacy_specialization_proof_step,
)
```

### 変更クラス・関数全文

```python
def specialize_nu5_eta8_suspension_zero_step(
  pi10_6_zero_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    pi10_6_zero_step,
    ProofStep,
  ):
    raise TypeError(
      "pi10_6_zero_step must be a ProofStep"
    )

  if not _is_derived_pi10_6_zero_step(
    pi10_6_zero_step
  ):
    raise ValueError(
      "pi10_6_zero_step must be the derived "
      "Toda Proposition 5.8 pi_10^6 zero step "
      "with pi_9^5 = Z/2{nu_5 eta_8} provenance"
    )

  pi9_5_step = (
    _find_pi9_5_nu5_eta8_premise(
      pi10_6_zero_step
    )
  )

  if pi9_5_step is None:
    raise RuntimeError(
      "validated pi_10^6 zero step lost "
      "its pi_9^5 provenance"
    )

  nu5_eta8 = (
    pi9_5_step
    .conclusion
    .rhs
    .generator
  )

  return create_legacy_specialization_proof_step(
    conclusion=Relation(
      lhs=Suspension(
        expression=nu5_eta8,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(
      pi10_6_zero_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 128-2 theorem-specific handoff: "
      "E(nu_5 eta_8)=0 from the derived "
      "Toda Proposition 5.8 target group pi_10^6=0"
    ),
  )
```

## repository_nu5_stable_bridge_specialization.py

### 変更後の import 全文

```python
from expression import (
  GeneratorSymbol,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Suspension,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import ProofRepository
from repository_operation_query import (
  RepositoryGeneratorQuery,
  RepositoryMapOperationQuery,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatch,
  RepositoryOperationQueryMatchKind,
  RepositoryOperationQueryResult,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  build_repository_proof_scope,
)
from toda_rules import (
  toda_nu_family_definition_statement,
)
from phase164_r8_proofstep_factory import (
    create_legacy_specialization_proof_step,
)
```

### 変更クラス・関数全文

```python
def specialize_nu5_stable_bridge_step(
  symbolic_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    symbolic_step.conclusion
    != _symbolic_nu5_stable_bridge_relation()
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "nu_5 stable-family bridge"
    )

  nu_5 = (
    toda_nu_family_definition_statement(
      5
    ).element
  )

  nu_6 = (
    toda_nu_family_definition_statement(
      6
    ).element
  )

  return create_legacy_specialization_proof_step(
    conclusion=Relation(
      lhs=Suspension(
        expression=nu_5,
      ),
      rhs=nu_6,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 114-3 theorem-specific concrete "
      "specialization of the Toda Proposition 5.6 "
      "nu_5 stable-family bridge at n=6"
    ),
  )
```

## repository_nu_prime_suspension_membership_specialization.py

### 変更後の import 全文

```python
from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  GeneratorSymbol,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import ProofRepository
from repository_operation_query import (
  RepositoryGeneratorQuery,
  RepositoryMapOperationQuery,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatch,
  RepositoryOperationQueryMatchKind,
  RepositoryOperationQueryResult,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  build_repository_proof_scope,
)
from phase164_r8_proofstep_factory import (
    create_legacy_specialization_proof_step,
)
```

### 変更クラス・関数全文

```python
def specialize_nu_prime_suspension_membership_step(
  group_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    group_step,
    ProofStep,
  ):
    raise TypeError(
      "group_step must be a ProofStep"
    )

  if not _is_prop56_pi7_4_decomposition_step(
    group_step
  ):
    raise ValueError(
      "group_step must prove the Toda Proposition 5.6 "
      "pi_7^4 decomposition with E(nu_prime) as the "
      "order-four generator"
    )

  e_nu_prime = (
    group_step
    .conclusion
    .rhs
    .summands[
      1
    ]
    .generator
  )

  return create_legacy_specialization_proof_step(
    conclusion=HomotopyGroupMembershipStatement(
      element=e_nu_prime,
      group_dimension=7,
      sphere_dimension=4,
    ),
    premises=(
      group_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 129-4 theorem-specific membership handoff "
      "from the Toda Proposition 5.6 pi_7^4 decomposition"
    ),
  )
```

## repository_sigma11_suspension_specialization.py

### 変更後の import 全文

```python
from expression import (
  GeneratorSymbol,
  ScalarSymbol,
  Suspension,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import ProofRepository
from repository_operation_query import (
  RepositoryGeneratorQuery,
  RepositoryMapOperationQuery,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatch,
  RepositoryOperationQueryMatchKind,
  RepositoryOperationQueryResult,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  build_repository_proof_scope,
)
from toda_rules import (
  TodaSigmaFamilyDefinitionStatement,
  toda_sigma_family_definition_statement,
)
from phase164_r8_proofstep_factory import (
    create_legacy_specialization_proof_step,
)
```

### 変更クラス・関数全文

```python
def specialize_sigma11_suspension_step(
  symbolic_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if not _is_symbolic_sigma_family_definition_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda sigma-family definition"
    )

  sigma_family_statement = (
    symbolic_step.conclusion
  )

  sigma_11_definition = (
    toda_sigma_family_definition_statement(
      11,
      sigma_family_statement.sigma8_statement,
    )
  )

  sigma_12_definition = (
    toda_sigma_family_definition_statement(
      12,
      sigma_family_statement.sigma8_statement,
    )
  )

  return create_legacy_specialization_proof_step(
    conclusion=Relation(
      lhs=Suspension(
        expression=sigma_11_definition.element,
      ),
      rhs=sigma_12_definition.element,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 115-4 theorem-specific concrete "
      "specialization of the Toda sigma-family "
      "definition from sigma_11 to sigma_12"
    ),
  )
```

## repository_symbolic_sigma_specialization.py

### 変更後の import 全文

```python
from expression import (
  GeneratorSymbol,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  RepositoryProofScopeResult,
)
from toda_rules import (
  TodaSigmaFamilyDefinitionStatement,
  toda_sigma_family_definition_statement,
)
from phase164_r8_proofstep_factory import (
    create_legacy_specialization_proof_step,
)
```

### 変更クラス・関数全文

```python
def specialize_toda_prop515_sigma_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 10:
    raise ValueError(
      "index must be at least 10"
    )

  if not _is_symbolic_prop515_sigma_group_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.15 sigma-family group"
    )

  n = ScalarSymbol(
    name="n",
  )

  sigma_family_steps = tuple(
    premise
    for premise in symbolic_step.premises
    if (
      isinstance(
        premise,
        ProofStep,
      )
      and isinstance(
        premise.conclusion,
        TodaSigmaFamilyDefinitionStatement,
      )
      and premise.conclusion.index
      == n
    )
  )

  if len(
    sigma_family_steps
  ) != 1:
    raise ValueError(
      "symbolic_step must have exactly one "
      "symbolic sigma-family definition premise"
    )

  sigma_family_statement = (
    sigma_family_steps[
      0
    ].conclusion
  )

  sigma_definition = (
    toda_sigma_family_definition_statement(
      index,
      sigma_family_statement
      .sigma8_statement,
    )
  )

  conclusion = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=(
        index
        + 7
      ),
      sphere_dimension=index,
    ),
    rhs=FiniteCyclicGroup(
      order=16,
      generator=(
        sigma_definition.element
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  return create_legacy_specialization_proof_step(
    conclusion=conclusion,
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 109-22 theorem-specific concrete "
      "specialization of Toda Proposition 5.15 "
      f"at n={index}"
    ),
  )
```

## repository_symbolic_stable_group_specialization.py

### 変更後の import 全文

```python
from expression import (
  Composition,
  GeneratorSymbol,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  RepositoryProofScopeResult,
)
from toda_group_query import TodaGroupQuery
from toda_rules import (
  toda_eta_family_definition_statement,
  toda_nu_family_definition_statement,
)
from phase164_r8_proofstep_factory import (
    create_legacy_specialization_proof_step,
)
```

### 変更クラス・関数全文

```python
def specialize_toda_prop51_eta_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 3:
    raise ValueError(
      "index must be at least 3"
    )

  if not _is_symbolic_prop51_eta_group_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.1 eta-family group"
    )

  eta_definition = (
    toda_eta_family_definition_statement(
      index
    )
  )

  return create_legacy_specialization_proof_step(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=index + 1,
        sphere_dimension=index,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_definition.element,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-6 theorem-specific concrete "
      "specialization of Toda Proposition 5.1 "
      f"at n={index}"
    ),
  )
```

```python
def specialize_toda_prop53_eta_squared_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 5:
    raise ValueError(
      "index must be at least 5"
    )

  if not _is_symbolic_prop53_eta_squared_group_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.3 eta-squared group"
    )

  eta_n = (
    toda_eta_family_definition_statement(
      index
    ).element
  )
  eta_n_plus_one = (
    toda_eta_family_definition_statement(
      index + 1
    ).element
  )

  return create_legacy_specialization_proof_step(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=index + 2,
        sphere_dimension=index,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=Composition(
          left=eta_n,
          right=eta_n_plus_one,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-6 theorem-specific concrete "
      "specialization of Toda Proposition 5.3 "
      f"at n={index}"
    ),
  )
```

```python
def specialize_toda_prop56_nu_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 6:
    raise ValueError(
      "index must be at least 6"
    )

  if not _is_symbolic_prop56_nu_group_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.6 nu-family group"
    )

  nu_definition = (
    toda_nu_family_definition_statement(
      index
    )
  )

  return create_legacy_specialization_proof_step(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=index + 3,
        sphere_dimension=index,
      ),
      rhs=FiniteCyclicGroup(
        order=8,
        generator=nu_definition.element,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-6 theorem-specific concrete "
      "specialization of Toda Proposition 5.6 "
      f"at n={index}"
    ),
  )
```

```python
def specialize_toda_prop58_four_stem_zero_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 6:
    raise ValueError(
      "index must be at least 6"
    )

  if not _is_symbolic_prop58_four_stem_zero_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.8 four-stem zero group"
    )

  return create_legacy_specialization_proof_step(
    conclusion=TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=index + 4,
        sphere_dimension=index,
      ),
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-8 theorem-specific concrete "
      "specialization of Toda Proposition 5.8 "
      f"at n={index}"
    ),
  )
```

```python
def specialize_toda_prop59_five_stem_zero_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 7:
    raise ValueError(
      "index must be at least 7"
    )

  if not _is_symbolic_prop59_five_stem_zero_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.9 five-stem zero group"
    )

  return create_legacy_specialization_proof_step(
    conclusion=TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=index + 5,
        sphere_dimension=index,
      ),
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-8 theorem-specific concrete "
      "specialization of Toda Proposition 5.9 "
      f"at n={index}"
    ),
  )
```

```python
def specialize_toda_prop511_nu_squared_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 9:
    raise ValueError(
      "index must be at least 9"
    )

  if not _is_symbolic_prop511_nu_squared_group_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.11 nu-squared group"
    )

  nu_n = (
    toda_nu_family_definition_statement(
      index
    ).element
  )
  nu_n_plus_three = (
    toda_nu_family_definition_statement(
      index + 3
    ).element
  )

  return create_legacy_specialization_proof_step(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=index + 6,
        sphere_dimension=index,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=Composition(
          left=nu_n,
          right=nu_n_plus_three,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-8 theorem-specific concrete "
      "specialization of Toda Proposition 5.11 "
      f"at n={index}"
    ),
  )
```

## toda_midstream_bootstrap.py

### 変更後の import 全文

```python
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaSuspensionIsomorphismStatement,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaProp53FiniteDimensionalStatement,
  toda_53_n3_hopf_eta5_surjective_inference_rule,
  toda_53_n3_hopf_surjective_delta_zero_inference_rule,
  toda_53_n3_delta_zero_suspension_injective_inference_rule,
  toda_53_n3_suspension_isomorphism_inference_rule,
  toda_55_nu_family_finite_dimensional_integration_inference_rule,
  toda_55_nu_family_literature_statements,
  toda_56_nu4_decomposition_integration_inference_rule,
  toda_56_nu4_decomposition_literature_statements,
  toda_48_lemma54_hopf_odd_multiple_inference_rule,
  toda_eta_family_definition_statement,
  toda_lemma54_pi6_5_finite_cyclic_inference_rule,
  toda_prop53_finite_dimensional_integration_inference_rule,
  toda_prop53_higher_eta_squared_bridge_inference_rule,
  toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule,
  toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
  toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule,
  toda_53_n3_prop51_delta_injective_inference_rule,
  toda_53_n3_delta_injective_hopf_zero_inference_rule,
  toda_53_n3_hopf_zero_suspension_surjective_inference_rule,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_phase59_pi5_3_step(
  pi4_2_step: ProofStep,
  suspension_isomorphism_step: ProofStep,
) -> ProofStep:
  eta3_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      3
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta4_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      4
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  expected_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=eta_3,
        right=eta_4,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop53_n3_eta_square_suspension_bridge_inference_rule(),
      toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule(),
    ),
    (
      pi4_2_step,
      suspension_isomorphism_step,
      eta3_definition_step,
      eta4_definition_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected_relation
    ),
    "pi_5^3",
  )
```

```python
def build_phase59_hopf_surjective_step(
  prop51_step: ProofStep,
  hopf_eta5_step: ProofStep,
) -> ProofStep:
  pi_4_2 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=2,
  )
  pi_5_3 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=3,
  )
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )
  pi_6_3 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )
  pi_6_5 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=5,
  )
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  premise_steps = (
    prop51_step,
    hopf_eta5_step,
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_5_3,
          middle_term=pi_5_5,
          target_term=pi_3_2,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_4_2,
          middle_term=pi_5_3,
          target_term=pi_5_5,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_6_3,
          middle_term=pi_6_5,
          target_term=pi_4_2,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_6_5,
          middle_term=pi_4_2,
          target_term=pi_5_3,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = run_inference_until_stable_with_history(
    (
      toda_53_n3_prop51_delta_injective_inference_rule(),
      toda_53_n3_delta_injective_hopf_zero_inference_rule(),
      toda_53_n3_hopf_zero_suspension_surjective_inference_rule(),
      toda_53_n3_hopf_eta5_surjective_inference_rule(),
      toda_53_n3_hopf_surjective_delta_zero_inference_rule(),
      toda_53_n3_delta_zero_suspension_injective_inference_rule(),
      toda_53_n3_suspension_isomorphism_inference_rule(),
    ),
    premise_steps,
  )

  expected = TodaHopfInvariantSurjectiveStatement(
    map=TodaHopfInvariantMap(
      source_group=pi_6_3,
      target_group=pi_6_5,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected
    ),
    "H: pi_6^3 -> pi_6^5 surjective",
  )
```

```python
def build_phase59_prop53_step(
  pi4_2_step: ProofStep,
  pi5_3_step: ProofStep,
  pi6_4_step: ProofStep,
  higher_transport_step: ProofStep,
  higher_range_step: ProofStep,
) -> ProofStep:
  n = higher_range_step.conclusion.left

  eta_n_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      n
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )
  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  eta_n = eta_n_definition_step.conclusion.element
  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )
  eta_n_plus_one = HomotopyElement(
    name="η_(n+1)",
    dimension=n_plus_one,
    source=ScalarSum(
      left=n,
      right=2,
    ),
    target=n_plus_one,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_one,
    ),
  )
  eta_n_squared = Composition(
    left=eta_n,
    right=eta_n_plus_one,
  )

  expected_higher_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=2,
      ),
      sphere_dimension=n,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_n_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_statement = TodaProp53FiniteDimensionalStatement(
    pi4_2_group_relation=pi4_2_step.conclusion,
    pi5_3_group_relation=pi5_3_step.conclusion,
    pi6_4_group_relation=pi6_4_step.conclusion,
    higher_eta_squared_group_relation=(
      expected_higher_relation
    ),
    higher_range=higher_range_step.conclusion,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop53_higher_eta_squared_bridge_inference_rule(),
      toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule(),
      toda_prop53_finite_dimensional_integration_inference_rule(),
    ),
    (
      pi4_2_step,
      pi5_3_step,
      pi6_4_step,
      higher_transport_step,
      higher_range_step,
      eta_n_definition_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected_statement
    ),
    "Toda Proposition 5.3",
  )
```

## toda_phase65_bootstrap.py

### 変更後の import 全文

```python
from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_7_7_free_cyclic_fact,
)
from hopf_rules import (
  toda_prop22_right_inference_rule,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
  apply_inference_match,
  find_inference_match,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_proof_builders import (
  build_toda_prop56_proof_step,
)
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
)
from toda_rules import (
  TodaIteratedSuspensionInjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaProp56Pi8_5QuotientStatement,
  TodaSuspensionInjectiveStatement,
  toda_eta_family_definition_statement,
  toda_nu_family_definition_statement,
  toda_57_nu_prime_eta6_hopf_inference_rule,
  toda_prop56_e2_nu_prime_order_four_inference_rule,
  toda_prop56_eta3_cube_order_two_inference_rule,
  toda_prop56_higher_nu_family_bridge_inference_rule,
  toda_prop56_higher_nu_finite_cyclic_generator_inference_rule,
  toda_prop56_nu5_double_relation_inference_rule,
  toda_prop56_nu5_order_eight_inference_rule,
  toda_prop56_nu_prime_order_four_inference_rule,
  toda_prop56_pi5_2_eta2_cube_inference_rule,
  toda_prop56_pi5_2_suspension_injective_inference_rule,
  toda_prop56_pi6_3_e2_injective_inference_rule,
  toda_prop56_pi6_3_finite_cyclic_inference_rule,
  toda_prop56_pi7_3_hopf_surjective_inference_rule,
  toda_prop56_pi7_4_decomposition_inference_rule,
  toda_prop56_pi7_5_delta_zero_inference_rule,
  toda_prop56_pi8_5_finite_cyclic_inference_rule,
  toda_prop56_pi8_5_quotient_inference_rule,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_toda_prop56_bootstrap_step(
  toda52_step: ProofStep,
  pi5_3_step: ProofStep,
  hopf_nu_prime_step: ProofStep,
  prop53_step: ProofStep,
  double_step: ProofStep,
  membership_step: ProofStep,
  hopf_surjective_step: ProofStep,
  pi6_5_step: ProofStep,
  toda55_step: ProofStep,
  toda56_step: ProofStep,
  stable_isomorphism_step: ProofStep,
) -> ProofStep:
  pi5_2_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop56_pi5_2_eta2_cube_inference_rule(),
      ),
      (
        pi5_3_step,
        toda52_step,
      ),
    )
  )

  pi5_2_step = _find_unique_step(
    pi5_2_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      == RelationType.EQUALITY
      and step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=2,
      )
    ),
    "pi_5^2",
  )

  eta5_definition_step = create_legacy_given_proof_step(
    conclusion=(
      toda_eta_family_definition_statement(
        5
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta6_definition_step = create_legacy_given_proof_step(
    conclusion=(
      toda_eta_family_definition_statement(
        6
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi_7_3 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=3,
  )

  pi_7_5 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=5,
  )

  pi_5_2 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=2,
  )

  pi_6_3 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )

  h_delta_exactness_step = create_legacy_given_proof_step(
    conclusion=(
      TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_7_3,
          middle_term=pi_7_5,
          target_term=pi_5_2,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        ),
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  delta_e_exactness_step = create_legacy_given_proof_step(
    conclusion=(
      TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_7_5,
          middle_term=pi_5_2,
          target_term=pi_6_3,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        ),
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  hopf_relation = (
    hopf_nu_prime_step.conclusion
  )
  prop22_rule = (
    toda_prop22_right_inference_rule(
      alpha=(
        hopf_relation
        .lhs
        .expression
      ),
      gamma=hopf_relation.rhs,
    )
  )

  prop22_match = (
    find_inference_match(
      prop22_rule,
      (),
    )
  )

  if prop22_match is None:
    raise ValueError(
      "Toda Proposition 2.2 must be directly applicable"
    )

  prop22_step = (
    derive_inference_proof_step(
      prop22_match
    )
  )

  equation57_result = (
    run_inference_until_stable_with_history(
      (
        toda_57_nu_prime_eta6_hopf_inference_rule(),
        toda_prop56_pi7_3_hopf_surjective_inference_rule(),
        toda_prop56_pi7_5_delta_zero_inference_rule(),
        toda_prop56_pi5_2_suspension_injective_inference_rule(),
      ),
      (
        hopf_nu_prime_step,
        prop53_step,
        eta5_definition_step,
        eta6_definition_step,
        prop22_step,
        h_delta_exactness_step,
        delta_e_exactness_step,
      ),
    )
  )

  suspension_injective_step = (
    _find_unique_step(
      equation57_result.steps,
      lambda step: (
        isinstance(
          step.conclusion,
          TodaSuspensionInjectiveStatement,
        )
        and (
          step.conclusion
          .map
          .source_group
          == pi_5_2
        )
        and (
          step.conclusion
          .map
          .target_group
          == pi_6_3
        )
      ),
      "pi_5^2 suspension injective",
    )
  )

  pi_6_5 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=5,
  )

  e_h_exactness_step = create_legacy_given_proof_step(
    conclusion=(
      TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_5_2,
          middle_term=pi_6_3,
          target_term=pi_6_5,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        ),
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi6_3_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop56_eta3_cube_order_two_inference_rule(),
        toda_prop56_nu_prime_order_four_inference_rule(),
        toda_prop56_pi6_3_finite_cyclic_inference_rule(),
      ),
      (
        pi5_2_step,
        suspension_injective_step,
        double_step,
        membership_step,
        e_h_exactness_step,
        hopf_surjective_step,
        pi6_5_step,
      ),
    )
  )

  pi6_3_step = _find_unique_step(
    pi6_3_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      == RelationType.EQUALITY
      and step.conclusion.lhs
      == pi_6_3
    ),
    "pi_6^3",
  )

  pi7_7_step = create_legacy_given_proof_step(
    conclusion=(
      pi_7_7_free_cyclic_fact()
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi7_4_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop56_pi7_4_decomposition_inference_rule(),
      ),
      (
        toda56_step,
        pi6_3_step,
        pi7_7_step,
      ),
    )
  )

  pi7_4_step = _find_unique_step(
    pi7_4_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      == RelationType.EQUALITY
      and step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=4,
      )
    ),
    "pi_7^4",
  )

  e2_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop56_pi8_5_quotient_inference_rule(),
        toda_prop56_pi6_3_e2_injective_inference_rule(),
      ),
      (
        toda56_step,
      ),
    )
  )

  quotient_step = _find_unique_step(
    e2_result.steps,
    lambda step: isinstance(
      step.conclusion,
      TodaProp56Pi8_5QuotientStatement,
    ),
    "pi_8^5 quotient",
  )

  e2_injective_step = _find_unique_step(
    e2_result.steps,
    lambda step: isinstance(
      step.conclusion,
      TodaIteratedSuspensionInjectiveStatement,
    ),
    "E^2 injective",
  )

  nu5_definition_step = create_legacy_given_proof_step(
    conclusion=(
      toda_nu_family_definition_statement(
        5
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi8_5_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop56_nu5_double_relation_inference_rule(),
        toda_prop56_e2_nu_prime_order_four_inference_rule(),
        toda_prop56_nu5_order_eight_inference_rule(),
        toda_prop56_pi8_5_finite_cyclic_inference_rule(),
      ),
      (
        toda55_step,
        nu5_definition_step,
        pi6_3_step,
        e2_injective_step,
        quotient_step,
      ),
    )
  )

  pi8_5_step = _find_unique_step(
    pi8_5_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      == RelationType.EQUALITY
      and step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      )
    ),
    "pi_8^5",
  )

  n = ScalarSymbol(
    name="n",
  )

  higher_range_step = create_legacy_given_proof_step(
    conclusion=(
      ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu_n_definition_step = create_legacy_given_proof_step(
    conclusion=(
      toda_nu_family_definition_statement(
        n
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  stable_result = (
    run_inference_until_stable_with_history(
      (
        toda_45_generic_finite_cyclic_transport_inference_rule(),
        toda_prop56_higher_nu_family_bridge_inference_rule(),
        toda_prop56_higher_nu_finite_cyclic_generator_inference_rule(),
      ),
      (
        pi8_5_step,
        stable_isomorphism_step,
        higher_range_step,
        nu5_definition_step,
        nu_n_definition_step,
      ),
    )
  )

  higher_group = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=n,
      right=3,
    ),
    sphere_dimension=n,
  )

  expected_final_relation = Relation(
    lhs=higher_group,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=(
        nu_n_definition_step
        .conclusion
        .element
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  higher_step = _find_unique_step(
    stable_result.steps,
    lambda step: (
      step.conclusion
      == expected_final_relation
    ),
    "higher nu family",
  )

  return build_toda_prop56_proof_step(
    pi5_2_step,
    pi6_3_step,
    pi7_4_step,
    pi8_5_step,
    higher_step,
    higher_range_step,
  )
```

## toda_proof_builders.py

### 変更後の import 全文

```python
from proof import (
  ProofStep,
  apply_inference_match,
  find_inference_match,
)
from toda_rules import (
  toda_prop56_finite_dimensional_integration_inference_rule,
  toda_prop58_finite_dimensional_integration_inference_rule,
  toda_prop511_finite_dimensional_integration_inference_rule,
  toda_prop515_finite_dimensional_integration_inference_rule,
)
from phase164_r8_proofstep_factory import (
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_toda_prop56_proof_step(
  pi5_2_step: ProofStep,
  pi6_3_step: ProofStep,
  pi7_4_step: ProofStep,
  pi8_5_step: ProofStep,
  higher_step: ProofStep,
  higher_range_step: ProofStep,
) -> ProofStep:
  premise_steps = (
    pi5_2_step,
    pi6_3_step,
    pi7_4_step,
    pi8_5_step,
    higher_step,
    higher_range_step,
  )

  rule = (
    toda_prop56_finite_dimensional_integration_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  if match is None:
    raise ValueError(
      "premises do not derive "
      "Toda Proposition 5.6"
    )

  return derive_inference_proof_step(
    match
  )
```

```python
def build_toda_prop58_proof_step(
  pi6_2_step: ProofStep,
  pi7_3_step: ProofStep,
  pi8_4_step: ProofStep,
  pi9_5_step: ProofStep,
  higher_zero_step: ProofStep,
  higher_range_step: ProofStep,
) -> ProofStep:
  premise_steps = (
    pi6_2_step,
    pi7_3_step,
    pi8_4_step,
    pi9_5_step,
    higher_zero_step,
    higher_range_step,
  )

  rule = (
    toda_prop58_finite_dimensional_integration_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  if match is None:
    raise ValueError(
      "premises do not derive "
      "Toda Proposition 5.8"
    )

  return derive_inference_proof_step(
    match
  )
```

```python
def build_toda_prop511_proof_step(
  pi8_2_step: ProofStep,
  pi9_3_zero_step: ProofStep,
  pi10_4_step: ProofStep,
  nu_squared_step: ProofStep,
) -> ProofStep:
  premise_steps = (
    pi8_2_step,
    pi9_3_zero_step,
    pi10_4_step,
    nu_squared_step,
  )

  rule = (
    toda_prop511_finite_dimensional_integration_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  if match is None:
    raise ValueError(
      "premises do not derive "
      "Toda Proposition 5.11"
    )

  return derive_inference_proof_step(
    match
  )
```

```python
def build_toda_prop515_proof_step(
  pi9_2_step: ProofStep,
  pi10_3_step: ProofStep,
  pi11_4_step: ProofStep,
  pi12_5_step: ProofStep,
  pi13_6_step: ProofStep,
  pi14_7_step: ProofStep,
  pi15_8_step: ProofStep,
  higher_step: ProofStep,
  higher_range_step: ProofStep,
) -> ProofStep:
  premise_steps = (
    pi9_2_step,
    pi10_3_step,
    pi11_4_step,
    pi12_5_step,
    pi13_6_step,
    pi14_7_step,
    pi15_8_step,
    higher_step,
    higher_range_step,
  )

  rule = (
    toda_prop515_finite_dimensional_integration_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  if match is None:
    raise ValueError(
      "premises do not derive "
      "Toda Proposition 5.15"
    )

  return derive_inference_proof_step(
    match
  )
```

## toda_prop511_zero_bootstrap.py

### 変更後の import 全文

```python
from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
  barratt_hilton_first_inference_rule,
  barratt_hilton_second_inference_rule,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
  WhiteheadProduct,
  Zero,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  HomotopyEHPExactnessWindow,
  HomotopyGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaPrimaryGroupZeroStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_prop56_zero_bootstrap import (
  _build_phase60_toda54,
)
from toda_prop58_zero_bootstrap import (
  _build_delta_eta9_step,
  _build_equation57_steps,
  _build_eta2_nu_prime_zero_step,
  _build_higher_eta_nu_zero_step,
  _build_nu6_eta9_zero_step,
  _build_phase66_step,
  _build_pi6_2_step,
  _build_pi7_3_steps,
  _build_pi8_4_step,
  _build_pi9_5_step,
  _build_support,
  _build_toda59_step,
  build_toda_prop58_zero_argument_step,
)
from toda_stable_generator_normalization import (
  toda_nu_squared_transport_generator_normalization_inference_rule,
)
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
  toda_45_generic_zero_group_transport_inference_rule,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaLemma510BracketModuloStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
  TodaProp59DeltaKernelStatement,
  TodaProp59FiniteDimensionalStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
  TodaSuspensionZeroStatement,
  serre_42_finite_homotopy_group_inference_rule,
  toda_211_ordinary_ehp_applicability_inference_rule,
  toda_211_ordinary_ehp_exactness_inference_rule,
  toda_32_phase60_suspension_surjective_inference_rule,
  toda_54_t0_bridge_inference_rule,
  toda_512_n4_delta_injective_inference_rule,
  toda_512_n5_delta_injective_inference_rule,
  toda_512_n6_delta_injective_inference_rule,
  toda_eq510_concrete_delta_e_exactness_inference_rule,
  toda_eq510_delta_iota11_inference_rule,
  toda_eq510_delta_surjective_inference_rule,
  toda_eta_family_definition_statement,
  toda_lemma510_corrected_exactness_core_inference_rule,
  toda_lemma510_corrected_modulo_integration_inference_rule,
  toda_lemma510_eta8_two_iota9_zero_inference_rule,
  toda_lemma510_eta9_two_iota10_zero_inference_rule,
  toda_lemma510_hopf_from_split_inference_rule,
  toda_lemma510_nu6_ordinary_composition_reduction_inference_rule,
  toda_lemma510_nu6_ordinary_composition_zero_inference_rule,
  toda_lemma510_ordinary_indeterminacy_double_inference_rule,
  toda_lemma510_ordinary_suspension_image_finite_inference_rule,
  toda_lemma510_ordinary_suspension_image_in_double_inference_rule,
  toda_lemma510_ordinary_suspension_image_two_primary_zero_inference_rule,
  toda_lemma510_prop26_indexed_hopf_inference_rule,
  toda_lemma510_split_115_inference_rule,
  toda_lemma57_concrete_delta_e_exactness_inference_rule,
  toda_lemma57_delta_nu5_generator_inference_rule,
  toda_lemma57_delta_surjective_inference_rule,
  toda_nu_family_definition_statement,
  toda_prop44_first_summand_restriction_inference_rule,
  toda_prop44_isomorphism_inference_rule,
  toda_prop44_suspension_injective_inference_rule,
  toda_prop58_e_nu4_eta7_bridge_inference_rule,
  toda_prop58_pi10_6_concrete_exactness_inference_rule,
  toda_prop58_pi10_6_suspension_surjective_inference_rule,
  toda_prop58_pi10_6_zero_inference_rule,
  toda_prop59_concrete_e_h_exactness_inference_rule,
  toda_prop59_concrete_h_delta_exactness_inference_rule,
  toda_prop59_delta_eta11_inference_rule,
  toda_prop59_delta_eta9_squared_inference_rule,
  toda_prop59_delta_iota13_hopf_inference_rule,
  toda_prop59_delta_nu5_kernel_inference_rule,
  toda_prop59_e_nu4_eta7_squared_bridge_inference_rule,
  toda_prop59_e_nu5_eta8_squared_zero_inference_rule,
  toda_prop59_e_nu_prime_eta6_squared_bridge_inference_rule,
  toda_prop59_finite_dimensional_integration_inference_rule,
  toda_prop59_finite_dimensional_literature_statements,
  toda_prop59_nu_prime_eta6_squared_hopf_inference_rule,
  toda_prop59_pi10_5_concrete_exactness_inference_rule,
  toda_prop59_pi10_5_delta_e_exactness_inference_rule,
  toda_prop59_pi10_5_finite_cyclic_inference_rule,
  toda_prop59_pi10_5_hopf_zero_inference_rule,
  toda_prop59_pi10_5_suspension_surjective_inference_rule,
  toda_prop59_pi10_9_delta_injective_inference_rule,
  toda_prop59_pi11_11_delta_kernel_inference_rule,
  toda_prop59_pi11_6_concrete_exactness_inference_rule,
  toda_prop59_pi11_6_free_cyclic_inference_rule,
  toda_prop59_pi11_6_hopf_injective_inference_rule,
  toda_prop59_pi12_7_concrete_exactness_inference_rule,
  toda_prop59_pi12_7_suspension_surjective_inference_rule,
  toda_prop59_pi12_7_zero_inference_rule,
  toda_prop59_pi13_13_delta_surjective_inference_rule,
  toda_prop59_pi7_2_eta2_nu_prime_eta6_inference_rule,
  toda_prop59_pi7_2_suspension_zero_inference_rule,
  toda_prop59_pi8_3_finite_cyclic_inference_rule,
  toda_prop59_pi8_3_hopf_injective_inference_rule,
  toda_prop59_pi9_4_decomposition_inference_rule,
  toda_prop511_513_delta_eta11_squared_zero_inference_rule,
  toda_prop511_513_delta_eta13_zero_inference_rule,
  toda_prop511_513_delta_nu9_inference_rule,
  toda_prop511_finite_dimensional_integration_inference_rule,
  toda_prop511_finite_dimensional_literature_statements,
  toda_prop511_nu_squared_finite_dimensional_integration_inference_rule,
  toda_prop511_nu_squared_finite_dimensional_literature_statements,
  toda_prop511_pi10_4_nu4_squared_inference_rule,
  toda_prop511_pi10_7_nu7_inference_rule,
  toda_prop511_pi11_5_concrete_exactness_inference_rule,
  toda_prop511_pi11_5_hopf_zero_inference_rule,
  toda_prop511_pi11_5_nu5_squared_inference_rule,
  toda_prop511_pi11_5_suspension_surjective_inference_rule,
  toda_prop511_pi12_6_concrete_exactness_inference_rule,
  toda_prop511_pi12_6_hopf_zero_inference_rule,
  toda_prop511_pi12_6_nu6_squared_inference_rule,
  toda_prop511_pi12_6_suspension_injective_inference_rule,
  toda_prop511_pi12_6_suspension_isomorphism_inference_rule,
  toda_prop511_pi12_6_suspension_surjective_inference_rule,
  toda_prop511_pi12_9_nu9_inference_rule,
  toda_prop511_pi13_11_eta11_squared_inference_rule,
  toda_prop511_pi13_7_concrete_exactness_inference_rule,
  toda_prop511_pi13_7_hopf_zero_inference_rule,
  toda_prop511_pi13_7_nu7_squared_inference_rule,
  toda_prop511_pi13_7_suspension_injective_inference_rule,
  toda_prop511_pi13_7_suspension_isomorphism_inference_rule,
  toda_prop511_pi13_7_suspension_surjective_inference_rule,
  toda_prop511_pi14_13_eta13_inference_rule,
  toda_prop511_pi14_8_nu8_squared_inference_rule,
  toda_prop511_pi14_8_prop44_zero_second_summand_suspension_isomorphism_inference_rule,
  toda_prop511_pi7_2_suspension_zero_inference_rule,
  toda_prop511_pi8_2_eta2_nu_prime_eta6_squared_inference_rule,
  toda_prop511_pi8_2_suspension_zero_inference_rule,
  toda_prop511_pi9_3_concrete_exactness_inference_rule,
  toda_prop511_pi9_3_zero_inference_rule,
  toda_prop511_pi9_5_to_pi7_2_delta_injective_inference_rule,
  toda_prop511_zero_suspension_left_implies_hopf_injective_inference_rule,
  toda_prop511_zero_suspension_right_implies_delta_surjective_inference_rule,
)
from toda_upstream_bootstrap import (
  build_toda_45_stable_isomorphism_step,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    create_legacy_specialization_proof_step,
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def _apply(
  rule,
  premises: tuple[ProofStep, ...],
  description: str,
) -> ProofStep:
  match = find_inference_match(
    rule,
    premises,
  )

  if match is None:
    raise ValueError(
      f"expected {description} inference match"
    )

  return derive_inference_proof_step(
    match
  )
```

```python
def _given(
  conclusion,
) -> ProofStep:
  return create_legacy_given_proof_step(
    conclusion=conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )
```

```python
def _build_phase68_generator_bridge(
  context: dict[
    str,
    ProofStep,
  ],
) -> ProofStep:
  pi8_4_step = context[
    "pi8_4_step"
  ]

  nu5_definition_step = _given(
    toda_nu_family_definition_statement(
      5
    )
  )

  rule = (
    toda_prop58_e_nu4_eta7_bridge_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      pi8_4_step,
      nu5_definition_step,
    ),
  )

  if match is not None:
    return derive_inference_proof_step(
      match
    )

  pi10_9 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=9,
  )
  pi8_4 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=4,
  )
  pi9_5 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )
  pi9_9 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=9,
  )
  pi7_4 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=4,
  )

  from toda_rules import (
    toda_prop58_pi9_5_concrete_exactness_inference_rule,
    toda_prop58_pi9_5_finite_cyclic_inference_rule,
    toda_prop58_pi9_5_hopf_zero_inference_rule,
    toda_prop58_pi9_5_suspension_surjective_inference_rule,
    toda_prop58_pi9_9_delta_injective_inference_rule,
  )
  from proof import (
    run_inference_until_stable_with_history,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop58_pi9_5_concrete_exactness_inference_rule(),
      toda_prop58_pi9_9_delta_injective_inference_rule(),
      toda_prop58_pi9_5_hopf_zero_inference_rule(),
      toda_prop58_pi9_5_suspension_surjective_inference_rule(),
      toda_prop58_e_nu4_eta7_bridge_inference_rule(),
      toda_prop58_pi9_5_finite_cyclic_inference_rule(),
    ),
    (
      context[
        "prop56_step"
      ],
      context[
        "phase66_step"
      ],
      pi8_4_step,
      context[
        "prop51_step"
      ],
      context[
        "delta_eta9_step"
      ],
      nu5_definition_step,
      _given(
        TodaEHPExactnessWindow(
          source_term=pi10_9,
          middle_term=pi8_4,
          target_term=pi9_5,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        )
      ),
      _given(
        TodaEHPExactnessWindow(
          source_term=pi8_4,
          middle_term=pi9_5,
          target_term=pi9_9,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        )
      ),
      _given(
        TodaEHPExactnessWindow(
          source_term=pi9_5,
          middle_term=pi9_9,
          target_term=pi7_4,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        )
      ),
    ),
  )

  nu4_eta7 = (
    pi8_4_step
    .conclusion
    .rhs
    .summands[0]
    .generator
  )

  return next(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == Suspension(
        expression=nu4_eta7,
      )
    )
  )
```

```python
def _build_pi14_8_suspension_isomorphism_step() -> ProofStep:
  pi13_7 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=7,
  )

  pi14_15 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=15,
  )

  pi14_8 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=8,
  )

  beta = HomotopyElement(
    name="β",
    dimension=13,
    source=13,
    target=7,
    generator=GeneratorSymbol(
      family="β",
    ),
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=14,
    source=14,
    target=15,
    generator=GeneratorSymbol(
      family="γ",
    ),
  )

  sigma_8 = HomotopyElement(
    name="σ₈",
    dimension=8,
    source=15,
    target=8,
    generator=GeneratorSymbol(
      family="σ",
      index=8,
    ),
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=DirectSumGroup(
        summands=(
          pi13_7,
          pi14_15,
        ),
      ),
      target_group=pi14_8,
      alpha=sigma_8,
      beta=beta,
      gamma=gamma,
      formula=Sum(
        left=Suspension(
          expression=beta,
        ),
        right=Composition(
          left=sigma_8,
          right=gamma,
        ),
      ),
    )
  )

  prop44_step = create_legacy_specialization_proof_step(
    conclusion=TodaProp44IsomorphismStatement(
      map=decomposition_map,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  zero_step = _given(
    TodaPrimaryGroupZeroStatement(
      group=pi14_15,
    )
  )

  return _apply(
    toda_prop511_pi14_8_prop44_zero_second_summand_suspension_isomorphism_inference_rule(),
    (
      prop44_step,
      zero_step,
    ),
    "pi_14^8 suspension isomorphism",
  )
```

## toda_prop515_low_bootstrap.py

### 変更後の import 全文

```python
from dataclasses import dataclass
from functools import lru_cache
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  run_inference_until_stable_with_history,
)
from toda_prop56_zero_bootstrap import (
  build_toda_prop56_zero_argument_step,
)
from toda_prop58_zero_bootstrap import (
  build_toda_prop58_zero_argument_step,
)
from toda_prop511_zero_bootstrap import (
  build_toda_prop511_zero_argument_step,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  TodaDeltaImageUpToSignStatement,
  TodaLemma513Statement,
  TodaProp59FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  toda_exactness_zero_left_implies_hopf_injective_inference_rule,
  toda_lemma513_sigma_triple_prime_definition_inference_rule,
  toda_prop511_pi12_9_nu9_inference_rule,
  toda_prop515_pi9_2_zero_inference_rule,
  toda_prop515_pi10_3_concrete_exactness_inference_rule,
  toda_prop515_pi10_3_delta_injective_inference_rule,
  toda_prop515_pi10_3_delta_surjective_inference_rule,
  toda_prop515_pi10_3_zero_inference_rule,
  toda_prop515_pi11_4_zero_inference_rule,
  toda_prop515_pi12_5_concrete_exactness_inference_rule,
  toda_prop515_pi12_5_finite_cyclic_inference_rule,
  toda_prop515_pi12_5_hopf_isomorphism_inference_rule,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_toda_prop515_low_bootstrap():
  prop56_step = (
    build_toda_prop56_zero_argument_step()
  )

  prop58_step = (
    build_toda_prop58_zero_argument_step()
  )

  prop511_step = (
    build_toda_prop511_zero_argument_step()
  )

  upstream_steps = (
    _proof_step_closure(
      (
        prop56_step,
        prop58_step,
        prop511_step,
      )
    )
  )

  toda52_step = (
    _require_unique_inference_step(
      upstream_steps,
      Toda52CompositionIsomorphismStatement,
      lambda statement: (
        statement.source_group
        .sphere_dimension
        == 3
        and statement.target_group
        .sphere_dimension
        == 2
        and statement.source_group
        .group_dimension
        == statement.target_group
        .group_dimension
      ),
    )
  )

  prop59_step = (
    _require_unique_inference_step(
      upstream_steps,
      TodaProp59FiniteDimensionalStatement,
    )
  )

  toda56_step = (
    _require_unique_inference_step(
      upstream_steps,
      Toda56Nu4DecompositionIsomorphismStatement,
    )
  )

  toda55_step = (
    _require_unique_inference_step(
      upstream_steps,
      Toda55NuFamilyFiniteDimensionalStatement,
    )
  )

  delta_nu9_step = (
    _require_unique_inference_step(
      upstream_steps,
      TodaDeltaImageUpToSignStatement,
      lambda statement: (
        statement.map.source_group
        == TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=9,
        )
        and statement.map.target_group
        == TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=4,
        )
      ),
    )
  )

  pi9_2_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_pi9_2_zero_inference_rule(),
      ),
      (
        prop511_step,
        toda52_step,
      ),
    )
  )

  pi9_2_zero = (
    TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=2,
      ),
    )
  )

  pi9_2_zero_step = next(
    step
    for step in pi9_2_result.steps
    if (
      step.conclusion
      == pi9_2_zero
    )
  )

  pi9_2 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=2,
  )

  pi10_3 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=3,
  )

  pi10_5 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  pi8_2 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=2,
  )

  pi9_3 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=3,
  )

  pi10_e_h_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi9_2,
      middle_term=pi10_3,
      target_term=pi10_5,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi10_h_delta_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi10_3,
      middle_term=pi10_5,
      target_term=pi8_2,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi10_delta_e_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi10_5,
      middle_term=pi8_2,
      target_term=pi9_3,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi10_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_pi10_3_concrete_exactness_inference_rule(),
        toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
        toda_prop515_pi10_3_delta_surjective_inference_rule(),
        toda_prop515_pi10_3_delta_injective_inference_rule(),
        toda_prop515_pi10_3_zero_inference_rule(),
      ),
      (
        pi9_2_zero_step,
        prop59_step,
        prop511_step,
        pi10_e_h_window_step,
        pi10_h_delta_window_step,
        pi10_delta_e_window_step,
      ),
    )
  )

  pi10_3_zero = (
    TodaPrimaryGroupZeroStatement(
      group=pi10_3,
    )
  )

  pi10_3_zero_step = next(
    step
    for step in pi10_result.steps
    if (
      step.conclusion
      == pi10_3_zero
    )
  )

  pi11_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_pi11_4_zero_inference_rule(),
      ),
      (
        pi10_3_zero_step,
        prop58_step,
        toda56_step,
      ),
    )
  )

  pi11_4_zero = (
    TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=4,
      ),
    )
  )

  pi11_4_zero_step = next(
    step
    for step in pi11_result.steps
    if (
      step.conclusion
      == pi11_4_zero
    )
  )

  pi12_9_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop511_pi12_9_nu9_inference_rule(),
      ),
      (
        prop56_step,
      ),
    )
  )

  pi12_9 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=9,
  )

  pi12_9_step = next(
    step
    for step in pi12_9_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi12_9
    )
  )

  pi12_5 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=5,
  )

  pi10_4 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=4,
  )

  pi12_e_h_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=4,
      ),
      middle_term=pi12_5,
      target_term=pi12_9,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi12_h_delta_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi12_5,
      middle_term=pi12_9,
      target_term=pi10_4,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi12_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_pi12_5_concrete_exactness_inference_rule(),
        toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
        toda_prop515_pi12_5_hopf_isomorphism_inference_rule(),
        toda_lemma513_sigma_triple_prime_definition_inference_rule(),
        toda_prop515_pi12_5_finite_cyclic_inference_rule(),
      ),
      (
        pi11_4_zero_step,
        toda55_step,
        delta_nu9_step,
        prop511_step,
        pi12_9_step,
        pi12_e_h_window_step,
        pi12_h_delta_window_step,
      ),
    )
  )

  hopf_isomorphism_step = next(
    step
    for step in pi12_result.steps
    if isinstance(
      step.conclusion,
      TodaProp515Pi12_5HopfIsomorphismStatement,
    )
  )

  lemma513_step = next(
    step
    for step in pi12_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma513Statement,
    )
  )

  pi12_5_step = next(
    step
    for step in pi12_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi12_5
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 2
      and step.conclusion.rhs.generator
      == (
        lemma513_step
        .conclusion
        .sigma_triple_prime
      )
    )
  )

  return (
    TodaProp515LowBootstrapResult(
      prop56_step=prop56_step,
      prop58_step=prop58_step,
      prop511_step=prop511_step,
      toda52_step=toda52_step,
      prop59_step=prop59_step,
      toda56_step=toda56_step,
      toda55_step=toda55_step,
      delta_nu9_step=delta_nu9_step,
      pi9_2_zero_step=(
        pi9_2_zero_step
      ),
      pi10_3_zero_step=(
        pi10_3_zero_step
      ),
      pi11_4_zero_step=(
        pi11_4_zero_step
      ),
      pi12_9_step=pi12_9_step,
      hopf_isomorphism_step=(
        hopf_isomorphism_step
      ),
      lemma513_step=lemma513_step,
      pi12_5_step=pi12_5_step,
    )
  )
```

## toda_prop515_sigma_chain_bootstrap.py

### 変更後の import 全文

```python
from dataclasses import dataclass
from functools import lru_cache
from expression import (
  Composition,
  MapApplication,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
)
from toda_prop515_low_bootstrap import (
  _proof_step_closure,
  _require_unique_inference_step,
  build_toda_prop515_low_bootstrap,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda514FirstShortExactStatement,
  Toda514SecondShortExactStatement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma514Sigma8Statement,
  TodaLemma54Statement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp53FiniteDimensionalStatement,
  toda_36_lemma514_sigma_double_prime_bridge_inference_rule,
  toda_514_delta_eta13_squared_zero_inference_rule,
  toda_514_delta_nu11_zero_inference_rule,
  toda_514_first_short_exact_concrete_exactness_inference_rule,
  toda_514_first_short_exact_inference_rule,
  toda_514_second_short_exact_concrete_exactness_inference_rule,
  toda_514_second_short_exact_inference_rule,
  toda_lemma514_sigma_double_prime_inference_rule,
  toda_lemma514_sigma_prime_inference_rule,
  toda_lemma514_sigma8_inference_rule,
  toda_prop511_513_delta_eta11_squared_zero_inference_rule,
  toda_prop511_pi13_11_eta11_squared_inference_rule,
  toda_prop511_pi14_13_eta13_inference_rule,
  toda_prop515_pi13_6_finite_cyclic_inference_rule,
  toda_prop515_pi14_7_finite_cyclic_inference_rule,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_toda_prop515_sigma_chain_bootstrap():
  low_result = (
    build_toda_prop515_low_bootstrap()
  )

  upstream_steps = (
    _proof_step_closure(
      (
        low_result.prop56_step,
        low_result.prop58_step,
        low_result.prop511_step,
        low_result.pi12_5_step,
      )
    )
  )

  prop51_step = (
    _require_unique_inference_step(
      upstream_steps,
      TodaProp51FiniteDimensionalStatement,
    )
  )

  prop53_step = (
    _require_unique_inference_step(
      upstream_steps,
      TodaProp53FiniteDimensionalStatement,
    )
  )

  lemma54_step = (
    _require_unique_inference_step(
      upstream_steps,
      TodaLemma54Statement,
    )
  )

  eta_n_nu_n_plus_one_zero_step = (
    _require_unique_inference_step(
      upstream_steps,
      Relation,
      _is_eta_n_nu_n_plus_one_zero,
    )
  )

  delta_iota11_step = (
    _require_unique_inference_step(
      upstream_steps,
      Relation,
      _is_delta_iota11_relation,
    )
  )

  delta_eta13_step = (
    _require_unique_inference_step(
      upstream_steps,
      Relation,
      _is_delta_eta13_zero,
    )
  )

  delta_eta11_squared_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop511_513_delta_eta11_squared_zero_inference_rule(),
      ),
      (
        delta_iota11_step,
        low_result.toda55_step,
        low_result.delta_nu9_step,
      ),
    )
  )

  delta_eta11_squared_step = next(
    step
    for step in delta_eta11_squared_result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      == RelationType.ZERO
      and isinstance(
        step.conclusion.lhs,
        MapApplication,
      )
      and step.conclusion.lhs.map
      == EHP_DELTA_MAP
      and isinstance(
        step.conclusion.lhs.expression,
        Composition,
      )
      and getattr(
        getattr(
          step.conclusion
          .lhs
          .expression
          .left,
          "generator",
          None,
        ),
        "index",
        None,
      )
      == 11
    )
  )

  pi13_11_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop511_pi13_11_eta11_squared_inference_rule(),
      ),
      (
        prop53_step,
      ),
    )
  )

  pi13_11 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=11,
  )

  pi13_11_step = next(
    step
    for step in pi13_11_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi13_11
    )
  )

  pi14_11 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=11,
  )

  pi12_5 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=5,
  )

  pi13_6 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=6,
  )

  pi11_5 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=5,
  )

  first_delta_e_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi14_11,
      middle_term=pi12_5,
      target_term=pi13_6,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_e_h_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi12_5,
      middle_term=pi13_6,
      target_term=pi13_11,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_h_delta_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi13_6,
      middle_term=pi13_11,
      target_term=pi11_5,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_short_exact_result = (
    run_inference_until_stable_with_history(
      (
        toda_514_delta_nu11_zero_inference_rule(),
        toda_514_first_short_exact_concrete_exactness_inference_rule(),
        toda_514_first_short_exact_inference_rule(),
      ),
      (
        delta_iota11_step,
        eta_n_nu_n_plus_one_zero_step,
        low_result.toda55_step,
        low_result.prop56_step,
        delta_eta11_squared_step,
        pi13_11_step,
        first_delta_e_window_step,
        first_e_h_window_step,
        first_h_delta_window_step,
      ),
    )
  )

  first_short_exact_step = next(
    step
    for step in first_short_exact_result.steps
    if isinstance(
      step.conclusion,
      Toda514FirstShortExactStatement,
    )
  )

  sigma_double_prime_result = (
    run_inference_until_stable_with_history(
      (
        toda_36_lemma514_sigma_double_prime_bridge_inference_rule(),
        toda_lemma514_sigma_double_prime_inference_rule(),
      ),
      (
        lemma54_step,
        low_result.prop511_step,
        low_result.prop58_step,
        low_result.lemma513_step,
        low_result.pi12_5_step,
        first_short_exact_step,
        pi13_11_step,
      ),
    )
  )

  bridge_step = next(
    step
    for step in sigma_double_prime_result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma514SigmaDoublePrimeBridgeStatement,
    )
  )

  sigma_double_prime_step = next(
    step
    for step in sigma_double_prime_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma514SigmaDoublePrimeStatement,
    )
  )

  pi13_6_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_pi13_6_finite_cyclic_inference_rule(),
      ),
      (
        sigma_double_prime_step,
        first_short_exact_step,
        low_result.pi12_5_step,
        pi13_11_step,
      ),
    )
  )

  pi13_6_step = next(
    step
    for step in pi13_6_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi13_6
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 4
    )
  )

  pi14_13_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop511_pi14_13_eta13_inference_rule(),
      ),
      (
        prop51_step,
      ),
    )
  )

  pi14_13 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=13,
  )

  pi14_13_step = next(
    step
    for step in pi14_13_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi14_13
    )
  )

  delta_eta13_squared_result = (
    run_inference_until_stable_with_history(
      (
        toda_514_delta_eta13_squared_zero_inference_rule(),
      ),
      (
        delta_eta13_step,
        prop53_step,
      ),
    )
  )

  delta_eta13_squared_step = next(
    step
    for step in delta_eta13_squared_result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      == RelationType.ZERO
      and isinstance(
        step.conclusion.lhs,
        MapApplication,
      )
      and step.conclusion.lhs.map
      == EHP_DELTA_MAP
      and isinstance(
        step.conclusion.lhs.expression,
        Composition,
      )
      and getattr(
        getattr(
          step.conclusion
          .lhs
          .expression
          .left,
          "generator",
          None,
        ),
        "index",
        None,
      )
      == 13
    )
  )

  pi15_13 = TodaPrimaryGroup(
    group_dimension=15,
    sphere_dimension=13,
  )

  pi14_7 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=7,
  )

  pi12_6 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=6,
  )

  second_delta_e_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi15_13,
      middle_term=pi13_6,
      target_term=pi14_7,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_e_h_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi13_6,
      middle_term=pi14_7,
      target_term=pi14_13,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_h_delta_window_step = create_legacy_given_proof_step(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi14_7,
      middle_term=pi14_13,
      target_term=pi12_6,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_short_exact_result = (
    run_inference_until_stable_with_history(
      (
        toda_514_second_short_exact_concrete_exactness_inference_rule(),
        toda_514_second_short_exact_inference_rule(),
      ),
      (
        delta_eta13_squared_step,
        delta_eta13_step,
        prop53_step,
        pi14_13_step,
        second_delta_e_window_step,
        second_e_h_window_step,
        second_h_delta_window_step,
      ),
    )
  )

  second_short_exact_step = next(
    step
    for step in second_short_exact_result.steps
    if isinstance(
      step.conclusion,
      Toda514SecondShortExactStatement,
    )
  )

  sigma_prime_result = (
    run_inference_until_stable_with_history(
      (
        toda_lemma514_sigma_prime_inference_rule(),
      ),
      (
        sigma_double_prime_step,
        second_short_exact_step,
        pi13_6_step,
        pi14_13_step,
      ),
    )
  )

  sigma_prime_step = next(
    step
    for step in sigma_prime_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma514SigmaPrimeStatement,
    )
  )

  pi14_7_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_pi14_7_finite_cyclic_inference_rule(),
      ),
      (
        sigma_prime_step,
        second_short_exact_step,
        pi13_6_step,
        pi14_13_step,
      ),
    )
  )

  pi14_7_step = next(
    step
    for step in pi14_7_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi14_7
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 8
    )
  )

  sigma8_result = (
    run_inference_until_stable_with_history(
      (
        toda_lemma514_sigma8_inference_rule(),
      ),
      (
        bridge_step,
        sigma_prime_step,
        pi14_7_step,
      ),
    )
  )

  sigma8_step = next(
    step
    for step in sigma8_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma514Sigma8Statement,
    )
  )

  return (
    TodaProp515SigmaChainBootstrapResult(
      low_result=low_result,
      prop51_step=prop51_step,
      prop53_step=prop53_step,
      lemma54_step=lemma54_step,
      eta_n_nu_n_plus_one_zero_step=(
        eta_n_nu_n_plus_one_zero_step
      ),
      delta_iota11_step=(
        delta_iota11_step
      ),
      delta_eta13_step=(
        delta_eta13_step
      ),
      pi13_11_step=pi13_11_step,
      first_short_exact_step=(
        first_short_exact_step
      ),
      bridge_step=bridge_step,
      sigma_double_prime_step=(
        sigma_double_prime_step
      ),
      pi13_6_step=pi13_6_step,
      pi14_13_step=pi14_13_step,
      second_short_exact_step=(
        second_short_exact_step
      ),
      sigma_prime_step=(
        sigma_prime_step
      ),
      pi14_7_step=pi14_7_step,
      sigma8_step=sigma8_step,
    )
  )
```

## toda_prop515_upper_bootstrap.py

### 変更後の import 全文

```python
from dataclasses import dataclass
from functools import lru_cache
from expression import (
  Composition,
  HomotopyElement,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
)
from low_dimensional_facts import (
  pi_15_15_free_cyclic_fact,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_prop515_sigma_chain_bootstrap import (
  TodaProp515SigmaChainBootstrapResult,
  build_toda_prop515_sigma_chain_bootstrap,
)
from toda_stable_generator_normalization import (
  toda_sigma_transport_generator_normalization_inference_rule,
)
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda515Sigma8Prop44SpecializationStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp44IsomorphismStatement,
  TodaProp515FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
  toda_45_isomorphism_inference_rule,
  toda_48_pi16_9_order_and_e4_injective_inference_rule,
  toda_lemma514_sigma_family_definition_inference_rule,
  toda_prop515_finite_dimensional_integration_inference_rule,
  toda_prop515_pi15_8_final_group_inference_rule,
  toda_prop515_pi16_9_sigma9_finite_cyclic_inference_rule,
  toda_prop515_sigma8_prop44_isomorphism_inference_rule,
  toda_prop515_sigma8_prop44_specialization_inference_rule,
  toda_prop515_sigma8_transported_decomposition_inference_rule,
  toda_sigma_family_definition_statement,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    create_legacy_specialization_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_toda_prop515_upper_bootstrap():
  sigma_chain_result = (
    build_toda_prop515_sigma_chain_bootstrap()
  )

  low_result = (
    sigma_chain_result.low_result
  )

  sigma8_step = (
    sigma_chain_result.sigma8_step
  )

  pi14_7_step = (
    sigma_chain_result.pi14_7_step
  )

  specialization_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_sigma8_prop44_specialization_inference_rule(),
      ),
      (
        sigma8_step,
      ),
    )
  )

  specialization_step = next(
    step
    for step in specialization_result.steps
    if isinstance(
      step.conclusion,
      Toda515Sigma8Prop44SpecializationStatement,
    )
  )

  sigma8 = (
    specialization_step
    .conclusion
    .alpha
  )

  pi14_7 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=7,
  )

  pi15_15 = TodaPrimaryGroup(
    group_dimension=15,
    sphere_dimension=15,
  )

  pi15_8 = TodaPrimaryGroup(
    group_dimension=15,
    sphere_dimension=8,
  )

  first_variable = HomotopyElement(
    name="α",
    dimension=14,
  )

  second_variable = HomotopyElement(
    name="β",
    dimension=15,
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=DirectSumGroup(
        summands=(
          pi14_7,
          pi15_15,
        ),
      ),
      target_group=pi15_8,
      alpha=sigma8,
      beta=first_variable,
      gamma=second_variable,
      formula=Sum(
        left=Suspension(
          expression=first_variable,
        ),
        right=Composition(
          left=sigma8,
          right=second_variable,
        ),
      ),
    )
  )

  decomposition_map_step = create_legacy_given_proof_step(
    conclusion=decomposition_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  prop44_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_sigma8_prop44_isomorphism_inference_rule(),
      ),
      (
        specialization_step,
        decomposition_map_step,
      ),
    )
  )

  prop44_isomorphism_step = next(
    step
    for step in prop44_result.steps
    if (
      step.conclusion
      == TodaProp44IsomorphismStatement(
        map=decomposition_map,
      )
    )
  )

  pi15_15_step = create_legacy_given_proof_step(
    conclusion=pi_15_15_free_cyclic_fact(),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  transported_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_sigma8_transported_decomposition_inference_rule(),
      ),
      (
        prop44_isomorphism_step,
        pi14_7_step,
        pi15_15_step,
      ),
    )
  )

  transported_decomposition_step = next(
    step
    for step in transported_result.steps
    if isinstance(
      step.conclusion,
      Toda515Sigma8TransportedDecompositionStatement,
    )
  )

  pi15_8_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_pi15_8_final_group_inference_rule(),
      ),
      (
        transported_decomposition_step,
      ),
    )
  )

  pi15_8_step = next(
    step
    for step in pi15_8_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi15_8
    )
  )

  n = ScalarSymbol(
    name="n",
  )

  sigma_family_range_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=8,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sigma_family_result = (
    run_inference_until_stable_with_history(
      (
        toda_lemma514_sigma_family_definition_inference_rule(),
      ),
      (
        sigma8_step,
        sigma_family_range_step,
      ),
    )
  )

  sigma_family_step = next(
    step
    for step in sigma_family_result.steps
    if isinstance(
      step.conclusion,
      TodaSigmaFamilyDefinitionStatement,
    )
    and step.conclusion.index
    == n
  )

  sigma9_definition_step = create_legacy_specialization_proof_step(
    conclusion=(
      toda_sigma_family_definition_statement(
        9,
        sigma8_step.conclusion,
      )
    ),
    premises=(
      sigma8_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  prop48_result = (
    run_inference_until_stable_with_history(
      (
        toda_48_pi16_9_order_and_e4_injective_inference_rule(),
      ),
      (
        low_result.pi12_5_step,
      ),
    )
  )

  prop48_step = next(
    step
    for step in prop48_result.steps
    if isinstance(
      step.conclusion,
      Toda48Pi16_9OrderAndE4InjectiveStatement,
    )
  )

  pi16_9_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_pi16_9_sigma9_finite_cyclic_inference_rule(),
      ),
      (
        prop48_step,
        sigma8_step,
        sigma9_definition_step,
        low_result.pi12_5_step,
      ),
    )
  )

  pi16_9 = TodaPrimaryGroup(
    group_dimension=16,
    sphere_dimension=9,
  )

  pi16_9_step = next(
    step
    for step in pi16_9_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi16_9
    )
  )

  stable_range_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=9,
      right=ScalarSum(
        left=7,
        right=2,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  higher_range_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=9,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  target_group = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=n,
      right=7,
    ),
    sphere_dimension=n,
  )

  stable_suspension_map = (
    TodaIteratedSuspensionMap(
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=9,
        ),
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=9,
          right=7,
        ),
        sphere_dimension=9,
      ),
      target_group=target_group,
    )
  )

  stable_suspension_map_step = create_legacy_given_proof_step(
    conclusion=stable_suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  stable_result = (
    run_inference_until_stable_with_history(
      (
        toda_45_isomorphism_inference_rule(),
        toda_45_generic_finite_cyclic_transport_inference_rule(),
        toda_sigma_transport_generator_normalization_inference_rule(),
      ),
      (
        pi16_9_step,
        sigma_family_step,
        sigma9_definition_step,
        stable_range_step,
        higher_range_step,
        stable_suspension_map_step,
      ),
    )
  )

  stable_isomorphism_step = next(
    step
    for step in stable_result.steps
    if (
      step.conclusion
      == Toda45IsomorphismStatement(
        map=stable_suspension_map,
      )
    )
  )

  higher_step = next(
    step
    for step in stable_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == target_group
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 16
      and step.conclusion.rhs.generator
      == sigma_family_step.conclusion.element
    )
  )

  aggregate_result = (
    run_inference_until_stable_with_history(
      (
        toda_prop515_finite_dimensional_integration_inference_rule(),
      ),
      (
        low_result.pi9_2_zero_step,
        low_result.pi10_3_zero_step,
        low_result.pi11_4_zero_step,
        low_result.pi12_5_step,
        sigma_chain_result.pi13_6_step,
        sigma_chain_result.pi14_7_step,
        pi15_8_step,
        higher_step,
        higher_range_step,
      ),
    )
  )

  aggregate_step = next(
    step
    for step in aggregate_result.steps
    if isinstance(
      step.conclusion,
      TodaProp515FiniteDimensionalStatement,
    )
  )

  return (
    TodaProp515UpperBootstrapResult(
      sigma_chain_result=(
        sigma_chain_result
      ),
      specialization_step=(
        specialization_step
      ),
      decomposition_map_step=(
        decomposition_map_step
      ),
      prop44_isomorphism_step=(
        prop44_isomorphism_step
      ),
      pi15_15_step=pi15_15_step,
      transported_decomposition_step=(
        transported_decomposition_step
      ),
      pi15_8_step=pi15_8_step,
      sigma_family_step=sigma_family_step,
      sigma9_definition_step=(
        sigma9_definition_step
      ),
      prop48_step=prop48_step,
      pi16_9_step=pi16_9_step,
      stable_isomorphism_step=(
        stable_isomorphism_step
      ),
      higher_range_step=higher_range_step,
      higher_step=higher_step,
      aggregate_step=aggregate_step,
    )
  )
```

## toda_prop56_zero_bootstrap.py

### 変更後の import 全文

```python
from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
  TodaBracket,
  WhiteheadProduct,
  Zero,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from low_dimensional_facts import (
  pi_6_7_zero_fact,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  equality_preserved_under_multiple_inference_rule,
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
  nested_integer_multiple_inference_rule,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_midstream_bootstrap import (
  build_phase59_hopf_surjective_step,
  build_phase59_pi5_3_step,
  build_phase59_prop53_step,
  build_phase60_pi6_5_step,
  build_phase62_toda55_step,
  build_phase63_toda56_step,
)
from toda_phase65_bootstrap import (
  build_toda_prop56_bootstrap_step,
)
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
)
from toda_rules import (
  Toda36Lemma54SpecializationStatement,
  Toda45IsomorphismStatement,
  Toda54BracketUpToSignStatement,
  Toda54IndeterminacyGeneratorStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  Toda56Nu4Prop44SpecializationStatement,
  TodaBracketMembershipStatement,
  TodaDeltaImageUpToSignStatement,
  TodaLemma54DoubleSuspensionUpToSignStatement,
  TodaLemma54HopfOddMultipleStatement,
  TodaLemma54Nu4BranchFormula,
  TodaLemma54Nu4ConstructionStatement,
  TodaLemma54Statement,
  TodaLemma54WhiteheadCorrectionDataStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaSuspensionSurjectiveStatement,
  toda_32_phase60_suspension_surjective_inference_rule,
  toda_36_lemma54_specialization_inference_rule,
  toda_53_eta3_twice_zero_inference_rule,
  toda_53_n3_delta_injective_hopf_zero_inference_rule,
  toda_53_n3_delta_zero_suspension_injective_inference_rule,
  toda_53_n3_hopf_eta5_surjective_inference_rule,
  toda_53_n3_hopf_surjective_delta_zero_inference_rule,
  toda_53_n3_hopf_zero_suspension_surjective_inference_rule,
  toda_53_n3_prop51_delta_injective_inference_rule,
  toda_53_n3_suspension_isomorphism_inference_rule,
  toda_54_indeterminacy_double_nu_prime_generator_inference_rule,
  toda_54_n5_t3_specialization_inference_rule,
  toda_54_nu_prime_bracket_inclusion_inference_rule,
  toda_54_nu_prime_triple_eta_transport_inference_rule,
  toda_54_t0_bridge_inference_rule,
  toda_54_t_ge_1_indeterminacy_eta_cube_inference_rule,
  toda_54_t_ge_1_up_to_sign_inference_rule,
  toda_55_nu_family_double_suspension_transport_inference_rule,
  toda_56_nu4_decomposition_isomorphism_inference_rule,
  toda_56_nu4_prop44_isomorphism_inference_rule,
  toda_56_nu4_prop44_specialization_inference_rule,
  toda_lemma54_double_suspension_up_to_sign_inference_rule,
  toda_lemma54_eta6_twice_zero_inference_rule,
  toda_lemma54_integration_inference_rule,
  toda_lemma54_literature_statements,
  toda_lemma54_nu4_double_suspension_inference_rule,
  toda_lemma54_nu4_hopf_inference_rule,
  toda_lemma54_nu4_membership_inference_rule,
  toda_lemma54_nu4_piecewise_construction_inference_rule,
  toda_lemma54_whitehead_correction_data_inference_rule,
  toda_nu_family_definition_statement,
  toda_prop44_first_summand_restriction_inference_rule,
  toda_prop44_isomorphism_inference_rule,
  toda_prop44_suspension_injective_inference_rule,
  toda_prop53_n4_eta_square_suspension_bridge_inference_rule,
  toda_prop53_n4_phase48_injectivity_bridge_inference_rule,
  toda_prop53_n4_pi6_4_finite_cyclic_transport_inference_rule,
  toda_prop53_n4_suspension_isomorphism_inference_rule,
  toda_prop53_n4_zero_right_suspension_surjective_inference_rule,
  toda_delta_iota5_two_eta2_up_to_sign_inference_rule,
  toda_eta3_suspension_relation_inference_rule,
  toda_eta_family_definition_statement,
  toda_higher_eta_family_bridge_inference_rule,
  toda_higher_eta_finite_cyclic_generator_inference_rule,
  toda_prop51_finite_dimensional_integration_inference_rule,
)
from toda_upstream_bootstrap import (
  _build_phase49_result,
  _build_phase50_result,
  build_toda_45_stable_isomorphism_step,
  build_toda_prop56_upstream_core,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    create_legacy_specialization_proof_step,
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def _require_match(
  rule,
  premises,
) -> ProofStep:
  match = find_inference_match(
    rule,
    premises,
  )

  if match is None:
    raise ValueError(
      "expected inference rule to match"
    )

  return derive_inference_proof_step(
    match
  )
```

```python
def _build_pi4_3_prop51_specialization_link_step(
  pi4_3_step: ProofStep,
  prop51_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    pi4_3_step,
    ProofStep,
  ):
    raise TypeError(
      "pi4_3_step must be a ProofStep"
    )

  if not isinstance(
    prop51_step,
    ProofStep,
  ):
    raise TypeError(
      "prop51_step must be a ProofStep"
    )

  if not isinstance(
    pi4_3_step.conclusion,
    Relation,
  ):
    raise TypeError(
      "pi4_3_step conclusion must be a Relation"
    )

  if (
    pi4_3_step.conclusion.lhs
    != TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )
  ):
    raise ValueError(
      "pi4_3_step must conclude a relation for pi_4^3"
    )

  if not isinstance(
    prop51_step.conclusion,
    TodaProp51FiniteDimensionalStatement,
  ):
    raise TypeError(
      "prop51_step must conclude a "
      "TodaProp51FiniteDimensionalStatement"
    )

  general_step = create_legacy_specialization_proof_step(
    conclusion=(
      prop51_step
      .conclusion
      .higher_eta_group_relation
    ),
    premises=(
      prop51_step,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=(
        "Toda Proposition 5.1 "
        "higher eta group relation"
      ),
      description=(
        "Expose the higher-eta group component "
        "of Toda Proposition 5.1 as a fixed "
        "general literature statement."
      ),
      literature_reference=LiteratureReference(
        label="Toda Proposition 5.1",
        locator="Proposition 5.1",
      ),
    ),
  )

  return create_legacy_specialization_proof_step(
    conclusion=pi4_3_step.conclusion,
    premises=(
      pi4_3_step,
      general_step,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=(
        "pi_4^3 Proposition 5.1 "
        "specialization linkage"
      ),
      description=(
        "Link the independently derived concrete "
        "pi_4^3 group relation to the general "
        "higher-eta group component of Toda "
        "Proposition 5.1 without replacing the "
        "existing pi_4^3 derivation."
      ),
    ),
  )
```

```python
def _build_prop51_step() -> ProofStep:
  phase49 = _build_phase49_result()
  phase50 = _build_phase50_result()

  pi3_2_step = _find_unique_step(
    phase49[
      "result"
    ].steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=3,
        sphere_dimension=2,
      )
      and isinstance(
        step.conclusion.rhs,
        FreeCyclicGroup,
      )
    ),
    "pi_3^2",
  )

  eta2_hopf_step = _find_unique_step(
    phase49[
      "result"
    ].steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        MapApplication,
      )
      and step.conclusion.lhs.map
      == EHP_H_MAP
      and getattr(
        step.conclusion.lhs.expression,
        "name",
        None,
      )
      == "η₂"
    ),
    "H(eta_2)",
  )

  delta_step = _find_unique_step(
    phase50[
      "result"
    ].steps,
    lambda step: (
      isinstance(
        step.conclusion,
        TodaDeltaImageUpToSignStatement,
      )
      and isinstance(
        step.conclusion.positive_value,
        Multiple,
      )
      and step.conclusion.positive_value.coefficient
      == 2
      and (
        step.inference_rule
        is not None
      )
      and (
        step.inference_rule
        .literature_reference
        is not None
      )
      and (
        step.inference_rule
        .literature_reference
        .locator
        == "Proposition 5.1"
      )
    ),
    "Delta(iota_5)=+-2eta_2",
  )

  n = ScalarSymbol(
    name="n",
  )

  stable_step = build_toda_45_stable_isomorphism_step(
    n=3,
    k=1,
    m=n,
  )

  transported_result = (
    run_inference_until_stable_with_history(
      toda_45_generic_finite_cyclic_transport_inference_rule(),
      (
        phase50[
          "final_group_step"
        ],
        stable_step,
      ),
    )
  )

  transported_step = _find_unique_step(
    transported_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
    ),
    "higher eta transported group",
  )

  eta_n_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      n
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta3_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      3
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta3_result = run_inference_until_stable_with_history(
    toda_eta3_suspension_relation_inference_rule(),
    (
      eta3_definition_step,
    ),
  )

  eta3_relation_step = _find_unique_step(
    eta3_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == eta3_definition_step.conclusion.element
    ),
    "eta_3 suspension relation",
  )

  higher_bridge_result = (
    run_inference_until_stable_with_history(
      toda_higher_eta_family_bridge_inference_rule(),
      (
        eta_n_definition_step,
        eta3_relation_step,
      ),
    )
  )

  higher_bridge_step = _find_unique_step(
    higher_bridge_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.rhs
      == eta_n_definition_step.conclusion.element
    ),
    "higher eta bridge",
  )

  higher_result = run_inference_until_stable_with_history(
    toda_higher_eta_finite_cyclic_generator_inference_rule(),
    (
      transported_step,
      higher_bridge_step,
    ),
  )

  higher_step = _find_unique_step(
    higher_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == transported_step.conclusion.lhs
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.generator
      == eta_n_definition_step.conclusion.element
    ),
    "higher eta group",
  )

  expected = TodaProp51FiniteDimensionalStatement(
    pi3_2_group_relation=pi3_2_step.conclusion,
    eta2_hopf_relation=eta2_hopf_step.conclusion,
    delta_iota5_relation=delta_step.conclusion,
    higher_eta_group_relation=higher_step.conclusion,
  )

  result = run_inference_until_stable_with_history(
    toda_prop51_finite_dimensional_integration_inference_rule(),
    (
      pi3_2_step,
      eta2_hopf_step,
      delta_step,
      higher_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: step.conclusion == expected,
    "Toda Proposition 5.1",
  )
```

```python
def _build_n3_suspension_isomorphism_step(
  prop51_step: ProofStep,
  hopf_eta5_step: ProofStep,
) -> ProofStep:
  pi_4_2 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=2,
  )
  pi_5_3 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=3,
  )
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )
  pi_6_3 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )
  pi_6_5 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=5,
  )
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  exactness_steps = (
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_5_3,
          middle_term=pi_5_5,
          target_term=pi_3_2,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_4_2,
          middle_term=pi_5_3,
          target_term=pi_5_5,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_6_3,
          middle_term=pi_6_5,
          target_term=pi_4_2,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_6_5,
          middle_term=pi_4_2,
          target_term=pi_5_3,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = run_inference_until_stable_with_history(
    (
      toda_53_n3_prop51_delta_injective_inference_rule(),
      toda_53_n3_delta_injective_hopf_zero_inference_rule(),
      toda_53_n3_hopf_zero_suspension_surjective_inference_rule(),
      toda_53_n3_hopf_eta5_surjective_inference_rule(),
      toda_53_n3_hopf_surjective_delta_zero_inference_rule(),
      toda_53_n3_delta_zero_suspension_injective_inference_rule(),
      toda_53_n3_suspension_isomorphism_inference_rule(),
    ),
    (
      prop51_step,
      hopf_eta5_step,
      *exactness_steps,
    ),
  )

  expected = TodaSuspensionIsomorphismStatement(
    map=TodaSuspensionMap(
      source_group=pi_4_2,
      target_group=pi_5_3,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: step.conclusion == expected,
    "E: pi_4^2 -> pi_5^3 isomorphism",
  )
```

```python
def _build_phase48_injectivity_step() -> ProofStep:
  i = 6
  n = 4
  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )
  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )
  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=two_n_minus_one,
  )
  beta = HomotopyElement(
    name="β",
    dimension=i_minus_one,
  )
  gamma = HomotopyElement(
    name="γ",
    dimension=i,
  )
  iota = HomotopyElement(
    name="ι_(2n-1)",
    dimension=two_n_minus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=two_n_minus_one,
    ),
  )

  first_summand = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=n_minus_one,
  )
  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=two_n_minus_one,
  )
  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  decomposition_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(
        first_summand,
        second_summand,
      ),
    ),
    target_group=target_group,
    alpha=alpha,
    beta=beta,
    gamma=gamma,
    formula=Sum(
      left=Suspension(
        expression=beta,
      ),
      right=Composition(
        left=alpha,
        right=gamma,
      ),
    ),
  )

  suspension_map = TodaSuspensionMap(
    source_group=first_summand,
    target_group=target_group,
  )

  premise_steps = (
    create_legacy_given_proof_step(
      conclusion=TodaPrimaryGroupMembershipStatement(
        element=alpha,
        group=TodaPrimaryGroup(
          group_dimension=two_n_minus_one,
          sphere_dimension=n,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=alpha,
        ),
        rhs=iota,
        relation_type=RelationType.EQUALITY,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=decomposition_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=suspension_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop44_isomorphism_inference_rule(),
      toda_prop44_first_summand_restriction_inference_rule(),
      toda_prop44_suspension_injective_inference_rule(),
    ),
    premise_steps,
  )

  return _find_unique_step(
    result.steps,
    lambda step: isinstance(
      step.conclusion,
      TodaProp44SuspensionInjectiveStatement,
    ),
    "Phase 48 suspension injectivity",
  )
```

```python
def _build_n4_suspension_isomorphism_step() -> ProofStep:
  pi_5_3 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=3,
  )
  pi_6_4 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=4,
  )
  pi_6_7 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=7,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop53_n4_phase48_injectivity_bridge_inference_rule(),
      toda_prop53_n4_zero_right_suspension_surjective_inference_rule(),
      toda_prop53_n4_suspension_isomorphism_inference_rule(),
    ),
    (
      _build_phase48_injectivity_step(),
      create_legacy_given_proof_step(
        conclusion=pi_6_7_zero_fact(),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=TodaProp42ExactnessStatement(
          window=TodaEHPExactnessWindow(
            source_term=pi_5_3,
            middle_term=pi_6_4,
            target_term=pi_6_7,
            first_map=EHP_E_MAP,
            second_map=EHP_H_MAP,
          ),
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    ),
  )

  expected = TodaSuspensionIsomorphismStatement(
    map=TodaSuspensionMap(
      source_group=pi_5_3,
      target_group=pi_6_4,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: step.conclusion == expected,
    "E: pi_5^3 -> pi_6^4 isomorphism",
  )
```

```python
def _build_pi6_4_step(
  pi5_3_step: ProofStep,
) -> ProofStep:
  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )
  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  expected = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=eta_4,
        right=eta_5,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop53_n4_eta_square_suspension_bridge_inference_rule(),
      toda_prop53_n4_pi6_4_finite_cyclic_transport_inference_rule(),
    ),
    (
      pi5_3_step,
      _build_n4_suspension_isomorphism_step(),
      create_legacy_given_proof_step(
        conclusion=toda_eta_family_definition_statement(
          4
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=toda_eta_family_definition_statement(
          5
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: step.conclusion == expected,
    "pi_6^4",
  )
```

```python
def _build_higher_eta_transport(
  pi6_4_step: ProofStep,
) -> tuple[
  ProofStep,
  ProofStep,
]:
  n = ScalarSymbol(
    name="n",
  )

  stable_step = build_toda_45_stable_isomorphism_step(
    n=4,
    k=2,
    m=n,
  )

  higher_range_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable_with_history(
    toda_45_generic_finite_cyclic_transport_inference_rule(),
    (
      pi6_4_step,
      stable_step,
    ),
  )

  higher_step = _find_unique_step(
    result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=2,
        ),
        sphere_dimension=n,
      )
    ),
    "higher eta-square transport",
  )

  return (
    higher_step,
    higher_range_step,
  )
```

```python
def _build_phase60_toda54(
  prop53_step: ProofStep,
  nu_prime_double_step: ProofStep,
) -> tuple[
  ProofStep,
  ProofStep,
]:
  n = ScalarSymbol(
    name="n",
  )
  t = ScalarSymbol(
    name="t",
  )
  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )
  n_plus_two = ScalarSum(
    left=n,
    right=2,
  )

  eta_n = HomotopyElement(
    name="η_n",
    dimension=n,
    source=n_plus_one,
    target=n,
    generator=GeneratorSymbol(
      family="η",
      index=n,
    ),
  )
  eta_n_plus_one = HomotopyElement(
    name="η_(n+1)",
    dimension=n_plus_one,
    source=n_plus_two,
    target=n_plus_one,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_one,
    ),
  )
  eta_n_plus_two = HomotopyElement(
    name="η_(n+2)",
    dimension=n_plus_two,
    source=ScalarSum(
      left=n,
      right=3,
    ),
    target=n_plus_two,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_two,
    ),
  )
  iota_n_plus_one = HomotopyElement(
    name="ι_(n+1)",
    dimension=n_plus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=n_plus_one,
    ),
  )

  bracket = TodaBracket(
    first=eta_n,
    second=Multiple(
      coefficient=2,
      expression=iota_n_plus_one,
    ),
    third=eta_n_plus_one,
    index=t,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  suspended_nu_prime = IteratedSuspension(
    expression=nu_prime,
    exponent=ScalarSum(
      left=n,
      right=ScalarProduct(
        left=-1,
        right=3,
      ),
    ),
  )

  indeterminacy_result = (
    run_inference_until_stable_with_history(
      (
        toda_54_t_ge_1_indeterminacy_eta_cube_inference_rule(),
        toda_54_nu_prime_triple_eta_transport_inference_rule(),
        toda_54_indeterminacy_double_nu_prime_generator_inference_rule(),
      ),
      (
        prop53_step,
        nu_prime_double_step,
        create_legacy_given_proof_step(
          conclusion=ScalarGreaterEqualStatement(
            left=n,
            right=3,
          ),
          premises=(),
          rule=ProofRule.GIVEN,
        ),
        create_legacy_given_proof_step(
          conclusion=ScalarGreaterEqualStatement(
            left=t,
            right=1,
          ),
          premises=(),
          rule=ProofRule.GIVEN,
        ),
      ),
    )
  )

  indeterminacy_step = _find_unique_step(
    indeterminacy_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Toda54IndeterminacyGeneratorStatement,
      )
      and step.conclusion.bracket
      == bracket
      and step.conclusion.generator
      == Multiple(
        coefficient=2,
        expression=suspended_nu_prime,
      )
    ),
    "Toda (5.4) indeterminacy",
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )
  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )
  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  source_membership_step = create_legacy_given_proof_step(
    conclusion=TodaBracketMembershipStatement(
      element=nu_prime,
      bracket=TodaBracket(
        first=eta_3,
        second=Multiple(
          coefficient=2,
          expression=iota_4,
        ),
        third=eta_4,
        index=1,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  from toda_rules import (
    toda_53_nu_prime_bracket_specialization_inference_rule,
  )

  inclusion_result = (
    run_inference_until_stable_with_history(
      (
        toda_53_nu_prime_bracket_specialization_inference_rule(),
        toda_54_nu_prime_bracket_inclusion_inference_rule(),
      ),
      (
        source_membership_step,
        create_legacy_given_proof_step(
          conclusion=ScalarGreaterEqualStatement(
            left=n,
            right=3,
          ),
          premises=(),
          rule=ProofRule.GIVEN,
        ),
        create_legacy_given_proof_step(
          conclusion=ScalarGreaterEqualStatement(
            left=t,
            right=1,
          ),
          premises=(),
          rule=ProofRule.GIVEN,
        ),
        create_legacy_given_proof_step(
          conclusion=ScalarGreaterEqualStatement(
            left=ScalarSum(
              left=n,
              right=-2,
            ),
            right=t,
          ),
          premises=(),
          rule=ProofRule.GIVEN,
        ),
      ),
    )
  )

  membership_step = _find_unique_step(
    inclusion_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        TodaBracketMembershipStatement,
      )
      and step.conclusion.element
      == suspended_nu_prime
      and step.conclusion.bracket
      == bracket
    ),
    "Toda (5.4) inclusion",
  )

  result = run_inference_until_stable_with_history(
    (
      toda_54_t_ge_1_up_to_sign_inference_rule(),
      toda_32_phase60_suspension_surjective_inference_rule(),
      toda_54_t0_bridge_inference_rule(),
    ),
    (
      indeterminacy_step,
      membership_step,
      create_legacy_given_proof_step(
        conclusion=ScalarGreaterEqualStatement(
          left=n,
          right=3,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    ),
  )

  indexed_step = _find_unique_step(
    result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Toda54BracketUpToSignStatement,
      )
      and step.conclusion.bracket
      == bracket
    ),
    "Toda (5.4) indexed up-to-sign",
  )

  return (
    indexed_step,
    indeterminacy_step,
  )
```

```python
def _build_lemma54_step(
  prop51_step: ProofStep,
  prop53_step: ProofStep,
  nu_prime_hopf_step: ProofStep,
  nu_prime_double_step: ProofStep,
  pi4_3_step: ProofStep,
) -> tuple[
  ProofStep,
  ProofStep,
]:
  two_eta3_result = run_inference_until_stable_with_history(
    toda_53_eta3_twice_zero_inference_rule(),
    (
      pi4_3_step,
    ),
  )

  two_eta3_step = _find_unique_step(
    two_eta3_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      == RelationType.ZERO
    ),
    "2 eta_3 zero",
  )

  indexed_toda54_step, _ = _build_phase60_toda54(
    prop53_step,
    nu_prime_double_step,
  )

  phase60_6_result = (
    run_inference_until_stable_with_history(
      (
        toda_lemma54_eta6_twice_zero_inference_rule(),
        toda_36_lemma54_specialization_inference_rule(),
        toda_54_n5_t3_specialization_inference_rule(),
        toda_lemma54_double_suspension_up_to_sign_inference_rule(),
      ),
      (
        prop51_step,
        two_eta3_step,
        indexed_toda54_step,
      ),
    )
  )

  theorem36_step = _find_unique_step(
    phase60_6_result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda36Lemma54SpecializationStatement,
    ),
    "Toda (3.6) Lemma 5.4 specialization",
  )

  final_double_step = _find_unique_step(
    phase60_6_result.steps,
    lambda step: isinstance(
      step.conclusion,
      TodaLemma54DoubleSuspensionUpToSignStatement,
    ),
    "Lemma 5.4 double suspension",
  )

  pi6_5_step = build_phase60_pi6_5_step(
    prop51_step,
    theorem36_step,
    final_double_step,
    nu_prime_hopf_step,
  )

  from toda_rules import (
    toda_48_lemma54_hopf_odd_multiple_inference_rule,
    toda_lemma54_pi6_5_finite_cyclic_inference_rule,
  )

  phase60_7_result = (
    run_inference_until_stable_with_history(
      (
        toda_lemma54_pi6_5_finite_cyclic_inference_rule(),
        toda_48_lemma54_hopf_odd_multiple_inference_rule(),
      ),
      (
        prop51_step,
        theorem36_step,
        final_double_step,
        nu_prime_hopf_step,
      ),
    )
  )

  expected_hopf_odd = (
    TodaLemma54HopfOddMultipleStatement(
      alpha_star=theorem36_step.conclusion.alpha_star,
      parameter=ScalarSymbol(
        name="s",
      ),
      generator=HomotopyElement(
        name="ι_7",
        dimension=7,
        generator=GeneratorSymbol(
          family="ι",
          index=7,
        ),
      ),
    )
  )

  hopf_odd_step = _find_unique_step(
    phase60_7_result.steps,
    lambda step: (
      step.conclusion
      == expected_hopf_odd
    ),
    "Lemma 5.4 Hopf odd multiple",
  )

  alpha_star = theorem36_step.conclusion.alpha_star
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )
  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )
  iota_7 = HomotopyElement(
    name="ι_7",
    dimension=7,
    generator=GeneratorSymbol(
      family="ι",
      index=7,
    ),
  )
  whitehead_square = WhiteheadProduct(
    left=iota_4,
    right=iota_4,
  )
  whitehead_step = create_legacy_given_proof_step(
    conclusion=whitehead_square,
    premises=(),
    rule=ProofRule.GIVEN,
  )
  s = ScalarSymbol(
    name="s",
  )
  u = ScalarSymbol(
    name="u",
  )

  expected_whitehead_data = (
    TodaLemma54WhiteheadCorrectionDataStatement(
      whitehead_square=whitehead_square,
      sign_parameter=u,
      hopf_positive_value=Multiple(
        coefficient=2,
        expression=iota_7,
      ),
      suspension_zero_relation=Relation(
        lhs=Suspension(
          expression=whitehead_square,
        ),
        rhs=Zero(),
        relation_type=RelationType.ZERO,
      ),
    )
  )

  nu4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  expected_construction = (
    TodaLemma54Nu4ConstructionStatement(
      alpha_star=alpha_star,
      nu4=nu4,
      parameter=s,
      whitehead_data=expected_whitehead_data,
      double_suspension_value=(
        IteratedSuspension(
          expression=nu_prime,
          exponent=2,
        )
      ),
      positive_branch=TodaLemma54Nu4BranchFormula(
        double_suspension_sign=1,
        alpha_star_sign=1,
        whitehead_coefficient_sign=-1,
        parameter_offset=0,
      ),
      negative_branch=TodaLemma54Nu4BranchFormula(
        double_suspension_sign=-1,
        alpha_star_sign=-1,
        whitehead_coefficient_sign=1,
        parameter_offset=1,
      ),
    )
  )

  phase60_8_result = (
    run_inference_until_stable_with_history(
      (
        toda_lemma54_whitehead_correction_data_inference_rule(),
        toda_lemma54_nu4_piecewise_construction_inference_rule(),
        toda_lemma54_nu4_membership_inference_rule(),
        toda_lemma54_nu4_hopf_inference_rule(),
        toda_lemma54_nu4_double_suspension_inference_rule(),
      ),
      (
        hopf_odd_step,
        final_double_step,
        whitehead_step,
      ),
    )
  )

  construction_step = _find_unique_step(
    phase60_8_result.steps,
    lambda step: step.conclusion == expected_construction,
    "nu_4 construction",
  )

  membership_step = _find_unique_step(
    phase60_8_result.steps,
    lambda step: isinstance(
      step.conclusion,
      HomotopyGroupMembershipStatement,
    ),
    "nu_4 membership",
  )

  hopf_step = _find_unique_step(
    phase60_8_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        MapApplication,
      )
      and step.conclusion.lhs.expression
      == nu4
    ),
    "H(nu_4)",
  )

  double_step = _find_unique_step(
    phase60_8_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        Multiple,
      )
      and step.conclusion.lhs.expression
      == Suspension(
        expression=nu4,
      )
    ),
    "2E nu_4",
  )

  expected_lemma54 = TodaLemma54Statement(
    nu4=nu4,
    membership=membership_step.conclusion,
    hopf_relation=hopf_step.conclusion,
    double_suspension_relation=double_step.conclusion,
    literature_statements=toda_lemma54_literature_statements(),
  )

  integration_result = (
    run_inference_until_stable_with_history(
      toda_lemma54_integration_inference_rule(),
      (
        membership_step,
        hopf_step,
        double_step,
      ),
    )
  )

  lemma54_step = _find_unique_step(
    integration_result.steps,
    lambda step: (
      step.conclusion
      == expected_lemma54
    ),
    "Toda Lemma 5.4",
  )

  return (
    lemma54_step,
    pi6_5_step,
  )
```

```python
def _build_toda55_step(
  lemma54_step: ProofStep,
  triple_eta_step: ProofStep,
) -> ProofStep:
  n = ScalarSymbol(
    name="n",
  )

  definition_step = create_legacy_given_proof_step(
    conclusion=toda_nu_family_definition_statement(
      n
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  n_range_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  double_result = run_inference_until_stable_with_history(
    toda_55_nu_family_double_suspension_transport_inference_rule(),
    (
      lemma54_step,
      definition_step,
      n_range_step,
    ),
  )

  double_step = _find_unique_step(
    double_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        Multiple,
      )
      and step.conclusion.lhs.coefficient
      == 2
    ),
    "2 nu_n",
  )

  doubled_step = _require_match(
    equality_preserved_under_multiple_inference_rule(
      coefficient=2,
    ),
    (
      double_step,
    ),
  )

  nu_n = definition_step.conclusion.element

  nested_step = _require_match(
    nested_integer_multiple_inference_rule(
      outer_coefficient=2,
      inner_coefficient=2,
      expression=nu_n,
    ),
    (),
  )

  nested_symmetry_step = _require_match(
    equality_symmetry_inference_rule(),
    (
      nested_step,
    ),
  )

  four_to_double_step = _require_match(
    equality_transitivity_inference_rule(),
    (
      nested_symmetry_step,
      doubled_step,
    ),
  )

  quadruple_step = _require_match(
    equality_transitivity_inference_rule(),
    (
      four_to_double_step,
      triple_eta_step,
    ),
  )

  return build_phase62_toda55_step(
    lemma54_step,
    definition_step,
    n_range_step,
    double_step,
    quadruple_step,
  )
```

```python
def _build_toda56_step(
  lemma54_step: ProofStep,
) -> ProofStep:
  specialization_result = (
    run_inference_until_stable_with_history(
      toda_56_nu4_prop44_specialization_inference_rule(),
      (
        lemma54_step,
      ),
    )
  )

  specialization_step = _find_unique_step(
    specialization_result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda56Nu4Prop44SpecializationStatement,
    ),
    "nu_4 Prop.4.4 specialization",
  )

  nu_4 = specialization_step.conclusion.alpha
  i = ScalarSymbol(
    name="i",
  )
  first_variable = HomotopyElement(
    name="α",
    dimension=3,
    source=ScalarSum(
      left=i,
      right=-1,
    ),
    target=3,
  )
  second_variable = HomotopyElement(
    name="β",
    dimension=7,
    source=i,
    target=7,
  )

  decomposition_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=i,
            right=-1,
          ),
          sphere_dimension=3,
        ),
        TodaPrimaryGroup(
          group_dimension=i,
          sphere_dimension=7,
        ),
      ),
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=4,
    ),
    alpha=nu_4,
    beta=first_variable,
    gamma=second_variable,
    formula=Sum(
      left=Suspension(
        expression=first_variable,
      ),
      right=Composition(
        left=nu_4,
        right=second_variable,
      ),
    ),
  )

  prop44_result = run_inference_until_stable_with_history(
    toda_56_nu4_prop44_isomorphism_inference_rule(),
    (
      specialization_step,
      create_legacy_given_proof_step(
        conclusion=decomposition_map,
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    ),
  )

  prop44_step = _find_unique_step(
    prop44_result.steps,
    lambda step: isinstance(
      step.conclusion,
      TodaProp44IsomorphismStatement,
    ),
    "nu_4 Prop.4.4 isomorphism",
  )

  semantics_result = (
    run_inference_until_stable_with_history(
      toda_56_nu4_decomposition_isomorphism_inference_rule(),
      (
        prop44_step,
      ),
    )
  )

  decomposition_step = _find_unique_step(
    semantics_result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda56Nu4DecompositionIsomorphismStatement,
    ),
    "Toda (5.6) semantics",
  )

  return build_phase63_toda56_step(
    decomposition_step,
    lemma54_step,
  )
```

```python
def build_toda_prop56_zero_argument_step() -> ProofStep:
  core = build_toda_prop56_upstream_core()

  phase50 = _build_phase50_result()
  pi4_3_step = phase50[
    "final_group_step"
  ]

  prop51_step = _build_prop51_step()

  pi4_2_step = _build_pi4_2_step(
    pi4_3_step,
    core[
      "toda52_step"
    ],
    prop51_step=prop51_step,
  )

  n3_isomorphism_step = (
    _build_n3_suspension_isomorphism_step(
      prop51_step,
      core[
        "hopf_nu_prime_step"
      ],
    )
  )

  pi5_3_step = build_phase59_pi5_3_step(
    pi4_2_step,
    n3_isomorphism_step,
  )

  pi6_4_step = _build_pi6_4_step(
    pi5_3_step
  )

  (
    higher_transport_step,
    higher_range_step,
  ) = _build_higher_eta_transport(
    pi6_4_step
  )

  prop53_step = build_phase59_prop53_step(
    pi4_2_step,
    pi5_3_step,
    pi6_4_step,
    higher_transport_step,
    higher_range_step,
  )

  hopf_surjective_step = (
    build_phase59_hopf_surjective_step(
      prop51_step,
      core[
        "hopf_nu_prime_step"
      ],
    )
  )

  lemma54_step, pi6_5_step = (
    _build_lemma54_step(
      prop51_step,
      prop53_step,
      core[
        "hopf_nu_prime_step"
      ],
      core[
        "double_step"
      ],
      pi4_3_step,
    )
  )

  n = ScalarSymbol(
    name="n",
  )
  t = ScalarSymbol(
    name="t",
  )

  phase60_3_result = (
    run_inference_until_stable_with_history(
      (
        toda_54_t_ge_1_indeterminacy_eta_cube_inference_rule(),
        toda_54_nu_prime_triple_eta_transport_inference_rule(),
        toda_54_indeterminacy_double_nu_prime_generator_inference_rule(),
      ),
      (
        prop53_step,
        core[
          "double_step"
        ],
        create_legacy_given_proof_step(
          conclusion=ScalarGreaterEqualStatement(
            left=n,
            right=3,
          ),
          premises=(),
          rule=ProofRule.GIVEN,
        ),
        create_legacy_given_proof_step(
          conclusion=ScalarGreaterEqualStatement(
            left=t,
            right=1,
          ),
          premises=(),
          rule=ProofRule.GIVEN,
        ),
      ),
    )
  )

  triple_eta_step = _find_unique_step(
    phase60_3_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        Multiple,
      )
      and step.conclusion.lhs.coefficient
      == 2
      and isinstance(
        step.conclusion.lhs.expression,
        IteratedSuspension,
      )
    ),
    "triple eta transport",
  )

  toda55_step = _build_toda55_step(
    lemma54_step,
    triple_eta_step,
  )

  toda56_step = _build_toda56_step(
    lemma54_step
  )

  return build_toda_prop56_bootstrap_step(
    core[
      "toda52_step"
    ],
    pi5_3_step,
    core[
      "hopf_nu_prime_step"
    ],
    prop53_step,
    core[
      "double_step"
    ],
    core[
      "membership_step"
    ],
    hopf_surjective_step,
    pi6_5_step,
    toda55_step,
    toda56_step,
    core[
      "stable_isomorphism_step"
    ],
  )
```

## toda_prop58_zero_bootstrap.py

### 変更後の import 全文

```python
from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
  barratt_hilton_first_inference_rule,
  barratt_hilton_second_inference_rule,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarPower,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
  WhiteheadProduct,
  Zero,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from hopf_rules import (
  toda_prop22_right_inference_rule,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
  apply_inference_match,
  find_inference_match,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_midstream_bootstrap import (
  build_phase59_pi5_3_step,
  build_phase59_prop53_step,
)
from toda_prop56_zero_bootstrap import (
  _build_higher_eta_transport,
  _build_lemma54_step,
  _build_n3_suspension_isomorphism_step,
  _build_pi4_2_step,
  _build_pi6_4_step,
  _build_prop51_step,
  _build_toda55_step,
  _build_toda56_step,
  build_toda_prop56_zero_argument_step,
)
from toda_stable_group_transport import (
  toda_45_generic_zero_group_transport_inference_rule,
)
from toda_rules import (
  Toda58EquationStatement,
  Toda58WhiteheadSquareUpToSignStatement,
  TodaDeltaImageUpToSignStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaSurjectiveStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaLemma54WhiteheadCorrectionDataStatement,
  TodaLemma57TwoIota5ImageMembershipStatement,
  TodaProp42ExactnessStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaSuspensionSurjectiveStatement,
  toda_510_eta5_nu6_bridge_inference_rule,
  toda_510_eta5_nu6_zero_inference_rule,
  toda_510_higher_eta_nu_zero_inference_rule,
  toda_54_indeterminacy_double_nu_prime_generator_inference_rule,
  toda_54_nu_prime_triple_eta_transport_inference_rule,
  toda_54_t_ge_1_indeterminacy_eta_cube_inference_rule,
  toda_57_nu_prime_eta6_hopf_inference_rule,
  toda_58_delta_iota9_nu4_nu_prime_inference_rule,
  toda_58_delta_iota9_whitehead_square_inference_rule,
  toda_58_integration_inference_rule,
  toda_58_literature_statements,
  toda_58_whitehead_square_nu_expression_inference_rule,
  toda_59_eta3_nu4_inference_rule,
  toda_hopf_injective_surjective_implies_isomorphism_inference_rule,
  toda_lemma45_n3_suspension_zero_reflection_inference_rule,
  toda_lemma57_e2_eta2_alpha_composition_inference_rule,
  toda_lemma57_e2_eta2_alpha_zero_inference_rule,
  toda_lemma57_nu_prime_hypothesis_inference_rule,
  toda_lemma57_pi6_2_eta2_nu_prime_inference_rule,
  toda_nu_family_definition_statement,
  toda_prop25_delta_eta9_composition_inference_rule,
  toda_prop31_nu6_eta9_zero_inference_rule,
  toda_prop51_eta4_twice_zero_inference_rule,
  toda_prop56_nu5_double_relation_inference_rule,
  toda_prop56_pi5_2_suspension_injective_inference_rule,
  toda_prop56_pi7_3_hopf_surjective_inference_rule,
  toda_prop56_pi7_5_delta_zero_inference_rule,
  toda_prop58_concrete_e_h_exactness_inference_rule,
  toda_prop58_delta_eta9_inference_rule,
  toda_prop58_e_nu4_eta7_bridge_inference_rule,
  toda_prop58_e_nu_prime_eta6_bridge_inference_rule,
  toda_prop58_eta6_nu7_zero_specialization_inference_rule,
  toda_prop58_finite_dimensional_integration_inference_rule,
  toda_prop58_finite_dimensional_literature_statements,
  toda_prop58_higher_nu_eta_zero_inference_rule,
  toda_prop58_pi10_6_concrete_exactness_inference_rule,
  toda_prop58_pi10_6_suspension_surjective_inference_rule,
  toda_prop58_pi10_6_zero_inference_rule,
  toda_prop58_pi7_3_finite_cyclic_inference_rule,
  toda_prop58_pi7_3_hopf_injective_inference_rule,
  toda_prop58_pi8_4_decomposition_inference_rule,
  toda_prop58_pi9_5_concrete_exactness_inference_rule,
  toda_prop58_pi9_5_finite_cyclic_inference_rule,
  toda_prop58_pi9_5_hopf_zero_inference_rule,
  toda_prop58_pi9_5_suspension_surjective_inference_rule,
  toda_prop58_pi9_9_delta_injective_inference_rule,
  toda_prop58_eta3_nu4_hopf_inference_rule,
  toda_eta_family_definition_statement,
)
from toda_upstream_bootstrap import (
  _build_phase50_result,
  build_toda_45_stable_isomorphism_step,
  build_toda_prop56_upstream_core,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def _build_support() -> dict[
  str,
  ProofStep,
]:
  core = (
    build_toda_prop56_upstream_core()
  )

  phase50 = _build_phase50_result()

  pi4_3_step = phase50[
    "final_group_step"
  ]

  pi4_2_step = _build_pi4_2_step(
    pi4_3_step,
    core[
      "toda52_step"
    ],
  )

  prop51_step = _build_prop51_step()

  n3_isomorphism_step = (
    _build_n3_suspension_isomorphism_step(
      prop51_step,
      core[
        "hopf_nu_prime_step"
      ],
    )
  )

  pi5_3_step = (
    build_phase59_pi5_3_step(
      pi4_2_step,
      n3_isomorphism_step,
    )
  )

  pi6_4_step = _build_pi6_4_step(
    pi5_3_step
  )

  (
    higher_transport_step,
    higher_range_step,
  ) = _build_higher_eta_transport(
    pi6_4_step
  )

  prop53_step = (
    build_phase59_prop53_step(
      pi4_2_step,
      pi5_3_step,
      pi6_4_step,
      higher_transport_step,
      higher_range_step,
    )
  )

  lemma54_step, pi6_5_step = (
    _build_lemma54_step(
      prop51_step,
      prop53_step,
      core[
        "hopf_nu_prime_step"
      ],
      core[
        "double_step"
      ],
      pi4_3_step,
    )
  )

  n = ScalarSymbol(
    name="n",
  )
  t = ScalarSymbol(
    name="t",
  )

  phase60_3_result = (
    run_inference_until_stable_with_history(
      (
        toda_54_t_ge_1_indeterminacy_eta_cube_inference_rule(),
        toda_54_nu_prime_triple_eta_transport_inference_rule(),
        toda_54_indeterminacy_double_nu_prime_generator_inference_rule(),
      ),
      (
        prop53_step,
        core[
          "double_step"
        ],
        create_legacy_given_proof_step(
          conclusion=ScalarGreaterEqualStatement(
            left=n,
            right=3,
          ),
          premises=(),
          rule=ProofRule.GIVEN,
        ),
        create_legacy_given_proof_step(
          conclusion=ScalarGreaterEqualStatement(
            left=t,
            right=1,
          ),
          premises=(),
          rule=ProofRule.GIVEN,
        ),
      ),
    )
  )

  triple_eta_step = _find_unique_step(
    phase60_3_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        Multiple,
      )
      and step.conclusion.lhs.coefficient
      == 2
      and isinstance(
        step.conclusion.lhs.expression,
        IteratedSuspension,
      )
    ),
    "triple eta transport",
  )

  toda55_step = _build_toda55_step(
    lemma54_step,
    triple_eta_step,
  )

  toda56_step = _build_toda56_step(
    lemma54_step
  )

  return {
    "prop56_step": (
      build_toda_prop56_zero_argument_step()
    ),
    "toda52_step": (
      core[
        "toda52_step"
      ]
    ),
    "hopf_nu_prime_step": (
      core[
        "hopf_nu_prime_step"
      ]
    ),
    "double_nu_prime_step": (
      core[
        "double_step"
      ]
    ),
    "prop51_step": prop51_step,
    "prop53_step": prop53_step,
    "lemma54_step": lemma54_step,
    "toda55_step": toda55_step,
    "toda56_step": toda56_step,
    "pi6_5_step": pi6_5_step,
    "pi4_3_step": pi4_3_step,
  }
```

```python
def _build_equation57_steps(
  support: dict[
    str,
    ProofStep,
  ],
) -> tuple[
  ProofStep,
  ProofStep,
]:
  eta5_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      5
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta6_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      6
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi_7_3 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=3,
  )
  pi_7_5 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=5,
  )
  pi_5_2 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=2,
  )
  pi_6_3 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )

  hopf_relation = (
    support[
      "hopf_nu_prime_step"
    ].conclusion
  )
  prop22_rule = (
    toda_prop22_right_inference_rule(
      alpha=(
        hopf_relation
        .lhs
        .expression
      ),
      gamma=hopf_relation.rhs,
    )
  )

  prop22_match = (
    find_inference_match(
      prop22_rule,
      (),
    )
  )

  if prop22_match is None:
    raise ValueError(
      "Toda Proposition 2.2 must be directly applicable"
    )

  prop22_step = (
    derive_inference_proof_step(
      prop22_match
    )
  )

  result = run_inference_until_stable_with_history(
    (
      toda_57_nu_prime_eta6_hopf_inference_rule(),
      toda_prop56_pi7_3_hopf_surjective_inference_rule(),
      toda_prop56_pi7_5_delta_zero_inference_rule(),
      toda_prop56_pi5_2_suspension_injective_inference_rule(),
    ),
    (
      support[
        "hopf_nu_prime_step"
      ],
      support[
        "prop53_step"
      ],
      eta5_definition_step,
      eta6_definition_step,
      prop22_step,
      create_legacy_given_proof_step(
        conclusion=TodaProp42ExactnessStatement(
          window=TodaEHPExactnessWindow(
            source_term=pi_7_3,
            middle_term=pi_7_5,
            target_term=pi_5_2,
            first_map=EHP_H_MAP,
            second_map=EHP_DELTA_MAP,
          ),
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=TodaProp42ExactnessStatement(
          window=TodaEHPExactnessWindow(
            source_term=pi_7_5,
            middle_term=pi_5_2,
            target_term=pi_6_3,
            first_map=EHP_DELTA_MAP,
            second_map=EHP_E_MAP,
          ),
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    ),
  )

  equation57_step = _find_unique_step(
    result.steps,
    lambda step: (
      step.inference_rule is not None
      and step.inference_rule.name
      == (
        "Toda Equation 5.7 "
        "nu-prime eta_6 Hopf value"
      )
    ),
    "Equation (5.7)",
  )

  hopf_surjective_step = (
    _find_unique_step(
      result.steps,
      lambda step: (
        isinstance(
          step.conclusion,
          TodaHopfInvariantSurjectiveStatement,
        )
        and step.conclusion.map.source_group
        == pi_7_3
      ),
      "pi_7^3 Hopf surjective",
    )
  )

  return (
    equation57_step,
    hopf_surjective_step,
  )
```

```python
def _build_eta2_nu_prime_zero_step(
  support: dict[
    str,
    ProofStep,
  ],
) -> ProofStep:
  nu5_definition_step = create_legacy_given_proof_step(
    conclusion=toda_nu_family_definition_statement(
      5
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )
  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  result = run_inference_until_stable_with_history(
    (
      toda_lemma57_nu_prime_hypothesis_inference_rule(),
      toda_prop51_eta4_twice_zero_inference_rule(),
      toda_lemma57_e2_eta2_alpha_composition_inference_rule(),
      toda_lemma57_e2_eta2_alpha_zero_inference_rule(),
      toda_lemma45_n3_suspension_zero_reflection_inference_rule(),
    ),
    (
      support[
        "prop51_step"
      ],
      support[
        "lemma54_step"
      ],
      nu5_definition_step,
    ),
  )

  expected = Relation(
    lhs=Suspension(
      expression=Composition(
        left=eta_2,
        right=nu_prime,
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected
    ),
    "E(eta_2 nu-prime)=0",
  )
```

```python
def _build_pi7_3_steps(
  support: dict[
    str,
    ProofStep,
  ],
  equation57_step: ProofStep,
  hopf_surjective_step: ProofStep,
  eta2_nu_prime_zero_step: ProofStep,
  pi6_2_step: ProofStep,
) -> tuple[
  ProofStep,
  ProofStep,
]:
  pi6_2 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=2,
  )
  pi7_3 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=3,
  )
  pi7_5 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=5,
  )

  window = TodaEHPExactnessWindow(
    source_term=pi6_2,
    middle_term=pi7_3,
    target_term=pi7_5,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop58_concrete_e_h_exactness_inference_rule(),
      toda_prop58_pi7_3_hopf_injective_inference_rule(),
      toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
      toda_prop58_pi7_3_finite_cyclic_inference_rule(),
    ),
    (
      equation57_step,
      hopf_surjective_step,
      support[
        "prop53_step"
      ],
      eta2_nu_prime_zero_step,
      pi6_2_step,
      create_legacy_given_proof_step(
        conclusion=window,
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    ),
  )

  hopf_map = TodaHopfInvariantMap(
    source_group=pi7_3,
    target_group=pi7_5,
  )

  hopf_isomorphism_step = (
    _find_unique_step(
      result.steps,
      lambda step: (
        isinstance(
          step.conclusion,
          TodaHopfInvariantIsomorphismStatement,
        )
        and step.conclusion.map
        == hopf_map
      ),
      "pi_7^3 Hopf isomorphism",
    )
  )

  final_step = _find_unique_step(
    result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi7_3
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 2
    ),
    "pi_7^3",
  )

  return (
    final_step,
    hopf_isomorphism_step,
  )
```

```python
def _build_pi9_5_step(
  support: dict[
    str,
    ProofStep,
  ],
  phase66_step: ProofStep,
  pi8_4_step: ProofStep,
  delta_eta9_step: ProofStep,
) -> ProofStep:
  pi10_9 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=9,
  )
  pi8_4 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=4,
  )
  pi9_5 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )
  pi9_9 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=9,
  )
  pi7_4 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=4,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop58_pi9_5_concrete_exactness_inference_rule(),
      toda_prop58_pi9_9_delta_injective_inference_rule(),
      toda_prop58_pi9_5_hopf_zero_inference_rule(),
      toda_prop58_pi9_5_suspension_surjective_inference_rule(),
      toda_prop58_e_nu4_eta7_bridge_inference_rule(),
      toda_prop58_pi9_5_finite_cyclic_inference_rule(),
    ),
    (
      support[
        "prop56_step"
      ],
      phase66_step,
      pi8_4_step,
      support[
        "prop51_step"
      ],
      delta_eta9_step,
      create_legacy_given_proof_step(
        conclusion=toda_nu_family_definition_statement(
          5
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=TodaEHPExactnessWindow(
          source_term=pi10_9,
          middle_term=pi8_4,
          target_term=pi9_5,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=TodaEHPExactnessWindow(
          source_term=pi8_4,
          middle_term=pi9_5,
          target_term=pi9_9,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=TodaEHPExactnessWindow(
          source_term=pi9_5,
          middle_term=pi9_9,
          target_term=pi7_4,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi9_5
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 2
    ),
    "pi_9^5",
  )
```

```python
def _build_double_nu5_step(
  toda55_step: ProofStep,
) -> ProofStep:
  nu5_definition_step = create_legacy_given_proof_step(
    conclusion=toda_nu_family_definition_statement(
      5
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable_with_history(
    toda_prop56_nu5_double_relation_inference_rule(),
    (
      toda55_step,
      nu5_definition_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        Multiple,
      )
      and step.conclusion.lhs.coefficient
      == 2
      and step.conclusion.lhs.expression
      == (
        nu5_definition_step
        .conclusion
        .element
      )
    ),
    "2 nu_5",
  )
```

```python
def _build_higher_eta_nu_zero_step(
  support: dict[
    str,
    ProofStep,
  ],
  pi9_5_step: ProofStep,
  toda59_step: ProofStep,
) -> ProofStep:
  toda55_step = support[
    "toda55_step"
  ]
  double_nu5_step = (
    _build_double_nu5_step(
      toda55_step
    )
  )

  n = (
    toda55_step
    .conclusion
    .nu_family_definition
    .index
  )

  result = run_inference_until_stable_with_history(
    (
      toda_510_eta5_nu6_bridge_inference_rule(),
      toda_510_eta5_nu6_zero_inference_rule(),
      toda_510_higher_eta_nu_zero_inference_rule(),
    ),
    (
      toda59_step,
      create_legacy_given_proof_step(
        conclusion=toda_nu_family_definition_statement(
          6
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      double_nu5_step,
      pi9_5_step,
      toda55_step,
      create_legacy_given_proof_step(
        conclusion=toda_eta_family_definition_statement(
          n
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      == RelationType.ZERO
      and isinstance(
        step.conclusion.lhs,
        Composition,
      )
      and getattr(
        step.conclusion.lhs.left,
        "name",
        None,
      )
      == "η_n"
    ),
    "higher eta_n nu_(n+1) zero",
  )
```

```python
def _build_nu6_eta9_zero_step(
  support: dict[
    str,
    ProofStep,
  ],
  higher_eta_nu_zero_step: ProofStep,
) -> ProofStep:
  toda55_step = support[
    "toda55_step"
  ]

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )
  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  n = (
    toda55_step
    .conclusion
    .nu_family_definition
    .index
  )

  result = run_inference_until_stable_with_history(
    (
      barratt_hilton_first_inference_rule(
        alpha=eta_2,
        beta=nu_4,
        p=2,
        q=4,
        k=1,
        h=3,
      ),
      barratt_hilton_second_inference_rule(
        alpha=eta_2,
        beta=nu_4,
        p=2,
        q=4,
        k=1,
        h=3,
      ),
      toda_prop58_eta6_nu7_zero_specialization_inference_rule(),
      toda_prop31_nu6_eta9_zero_inference_rule(),
      toda_prop58_higher_nu_eta_zero_inference_rule(),
    ),
    (
      toda55_step,
      higher_eta_nu_zero_step,
      create_legacy_given_proof_step(
        conclusion=toda_eta_family_definition_statement(
          6
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=toda_nu_family_definition_statement(
          7
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=HomotopyGroupMembershipStatement(
          element=eta_2,
          group_dimension=3,
          sphere_dimension=2,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=HomotopyGroupMembershipStatement(
          element=nu_4,
          group_dimension=7,
          sphere_dimension=4,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=ScalarGreaterEqualStatement(
          left=n,
          right=6,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    ),
  )

  nu_6 = (
    toda_nu_family_definition_statement(
      6
    ).element
  )
  eta_9 = (
    toda_eta_family_definition_statement(
      9
    ).element
  )

  expected = Relation(
    lhs=Composition(
      left=nu_6,
      right=eta_9,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected
    ),
    "nu_6 eta_9 zero",
  )
```

```python
def _build_higher_zero_steps(
  pi9_5_step: ProofStep,
  nu6_eta9_zero_step: ProofStep,
) -> tuple[
  ProofStep,
  ProofStep,
]:
  pi9_5 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )
  pi10_6 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=6,
  )
  pi10_11 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=11,
  )

  n = ScalarSymbol(
    name="n",
  )

  n_ge_6_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=6,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop58_pi10_6_concrete_exactness_inference_rule(),
      toda_prop58_pi10_6_suspension_surjective_inference_rule(),
      toda_prop58_pi10_6_zero_inference_rule(),
      toda_45_generic_zero_group_transport_inference_rule(),
    ),
    (
      pi9_5_step,
      nu6_eta9_zero_step,
      create_legacy_given_proof_step(
        conclusion=TodaEHPExactnessWindow(
          source_term=pi9_5,
          middle_term=pi10_6,
          target_term=pi10_11,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=TodaPrimaryGroupZeroStatement(
          group=pi10_11,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      build_toda_45_stable_isomorphism_step(
        n=6,
        k=4,
        m=n,
      ),
      n_ge_6_step,
    ),
  )

  expected = TodaPrimaryGroupZeroStatement(
    group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=4,
      ),
      sphere_dimension=n,
    )
  )

  final_step = _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected
    ),
    "higher four-stem zero",
  )

  return (
    final_step,
    n_ge_6_step,
  )
```

## toda_rules.py

### 変更後の import 全文

```python
from proof import LiteratureReference
from dataclasses import dataclass
from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  Expression,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  MapSymbol,
  Multiple,
  ScalarPower,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
  TodaBracket,
  WhiteheadProduct,
  Zero,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FiniteHomotopyGroupStatement,
  FreeCyclicGroup,
  HomotopyEHPExactnessWindow,
  HomotopyGroup,
  PrimaryComponent,
  PrimaryComponentMembershipStatement,
  StableHomotopyGroup,
  StablePrimaryComponent,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaPrimaryGroupZeroStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ExactnessStatement,
  InferenceRule,
  LiteratureReference,
  LiteratureStatement,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
  ScalarGreaterEqualStatement,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
)
```

### 変更クラス・関数全文

```python
def toda_bracket_membership_proof_step(
  statement,
):
  if not isinstance(
    statement,
    TodaBracketMembershipStatement,
  ):
    raise TypeError(
      "statement must be a "
      "TodaBracketMembershipStatement"
    )

  return create_legacy_given_proof_step(
    conclusion=statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )
```

```python
def toda_bracket_membership_theorem_proof_step(
  statement,
):
  if not isinstance(
    statement,
    TodaBracketMembershipTheoremStatement,
  ):
    raise TypeError(
      "statement must be a "
      "TodaBracketMembershipTheoremStatement"
    )

  return create_legacy_given_proof_step(
    conclusion=statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )
```

## toda_stable_eta_generator_normalization.py

### 変更後の import 全文

```python
from dataclasses import dataclass
from expression import IteratedSuspension, ScalarProduct, ScalarSum
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    run_inference_until_stable_with_history,
)
from toda_rules import (
    TodaEtaFamilyDefinitionStatement,
    toda_eta_family_definition_statement,
)
from toda_stable_concrete_transport_proof import (
    TodaStableConcreteTransportProof,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_toda_stable_eta_normalized_proof(
    transport_proof: TodaStableConcreteTransportProof,
) -> TodaStableEtaNormalizedProof:
    """Derive a named eta generator from a concrete 1-stem transport proof."""
    if not isinstance(transport_proof, TodaStableConcreteTransportProof):
        raise TypeError("transport_proof must be a TodaStableConcreteTransportProof")
    n = transport_proof.target.sphere_dimension
    if isinstance(n, bool) or not isinstance(n, int) or n <= 3:
        raise ValueError("only concrete transported eta-family targets are supported")
    if transport_proof.target.group_dimension != n + 1:
        raise ValueError("only the eta-family 1-stem is supported")
    base_definition = create_legacy_given_proof_step(
        conclusion=toda_eta_family_definition_statement(3),
        premises=(),
        rule=ProofRule.GIVEN,
    )
    target_definition = create_legacy_given_proof_step(
        conclusion=toda_eta_family_definition_statement(n),
        premises=(),
        rule=ProofRule.GIVEN,
    )
    rule = toda_eta_concrete_generator_normalization_inference_rule()
    result = run_inference_until_stable_with_history(
        rule,
        (transport_proof.transported_step, base_definition, target_definition),
    )
    matches = tuple(
        step for step in result.steps
        if step.inference_rule is rule
        and step.premises == (
            transport_proof.transported_step, base_definition, target_definition
        )
    )
    if len(matches) != 1:
        raise ValueError("eta normalization could not be derived from the supplied premises")
    return TodaStableEtaNormalizedProof(
        transport_proof=transport_proof,
        base_definition_step=base_definition,
        target_definition_step=target_definition,
        normalized_step=matches[0],
    )
```

## toda_stable_transport.py

### 変更後の import 全文

```python
from expression import (
  ScalarProduct,
  ScalarSum,
)
from homotopy_groups import (
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from stable_rules import (
  canonical_toda_stable_base,
  toda_primary_group_stem,
  toda_stable_transport_exponent,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_45_isomorphism_inference_rule,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_canonical_toda_45_isomorphism_step(
  target: TodaPrimaryGroup,
) -> ProofStep:
  stem = toda_primary_group_stem(
    target
  )
  base = canonical_toda_stable_base(
    target
  )
  transport_map = (
    build_canonical_toda_stable_transport_map(
      target
    )
  )

  base_sphere_dimension = (
    base.sphere_dimension
  )
  target_sphere_dimension = (
    target.sphere_dimension
  )

  stable_range_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=base_sphere_dimension,
      right=ScalarSum(
        left=stem,
        right=2,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_range_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=target_sphere_dimension,
      right=base_sphere_dimension,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_map_step = create_legacy_given_proof_step(
    conclusion=transport_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_45_isomorphism_inference_rule(),
      (
        stable_range_step,
        suspension_range_step,
        suspension_map_step,
      ),
    )
  )

  matches = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == Toda45IsomorphismStatement(
        map=transport_map,
      )
    )
  )

  if len(matches) != 1:
    raise ValueError(
      "expected exactly one canonical "
      "Toda (4.5) isomorphism step"
    )

  return matches[0]
```

## toda_upstream_bootstrap.py

### 変更後の import 全文

```python
from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
  TodaBracket,
  WhiteheadProduct,
  Zero,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
)
from low_dimensional_facts import (
  e_pi_1_1_to_pi_2_2_isomorphism_fact,
  pi_2_1_zero_fact,
  pi_3_3_free_cyclic_fact,
  pi_4_5_zero_fact,
  pi_5_5_free_cyclic_fact,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
  FoundationalReferenceIdentity,
)
from relation_rules import (
  equality_preserved_under_left_composition_inference_rule,
  equality_preserved_under_right_composition_inference_rule,
  equality_transitivity_inference_rule,
)
from toda_delta_image_rules import (
  free_cyclic_generator_delta_image_inference_rule,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  TodaBracketMembershipStatement,
  TodaDeltaImageUpToSignStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaPi32Eta2DefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaSuspensionInjectiveStatement,
  toda_45_isomorphism_inference_rule,
  toda_52_eta2_composition_isomorphism_inference_rule,
  toda_53_eta3_twice_zero_inference_rule,
  toda_53_eta4_suspension_bridge_inference_rule,
  toda_53_eta5_iterated_suspension_bridge_inference_rule,
  toda_53_nu_prime_bracket_specialization_inference_rule,
  toda_53_nu_prime_lemma52_double_inference_rule,
  toda_53_nu_prime_lemma52_hopf_inference_rule,
  toda_53_nu_prime_lemma52_membership_inference_rule,
  toda_eta_family_definition_statement,
  toda_eta3_suspension_relation_inference_rule,
  toda_exactness_injective_right_implies_delta_zero_inference_rule,
  toda_exactness_zero_delta_implies_hopf_surjective_inference_rule,
  toda_exactness_zero_left_implies_hopf_injective_inference_rule,
  toda_hopf_injective_surjective_implies_isomorphism_inference_rule,
  toda_pi3_2_define_eta2_inference_rule,
  toda_pi3_2_eta2_hopf_relation_inference_rule,
  toda_pi3_2_free_cyclic_generator_inference_rule,
  toda_pi3_2_whitehead_square_up_to_sign_inference_rule,
  toda_pi4_3_eta3_generator_inference_rule,
  toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule,
  toda_pi4_3_finite_cyclic_inference_rule,
  toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule,
  toda_pi_i_minus_1_1_zero_inference_rule,
  toda_prop27_iota2_whitehead_hopf_invariant_inference_rule,
  toda_prop44_eta2_n2_isomorphism_inference_rule,
  toda_prop44_eta2_second_summand_restriction_inference_rule,
  toda_suspension_isomorphism_implies_injective_inference_rule,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    create_legacy_specialization_proof_step,
    derive_inference_proof_step,
)
```

### 変更クラス・関数全文

```python
def build_toda_45_stable_isomorphism_step(
  n=5,
  k=3,
  m=None,
) -> ProofStep:
  if m is None:
    m = ScalarSymbol(
      name="n",
    )

  stable_range_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=ScalarSum(
        left=k,
        right=2,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_range_step = create_legacy_given_proof_step(
    conclusion=ScalarGreaterEqualStatement(
      left=m,
      right=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_map_step = create_legacy_given_proof_step(
    conclusion=TodaIteratedSuspensionMap(
      exponent=ScalarSum(
        left=m,
        right=ScalarProduct(
          left=-1,
          right=n,
        ),
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=k,
        ),
        sphere_dimension=n,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=m,
          right=k,
        ),
        sphere_dimension=m,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable_with_history(
    toda_45_isomorphism_inference_rule(),
    (
      stable_range_step,
      suspension_range_step,
      suspension_map_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda45IsomorphismStatement,
    ),
    "Toda (4.5) isomorphism",
  )
```

```python
def _build_phase49_result():
  pi_2_1 = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=1,
  )
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )
  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )
  pi_1_1 = TodaPrimaryGroup(
    group_dimension=1,
    sphere_dimension=1,
  )
  pi_2_2 = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=2,
  )

  premise_steps = (
    create_legacy_given_proof_step(
      conclusion=pi_2_1_zero_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
      inference_rule=InferenceRule(
        name=(
          "Toda (5.1) circle higher homotopy zero"
        ),
        literature_reference=LiteratureReference(
          label="Toda (5.1)",
          locator="(5.1)",
        ),
      ),
    ),
    create_legacy_given_proof_step(
      conclusion=pi_3_3_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
      inference_rule=InferenceRule(
        name=(
          "Toda (5.1) diagonal identity group"
        ),
        literature_reference=LiteratureReference(
          label="Toda (5.1)",
          locator="(5.1)",
        ),
      ),
    ),
    create_legacy_given_proof_step(
      conclusion=e_pi_1_1_to_pi_2_2_isomorphism_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
      inference_rule=InferenceRule(
        name=(
          "Toda (5.1) low-dimensional "
          "suspension isomorphism"
        ),
        literature_reference=LiteratureReference(
          label="Toda (5.1)",
          locator="(5.1)",
        ),
      ),
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_2_1,
          middle_term=pi_3_2,
          target_term=pi_3_3,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_3_2,
          middle_term=pi_3_3,
          target_term=pi_1_1,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_3_3,
          middle_term=pi_1_1,
          target_term=pi_2_2,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  rules = (
    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
    toda_suspension_isomorphism_implies_injective_inference_rule(),
    toda_exactness_injective_right_implies_delta_zero_inference_rule(),
    toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
    toda_pi3_2_define_eta2_inference_rule(),
    toda_pi3_2_eta2_hopf_relation_inference_rule(),
    toda_pi3_2_free_cyclic_generator_inference_rule(),
  )

  result = run_inference_until_stable_with_history(
    rules,
    premise_steps,
  )

  return {
    "premise_steps": premise_steps,
    "rules": rules,
    "result": result,
  }
```

```python
def _build_phase50_result():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )
  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )
  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )
  pi_4_5 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=5,
  )

  iota_2 = HomotopyElement(
    name="ι_2",
    dimension=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )
  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )
  iota_5 = HomotopyElement(
    name="ι_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="ι",
      index=5,
    ),
  )
  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )
  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  hopf_map = TodaHopfInvariantMap(
    source_group=pi_3_2,
    target_group=pi_3_3,
  )

  delta_map = TodaDeltaMap(
    source_group=pi_5_5,
    target_group=pi_3_2,
  )

  prop51_delta_step = create_legacy_specialization_proof_step(
    conclusion=(
      TodaDeltaImageUpToSignStatement(
        map=delta_map,
        element=iota_5,
        positive_value=Multiple(
          coefficient=2,
          expression=eta_2,
        ),
      )
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=(
        "Toda Proposition 5.1 "
        "Delta iota_5"
      ),
      description=(
        "Toda Proposition 5.1 gives "
        "Delta(iota_5)=+/-2 eta_2."
      ),
      literature_reference=(
        LiteratureReference(
          label="Toda Proposition 5.1",
          author="H. Toda",
          title=(
            "Composition Methods in "
            "Homotopy Groups of Spheres"
          ),
          year=1962,
          locator="Proposition 5.1",
        )
      ),
    ),
  )

  premise_steps = (
    create_legacy_given_proof_step(
      conclusion=WhiteheadProduct(
        left=iota_2,
        right=iota_2,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaPi32Eta2DefinitionStatement(
        map=hopf_map,
        element=eta_2,
        image=iota_3,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=eta_2,
        ),
        rhs=iota_3,
        relation_type=RelationType.EQUALITY,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaHopfInvariantInjectiveStatement(
        map=hopf_map,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=pi_5_5_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
      inference_rule=(
        _toda_fixed_reference_metadata_rule(
          'Toda (5.1) diagonal identity group',
          '(5.1)',
        )
      ),
    ),
    create_legacy_given_proof_step(
      conclusion=pi_4_5_zero_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
      inference_rule=(
        _toda_fixed_reference_metadata_rule(
          'Toda (5.1) sphere connectivity zero',
          '(5.1)',
        )
      ),
    ),
    create_legacy_given_proof_step(
      conclusion=delta_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    prop51_delta_step,
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_5_5,
          middle_term=pi_3_2,
          target_term=pi_4_3,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_3_2,
          middle_term=pi_4_3,
          target_term=pi_4_5,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    create_legacy_given_proof_step(
      conclusion=Relation(
        lhs=pi_3_2,
        rhs=FreeCyclicGroup(
          generator=eta_2,
        ),
        relation_type=RelationType.EQUALITY,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
      inference_rule=(
        _toda_fixed_reference_metadata_rule(
          'Toda Proposition 5.1 pi_3^2 group relation',
          'Proposition 5.1',
        )
      ),
    ),
    create_legacy_given_proof_step(
      conclusion=toda_eta_family_definition_statement(
        3
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  rules = (
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
    free_cyclic_generator_delta_image_inference_rule(),
    toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
    toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
    toda_pi4_3_finite_cyclic_inference_rule(),
    toda_eta3_suspension_relation_inference_rule(),
    toda_pi4_3_eta3_generator_inference_rule(),
  )

  result = run_inference_until_stable_with_history(
    rules,
    premise_steps,
  )

  final_group_step = _find_unique_step(
    result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi_4_3
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 2
      and step.conclusion.rhs.generator
      == eta_3
    ),
    "pi_4^3",
  )

  return {
    "result": result,
    "final_group_step": final_group_step,
  }
```

```python
def build_toda_52_composition_isomorphism_step() -> ProofStep:
  phase49 = _build_phase49_result()

  i = ScalarSymbol(
    name="i",
  )
  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )
  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )
  beta = HomotopyElement(
    name="β",
    dimension=i_minus_one,
  )
  gamma = HomotopyElement(
    name="γ",
    dimension=i,
    source=i,
    target=3,
  )

  first_summand = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=1,
  )
  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=3,
  )
  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=2,
  )

  decomposition_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(
        first_summand,
        second_summand,
      ),
    ),
    target_group=target_group,
    alpha=eta_2,
    beta=beta,
    gamma=gamma,
    formula=Sum(
      left=Suspension(
        expression=beta,
      ),
      right=Composition(
        left=eta_2,
        right=gamma,
      ),
    ),
  )

  premise_steps = (
    phase49[
      "premise_steps"
    ]
    + (
      create_legacy_given_proof_step(
        conclusion=ScalarGreaterEqualStatement(
          left=i,
          right=3,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=decomposition_map,
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    )
  )

  rules = (
    phase49[
      "rules"
    ]
    + (
      toda_pi_i_minus_1_1_zero_inference_rule(),
      toda_prop44_eta2_n2_isomorphism_inference_rule(),
      toda_prop44_eta2_second_summand_restriction_inference_rule(),
      toda_52_eta2_composition_isomorphism_inference_rule(),
    )
  )

  result = run_inference_until_stable_with_history(
    rules,
    premise_steps,
  )

  return _find_unique_step(
    result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda52CompositionIsomorphismStatement,
    ),
    "Toda (5.2) composition isomorphism",
  )
```

```python
def build_toda_53_nu_prime_steps() -> tuple[
  ProofStep,
  ProofStep,
  ProofStep,
]:
  phase50 = _build_phase50_result()

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )
  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )
  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )
  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  bracket_membership_step = create_legacy_specialization_proof_step(
    conclusion=TodaBracketMembershipStatement(
      element=nu_prime,
      bracket=TodaBracket(
        first=eta_3,
        second=Multiple(
          coefficient=2,
          expression=iota_4,
        ),
        third=eta_4,
        index=1,
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=(
        "Toda (5.3) nu-prime bracket definition"
      ),
      description=(
        "Record the fixed Toda (5.3) definition "
        "nu-prime in "
        "{eta_3, 2 iota_4, eta_4}_1."
      ),
      literature_reference=LiteratureReference(
        label="Toda (5.3)",
        author="H. Toda",
        title=(
          "Composition Methods in "
          "Homotopy Groups of Spheres"
        ),
        year=1962,
        locator="(5.3)",
      ),
    ),
  )

  specialization_result = (
    run_inference_until_stable_with_history(
      toda_53_nu_prime_bracket_specialization_inference_rule(),
      (
        bracket_membership_step,
      ),
    )
  )

  specialization_step = _find_unique_step(
    specialization_result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda53NuPrimeBracketSpecializationStatement,
    ),
    "nu-prime bracket specialization",
  )

  eta3_zero_result = (
    run_inference_until_stable_with_history(
      toda_53_eta3_twice_zero_inference_rule(),
      (
        phase50[
          "final_group_step"
        ],
      ),
    )
  )

  two_eta3_zero_step = _find_unique_step(
    eta3_zero_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=Multiple(
          coefficient=2,
          expression=eta_3,
        ),
        rhs=Zero(),
        relation_type=RelationType.ZERO,
      )
    ),
    "2 eta_3 zero",
  )

  raw_result = (
    run_inference_until_stable_with_history(
      (
        toda_53_nu_prime_lemma52_hopf_inference_rule(),
        toda_53_nu_prime_lemma52_double_inference_rule(),
        toda_53_nu_prime_lemma52_membership_inference_rule(),
      ),
      (
        specialization_step,
        two_eta3_zero_step,
      ),
    )
  )

  raw_hopf_step = _find_unique_step(
    raw_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=nu_prime,
        ),
        rhs=IteratedSuspension(
          expression=eta_3,
          exponent=2,
        ),
        relation_type=RelationType.EQUALITY,
      )
    ),
    "raw H(nu-prime)",
  )

  raw_double_step = _find_unique_step(
    raw_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=Multiple(
          coefficient=2,
          expression=nu_prime,
        ),
        rhs=Composition(
          left=eta_3,
          right=Composition(
            left=Suspension(
              expression=eta_3,
            ),
            right=eta_5,
          ),
        ),
        relation_type=RelationType.EQUALITY,
      )
    ),
    "raw 2 nu-prime",
  )

  membership_step = _find_unique_step(
    raw_result.steps,
    lambda step: (
      step.conclusion
      == HomotopyGroupMembershipStatement(
        element=nu_prime,
        group_dimension=6,
        sphere_dimension=3,
      )
    ),
    "nu-prime membership",
  )

  eta3_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      3
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )
  eta4_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      4
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )
  eta5_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      5
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta5_bridge_result = (
    run_inference_until_stable_with_history(
      toda_53_eta5_iterated_suspension_bridge_inference_rule(),
      (
        eta3_definition_step,
        eta5_definition_step,
      ),
    )
  )

  eta5_bridge_step = _find_unique_step(
    eta5_bridge_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=IteratedSuspension(
          expression=eta_3,
          exponent=2,
        ),
        rhs=eta_5,
        relation_type=RelationType.EQUALITY,
      )
    ),
    "eta_5 suspension bridge",
  )

  hopf_result = (
    run_inference_until_stable_with_history(
      equality_transitivity_inference_rule(),
      (
        raw_hopf_step,
        eta5_bridge_step,
      ),
    )
  )

  final_hopf_step = _find_unique_step(
    hopf_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=nu_prime,
        ),
        rhs=eta_5,
        relation_type=RelationType.EQUALITY,
      )
    ),
    "H(nu-prime)=eta_5",
  )

  eta4_bridge_result = (
    run_inference_until_stable_with_history(
      toda_53_eta4_suspension_bridge_inference_rule(),
      (
        eta3_definition_step,
        eta4_definition_step,
      ),
    )
  )

  eta4_bridge_step = _find_unique_step(
    eta4_bridge_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=Suspension(
          expression=eta_3,
        ),
        rhs=eta_4,
        relation_type=RelationType.EQUALITY,
      )
    ),
    "eta_4 suspension bridge",
  )

  right_rule = (
    equality_preserved_under_right_composition_inference_rule(
      eta_5,
    )
  )
  right_match = find_inference_match(
    right_rule,
    (
      eta4_bridge_step,
    ),
  )

  if right_match is None:
    raise ValueError(
      "eta_4 bridge right-composition did not match"
    )

  right_step = derive_inference_proof_step(
    right_match
  )

  left_rule = (
    equality_preserved_under_left_composition_inference_rule(
      eta_3,
    )
  )
  left_match = find_inference_match(
    left_rule,
    (
      right_step,
    ),
  )

  if left_match is None:
    raise ValueError(
      "eta_4 bridge left-composition did not match"
    )

  composition_step = derive_inference_proof_step(
    left_match
  )

  double_result = (
    run_inference_until_stable_with_history(
      equality_transitivity_inference_rule(),
      (
        raw_double_step,
        composition_step,
      ),
    )
  )

  final_double_step = _find_unique_step(
    double_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=Multiple(
          coefficient=2,
          expression=nu_prime,
        ),
        rhs=Composition(
          left=eta_3,
          right=Composition(
            left=eta_4,
            right=eta_5,
          ),
        ),
        relation_type=RelationType.EQUALITY,
      )
    ),
    "2 nu-prime",
  )

  return (
    membership_step,
    final_hopf_step,
    final_double_step,
  )
```
