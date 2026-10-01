Phase 154-R5 Fix1 — Graph-backed Reference linkage implementation

変更対象
--------
1. toda_group_proof_narrative_contribution_renderer.py
   - 追加:
     _phase154_r5_selected_reference_steps_by_number()
     _phase154_r5_unique_visible_non_root_consumer_line()
     link_toda_group_proof_narrative_reference_body_consumers()
   - 変更:
     render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

2. tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py
   - 新規追加

import の変更
-------------
なし。

追加位置
--------
3つの helper は
suppress_toda_group_proof_narrative_reference_body_duplicates()
の直前に追加する。

一般規則
--------
- Reference の selected step を Proof graph から取得する。
- selected step から descendants を距離順にたどる。
- public body に実際に現れる non-root consumer を探す。
- 最短距離に visible consumer が一意に1つだけ存在するときだけ、
  neutral reference-use sentence と consumer sentence を結合する。
- root のみ、visible consumer が複数、marker/consumer の位置が曖昧、
  consumer が Reference より前にある場合は変更しない。
- pi11_4 固有分岐は設けない。

期待する pi11_4 の変化
----------------------
変更前:

  まず、[R2]を用いる。
  このことから、$\nu_{4}$ の分解写像は同型写像である.

変更後:

  [R2]より、$\nu_{4}$ の分解写像は同型写像である.

[R1] は visible non-root consumer が一意に取れず root 結論へ直接つながるので、
中立な [R1]を用いる。表現を維持する。

追加 helper 全文
----------------
def _phase154_r5_selected_reference_steps_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    ProofStep,
    ...,
  ],
]:
  selected_by_number = {}

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    if selected_steps:
      selected_by_number[
        entry.number
      ] = selected_steps

  return selected_by_number


def _phase154_r5_unique_visible_non_root_consumer_line(
  presentation: TodaGroupProofPresentation,
  source_steps: tuple[
    ProofStep,
    ...,
  ],
  body_markdown: str,
) -> str | None:
  if not source_steps:
    return None

  children_by_step_id = {}

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
      source_step,
      0,
    )
    for source_step in source_steps
  )
  visited_step_ids = {
    id(
      source_step
    )
    for source_step in source_steps
  }
  visible_by_distance = {}

  while queue:
    current_step, distance = queue.popleft()

    for child_step in children_by_step_id.get(
      id(
        current_step
      ),
      (),
    ):
      child_step_id = id(
        child_step
      )

      if child_step_id in visited_step_ids:
        continue

      visited_step_ids.add(
        child_step_id
      )
      child_distance = distance + 1

      if child_step is presentation.root_step:
        continue

      rendered_child = (
        _render_generic_narrative_step(
          child_step
        )
      )

      if (
        rendered_child
        and rendered_child in body_markdown
      ):
        visible_by_distance.setdefault(
          child_distance,
          [],
        ).append(
          rendered_child
        )
        continue

      queue.append(
        (
          child_step,
          child_distance,
        )
      )

  if not visible_by_distance:
    return None

  nearest_distance = min(
    visible_by_distance
  )
  nearest_lines = tuple(
    dict.fromkeys(
      visible_by_distance[
        nearest_distance
      ]
    )
  )

  if len(
    nearest_lines
  ) != 1:
    return None

  return nearest_lines[
    0
  ]


def link_toda_group_proof_narrative_reference_body_consumers(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  selected_by_number = (
    _phase154_r5_selected_reference_steps_by_number(
      presentation,
      reference_entries,
    )
  )
  lines = body_markdown.splitlines()

  for reference_number, selected_steps in (
    selected_by_number.items()
  ):
    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    marker_indices = tuple(
      index
      for index, line in enumerate(
        lines
      )
      if (
        marker in line
        and line.rstrip().endswith(
          marker
          + "を用いる。"
        )
      )
    )

    if len(
      marker_indices
    ) != 1:
      continue

    current_body = "\n".join(
      lines
    )
    consumer_line = (
      _phase154_r5_unique_visible_non_root_consumer_line(
        presentation,
        selected_steps,
        current_body,
      )
    )

    if consumer_line is None:
      continue

    consumer_indices = tuple(
      index
      for index, line in enumerate(
        lines
      )
      if (
        index != marker_indices[0]
        and consumer_line in line
      )
    )

    if len(
      consumer_indices
    ) != 1:
      continue

    marker_index = marker_indices[
      0
    ]
    consumer_index = consumer_indices[
      0
    ]

    if consumer_index <= marker_index:
      continue

    lines[
      marker_index
    ] = (
      marker
      + "より、"
      + consumer_line
    )
    del lines[
      consumer_index
    ]

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()


変更関数全文
------------
def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> str:
  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )
  contribution_markdown = (
    _insert_toda_group_proof_narrative_argument_contributions(
      presentation,
      base_markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  rendered = (
    insert_toda_group_proof_narrative_reason_prose(
      contribution_markdown,
      reason_sidecar,
    )
  )
  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
      presentation.root_step,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      rendered,
      statement_lines_by_reference_number,
    )
  )
  rendered = (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )
  if "[R" in rendered:
    (
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
  else:
    generic_used_step_ids = (
      build_toda_group_proof_narrative_generic_used_step_ids(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        ordered_contributions,
      )
    )
    (
      reference_entries,
      statement_lines_by_reference_number,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        reference_entries,
        statement_lines_by_reference_number,
        generic_used_step_ids,
        presentation.root_step,
      )
    )

  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  if not reference_section:
    return rendered

  return (
    reference_section
    + "\n\n"
    + rendered
  )


テスト全文
----------
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  link_toda_group_proof_narrative_reference_body_consumers,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _presentation(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
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


def _render_group(
  n: int,
  k: int,
) -> str:
  return render_toda_group_proof_narrative_markdown(
    _presentation(
      n,
      k,
    )
  )


def test_phase154_r5_fix1_pi11_4_links_prop44_reference_to_visible_consumer():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    r"[R2]より、$\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert "まず、[R2]を用いる。" not in rendered
  assert (
    r"このことから、$\nu_{4}$ の分解写像は同型写像である."
    not in rendered
  )
  assert r"\pi_{11}^{4} = 0" in rendered


def test_phase154_r5_fix1_pi11_4_keeps_root_only_reference_neutral():
  rendered = _render_group(
    4,
    7,
  )

  assert "[R1]を用いる。" in rendered
  assert r"[R1]より、$\pi_{11}^{4} = 0" not in rendered


def test_phase154_r5_fix1_does_not_duplicate_linked_consumer_fact():
  rendered = _render_group(
    4,
    7,
  )
  consumer = (
    r"$\nu_{4}$ の分解写像は同型写像である."
  )

  assert rendered.count(
    consumer
  ) == 1


def test_phase154_r5_fix1_linkage_helper_keeps_ambiguous_or_missing_marker_body():
  raw_presentation = _presentation(
    4,
    7,
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  body = (
    "参照記号を含まない本文。\n"
    r"$\nu_{4}$ の分解写像は同型写像である."
  )

  assert (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      body,
      entries,
    )
    == body
  )


def test_phase154_r5_fix1_keeps_r2_internal_fallback_repairs():
  pi10_4 = _render_group(
    4,
    6,
  )
  pi11_4 = _render_group(
    4,
    7,
  )

  assert (
    "Toda (5.6) nu_4 decomposition integration"
    not in pi10_4
  )
  assert r"\text{ is injective}" not in pi11_4
  assert r"\text{ is exact}" not in pi11_4
  assert "である.を用いる。" not in pi11_4


実行する pytest
---------------
- tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py
- tests/test_phase154_r4_semantic_duplication_transition_refinement.py
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase153_r8_reference_use_prose_normalization.py

全体テスト
----------
実行しない。Phase 154 の最後まで保留。

完了条件
--------
1. pi11_4 public Narrative で public [R2] と nu4 decomposition isomorphism が1文に結合される。
2. consumer fact が二重表示されない。
3. root-only の public [R1] は中立表現を維持する。
4. R2/R4 の focused contract を壊さない。
5. focused tests が PASS。
6. pi11_4 representative check が PASS。

次 Phase との境界
-----------------
Fix1 後に代表群を再監査する。
Reference linkage の残存問題がなければ R5 完了として R6 punctuation normalization へ進む。
