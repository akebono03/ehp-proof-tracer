from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_r11_r14"
BACKUP.mkdir(exist_ok=True)

CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
REFERENCES = ROOT / "toda_group_proof_narrative_references.py"
R11_TEST = ROOT / "tests" / "test_phase157_r11_reference_reason_punctuation.py"


def backup(path: Path) -> None:
  destination = BACKUP / path.name
  if not destination.exists():
    shutil.copy2(path, destination)


for path in (
  CONTRIBUTION,
  REFERENCES,
  R11_TEST,
):
  backup(path)


def replace_once(
  path: Path,
  old: str,
  new: str,
  label: str,
) -> None:
  text = path.read_text(encoding="utf-8")

  if new in text:
    print(f"Already applied: {label}")
    return

  count = text.count(old)

  if count != 1:
    raise RuntimeError(
      f"expected exactly one match for {label} in {path}, found {count}"
    )

  path.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
  )
  print(f"Applied: {label}")


def insert_order_support_function() -> None:
  text = CONTRIBUTION.read_text(encoding="utf-8")

  function_name = (
    "def order_toda_group_proof_narrative_order_support("
  )

  if function_name in text:
    print("Already applied: ORDER support ordering function")
    return

  anchor = (
    "def order_toda_group_proof_narrative_surjectivity_support(\n"
  )

  if anchor not in text:
    raise RuntimeError(
      "could not locate ORDER support insertion point"
    )

  function = r'''def order_toda_group_proof_narrative_order_support(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    target_key = (
      _phase157_r11_reference_statement_match_key(
        rendered
      )
    )

    matching = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      ) == target_key
    )

    if len(
      matching
    ) != 1:
      return None

    return matching[
      0
    ]

  for node in presentation.nodes:
    order_step = node.proof_step

    if (
      classify_toda_proof_step_role(
        order_step
      )
      is not TodaProofDependencyRole.ORDER
    ):
      continue

    conclusion_index = paragraph_index_for_step(
      order_step
    )

    if conclusion_index is None:
      continue

    premise_indices = tuple(
      index
      for premise in order_step.premises
      for index in (
        paragraph_index_for_step(
          premise
        ),
      )
      if index is not None
    )

    if not premise_indices:
      continue

    latest_premise_index = max(
      premise_indices
    )

    if latest_premise_index < conclusion_index:
      continue

    block_end = conclusion_index + 1

    if (
      block_end < len(
        paragraphs
      )
      and paragraphs[
        block_end
      ].strip()
      == "以上より,"
    ):
      block_end += 1

    conclusion_block = paragraphs[
      conclusion_index:
      block_end
    ]

    del paragraphs[
      conclusion_index:
      block_end
    ]

    premise_indices_after_removal = tuple(
      index
      for premise in order_step.premises
      for index in (
        paragraph_index_for_step(
          premise
        ),
      )
      if index is not None
    )

    if not premise_indices_after_removal:
      continue

    insertion_index = (
      max(
        premise_indices_after_removal
      )
      + 1
    )

    paragraphs[
      insertion_index:
      insertion_index
    ] = conclusion_block

  return "\n\n".join(
    paragraphs
  )


'''

  CONTRIBUTION.write_text(
    text.replace(
      anchor,
      function + anchor,
      1,
    ),
    encoding="utf-8",
  )

  print("Applied: generic ORDER dependency ordering")


insert_order_support_function()


start_marker = (
  "def order_toda_group_proof_narrative_surjectivity_support(\n"
)
end_marker = (
  "\n\ndef insert_toda_group_proof_narrative_reference_map_values_before_surjectivity(\n"
)

text = CONTRIBUTION.read_text(encoding="utf-8")
start = text.find(start_marker)
end = text.find(end_marker, start)

if start < 0 or end < 0:
  raise RuntimeError(
    "could not locate surjectivity-support function"
  )

replacement_surjectivity = r'''def order_toda_group_proof_narrative_surjectivity_support(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    rendered_statement = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered_statement:
      return None

    target_key = (
      _phase157_r11_reference_statement_match_key(
        rendered_statement
      )
    )

    matching_indices = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      ) == target_key
    )

    if len(
      matching_indices
    ) != 1:
      return None

    return matching_indices[
      0
    ]

  for node in presentation.nodes:
    map_step = node.proof_step

    if (
      classify_toda_proof_step_role(
        map_step
      )
      is not TodaProofDependencyRole.MAP_PROPERTY
    ):
      continue

    map_index = paragraph_index_for_step(
      map_step
    )

    if map_index is None:
      continue

    equality_premises = tuple(
      premise
      for premise in map_step.premises
      if (
        isinstance(
          premise.conclusion,
          Relation,
        )
        and premise.conclusion.relation_type
        is RelationType.EQUALITY
      )
    )

    support_steps = []

    for equality_premise in equality_premises:
      support_steps.extend(
        premise
        for premise in equality_premise.premises
        if (
          isinstance(
            premise.conclusion,
            Relation,
          )
          and premise.conclusion.relation_type
          is RelationType.EQUALITY
        )
      )
      support_steps.append(
        equality_premise
      )

    support_indices = tuple(
      index
      for proof_step in support_steps
      for index in (
        paragraph_index_for_step(
          proof_step
        ),
      )
      if index is not None
    )

    if (
      support_steps
      and len(
        support_indices
      ) == len(
        support_steps
      )
    ):
      first_support_index = min(
        support_indices
      )
      last_support_index = max(
        support_indices
      )

      if not (
        first_support_index < map_index
        and last_support_index < map_index
      ):
        support_block = paragraphs[
          first_support_index:
          last_support_index + 1
        ]

        del paragraphs[
          first_support_index:
          last_support_index + 1
        ]

        map_index = paragraph_index_for_step(
          map_step
        )

        if map_index is not None:
          paragraphs[
            map_index:
            map_index
          ] = support_block

    map_index = paragraph_index_for_step(
      map_step
    )

    if map_index is None:
      continue

    short_exact_reason_index = next(
      (
        index
        for index in range(
          map_index
        )
        if (
          "右の写像が全射"
          in paragraphs[
            index
          ]
          and "短完全列"
          in paragraphs[
            index
          ]
        )
      ),
      None,
    )

    if short_exact_reason_index is None:
      continue

    support_indices = tuple(
      index
      for proof_step in support_steps
      for index in (
        paragraph_index_for_step(
          proof_step
        ),
      )
      if index is not None
    )

    block_start = (
      min(
        support_indices
      )
      if support_indices
      else map_index
    )
    block_end = map_index + 1

    if block_start <= short_exact_reason_index:
      continue

    dependency_block = paragraphs[
      block_start:
      block_end
    ]

    del paragraphs[
      block_start:
      block_end
    ]

    paragraphs[
      short_exact_reason_index:
      short_exact_reason_index
    ] = dependency_block

  for map_index, paragraph in enumerate(
    tuple(
      paragraphs
    )
  ):
    stripped = paragraph.strip()

    if (
      not stripped.startswith(
        "$H:"
      )
      or " は全射である." not in stripped
      or r"\to " not in stripped
    ):
      continue

    target_fragment = stripped.split(
      r"\to ",
      1,
    )[1].split(
      "$",
      1,
    )[0].strip()

    group_index = next(
      (
        index
        for index in range(
          map_index + 1,
          len(
            paragraphs
          ),
        )
        if paragraphs[
          index
        ].strip().startswith(
          "$"
          + target_fragment
          + " = "
        )
      ),
      None,
    )

    if group_index is None:
      continue

    group_paragraph = paragraphs.pop(
      group_index
    )
    paragraphs.insert(
      map_index,
      group_paragraph,
    )

  return "\n\n".join(
    paragraphs
  )
'''

CONTRIBUTION.write_text(
  text[:start]
  + replacement_surjectivity
  + text[end:],
  encoding="utf-8",
)

print(
  "Applied: map-property support precedes short-exact derivation"
)


old_pipeline = '''  rendered = (
    order_toda_group_proof_narrative_local_equation_derivations(
      rendered
    )
  )

  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
    )
  )
'''

new_pipeline = '''  rendered = (
    order_toda_group_proof_narrative_local_equation_derivations(
      rendered
    )
  )
  rendered = (
    order_toda_group_proof_narrative_order_support(
      presentation,
      rendered,
    )
  )

  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
    )
  )
'''

replace_once(
  CONTRIBUTION,
  old_pipeline,
  new_pipeline,
  "ORDER dependency ordering pipeline call",
)


old_signature_tail = '''  used_step_ids: frozenset[
    int
  ],
) -> tuple[
'''

new_signature_tail = '''  used_step_ids: frozenset[
    int
  ],
  presentation: TodaGroupProofPresentation | None = None,
) -> tuple[
'''

replace_once(
  REFERENCES,
  old_signature_tail,
  new_signature_tail,
  "optional presentation argument for fixed-Reference restoration",
)


old_validation_tail = '''  if not isinstance(
    used_step_ids,
    frozenset,
  ):
    raise TypeError(
      "used_step_ids must be a frozenset"
    )

  retained_reference_keys = {
'''

new_validation_tail = '''  if not isinstance(
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
'''

replace_once(
  REFERENCES,
  old_validation_tail,
  new_validation_tail,
  "presentation validation in fixed-Reference restoration",
)


old_desired_entries = '''  desired_entries = []

  for entry in original_entries:
    has_selected_statement = (
'''

new_desired_entries = '''  reference_internal_step_ids = {
    id(
      proof_step
    )
    for entry in original_entries
    for proof_step in entry.proof_steps
    if proof_step is not root_step
  }
  consumers_by_step_id = {}

  if presentation is not None:
    for edge in presentation.edges:
      consumers_by_step_id.setdefault(
        id(
          edge.premise_step
        ),
        [],
      ).append(
        edge.parent_step
      )

  desired_entries = []

  for entry in original_entries:
    has_selected_statement = (
'''

replace_once(
  REFERENCES,
  old_desired_entries,
  new_desired_entries,
  "consumer map for ancestry-only fixed-Reference pruning",
)


old_used_fixed = '''    is_used_fixed_reference = (
      has_selected_statement
      and any(
        id(
          proof_step
        )
        in used_step_ids
        for proof_step in entry.proof_steps
      )
    )
'''

new_used_fixed = '''    is_used_fixed_reference = (
      has_selected_statement
      and any(
        id(
          proof_step
        )
        in used_step_ids
        and (
          presentation is None
          or any(
            consumer is root_step
            or id(
              consumer
            )
            not in reference_internal_step_ids
            for consumer in consumers_by_step_id.get(
              id(
                proof_step
              ),
              (),
            )
          )
        )
        for proof_step in entry.proof_steps
      )
    )
'''

replace_once(
  REFERENCES,
  old_used_fixed,
  new_used_fixed,
  "do not restore ancestry-only fixed References",
)


old_restore_call = '''        presentation.root_step,
        generic_used_step_ids,
      )
'''

new_restore_call = '''        presentation.root_step,
        generic_used_step_ids,
        presentation=presentation,
      )
'''

replace_once(
  CONTRIBUTION,
  old_restore_call,
  new_restore_call,
  "pass presentation to fixed-Reference restoration",
)


def append_tests() -> None:
  text = R11_TEST.read_text(
    encoding="utf-8"
  )

  additions = []

  if (
    "def test_phase157_r11_r14_eta3_cube_order_follows_injectivity():"
    not in text
  ):
    additions.append(
      r'''


def test_phase157_r11_r14_eta3_cube_order_follows_injectivity():
  _, body = _reference_and_body()

  injectivity = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
  )
  eta_cube_order = (
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$."
  )

  assert injectivity in body
  assert eta_cube_order in body
  assert body.index(
    injectivity
  ) < body.index(
    eta_cube_order
  )
'''
    )

  if (
    "def test_phase157_r11_r14_surjectivity_precedes_short_exact_derivation():"
    not in text
  ):
    additions.append(
      r'''


def test_phase157_r11_r14_surjectivity_precedes_short_exact_derivation():
  _, body = _reference_and_body()

  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である."
  )
  short_exact_reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
  short_exact = (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$."
  )

  assert surjectivity in body
  assert short_exact_reason in body
  assert short_exact in body
  assert body.index(
    surjectivity
  ) < body.index(
    short_exact_reason
  )
  assert body.index(
    surjectivity
  ) < body.index(
    short_exact
  )
'''
    )

  if (
    "def test_phase157_r11_r14_ancestry_only_reference_is_not_public():"
    not in text
  ):
    additions.append(
      r'''


def test_phase157_r11_r14_ancestry_only_reference_is_not_public():
  reference, body = _reference_and_body()

  assert "**[R3] Proposition 5.3.**" not in reference
  assert "[R3]" not in body
'''
    )

  if additions:
    R11_TEST.write_text(
      text.rstrip()
      + "".join(additions)
      + "\n",
      encoding="utf-8",
    )
    print(
      "Added: R11-R14 dependency/reference regression tests"
    )
  else:
    print(
      "Already applied: R11-R14 regression tests"
    )


append_tests()

print("")
print("Phase157 R11-R14 patch applied successfully.")
