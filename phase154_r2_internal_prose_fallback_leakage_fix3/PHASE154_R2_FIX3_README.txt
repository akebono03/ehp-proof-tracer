Phase 154-R2 Fix3 — Reference marker sentence completion

前提
----
Phase 154-R2 初版、Fixed1、Fix2 が適用済みであること。

原因
----
Phase 153-R8 の reference body duplicate suppression は、
statement を [R#] に置換した後、

- [R#]を得る。
- 既に [R#] を含む行

は正規化できていた。

しかし Fix2 により生成された

  まず、<reference statement>

が

  まず、[R2]

に置換された場合、marker だけで文が終わるケースが未処理だった。

変更対象
--------
toda_group_proof_narrative_contribution_renderer.py

変更関数
--------
suppress_toda_group_proof_narrative_reference_body_duplicates()

import の変更
-------------
なし。

変更後関数全文
--------------
def suppress_toda_group_proof_narrative_reference_body_duplicates(
  body_markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  lines = body_markdown.splitlines()

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    if (
      isinstance(
        reference_number,
        bool,
      )
      or not isinstance(
        reference_number,
        int,
      )
    ):
      raise TypeError(
        "statement_lines_by_reference_number keys "
        "must be integers"
      )

    if not isinstance(
      statement_lines,
      tuple,
    ):
      raise TypeError(
        "statement_lines_by_reference_number values "
        "must be tuples"
      )

    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    for statement_line in statement_lines:
      if not isinstance(
        statement_line,
        str,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

      if not statement_line:
        continue

      updated_lines = []

      for line in lines:
        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue

        if line.strip() == statement_line:
          continue

        if marker in line:
          updated_lines.append(
            marker
            + "を用いる。"
          )
          continue

        replaced_line = line.replace(
          statement_line,
          marker,
        )

        if (
          marker in replaced_line
          and (
            replaced_line.rstrip().endswith(
              marker
              + "を得る。"
            )
            or replaced_line.rstrip().endswith(
              marker
              + "を得る."
            )
          )
        ):
          updated_lines.append(
            marker
            + "を用いる。"
          )
          continue

        if replaced_line.rstrip().endswith(
          marker
        ):
          updated_lines.append(
            replaced_line.rstrip()
            + "を用いる。"
          )
          continue

        updated_lines.append(
          replaced_line
        )

      lines = updated_lines

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


新規テスト
----------
tests/test_phase154_r2_fix3_reference_marker_completion.py

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_reference_body_duplicates,
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


def _render_group(
  n: int,
  k: int,
) -> str:
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase154_r2_fix3_completes_bare_reference_marker_after_replacement():
  statement = (
    r"$(α, \beta) \mapsto Eα + \nu_{4}\beta: "
    r"\pi_{i - 1}^{3} \oplus \pi_{i}^{7} "
    r"\to \pi_{i}^{4}$ は同型写像である."
  )
  body = (
    "まず、"
    + statement
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert rendered == "まず、[R2]を用いる。"


def test_phase154_r2_fix3_keeps_reference_marker_with_following_prose():
  statement = "$E: A \\xrightarrow{\\cong} B$"
  body = (
    "まず、"
    + statement
    + "を確認し、次の計算へ進む。"
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert rendered == (
    "まず、[R2]を確認し、次の計算へ進む。"
  )


def test_phase154_r2_fix3_pi11_4_has_complete_reference_use_sentence():
  rendered = _render_group(
    4,
    7,
  )

  assert "まず、[R2]" not in rendered.replace(
    "まず、[R2]を用いる。",
    "",
  )
  assert "まず、[R2]を用いる。" in rendered
  assert (
    r"$\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert r"\pi_{11}^{4} = 0" in rendered


def test_phase154_r2_fix3_keeps_previous_r2_repairs():
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
  assert (
    r"$\nu_{4}$ の分解を用いる."
    in pi10_4
  )

  forbidden = (
    "Toda Proposition 5.15を用いる。",
    r"\text{ is injective}",
    r"\text{ is exact}",
    "である.を用いる。",
    "Toda (5.6) の ν₄ 分解同型",
  )

  for fragment in forbidden:
    assert fragment not in pi11_4


一般規則
--------
statement replacement 後の行が [R#] で終わる場合だけ、

  <prefix>[R#]

を

  <prefix>[R#]を用いる。

にする。

[R#] の後に「を確認し」など意味のある本文が続く場合は変更しない。

今回触れないもの
----------------
- semantic duplication
- transition repetition
- Reference の数学的役割説明
- punctuation normalization
- Test Suite Consolidation

実行する pytest
---------------
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase153_r8_reference_use_prose_normalization.py
- tests/test_phase153_r3_11_reference_body_ownership_repair.py

全体テストは実行しない。

完了条件
--------
1. pi_11^4 の "まず、[R2]" が "まず、[R2]を用いる。" になる。
2. Reference statement の重複抑制を維持する。
3. "[R2]を確認し..." のような既存の意味ある周辺文を壊さない。
4. R2 初版〜Fix2 の修正を維持する。
5. focused tests が PASS する。

次 Phase との境界
-----------------
Fix3 が通れば Phase 154-R2 を完了とし、
Phase 154-R3 では同じ代表群を再監査して残存 defect category を再分類する。
