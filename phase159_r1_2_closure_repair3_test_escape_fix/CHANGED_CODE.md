# Phase 159-R1-2 closure repair3

## 変更対象

- production code: **変更なし**
- `tests/test_phase159_r1_2_pi3_2_closure.py`
  - テストファイル全文を置換
  - LaTeX 文字列の過剰な escape（エスケープ）のみ修正

## 原因

失敗した期待値は Python runtime 上で、

```text
$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$
```

すなわちバックスラッシュ2個を期待していました。

実際の renderer 出力は正しく、

```text
$E: \pi_{1}^{1} \to \pi_{2}^{2}$
```

です。

repair2 で追加した production code は変更しません。

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
    "$E: \\pi_{1}^{1} \\to "
    "\\pi_{2}^{2}$ は同型写像である."
  )
  injectivity = (
    "$E: \\pi_{1}^{1} \\to "
    "\\pi_{2}^{2}$ は単射である."
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

その後 `git diff --check` を実行します。

## 完了条件

- focused tests 3件 PASS
- generic dependency regression PASS
- public generic route regression PASS
- `git diff --check` PASS

全体 pytest は Phase 159 の最後まで実行しません。
