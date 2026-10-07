# Phase 159 pi3_2 Reference general-form repair19

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_6c_canonicalize_toda_51_reference()`
  - `render_toda_group_proof_narrative_markdown()` の最終 return

import の変更はありません。

テストファイルの変更はありません。既存の
`test_phase159_r1_6c_toda_51_reference_is_source_faithful()`
を今回の契約テストとして使用します。

## `_phase159_r1_6c_canonicalize_toda_51_reference()` 全文

```python
def _phase159_r1_6c_canonicalize_toda_51_reference(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  reference_marker = (
    "## 使用する結果\n\n"
  )
  proof_boundary = (
    "\n---\n\n## 証明"
  )
  reference_start = rendered.find(
    reference_marker
  )

  if reference_start < 0:
    return rendered

  content_start = (
    reference_start
    + len(
      reference_marker
    )
  )
  boundary_index = rendered.find(
    proof_boundary,
    content_start,
  )

  if boundary_index < 0:
    return rendered

  reference_body = rendered[
    content_start:
    boundary_index
  ]
  lines = reference_body.splitlines()
  output = []
  index = 0

  while index < len(
    lines
  ):
    match = re.match(
      r"^\*\*\[R([0-9]+)\] "
      r"\(5\.1\)\.\*\*$",
      lines[
        index
      ].strip(),
    )

    if match is None:
      output.append(
        lines[
          index
        ]
      )
      index += 1
      continue

    output.append(
      lines[
        index
      ]
    )
    output.append(
      (
        r"$\pi_{i}^{1} = 0\ (i > 1),"
        r"\qquad "
        r"\pi_{i}^{n} = 0\ (i < n)$."
      )
    )
    output.append(
      (
        r"$\pi_{n}^{n} = "
        r"\mathbb{Z}\{\iota_{n}\}$."
      )
    )

    index += 1

    while (
      index < len(
        lines
      )
      and not lines[
        index
      ].strip().startswith(
        "**[R"
      )
    ):
      index += 1

  normalized_reference = "\n".join(
    output
  ).rstrip()

  return (
    rendered[
      :content_start
    ]
    + normalized_reference
    + rendered[
      boundary_index:
    ]
  )
```

## `render_toda_group_proof_narrative_markdown()` の変更方針

repair18 後のローカル関数全体を GitHub 版で上書きしません。
適用スクリプトは現在の関数の最終 `return` を AST で検出し、
その返値だけを次の形に包みます。

```python
  return (
    _phase159_r1_6c_canonicalize_toda_51_reference(
      <repair18 後の現在の最終返値>
    )
  )
```

このため、repair18 で入った本文順序処理は保持されます。

## 期待する Reference

```text
**[R1] (5.1).**
$\pi_{i}^{1} = 0\ (i > 1),\qquad \pi_{i}^{n} = 0\ (i < n)$.
$\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}$.
```

Reference から次を除去します。

```text
$\pi_{2}^{1} = 0$.
$\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}$.
$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型.
```

これらの proof body 側の扱いは今回変更しません。
