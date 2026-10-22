# R3-10 変更対象

- `phase168_r3_3_proof_narrative_model.py`: import 全体と `build_proof_narrative_model()` 全体。クラス変更なし。
- `tests/test_phase168_r3_10_registered_alias.py`: 新規テスト全体。
- `tests/test_phase168_r3_9_citation_dedup.py`: 既存テストを同梱（変更なし）。
- `probe.py`: 診断全体。

モデル全体をそのまま置換できます。新規関数は作成していません。

## モデル全文
```python
"""Proof-tree-backed citation projection; no rendering or search decisions."""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult
from proof import LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import ProofStepLink, UnifiedStatementRegistry


@dataclass(frozen=True)
class NarrativeCitation:
    number: int
    reference: LiteratureReference
    step_indices: tuple[int, ...]
    assertion_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProofNarrativeModel:
    steps: tuple[ProofStep, ...]
    citations: tuple[NarrativeCitation, ...]
    step_citation_numbers: tuple[tuple[int, ...], ...]
    root_index: int | None


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
    # Locator is the printed source position. Labels are presentation metadata,
    # not independent source identities. Exact matching avoids conflating nearby
    # propositions or components with different locators.
    references: list[LiteratureReference] = []
    locators: list[str] = []
    associations: list[list[int]] = []
    assertion_ids: list[list[str]] = []
    per_step: list[tuple[int, ...]] = []

    for step_index, step in enumerate(steps):
        linked: list[tuple[LiteratureReference, str | None]] = []
        if registry is not None:
            for link in proof_links:
                if link.step is None or link.step != step:
                    continue
                assertion = registry.assertion(link.assertion_id)
                entry = registry.reference(assertion.reference_id)
                linked.append((LiteratureReference(
                    label=entry.locator, locator=entry.locator,
                ), assertion.assertion_id))

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

            if not any(same_source_heading(reference) for reference, _ in linked):
                located.append((rule_reference, None))

        numbers: list[int] = []
        for reference, assertion_id in located:
            locator = reference.locator or reference.label
            try:
                ref_index = locators.index(locator)
            except ValueError:
                ref_index = len(references)
                locators.append(locator)
                references.append(reference)
                associations.append([])
                assertion_ids.append([])
            number = ref_index + 1
            if step_index not in associations[ref_index]:
                associations[ref_index].append(step_index)
            if assertion_id is not None and assertion_id not in assertion_ids[ref_index]:
                assertion_ids[ref_index].append(assertion_id)
            if number not in numbers:
                numbers.append(number)
        per_step.append(tuple(numbers))

    citations = tuple(
        NarrativeCitation(
            number=i + 1,
            reference=reference,
            step_indices=tuple(associations[i]),
            assertion_ids=tuple(assertion_ids[i]),
        )
        for i, reference in enumerate(references)
    )
    return ProofNarrativeModel(
        steps=steps,
        citations=citations,
        step_citation_numbers=tuple(per_step),
        root_index=root_index,
    )

```

## 新規テスト全文
```python
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def _project(registered_locator: str, rule_locator: str, rule: ProofRule = ProofRule.GIVEN):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="source", kind=ReferenceKind.DEFINITION,
        locator=registered_locator,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="fact", reference_id="source",
        kind=AssertionKind.STATEMENT, content="x",
    ))
    step = ProofStep(
        conclusion="x", premises=(), rule=rule,
        inference_rule=InferenceRule(
            name="recorded rule", literature_reference=LiteratureReference(
                label="Toda " + rule_locator, locator=rule_locator,
            ),
        ),
    )
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(step,), conclusion="x",
    )
    return build_proof_narrative_model(
        result, registry=registry,
        proof_links=(ProofStepLink(assertion_id="fact", step=step),),
    )


def test_descriptive_heading_on_same_given_uses_registered_source():
    model = _project(
        "Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation",
        "Chapter V, i)",
    )
    assert len(model.citations) == 1
    assert model.citations[0].reference.locator == "Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation"
    assert model.citations[0].assertion_ids == ("fact",)
    assert model.step_citation_numbers == ((1,),)


def test_different_locator_same_given_remains_separate():
    model = _project("Proposition 5.1", "(5.1)")
    assert len(model.citations) == 2
    assert model.step_citation_numbers == ((1, 2),)


def test_numbered_subsection_is_not_a_description_alias():
    model = _project("Proposition 5.1 (iii)", "Proposition 5.1")
    assert len(model.citations) == 2


def test_derived_inference_keeps_both_provenances():
    model = _project("Chapter V, i) The Groups pi^(n)_(n+1)", "Chapter V, i)", ProofRule.INFERENCE)
    assert len(model.citations) == 2

```

## 実行プローブ全文
```python
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model


def main():
    for n, k in ((2, 1), (3, 1), (2, 2)):
        bridge = build_shared_typed_bridge()
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        model = build_linked_proof_narrative_model(result, bridge)
        locators = [c.reference.locator or c.reference.label for c in model.citations]
        print(f"PI_{n+k}^{n}: {locators}")
        assert len(locators) == len(set(locators))
        if (n, k) == (2, 1):
            assert len(locators) == 4
        if (n, k) == (3, 1):
            assert len(locators) == 4, locators
            assert sum(locator.startswith("Chapter V, i)") for locator in locators) == 1
        if (n, k) == (2, 2):
            assert locators == ["Proposition 5.1", "(5.2)"]
    print("R3-10 REGISTERED HEADING ALIAS: PASS")
    print("DEFAULT WEB ROUTE: UNCHANGED")


if __name__ == "__main__":
    main()

```

## 実行スクリプト全文
```powershell
$ErrorActionPreference = "Stop"
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $project "phase168_r3_3_proof_narrative_model.py"
if (-not (Test-Path $target)) { throw "Missing R3-3 model: $target" }
if (-not (Test-Path (Join-Path $project "phase168_r3_4_link_bridge.py"))) { throw "Missing R3-4 bridge adapter" }
$backup = Join-Path $package "backup"
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item $target (Join-Path $backup "phase168_r3_3_proof_narrative_model.py") -Force
Copy-Item (Join-Path $package "phase168_r3_3_proof_narrative_model.py") $target -Force
$env:PYTHONPATH = "$project;$package;$env:PYTHONPATH"
python -m pytest -q (Join-Path $package "tests/test_phase168_r3_9_citation_dedup.py") (Join-Path $package "tests/test_phase168_r3_10_registered_alias.py")
if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed" }
python (Join-Path $package "probe.py")
if ($LASTEXITCODE -ne 0) { throw "Real search probe failed" }
Write-Host "R3-10 installed; default renderer unchanged; full suite not run."

```
