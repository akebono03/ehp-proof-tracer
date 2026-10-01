# Phase 154-R4 Fix1 — pi6_3 Residual Duplicate Audit

Production changes: none.

Conditions:
- group: $\pi_6^3$
- view: Narrative
- depth: 2

## Exact duplicate summary

duplicate_text_count: 2
duplicate_occurrence_excess: 3

### Duplicate 1

- text: `以上より、`
- count: 2
- audit classification: transition connector repeats; compare its target conclusions before deciding whether it is redundant

Occurrences:

- line 37
  - previous: `$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$`
  - current: `以上より、`
  - next: `以上で得た群構造、生成元、および写像に関する結果を合わせると、`
- line 65
  - previous: `$0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$`
  - current: `以上より、`
  - next: `この短完全列と両端の群の位数より、中央の群の位数は $2\cdot2=4$ である.`

### Duplicate 2

- text: `したがって、`
- count: 3
- audit classification: transition connector repeats; compare its target conclusions before deciding whether it is redundant

Occurrences:

- line 44
  - previous: `この完全性と $Δ=0$ より、$\ker E=\operatorname{Im}Δ=0$ である.`
  - current: `したがって、`
  - next: `$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.`
- line 49
  - previous: `$\operatorname{ord}(\eta_{3}\eta_{4}\eta_{5})=2$ かつ $2\nu'=\eta_{3}\eta_{4}\eta_{5}$ より、$4\nu'=0$ かつ $2\nu'\neq0$ である.`
  - current: `したがって、`
  - next: `$\operatorname{ord}\left(\nu'\right) = 4$`
- line 69
  - previous: `また、$\nu'$ は中央の群に属し、$\operatorname{ord}(\nu')=4=4$ であるから、$\nu'$ は中央の群を生成する.`
  - current: `したがって、`
  - next: `$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$`

## Reason sidecar inventory

- DEFINITION_APPLICABILITY: 1
- EXACTNESS_TO_MAP_PROPERTY: 1
- FINAL_GROUP_STRUCTURE: 1
- FINAL_RESULT_DERIVATION: 2
- MULTIPLE_RELATION_TO_ORDER: 1

## Reason details

### Reason 1

- kind: `DEFINITION_APPLICABILITY`
- conclusion type: `TodaBracketMembershipStatement`
- rendered sentence: `この前提条件を満たすので、Lemma 5.2 を適用できる.\nLemma 5.2 の $\beta$ を $\nu'$ と定めると、`

### Reason 2

- kind: `FINAL_GROUP_STRUCTURE`
- conclusion type: `Relation`
- rendered sentence: `この短完全列と両端の群の位数より、中央の群の位数は $2\cdot2=4$ である.\nまた、$\nu'$ は中央の群に属し、$\operatorname{ord}(\nu')=4=4$ であるから、$\nu'$ は中央の群を生成する.\nしたがって、`

### Reason 3

- kind: `MULTIPLE_RELATION_TO_ORDER`
- conclusion type: `Relation`
- rendered sentence: `$\operatorname{ord}(\eta_{3}\eta_{4}\eta_{5})=2$ かつ $2\nu'=\eta_{3}\eta_{4}\eta_{5}$ より、$4\nu'=0$ かつ $2\nu'\neq0$ である.\nしたがって、`

### Reason 4

- kind: `FINAL_RESULT_DERIVATION`
- conclusion type: `Relation`
- rendered sentence: `以上で得た群構造、生成元、および写像に関する結果を合わせると、`

### Reason 5

- kind: `EXACTNESS_TO_MAP_PROPERTY`
- conclusion type: `TodaSuspensionInjectiveStatement`
- rendered sentence: `この完全性と $Δ=0$ より、$\ker E=\operatorname{Im}Δ=0$ である.\nしたがって、`

### Reason 6

- kind: `FINAL_RESULT_DERIVATION`
- conclusion type: `Relation`
- rendered sentence: `以上で得た群構造、生成元、および写像に関する結果を合わせると、`

## Full Narrative

使用する結果を先にまとめる.

**[R1] (5.3).**
$\nu' \in \pi_{6}^{3}$
$2\nu' = \eta_{3}E\eta_{3}\eta_{5}$
**[R2] Proposition 5.3.**
$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.
$\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$
**[R3] Lemma 5.4.**
$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$
**[R4] (5.3) / Lemma 5.2.**
$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ が成り立つ.
**[R5] (5.2).**
$\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である.
**[R6] Proposition 5.1.**
$\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ.

まず、$\nu'$ を定める.

$2\eta_{3} = 0$

この前提条件を満たすので、Lemma 5.2 を適用できる.
Lemma 5.2 の $\beta$ を $\nu'$ と定めると、

$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$

次に、$\nu'$ の位数を決定するために、次の完全列を考える.

$\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$

$2\nu' = \eta_{3}E\eta_{3}\eta_{5}\tag{1}$

$\eta_{3}E\eta_{3}\eta_{5} = \eta_{3}^{3}\tag{2}$

$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$

以上より、

以上で得た群構造、生成元、および写像に関する結果を合わせると、

$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$

この完全性と $Δ=0$ より、$\ker E=\operatorname{Im}Δ=0$ である.
したがって、

$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.

$\operatorname{ord}(\eta_{3}\eta_{4}\eta_{5})=2$ かつ $2\nu'=\eta_{3}\eta_{4}\eta_{5}$ より、$4\nu'=0$ かつ $2\nu'\neq0$ である.
したがって、

$\operatorname{ord}\left(\nu'\right) = 4$

(1) と (2) より、

$2\nu' = \eta_{3}^{3}\tag{3}$

最後に、$\pi_{6}^{3}$ の群構造を決定するために、次の完全列を考える.

$\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}$

この完全性と、左の写像が単射、右の写像が全射であることより、次の短完全列を得る.

$0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$

以上より、

この短完全列と両端の群の位数より、中央の群の位数は $2\cdot2=4$ である.
また、$\nu'$ は中央の群に属し、$\operatorname{ord}(\nu')=4=4$ であるから、$\nu'$ は中央の群を生成する.
したがって、

$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$

## Decision boundary

- If both residual duplicate texts are transition/prose lines with different target contexts, keep them and close R4.
- If a mathematical fact is emitted twice from the same ProofStep ownership path, prepare R4 Fix2 using the upstream ownership rule rather than line-based deduplication.
- Reference linkage remains R5; punctuation remains R6.
