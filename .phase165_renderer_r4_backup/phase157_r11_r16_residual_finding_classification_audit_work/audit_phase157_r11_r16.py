from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(0, str(REPO_ROOT))

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  filter_phase157_r3_pi6_3_reference_entries,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

TARGET_GROUPS = (
  (3, 3),
  (4, 6),
  (5, 3),
  (5, 7),
  (8, 7),
  (9, 7),
)

REFERENCE_HEADER_RE = re.compile(
  r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*"
)
REFERENCE_MARKER_RE = re.compile(r"\[R([0-9]+)\]")
REPEATED_NUMERIC_EQUALITY_RE = re.compile(
  r"=\s*([0-9]+)\s*=\s*\1(?:[^0-9]|$)"
)
STANDALONE_CONNECTORS = (
  "以上より,",
  "したがって,",
  "これより,",
)


def label(n: int, k: int) -> str:
  return f"pi_{n + k}^{n}"


def build_raw(n: int, k: int):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  if not report.candidates:
    raise AssertionError(
      f"no report candidate for n={n}, k={k}"
    )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def split_reference_body(rendered: str):
  marker = "\n## 証明\n"
  if marker not in rendered:
    return "", rendered
  return rendered.split(
    marker,
    1,
  )


def paragraphs(body: str):
  return tuple(
    paragraph
    for paragraph in body.split("\n\n")
    if paragraph.strip()
  )


def reference_headers(reference: str):
  return tuple(
    (
      int(match.group(1)),
      match.group(2),
    )
    for match in REFERENCE_HEADER_RE.finditer(
      reference
    )
  )


def marker_numbers(body: str):
  return frozenset(
    int(match.group(1))
    for match in REFERENCE_MARKER_RE.finditer(
      body
    )
  )


def reference_identity(step):
  reference = extract_toda_group_proof_step_literature_reference(
    step
  )
  if reference is None:
    return None
  return (
    reference.locator
    or reference.label
  )


def context(paragraph_values, index: int, radius: int = 2):
  start = max(
    0,
    index - radius,
  )
  end = min(
    len(paragraph_values),
    index + radius + 1,
  )
  return tuple(
    (
      paragraph_index,
      paragraph_values[paragraph_index],
    )
    for paragraph_index in range(
      start,
      end,
    )
  )


def entry_map(presentation):
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  entries = filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
    entries,
    presentation.root_step,
  )
  entries = filter_phase157_r3_pi6_3_reference_entries(
    entries,
    presentation.root_step,
  )
  return {
    (
      entry.reference.locator
      or entry.reference.label
    ): entry
    for entry in entries
  }


def main() -> int:
  output_dir = PACKAGE_DIR / "audit_output"
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  rows = []
  report_lines = [
    "=" * 78,
    "Phase157 R11-R16 — Residual Finding Classification Audit",
    "=" * 78,
    "Production code changes: none",
    "Test code changes: none",
    "Target groups: 6 groups from R11-R15 findings",
    "",
  ]

  for n, k in TARGET_GROUPS:
    group = label(
      n,
      k,
    )
    raw = build_raw(
      n,
      k,
    )
    presentation = build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
    rendered = render_toda_group_proof_narrative_markdown(
      raw
    )
    reference, body = split_reference_body(
      rendered
    )
    body_paragraphs = paragraphs(
      body
    )
    headers = reference_headers(
      reference
    )
    markers = marker_numbers(
      body
    )
    entries = entry_map(
      presentation
    )

    consumers_by_step_id = {}
    for edge in presentation.edges:
      consumers_by_step_id.setdefault(
        id(edge.premise_step),
        [],
      ).append(
        edge.parent_step
      )

    report_lines.extend(
      (
        "-" * 78,
        group,
        "-" * 78,
      )
    )

    for index, paragraph in enumerate(
      body_paragraphs
    ):
      stripped = paragraph.strip()

      if stripped in STANDALONE_CONNECTORS:
        report_lines.append(
          f"Standalone connector at paragraph[{index}]: {stripped!r}"
        )
        for c_index, c_paragraph in context(
          body_paragraphs,
          index,
        ):
          marker = (
            ">>"
            if c_index == index
            else "  "
          )
          report_lines.append(
            f"  {marker} [{c_index}] "
            + c_paragraph.replace(
              "\n",
              " | ",
            )
          )
        rows.append(
          {
            "group": group,
            "category": "standalone_connector",
            "item": stripped,
            "classification": "review_required",
            "evidence": f"paragraph_index={index}",
          }
        )

      if REPEATED_NUMERIC_EQUALITY_RE.search(
        stripped
      ):
        report_lines.append(
          "Repeated numeric equality: "
          + stripped.replace(
            "\n",
            " | ",
          )
        )
        rows.append(
          {
            "group": group,
            "category": "repeated_numeric_equality",
            "item": stripped,
            "classification": "confirmed_display_defect",
            "evidence": "same numeric literal repeated around '='",
          }
        )

    unused_headers = tuple(
      (
        number,
        title,
      )
      for number, title in headers
      if number not in markers
    )

    if unused_headers:
      report_lines.append(
        "Public References without body marker:"
      )

    for number, title in unused_headers:
      report_lines.append(
        f"  [R{number}] {title}"
      )
      entry = entries.get(
        title
      )

      if entry is None:
        rows.append(
          {
            "group": group,
            "category": "public_reference_without_body_marker",
            "item": f"[R{number}] {title}",
            "classification": "entry_lookup_failed",
            "evidence": "",
          }
        )
        report_lines.append(
          "    entry not found in pre-public Reference entries"
        )
        continue

      direct_public_consumers = []
      root_consumers = []
      reference_only_consumers = []

      for step in entry.proof_steps:
        report_lines.append(
          "    statement: "
          + _render_generic_narrative_step(
            step
          )
        )

        for consumer in consumers_by_step_id.get(
          id(step),
          (),
        ):
          consumer_rendered = _render_generic_narrative_step(
            consumer
          )
          consumer_reference = reference_identity(
            consumer
          )
          is_root = (
            consumer is presentation.root_step
          )
          report_lines.append(
            "      consumer: "
            + consumer_rendered
            + " | reference="
            + repr(consumer_reference)
            + " | root="
            + str(is_root)
          )

          if is_root:
            root_consumers.append(
              consumer
            )
          elif (
            consumer_reference is None
            and consumer_rendered in body
          ):
            direct_public_consumers.append(
              consumer
            )
          elif consumer_reference is not None:
            reference_only_consumers.append(
              consumer
            )

      if direct_public_consumers:
        classification = "needed_but_marker_missing"
      elif root_consumers:
        classification = "needed_for_root_but_marker_missing"
      elif reference_only_consumers:
        classification = "ancestry_only_candidate"
      else:
        classification = "no_visible_direct_consumer_candidate"

      evidence = (
        "direct_public_consumers="
        + str(len(direct_public_consumers))
        + "; root_consumers="
        + str(len(root_consumers))
        + "; reference_only_consumers="
        + str(len(reference_only_consumers))
      )
      rows.append(
        {
          "group": group,
          "category": "public_reference_without_body_marker",
          "item": f"[R{number}] {title}",
          "classification": classification,
          "evidence": evidence,
        }
      )

    hidden_zero_map_steps = tuple(
      node.proof_step
      for node in presentation.nodes
      if (
        "零写像である."
        in _render_generic_narrative_step(
          node.proof_step
        )
        and _render_generic_narrative_step(
          node.proof_step
        )
        not in body
      )
    )

    if (
      "Δ=0" in body
      or r"\Delta=0" in body
    ):
      for step in hidden_zero_map_steps:
        rendered_step = _render_generic_narrative_step(
          step
        )
        if (
          r"\Delta"
          not in rendered_step
          and "Delta"
          not in (
            step.inference_rule.name
            if step.inference_rule is not None
            else ""
          )
        ):
          continue

        report_lines.append(
          "Hidden zero-map statement used via shorthand:"
        )
        report_lines.append(
          "  "
          + rendered_step
        )

        for consumer in consumers_by_step_id.get(
          id(step),
          (),
        ):
          report_lines.append(
            "    consumer: "
            + _render_generic_narrative_step(
              consumer
            )
          )

        rows.append(
          {
            "group": group,
            "category": "zero_map_used_without_visible_statement",
            "item": rendered_step,
            "classification": "confirmed_visibility_gap",
            "evidence": (
              "body contains Delta=0 shorthand "
              "while full zero-map statement is hidden"
            ),
          }
        )

    four_term_indices = tuple(
      index
      for index, paragraph in enumerate(
        body_paragraphs
      )
      if (
        r"\xrightarrow{\Delta}" in paragraph
        and r"\xrightarrow{E}" in paragraph
        and r"\xrightarrow{H}" in paragraph
      )
    )
    injective_indices = tuple(
      index
      for index, paragraph in enumerate(
        body_paragraphs
      )
      if (
        paragraph.strip().startswith(
          "$E:"
        )
        and " は単射である."
        in paragraph
      )
    )

    if (
      four_term_indices
      and injective_indices
    ):
      first_injective = min(
        injective_indices
      )

      for index in four_term_indices:
        if index <= first_injective:
          continue

        report_lines.append(
          "Four-term EHP after visible E-injectivity:"
        )
        for c_index, c_paragraph in context(
          body_paragraphs,
          index,
        ):
          marker = (
            ">>"
            if c_index == index
            else "  "
          )
          report_lines.append(
            f"  {marker} [{c_index}] "
            + c_paragraph.replace(
              "\n",
              " | ",
            )
          )

        rows.append(
          {
            "group": group,
            "category": "possible_redundant_left_ehp_term",
            "item": body_paragraphs[index],
            "classification": "confirmed_presentation_redundancy_candidate",
            "evidence": (
              f"E injective at paragraph[{first_injective}], "
              f"four-term sequence at paragraph[{index}]"
            ),
          }
        )

    report_lines.append("")

  csv_path = output_dir / "classification.csv"

  with csv_path.open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    fieldnames = (
      "group",
      "category",
      "item",
      "classification",
      "evidence",
    )
    writer = csv.DictWriter(
      handle,
      fieldnames=fieldnames,
    )
    writer.writeheader()
    writer.writerows(
      rows
    )

  summary_counts = {}

  for row in rows:
    key = (
      row["category"],
      row["classification"],
    )
    summary_counts[key] = (
      summary_counts.get(
        key,
        0,
      )
      + 1
    )

  report_lines.extend(
    (
      "=" * 78,
      "Classification summary",
      "=" * 78,
    )
  )

  for key, count in sorted(
    summary_counts.items()
  ):
    category, classification = key
    report_lines.append(
      f"{category} / {classification}: {count}"
    )

  report_lines.extend(
    (
      "",
      "Output:",
      "audit_output/classification.txt",
      "audit_output/classification.csv",
      "",
      "Production code changes: none",
      "Test code changes: none",
      "pytest: not run",
      "=" * 78,
    )
  )

  report = (
    "\n".join(
      report_lines
    )
    + "\n"
  )

  (
    output_dir
    / "classification.txt"
  ).write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
