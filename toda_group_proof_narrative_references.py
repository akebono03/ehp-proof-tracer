from dataclasses import (
  dataclass,
  replace,
)
import re

from proof import (
  LiteratureReference,
  ProofStep,
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

  retained_entries = tuple(
    entry
    for entry in entries
    if not _same_toda_group_proof_literature_reference(
      entry.reference,
      root_reference,
    )
  )

  if len(retained_entries) == len(entries):
    return (
      entries,
      statement_lines_by_reference_number,
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
    if entry.number in statement_lines_by_reference_number
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

  boundary_used_candidates = tuple(
    step
    for step in eligible_candidates
    if id(
      step
    ) in boundary_used_step_ids
  )

  if boundary_used_candidates:
    return boundary_used_candidates

  proof_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in proof_edges
  }

  proof_used_candidates = tuple(
    step
    for step in eligible_candidates
    if id(
      step
    ) in proof_used_step_ids
  )

  if proof_used_candidates:
    return proof_used_candidates

  return (
    eligible_candidates[0],
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

  lines = ["使用する結果を先にまとめる。", ""]

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
