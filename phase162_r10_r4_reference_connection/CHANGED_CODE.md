# R10-R4: full modified functions

## Modified files and functions
- toda_literature_statement_boundary.py: classify_toda_literature_statement_step
- toda_group_proof_narrative_references.py: extract_toda_group_proof_step_literature_reference, filter_toda_group_proof_narrative_reference_entries_by_body_usage
- New module: phase162_r10_reference_identity.py

## Imports
No top-level imports changed; all new imports are local to the full functions shown below.

## toda_literature_statement_boundary.py — classify_toda_literature_statement_step
```python
def classify_toda_literature_statement_step(
  proof_step: ProofStep,
) -> TodaLiteratureStatementBoundary | None:
  if not isinstance(proof_step, ProofStep):
    raise TypeError("proof_step must be a ProofStep")

  from proof import ProofRule
  from phase162_r10_reference_identity import fixed_citation_identity
  citation = fixed_citation_identity(proof_step)
  if citation is not None and proof_step.rule is ProofRule.INFERENCE:
    return TodaLiteratureStatementBoundary(
      classification=TodaLiteratureStatementClassification.FIXED_STATEMENT,
      reference_locator=citation[0],
      component_key=citation[1],
    )

  inference_rule = proof_step.inference_rule
  if inference_rule is None:
    return None

  rule_name = inference_rule.name
  fixed_locator = _REFERENCE_LOCATOR_BY_FIXED_RULE_NAME.get(
    rule_name
  )

  if fixed_locator is not None:
    return TodaLiteratureStatementBoundary(
      classification=(
        TodaLiteratureStatementClassification.FIXED_STATEMENT
      ),
      reference_locator=fixed_locator,
      component_key=_FIXED_RULE_COMPONENT_KEYS[
        rule_name
      ],
    )

  locator = _proof_step_reference_locator(
    proof_step
  )

  if locator not in _TRACKED_REFERENCE_LOCATORS:
    return None

  return TodaLiteratureStatementBoundary(
    classification=(
      TodaLiteratureStatementClassification.PROOF_INTERNAL
    ),
    reference_locator=locator,
    component_key=None,
  )
```

## toda_group_proof_narrative_references.py — extract_toda_group_proof_step_literature_reference
```python
def extract_toda_group_proof_step_literature_reference(
  proof_step: ProofStep,
) -> LiteratureReference | None:
  if not isinstance(proof_step, ProofStep):
    raise TypeError("proof_step must be a ProofStep")

  from phase162_r10_reference_identity import fixed_citation_identity
  citation = fixed_citation_identity(proof_step)
  if citation is not None:
    return LiteratureReference(
      label="Toda " + citation[0],
      locator=citation[0],
    )

  inference_rule = proof_step.inference_rule
  if inference_rule is None:
    return None

  boundary = classify_toda_literature_statement_step(
    proof_step
  )

  if (
    boundary is not None
    and boundary.classification
    == TodaLiteratureStatementClassification.FIXED_STATEMENT
  ):
    fixed_locator = boundary.reference_locator
    existing_reference = (
      inference_rule.literature_reference
    )

    if (
      existing_reference is not None
      and existing_reference.locator
      == fixed_locator
    ):
      return existing_reference

    if existing_reference is not None:
      return replace(
        existing_reference,
        label="Toda " + fixed_locator,
        locator=fixed_locator,
      )

    return LiteratureReference(
      label="Toda " + fixed_locator,
      locator=fixed_locator,
    )

  if inference_rule.literature_reference is not None:
    return inference_rule.literature_reference

  return _infer_toda_group_proof_literature_reference_from_rule_name(
    inference_rule.name
  )
```

## toda_group_proof_narrative_references.py — filter_toda_group_proof_narrative_reference_entries_by_body_usage
```python
def filter_toda_group_proof_narrative_reference_entries_by_body_usage(
  entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  body_markdown: str,
) -> tuple[
  tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  str,
]:
  if not isinstance(
    entries,
    tuple,
  ):
    raise TypeError(
      "entries must be a tuple"
    )

  if not all(
    isinstance(
      entry,
      TodaGroupProofNarrativeReferenceEntry,
    )
    for entry in entries
  ):
    raise TypeError(
      "entries must contain only "
      "TodaGroupProofNarrativeReferenceEntry objects"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  body_reference_numbers = tuple(
    int(
      match.group(
        1
      )
    )
    for match in re.finditer(
      r"\[R([0-9]+)\]",
      body_markdown,
    )
  )

  used_reference_numbers = set(
    body_reference_numbers
  )
  from phase162_r10_reference_identity import is_cited_inference
  for entry in entries:
    if any(is_cited_inference(step) for step in entry.proof_steps):
      used_reference_numbers.add(entry.number)

  used_entries = tuple(
    entry
    for entry in entries
    if entry.number in used_reference_numbers
  )

  number_map = {
    entry.number: new_number
    for new_number, entry in enumerate(
      used_entries,
      start=1,
    )
  }

  filtered_entries = tuple(
    replace(
      entry,
      number=number_map[
        entry.number
      ],
    )
    for entry in used_entries
  )

  filtered_statement_lines = {
    number_map[
      entry.number
    ]: statement_lines_by_reference_number[
      entry.number
    ]
    for entry in used_entries
    if entry.number in statement_lines_by_reference_number
  }

  def replace_marker(
    match,
  ):
    old_number = int(
      match.group(
        1
      )
    )
    new_number = number_map.get(
      old_number
    )

    if new_number is None:
      return match.group(
        0
      )

    return (
      "[R"
      + str(
        new_number
      )
      + "]"
    )

  filtered_body = re.sub(
    r"\[R([0-9]+)\]",
    replace_marker,
    body_markdown,
  )

  return (
    filtered_entries,
    filtered_statement_lines,
    filtered_body,
  )
```

## New complete module
```python
"""Recognize an R10 fixed-statement citation from recorded ProofStep structure.

An arbitrary foundational_reference is not sufficient: its registered component,
provenance shape, label, and citation rule must agree. This is a structural
reference classifier, not a replacement for external mathematical verification.
"""
from __future__ import annotations

from proof import ProofRule, ProofStep


def fixed_citation_identity(step: ProofStep) -> tuple[str, str] | None:
    if not isinstance(step, ProofStep):
        raise TypeError("step must be a ProofStep")
    identity = step.foundational_reference
    if identity is None or not isinstance(identity.key, str):
        return None
    if not identity.key.startswith("literature:"):
        return None
    payload = identity.key[len("literature:"):]
    locator, separator, component_key = payload.rpartition(":")
    if not separator or not locator or not component_key or identity.label != locator:
        return None
    from toda_literature_statement_boundary import get_toda_fixed_statement_component
    try:
        component = get_toda_fixed_statement_component(locator, component_key)
    except (KeyError, ValueError, TypeError):
        return None
    if component is None or component.reference_locator != locator or component.component_key != component_key:
        return None
    if step.rule is ProofRule.GIVEN:
        if step.premises or step.inference_rule is not None:
            return None
        return locator, component_key
    if step.rule is not ProofRule.INFERENCE or len(step.premises) != 1:
        return None
    premise = step.premises[0]
    if not isinstance(premise, ProofStep) or premise is step:
        return None
    if (premise.rule is not ProofRule.GIVEN or premise.premises
            or premise.inference_rule is not None
            or premise.foundational_reference != identity
            or premise.conclusion != step.conclusion):
        return None
    rule = step.inference_rule
    if (rule is None or rule.name != "phase162_verified_literature_citation"
            or rule.literature_reference is None
            or rule.literature_reference.locator != locator):
        return None
    return locator, component_key


def is_cited_inference(step: ProofStep) -> bool:
    return step.rule is ProofRule.INFERENCE and fixed_citation_identity(step) is not None
```
