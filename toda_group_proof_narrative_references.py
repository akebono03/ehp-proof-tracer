from dataclasses import (
  dataclass,
  replace,
)
import re

from proof import (
  LiteratureReference,
  ProofStep,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_component,
  get_toda_fixed_statement_components,
  is_toda_fixed_statement_component_reference_eligible,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_dependency import (
  TodaProofEdge,
)


@dataclass(frozen=True)
class TodaGroupProofNarrativeReferenceEntry:
  number: int
  reference: LiteratureReference
  proof_steps: tuple[ProofStep, ...]

  def __post_init__(self) -> None:
    if isinstance(self.number, bool) or not isinstance(self.number, int):
      raise TypeError("number must be an int")
    if self.number <= 0:
      raise ValueError("number must be positive")
    if not isinstance(self.reference, LiteratureReference):
      raise TypeError("reference must be a LiteratureReference")
    if not isinstance(self.proof_steps, tuple):
      raise TypeError("proof_steps must be a tuple")
    if not self.proof_steps:
      raise ValueError("proof_steps must not be empty")
    if not all(isinstance(step, ProofStep) for step in self.proof_steps):
      raise TypeError("proof_steps must contain only ProofStep objects")


def _infer_toda_group_proof_literature_reference_from_rule_name(
  rule_name: str,
) -> LiteratureReference | None:
  if not isinstance(rule_name, str):
    raise TypeError("rule_name must be a str")

  normalized_rule_name = rule_name.lower()

  if "bridge" in normalized_rule_name:
    return None

  named_match = re.match(
    r"^Toda (Proposition|Lemma|Theorem|Equation) ([0-9]+(?:\.[0-9]+)*)\b",
    rule_name,
  )
  if named_match is not None:
    kind, number = named_match.groups()
    locator = f"{kind} {number}"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  parenthesized_match = re.match(
    r"^Toda \(([0-9]+(?:\.[0-9]+)*)\)\b",
    rule_name,
  )
  if parenthesized_match is not None:
    number = parenthesized_match.group(1)
    locator = f"({number})"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  bare_equation_match = re.match(
    r"^Toda ([0-9]+\.[0-9]+)\b",
    rule_name,
  )
  if bare_equation_match is not None:
    number = bare_equation_match.group(1)
    locator = f"({number})"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  return None


def extract_toda_group_proof_step_literature_reference(
  proof_step: ProofStep,
) -> LiteratureReference | None:
  if not isinstance(proof_step, ProofStep):
    raise TypeError("proof_step must be a ProofStep")

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

def _same_toda_group_proof_literature_reference(
  left: LiteratureReference | None,
  right: LiteratureReference | None,
) -> bool:
  if left is None or right is None:
    return left is right

  if (
    left.locator is not None
    and right.locator is not None
  ):
    return left.locator == right.locator

  return left == right








def build_toda_group_proof_narrative_reference_entries(
  presentation: TodaGroupProofPresentation,
) -> tuple[TodaGroupProofNarrativeReferenceEntry, ...]:
  if not isinstance(presentation, TodaGroupProofPresentation):
    raise TypeError("presentation must be a TodaGroupProofPresentation")

  references = []
  steps_by_reference = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    reference = extract_toda_group_proof_step_literature_reference(
      proof_step
    )
    if reference is None:
      continue

    try:
      index = references.index(reference)
    except ValueError:
      references.append(reference)
      steps_by_reference.append([proof_step])
    else:
      steps_by_reference[index].append(proof_step)

  return tuple(
    TodaGroupProofNarrativeReferenceEntry(
      number=number,
      reference=reference,
      proof_steps=tuple(proof_steps),
    )
    for number, (reference, proof_steps) in enumerate(
      zip(references, steps_by_reference),
      start=1,
    )
  )


def exclude_toda_group_proof_narrative_root_reference(
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
  root_step: ProofStep,
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
]:
  if not isinstance(entries, tuple):
    raise TypeError("entries must be a tuple")

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
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  root_reference = (
    extract_toda_group_proof_step_literature_reference(
      root_step
    )
  )

  if root_reference is None:
    return (
      entries,
      statement_lines_by_reference_number,
    )

  root_boundary = (
    classify_toda_literature_statement_step(
      root_step
    )
  )

  retained_entries = []

  for entry in entries:
    if not _same_toda_group_proof_literature_reference(
      entry.reference,
      root_reference,
    ):
      retained_entries.append(
        entry
      )
      continue

    if (
      root_boundary is None
      or root_boundary.classification
      is not TodaLiteratureStatementClassification.FIXED_STATEMENT
      or root_boundary.component_key is None
    ):
      continue

    eligible_steps = []

    for proof_step in entry.proof_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is None
        or boundary.classification
        is not TodaLiteratureStatementClassification.FIXED_STATEMENT
        or boundary.reference_locator
        != root_boundary.reference_locator
        or boundary.component_key is None
      ):
        continue

      component = get_toda_fixed_statement_component(
        boundary.reference_locator,
        boundary.component_key,
      )

      if not (
        is_toda_fixed_statement_component_reference_eligible(
          component,
          root_boundary.reference_locator,
          root_boundary.component_key,
        )
      ):
        continue

      eligible_steps.append(
        proof_step
      )

    if eligible_steps:
      retained_entries.append(
        replace(
          entry,
          proof_steps=tuple(
            eligible_steps
          ),
        )
      )

  retained_entries = tuple(
    retained_entries
  )

  number_map = {
    entry.number: new_number
    for new_number, entry in enumerate(
      retained_entries,
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
    for entry in retained_entries
  )

  filtered_statement_lines = {
    number_map[
      entry.number
    ]: statement_lines_by_reference_number[
      entry.number
    ]
    for entry in retained_entries
    if entry.number
    in statement_lines_by_reference_number
  }

  return (
    filtered_entries,
    filtered_statement_lines,
  )


def select_toda_group_proof_narrative_reference_statement_steps(
  entry: TodaGroupProofNarrativeReferenceEntry,
  candidate_steps: tuple[ProofStep, ...],
  proof_edges: tuple[TodaProofEdge, ...],
  root_step: ProofStep | None = None,
) -> tuple[ProofStep, ...]:
  if not isinstance(
    entry,
    TodaGroupProofNarrativeReferenceEntry,
  ):
    raise TypeError(
      "entry must be a "
      "TodaGroupProofNarrativeReferenceEntry"
    )

  if not isinstance(
    candidate_steps,
    tuple,
  ):
    raise TypeError(
      "candidate_steps must be a tuple"
    )

  if not all(
    isinstance(
      step,
      ProofStep,
    )
    for step in candidate_steps
  ):
    raise TypeError(
      "candidate_steps must contain only "
      "ProofStep objects"
    )

  if (
    root_step is not None
    and not isinstance(
      root_step,
      ProofStep,
    )
  ):
    raise TypeError(
      "root_step must be a ProofStep or None"
    )

  entry_step_ids = {
    id(
      step
    )
    for step in entry.proof_steps
  }
  seen_candidate_step_ids = set()

  for step in candidate_steps:
    step_id = id(
      step
    )

    if step_id not in entry_step_ids:
      raise ValueError(
        "candidate_steps must contain only "
        "steps from entry.proof_steps"
      )

    if step_id in seen_candidate_step_ids:
      raise ValueError(
        "candidate_steps must not contain "
        "the same ProofStep more than once"
      )

    seen_candidate_step_ids.add(
      step_id
    )

  if not isinstance(
    proof_edges,
    tuple,
  ):
    raise TypeError(
      "proof_edges must be a tuple"
    )

  if not all(
    isinstance(
      edge,
      TodaProofEdge,
    )
    for edge in proof_edges
  ):
    raise TypeError(
      "proof_edges must contain only "
      "TodaProofEdge objects"
    )

  eligible_candidates = tuple(
    step
    for step in candidate_steps
    if step is not root_step
  )

  if not eligible_candidates:
    return ()

  boundary_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in proof_edges
    if (
      edge.premise_step
      is not root_step
      and extract_toda_group_proof_step_literature_reference(
        edge.premise_step
      )
      == entry.reference
      and extract_toda_group_proof_step_literature_reference(
        edge.parent_step
      )
      != entry.reference
    )
  }

  entry_external_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in proof_edges
    if id(
      edge.parent_step
    ) not in entry_step_ids
  }

  used_candidate_step_ids = (
    boundary_used_step_ids
    | entry_external_used_step_ids
  )

  used_candidate_conclusions = tuple(
    edge.premise_step.conclusion
    for edge in proof_edges
    if id(
      edge.premise_step
    ) in used_candidate_step_ids
  )

  used_candidates = tuple(
    step
    for step in eligible_candidates
    if (
      id(
        step
      ) in used_candidate_step_ids
      or any(
        step.conclusion == used_conclusion
        for used_conclusion in used_candidate_conclusions
      )
    )
  )

  if used_candidates:
    return used_candidates

  return (
    eligible_candidates[
      0
    ],
  )
def filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
  entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  root_step: ProofStep,
) -> tuple[
  TodaGroupProofNarrativeReferenceEntry,
  ...,
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
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  root_boundary = (
    classify_toda_literature_statement_step(
      root_step
    )
  )

  target_reference_locator = (
    None
    if root_boundary is None
    else root_boundary.reference_locator
  )
  target_component_key = (
    None
    if root_boundary is None
    else root_boundary.component_key
  )

  retained_entries = []

  for entry in entries:
    retained_steps = []

    for proof_step in entry.proof_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is None
        or boundary.classification
        != TodaLiteratureStatementClassification.FIXED_STATEMENT
      ):
        continue

      if boundary.component_key is None:
        fixed_components = (
          get_toda_fixed_statement_components(
            boundary.reference_locator
          )
        )

        if fixed_components:
          retained_steps.append(
            proof_step
          )

        continue

      component = (
        get_toda_fixed_statement_component(
          boundary.reference_locator,
          boundary.component_key,
        )
      )

      if component is None:
        continue

      if (
        target_reference_locator is not None
        and target_component_key is not None
        and not is_toda_fixed_statement_component_reference_eligible(
          component,
          target_reference_locator,
          target_component_key,
        )
      ):
        continue

      retained_steps.append(
        proof_step
      )

    if not retained_steps:
      continue

    retained_entries.append(
      replace(
        entry,
        number=len(
          retained_entries
        ) + 1,
        proof_steps=tuple(
          retained_steps
        ),
      )
    )

  return tuple(
    retained_entries
  )


def filter_phase157_r4_representative_reference_entries_by_fixed_statement_boundary(
  entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  root_step: ProofStep,
) -> tuple[
  TodaGroupProofNarrativeReferenceEntry,
  ...,
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
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  conclusion = root_step.conclusion
  lhs = getattr(
    conclusion,
    "lhs",
    None,
  )

  target = (
    getattr(
      lhs,
      "group_dimension",
      None,
    ),
    getattr(
      lhs,
      "sphere_dimension",
      None,
    ),
  )

  representative_targets = {
    (8, 5),
    (10, 4),
    (12, 5),
    (15, 8),
    (16, 9),
  }

  if target not in representative_targets:
    return entries

  root_boundary = (
    classify_toda_literature_statement_step(
      root_step
    )
  )

  target_reference_locator = (
    None
    if root_boundary is None
    else root_boundary.reference_locator
  )
  target_component_key = (
    None
    if root_boundary is None
    else root_boundary.component_key
  )

  retained_entries = []

  for entry in entries:
    retained_steps = []

    for proof_step in entry.proof_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is None
        or boundary.classification
        != TodaLiteratureStatementClassification.FIXED_STATEMENT
        or boundary.component_key is None
      ):
        continue

      component = (
        get_toda_fixed_statement_component(
          boundary.reference_locator,
          boundary.component_key,
        )
      )

      if component is None:
        continue

      if (
        target_reference_locator is not None
        and target_component_key is not None
        and not is_toda_fixed_statement_component_reference_eligible(
          component,
          target_reference_locator,
          target_component_key,
        )
      ):
        continue

      retained_steps.append(
        proof_step
      )

    if not retained_steps:
      continue

    retained_entries.append(
      replace(
        entry,
        number=len(
          retained_entries
        ) + 1,
        proof_steps=tuple(
          retained_steps
        ),
      )
    )

  return tuple(
    retained_entries
  )

def filter_toda_group_proof_narrative_reference_entries_by_step_usage(
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
  used_step_ids: frozenset[
    int
  ],
  root_step: ProofStep,
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
    used_step_ids,
    frozenset,
  ):
    raise TypeError(
      "used_step_ids must be a frozenset"
    )

  if not all(
    isinstance(
      step_id,
      int,
    )
    and not isinstance(
      step_id,
      bool,
    )
    for step_id in used_step_ids
  ):
    raise TypeError(
      "used_step_ids must contain only integers"
    )

  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  root_reference = (
    extract_toda_group_proof_step_literature_reference(
      root_step
    )
  )

  used_entries = tuple(
    entry
    for entry in entries
    if (
      not _same_toda_group_proof_literature_reference(
        entry.reference,
        root_reference,
      )
      and any(
        id(
          proof_step
        )
        in used_step_ids
        for proof_step in entry.proof_steps
      )
    )
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

  return (
    filtered_entries,
    filtered_statement_lines,
  )


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

  if not body_reference_numbers:
    return (
      entries,
      statement_lines_by_reference_number,
      body_markdown,
    )

  used_reference_numbers = set(
    body_reference_numbers
  )
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



def restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(
  original_entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  original_statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  filtered_entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  filtered_statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  body_markdown: str,
  root_step: ProofStep,
  used_step_ids: frozenset[
    int
  ],
  presentation: TodaGroupProofPresentation | None = None,
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
    original_entries,
    tuple,
  ):
    raise TypeError(
      "original_entries must be a tuple"
    )

  if not isinstance(
    original_statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "original_statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    filtered_entries,
    tuple,
  ):
    raise TypeError(
      "filtered_entries must be a tuple"
    )

  if not isinstance(
    filtered_statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "filtered_statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  if not isinstance(
    used_step_ids,
    frozenset,
  ):
    raise TypeError(
      "used_step_ids must be a frozenset"
    )

  if (
    presentation is not None
    and not isinstance(
      presentation,
      TodaGroupProofPresentation,
    )
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation or None"
    )

  retained_reference_keys = {
    (
      entry.reference.locator,
      entry.reference.label,
      tuple(
        id(
          proof_step
        )
        for proof_step in entry.proof_steps
      ),
    )
    for entry in filtered_entries
  }

  reference_internal_step_ids = {
    id(
      proof_step
    )
    for entry in original_entries
    for proof_step in entry.proof_steps
    if proof_step is not root_step
  }

  consumers_by_step_id = {}
  presentation_steps = ()

  if presentation is not None:
    presentation_steps = tuple(
      node.proof_step
      for node in presentation.nodes
    )

    for edge in presentation.edges:
      consumers_by_step_id.setdefault(
        id(
          edge.premise_step
        ),
        [],
      ).append(
        edge.parent_step
      )

  def equivalent_step_ids(
    proof_step: ProofStep,
  ) -> frozenset[
    int
  ]:
    if presentation is None:
      return frozenset(
        {
          id(
            proof_step
          )
        }
      )

    return frozenset(
      id(
        candidate
      )
      for candidate in presentation_steps
      if (
        candidate is proof_step
        or candidate.conclusion
        == proof_step.conclusion
      )
    )

  def has_used_external_descendant(
    proof_step: ProofStep,
  ) -> bool:
    starting_ids = equivalent_step_ids(
      proof_step
    )

    if any(
      step_id in used_step_ids
      and step_id
      not in reference_internal_step_ids
      for step_id in starting_ids
    ):
      return True

    if presentation is None:
      return any(
        step_id in used_step_ids
        for step_id in starting_ids
      )

    frontier = []

    for step_id in starting_ids:
      frontier.extend(
        consumers_by_step_id.get(
          step_id,
          (),
        )
      )

    seen_step_ids = set(
      starting_ids
    )

    while frontier:
      consumer = frontier.pop(
        0
      )
      consumer_id = id(
        consumer
      )

      if consumer_id in seen_step_ids:
        continue

      equivalent_consumer_ids = (
        equivalent_step_ids(
          consumer
        )
      )

      seen_step_ids.update(
        equivalent_consumer_ids
      )

      if (
        consumer is root_step
        or id(
          root_step
        )
        in equivalent_consumer_ids
        or any(
          step_id in used_step_ids
          and step_id
          not in reference_internal_step_ids
          for step_id in equivalent_consumer_ids
        )
      ):
        return True

      for step_id in equivalent_consumer_ids:
        frontier.extend(
          consumers_by_step_id.get(
            step_id,
            (),
          )
        )

    return False

  desired_entries = []

  for entry in original_entries:
    has_selected_statement = (
      entry.number
      in original_statement_lines_by_reference_number
      and bool(
        original_statement_lines_by_reference_number[
          entry.number
        ]
      )
    )

    is_used_fixed_reference = (
      has_selected_statement
      and any(
        has_used_external_descendant(
          proof_step
        )
        for proof_step in entry.proof_steps
      )
    )

    entry_key = (
      entry.reference.locator,
      entry.reference.label,
      tuple(
        id(
          proof_step
        )
        for proof_step in entry.proof_steps
      ),
    )

    if (
      entry_key
      in retained_reference_keys
      or is_used_fixed_reference
    ):
      desired_entries.append(
        entry
      )

  if len(
    desired_entries
  ) == len(
    filtered_entries
  ):
    return (
      filtered_entries,
      filtered_statement_lines_by_reference_number,
      body_markdown,
    )

  number_map = {
    entry.number: new_number
    for new_number, entry in enumerate(
      desired_entries,
      start=1,
    )
  }

  restored_entries = tuple(
    replace(
      entry,
      number=number_map[
        entry.number
      ],
    )
    for entry in desired_entries
  )

  restored_statement_lines = {
    number_map[
      entry.number
    ]: original_statement_lines_by_reference_number[
      entry.number
    ]
    for entry in desired_entries
    if (
      entry.number
      in original_statement_lines_by_reference_number
    )
  }

  filtered_original_number_by_new_number = {}

  for filtered_entry in filtered_entries:
    filtered_key = (
      filtered_entry.reference.locator,
      filtered_entry.reference.label,
      tuple(
        id(
          proof_step
        )
        for proof_step in filtered_entry.proof_steps
      ),
    )

    matching_original_entry = next(
      (
        original_entry
        for original_entry in original_entries
        if (
          (
            original_entry.reference.locator,
            original_entry.reference.label,
            tuple(
              id(
                proof_step
              )
              for proof_step
              in original_entry.proof_steps
            ),
          )
          == filtered_key
        )
      ),
      None,
    )

    if matching_original_entry is not None:
      filtered_original_number_by_new_number[
        filtered_entry.number
      ] = matching_original_entry.number

  marker_placeholders = {}

  def placeholder_marker(
    match,
  ):
    old_number = int(
      match.group(
        1
      )
    )
    original_number = (
      filtered_original_number_by_new_number.get(
        old_number
      )
    )

    if original_number is None:
      return match.group(
        0
      )

    new_number = number_map.get(
      original_number
    )

    if new_number is None:
      return match.group(
        0
      )

    placeholder = (
      "__PHASE157_R20_REFERENCE_ALIAS_"
      + str(
        len(
          marker_placeholders
        )
      )
      + "__"
    )

    marker_placeholders[
      placeholder
    ] = (
      "[R"
      + str(
        new_number
      )
      + "]"
    )

    return placeholder

  remapped_body = re.sub(
    r"\[R([0-9]+)\]",
    placeholder_marker,
    body_markdown,
  )

  for placeholder, marker in marker_placeholders.items():
    remapped_body = remapped_body.replace(
      placeholder,
      marker,
    )

  return (
    restored_entries,
    restored_statement_lines,
    remapped_body,
  )


def restore_phase157_r4_representative_fixed_reference_entries_after_body_usage(
  original_entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  original_statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  filtered_entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  filtered_statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  body_markdown: str,
  root_step: ProofStep,
  used_step_ids: frozenset[
    int
  ],
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
    original_entries,
    tuple,
  ):
    raise TypeError(
      "original_entries must be a tuple"
    )

  if not isinstance(
    original_statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "original_statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    filtered_entries,
    tuple,
  ):
    raise TypeError(
      "filtered_entries must be a tuple"
    )

  if not isinstance(
    filtered_statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "filtered_statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  if not isinstance(
    used_step_ids,
    frozenset,
  ):
    raise TypeError(
      "used_step_ids must be a frozenset"
    )

  conclusion = root_step.conclusion
  lhs = getattr(
    conclusion,
    "lhs",
    None,
  )
  target = (
    getattr(
      lhs,
      "group_dimension",
      None,
    ),
    getattr(
      lhs,
      "sphere_dimension",
      None,
    ),
  )

  representative_targets = {
    (8, 5),
    (10, 4),
    (12, 5),
    (15, 8),
    (16, 9),
  }

  if target not in representative_targets:
    return (
      filtered_entries,
      filtered_statement_lines_by_reference_number,
      body_markdown,
    )

  retained_reference_keys = {
    (
      entry.reference.locator,
      entry.reference.label,
      tuple(
        id(
          proof_step
        )
        for proof_step in entry.proof_steps
      ),
    )
    for entry in filtered_entries
  }

  desired_entries = []

  for entry in original_entries:
    has_selected_statement = (
      entry.number
      in original_statement_lines_by_reference_number
      and bool(
        original_statement_lines_by_reference_number[
          entry.number
        ]
      )
    )
    is_used_fixed_reference = (
      has_selected_statement
      and any(
        id(
          proof_step
        )
        in used_step_ids
        for proof_step in entry.proof_steps
      )
    )

    if (
      (
        entry.reference.locator,
        entry.reference.label,
        tuple(
          id(
            proof_step
          )
          for proof_step in entry.proof_steps
        ),
      )
      in retained_reference_keys
      or is_used_fixed_reference
    ):
      desired_entries.append(
        entry
      )

  if len(
    desired_entries
  ) == len(
    filtered_entries
  ):
    return (
      filtered_entries,
      filtered_statement_lines_by_reference_number,
      body_markdown,
    )

  number_map = {
    entry.number: new_number
    for new_number, entry in enumerate(
      desired_entries,
      start=1,
    )
  }

  restored_entries = tuple(
    replace(
      entry,
      number=number_map[
        entry.number
      ],
    )
    for entry in desired_entries
  )

  restored_statement_lines = {
    number_map[
      entry.number
    ]: original_statement_lines_by_reference_number[
      entry.number
    ]
    for entry in desired_entries
    if (
      entry.number
      in original_statement_lines_by_reference_number
    )
  }

  filtered_original_number_by_new_number = {}

  for filtered_entry in filtered_entries:
    matching_original_entry = next(
      (
        original_entry
        for original_entry in original_entries
        if (
          original_entry.reference
          == filtered_entry.reference
          and original_entry.proof_steps
          == filtered_entry.proof_steps
        )
      ),
      None,
    )

    if matching_original_entry is not None:
      filtered_original_number_by_new_number[
        filtered_entry.number
      ] = matching_original_entry.number

  marker_placeholders = {}

  def placeholder_marker(
    match,
  ):
    old_number = int(
      match.group(
        1
      )
    )
    original_number = (
      filtered_original_number_by_new_number.get(
        old_number
      )
    )

    if original_number is None:
      return match.group(
        0
      )

    new_number = number_map.get(
      original_number
    )

    if new_number is None:
      return match.group(
        0
      )

    placeholder = (
      "__PHASE157_R4_R3_REFERENCE_"
      + str(
        len(
          marker_placeholders
        )
      )
      + "__"
    )
    marker_placeholders[
      placeholder
    ] = (
      "[R"
      + str(
        new_number
      )
      + "]"
    )
    return placeholder

  remapped_body = re.sub(
    r"\[R([0-9]+)\]",
    placeholder_marker,
    body_markdown,
  )

  for placeholder, marker in marker_placeholders.items():
    remapped_body = remapped_body.replace(
      placeholder,
      marker,
    )

  return (
    restored_entries,
    restored_statement_lines,
    remapped_body,
  )

def render_toda_group_proof_narrative_reference_entries_markdown(
  entries: tuple[TodaGroupProofNarrativeReferenceEntry, ...],
  statement_lines_by_reference_number: (
    dict[
      int,
      tuple[
        str,
        ...,
      ],
    ]
    | None
  ) = None,
) -> str:
  if not isinstance(entries, tuple):
    raise TypeError("entries must be a tuple")

  if (
    statement_lines_by_reference_number is not None
    and not isinstance(
      statement_lines_by_reference_number,
      dict,
    )
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be "
      "a dict or None"
    )

  if statement_lines_by_reference_number is not None:
    for reference_number, statement_lines in (
      statement_lines_by_reference_number.items()
    ):
      if (
        isinstance(
          reference_number,
          bool,
        )
        or not isinstance(
          reference_number,
          int,
        )
      ):
        raise TypeError(
          "statement_lines_by_reference_number keys "
          "must be integers"
        )

      if not isinstance(
        statement_lines,
        tuple,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must be tuples"
        )

      if not all(
        isinstance(
          line,
          str,
        )
        for line in statement_lines
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

  if not entries:
    return ""

  lines = []

  for entry in entries:
    if not isinstance(entry, TodaGroupProofNarrativeReferenceEntry):
      raise TypeError(
        "entries must contain only "
        "TodaGroupProofNarrativeReferenceEntry objects"
      )

    title = entry.reference.locator or entry.reference.label
    lines.append(f"**[R{entry.number}] {title}.**")

    statement_lines = (
      ()
      if statement_lines_by_reference_number is None
      else statement_lines_by_reference_number.get(
        entry.number,
        (),
      )
    )

    for statement_line in statement_lines:
      lines.append(
        statement_line
      )

  return "\n".join(lines)
