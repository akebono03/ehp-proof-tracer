# Phase 159-R1-7c R2 repair1 runtime diagnosis

Production code changes: none
Test changes: none
pytest: not run

## Current public render function source

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  normalized = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )

  return (
    _phase159_r1_7c_normalize_public_equality_chains(
      presentation,
      normalized,
    )
  )
```

## Phase 158 normalizer tail

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

  source_lines = rendered.rstrip().splitlines()

  if source_lines and source_lines[0] == title:
    content_lines = source_lines[1:]
  else:
    content_lines = source_lines[:]

  while content_lines and not content_lines[0].strip():
    content_lines.pop(0)

  def exact_index(
    marker: str,
  ) -> int | None:
    try:
      return content_lines.index(marker)
    except ValueError:
      return None

  target_index = exact_index(target_header)
  reference_index = exact_index(reference_header)
  proof_index = exact_index(proof_header)

  target_body = _phase158_public_narrative_target_lines(
    presentation
  )

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

  while reference_body and not reference_body[0].strip():
    reference_body.pop(0)

  while reference_body and not reference_body[-1].strip():
    reference_body.pop()

  if (
    reference_body
    and reference_body[-1].strip() == separator
  ):
    reference_body.pop()
    while reference_body and not reference_body[-1].strip():
      reference_body.pop()

  if proof_index is not None:
    proof_body = content_lines[proof_index + 1:]
  elif target_index is None and reference_index is None:
    proof_body = content_lines[:]
  else:
    proof_body = []

  while proof_body and not proof_body[0].strip():
    proof_body.pop(0)

  proof_body = _phase158_strip_terminal_qed_lines(
    proof_body
  )
  proof_body = _phase158_normalize_public_equation_numbers(
    proof_body
  )
  proof_body = (
    _phase159_r1_7b_normalize_public_exact_sequences(
      presentation,
      proof_body,
    )
  )
  proof_body = _phase159_project_generic_semantics_to_public_proof(
    presentation,
    proof_body,
  )

  lines = [
    title,
    "",
    target_header,
    "",
    *target_body,
    "",
    reference_header,
    "",
  ]

  if reference_body:
    lines.extend(
      (
        *reference_body,
        "",
      )
    )

  lines.extend(
    (
      separator,
      "",
      proof_header,
      "",
      *proof_body,
      "",
      qed,
    )
  )

  return "\n".join(lines).rstrip() + "\n"
```

## pi6_3 transitivity candidates

### step id=2377829508304
- conclusion rendered: "$2\\nu' = \\eta_{3}^{3}$"
- conclusion indices: ()
- premise 1 rendered: "$2\\nu' = \\eta_{3}\\eta_{4}\\eta_{5}$"
- premise 1 indices: ()
- premise 2 rendered: '$\\eta_{3}\\eta_{4}\\eta_{5} = \\eta_{3}^{3}$'
- premise 2 indices: ()

### step id=2377829583888
- conclusion rendered: "$H\\left(\\nu'\\right) = \\eta_{5}$"
- conclusion indices: (9,)
- premise 1 rendered: "$H\\left(\\nu'\\right) = \\eta_{5}$"
- premise 1 indices: (9,)
- premise 2 rendered: '$\\eta_{5} = \\eta_{5}$'
- premise 2 indices: (47,)

## pi6_3 relevant body lines

- 7: `"[R2]より, $2\\nu' = \\eta_{3}E\\eta_{3}\\eta_{5} = \\eta_{3}\\eta_{4}\\eta_{5}$."`
- 15: `'[R1] と $E$ の単射性より, $E(\\eta_{2}^{3})=\\eta_{3}^{3}\\neq0$ であり, 単射写像は元の位数を保つ.'`
- 21: `'$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は全射である.'`
- 33: `'$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射である.'`
- 35: `'$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2$.'`
- 37: `"$\\operatorname{ord}(\\eta_{3}^{3})=2$ かつ $2\\nu'=\\eta_{3}^{3}$ より, $4\\nu'=0$ かつ $2\\nu'\\neq0$ である."`
- 49: `'$H: \\pi_{6}^{3} \\to \\pi_{6}^{5}$ は全射である.'`

## pi11_4 relevant body lines

- 2: `'\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} \\xrightarrow{\\Delta} \\pi_{8}^{2}.'`
- 5: `'$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$ は全射である.'`
- 10: `'\\pi_{9}^{2} \\xrightarrow{E} \\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5}.'`
- 13: `'$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$ は単射である.'`

## pi6_3 rendered

```text
# Group proof narrative

## 証明対象

\[
\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}.
\]

## 使用する結果

**[R1] Proposition 5.6.**
$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$.
**[R2] (5.3).**
$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ とすると,
$\nu' \in \pi_{6}^{3}$.
$2\nu' = \eta_{3}\eta_{4}\eta_{5}$.
$H\left(\nu'\right) = \eta_{5}$.
**[R3] Proposition 5.3.**
$\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}\eta_{6}\}$.
**[R4] Proposition 5.1.**
$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.
**[R5] Equation 5.7.**
$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

---

## 証明

まず, $\nu'$ の位数を決定するために, 次の完全列を考える.

\[
\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}.
\]

[R2]より, $2\nu' = \eta_{3}E\eta_{3}\eta_{5} = \eta_{3}\eta_{4}\eta_{5}$.

[R2]より, $H\left(\nu'\right) = \eta_{5}$.

$\eta_{6}=E\eta_{5}$ である.

[R5]より, $H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

[R1] と $E$ の単射性より, $E(\eta_{2}^{3})=\eta_{3}^{3}\neq0$ であり, 単射写像は元の位数を保つ.

[R1]より, $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$.

[R3]より, $\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}\eta_{6}\}$.

$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である.

完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{7}^{5}$ である.

$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である.

この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

\[
\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}.
\]

$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.

$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$.

$\operatorname{ord}(\eta_{3}^{3})=2$ かつ $2\nu'=\eta_{3}^{3}$ より, $4\nu'=0$ かつ $2\nu'\neq0$ である.

$\operatorname{ord}\left(\nu'\right) = 4$.

最後に, $\pi_{6}^{3}$ の群構造を決定するために, 次の完全列を考える.

[R2]より, $\nu' \in \pi_{6}^{3}$.

[R4]より, $\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.

$\eta_{5} = \eta_{5}$.

$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.

この完全性と, 左の写像が単射, 右の写像が全射であることより, 次の短完全列を得る.

\[
0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0.
\]

この短完全列と両端の群の位数より, 中央の群の位数は $2\cdot2=4$ である.
また, $\nu'$ は中央の群に属し, $\operatorname{ord}(\nu')=4$ であるから, $\nu'$ は中央の群を生成する.

$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$.

□
```

## pi11_4 rendered

```text
# Group proof narrative

## 証明対象

\[
\pi_{11}^{4} = 0.
\]

## 使用する結果

**[R1] Proposition 5.15.**
$\pi_{10}^{3} = 0$.
$\pi_{9}^{2} = 0$.
**[R2] Proposition 5.8.**
$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.
**[R3] Proposition 4.4.**
$(α, \beta) \mapsto Eα + \nu_{4}\beta: \pi_{i - 1}^{3} \oplus \pi_{i}^{7} \to \pi_{i}^{4}$ は同型写像である.

---

## 証明

\[
\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} \xrightarrow{\Delta} \pi_{8}^{2}.
\]

$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ は全射である.

[R1]より, $\pi_{9}^{2} = 0$.

\[
\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5}.
\]

$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ は単射である.

[R1]より, $\pi_{10}^{3} = 0$.

$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$.

[R2]より, $\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.

[R3]を用いて, $\nu_{4}$ の分解写像は同型写像である.

以上より, $\pi_{11}^{4} = 0$.

□
```
