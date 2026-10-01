Phase 154-R5 Fix1 Repair3 — Current contract test update

状況
----
Repair2 の production behavior は期待どおり:

  [R2]より、$\nu_{4}$ の分解写像は同型写像である.

focused tests は 36 passed / 1 failed。

唯一の失敗は Phase 154-R2 Fix3 の public pi11_4 expectation であり、
R2 当時の旧 contract:

  まず、[R2]を用いる。

を要求している。

R5 では graph-backed linkage により、より具体的な current contract:

  [R2]より、$\nu_{4}$ の分解写像は同型写像である.

へ更新された。

変更対象
--------
tests/test_phase154_r2_fix3_reference_marker_completion.py

production files
----------------
変更なし。

import
------
変更なし。更新後 test file 全文:

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


重要
----
低レベル関数
suppress_toda_group_proof_narrative_reference_body_duplicates()
の既存 contract は変更しない。

したがって次の2テストは従来どおり:

- bare replacement -> `まず、[R2]を用いる。`
- following prose -> `まず、[R2]を確認し、次の計算へ進む。`

public pi11_4 の integration expectation だけを R5 に合わせる。

完了条件
--------
focused current-contract tests がすべて PASS。

全体テスト
----------
実行しない。Phase 154 最後まで保留。

次の境界
--------
PASS 後は R5 representative re-audit を行い、
残存 Reference linkage candidate がなければ R5 完了。
その後 R6 punctuation normalization。
