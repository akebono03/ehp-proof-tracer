# Phase 159-R1-2 closure repair2 変更内容

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - `_phase159_restore_isomorphism_to_injective_dependency_visibility`
- `tests/test_phase159_r1_2_pi3_2_closure.py`
  - ファイル全文を更新

production code の import 変更はありません。

## 原因

repair1 では `presentation.nodes` だけを調べていました。

しかし $\pi_3^2$ では、

$$
E:\pi_1^1\to\pi_2^2
$$

が同型写像である step と、そこから導かれる単射性 step は
`max_depth=2` の selected nodes（選択済みノード）より上流にあります。

一方、`presentation.root_step` から `ProofStep.premises` を再帰的にたどれば、
この dependency は保持されています。

したがって depth 規則そのものは変更せず、public Narrative に必要な
dependency visibility（依存関係の可視性）だけを復元します。

## 変更関数全文

```python
def _phase159_restore_isomorphism_to_injective_dependency_visibility(
  presentation: TodaGroupProofPresentation,
  proof_body: list[str],
) -> list[str]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    proof_body,
    list,
  ):
    raise TypeError(
      "proof_body must be a list"
    )

  dependency_pairs = []
  visited_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    step_id = id(
      proof_step
    )

    if step_id in visited_step_ids:
      return

    visited_step_ids.add(
      step_id
    )

    if isinstance(
      proof_step.conclusion,
      TodaSuspensionInjectiveStatement,
    ):
      injective_map = (
        proof_step.conclusion.map
      )
      isomorphism_step = next(
        (
          premise_step
          for premise_step in proof_step.premises
          if (
            isinstance(
              premise_step.conclusion,
              TodaSuspensionIsomorphismStatement,
            )
            and premise_step.conclusion.map
            == injective_map
          )
        ),
        None,
      )

      if isomorphism_step is not None:
        dependency_pairs.append(
          (
            isomorphism_step,
            proof_step,
          )
        )

    for premise_step in proof_step.premises:
      visit(
        premise_step
      )

  visit(
    presentation.root_step
  )

  rendered = "\n".join(
    proof_body
  )

  for (
    isomorphism_step,
    injective_step,
  ) in dependency_pairs:
    isomorphism_prose = (
      _render_generic_narrative_step(
        isomorphism_step
      )
    )
    injective_prose = (
      _render_generic_narrative_step(
        injective_step
      )
    )

    if (
      not isomorphism_prose
      or not injective_prose
    ):
      continue

    has_isomorphism = (
      isomorphism_prose in rendered
    )
    has_injectivity = (
      injective_prose in rendered
    )

    if (
      has_isomorphism
      and has_injectivity
    ):
      continue

    if has_injectivity:
      rendered = rendered.replace(
        injective_prose,
        (
          isomorphism_prose
          + "\n\n"
          + "したがって, "
          + injective_prose
        ),
        1,
      )
      continue

    if has_isomorphism:
      rendered = rendered.replace(
        isomorphism_prose,
        (
          isomorphism_prose
          + "\n\n"
          + "したがって, "
          + injective_prose
        ),
        1,
      )
      continue

    dependency_prose = (
      isomorphism_prose
      + "\n\n"
      + "したがって, "
      + injective_prose
    )

    if rendered:
      rendered = (
        dependency_prose
        + "\n\n"
        + rendered
      )
    else:
      rendered = dependency_prose

  return rendered.splitlines()

```

## テストファイル全文

```python
from homotopy_groups import (
  TodaSuspensionIsomorphismStatement,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaSuspensionInjectiveStatement,
)


def _build_phase159_r1_2_pi3_2_presentation():
  report = build_standard_toda_report(
    n=2,
    k=1,
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


def _render_phase159_r1_2_pi3_2() -> str:
  presentation = (
    _build_phase159_r1_2_pi3_2_presentation()
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _recursive_ancestry(
  proof_step,
):
  ordered = []
  visited = set()

  def visit(
    step,
  ):
    step_id = id(
      step
    )

    if step_id in visited:
      return

    visited.add(
      step_id
    )
    ordered.append(
      step
    )

    for premise in step.premises:
      visit(
        premise
      )

  visit(
    proof_step
  )

  return tuple(
    ordered
  )


def test_phase159_r1_2_pi3_2_omits_empty_reference_section():
  rendered = (
    _render_phase159_r1_2_pi3_2()
  )

  assert "## 使用する結果" not in rendered
  assert "## 証明" in rendered


def test_phase159_r1_2_pi3_2_dependency_exists_in_recursive_ancestry():
  presentation = (
    _build_phase159_r1_2_pi3_2_presentation()
  )
  ancestry = (
    _recursive_ancestry(
      presentation.root_step
    )
  )

  injective_step = next(
    step
    for step in ancestry
    if isinstance(
      step.conclusion,
      TodaSuspensionInjectiveStatement,
    )
  )

  assert any(
    (
      isinstance(
        premise.conclusion,
        TodaSuspensionIsomorphismStatement,
      )
      and premise.conclusion.map
      == injective_step.conclusion.map
    )
    for premise in injective_step.premises
  )


def test_phase159_r1_2_pi3_2_shows_isomorphism_before_injectivity():
  rendered = (
    _render_phase159_r1_2_pi3_2()
  )

  isomorphism = (
    "$E: \\\\pi_{1}^{1} \\\\to "
    "\\\\pi_{2}^{2}$ は同型写像である."
  )
  injectivity = (
    "$E: \\\\pi_{1}^{1} \\\\to "
    "\\\\pi_{2}^{2}$ は単射である."
  )

  assert isomorphism in rendered
  assert injectivity in rendered
  assert (
    rendered.index(
      isomorphism
    )
    < rendered.index(
      injectivity
    )
  )
  assert (
    "したがって, "
    + injectivity
  ) in rendered

```

## 実行する pytest

```powershell
python -m pytest -q .\tests\test_phase159_r1_2_pi3_2_closure.py
python -m pytest -q .\tests\test_phase157_r20_generic_dependency_rendering.py
python -m pytest -q .\tests\test_phase158_r5_5b_public_generic_order_route.py
```

続けて `git diff --check` を実行します。

## 完了条件

- 空の `使用する結果` が表示されない。
- recursive ancestry に `isomorphism => injective` が実在することを focused test で確認できる。
- public Narrative に
  「$E$ は同型写像である。したがって $E$ は単射である。」
  がこの順序で表示される。
- 関連 regression が PASS する。
- `git diff --check` が PASS する。

## 次 Phase との境界

- reference policy は変更しない。
- `max_depth` の意味も変更しない。
- $\pi_2^1=0$ と $\pi_3^3=\mathbb Z\{\iota_3\}$ の Reference 昇格は行わない。
- Phase 159-R1-3 $\pi_4^3$ は先取りしない。
