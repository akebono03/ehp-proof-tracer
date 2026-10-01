Phase 154-R5 Fix1 Repair1 — Reference entry frontier linkage

失敗原因
--------
Fix1 は selected Reference step だけを探索起点にしたが、
pi11_4 の public Narrative では、その selected step から
visible consumer を文字列として回収できず linkage が発火しなかった。

Repair1
-------
Reference ownership を広げず、同じ Reference entry に属する proof steps 全体を
graph frontier として探索起点にする。

一般規則:
- selected steps を先頭に置く。
- 同じ Reference entry の proof steps を追加する。
- Reference entry 外へ出た descendant だけを consumer 候補とする。
- public body に実際に表示される non-root consumer を距離順に探す。
- 最短距離の visible consumer が一意な場合だけ結合する。
- root-only / 複数候補 / consumer が marker より前なら中立文を維持する。
- pi11_4 固有分岐はない。

変更対象
--------
toda_group_proof_narrative_contribution_renderer.py

置換する helper 全文
--------------------
def _phase154_r5_reference_source_steps_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    ProofStep,
    ...,
  ],
]:
  source_steps_by_number = {}

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not rendered_statement:
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

    ordered_source_steps = []
    seen_step_ids = set()

    for proof_step in (
      *selected_steps,
      *entry.proof_steps,
    ):
      proof_step_id = id(
        proof_step
      )

      if proof_step_id in seen_step_ids:
        continue

      seen_step_ids.add(
        proof_step_id
      )
      ordered_source_steps.append(
        proof_step
      )

    if ordered_source_steps:
      source_steps_by_number[
        entry.number
      ] = tuple(
        ordered_source_steps
      )

  return source_steps_by_number


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

  source_step_ids = {
    id(
      source_step
    )
    for source_step in source_steps
  }
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
  visited_distance_by_step_id = {}
  visible_by_distance = {}

  while queue:
    current_step, distance = queue.popleft()
    current_step_id = id(
      current_step
    )
    known_distance = visited_distance_by_step_id.get(
      current_step_id
    )

    if (
      known_distance is not None
      and known_distance <= distance
    ):
      continue

    visited_distance_by_step_id[
      current_step_id
    ] = distance

    for child_step in children_by_step_id.get(
      current_step_id,
      (),
    ):
      child_step_id = id(
        child_step
      )
      child_distance = distance + 1

      if child_step_id in source_step_ids:
        queue.append(
          (
            child_step,
            child_distance,
          )
        )
        continue

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

  source_steps_by_number = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      reference_entries,
    )
  )
  lines = body_markdown.splitlines()

  for reference_number, source_steps in (
    source_steps_by_number.items()
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
        source_steps,
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


import の変更
-------------
なし。

新規テスト
----------
tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py

テスト全文
----------
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _phase154_r5_reference_source_steps_by_number,
  _phase154_r5_unique_visible_non_root_consumer_line,
  link_toda_group_proof_narrative_reference_body_consumers,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
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


def _raw_presentation(
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
    _raw_presentation(
      n,
      k,
    )
  )


def test_phase154_r5_fix1_repair1_pi11_4_links_prop44_reference_to_consumer():
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


def test_phase154_r5_fix1_repair1_consumer_is_unique_and_non_root():
  raw_presentation = _raw_presentation(
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
  statement_lines = {
    entry.number: tuple(
      ()
    )
    for entry in entries
  }
  entries, _ = (
    exclude_toda_group_proof_narrative_root_reference(
      entries,
      statement_lines,
      presentation.root_step,
    )
  )
  sources = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      entries,
    )
  )
  body = (
    "まず、[R3]を用いる。\n"
    r"このことから、$\nu_{4}$ の分解写像は同型写像である."
    "\n"
    r"$\pi_{11}^{4} = 0$"
  )

  assert (
    _phase154_r5_unique_visible_non_root_consumer_line(
      presentation,
      sources[3],
      body,
    )
    == r"$\nu_{4}$ の分解写像は同型写像である."
  )


def test_phase154_r5_fix1_repair1_keeps_root_only_reference_neutral():
  rendered = _render_group(
    4,
    7,
  )

  assert "[R1]を用いる。" in rendered
  assert r"[R1]より、$\pi_{11}^{4} = 0" not in rendered


def test_phase154_r5_fix1_repair1_does_not_duplicate_consumer_fact():
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


def test_phase154_r5_fix1_repair1_preserves_final_conclusion():
  rendered = _render_group(
    4,
    7,
  )

  assert r"\pi_{11}^{4} = 0" in rendered


focused pytest
--------------
- tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py
- tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py
- tests/test_phase154_r4_semantic_duplication_transition_refinement.py
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase153_r8_reference_use_prose_normalization.py

完了条件
--------
1. public pi11_4 に `[R2]より、$\nu_{4}$ の分解写像は同型写像である.` が出る。
2. `まず、[R2]を用いる。` が消える。
3. consumer fact は1回だけ。
4. [R1] root-only linkage は中立のまま。
5. final conclusion を維持。
6. focused tests PASS。

全体テスト
----------
実行しない。Phase 154 最後まで保留。
