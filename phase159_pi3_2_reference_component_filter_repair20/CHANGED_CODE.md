# Phase 159 $\pi_3^2$ Reference component-filter repair20

## 変更対象

- `toda_group_proof_narrative_references.py`
  - `filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary()`
- `toda_group_proof_narrative_contribution_renderer.py`
  - `_phase157_r20_canonical_fixed_reference_line()`
- `toda_group_proof_narrative_renderer.py`
  - `render_toda_group_proof_narrative_markdown()` の repair19 wrapper のみ除去
- `tests/test_phase159_r1_6c_source_faithful_reference_linkage.py`
  - `test_phase159_r1_6c_toda_51_reference_is_source_faithful()`

import の変更はありません。

## `filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary()` 全文

```python
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

      if not (
        component
        .range_is_explicit_in_current_aggregate
      ):
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

  retained_entries = sorted(
    retained_entries,
    key=lambda entry: (
      0
      if entry.reference.locator
      == "(5.1)"
      else 1
    ),
  )

  return tuple(
    replace(
      entry,
      number=number,
    )
    for number, entry in enumerate(
      retained_entries,
      start=1,
    )
  )
```

## `_phase157_r20_canonical_fixed_reference_line()` 全文

```python
def _phase157_r20_canonical_fixed_reference_line(
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if (
    boundary is not None
    and boundary.reference_locator
    == "(5.1)"
    and boundary.component_key
    == "circle_higher_homotopy_zero"
  ):
    return (
      r"$\pi_{i}^{1} = 0\ (i > 1)$."
    )

  if (
    boundary is not None
    and boundary.reference_locator
    == "(5.1)"
    and boundary.component_key
    == "sphere_connectivity_zero"
  ):
    return (
      r"$\pi_{i}^{n} = 0\ (i < n)$."
    )

  if (
    boundary is not None
    and boundary.reference_locator
    == "(5.1)"
    and boundary.component_key
    == "diagonal_identity_group"
  ):
    return (
      r"$\pi_{n}^{n} = "
      r"\mathbb{Z}\{\iota_{n}\}$."
    )

  if (
    boundary is not None
    and boundary.component_key
    == "hopf_right_composition_formula"
  ):
    return (
      r"$H(\alpha\circ E\beta)"
      r" = H(\alpha)\circ E\beta$."
    )

  return rendered_statement
```

## `render_toda_group_proof_narrative_markdown()`

この関数は repair18 後のローカル内容をそのまま保持します。

repair19 が付加した最終

```python
_phase159_r1_6c_canonicalize_toda_51_reference(...)
```

wrapper だけを AST で取り除き、repair19 適用前の最終返値へ戻します。

したがって repair18 の ordering / locality 処理は変更しません。

## テスト関数全文

```python
def test_phase159_r1_6c_toda_51_reference_is_source_faithful():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6c_pi3_2_presentation()
    )
  )
  reference = (
    rendered.split(
      "## 使用する結果\n\n",
      1,
    )[1].split(
      "\n---\n",
      1,
    )[0]
  )

  assert "**[R1] (5.1).**" in reference
  assert (
    r"$\pi_{i}^{1} = 0\ (i > 1)$."
    in reference
  )
  assert (
    r"$\pi_{n}^{n} = "
    r"\mathbb{Z}\{\iota_{n}\}$."
    in reference
  )

  assert (
    r"$\pi_{i}^{n} = 0\ (i < n)$."
    not in reference
  )
  assert r"\langle" not in reference
  assert r"\rangle" not in reference
  assert r"\pi_{2}^{1} = 0" not in reference
  assert r"\pi_{3}^{3}" not in reference
  assert (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$"
    not in reference
  )
```

## 変更一覧

1. fixed-statement component の既存 metadata
   `range_is_explicit_in_current_aggregate`
   を Reference filter で使用する。
2. `(5.1)` の一般形は selected component ごとに描画する。
3. repair19 の「(5.1) 全文を後から固定挿入する」処理を public renderer から外す。
4. $\pi_3^2$ では未使用の
   $\pi_i^n=0\ (i<n)$
   を Reference に表示しない。
5. proof body と repair18 の順序制御は変更しない。

## 実行する pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py::test_phase159_r1_6c_toda_51_reference_is_source_faithful" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py::test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry"
```

加えて repair18 locality test が存在する場合だけ実行します。

## 完了条件

$\pi_3^2$ の Reference が

```text
**[R1] (5.1).**
$\pi_{i}^{1} = 0\ (i > 1)$.
$\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}$.
```

となり、

```text
$\pi_{i}^{n} = 0\ (i < n)$.
```

および low-dimensional suspension isomorphism が Reference に現れないこと。

## 次 Phase / 次 repair との境界

今回は Reference selection / rendering だけを直します。

`E(\iota_1)=\iota_2` の本文復元、specific GIVEN の削除、proof derivation の変更には進みません。
