from pathlib import Path

REFERENCES = Path("toda_group_proof_narrative_references.py")
CONTRIBUTION = Path("toda_group_proof_narrative_contribution_renderer.py")
RENDERER = Path("toda_group_proof_narrative_renderer.py")


RESTORE_FUNCTION = r'''

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
      entry.reference,
      entry.proof_steps,
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
        entry.reference,
        entry.proof_steps,
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
'''


def insert_restore_function(
    text: str,
) -> str:
    name = (
        "def restore_phase157_r4_representative_fixed_reference_entries_"
        "after_body_usage("
    )

    if name in text:
        return text

    anchor = (
        "\ndef render_toda_group_proof_narrative_reference_entries_markdown("
    )
    index = text.find(
        anchor
    )

    if index < 0:
        raise SystemExit(
            "restore function insertion anchor not found"
        )

    return (
        text[:index]
        + RESTORE_FUNCTION
        + text[index:]
    )


def add_import_name(
    text: str,
    name: str,
) -> str:
    import_line = (
        "  "
        + name
        + ",\n"
    )

    if import_line in text:
        return text

    anchor = (
        "  render_toda_group_proof_narrative_reference_entries_markdown,\n"
    )
    if anchor not in text:
        raise SystemExit(
            "reference import anchor not found for "
            + name
        )

    return text.replace(
        anchor,
        import_line + anchor,
        1,
    )


FILTER_NAME = (
    "filter_phase157_r4_representative_reference_entries_"
    "by_fixed_statement_boundary"
)

RESTORE_NAME = (
    "restore_phase157_r4_representative_fixed_reference_entries_"
    "after_body_usage"
)


BUILD_BLOCK = '''  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
'''

FILTER_BLOCK = '''  reference_entries = (
    filter_phase157_r4_representative_reference_entries_by_fixed_statement_boundary(
      reference_entries,
      presentation.root_step,
    )
  )
'''


def ensure_renderer_filter_connections(
    text: str,
) -> str:
    build_positions = []
    start = 0

    while True:
      position = text.find(
        BUILD_BLOCK,
        start,
      )
      if position < 0:
        break
      build_positions.append(
        position
      )
      start = (
        position
        + len(
          BUILD_BLOCK
        )
      )

    if len(
      build_positions
    ) != 2:
      raise SystemExit(
        "expected exactly 2 current renderer reference build blocks, found "
        + str(
          len(
            build_positions
          )
        )
      )

    offset = 0

    for position in build_positions:
      adjusted = (
        position
        + offset
        + len(
          BUILD_BLOCK
        )
      )
      following = text[
        adjusted:
        adjusted
        + len(
          FILTER_BLOCK
        )
        + 80
      ]

      if FILTER_NAME in following:
        continue

      text = (
        text[:adjusted]
        + FILTER_BLOCK
        + text[adjusted:]
      )
      offset += len(
        FILTER_BLOCK
      )

    return text


def patch_contribution_restore(
    text: str,
) -> str:
    capture_anchor = '''  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
'''

    capture_block = capture_anchor + '''  phase157_r4_reference_entries_before_usage_filter = (
    reference_entries
  )
  phase157_r4_statement_lines_before_usage_filter = dict(
    statement_lines_by_reference_number
  )
'''

    if (
      "phase157_r4_reference_entries_before_usage_filter"
      not in text
    ):
      if capture_anchor not in text:
        raise SystemExit(
            "contribution capture anchor not found"
        )
      text = text.replace(
        capture_anchor,
        capture_block,
        1,
      )

    body_filter_block = '''    (
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_body_usage(
        reference_entries,
        statement_lines_by_reference_number,
        rendered,
      )
    )
'''

    restore_call_marker = (
      "restore_phase157_r4_representative_fixed_reference_entries_"
      "after_body_usage(\n"
      "        phase157_r4_reference_entries_before_usage_filter,"
    )

    if restore_call_marker not in text:
      if body_filter_block not in text:
        raise SystemExit(
            "contribution body-usage block not found"
        )

      restore_block = body_filter_block + '''    (
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    ) = (
      restore_phase157_r4_representative_fixed_reference_entries_after_body_usage(
        phase157_r4_reference_entries_before_usage_filter,
        phase157_r4_statement_lines_before_usage_filter,
        reference_entries,
        statement_lines_by_reference_number,
        rendered,
        presentation.root_step,
        generic_used_step_ids,
      )
    )
'''
      text = text.replace(
        body_filter_block,
        restore_block,
        1,
      )

    return text


def main():
    for path in (
      REFERENCES,
      CONTRIBUTION,
      RENDERER,
    ):
      if not path.exists():
        raise SystemExit(
          f"target not found: {path}"
        )

    references_text = REFERENCES.read_text(
      encoding="utf-8"
    )
    references_text = insert_restore_function(
      references_text
    )
    REFERENCES.write_text(
      references_text,
      encoding="utf-8",
      newline="\n",
    )

    contribution_text = CONTRIBUTION.read_text(
      encoding="utf-8"
    )
    contribution_text = add_import_name(
      contribution_text,
      RESTORE_NAME,
    )
    contribution_text = patch_contribution_restore(
      contribution_text
    )
    CONTRIBUTION.write_text(
      contribution_text,
      encoding="utf-8",
      newline="\n",
    )

    renderer_text = RENDERER.read_text(
      encoding="utf-8"
    )
    renderer_text = add_import_name(
      renderer_text,
      FILTER_NAME,
    )
    renderer_text = ensure_renderer_filter_connections(
      renderer_text
    )
    RENDERER.write_text(
      renderer_text,
      encoding="utf-8",
      newline="\n",
    )

    print("Phase157-R4-R3 repair1 changes applied.")
    print(f"updated: {REFERENCES.resolve()}")
    print(f"updated: {CONTRIBUTION.resolve()}")
    print(f"updated: {RENDERER.resolve()}")


if __name__ == "__main__":
  main()
