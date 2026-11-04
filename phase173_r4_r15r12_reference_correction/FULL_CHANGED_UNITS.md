# R15R12 Complete changed units

All modified functions and their complete module imports appear below.

# phase168_r3_37c_reference_projection.py

## Complete imports and module prefix

```python
"""Common typed reference sentence projection. No source lookup."""
from phase168_r3_27_typed_statement_projection import typed_sentence
from web_group_proof_common import _group_proof_statement_latex
```

## Complete function: _verified_source_sentence

```python
def _verified_source_sentence(statement: object) -> str | None:
    """Render a fully source-screened typed statement without deducing a fact."""
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource

    if type(statement) is TodaLemma54TypedSource and statement == TodaLemma54TypedSource():
        return (
            r"$\nu_4\in\pi_7^4$, "
            r"$H(\nu_4)=\iota_7$ および "
            r"$2E\nu_4=E^2\nu'$."
        )
    return None
```

## Complete function: project_cited_proof_step_reference_bodies

```python
def project_cited_proof_step_reference_bodies(
    reference: object, cited_steps: tuple[object, ...],
) -> tuple[str, ...]:
    """Use an already cited GIVEN statement if registry links do not expose its body.

    The citation must already own the exact source step; simply finding a
    literature locator or a mathematically similar statement is insufficient.
    """
    from proof import LiteratureReference, ProofRule, ProofStep

    if not isinstance(reference, LiteratureReference) or not isinstance(cited_steps, tuple):
        return ()
    locator = reference.locator or reference.label
    candidates = tuple(
        (step, _verified_source_sentence(step.conclusion))
        for step in cited_steps
        if isinstance(step, ProofStep) and step.rule is ProofRule.GIVEN
        and not step.premises
    )
    verified = tuple(
        sentence for step, sentence in candidates
        if sentence is not None and locator == "Lemma 5.4"
    )
    return verified if len(verified) == 1 else ()
```

## Complete function: project_reference_bodies

```python
def project_reference_bodies(registry, assertion_ids):
    """Project only cited, typed source statements, including registered composite fields.

    Composite expansion follows the assertion's registered field scope. It does
    not read text from a literature catalog or create a new proof premise.
    """
    if registry is None:
        return ()
    from dataclasses import fields, is_dataclass
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase169_r10d2_general_family_definition.family_citation import (
        CitedStableFamilyDefinition, cited_family_reference_sentence,
    )
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement
    from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
    from toda_rules import Toda45IsomorphismStatement
    from expression import ScalarSymbol, ScalarSum, ScalarProduct
    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroupZeroStatement
    from proof import Relation

    result = []
    for assertion_id in assertion_ids:
        assertion = registry.assertion(assertion_id)
        content = assertion.content
        scope = getattr(assertion, "scope", ())
        statements = (content,)
        if (isinstance(scope, tuple) and len(scope) >= 2
                and scope[0] == "typed_composite_fields"):
            field_names = scope[1]
            if not isinstance(field_names, tuple) or len(field_names) < 2:
                raise ValueError("registered composite field scope is inconsistent")
            content_fields = (
                tuple(field.name for field in fields(content))
                if is_dataclass(content) and not isinstance(content, type) else ()
            )
            if content_fields == field_names:
                statements = tuple(getattr(content, field_name) for field_name in field_names)
            else:
                # The registered component bridge retains the parent's scope
                # on an atomic child. Validate the exact parent dependency and
                # field content instead of expanding this child a second time.
                dependencies = getattr(assertion, "dependencies", ())
                if not isinstance(dependencies, tuple) or len(dependencies) != 1:
                    raise ValueError("registered composite field scope is inconsistent")
                parent = registry.assertion(dependencies[0])
                parent_content = parent.content
                parent_fields = (
                    tuple(field.name for field in fields(parent_content))
                    if is_dataclass(parent_content) and not isinstance(parent_content, type)
                    else ()
                )
                if (parent.scope != scope
                        or parent_fields != field_names
                        or not any(
                            type(content) is type(getattr(parent_content, field_name))
                            and content == getattr(parent_content, field_name)
                            for field_name in field_names
                        )):
                    raise ValueError("registered composite field scope is inconsistent")

        for statement in statements:
            sentence = _verified_source_sentence(statement)
            if isinstance(statement, TodaEtaFamilyGeneralDefinition):
                if statement.lower_bound == 2:
                    sentence = r"$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する."
            elif isinstance(statement, CitedStableFamilyDefinition):
                sentence = cited_family_reference_sentence(statement)
            elif (isinstance(statement, TodaPrimaryGroupZeroStatement)
                  and isinstance(statement.group.group_dimension, ScalarSymbol)
                  and statement.group.sphere_dimension == 1):
                sentence = r"$\pi_i^1=0\quad(i>1)$."
            elif isinstance(statement, Toda51BelowDiagonalZeroStatement):
                sentence = r"$\pi_i^n=0\quad(i<n)$."
            elif (type(statement) is TodaProp44UniversalStatement
                  and statement == TodaProp44UniversalStatement()
                  and statement.preceding_hopf_fibration_dimensions == (2, 4, 8)):
                sentence = (
                    r"$\alpha\in\pi_{2n-1}^{n}$ で "
                    r"$H(\alpha)=\pm\iota_{2n-1}$ とする."
                    "\n"
                    r"このとき, 任意の $i$ に対して次の写像は同型である."
                    "\n"
                    r"$\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\;\cong\;}\pi_i^n,\quad"
                    r"(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma$."
                    "\n"
                    r"特に $E:\pi_{i-1}^{n-1}\to\pi_i^{n}$ は単射である."
                )
            elif isinstance(statement, TodaProp42GeneralExactnessStatement):
                sentence = (
                    r"$\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}"
                    r"\xrightarrow{H}\pi_{i+1}^{2n+1}"
                    r"\xrightarrow{\Delta}\pi_{i-1}^{n}"
                    r"\xrightarrow{E}\pi_i^{n+1}$ は完全."
                )
            elif isinstance(statement, Toda52UniversalStatement):
                if (statement.variable == "i" and statement.minimum_i == 3
                        and statement.map_formula == "alpha -> eta_2 o alpha"
                        and statement.source_group == "pi_i^3"
                        and statement.target_group == "pi_i^2"):
                    sentence = (
                        r"$i\ge 3$ に対し, "
                        r"$\eta_2\circ(-):\pi_i^3\xrightarrow{\cong}\pi_i^2$ は同型."
                    )
            elif isinstance(statement, Toda45IsomorphismStatement):
                mapping = statement.map
                n, m, k = ScalarSymbol("n"), ScalarSymbol("m"), ScalarSymbol("k")
                if (
                    isinstance(mapping, TodaIteratedSuspensionMap)
                    and mapping.exponent == ScalarSum(left=m, right=ScalarProduct(left=-1, right=n))
                    and mapping.source_group.sphere_dimension == n
                    and mapping.target_group.sphere_dimension == m
                    and mapping.source_group.group_dimension == ScalarSum(left=n, right=k)
                    and mapping.target_group.group_dimension == ScalarSum(left=m, right=k)
                ):
                    sentence = (
                        r"$n\ge k+2$, $m\ge n$, $k\ge0$ に対し, "
                        r"$E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}$ "
                        r"が成り立つ."
                    )
            elif isinstance(statement, Relation) and _is_generic_eta_group_relation(statement):
                # The typed source schema, already guarded by the general
                # eta-group recognizer, has the documented n >= 4 range.
                variable = statement.lhs.sphere_dimension.name
                sentence = (
                    r"$\pi_{" + variable + r"+1}^{" + variable + r"}="
                    r"\mathbb{Z}/2\{\eta_{" + variable + r"}\}"
                    r"\quad(" + variable + r"\ge4)$."
                )
            if sentence is None:
                sentence = typed_sentence(statement, None)
            if sentence is None:
                latex, fallback = _group_proof_statement_latex(statement)
                if latex is not None and fallback is None:
                    sentence = "$" + latex + "$."
            if (sentence is not None and r"\pi_{n}^{n}" in sentence
                    and r"\mathbb{Z}" in sentence and r"n\ge" not in sentence
                    and sentence.endswith("$.")):
                sentence = sentence[:-2] + r"\quad(n\ge 1)$."
            if sentence is not None and sentence not in result:
                result.append(sentence)
    return tuple(result)
```


# phase168_r3_3_proof_narrative_model.py

## Complete imports and module prefix

```python
"""Proof-tree-backed citation projection; no rendering or search decisions."""
from __future__ import annotations

from dataclasses import dataclass
from homotopy_groups import TodaPrimaryGroup

from phase165_r52_partial_proof import CertifiedAbstractStructure, PartialProofResult, ProofSearchStatus
from proof import LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import ProofStepLink, UnifiedStatementRegistry


@dataclass(frozen=True)
```

## Complete function: build_proof_narrative_model

```python
def build_proof_narrative_model(
    result: PartialProofResult,
    *,
    registry: UnifiedStatementRegistry | None = None,
    proof_links: tuple[ProofStepLink, ...] = (),
) -> ProofNarrativeModel:
    """Project only explicit proof-step and registered-link citations.

    Matching a link requires an exact ProofStep value; merely matching a
    conclusion or a display string is not sufficient. Root inference citations
    remain eligible. Neither a root conclusion nor an unused registry assertion
    becomes a premise through this projection.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if registry is not None and not isinstance(registry, UnifiedStatementRegistry):
        raise TypeError("registry must be UnifiedStatementRegistry or None")
    if not isinstance(proof_links, tuple) or not all(
        isinstance(link, ProofStepLink) for link in proof_links
    ):
        raise TypeError("proof_links must be a tuple of ProofStepLink")
    if proof_links and registry is None:
        raise ValueError("registry is required for proof_links")

    steps = result.proven_steps
    root_index = next(
        (i for i in range(len(steps) - 1, -1, -1)
         if result.conclusion is not None and steps[i].conclusion == result.conclusion),
        None,
    )
    # Complete proofs cite only the actual final-root ancestry. Preserve all
    # steps and the full (including unrelated) verified search record.
    citation_scope = (
        root_ancestor_step_indices(steps, root_index)
        if result.status is ProofSearchStatus.COMPLETE
        else frozenset(range(len(steps)))
    )
    # Locator is the printed source position. Labels are presentation metadata,
    # not independent source identities. Exact matching avoids conflating nearby
    # propositions or components with different locators.
    references: list[LiteratureReference] = []
    locators: list[str] = []
    associations: list[list[int]] = []
    assertion_ids: list[list[str]] = []
    reference_ids: list[list[str]] = []
    registry_index: dict[str, int] = {}
    per_step: list[tuple[int, ...]] = []

    for step_index, step in enumerate(steps):
        if step_index not in citation_scope:
            per_step.append(())
            continue
        linked: list[tuple[LiteratureReference, str | None, str | None]] = []
        if registry is not None:
            for link in proof_links:
                if link.step is None or link.step != step:
                    continue
                assertion = registry.assertion(link.assertion_id)
                entry = registry.reference(assertion.reference_id)
                linked.append((LiteratureReference(
                    label=entry.locator, locator=entry.locator,
                ), assertion.assertion_id, assertion.reference_id))

        located = list(linked)
        inference_rule = step.inference_rule
        if inference_rule is not None and inference_rule.literature_reference is not None:
            rule_reference = inference_rule.literature_reference
            rule_locator = rule_reference.locator or rule_reference.label
            # A registry heading may include a descriptive title following the
            # short printed heading attached to the very same GIVEN. Only that
            # heading/title shape is an alias; a numbered subsection or a
            # genuinely different locator remains a distinct citation.
            def same_source_heading(registered: LiteratureReference) -> bool:
                registered_locator = registered.locator or registered.label
                if registered_locator == rule_locator:
                    return True
                if step.rule is not ProofRule.GIVEN:
                    return False
                prefix = rule_locator + " "
                if not registered_locator.startswith(prefix):
                    return False
                suffix = registered_locator[len(prefix):]
                return suffix.startswith("The ") and len(suffix) > 4

            if not any(same_source_heading(reference) for reference, _, _ in linked):
                located.append((rule_reference, None, None))

        numbers: list[int] = []
        for reference, assertion_id, reference_id in located:
            locator = reference.locator or reference.label
            # The registered identity takes precedence over display labels.
            # Printed locator remains the compatibility fallback for independent
            # registry copies and inference rules without a registry entry.
            if reference_id is not None and reference_id in registry_index:
                ref_index = registry_index[reference_id]
            elif locator in locators:
                ref_index = locators.index(locator)
            else:
                ref_index = len(references)
                locators.append(locator)
                references.append(reference)
                associations.append([])
                assertion_ids.append([])
                reference_ids.append([])
            if reference_id is not None:
                registry_index[reference_id] = ref_index
                if reference_id not in reference_ids[ref_index]:
                    reference_ids[ref_index].append(reference_id)
                # Prefer the richer registered locator over an earlier
                # inference-only display entry for the same printed source.
                if references[ref_index].locator != locator:
                    references[ref_index] = reference
            number = ref_index + 1
            if step_index not in associations[ref_index]:
                associations[ref_index].append(step_index)
            if assertion_id is not None and assertion_id not in assertion_ids[ref_index]:
                assertion_ids[ref_index].append(assertion_id)
            if number not in numbers:
                numbers.append(number)
        per_step.append(tuple(numbers))

    from phase168_r3_37c_reference_projection import (
        project_reference_bodies, project_cited_proof_step_reference_bodies,
    )
    citations = tuple(
        NarrativeCitation(
            number=i + 1,
            reference=reference,
            step_indices=tuple(associations[i]),
            assertion_ids=tuple(assertion_ids[i]),
            reference_ids=tuple(reference_ids[i]),
            statement_bodies=(
                project_reference_bodies(registry, tuple(assertion_ids[i]))
                or project_cited_proof_step_reference_bodies(
                    reference, tuple(steps[j] for j in associations[i]),
                )
            ),
        )
        for i, reference in enumerate(references)
    )
    return ProofNarrativeModel(
        steps=steps,
        citations=citations,
        step_citation_numbers=tuple(per_step),
        root_index=root_index,
        status=result.status,
        target=result.target,
        open_goals=result.open_goals,
        diagnostics=result.diagnostics,
        abstract_structure=result.abstract_structure,
    )
```


# web_group_proof_common.py

## Complete imports and module prefix

```python
from dataclasses import dataclass
from toda_conclusion_latex_renderer import render_repository_conclusion_latex
from toda_human_readable_renderer import render_toda_public_group_relation_latex
from toda_proof_narrative_renderer import render_toda_proof_statement_latex

@dataclass(frozen=True)
```

## Complete function: _build_group_proof_inline_segments

```python
def _build_group_proof_inline_segments(
  line: str,
) -> tuple[
  WebGroupProofInlineSegmentView,
  ...,
]:
  if not isinstance(line, str):
    raise TypeError("line must be a str")

  segments = []
  cursor = 0
  while cursor < len(line):
    next_math = line.find("$", cursor)
    next_strong = line.find("**", cursor)
    delimiters = tuple(
      (position, kind)
      for position, kind in (
        (next_math, "inline_math"),
        (next_strong, "strong"),
      )
      if position >= 0
    )
    if not delimiters:
      segments.append(WebGroupProofInlineSegmentView(
        kind="text", value=line[cursor:]
      ))
      break

    position, kind = min(delimiters, key=lambda item: item[0])
    if position > cursor:
      segments.append(WebGroupProofInlineSegmentView(
        kind="text", value=line[cursor:position]
      ))

    if kind == "inline_math":
      closing = line.find("$", position + 1)
      if closing < 0:
        segments.append(WebGroupProofInlineSegmentView(
          kind="text", value=line[position:]
        ))
        break
      math_value = line[position + 1:closing]
      if not math_value:
        segments.append(WebGroupProofInlineSegmentView(
          kind="text", value="$$"
        ))
        cursor = closing + 1
        continue

      is_tagged = r"\tag{" in math_value
      cursor = closing + 1
      if is_tagged:
        # A tagged equation renders as a display block.  A standalone
        # punctuation suffix otherwise becomes an orphaned HTML text span.
        # Keep the punctuation with the equation, before its equation tag.
        suffix = line[cursor:]
        if suffix.strip() in (".", "。", ",", "、"):
          mark = "." if suffix.strip() in (".", "。") else ","
          tag_position = math_value.rfind(r"\tag{")
          math_value = (
            math_value[:tag_position]
            + r"\text{" + mark + "}"
            + math_value[tag_position:]
          )
          cursor = len(line)

      segments.append(WebGroupProofInlineSegmentView(
        kind="display_math" if is_tagged else "inline_math",
        value=math_value,
      ))
      continue

    closing = line.find("**", position + 2)
    if closing < 0:
      segments.append(WebGroupProofInlineSegmentView(
        kind="text", value=line[position:]
      ))
      break
    strong_value = line[position + 2:closing]
    chunks = strong_value.split("$")
    if (len(chunks) > 1 and len(chunks) % 2 == 1
        and all(chunks[i] for i in range(1, len(chunks), 2))):
      for i, chunk in enumerate(chunks):
        if chunk:
          segments.append(WebGroupProofInlineSegmentView(
            kind="inline_math" if i % 2 else "strong", value=chunk,
          ))
    else:
      segments.append(WebGroupProofInlineSegmentView(
        kind="strong" if strong_value else "text",
        value=strong_value if strong_value else "****",
      ))
    cursor = closing + 2

  return tuple(segments)
```


# phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py

## Complete imports and module prefix

```python
"""R4G: pre-Proposition 4.4 fibration is an explicitly verified Reference source."""
from __future__ import annotations

import re
from dataclasses import replace
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r27_r5_literature import (
    TodaProp44UniversalStatement,
    verify_prop44_hopf_fibration_source,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
```

## Complete function: pi64

```python
@pytest.fixture(scope="module")
def pi64():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert any(step.conclusion == result.conclusion for step in result.proven_steps)
    assert result.open_goals == ()
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    text = render_model_backed_narrative_markdown(result, model)
    assert "\n証明\n" in text
    reference, body = text.split("\n証明\n", 1)
    return result, model, reference, body
```

## Complete function: test_r4g_fibration_is_in_same_source_bound_reference

```python
def test_r4g_fibration_is_in_same_source_bound_reference(pi64):
    """Source prelude stays verified; Reference displays the proposition itself."""
    _, model, reference, body = pi64
    assert len(model.citations) == 5
    prop44 = [c for c in model.citations
              if (c.reference.locator or c.reference.label) == "Proposition 4.4"]
    assert len(prop44) == 1
    citation = prop44[0]
    assert len(citation.assertion_ids) == 1
    assert len(citation.statement_bodies) == 1
    text = citation.statement_bodies[0]
    assert "Proposition 4.4 直前の記述" not in text
    assert "Steenrod1951" not in text
    assert r"$\alpha\in\pi_{2n-1}^{n}$" in text
    assert r"$H(\alpha)=\pm\iota_{2n-1}$" in text
    assert r"\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}" in text
    assert r"\xrightarrow{\;\cong\;}" in text
    assert r"(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma" in text
    assert r"E:\pi_{i-1}^{n-1}\to\pi_i^{n}" in text
    assert text in reference
    assert f"[R{citation.number}]より" in body
    assert r"$h:S^7\to S^4$" in body
    assert "Lemma 5.4" not in reference + body
    assert body.rstrip().endswith("□")
```

## Complete function: test_r4g_web_and_pi53_existing_route_unchanged

```python
def test_r4g_web_and_pi53_existing_route_unchanged(pi64):
    _, model, reference, body = pi64
    all_numbers = {c.number for c in model.citations}
    reference_numbers = {int(x) for x in re.findall(r"\*\*\[R(\d+)\]", reference)}
    body_numbers = {int(x) for x in re.findall(r"\[R(\d+)\]", body)}
    assert all_numbers == reference_numbers == body_numbers == {1, 2, 3, 4, 5}
    view = build_standard_web_group_proof_view(4, 2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert len(view.steps) == len(pi64[0].proven_steps)
    lines = ["".join(s.value for s in line.segments) for line in view.rendered_lines]
    assert any(r"\xrightarrow{\;\cong\;}" in line for line in lines)
    assert not any("Proposition 4.4 直前" in line for line in lines)
    bridge = build_shared_typed_bridge()
    contexts = []
    previous = search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=contexts.append)
    assert previous.status is ProofSearchStatus.COMPLETE
    assert any(step.conclusion == previous.conclusion for step in previous.proven_steps)
    model53 = build_linked_proof_narrative_model(previous, contexts[0])
    markdown53 = render_model_backed_narrative_markdown(previous, model53)
    assert "Hopf fibration" not in markdown53
```


# phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py

## Complete imports and module prefix

```python
"""R4E: bibliography and body citations are owned by genuine ProofSteps."""
from __future__ import annotations

import re

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
```

## Complete function: pi64

```python
@pytest.fixture(scope="module")
def pi64():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert any(step.conclusion == result.conclusion for step in result.proven_steps)
    assert result.open_goals == ()
    assert len(contexts) == 1
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "\n証明\n" in markdown
    reference, body = markdown.split("\n証明\n", 1)
    return result, model, reference, body
```

## Complete function: test_r4e_standard_web_path_remains_verified_and_complete

```python
def test_r4e_standard_web_path_remains_verified_and_complete(pi64):
    view = build_standard_web_group_proof_view(4, 2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert len(view.steps) == len(pi64[0].proven_steps)
    assert len(view.rendered_lines) >= 20
    rendered = ["".join(segment.value for segment in line.segments)
                for line in view.rendered_lines]
    assert any("[R2]より" in text and "単射" in text for text in rendered)
    assert any("[R3]より" in text and "は完全" in text for text in rendered)
```


