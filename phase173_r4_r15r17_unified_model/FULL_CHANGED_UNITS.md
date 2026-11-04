# Phase 173 R15R17 — 完全な変更単位

この文書は、Source Guard 合格後のローカル実ファイルから生成した。
省略はなく、変更後の関数は全行を掲載する。

## 変更対象

- `phase168_r3_3_proof_narrative_model.py`: verified_narrative_steps, build_proof_narrative_model
- `phase168_r3_12_body_binding.py`: build_narrative_body_lines
- `web_group_proof_common.py`: _group_proof_statement_latex
- `phase173_r4_r15r9_shared_abstract_renderer/projection.py`: render_certified_abstract_model_section
- `phase165_r52_r3_web_adapter.py`: build_partial_web_group_proof_view

## Import 変更後の全文

### `phase168_r3_12_body_binding.py`

```python
"""Validated, proof-step-indexed narrative body projection.

This module never infers citations from mathematical text or rule names.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, verified_narrative_steps
from proof import ProofRule
from web_group_proof_common import _group_proof_statement_latex
```

## 変更後の関数全文

### `phase168_r3_3_proof_narrative_model.py` — `verified_narrative_steps`

```python
def verified_narrative_steps(result: PartialProofResult) -> tuple[ProofStep, ...]:
    """Join actual searched steps and a separately certified tree without inference.

    Search results remain immutable. A certified inference root contributes its
    actual guarded ancestry once, with original ProofStep identities retained.
    The returned sequence is presentation data, never a named proof result.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    existing = list(result.proven_steps)
    structure = result.abstract_structure
    if structure is None:
        return tuple(existing)
    if structure.group != result.target or result.status is ProofSearchStatus.COMPLETE:
        raise ValueError("incompatible abstract certificate for narrative")

    from phase173_r4_r15r16r3_staged_guard_fix.tree_adapter import (
        verified_tree_postorder,
    )
    for step in verified_tree_postorder(structure.proof_step):
        if not any(previous is step for previous in existing):
            existing.append(step)
    return tuple(existing)
```

### `phase168_r3_3_proof_narrative_model.py` — `build_proof_narrative_model`

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

    steps = verified_narrative_steps(result)
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

### `phase168_r3_12_body_binding.py` — `build_narrative_body_lines`

```python
def build_narrative_body_lines(
    result: PartialProofResult,
    model: ProofNarrativeModel,
) -> tuple[NarrativeBodyLine, ...]:
    """Bind renderable conclusions to their exact Proof Tree citation indices.

    Unrenderable conclusions are not replaced with guessed prose. Citation
    membership is validated in both directions; a malformed model fails closed.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if model.steps != verified_narrative_steps(result):
        raise ValueError("model steps must match the verified searched and certified trees")
    if len(model.step_citation_numbers) != len(model.steps):
        raise ValueError("step citation mapping has the wrong length")
    if result.status is ProofSearchStatus.COMPLETE and model.root_index is None:
        raise ValueError("complete result requires a root step")
    if model.root_index is not None and not 0 <= model.root_index < len(model.steps):
        raise ValueError("root step index is invalid")

    known = {citation.number: citation for citation in model.citations}
    if len(known) != len(model.citations) or set(known) != set(range(1, len(known) + 1)):
        raise ValueError("citation numbers must be unique and contiguous")
    for number, citation in known.items():
        for index in citation.step_indices:
            if not 0 <= index < len(model.steps):
                raise ValueError("citation refers to a nonexistent proof step")
            if number not in model.step_citation_numbers[index]:
                raise ValueError("citation and step map disagree")

    lines = []
    for index, step in enumerate(model.steps):
        numbers = model.step_citation_numbers[index]
        if len(set(numbers)) != len(numbers):
            raise ValueError("a proof step contains duplicate citation numbers")
        for number in numbers:
            if number not in known or index not in known[number].step_indices:
                raise ValueError("step cites a missing or unrelated source")
        latex, fallback_type = _group_proof_statement_latex(step.conclusion)
        if latex is None or fallback_type is not None:
            continue
        role = "given" if step.rule is ProofRule.GIVEN else (
            "root" if index == model.root_index else "inference"
        )
        lines.append(NarrativeBodyLine(index, latex, numbers, role))
    return tuple(lines)
```

### `web_group_proof_common.py` — `_group_proof_statement_latex`

```python
def _group_proof_statement_latex(
  statement,
) -> tuple[
  str | None,
  str | None,
]:
  from expression import Expression
  from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
  from phase165_r12_r2_quotient_rules import CyclicStructureStatement
  from proof import Relation, RelationType

  if (
    isinstance(statement, CyclicStructureStatement)
    and isinstance(statement.group, TodaPrimaryGroup)
    and isinstance(statement.generator, Expression)
    and (
      statement.order is None
      or (type(statement.order) is int and statement.order >= 1)
    )
  ):
    structure = (
      FreeCyclicGroup(statement.generator)
      if statement.order is None
      else FiniteCyclicGroup(statement.order, statement.generator)
    )
    try:
      cyclic_latex = render_toda_public_group_relation_latex(
        Relation(
          lhs=statement.group,
          rhs=structure,
          relation_type=RelationType.EQUALITY,
        )
      )
    except (TypeError, ValueError):
      cyclic_latex = None
    if cyclic_latex is not None:
      return cyclic_latex, None

  abstract_group = getattr(statement, "group", None)
  abstract_invariants = getattr(statement, "invariant_summands", None)
  if (isinstance(abstract_group, TodaPrimaryGroup)
      and type(abstract_group.group_dimension) is int
      and type(abstract_group.sphere_dimension) is int
      and isinstance(abstract_invariants, tuple)):
    # A typed, already verified abstract invariant has no named generator.
    # This is a generic statement formatter, not an inference or Narrative.
    from phase173_r4_r15r9_shared_abstract_renderer.projection import (
      abstract_invariants_latex,
    )
    invariant_latex = abstract_invariants_latex(abstract_invariants)
    return (
      rf"\pi_{{{abstract_group.group_dimension}}}^{{{abstract_group.sphere_dimension}}}"
      rf" \cong {invariant_latex}",
      None,
    )

  public_group_latex = (
    render_toda_public_group_relation_latex(
      statement
    )
  )

  if public_group_latex is not None:
    return (
      public_group_latex,
      None,
    )

  try:
    latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    latex = (
      render_toda_proof_statement_latex(
        statement
      )
    )

  if latex is None:
    return (
      None,
      type(
        statement
      ).__name__,
    )

  return (
    latex,
    None,
  )
```

### `phase173_r4_r15r9_shared_abstract_renderer/projection.py` — `render_certified_abstract_model_section`

```python
def render_certified_abstract_model_section(model: object) -> str:
    """Render only certificate evidence explicitly carried by ProofNarrativeModel."""
    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel

    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("expected canonical ProofNarrativeModel")
    structure = model.abstract_structure
    if structure is None:
        return ""
    if (
        not isinstance(structure, CertifiedAbstractStructure)
        or structure.group != model.target
        or model.status not in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        or model.root_index is not None
    ):
        raise ValueError("unverified Model abstract result cannot be presented")
    # The certified root is already a normal ProofStep in the unified Model.
    # Do not render the same tree a second time as a separate appendix.
    if any(step is structure.proof_step for step in model.steps):
        return ""
    return _render_abstract_claim(model.target, structure)
```

### `phase165_r52_r3_web_adapter.py` — `build_partial_web_group_proof_view`

```python
def build_partial_web_group_proof_view(
    result: PartialProofResult,
    *,
    max_depth: int = 2,
    mode: str = "narrative",
    narrative_model: ProofNarrativeModel | None = None,
) -> WebGroupProofView:
    """Adapt searched steps; render a supplied proof model without rewriting it."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an int")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")
    if narrative_model is not None and not isinstance(narrative_model, ProofNarrativeModel):
        raise TypeError("narrative_model must be ProofNarrativeModel or None")

    n = result.target.sphere_dimension
    dimension = result.target.group_dimension
    k = dimension - n
    target_latex = rf"\pi_{{{dimension}}}^{{{n}}}"
    if result.status is ProofSearchStatus.COMPLETE:
        target_statement = result.conclusion
    else:
        target_statement = next(
            (
                item for item in reversed(result.open_goals)
                if getattr(item, "lhs", None) == result.target
                or getattr(item, "group", None) == result.target
            ),
            None,
        )
    if target_statement is not None:
        statement_latex, fallback_type = _group_proof_statement_latex(target_statement)
        if statement_latex is not None and fallback_type is None:
            target_latex = statement_latex

    steps = []
    display_steps = (
        narrative_model.steps
        if narrative_model is not None and mode != "trace"
        else result.proven_steps
    )
    for step in display_steps:
        statement_latex, fallback_type_name = _group_proof_statement_latex(step.conclusion)
        steps.append(WebGroupProofStepView(
            depth=0,
            statement_latex=statement_latex,
            fallback_type_name=fallback_type_name,
            rule_name=_group_proof_rule_name(step),
            role_name="derived",
        ))

    if mode == "trace":
        rendered_lines = ()
    else:
        if narrative_model is None:
            # Preserve the existing legacy/compatibility narrative route.
            markdown = render_partial_proof_markdown(result)
            from phase173_r4_r15r9_shared_abstract_renderer.projection import (
                render_certified_abstract_section,
            )
            abstract_markdown = render_certified_abstract_section(result)
            if abstract_markdown:
                markdown = markdown.rstrip() + "\n\n" + abstract_markdown + "\n"
        else:
            from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
            markdown = render_model_backed_narrative_markdown(result, narrative_model)
        rendered_lines = _build_group_proof_rendered_lines(markdown)

    return WebGroupProofView(
        n=n,
        k=k,
        conclusion_latex=target_latex,
        theorem=None,
        phase="165 R52-R3",
        key=("generic-complete-proof" if result.status is ProofSearchStatus.COMPLETE else "generic-partial-proof"),
        steps=tuple(steps),
        max_depth=max_depth,
        mode=mode,
        rendered_lines=rendered_lines,
        partial_result=(result.status is not ProofSearchStatus.COMPLETE),
        abstract_structure_certified=(result.abstract_structure is not None),
    )
```

## 新規テストファイルの全文

### `tests/test_unified_web.py`

```python
"""Phase 173 R15R17: one certified Model, one Reference and one Renderer."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_12_body_binding import build_narrative_body_lines
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r16r3_staged_guard_fix.tree_adapter import verified_tree_postorder
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _group_proof_statement_latex


@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_verified_abstract_root_is_inside_one_canonical_model(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    structure = result.abstract_structure
    assert structure is not None
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    model = build_proof_narrative_model(result)
    evidence = verified_tree_postorder(structure.proof_step)
    assert all(any(step is item for item in model.steps) for step in evidence)
    assert model.steps[-1] is structure.proof_step
    assert model.root_index is None
    assert model.status is result.status
    assert model.open_goals == result.open_goals
    assert model.diagnostics == result.diagnostics
    assert len(model.citations) >= 4
    assert len(build_narrative_body_lines(result, model)) >= 1
    latex, fallback = _group_proof_statement_latex(structure.proof_step.conclusion)
    assert fallback is None and latex is not None
    assert r"\cong" in latex
    markdown = render_model_backed_narrative_markdown(result, model)
    assert markdown.count("## 使用する結果") == 1
    assert "Proposition 4.4" in markdown
    assert "Lemma 5.4" in markdown
    assert "DB prior: sphere.csv" in markdown
    assert r"\cong" in markdown
    assert "### 検証済み証明木の Reference" not in markdown
    assert "## 証明済みの抽象群構造" not in markdown
    assert "参照情報を持つ ProofStep はありません" not in markdown
    assert markdown.count("## 未解決 Goal") == 1


@pytest.mark.parametrize("k", (8, 31))
def test_public_web_uses_one_reference_and_preserves_named_open_goals(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-partial-proof"
    assert view.partial_result
    assert view.abstract_structure_certified
    assert len(view.steps) >= 4
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("未解決 Goal") == 1
    assert "検証済み証明木の Reference" not in headings
    assert "証明済みの抽象群構造" not in headings
    joined = "\n".join(segment.value for line in view.rendered_lines
                       for segment in line.segments)
    assert "Proposition 4.4" in joined
    assert "Lemma 5.4" in joined
    assert "、" not in joined and "。" not in joined


def test_uncertified_failed_search_does_not_gain_proof_steps() -> None:
    result = search_group_from_registered_goal(n=5, k=3)
    assert result.abstract_structure is None
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    assert model.status is ProofSearchStatus.SEARCH_FAILED
    assert model.open_goals
    view = build_standard_web_group_proof_view(n=5, k=3, mode="narrative")
    assert view.partial_result
    assert not view.abstract_structure_certified
    assert not any("Proposition 4.4" in segment.value
                   for line in view.rendered_lines for segment in line.segments)


def test_completed_group_keeps_original_model_and_citations() -> None:
    result = search_group_from_registered_goal(n=4, k=4)
    model = build_proof_narrative_model(result)
    assert result.status is ProofSearchStatus.COMPLETE
    assert model.steps == result.proven_steps
    assert model.root_index is not None
    assert model.abstract_structure is None
    view = build_standard_web_group_proof_view(n=4, k=4, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert not view.abstract_structure_certified
    assert any("[R" in segment.value
               for line in view.rendered_lines for segment in line.segments)


def test_tampered_unified_model_fails_closed() -> None:
    goal = exact_prior_database_result(4, 8)
    result = search_group_from_registered_goal(n=4, k=8, goal=goal)
    model = build_proof_narrative_model(result)
    with pytest.raises(ValueError, match="verified searched and certified trees"):
        build_narrative_body_lines(result, replace(model, steps=result.proven_steps))


def test_public_route_renders_one_narrative_only(monkeypatch) -> None:
    import phase168_r3_5_model_renderer as renderer
    import phase173_r4_r15r16r3_staged_guard_fix.tree_adapter as separate

    invocations = []
    original = renderer.render_model_backed_narrative_markdown

    def recorded(result, model):
        invocations.append(model)
        return original(result, model)

    def forbidden_secondary_render(target, root):
        raise AssertionError("a second verified-tree Narrative is forbidden")

    monkeypatch.setattr(renderer, "render_model_backed_narrative_markdown", recorded)
    monkeypatch.setattr(separate, "render_verified_tree_progress", forbidden_secondary_render)
    view = build_standard_web_group_proof_view(
        n=4, k=8, mode="narrative", citation_source="model",
    )
    assert view.partial_result
    assert len(invocations) == 1
    assert invocations[0].abstract_structure is not None

```

### `tests/test_patch_contract.py`

```python
"""Stand-alone review of fail-closed source rewrites."""
from __future__ import annotations

import ast

import pytest

from phase173_r4_r15r17_unified_model.patches import (
    EXPECTED_BLOBS,
    MODEL,
    NEW_STEPS_HELPER,
    replace_once,
)


def test_source_guard_has_all_five_explicit_production_blobs() -> None:
    assert len(EXPECTED_BLOBS) == 5
    assert MODEL in EXPECTED_BLOBS
    assert all(len(blob) == 40 for blob in EXPECTED_BLOBS.values())


def test_repeated_or_missing_anchor_is_rejected() -> None:
    assert replace_once("A\n", "A\n", "B\n", "fixture") == "B\n"
    with pytest.raises(RuntimeError, match="unreviewed or already patched"):
        replace_once("B\n", "A\n", "B\n", "fixture")
    with pytest.raises(RuntimeError, match="unreviewed or already patched"):
        replace_once("A\nA\n", "A\n", "B\n", "fixture")


def test_new_step_merger_has_no_dimension_or_named_generator_cases() -> None:
    tree = ast.parse(NEW_STEPS_HELPER)
    assert any(isinstance(node, ast.FunctionDef)
               and node.name == "verified_narrative_steps" for node in tree.body)
    assert "verified_tree_postorder" in NEW_STEPS_HELPER
    assert "result.proven_steps" in NEW_STEPS_HELPER
    assert "result.abstract_structure" in NEW_STEPS_HELPER
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            assert "\\nu" not in node.value
            assert "\\varepsilon" not in node.value

```
