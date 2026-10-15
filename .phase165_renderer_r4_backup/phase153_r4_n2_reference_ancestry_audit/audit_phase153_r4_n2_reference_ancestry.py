from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


from proof import ProofStep
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGETS = (
  (2, 2),
  (2, 3),
  (2, 4),
  (2, 5),
  (2, 6),
  (2, 7),
)


@dataclass(frozen=True)
class StepAudit:
  step: ProofStep
  node_index: int
  rendered_statement: str
  is_root: bool
  is_candidate: bool
  is_selected: bool
  used_as_premise: bool
  direct_parent_indices: tuple[int, ...]
  distance_to_root: int | None


@dataclass(frozen=True)
class ReferenceAudit:
  entry: TodaGroupProofNarrativeReferenceEntry
  steps: tuple[StepAudit, ...]
  root_in_entry: bool
  root_selected: bool


@dataclass(frozen=True)
class GroupAudit:
  n: int
  k: int
  presentation: TodaGroupProofPresentation
  references: tuple[ReferenceAudit, ...]


def _build_presentation(
  *,
  n: int,
  k: int,
) -> TodaGroupProofPresentation:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise RuntimeError(
      f"no standard group result candidate for n={n}, k={k}"
    )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=7,
  )

  return build_toda_group_proof_presentation(
    replay
  )


def _node_index_by_step_id(
  presentation: TodaGroupProofPresentation,
) -> dict[int, int]:
  return {
    id(node.proof_step): index
    for index, node in enumerate(
      presentation.nodes
    )
  }


def _candidate_steps(
  entry: TodaGroupProofNarrativeReferenceEntry,
) -> tuple[ProofStep, ...]:
  result = []
  seen_rendered = set()

  for proof_step in entry.proof_steps:
    rendered = _render_generic_narrative_step(
      proof_step
    )

    if not (
      _is_toda_group_proof_narrative_reference_statement_candidate(
        proof_step,
        rendered,
      )
    ):
      continue

    if rendered in seen_rendered:
      continue

    seen_rendered.add(
      rendered
    )
    result.append(
      proof_step
    )

  return tuple(
    result
  )


def _direct_parent_step_ids(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
) -> tuple[int, ...]:
  result = []

  for edge in presentation.edges:
    if edge.premise_step is not proof_step:
      continue

    parent_id = id(
      edge.parent_step
    )

    if parent_id in result:
      continue

    result.append(
      parent_id
    )

  return tuple(
    result
  )


def _distance_to_root(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
) -> int | None:
  if proof_step is presentation.root_step:
    return 0

  children_by_step_id: dict[int, list[ProofStep]] = {}

  for edge in presentation.edges:
    children_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  queue = deque(
    (
      child,
      1,
    )
    for child in children_by_step_id.get(
      id(
        proof_step
      ),
      (),
    )
  )
  visited = {
    id(
      proof_step
    ),
  }

  while queue:
    current, distance = queue.popleft()
    current_id = id(
      current
    )

    if current_id in visited:
      continue

    visited.add(
      current_id
    )

    if current is presentation.root_step:
      return distance

    for child in children_by_step_id.get(
      current_id,
      (),
    ):
      queue.append(
        (
          child,
          distance + 1,
        )
      )

  return None


def audit_group(
  *,
  n: int,
  k: int,
) -> GroupAudit:
  presentation = _build_presentation(
    n=n,
    k=k,
  )
  index_by_step_id = _node_index_by_step_id(
    presentation
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_audits = []

  for entry in entries:
    candidates = _candidate_steps(
      entry
    )
    selected = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        candidates,
        presentation.edges,
      )
    )
    candidate_ids = {
      id(
        step
      )
      for step in candidates
    }
    selected_ids = {
      id(
        step
      )
      for step in selected
    }
    step_audits = []

    for proof_step in entry.proof_steps:
      direct_parent_ids = (
        _direct_parent_step_ids(
          presentation,
          proof_step,
        )
      )
      step_audits.append(
        StepAudit(
          step=proof_step,
          node_index=index_by_step_id[
            id(
              proof_step
            )
          ],
          rendered_statement=(
            _render_generic_narrative_step(
              proof_step
            )
          ),
          is_root=(
            proof_step
            is presentation.root_step
          ),
          is_candidate=(
            id(
              proof_step
            )
            in candidate_ids
          ),
          is_selected=(
            id(
              proof_step
            )
            in selected_ids
          ),
          used_as_premise=bool(
            direct_parent_ids
          ),
          direct_parent_indices=tuple(
            index_by_step_id[
              parent_id
            ]
            for parent_id in direct_parent_ids
          ),
          distance_to_root=_distance_to_root(
            presentation,
            proof_step,
          ),
        )
      )

    reference_audits.append(
      ReferenceAudit(
        entry=entry,
        steps=tuple(
          step_audits
        ),
        root_in_entry=any(
          step.is_root
          for step in step_audits
        ),
        root_selected=any(
          step.is_root
          and step.is_selected
          for step in step_audits
        ),
      )
    )

  return GroupAudit(
    n=n,
    k=k,
    presentation=presentation,
    references=tuple(
      reference_audits
    ),
  )


def _flag(
  value: bool,
) -> str:
  return (
    "YES"
    if value
    else "no"
  )


def _safe_text(
  value: str,
) -> str:
  return (
    value
    .replace(
      "\r",
      " ",
    )
    .replace(
      "\n",
      " ",
    )
  )


def render_group_audit_markdown(
  audit: GroupAudit,
) -> str:
  lines = [
    (
      f"## $\\pi_{{{audit.n + audit.k}}}^{{{audit.n}}}$ "
      f"(n={audit.n}, k={audit.k})"
    ),
    "",
    (
      f"- presentation nodes: "
      f"{len(audit.presentation.nodes)}"
    ),
    (
      f"- proof edges: "
      f"{len(audit.presentation.edges)}"
    ),
    (
      f"- references: "
      f"{len(audit.references)}"
    ),
    (
      "- root statement: "
      + _safe_text(
        _render_generic_narrative_step(
          audit.presentation.root_step
        )
      )
    ),
    "",
  ]

  if not audit.references:
    lines.append(
      "No literature Reference entries."
    )
    lines.append(
      ""
    )
    return "\n".join(
      lines
    )

  for reference_audit in audit.references:
    entry = reference_audit.entry
    title = (
      entry.reference.locator
      or entry.reference.label
    )
    lines.extend(
      [
        (
          f"### [R{entry.number}] "
          f"{title}"
        ),
        "",
        (
          f"- entry steps: "
          f"{len(entry.proof_steps)}"
        ),
        (
          f"- root in entry: "
          f"{_flag(reference_audit.root_in_entry)}"
        ),
        (
          f"- root selected: "
          f"{_flag(reference_audit.root_selected)}"
        ),
        "",
        "| node | root | candidate | selected | premise | distance→root | parents | statement |",
        "| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |",
      ]
    )

    for step in reference_audit.steps:
      distance = (
        "—"
        if step.distance_to_root is None
        else str(
          step.distance_to_root
        )
      )
      parents = (
        "—"
        if not step.direct_parent_indices
        else ", ".join(
          str(
            index
          )
          for index in (
            step.direct_parent_indices
          )
        )
      )
      lines.append(
        "| "
        + " | ".join(
          (
            str(
              step.node_index
            ),
            _flag(
              step.is_root
            ),
            _flag(
              step.is_candidate
            ),
            _flag(
              step.is_selected
            ),
            _flag(
              step.used_as_premise
            ),
            distance,
            parents,
            _safe_text(
              step.rendered_statement
            ).replace(
              "|",
              r"\|",
            ),
          )
        )
        + " |"
      )

    lines.append(
      ""
    )

  return "\n".join(
    lines
  )


def render_summary_markdown(
  audits: tuple[GroupAudit, ...],
) -> str:
  lines = [
    "# Phase 153-R4 — 6-group n=2 Reference ancestry audit",
    "",
    "This is an audit only. Production code is not modified.",
    "",
    "## Summary",
    "",
    "| group | refs | root-in-reference | root-selected | selected statements |",
    "| --- | ---: | ---: | ---: | ---: |",
  ]

  for audit in audits:
    root_in_reference = sum(
      1
      for reference in audit.references
      if reference.root_in_entry
    )
    root_selected = sum(
      1
      for reference in audit.references
      if reference.root_selected
    )
    selected_statements = sum(
      1
      for reference in audit.references
      for step in reference.steps
      if step.is_selected
    )
    lines.append(
      "| "
      + " | ".join(
        (
          (
            f"$\\pi_{{{audit.n + audit.k}}}"
            f"^{{{audit.n}}}$"
          ),
          str(
            len(
              audit.references
            )
          ),
          str(
            root_in_reference
          ),
          str(
            root_selected
          ),
          str(
            selected_statements
          ),
        )
      )
      + " |"
    )

  lines.extend(
    [
      "",
      "## Interpretation guide",
      "",
      "- `root in entry = YES`: the target/root step itself carries the same literature Reference.",
      "- `root selected = YES`: the current statement-selection rule selected that root step for the Reference section.",
      "- `premise = YES`: the step is actually used as a premise by at least one proof edge in the presentation.",
      "- `distance→root`: shortest forward proof-edge distance from the step to the target/root; `0` means the root itself.",
      "- R4 does not decide the new rule. It records the evidence needed to distinguish target/root ownership from actually used external premise/ancestry.",
      "",
      "## Detailed audits",
      "",
    ]
  )

  for audit in audits:
    lines.append(
      render_group_audit_markdown(
        audit
      )
    )

  return "\n".join(
    lines
  ).rstrip() + "\n"


def main() -> int:
  audits = tuple(
    audit_group(
      n=n,
      k=k,
    )
    for n, k in TARGETS
  )

  markdown = render_summary_markdown(
    audits
  )

  output_dir = (
    PACKAGE_DIR
    / "output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  output_path = (
    output_dir
    / "phase153_r4_n2_reference_ancestry_audit.md"
  )
  output_path.write_text(
    markdown,
    encoding="utf-8",
  )

  print(
    markdown
  )
  print(
    "Audit output:"
  )
  print(
    output_path
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
