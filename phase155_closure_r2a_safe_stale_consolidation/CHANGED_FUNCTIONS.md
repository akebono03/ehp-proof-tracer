# Phase 155 Closure-R2A changed functions

Import changes: none.

Production changes: none.

Only the following 38 existing test functions are replaced.

## `tests/test_phase132_6_group_proof_narrative_renderer.py`

### `test_phase132_6_sigma_family_statements_use_readable_labels`

```python
def test_phase132_6_sigma_family_statements_use_readable_labels():
  data = build_phase132_6_sigma9_narrative(
    max_depth=1,
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  root_edges = tuple(
    edge
    for edge in presentation.edges
    if edge.parent_step is presentation.root_step
  )

  target_type_names = {
    "Toda48Pi16_9OrderAndE4InjectiveStatement",
    "TodaLemma514Sigma8Statement",
    "TodaSigmaFamilyDefinitionStatement",
  }

  labelled_steps = tuple(
    edge.premise_step
    for edge in root_edges
    if (
      type(
        edge.premise_step.conclusion
      ).__name__
      in target_type_names
    )
  )

  assert {
    type(
      step.conclusion
    ).__name__
    for step in labelled_steps
  } == target_type_names

  assert r"\pi_{16}^{9}" in rendered
  assert r"\mathbb{Z}/16" in rendered

  for step in labelled_steps:
    type_name = type(
      step.conclusion
    ).__name__

    assert type_name not in rendered

    if step.inference_rule is not None:
      assert (
        step.inference_rule.name
        not in rendered
      )
```

## `tests/test_phase132_8_group_proof_narrative_dedup.py`

### `test_phase132_8_shared_dependency_subtree_is_expanded_once`

```python
def test_phase132_8_shared_dependency_subtree_is_expanded_once():
  data = build_phase132_8_sigma9_narrative(
    max_depth=2,
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  counts = _incoming_use_count_by_step_id(
    presentation
  )

  shared_parent = next(
    node.proof_step
    for node in presentation.nodes
    if (
      counts[
        id(
          node.proof_step
        )
      ]
      > 1
      and any(
        edge.parent_step
        is node.proof_step
        for edge in presentation.edges
      )
      and node.proof_step
      is not presentation.root_step
    )
  )

  parent_fact = _render_group_proof_narrative_fact(
    shared_parent
  )

  assert parent_fact
  assert rendered.count(
    "Lemma 5.14.**"
  ) == 1
```

### `test_phase132_8_repeated_shared_dependency_uses_existing_reference`

```python
def test_phase132_8_repeated_shared_dependency_uses_existing_reference():
  data = build_phase132_8_sigma9_narrative(
    max_depth=2,
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  counts = _incoming_use_count_by_step_id(
    presentation
  )

  shared_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if counts[
      id(
        node.proof_step
      )
    ] > 1
  )

  assert shared_steps
  assert "[R1]" in rendered
  assert rendered.count(
    "Lemma 5.14.**"
  ) == 1
```

### `test_phase132_8_root_conclusion_and_source_remain_unchanged`

```python
def test_phase132_8_root_conclusion_and_source_remain_unchanged():
  data = build_phase132_8_sigma9_narrative(
    max_depth=2,
  )

  rendered = data[
    "rendered"
  ]

  assert "Lemma 5.14" in rendered
  assert r"\pi_{16}^{9}" in rendered
  assert r"\mathbb{Z}/16" in rendered
```

### `test_phase132_8_cli_narrative_uses_deduplicated_renderer`

```python
def test_phase132_8_cli_narrative_uses_deduplicated_renderer(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"\pi_{16}^{9}" in captured.out
  assert r"\mathbb{Z}/16" in captured.out
  assert captured.out.count(
    "Lemma 5.14.**"
  ) == 1
```

## `tests/test_phase133_10_sigma_label_wording.py`

### `test_phase133_10_sigma9_depth_two_uses_final_japanese_wording`

```python
def test_phase133_10_sigma9_depth_two_uses_final_japanese_wording(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "Lemma 5.14" in captured.out
  assert r"\pi_{16}^{9}" in captured.out
  assert r"\mathbb{Z}/16" in captured.out

  assert (
    "Theorem 3.6 から Lemma 5.14 への σ″ bridge"
    not in captured.out
  )
  assert (
    "Toda Lemma 5.14 の σ′ branch"
    not in captured.out
  )
```

## `tests/test_phase133_6_group_proof_narrative_labels.py`

### `test_phase133_6_pi10_4_uses_readable_nu4_decomposition_label`

```python
def test_phase133_6_pi10_4_uses_readable_nu4_decomposition_label(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "4",
      "6",
      "--depth",
      "1",
      "--mode",
      "narrative",
    ]
  )
  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"\pi_{10}^{4}" in captured.out
  assert r"\mathbb{Z}/8" in captured.out
  assert (
    "Toda Proposition 5.6 finite-dimensional integration"
    not in captured.out
  )
  assert (
    "Toda (5.6) nu_4 decomposition isomorphism semantics"
    not in captured.out
  )
```

### `test_phase133_6_pi12_5_uses_readable_sigma_triple_prime_labels`

```python
def test_phase133_6_pi12_5_uses_readable_sigma_triple_prime_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "5",
      "7",
      "--depth",
      "1",
      "--mode",
      "narrative",
    ]
  )
  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"\pi_{12}^{5}" in captured.out
  assert r"\mathbb{Z}/2" in captured.out
  assert (
    "Toda Lemma 5.13 sigma triple-prime definition"
    not in captured.out
  )
```

### `test_phase133_6_sigma9_depth_two_reuses_new_labels`

```python
def test_phase133_6_sigma9_depth_two_reuses_new_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )
  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"\pi_{12}^{5}" in captured.out
  assert r"\mathbb{Z}/2" in captured.out
  assert r"\mathbb{Z}/16" in captured.out
  assert "Lemma 5.14" in captured.out
```

## `tests/test_phase133_9_group_proof_narrative_labels.py`

### `test_phase133_9_pi10_4_depth_two_uses_final_readable_labels`

```python
def test_phase133_9_pi10_4_depth_two_uses_final_readable_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "4",
      "6",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"\pi_{10}^{4}" in captured.out
  assert r"\mathbb{Z}/8" in captured.out

  internal_names = (
    "Toda Proposition 5.6 finite-dimensional integration",
    "Toda (5.6) nu_4 decomposition isomorphism semantics",
    "Toda Lemma 5.4 integration",
  )

  for internal_name in internal_names:
    assert internal_name not in captured.out
```

### `test_phase133_9_pi16_9_depth_two_uses_final_sigma_labels`

```python
def test_phase133_9_pi16_9_depth_two_uses_final_sigma_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "Lemma 5.14" in captured.out
  assert r"\mathbb{Z}/16" in captured.out

  internal_names = (
    "Toda Theorem 3.6 Lemma 5.14 sigma double-prime bridge",
    "Toda Lemma 5.14 sigma-prime branch",
  )

  for internal_name in internal_names:
    assert internal_name not in captured.out
```

### `test_phase133_9_previous_labels_remain_available`

```python
def test_phase133_9_previous_labels_remain_available(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "5",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"\pi_{12}^{5}" in captured.out
  assert r"\mathbb{Z}/2" in captured.out
  assert "Lemma 5.13" in captured.out
```

## `tests/test_phase143_44_single_argument_narrative_renderer.py`

### `test_phase143_44_pi6_3_order_combines_header_method_and_body`

```python
def test_phase143_44_pi6_3_order_combines_header_method_and_body():
  (
    _argument,
    primary_component,
    rendered,
  ) = _single_argument_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .MIDDLE,
  )

  assert primary_component is not None
  assert (
    r"\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}"
    in rendered
  )
  assert (
    r"\operatorname{ord}\left(\nu'\right) = 4"
    in rendered
  )
```

### `test_phase143_44_pi6_3_definition_without_primary_has_no_method_transition`

```python
def test_phase143_44_pi6_3_definition_without_primary_has_no_method_transition():
  (
    _argument,
    primary_component,
    rendered,
  ) = _single_argument_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .FIRST,
  )

  assert primary_component is None
  assert r"$\nu'$" in rendered
  assert r"\nu' \in " in rendered
  assert "次の完全列を考える" not in rendered
```

### `test_phase143_44_pi8_5_detached_order_has_no_discourse_marker`

```python
def test_phase143_44_pi8_5_detached_order_has_no_discourse_marker():
  (
    _argument,
    primary_component,
    rendered,
  ) = _single_argument_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .DETACHED,
    occurrence=1,
  )

  assert primary_component is not None
  assert r"$\nu'$" in rendered
  assert not rendered.startswith(
    "まず"
  )
  assert not rendered.startswith(
    "次に"
  )
  assert not rendered.startswith(
    "最後に"
  )
```

## `tests/test_phase143_46_multi_argument_narrative_assembler.py`

### `test_phase143_46_pi6_3_assembles_three_main_arguments`

```python
def test_phase143_46_pi6_3_assembles_three_main_arguments():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert r"$\nu'$" in rendered
  assert (
    r"\operatorname{ord}\left(\nu'\right) = 4"
    in rendered
  )
  assert r"\pi_{6}^{3}" in rendered
  assert r"\mathbb{Z}/4" in rendered
```

### `test_phase143_46_pi16_9_assembles_definition_then_group_structure`

```python
def test_phase143_46_pi16_9_assembles_definition_then_group_structure():
  rendered = _render_multi_argument(
    9,
    7,
  )

  assert r"\sigma_{9}" in rendered
  assert r"\pi_{16}^{9}" in rendered
  assert r"\mathbb{Z}/16" in rendered
```

## `tests/test_phase143_61b_direct_premise_narrative.py`

### `test_phase143_61b_pi8_5_places_direct_derivation_premises_together`

```python
def test_phase143_61b_pi8_5_places_direct_derivation_premises_together():
  rendered = _render(
    5,
    3,
  )

  double_relation = (
    r"$2\nu_{5} = E^{2}\nu'$"
  )
  e2_order = (
    r"$\operatorname{ord}\left(E^{2}\nu'\right) = 4$"
  )
  conclusion = (
    r"$\operatorname{ord}\left(\nu_{5}\right) = 8$"
  )

  assert rendered.count(
    double_relation
  ) == 1
  assert rendered.count(
    e2_order
  ) == 1
  assert (
    rendered.index(
      double_relation
    )
    < rendered.index(
      e2_order
    )
    < rendered.index(
      conclusion
    )
  )
```

### `test_phase143_61b_pi6_3_keeps_local_calculation_derivation`

```python
def test_phase143_61b_pi6_3_keeps_local_calculation_derivation():
  rendered = _render(
    3,
    3,
  )

  source_one = (
    r"$2\nu' = \eta_{3}E\eta_{3}\eta_{5}\tag{1}$"
  )
  source_two = (
    r"$\eta_{3}E\eta_{3}\eta_{5} = \eta_{3}^{3}\tag{2}$"
  )
  target = (
    r"$2\nu' = \eta_{3}^{3}\tag{3}$"
  )

  assert (
    rendered.index(
      source_one
    )
    < rendered.index(
      source_two
    )
    < rendered.index(
      target
    )
  )
```

## `tests/test_phase143_74b_remaining_internal_narrative.py`

### `test_phase143_74b_prop44_isomorphism_renders_decomposition_semantics`

```python
def test_phase143_74b_prop44_isomorphism_renders_decomposition_semantics():
  beta = HomotopyElement(
    name="beta",
    dimension=6,
  )
  gamma = HomotopyElement(
    name="gamma",
    dimension=6,
  )
  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=gamma,
  )
  decomposition_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(),
    ),
    target_group=TodaPrimaryGroup(7, 4),
    alpha=beta,
    beta=beta,
    gamma=gamma,
    formula=formula,
  )

  rendered = _render_group_proof_narrative_fact(
    _step(
      TodaProp44IsomorphismStatement(
        map=decomposition_map,
      )
    )
  )

  assert "TodaProp44IsomorphismStatement" not in rendered
  assert r"\mapsto" in rendered
  assert "同型写像" in rendered
```

### `test_phase143_74b_suspension_isomorphism_renders_semantic_map`

```python
def test_phase143_74b_suspension_isomorphism_renders_semantic_map():
  rendered = _render_group_proof_narrative_fact(
    _step(
      TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
          source_group=TodaPrimaryGroup(6, 4),
          target_group=TodaPrimaryGroup(7, 5),
        )
      )
    )
  )

  assert r"$E: \pi_{6}^{4}" in rendered
  assert r"\pi_{7}^{5}$" in rendered
  assert "同型写像" in rendered
  assert "TodaSuspensionIsomorphismStatement" not in rendered
```

## `tests/test_phase143_75c_generic_semantic_rendering.py`

### `test_phase143_75c_renders_toda45_isomorphism_semantically`

```python
def test_phase143_75c_renders_toda45_isomorphism_semantically():
  proof_step = _find_production_step(
    n=4,
    k=1,
    statement_type=Toda45IsomorphismStatement,
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert rendered.startswith(
    "$E^{"
  )
  assert r"\to" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
```

### `test_phase143_75c_renders_hopf_isomorphism_semantically`

```python
def test_phase143_75c_renders_hopf_isomorphism_semantically():
  proof_step = _find_production_step(
    n=2,
    k=1,
    statement_type=(
      TodaHopfInvariantIsomorphismStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert rendered.startswith(
    "$H: "
  )
  assert r"\to" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
```

### `test_phase143_75c_renders_prop44_second_summand_semantically`

```python
def test_phase143_75c_renders_prop44_second_summand_semantically():
  proof_step = _find_production_step(
    n=2,
    k=2,
    statement_type=(
      TodaProp44SecondSummandRestrictionStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert r"\eta_{2}" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
  assert (
    type(
      proof_step.conclusion
    ).__name__
    not in rendered
  )
```

## `tests/test_phase143_75f_ehp_semantic_rendering.py`

### `test_phase143_75f_renders_delta_surjective_semantically`

```python
def test_phase143_75f_renders_delta_surjective_semantically():
  proof_step = _find_production_step(
    n=3,
    k=5,
    statement_type=TodaDeltaSurjectiveStatement,
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert r"\Delta:" in rendered
  assert r"\to" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
```

### `test_phase143_75f_renders_delta_kernel_semantically`

```python
def test_phase143_75f_renders_delta_kernel_semantically():
  proof_step = _find_production_step(
    n=6,
    k=5,
    statement_type=(
      TodaDeltaKernelFreeCyclicStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert r"\ker\Delta" in rendered
  assert r"\mathbb{Z}\{" in rendered
  assert r"\iota_{11}" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
```

## `tests/test_phase143_75i_whitehead_hopf_semantic_rendering.py`

### `test_phase143_75i_renders_prop27_whitehead_argument_semantically`

```python
def test_phase143_75i_renders_prop27_whitehead_argument_semantically():
  proof_step = _find_production_step(
    n=3,
    k=1,
    statement_type=(
      TodaProp27HopfInvariantUpToSignStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert (
    r"$H([\iota_{2}, \iota_{2}])"
    r" = \pm 2\iota_{3}$"
    in rendered
  )
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
```

### `test_phase143_75i_renders_prop27_map_application_semantically`

```python
def test_phase143_75i_renders_prop27_map_application_semantically():
  proof_step = _find_production_step(
    n=6,
    k=5,
    statement_type=(
      TodaProp27HopfInvariantUpToSignStatement
    ),
    predicate=lambda statement: (
      type(
        statement.argument
      ).__name__
      == "MapApplication"
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert rendered.startswith(
    r"$H(\Delta\left("
  )
  assert r" = \pm " in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
```

### `test_phase143_75i_renders_58_whitehead_square_semantically`

```python
def test_phase143_75i_renders_58_whitehead_square_semantically():
  proof_step = _find_production_step(
    n=5,
    k=4,
    statement_type=(
      Toda58WhiteheadSquareUpToSignStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert (
    r"$[\iota_{4}, \iota_{4}]"
    in rendered
  )
  assert r" = \pm " in rendered
  assert r"2\nu_{4}" in rendered
  assert r"E\nu'" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
```

## `tests/test_phase143_75p_prop44_suspension_injective_semantic_rendering.py`

### `test_phase143_75p_all_target_occurrences_render_semantically`

```python
def test_phase143_75p_all_target_occurrences_render_semantically():
  steps = _target_steps()

  assert len(
    steps
  ) >= 55

  for step in steps:
    rendered = _render_group_proof_narrative_fact(
      step
    )
    assert rendered.startswith(
      "$E: "
    )
    assert r" \to " in rendered
    assert rendered != step.inference_rule.name
```

### `test_phase143_75p_both_rule_families_use_same_semantic_renderer`

```python
def test_phase143_75p_both_rule_families_use_same_semantic_renderer():
  steps = _target_steps()

  rule_counts = Counter(
    step.inference_rule.name
    for step in steps
  )

  assert (
    "Toda Proposition 5.3 n=4 "
    "Phase 48 injectivity bridge"
    in rule_counts
  )
  assert (
    "Toda Proposition 4.4 "
    "suspension injectivity"
    in rule_counts
  )
  assert all(
    count > 0
    for count in rule_counts.values()
  )

  for step in steps:
    rendered = _render_group_proof_narrative_fact(
      step
    )
    assert "Proposition" not in rendered
    assert "injectivity" not in rendered
```

### `test_phase143_75p_concrete_map_uses_source_and_target_groups`

```python
def test_phase143_75p_concrete_map_uses_source_and_target_groups():
  steps = _target_steps()

  concrete = next(
    step
    for step in steps
    if (
      repr(step.conclusion.map.source_group)
      == (
        "TodaPrimaryGroup("
        "group_dimension=5, "
        "sphere_dimension=3)"
      )
      and repr(step.conclusion.map.target_group)
      == (
        "TodaPrimaryGroup("
        "group_dimension=6, "
        "sphere_dimension=4)"
      )
    )
  )

  rendered = _render_group_proof_narrative_fact(
    concrete
  )

  assert r"$E: \pi_{5}^{3}" in rendered
  assert r"\pi_{6}^{4}$" in rendered
  assert concrete.inference_rule.name not in rendered
```

## `tests/test_phase143_75s_toda58_whitehead_square_semantic_rendering.py`

### `test_phase143_75s_all_aggregate_components_render_semantically`

```python
def test_phase143_75s_all_aggregate_components_render_semantically():
  statements = _target_statements()

  assert len(
    statements
  ) >= 45

  rendered = tuple(
    render_toda_proof_statement_latex(
      statement
    )
    for statement in statements
  )

  assert all(
    value is not None
    for value in rendered
  )

  assert all(
    type(
      statement
    ).__name__
    == "Toda58WhiteheadSquareUpToSignStatement"
    for statement in statements
  )
```

## `tests/test_phase150_rc4_5b_3_r1_beta_latex.py`

### `test_phase150_rc4_5b_3_r1_beta_uses_general_greek_latex_table`

```python
def test_phase150_rc4_5b_3_r1_beta_uses_general_greek_latex_table():
  beta = HomotopyElement(
    name="β",
    dimension=3,
    source=6,
    target=3,
  )

  assert render_toda_expression_latex(
    beta
  ) == r"\beta"
```

## `tests/test_phase150_rc4_7a_cross_group_reference_normalization.py`

### `test_phase150_rc4_7a_pi10_4_numbers_normalized_references`

```python
def test_phase150_rc4_7a_pi10_4_numbers_normalized_references(
):
  rendered = _render_group(
    4,
    6,
  )

  assert "使用する結果を先にまとめる." in rendered
  assert "[R1]" in rendered
  assert r"\pi_{10}^{4}" in rendered
  assert r"\mathbb{Z}/8" in rendered
```

### `test_phase150_rc4_7a_pi12_5_numbers_normalized_references`

```python
def test_phase150_rc4_7a_pi12_5_numbers_normalized_references(
):
  rendered = _render_group(
    5,
    7,
  )

  assert "使用する結果を先にまとめる." in rendered
  assert "[R1]" in rendered
  assert r"\pi_{12}^{5}" in rendered
  assert r"\mathbb{Z}/2" in rendered
```

## `tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py`

### `test_phase150_rc4_7d_3_pi10_public_and_web_use_generic_reason_route`

```python
def test_phase150_rc4_7d_3_pi10_public_and_web_use_generic_reason_route():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(
      4,
      6,
    )
  )
  web_text = _web_text(
    4,
    6,
  )

  assert "以上で得た群構造" in markdown
  assert "結果を合わせると" in markdown
  assert "以上で得た群構造" in web_text
  assert "結果を合わせると" in web_text
```

### `test_phase150_rc4_7d_3_pi12_public_and_web_use_generic_reason_route`

```python
def test_phase150_rc4_7d_3_pi12_public_and_web_use_generic_reason_route():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(
      5,
      7,
    )
  )
  web_text = _web_text(
    5,
    7,
  )

  assert "この完全性" in markdown
  assert "結果を合わせると" in markdown
  assert "この完全性" in web_text
  assert "結果を合わせると" in web_text
```
