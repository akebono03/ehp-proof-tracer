# Phase 159 pi_(n+1)^n stable transport repair4

## 変更対象

- `tests/test_phase159_pi_nplus1_n_stable_transport.py`
  - `test_phase159_repair3_pi5_4_body_is_target_local_specialization`

production code の変更はありません。
import の変更もありません。

## 修正理由

実際の出力は

```text
[R1]を $(n,m,k)=(3,4,1)$ に適用すると, ...
```

であり、数学的にも表示上も正しい。

repair3 の focused test だけが

```text
$(n,m,k)=(3,4,1) 
```

のように `$` の内側ではなく外側に空白を期待していたため、
stale expectation として修正する。

## テストファイル全文

```python
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def _render(
  n: int,
) -> str:
  presentation, _, _, _ = (
    _method_evidence_data(
      n,
      1,
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def test_phase159_repair3_pi5_4_reference_is_general_toda45_and_prop51():
  rendered = _render(
    4
  )

  assert (
    "**[R1] (4.5).**"
    in rendered
  )
  assert (
    r"$n \ge k + 2$ のとき, "
    r"$E^{m-n}: "
    r"\pi_{n+k}^{n} "
    r"\to "
    r"\pi_{m+k}^{m}$ は同型."
    in rendered
  )
  assert (
    "**[R2] Proposition 5.1.**"
    in rendered
  )
  assert (
    r"$\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}$."
    in rendered
  )


def test_phase159_repair3_pi5_4_body_is_target_local_specialization():
  rendered = _render(
    4
  )
  proof_body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  assert (
    r"[R1]を $(n,m,k)=(3,4,1)$ "
    r"に適用すると, "
    r"$E: \pi_{4}^{3} "
    r"\to \pi_{5}^{4}$ は同型."
    in proof_body
  )
  assert (
    r"$E\eta_{3} = \eta_{4}$."
    in proof_body
  )
  assert (
    r"$\pi_{n + 1}^{n}"
    not in proof_body
  )
  assert (
    r"\tag{"
    not in proof_body
  )


def test_phase159_repair3_pi_nplus1_n_family_uses_same_proof():
  cases = (
    (
      5,
      r"$(n,m,k)=(3,5,1)",
      r"$E^{2}: \pi_{4}^{3} "
      r"\to \pi_{6}^{5}$ は同型.",
      r"$E^{2}\eta_{3} = \eta_{5}$.",
      r"$\pi_{6}^{5} = "
      r"\mathbb{Z}/2\{\eta_{5}\}$.",
    ),
    (
      6,
      r"$(n,m,k)=(3,6,1)",
      r"$E^{3}: \pi_{4}^{3} "
      r"\to \pi_{7}^{6}$ は同型.",
      r"$E^{3}\eta_{3} = \eta_{6}$.",
      r"$\pi_{7}^{6} = "
      r"\mathbb{Z}/2\{\eta_{6}\}$.",
    ),
  )

  for (
    n,
    specialization,
    isomorphism,
    generator_transport,
    conclusion,
  ) in cases:
    rendered = _render(
      n
    )

    assert (
      "**[R1] (4.5).**"
      in rendered
    )
    assert (
      "**[R2] Proposition 5.1.**"
      in rendered
    )
    assert (
      specialization
      in rendered
    )
    assert (
      isomorphism
      in rendered
    )
    assert (
      generator_transport
      in rendered
    )
    assert (
      conclusion
      in rendered
    )


def test_phase159_repair3_pi4_3_delegates_to_existing_renderer():
  rendered = _render(
    3
  )

  assert (
    r"\operatorname{Im}\Delta"
    in rendered
  )
  assert (
    r"\ker E"
    in rendered
  )
  assert (
    r"$E: \pi_{3}^{2} "
    r"\to \pi_{4}^{3}$ は全射."
    in rendered
  )
  assert (
    r"$(n,m,k)=(3,3,1)"
    not in rendered
  )

```

## Phase 境界

- production renderer は変更しない。
- `pi_(n+1)^n`, `n >= 4` の証明ロジックは repair3 のまま。
- `pi_4^3` の既存証明も変更しない。
- 全体テストは Phase 最後まで実行しない。
