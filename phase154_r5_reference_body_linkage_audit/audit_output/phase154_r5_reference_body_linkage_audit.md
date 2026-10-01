# Phase 154-R5 — Reference ↔ proof body linkage audit

Production changes: none.

Target:
- group: $\pi_{11}^{4}$
- view: Narrative
- depth: 2

## Public Narrative

# Group proof narrative

## 使用する結果

使用する結果を先にまとめる.

**[R1] Proposition 5.8.**
$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.
**[R2] Proposition 4.4.**
$(α, \beta) \mapsto Eα + \nu_{4}\beta: \pi_{i - 1}^{3} \oplus \pi_{i}^{7} \to \pi_{i}^{4}$ は同型写像である.

## 証明

まず、$H: \pi_{10}^{3} \to \pi_{10}^{5}$ は単射である.
また、$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ は単射である.
さらに、$\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} \xrightarrow{Δ} \pi_{8}^{2}$ は完全である.
これらから、$\pi_{10}^{3} = 0$を得る。
また、[R1]を用いる。
まず、[R2]を用いる。
このことから、$\nu_{4}$ の分解写像は同型写像である.

したがって、$\pi_{11}^{4} = 0$を得る。

## Reference graph audit

### [R1]

- literature reference: `Toda Proposition 5.8`
- selected reference statements:

#### selected step 1

- statement type: `TodaProp58FiniteDimensionalStatement`
- rendered statement: `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.`
- own reference: `Toda Proposition 5.8`
- direct consumer count: 1
- reaches root: True

Direct consumers:

- 1. TodaPrimaryGroupZeroStatement
  - rendered: `$\pi_{11}^{4} = 0$`
  - literature reference: `Toda Proposition 5.15`

Shortest selected-step → root path:

- 1. `TodaProp58FiniteDimensionalStatement`
  - rendered: `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.`
  - literature reference: `Toda Proposition 5.8`
- 2. `TodaPrimaryGroupZeroStatement`
  - rendered: `$\pi_{11}^{4} = 0$`
  - literature reference: `Toda Proposition 5.15`

### [R2]

- literature reference: `Toda Lemma 5.7`
- selected reference statements:

#### selected step 1

- statement type: `Relation`
- rendered statement: `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$`
- own reference: `Toda Lemma 5.7`
- direct consumer count: 1
- reaches root: True

Direct consumers:

- 1. TodaProp58FiniteDimensionalStatement
  - rendered: `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.`
  - literature reference: `Toda Proposition 5.8`

Shortest selected-step → root path:

- 1. `Relation`
  - rendered: `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$`
  - literature reference: `Toda Lemma 5.7`
- 2. `TodaProp58FiniteDimensionalStatement`
  - rendered: `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.`
  - literature reference: `Toda Proposition 5.8`
- 3. `TodaPrimaryGroupZeroStatement`
  - rendered: `$\pi_{11}^{4} = 0$`
  - literature reference: `Toda Proposition 5.15`

### [R3]

- literature reference: `Toda Proposition 4.4`
- selected reference statements:

#### selected step 1

- statement type: `TodaProp44IsomorphismStatement`
- rendered statement: `$(α, \beta) \mapsto Eα + \nu_{4}\beta: \pi_{i - 1}^{3} \oplus \pi_{i}^{7} \to \pi_{i}^{4}$ は同型写像である.`
- own reference: `Toda Proposition 4.4`
- direct consumer count: 1
- reaches root: True

Direct consumers:

- 1. Toda56Nu4DecompositionIsomorphismStatement
  - rendered: `$\nu_{4}$ の分解写像は同型写像である.`
  - literature reference: `None`

Shortest selected-step → root path:

- 1. `TodaProp44IsomorphismStatement`
  - rendered: `$(α, \beta) \mapsto Eα + \nu_{4}\beta: \pi_{i - 1}^{3} \oplus \pi_{i}^{7} \to \pi_{i}^{4}$ は同型写像である.`
  - literature reference: `Toda Proposition 4.4`
- 2. `Toda56Nu4DecompositionIsomorphismStatement`
  - rendered: `$\nu_{4}$ の分解写像は同型写像である.`
  - literature reference: `None`
- 3. `TodaPrimaryGroupZeroStatement`
  - rendered: `$\pi_{11}^{4} = 0$`
  - literature reference: `Toda Proposition 5.15`

## Statement lines used in the public Reference section

### [R1]

- `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.`

### [R2]

- `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$`

### [R3]

- `$(α, \beta) \mapsto Eα + \nu_{4}\beta: \pi_{i - 1}^{3} \oplus \pi_{i}^{7} \to \pi_{i}^{4}$ は同型写像である.`

## Decision rule for R5 implementation

- Do not generate linkage from line adjacency alone.
- Use the selected reference step and its graph consumer/path to identify the mathematical fact that the Reference supports.
- If the selected step has a unique proof path to a visible consumer, render the Reference marker as support for that fact.
- If graph ownership is ambiguous, keep the existing neutral `[R#]を用いる。` form rather than inventing a relation.
- R5 must remain generic; no pi11_4-specific branch.
