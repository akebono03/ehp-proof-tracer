# 変更対象

- `toda_group_proof_narrative_renderer.py`
  - 新規関数 `_phase159_restore_isomorphism_to_injective_dependency_visibility`
    - 追加位置: `_phase158_normalize_public_narrative_contract` の直前
  - 変更関数 `_phase158_normalize_public_narrative_contract`
- `tests/test_phase159_r1_2_pi3_2_closure.py`
  - 新規テストファイル

import の変更はありません。

## 新規関数全文

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

  rendered = "\n".join(
    proof_body
  )

  for node in presentation.nodes:
    injective_step = node.proof_step

    if not isinstance(
      injective_step.conclusion,
      TodaSuspensionInjectiveStatement,
    ):
      continue

    injective_map = (
      injective_step.conclusion.map
    )
    isomorphism_step = next(
      (
        premise_step
        for premise_step in injective_step.premises
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

    if isomorphism_step is None:
      continue

    injective_prose = (
      _render_generic_narrative_step(
        injective_step
      )
    )
    isomorphism_prose = (
      _render_generic_narrative_step(
        isomorphism_step
      )
    )

    if (
      not injective_prose
      or not isomorphism_prose
      or injective_prose not in rendered
      or isomorphism_prose in rendered
    ):
      continue

    replacement = (
      isomorphism_prose
      + "\n\n"
      + "したがって, "
      + injective_prose
    )
    rendered = rendered.replace(
      injective_prose,
      replacement,
      1,
    )

  return rendered.splitlines()

```

## 変更関数全文

```python
def _phase158_normalize_public_narrative_contract(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if presentation.max_depth < 2:
    return rendered

  title = "# Group proof narrative"
  target_header = "## 証明対象"
  reference_header = "## 使用する結果"
  separator = "---"
  proof_header = "## 証明"
  qed = "□"

  source_lines = (
    rendered.rstrip().splitlines()
  )

  if (
    source_lines
    and source_lines[0] == title
  ):
    content_lines = source_lines[1:]
  else:
    content_lines = source_lines[:]

  while (
    content_lines
    and not content_lines[0].strip()
  ):
    content_lines.pop(0)

  def exact_index(
    marker: str,
  ) -> int | None:
    try:
      return content_lines.index(
        marker
      )
    except ValueError:
      return None

  target_index = exact_index(
    target_header
  )
  reference_index = exact_index(
    reference_header
  )
  proof_index = exact_index(
    proof_header
  )

  if target_index is not None:
    target_end_candidates = [
      index
      for index in (
        reference_index,
        proof_index,
        len(
          content_lines
        ),
      )
      if (
        index is not None
        and index > target_index
      )
    ]
    target_end = min(
      target_end_candidates
    )
    target_body = content_lines[
      target_index + 1:
      target_end
    ]
  else:
    target_body = (
      _phase158_public_narrative_target_lines(
        presentation
      )
    )

  while (
    target_body
    and not target_body[0].strip()
  ):
    target_body.pop(0)

  while (
    target_body
    and not target_body[-1].strip()
  ):
    target_body.pop()

  reference_body: list[str] = []

  if (
    reference_index is not None
    and proof_index is not None
    and reference_index < proof_index
  ):
    reference_body = content_lines[
      reference_index + 1:
      proof_index
    ]

  while (
    reference_body
    and not reference_body[0].strip()
  ):
    reference_body.pop(0)

  while (
    reference_body
    and not reference_body[-1].strip()
  ):
    reference_body.pop()

  if (
    reference_body
    and reference_body[-1].strip()
    == separator
  ):
    reference_body.pop()

    while (
      reference_body
      and not reference_body[-1].strip()
    ):
      reference_body.pop()

  if proof_index is not None:
    proof_body = content_lines[
      proof_index + 1:
    ]
  elif (
    target_index is None
    and reference_index is None
  ):
    proof_body = content_lines[:]
  else:
    proof_body = []

  while (
    proof_body
    and not proof_body[0].strip()
  ):
    proof_body.pop(0)

  proof_body = (
    _phase158_strip_terminal_qed_lines(
      proof_body
    )
  )
  proof_body = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )
  proof_body = (
    _phase159_restore_isomorphism_to_injective_dependency_visibility(
      presentation,
      proof_body,
    )
  )

  lines = [
    title,
    "",
    target_header,
    "",
    *target_body,
    "",
  ]

  if reference_body:
    lines.extend(
      (
        reference_header,
        "",
        *reference_body,
        "",
        separator,
        "",
      )
    )

  lines.extend(
    (
      proof_header,
      "",
      *proof_body,
      "",
      qed,
    )
  )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )

```

## 新規テストファイル全文

```python
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


def _render_phase159_r1_2_pi3_2() -> str:
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_r1_2_pi3_2_omits_empty_reference_section():
  rendered = (
    _render_phase159_r1_2_pi3_2()
  )

  assert "## 使用する結果" not in rendered
  assert "## 証明" in rendered


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

続けて `git diff --check` を実行します。全体 pytest は実行しません。

## 完了条件

- $\pi_3^2$ で reference body が空なら `使用する結果` 見出しが出ない。
- proof graph に suspension isomorphism（懸垂写像の同型）から
  suspension injectivity（懸垂写像の単射性）への直接 dependency がある場合、
  public Narrative に「同型写像である。したがって単射である。」の順序が残る。
- 関連 generic regression が PASS する。
- `git diff --check` が PASS する。

## 次 Phase との境界

Phase 159-R1-2 では reference policy を拡張しません。
$\pi_2^1=0$ や $\pi_3^3=\mathbb Z\{\iota_3\}$ の Reference 昇格は行いません。
Phase 159-R1-3 の $\pi_4^3$ 監査・修正も先取りしません。
