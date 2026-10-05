# Phase 159-R1-2 closure repair5

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - `_phase158_normalize_public_narrative_contract()` 全体
- テストファイルの変更なし
- import の変更なし

## 原因

既存 `_phase136_compact_eta_powers()` は、

$$
\eta_2\eta_3\eta_4 \mapsto \eta_2^3,
$$

$$
\eta_3\eta_4\eta_5 \mapsto \eta_3^3
$$

などの canonical display（標準表示）を既に定義しています。

しかし Phase 158 の generic public contract（一般公開表示契約）が
Reference section を再構成した後、その最終文字列にはこの既存 normalization が
適用されていませんでした。

そのため $\pi_6^3$ の Reference に旧 composition 表記が再出現し、
既存 Phase 157 regression が正しく failure を検出しました。

## 変更後の関数全文

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

  normalized = (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )

  return (
    _phase136_compact_eta_powers(
      normalized
    )
  )

```

## 変更内容

repair1/2 の以下は維持します。

- 空の `使用する結果` は表示しない
- recursive ancestry に実在する
  `TodaSuspensionIsomorphismStatement`
  から `TodaSuspensionInjectiveStatement` への dependency を表示する

そのうえで、最終 public Narrative 全体へ既存
`_phase136_compact_eta_powers()` を適用します。

新しい置換規則は追加しません。

## 実行する pytest

```powershell
python -m pytest -q .\tests\test_phase159_r1_2_pi3_2_closure.py
python -m pytest -q .\tests\test_phase157_r20_generic_dependency_rendering.py
python -m pytest -q .\tests\test_phase158_r5_5b_public_generic_order_route.py
```

その後、

```powershell
git diff --check
```

を実行します。

## 完了条件

- Phase 159-R1-2 focused tests 3件 PASS
- Phase 157 generic dependency/canonicalization regression PASS
- Phase 158 public generic route regression PASS
- `git diff --check` PASS

## 次 Phase との境界

- Reference selection policy は変更しない
- proof depth は変更しない
- 新しい eta canonicalization 規則は追加しない
- $\pi_4^3$ の監査・修正は Phase 159-R1-3 に残す
- 全体 pytest は Phase 159 終了時まで実行しない
