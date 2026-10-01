# Phase 153-R4 — 6-group n=2 Reference ancestry audit

This is an audit only. Production code is not modified.

## Summary

| group | refs | root-in-reference | root-selected | selected statements |
| --- | ---: | ---: | ---: | ---: |
| $\pi_{4}^{2}$ | 4 | 1 | 1 | 5 |
| $\pi_{5}^{2}$ | 8 | 1 | 1 | 17 |
| $\pi_{6}^{2}$ | 18 | 1 | 1 | 61 |
| $\pi_{7}^{2}$ | 17 | 1 | 1 | 62 |
| $\pi_{8}^{2}$ | 24 | 1 | 1 | 130 |
| $\pi_{9}^{2}$ | 27 | 1 | 1 | 164 |

## Interpretation guide

- `root in entry = YES`: the target/root step itself carries the same literature Reference.
- `root selected = YES`: the current statement-selection rule selected that root step for the Reference section.
- `premise = YES`: the step is actually used as a premise by at least one proof edge in the presentation.
- `distance→root`: shortest forward proof-edge distance from the step to the target/root; `0` means the root itself.
- R4 does not decide the new rule. It records the evidence needed to distinguish target/root ownership from actually used external premise/ancestry.

## Detailed audits

## $\pi_{4}^{2}$ (n=2, k=2)

- presentation nodes: 39
- proof edges: 40
- references: 4
- root statement: $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$

### [R1] (5.2)

- entry steps: 1
- root in entry: YES
- root selected: YES

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 0 | YES | YES | YES | no | 0 | — | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$ |

### [R2] (5.2)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 2 | no | YES | YES | YES | 1 | 0 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |

### [R3] Proposition 4.4

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 6 | no | YES | YES | YES | 2 | 2, 7 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 7 | no | YES | YES | YES | 2 | 2 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |

### [R4] Proposition 2.7

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 28 | no | YES | YES | YES | 6 | 24 | $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ. |

## $\pi_{5}^{2}$ (n=2, k=3)

- presentation nodes: 57
- proof edges: 60
- references: 8
- root statement: $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$

### [R1] Proposition 5.6

- entry steps: 1
- root in entry: YES
- root selected: YES

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 0 | YES | YES | YES | no | 0 | — | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$ |

### [R2] Proposition 5.3

- entry steps: 8
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 1 | no | YES | YES | YES | 1 | 0 | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$ |
| 4 | no | YES | YES | YES | 2 | 1 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である. |
| 5 | no | YES | YES | YES | 2 | 1 | $E\eta_{2}\eta_{3} = \eta_{3}^{2}$ |
| 10 | no | YES | YES | YES | 3 | 4 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は単射である. |
| 11 | no | YES | YES | YES | 3 | 4 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は全射である. |
| 20 | no | YES | YES | YES | 4 | 10 | $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像である. |
| 22 | no | YES | YES | YES | 4 | 11 | $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像である. |
| 30 | no | YES | YES | YES | 5 | 20 | $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である. |

### [R3] (5.2)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 2 | no | YES | YES | YES | 1 | 0, 3 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |

### [R4] (5.2)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 3 | no | YES | YES | YES | 2 | 1 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$ |

### [R5] Proposition 4.4

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 7 | no | YES | YES | YES | 2 | 2, 8 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 8 | no | YES | YES | YES | 2 | 2 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |

### [R6] Proposition 5.1

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 32 | no | YES | YES | YES | 5 | 22 | $\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射である. |

### [R7] Proposition 5.1

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 41 | no | YES | YES | YES | 6 | 30, 32 | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ. |

### [R8] (5.3)

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 49 | no | YES | YES | YES | 7 | 40 | $H\left(\nu'\right) = E^{2}\eta_{3}$ |
| 50 | no | YES | YES | YES | 7 | 40 | $E^{2}\eta_{3} = \eta_{5}$ |

## $\pi_{6}^{2}$ (n=2, k=4)

- presentation nodes: 156
- proof edges: 202
- references: 18
- root statement: $\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$

### [R1] Lemma 5.7

- entry steps: 1
- root in entry: YES
- root selected: YES

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 0 | YES | YES | YES | no | 0 | — | $\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$ |

### [R2] Proposition 5.6

- entry steps: 18
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 1 | no | YES | YES | YES | 1 | 0 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$, $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$, $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$, $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$, $n \ge 6$ が成り立つ. |
| 3 | no | YES | YES | YES | 2 | 1, 4, 38 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$ |
| 4 | no | YES | YES | YES | 2 | 1, 5, 6, 49 | $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$ |
| 5 | no | YES | YES | YES | 2 | 1 | $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$ |
| 6 | no | YES | YES | YES | 2 | 1, 26 | $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$ |
| 7 | no | YES | YES | YES | 2 | 1 | $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$ |
| 14 | no | YES | YES | YES | 3 | 4 | $\operatorname{ord}\left(\nu'\right) = 4$ |
| 16 | no | YES | YES | YES | 3 | 4, 38 | $E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である. |
| 22 | no | YES | YES | YES | 3 | 6 | $\operatorname{ord}\left(\nu_{5}\right) = 8$ |
| 24 | no | YES | YES | YES | 3 | 6, 49 | $E^{2}: \pi_{6}^{3} \to \pi_{8}^{5}$ は単射である. |
| 25 | no | YES | YES | YES | 3 | 6 | $\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right) \cong \mathbb{Z}/2$ |
| 26 | no | YES | YES | YES | 3 | 7 | $\pi_{n + 3}^{n} = \mathbb{Z}/8\{E^{n - 5}\nu_{5}\}$ |
| 27 | no | YES | YES | YES | 3 | 7 | $E^{n - 5}\nu_{5} = \nu_{n}$ |
| 38 | no | YES | YES | YES | 4 | 14 | $\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$ |
| 42 | no | YES | YES | YES | 4 | 16 | $\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である. |
| 48 | no | YES | YES | YES | 4 | 22 | $2\nu_{5} = E^{2}\nu'$ |
| 49 | no | YES | YES | YES | 4 | 22 | $\operatorname{ord}\left(E^{2}\nu'\right) = 4$ |
| 67 | no | YES | YES | YES | 5 | 42 | $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である. |

### [R3] (5.2)

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 2 | no | YES | YES | YES | 1 | 0 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 13 | no | no | no | YES | 3 | 3, 32 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |

### [R4] Proposition 4.4

- entry steps: 4
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 10 | no | YES | YES | YES | 2 | 2, 11 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 11 | no | YES | YES | YES | 2 | 2 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |
| 36 | no | no | no | YES | 4 | 13, 37 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 37 | no | no | no | YES | 4 | 13 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |

### [R5] Proposition 5.3

- entry steps: 12
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 12 | no | YES | YES | YES | 3 | 3, 97, 135 | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$ |
| 18 | no | YES | YES | YES | 3 | 4 | $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である. |
| 33 | no | YES | YES | YES | 4 | 12 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である. |
| 34 | no | YES | YES | YES | 4 | 12 | $E\eta_{2}\eta_{3} = \eta_{3}^{2}$ |
| 55 | no | YES | YES | YES | 5 | 33 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は単射である. |
| 56 | no | YES | YES | YES | 5 | 33 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は全射である. |
| 87 | no | YES | YES | YES | 6 | 55 | $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像である. |
| 89 | no | YES | YES | YES | 6 | 56 | $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像である. |
| 97 | no | YES | YES | YES | 6 | 67 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$, $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$, $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$, $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$, $n \ge 5$ が成り立つ. |
| 122 | no | no | no | YES | 7 | 87 | $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である. |
| 135 | no | YES | YES | YES | 7 | 97 | $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$ |
| 136 | no | YES | YES | YES | 7 | 97 | $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$ |

### [R6] (5.3)

- entry steps: 6
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 15 | no | YES | YES | YES | 3 | 4 | $\nu' \in \pi_{6}^{3}$ |
| 41 | no | YES | YES | YES | 4 | 15, 63, 69 | $2\eta_{3} = 0$ |
| 63 | no | YES | YES | YES | 5 | 39 | $2\nu' = \eta_{3}E\eta_{3}\eta_{5}$ |
| 69 | no | YES | YES | YES | 5 | 44 | $H\left(\nu'\right) = E^{2}\eta_{3}$ |
| 70 | no | YES | YES | YES | 5 | 44 | $E^{2}\eta_{3} = \eta_{5}$ |
| 128 | no | YES | YES | YES | 7 | 93 | $E\eta_{3} = \eta_{4}$ |

### [R7] Lemma 5.4

- entry steps: 8
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 19 | no | YES | YES | YES | 3 | 4 | $\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$ |
| 47 | no | YES | YES | YES | 4 | 20, 79, 107, 112 | $\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ. |
| 76 | no | YES | YES | YES | 5 | 47 | $\nu_{4} \in \pi_{7}^{4}$ |
| 77 | no | YES | YES | YES | 5 | 47 | $H\left(\nu_{4}\right) = \iota_{7}$ |
| 78 | no | YES | YES | YES | 5 | 47 | $2E\nu_{4} = E^{2}\nu'$ |
| 109 | no | YES | YES | YES | 6 | 76, 77, 78 | $\begin{cases} \nu_{4} = α* - (-1)^{u}s[\iota_{4}, \iota_{4}] & \text{if } 2Eα* = E^{2}\nu' \\ \nu_{4} = -α* + (-1)^{u}\left(s + 1\right)[\iota_{4}, \iota_{4}] & \text{if } 2Eα* = -E^{2}\nu' \end{cases}$ |
| 150 | no | YES | YES | YES | 7 | 109, 149 | $2Eα* = \pm E^{2}\nu'$ |
| 151 | no | YES | YES | YES | 7 | 109 | $H\left([\iota_{4}, \iota_{4}]\right) = 2\iota_{7},\quad E[\iota_{4}, \iota_{4}] = 0,\quad u\text{ is the sign parameter}$ |

### [R8] (5.2)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 32 | no | YES | YES | YES | 4 | 12, 97 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$ |

### [R9] (5.3) / Lemma 5.2

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 40 | no | YES | YES | YES | 4 | 15, 63, 69 | $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ が成り立つ. |

### [R10] Proposition 5.1

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 45 | no | YES | YES | YES | 4 | 18, 19, 122, 124 | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ. |

### [R11] (4.5)

- entry steps: 3
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 50 | no | YES | YES | YES | 4 | 26 | $E^{n - 5}: \pi_{5 + 3}^{5} \to \pi_{n + 3}^{n}$ は同型写像である. |
| 105 | no | YES | YES | YES | 6 | 74 | $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ |
| 146 | no | YES | YES | YES | 7 | 105 | $E^{n - 3}: \pi_{3 + 1}^{3} \to \pi_{n + 1}^{n}$ は同型写像である. |

### [R12] Proposition 4.4

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 75 | no | YES | YES | YES | 5 | 46 | $(α, \beta) \mapsto Eα + \nu_{4}\beta: \pi_{i - 1}^{3} \oplus \pi_{i}^{7} \to \pi_{i}^{4}$ は同型写像である. |

### [R13] (5.5)

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 79 | no | YES | YES | YES | 5 | 48 | $\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ. |
| 112 | no | YES | YES | YES | 6 | 79 | $2\nu_{n} = E^{n - 3}\nu'$ |

### [R14] Equation 5.7

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 96 | no | YES | YES | YES | 6 | 67 | $H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$ |

### [R15] Proposition 5.1

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 124 | no | YES | YES | YES | 7 | 89 | $\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射である. |

### [R16] Proposition 2.7

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 141 | no | YES | YES | YES | 7 | 104 | $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ. |

### [R17] (4.8)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 149 | no | YES | YES | YES | 7 | 109 | $H\left(α*\right) = \left(2s + 1\right)\iota_{7}$ |

### [R18] (5.4)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 153 | no | YES | YES | YES | 7 | 113 | $2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ |

## $\pi_{7}^{2}$ (n=2, k=5)

- presentation nodes: 123
- proof edges: 149
- references: 17
- root statement: $\pi_{7}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}$

### [R1] Proposition 5.9

- entry steps: 1
- root in entry: YES
- root selected: YES

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 0 | YES | YES | YES | no | 0 | — | $\pi_{7}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}$ |

### [R2] Proposition 5.8

- entry steps: 3
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 1 | no | YES | YES | YES | 1 | 0 | $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$ |
| 9 | no | YES | YES | YES | 3 | 3 | $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は単射である. |
| 25 | no | YES | YES | YES | 4 | 9 | $\pi_{6}^{2} \xrightarrow{E} \pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \text{ is exact}$ |

### [R3] (5.2)

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 2 | no | YES | YES | YES | 1 | 0, 14, 24 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 94 | no | no | no | YES | 7 | 63 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |

### [R4] Equation 5.7

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 4 | no | YES | YES | YES | 2 | 1, 10 | $H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$ |

### [R5] Proposition 5.3

- entry steps: 19
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 5 | no | YES | YES | YES | 2 | 1, 10 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$, $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$, $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$, $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$, $n \ge 5$ が成り立つ. |
| 15 | no | YES | YES | YES | 3 | 5, 16 | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$ |
| 16 | no | YES | YES | YES | 3 | 5, 33 | $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$ |
| 17 | no | YES | YES | YES | 3 | 5 | $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$ |
| 29 | no | YES | YES | YES | 4 | 15 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である. |
| 30 | no | YES | YES | YES | 4 | 15 | $E\eta_{2}\eta_{3} = \eta_{3}^{2}$ |
| 31 | no | YES | YES | YES | 4 | 16 | $E: \pi_{5}^{3} \to \pi_{6}^{4}$ は同型写像である. |
| 32 | no | YES | YES | YES | 4 | 16 | $E\eta_{3}\eta_{4} = \eta_{4}^{2}$ |
| 33 | no | YES | YES | YES | 4 | 17 | $\pi_{n + 2}^{n} = \mathbb{Z}/2\{E^{n - 4}\eta_{4}\eta_{5}\}$ |
| 34 | no | YES | YES | YES | 4 | 17 | $E^{n - 4}\eta_{4}\eta_{5} = \eta_{n}\eta_{n + 1}$ |
| 47 | no | YES | YES | YES | 5 | 29 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は単射である. |
| 48 | no | YES | YES | YES | 5 | 29 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は全射である. |
| 51 | no | YES | YES | YES | 5 | 31 | $E: \pi_{5}^{3} \to \pi_{6}^{4}$ は単射である. |
| 52 | no | YES | YES | YES | 5 | 31 | $E: \pi_{5}^{3} \to \pi_{6}^{4}$ は全射である. |
| 75 | no | YES | YES | YES | 6 | 47 | $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像である. |
| 77 | no | YES | YES | YES | 6 | 48 | $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像である. |
| 93 | no | no | no | YES | 7 | 63 | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$ |
| 99 | no | YES | YES | YES | 7 | 64 | $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である. |
| 115 | no | no | no | YES | 7 | 75 | $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である. |

### [R6] Proposition 4.4

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 7 | no | YES | YES | YES | 2 | 2, 8 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 8 | no | YES | YES | YES | 2 | 2 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |

### [R7] Proposition 5.6

- entry steps: 14
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 10 | no | YES | YES | YES | 3 | 3 | $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である. |
| 39 | no | YES | YES | YES | 5 | 24 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$, $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$, $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$, $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$, $n \ge 6$ が成り立つ. |
| 63 | no | YES | YES | YES | 6 | 39, 64 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$ |
| 64 | no | YES | YES | YES | 6 | 39, 65, 66 | $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$ |
| 65 | no | YES | YES | YES | 6 | 39 | $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$ |
| 66 | no | YES | YES | YES | 6 | 39, 107 | $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$ |
| 67 | no | YES | YES | YES | 6 | 39 | $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$ |
| 95 | no | YES | YES | YES | 7 | 64 | $\operatorname{ord}\left(\nu'\right) = 4$ |
| 97 | no | YES | YES | YES | 7 | 64 | $E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である. |
| 103 | no | YES | YES | YES | 7 | 66 | $\operatorname{ord}\left(\nu_{5}\right) = 8$ |
| 105 | no | YES | YES | YES | 7 | 66 | $E^{2}: \pi_{6}^{3} \to \pi_{8}^{5}$ は単射である. |
| 106 | no | YES | YES | YES | 7 | 66 | $\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right) \cong \mathbb{Z}/2$ |
| 107 | no | YES | YES | YES | 7 | 67 | $\pi_{n + 3}^{n} = \mathbb{Z}/8\{E^{n - 5}\nu_{5}\}$ |
| 108 | no | YES | YES | YES | 7 | 67 | $E^{n - 5}\nu_{5} = \nu_{n}$ |

### [R8] (5.2)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 14 | no | YES | YES | YES | 3 | 5, 15 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$ |

### [R9] Lemma 4.5

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 23 | no | YES | YES | YES | 4 | 9 | $E\eta_{2}\nu' = 0$ |

### [R10] Lemma 5.7

- entry steps: 4
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 24 | no | YES | YES | YES | 4 | 9 | $\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$ |
| 37 | no | YES | YES | YES | 5 | 23, 38, 61 | $E^{2}\nu' \in 2\iota_{5}\circ \pi_{8}^{5}$ |
| 38 | no | YES | YES | YES | 5 | 23 | $E^{2}\eta_{2}\nu' = 0$ |
| 61 | no | YES | YES | YES | 6 | 38 | $E^{2}\eta_{2}\nu' = \eta_{4}E^{2}\nu'$ |

### [R11] (5.3)

- entry steps: 4
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 26 | no | YES | YES | YES | 4 | 11 | $H\left(\nu'\right) = E^{2}\eta_{3}$ |
| 27 | no | YES | YES | YES | 4 | 11 | $E^{2}\eta_{3} = \eta_{5}$ |
| 42 | no | YES | YES | YES | 5 | 26 | $2\eta_{3} = 0$ |
| 96 | no | YES | YES | YES | 7 | 64 | $\nu' \in \pi_{6}^{3}$ |

### [R12] (5.3) / Lemma 5.2

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 41 | no | YES | YES | YES | 5 | 26 | $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ が成り立つ. |

### [R13] (4.5)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 55 | no | YES | YES | YES | 5 | 33 | $E^{n - 4}: \pi_{4 + 2}^{4} \to \pi_{n + 2}^{n}$ は同型写像である. |

### [R14] Lemma 5.4

- entry steps: 5
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 59 | no | YES | YES | YES | 6 | 37 | $\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ. |
| 89 | no | YES | YES | YES | 7 | 59 | $\nu_{4} \in \pi_{7}^{4}$ |
| 90 | no | YES | YES | YES | 7 | 59 | $H\left(\nu_{4}\right) = \iota_{7}$ |
| 91 | no | YES | YES | YES | 7 | 59 | $2E\nu_{4} = E^{2}\nu'$ |
| 100 | no | YES | YES | YES | 7 | 64 | $\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$ |

### [R15] Proposition 5.1

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 62 | no | YES | YES | YES | 6 | 38 | $2\eta_{4} = 0$ |
| 117 | no | YES | YES | YES | 7 | 77 | $\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射である. |

### [R16] Proposition 4.4

- entry steps: 3
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 79 | no | YES | YES | YES | 6 | 51 | $E: \pi_{6 - 1}^{4 - 1} \to \pi_{6}^{4}$ は単射である. |
| 119 | no | YES | YES | YES | 7 | 79 | $(\beta, γ) \mapsto E\beta + αγ: \pi_{6 - 1}^{4 - 1} \oplus \pi_{6}^{2\,4 - 1} \to \pi_{6}^{4}$ は同型写像である. |
| 120 | no | YES | YES | YES | 7 | 79 | $\left.\left(E\beta + αγ\right)\right\|_{\pi_{6 - 1}^{4 - 1}} = E: \pi_{6 - 1}^{4 - 1} \to \pi_{6}^{4}$ |

### [R17] Proposition 5.1

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 92 | no | YES | YES | YES | 7 | 62, 115, 117 | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ. |

## $\pi_{8}^{2}$ (n=2, k=6)

- presentation nodes: 244
- proof edges: 343
- references: 24
- root statement: $\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}$

### [R1] Proposition 5.11

- entry steps: 1
- root in entry: YES
- root selected: YES

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 0 | YES | YES | YES | no | 0 | — | $\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}$ |

### [R2] Proposition 5.9

- entry steps: 33
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 1 | no | YES | YES | YES | 1 | 0 | $\pi_{7}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}$, $\pi_{8}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\eta_{7}\}$, $\pi_{9}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\eta_{8}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\eta_{8}\}$, $\pi_{10}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\eta_{9}\}$, $\pi_{11}^{6} = \mathbb{Z}\{\Delta\left(\iota_{13}\right)\}$, $\pi_{n + 5}^{n} = 0$, $n \ge 7$ が成り立つ. |
| 3 | no | YES | YES | YES | 2 | 1, 14, 37 | $\pi_{7}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}$ |
| 4 | no | YES | YES | YES | 2 | 1, 5, 20 | $\pi_{8}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\eta_{7}\}$ |
| 5 | no | YES | YES | YES | 2 | 1, 6, 21, 24 | $\pi_{9}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\eta_{8}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\eta_{8}\}$ |
| 6 | no | YES | YES | YES | 2 | 1, 25, 57 | $\pi_{10}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\eta_{9}\}$ |
| 7 | no | YES | YES | YES | 2 | 1, 64 | $\pi_{11}^{6} = \mathbb{Z}\{\Delta\left(\iota_{13}\right)\}$ |
| 8 | no | YES | YES | YES | 2 | 1 | $\pi_{n + 5}^{n} = 0$ |
| 14 | no | YES | YES | YES | 3 | 4 | $H: \pi_{8}^{3} \to \pi_{8}^{5}$ は単射である. |
| 15 | no | YES | YES | YES | 3 | 4 | $\pi_{8}^{3} \xrightarrow{H} \pi_{8}^{5} \xrightarrow{\Delta} \pi_{6}^{2} \text{ is exact}$ |
| 16 | no | YES | YES | YES | 3 | 4 | $\ker\left(\Delta: \pi_{8}^{5} \to \pi_{6}^{2}\right) = \mathbb{Z}/2\{4\nu_{5}\}$ |
| 17 | no | YES | YES | YES | 3 | 4 | $H\left(\nu'\eta_{6}\eta_{7}\right) = 4\nu_{5}$ |
| 20 | no | YES | YES | YES | 3 | 5 | $E\nu'\eta_{6}\eta_{7} = E\nu'\eta_{7}^{2}$ |
| 21 | no | YES | YES | YES | 3 | 6 | $\Delta\left(\eta_{9}\eta_{10}\right) = E\nu'\eta_{7}^{2}$ |
| 22 | no | YES | YES | YES | 3 | 6 | $\pi_{11}^{9} \xrightarrow{\Delta} \pi_{9}^{4} \xrightarrow{E} \pi_{10}^{5} \text{ is exact}$ |
| 23 | no | YES | YES | YES | 3 | 6 | $E: \pi_{9}^{4} \to \pi_{10}^{5}$ は全射である. |
| 24 | no | YES | YES | YES | 3 | 6 | $E\nu_{4}\eta_{7}\eta_{8} = \nu_{5}\eta_{8}^{2}$ |
| 25 | no | YES | YES | YES | 3 | 7 | $H: \pi_{11}^{6} \to \pi_{11}^{11}$ は単射である. |
| 26 | no | YES | YES | YES | 3 | 7 | $\pi_{11}^{6} \xrightarrow{H} \pi_{11}^{11} \xrightarrow{\Delta} \pi_{9}^{5} \text{ is exact}$ |
| 27 | no | YES | YES | YES | 3 | 7 | $\ker\Delta = \mathbb{Z}\{2\iota_{11}\}$ が成り立つ. |
| 28 | no | YES | YES | YES | 3 | 7 | $H(\Delta\left(\iota_{13}\right)) = \pm 2\iota_{11}$ が成り立つ. |
| 29 | no | YES | YES | YES | 3 | 8 | $\pi_{12}^{7} = 0$ |
| 37 | no | YES | YES | YES | 4 | 14 | $E\eta_{2}\nu'\eta_{6} = 0$ |
| 38 | no | YES | YES | YES | 4 | 14 | $\pi_{7}^{2} \xrightarrow{E} \pi_{8}^{3} \xrightarrow{H} \pi_{8}^{5} \text{ is exact}$ |
| 54 | no | YES | YES | YES | 4 | 23 | $H: \pi_{10}^{5} \to \pi_{10}^{9}$ は零写像である. |
| 55 | no | YES | YES | YES | 4 | 23 | $\pi_{9}^{4} \xrightarrow{E} \pi_{10}^{5} \xrightarrow{H} \pi_{10}^{9} \text{ is exact}$ |
| 57 | no | YES | YES | YES | 4 | 25 | $E\nu_{5}\eta_{8}\eta_{9} = 0$ |
| 58 | no | YES | YES | YES | 4 | 25 | $\pi_{10}^{5} \xrightarrow{E} \pi_{11}^{6} \xrightarrow{H} \pi_{11}^{11} \text{ is exact}$ |
| 64 | no | YES | YES | YES | 4 | 29 | $\Delta: \pi_{13}^{13} \to \pi_{11}^{6}$ は全射である. |
| 65 | no | YES | YES | YES | 4 | 29 | $\pi_{13}^{13} \xrightarrow{\Delta} \pi_{11}^{6} \xrightarrow{E} \pi_{12}^{7} \text{ is exact}$ |
| 66 | no | YES | YES | YES | 4 | 29 | $E: \pi_{11}^{6} \to \pi_{12}^{7}$ は全射である. |
| 103 | no | YES | YES | YES | 5 | 54 | $\Delta: \pi_{10}^{9} \to \pi_{8}^{4}$ は単射である. |
| 104 | no | YES | YES | YES | 5 | 54 | $\pi_{10}^{5} \xrightarrow{H} \pi_{10}^{9} \xrightarrow{\Delta} \pi_{8}^{4} \text{ is exact}$ |
| 116 | no | YES | YES | YES | 5 | 66 | $\pi_{11}^{6} \xrightarrow{E} \pi_{12}^{7} \xrightarrow{H} \pi_{12}^{13} \text{ is exact}$ |

### [R3] (5.2)

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 2 | no | YES | YES | YES | 1 | 0, 3, 42, 47 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 186 | no | no | no | YES | 7 | 125 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |

### [R4] Proposition 4.4

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 11 | no | YES | YES | YES | 2 | 2, 12 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 12 | no | YES | YES | YES | 2 | 2 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |

### [R5] Proposition 5.8

- entry steps: 19
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 13 | no | YES | YES | YES | 3 | 3, 102, 156 | $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$ |
| 52 | no | YES | YES | YES | 4 | 21, 61, 103 | $\Delta\left(\eta_{9}\right) = E\nu'\eta_{7}$ |
| 56 | no | YES | YES | YES | 4 | 24 | $E\nu_{4}\eta_{7} = \nu_{5}\eta_{8}$ |
| 61 | no | YES | YES | YES | 4 | 27, 62, 169 | $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$ |
| 72 | no | YES | YES | YES | 5 | 35 | $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は単射である. |
| 102 | no | YES | YES | YES | 5 | 52, 56, 61, 103, 112 | $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$ |
| 110 | no | YES | YES | YES | 5 | 61 | $\pi_{10}^{9} \xrightarrow{\Delta} \pi_{8}^{4} \xrightarrow{E} \pi_{9}^{5} \text{ is exact}$ |
| 111 | no | YES | YES | YES | 5 | 61 | $E: \pi_{8}^{4} \to \pi_{9}^{5}$ は全射である. |
| 112 | no | no | no | YES | 5 | 61 | $E\nu_{4}\eta_{7} = \nu_{5}\eta_{8}$ |
| 119 | no | YES | YES | YES | 6 | 72 | $\pi_{6}^{2} \xrightarrow{E} \pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \text{ is exact}$ |
| 156 | no | YES | YES | YES | 6 | 102 | $E\nu'\eta_{6} = E\nu'\eta_{7}$ |
| 162 | no | YES | YES | YES | 6 | 108 | $\eta_{6}\nu_{7} = 0$ |
| 166 | no | YES | YES | YES | 6 | 111 | $H: \pi_{9}^{5} \to \pi_{9}^{9}$ は零写像である. |
| 167 | no | YES | YES | YES | 6 | 111 | $\pi_{8}^{4} \xrightarrow{E} \pi_{9}^{5} \xrightarrow{H} \pi_{9}^{9} \text{ is exact}$ |
| 169 | no | YES | YES | YES | 6 | 113 | $\pi_{10}^{6} = 0$ |
| 232 | no | YES | YES | YES | 7 | 162 | $\eta_{n}\nu_{n + 1} = 0$ |
| 237 | no | YES | YES | YES | 7 | 166 | $\Delta: \pi_{9}^{9} \to \pi_{7}^{4}$ は単射である. |
| 238 | no | YES | YES | YES | 7 | 166 | $\pi_{9}^{5} \xrightarrow{H} \pi_{9}^{9} \xrightarrow{\Delta} \pi_{7}^{4} \text{ is exact}$ |
| 240 | no | YES | YES | YES | 7 | 169 | $E: \pi_{9}^{5} \to \pi_{10}^{6}$ は全射である. |

### [R6] Proposition 5.3

- entry steps: 18
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 19 | no | YES | YES | YES | 3 | 5, 6, 13, 20, 73 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$, $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$, $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$, $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$, $n \ge 5$ が成り立つ. |
| 48 | no | YES | YES | YES | 4 | 19, 49 | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$ |
| 49 | no | YES | YES | YES | 4 | 19, 99 | $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$ |
| 50 | no | YES | YES | YES | 4 | 19 | $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$ |
| 95 | no | YES | YES | YES | 5 | 48 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である. |
| 96 | no | YES | YES | YES | 5 | 48 | $E\eta_{2}\eta_{3} = \eta_{3}^{2}$ |
| 97 | no | YES | YES | YES | 5 | 49 | $E: \pi_{5}^{3} \to \pi_{6}^{4}$ は同型写像である. |
| 98 | no | YES | YES | YES | 5 | 49 | $E\eta_{3}\eta_{4} = \eta_{4}^{2}$ |
| 99 | no | YES | YES | YES | 5 | 50 | $\pi_{n + 2}^{n} = \mathbb{Z}/2\{E^{n - 4}\eta_{4}\eta_{5}\}$ |
| 100 | no | YES | YES | YES | 5 | 50 | $E^{n - 4}\eta_{4}\eta_{5} = \eta_{n}\eta_{n + 1}$ |
| 135 | no | YES | YES | YES | 6 | 83 | $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である. |
| 145 | no | YES | YES | YES | 6 | 95 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は単射である. |
| 146 | no | YES | YES | YES | 6 | 95 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は全射である. |
| 149 | no | YES | YES | YES | 6 | 97 | $E: \pi_{5}^{3} \to \pi_{6}^{4}$ は単射である. |
| 150 | no | YES | YES | YES | 6 | 97 | $E: \pi_{5}^{3} \to \pi_{6}^{4}$ は全射である. |
| 185 | no | no | no | YES | 7 | 125 | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$ |
| 212 | no | YES | YES | YES | 7 | 145 | $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像である. |
| 214 | no | YES | YES | YES | 7 | 146 | $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像である. |

### [R7] (4.5)

- entry steps: 3
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 30 | no | YES | YES | YES | 3 | 8 | $E^{n - 7}: \pi_{7 + 5}^{7} \to \pi_{n + 5}^{n}$ は同型写像である. |
| 153 | no | YES | YES | YES | 6 | 99 | $E^{n - 4}: \pi_{4 + 2}^{4} \to \pi_{n + 2}^{n}$ は同型写像である. |
| 230 | no | YES | YES | YES | 7 | 161 | $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ |

### [R8] Equation 5.7

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 36 | no | YES | YES | YES | 4 | 13, 17, 73 | $H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$ |

### [R9] Lemma 5.7

- entry steps: 7
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 40 | no | YES | YES | YES | 4 | 16 | $\Delta\left(\nu_{5}\right) = \pm \eta_{2}\nu'$ |
| 42 | no | YES | YES | YES | 4 | 16, 40, 72, 79 | $\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$ |
| 79 | no | YES | YES | YES | 5 | 40 | $\Delta: \pi_{8}^{5} \to \pi_{6}^{2}$ は全射である. |
| 122 | no | YES | YES | YES | 6 | 77, 123, 182 | $E^{2}\nu' \in 2\iota_{5}\circ \pi_{8}^{5}$ |
| 123 | no | YES | YES | YES | 6 | 77 | $E^{2}\eta_{2}\nu' = 0$ |
| 124 | no | YES | YES | YES | 6 | 79 | $\pi_{8}^{5} \xrightarrow{\Delta} \pi_{6}^{2} \xrightarrow{E} \pi_{7}^{3} \text{ is exact}$ |
| 182 | no | YES | YES | YES | 7 | 123 | $E^{2}\eta_{2}\nu' = \eta_{4}E^{2}\nu'$ |

### [R10] Proposition 5.6

- entry steps: 18
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 41 | no | YES | YES | YES | 4 | 16, 17, 80, 188 | $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$ |
| 73 | no | YES | YES | YES | 5 | 35 | $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である. |
| 80 | no | YES | YES | YES | 5 | 40, 42, 237 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$, $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$, $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$, $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$, $n \ge 6$ が成り立つ. |
| 81 | no | YES | YES | YES | 5 | 41 | $\operatorname{ord}\left(\nu_{5}\right) = 8$ |
| 83 | no | YES | YES | YES | 5 | 41, 80, 126, 130 | $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$ |
| 84 | no | YES | YES | YES | 5 | 41, 130 | $E^{2}: \pi_{6}^{3} \to \pi_{8}^{5}$ は単射である. |
| 85 | no | YES | YES | YES | 5 | 41 | $\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right) \cong \mathbb{Z}/2$ |
| 125 | no | YES | YES | YES | 6 | 80, 83, 191 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$ |
| 126 | no | YES | YES | YES | 6 | 80, 222 | $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$ |
| 127 | no | YES | YES | YES | 6 | 80 | $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$ |
| 129 | no | YES | YES | YES | 6 | 81 | $2\nu_{5} = E^{2}\nu'$ |
| 130 | no | YES | YES | YES | 6 | 81 | $\operatorname{ord}\left(E^{2}\nu'\right) = 4$ |
| 131 | no | YES | YES | YES | 6 | 83 | $\operatorname{ord}\left(\nu'\right) = 4$ |
| 133 | no | YES | YES | YES | 6 | 83, 191 | $E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である. |
| 188 | no | YES | YES | YES | 7 | 127 | $\pi_{n + 3}^{n} = \mathbb{Z}/8\{E^{n - 5}\nu_{5}\}$ |
| 189 | no | YES | YES | YES | 7 | 127 | $E^{n - 5}\nu_{5} = \nu_{n}$ |
| 191 | no | YES | YES | YES | 7 | 131 | $\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$ |
| 195 | no | YES | YES | YES | 7 | 133 | $\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である. |

### [R11] (5.5)

- entry steps: 3
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 43 | no | YES | YES | YES | 4 | 17, 162, 232 | $\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ. |
| 88 | no | YES | YES | YES | 5 | 43, 202 | $2\nu_{n} = E^{n - 3}\nu'$ |
| 190 | no | no | no | YES | 7 | 129 | $\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ. |

### [R12] Lemma 5.4

- entry steps: 9
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 46 | no | YES | YES | YES | 4 | 18, 43, 88, 122, 140 | $\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ. |
| 91 | no | YES | YES | YES | 5 | 46 | $\nu_{4} \in \pi_{7}^{4}$ |
| 92 | no | YES | YES | YES | 5 | 46 | $H\left(\nu_{4}\right) = \iota_{7}$ |
| 93 | no | YES | YES | YES | 5 | 46 | $2E\nu_{4} = E^{2}\nu'$ |
| 136 | no | YES | YES | YES | 6 | 83 | $\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$ |
| 142 | no | YES | YES | YES | 6 | 91, 92, 93 | $\begin{cases} \nu_{4} = α* - (-1)^{u}s[\iota_{4}, \iota_{4}] & \text{if } 2Eα* = E^{2}\nu' \\ \nu_{4} = -α* + (-1)^{u}\left(s + 1\right)[\iota_{4}, \iota_{4}] & \text{if } 2Eα* = -E^{2}\nu' \end{cases}$ |
| 200 | no | no | no | YES | 7 | 137, 190 | $\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ. |
| 206 | no | YES | YES | YES | 7 | 142, 205 | $2Eα* = \pm E^{2}\nu'$ |
| 207 | no | YES | YES | YES | 7 | 142, 223 | $H\left([\iota_{4}, \iota_{4}]\right) = 2\iota_{7},\quad E[\iota_{4}, \iota_{4}] = 0,\quad u\text{ is the sign parameter}$ |

### [R13] (5.2)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 47 | no | YES | YES | YES | 4 | 19, 48 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$ |

### [R14] Lemma 4.5

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 77 | no | YES | YES | YES | 5 | 37, 72, 79 | $E\eta_{2}\nu' = 0$ |

### [R15] Proposition 4.4

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 90 | no | YES | YES | YES | 5 | 45 | $(α, \beta) \mapsto Eα + \nu_{4}\beta: \pi_{i - 1}^{3} \oplus \pi_{i}^{7} \to \pi_{i}^{4}$ は同型写像である. |
| 216 | no | YES | YES | YES | 7 | 149 | $E: \pi_{6 - 1}^{4 - 1} \to \pi_{6}^{4}$ は単射である. |

### [R16] Proposition 2.5

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 101 | no | YES | YES | YES | 5 | 52 | $\Delta\left(\eta_{9}\right) = \pm 2\nu_{4} - E\nu'\eta_{7}$ |

### [R17] Proposition 5.1

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 106 | no | YES | YES | YES | 5 | 56, 61, 102, 103, 112, 156, 183 | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ. |
| 198 | no | no | no | YES | 7 | 135, 136 | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ. |

### [R18] Proposition 3.1

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 108 | no | YES | YES | YES | 5 | 57, 169 | $\nu_{6}\eta_{9} = 0$ |

### [R19] (5.3)

- entry steps: 5
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 120 | no | YES | YES | YES | 6 | 74 | $H\left(\nu'\right) = E^{2}\eta_{3}$ |
| 121 | no | YES | YES | YES | 6 | 74 | $E^{2}\eta_{3} = \eta_{5}$ |
| 132 | no | YES | YES | YES | 6 | 83 | $\nu' \in \pi_{6}^{3}$ |
| 178 | no | YES | YES | YES | 7 | 120 | $2\eta_{3} = 0$ |
| 194 | no | no | no | YES | 7 | 132 | $2\eta_{3} = 0$ |

### [R20] (5.4)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 139 | no | YES | YES | YES | 6 | 89 | $2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ |

### [R21] Equation 5.8

- entry steps: 4
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 155 | no | YES | YES | YES | 6 | 101, 237 | $\Delta\left(\iota_{9}\right) = \pm \left(2\nu_{4} - E\nu'\right) = \pm [\iota_{4}, \iota_{4}]$ |
| 222 | no | YES | YES | YES | 7 | 155, 223, 224 | $\Delta\left(\iota_{9}\right) = \pm \left(2\nu_{4} - E\nu'\right)$ |
| 223 | no | YES | YES | YES | 7 | 155, 224 | $[\iota_{4}, \iota_{4}] = \pm \left(2\nu_{4} - E\nu'\right)$ |
| 224 | no | YES | YES | YES | 7 | 155 | $\Delta\left(\iota_{9}\right) = \pm [\iota_{4}, \iota_{4}]$ |

### [R22] (5.3) / Lemma 5.2

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 177 | no | YES | YES | YES | 7 | 120 | $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ が成り立つ. |
| 193 | no | no | no | YES | 7 | 132 | $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ が成り立つ. |

### [R23] Proposition 5.1

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 183 | no | YES | YES | YES | 7 | 123 | $2\eta_{4} = 0$ |

### [R24] (4.8)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 205 | no | YES | YES | YES | 7 | 142 | $H\left(α*\right) = \left(2s + 1\right)\iota_{7}$ |

## $\pi_{9}^{2}$ (n=2, k=7)

- presentation nodes: 311
- proof edges: 453
- references: 27
- root statement: $\pi_{9}^{2} = 0$

### [R1] Proposition 5.15

- entry steps: 1
- root in entry: YES
- root selected: YES

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 0 | YES | YES | YES | no | 0 | — | $\pi_{9}^{2} = 0$ |

### [R2] Proposition 5.11

- entry steps: 42
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 1 | no | YES | YES | YES | 1 | 0 | $\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}$, $\pi_{9}^{3} = 0$, $\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$, $\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}\nu_{8}\}$, $\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}\nu_{9}\}$, $\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}\nu_{10}\}$, $\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}\nu_{11}\}$, $\pi_{n + 6}^{n} = \mathbb{Z}/2\{\nu_{n}\nu_{n + 3}\}$, $n \ge 9$ が成り立つ. |
| 3 | no | YES | YES | YES | 2 | 1, 37 | $\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}$ |
| 4 | no | YES | YES | YES | 2 | 1, 5, 46 | $\pi_{9}^{3} = 0$ |
| 5 | no | YES | YES | YES | 2 | 1, 17, 46 | $\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$ |
| 6 | no | YES | YES | YES | 2 | 1 | $\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}\nu_{8}\}$, $\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}\nu_{9}\}$, $\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}\nu_{10}\}$, $\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}\nu_{11}\}$, $\pi_{n + 6}^{n} = \mathbb{Z}/2\{\nu_{n}\nu_{n + 3}\}$, $n \ge 9$ が成り立つ. |
| 12 | no | YES | YES | YES | 3 | 4 | $H: \pi_{9}^{3} \to \pi_{9}^{5}$ は単射である. |
| 13 | no | YES | YES | YES | 3 | 4 | $\Delta: \pi_{9}^{5} \to \pi_{7}^{2}$ は単射である. |
| 14 | no | YES | YES | YES | 3 | 4 | $\pi_{9}^{3} \xrightarrow{H} \pi_{9}^{5} \xrightarrow{\Delta} \pi_{7}^{2} \text{ is exact}$ |
| 15 | no | YES | YES | YES | 3 | 5 | $\pi_{10}^{7} = \mathbb{Z}/8\{\nu_{7}\}$ |
| 17 | no | YES | YES | YES | 3 | 6, 18 | $\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}\nu_{8}\}$ |
| 18 | no | YES | YES | YES | 3 | 6, 19 | $\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}\nu_{9}\}$ |
| 19 | no | YES | YES | YES | 3 | 6, 20 | $\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}\nu_{10}\}$ |
| 20 | no | YES | YES | YES | 3 | 6, 21 | $\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}\nu_{11}\}$ |
| 21 | no | YES | YES | YES | 3 | 6 | $\pi_{n + 6}^{n} = \mathbb{Z}/2\{\nu_{n}\nu_{n + 3}\}$ |
| 37 | no | YES | YES | YES | 4 | 12 | $E: \pi_{8}^{2} \to \pi_{9}^{3} \text{ is the zero map}$ |
| 38 | no | YES | YES | YES | 4 | 12 | $\pi_{8}^{2} \xrightarrow{E} \pi_{9}^{3} \xrightarrow{H} \pi_{9}^{5} \text{ is exact}$ |
| 39 | no | YES | YES | YES | 4 | 13 | $\Delta: \pi_{9}^{5} \to \pi_{7}^{2}$ は全射である. |
| 45 | no | YES | YES | YES | 4 | 17 | $\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}$ |
| 47 | no | YES | YES | YES | 4 | 17 | $\pi_{12}^{9} \xrightarrow{\Delta} \pi_{10}^{4} \xrightarrow{E} \pi_{11}^{5} \text{ is exact}$ |
| 48 | no | YES | YES | YES | 4 | 17 | $E: \pi_{10}^{4} \to \pi_{11}^{5}$ は全射である. |
| 49 | no | YES | YES | YES | 4 | 18 | $E: \pi_{11}^{5} \to \pi_{12}^{6}$ は同型写像である. |
| 50 | no | YES | YES | YES | 4 | 19 | $E: \pi_{12}^{6} \to \pi_{13}^{7}$ は同型写像である. |
| 51 | no | YES | YES | YES | 4 | 20 | $E: \pi_{13}^{7} \to \pi_{14}^{8}$ は同型写像である. |
| 78 | no | YES | YES | YES | 5 | 39 | $E: \pi_{7}^{2} \to \pi_{8}^{3} \text{ is the zero map}$ |
| 79 | no | YES | YES | YES | 5 | 39 | $\pi_{9}^{5} \xrightarrow{\Delta} \pi_{7}^{2} \xrightarrow{E} \pi_{8}^{3} \text{ is exact}$ |
| 98 | no | YES | YES | YES | 5 | 48 | $H: \pi_{11}^{5} \to \pi_{11}^{9}$ は零写像である. |
| 99 | no | YES | YES | YES | 5 | 48 | $\pi_{10}^{4} \xrightarrow{E} \pi_{11}^{5} \xrightarrow{H} \pi_{11}^{9} \text{ is exact}$ |
| 100 | no | YES | YES | YES | 5 | 49 | $E: \pi_{11}^{5} \to \pi_{12}^{6}$ は単射である. |
| 101 | no | YES | YES | YES | 5 | 49 | $E: \pi_{11}^{5} \to \pi_{12}^{6}$ は全射である. |
| 102 | no | YES | YES | YES | 5 | 50 | $E: \pi_{12}^{6} \to \pi_{13}^{7}$ は単射である. |
| 103 | no | YES | YES | YES | 5 | 50 | $E: \pi_{12}^{6} \to \pi_{13}^{7}$ は全射である. |
| 185 | no | YES | YES | YES | 6 | 98 | $\pi_{11}^{5} \xrightarrow{H} \pi_{11}^{9} \xrightarrow{\Delta} \pi_{9}^{4} \text{ is exact}$ |
| 187 | no | YES | YES | YES | 6 | 100 | $\pi_{13}^{11} = \mathbb{Z}/2\{\eta_{11}\eta_{12}\}$ |
| 189 | no | YES | YES | YES | 6 | 100 | $\pi_{13}^{11} \xrightarrow{\Delta} \pi_{11}^{5} \xrightarrow{E} \pi_{12}^{6} \text{ is exact}$ |
| 190 | no | YES | YES | YES | 6 | 101 | $H: \pi_{12}^{6} \to \pi_{12}^{11}$ は零写像である. |
| 191 | no | YES | YES | YES | 6 | 101 | $\pi_{11}^{5} \xrightarrow{E} \pi_{12}^{6} \xrightarrow{H} \pi_{12}^{11} \text{ is exact}$ |
| 192 | no | YES | YES | YES | 6 | 102 | $\pi_{14}^{13} = \mathbb{Z}/2\{\eta_{13}\}$ |
| 194 | no | YES | YES | YES | 6 | 102 | $\pi_{14}^{13} \xrightarrow{\Delta} \pi_{12}^{6} \xrightarrow{E} \pi_{13}^{7} \text{ is exact}$ |
| 195 | no | YES | YES | YES | 6 | 103 | $H: \pi_{13}^{7} \to \pi_{13}^{13}$ は零写像である. |
| 196 | no | YES | YES | YES | 6 | 103 | $\pi_{12}^{6} \xrightarrow{E} \pi_{13}^{7} \xrightarrow{H} \pi_{13}^{13} \text{ is exact}$ |
| 301 | no | YES | YES | YES | 7 | 190 | $\pi_{12}^{6} \xrightarrow{H} \pi_{12}^{11} \xrightarrow{\Delta} \pi_{10}^{5} \text{ is exact}$ |
| 307 | no | YES | YES | YES | 7 | 195 | $\pi_{13}^{7} \xrightarrow{H} \pi_{13}^{13} \xrightarrow{\Delta} \pi_{11}^{6} \text{ is exact}$ |

### [R3] (5.2)

- entry steps: 4
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 2 | no | YES | YES | YES | 1 | 0 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 11 | no | no | no | YES | 3 | 3, 27, 117, 120 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 149 | no | no | no | YES | 6 | 80, 254 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 163 | no | no | no | YES | 6 | 86, 275 | $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |

### [R4] Proposition 4.4

- entry steps: 8
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 8 | no | YES | YES | YES | 2 | 2, 9 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 9 | no | YES | YES | YES | 2 | 2 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |
| 35 | no | no | no | YES | 4 | 11, 36 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 36 | no | no | no | YES | 4 | 11 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |
| 247 | no | no | no | YES | 7 | 149, 248 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 248 | no | no | no | YES | 7 | 149 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |
| 279 | no | no | no | YES | 7 | 163, 280 | $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である. |
| 280 | no | no | no | YES | 7 | 163 | 分解写像の第二成分は $\eta_{2}γ$ で与えられる. |

### [R5] Proposition 5.9

- entry steps: 33
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 10 | no | YES | YES | YES | 3 | 3, 13, 78 | $\pi_{7}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}$, $\pi_{8}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\eta_{7}\}$, $\pi_{9}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\eta_{8}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\eta_{8}\}$, $\pi_{10}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\eta_{9}\}$, $\pi_{11}^{6} = \mathbb{Z}\{\Delta\left(\iota_{13}\right)\}$, $\pi_{n + 5}^{n} = 0$, $n \ge 7$ が成り立つ. |
| 27 | no | YES | YES | YES | 4 | 10, 56, 113 | $\pi_{7}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}$ |
| 28 | no | YES | YES | YES | 4 | 10, 29, 61 | $\pi_{8}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\eta_{7}\}$ |
| 29 | no | YES | YES | YES | 4 | 10, 30, 62, 65, 184 | $\pi_{9}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\eta_{8}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\eta_{8}\}$ |
| 30 | no | YES | YES | YES | 4 | 10, 66, 130, 300 | $\pi_{10}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\eta_{9}\}$ |
| 31 | no | YES | YES | YES | 4 | 10, 137, 306 | $\pi_{11}^{6} = \mathbb{Z}\{\Delta\left(\iota_{13}\right)\}$ |
| 32 | no | YES | YES | YES | 4 | 10 | $\pi_{n + 5}^{n} = 0$ |
| 56 | no | YES | YES | YES | 5 | 28 | $H: \pi_{8}^{3} \to \pi_{8}^{5}$ は単射である. |
| 57 | no | YES | YES | YES | 5 | 28 | $\pi_{8}^{3} \xrightarrow{H} \pi_{8}^{5} \xrightarrow{\Delta} \pi_{6}^{2} \text{ is exact}$ |
| 58 | no | YES | YES | YES | 5 | 28 | $\ker\left(\Delta: \pi_{8}^{5} \to \pi_{6}^{2}\right) = \mathbb{Z}/2\{4\nu_{5}\}$ |
| 59 | no | YES | YES | YES | 5 | 28 | $H\left(\nu'\eta_{6}\eta_{7}\right) = 4\nu_{5}$ |
| 61 | no | YES | YES | YES | 5 | 29 | $E\nu'\eta_{6}\eta_{7} = E\nu'\eta_{7}^{2}$ |
| 62 | no | YES | YES | YES | 5 | 30, 184 | $\Delta\left(\eta_{9}\eta_{10}\right) = E\nu'\eta_{7}^{2}$ |
| 63 | no | YES | YES | YES | 5 | 30 | $\pi_{11}^{9} \xrightarrow{\Delta} \pi_{9}^{4} \xrightarrow{E} \pi_{10}^{5} \text{ is exact}$ |
| 64 | no | YES | YES | YES | 5 | 30 | $E: \pi_{9}^{4} \to \pi_{10}^{5}$ は全射である. |
| 65 | no | YES | YES | YES | 5 | 30 | $E\nu_{4}\eta_{7}\eta_{8} = \nu_{5}\eta_{8}^{2}$ |
| 66 | no | YES | YES | YES | 5 | 31 | $H: \pi_{11}^{6} \to \pi_{11}^{11}$ は単射である. |
| 67 | no | YES | YES | YES | 5 | 31 | $\pi_{11}^{6} \xrightarrow{H} \pi_{11}^{11} \xrightarrow{\Delta} \pi_{9}^{5} \text{ is exact}$ |
| 68 | no | YES | YES | YES | 5 | 31 | $\ker\Delta = \mathbb{Z}\{2\iota_{11}\}$ が成り立つ. |
| 69 | no | YES | YES | YES | 5 | 31 | $H(\Delta\left(\iota_{13}\right)) = \pm 2\iota_{11}$ が成り立つ. |
| 70 | no | YES | YES | YES | 5 | 32 | $\pi_{12}^{7} = 0$ |
| 113 | no | YES | YES | YES | 6 | 56 | $E\eta_{2}\nu'\eta_{6} = 0$ |
| 114 | no | YES | YES | YES | 6 | 56 | $\pi_{7}^{2} \xrightarrow{E} \pi_{8}^{3} \xrightarrow{H} \pi_{8}^{5} \text{ is exact}$ |
| 127 | no | YES | YES | YES | 6 | 64 | $H: \pi_{10}^{5} \to \pi_{10}^{9}$ は零写像である. |
| 128 | no | YES | YES | YES | 6 | 64 | $\pi_{9}^{4} \xrightarrow{E} \pi_{10}^{5} \xrightarrow{H} \pi_{10}^{9} \text{ is exact}$ |
| 130 | no | YES | YES | YES | 6 | 66 | $E\nu_{5}\eta_{8}\eta_{9} = 0$ |
| 131 | no | YES | YES | YES | 6 | 66 | $\pi_{10}^{5} \xrightarrow{E} \pi_{11}^{6} \xrightarrow{H} \pi_{11}^{11} \text{ is exact}$ |
| 137 | no | YES | YES | YES | 6 | 70 | $\Delta: \pi_{13}^{13} \to \pi_{11}^{6}$ は全射である. |
| 138 | no | YES | YES | YES | 6 | 70 | $\pi_{13}^{13} \xrightarrow{\Delta} \pi_{11}^{6} \xrightarrow{E} \pi_{12}^{7} \text{ is exact}$ |
| 139 | no | YES | YES | YES | 6 | 70 | $E: \pi_{11}^{6} \to \pi_{12}^{7}$ は全射である. |
| 221 | no | YES | YES | YES | 7 | 127 | $\Delta: \pi_{10}^{9} \to \pi_{8}^{4}$ は単射である. |
| 222 | no | YES | YES | YES | 7 | 127 | $\pi_{10}^{5} \xrightarrow{H} \pi_{10}^{9} \xrightarrow{\Delta} \pi_{8}^{4} \text{ is exact}$ |
| 234 | no | YES | YES | YES | 7 | 139 | $\pi_{11}^{6} \xrightarrow{E} \pi_{12}^{7} \xrightarrow{H} \pi_{12}^{13} \text{ is exact}$ |

### [R6] Proposition 5.8

- entry steps: 24
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 40 | no | YES | YES | YES | 4 | 13 | $\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ. |
| 55 | no | YES | YES | YES | 5 | 27, 220 | $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$ |
| 81 | no | no | no | YES | 5 | 40, 82, 155 | $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$ |
| 82 | no | YES | YES | YES | 5 | 40, 83, 156, 159 | $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$ |
| 83 | no | YES | YES | YES | 5 | 40, 160 | $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$ |
| 84 | no | YES | YES | YES | 5 | 40 | $\pi_{n + 4}^{n} = 0$ |
| 125 | no | YES | YES | YES | 6 | 62, 134, 221 | $\Delta\left(\eta_{9}\right) = E\nu'\eta_{7}$ |
| 129 | no | YES | YES | YES | 6 | 65 | $E\nu_{4}\eta_{7} = \nu_{5}\eta_{8}$ |
| 134 | no | no | no | YES | 6 | 68, 135 | $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$ |
| 155 | no | YES | YES | YES | 6 | 82 | $E\nu'\eta_{6} = E\nu'\eta_{7}$ |
| 156 | no | no | no | YES | 6 | 83 | $\Delta\left(\eta_{9}\right) = E\nu'\eta_{7}$ |
| 157 | no | YES | YES | YES | 6 | 83 | $\pi_{10}^{9} \xrightarrow{\Delta} \pi_{8}^{4} \xrightarrow{E} \pi_{9}^{5} \text{ is exact}$ |
| 158 | no | YES | YES | YES | 6 | 83 | $E: \pi_{8}^{4} \to \pi_{9}^{5}$ は全射である. |
| 159 | no | no | no | YES | 6 | 83 | $E\nu_{4}\eta_{7} = \nu_{5}\eta_{8}$ |
| 160 | no | YES | YES | YES | 6 | 84 | $\pi_{10}^{6} = 0$ |
| 201 | no | YES | YES | YES | 7 | 111 | $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は単射である. |
| 220 | no | no | no | YES | 7 | 125, 129, 134, 221, 230 | $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$ |
| 228 | no | no | no | YES | 7 | 134 | $\pi_{10}^{9} \xrightarrow{\Delta} \pi_{8}^{4} \xrightarrow{E} \pi_{9}^{5} \text{ is exact}$ |
| 229 | no | no | no | YES | 7 | 134 | $E: \pi_{8}^{4} \to \pi_{9}^{5}$ は全射である. |
| 230 | no | no | no | YES | 7 | 134 | $E\nu_{4}\eta_{7} = \nu_{5}\eta_{8}$ |
| 249 | no | no | no | YES | 7 | 150 | $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は単射である. |
| 267 | no | YES | YES | YES | 7 | 158 | $H: \pi_{9}^{5} \to \pi_{9}^{9}$ は零写像である. |
| 268 | no | YES | YES | YES | 7 | 158 | $\pi_{8}^{4} \xrightarrow{E} \pi_{9}^{5} \xrightarrow{H} \pi_{9}^{9} \text{ is exact}$ |
| 270 | no | YES | YES | YES | 7 | 160 | $E: \pi_{9}^{5} \to \pi_{10}^{6}$ は全射である. |

### [R7] Proposition 5.6

- entry steps: 25
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 42 | no | YES | YES | YES | 4 | 15, 45, 116, 117 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$, $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$, $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$, $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$, $n \ge 6$ が成り立つ. |
| 86 | no | YES | YES | YES | 5 | 42, 87, 281 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$ |
| 87 | no | YES | YES | YES | 5 | 42, 88, 89, 292 | $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$ |
| 88 | no | YES | YES | YES | 5 | 42, 181 | $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$ |
| 89 | no | YES | YES | YES | 5 | 42, 58, 59, 176 | $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$ |
| 90 | no | YES | YES | YES | 5 | 42 | $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$ |
| 148 | no | no | no | YES | 6 | 80 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$, $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$, $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$, $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$, $n \ge 6$ が成り立つ. |
| 164 | no | YES | YES | YES | 6 | 87 | $\operatorname{ord}\left(\nu'\right) = 4$ |
| 166 | no | YES | YES | YES | 6 | 87, 281 | $E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である. |
| 172 | no | YES | YES | YES | 6 | 89 | $\operatorname{ord}\left(\nu_{5}\right) = 8$ |
| 174 | no | YES | YES | YES | 6 | 89, 292 | $E^{2}: \pi_{6}^{3} \to \pi_{8}^{5}$ は単射である. |
| 175 | no | YES | YES | YES | 6 | 89 | $\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right) \cong \mathbb{Z}/2$ |
| 176 | no | YES | YES | YES | 6 | 90 | $\pi_{n + 3}^{n} = \mathbb{Z}/8\{E^{n - 5}\nu_{5}\}$ |
| 177 | no | YES | YES | YES | 6 | 90 | $E^{n - 5}\nu_{5} = \nu_{n}$ |
| 202 | no | YES | YES | YES | 7 | 111 | $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である. |
| 240 | no | no | no | YES | 7 | 148, 241 | $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$ |
| 241 | no | no | no | YES | 7 | 148, 242, 243 | $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$ |
| 242 | no | no | no | YES | 7 | 148 | $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$ |
| 243 | no | no | no | YES | 7 | 148 | $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$ |
| 244 | no | no | no | YES | 7 | 148 | $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$ |
| 250 | no | no | no | YES | 7 | 150 | $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である. |
| 281 | no | YES | YES | YES | 7 | 164 | $\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$ |
| 285 | no | YES | YES | YES | 7 | 166 | $\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である. |
| 291 | no | YES | YES | YES | 7 | 172 | $2\nu_{5} = E^{2}\nu'$ |
| 292 | no | YES | YES | YES | 7 | 172 | $\operatorname{ord}\left(E^{2}\nu'\right) = 4$ |

### [R8] Lemma 5.4

- entry steps: 10
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 44 | no | YES | YES | YES | 4 | 16, 118, 145, 178, 210 | $\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ. |
| 93 | no | YES | YES | YES | 5 | 44 | $\nu_{4} \in \pi_{7}^{4}$ |
| 94 | no | YES | YES | YES | 5 | 44 | $H\left(\nu_{4}\right) = \iota_{7}$ |
| 95 | no | YES | YES | YES | 5 | 44 | $2E\nu_{4} = E^{2}\nu'$ |
| 169 | no | YES | YES | YES | 6 | 87 | $\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$ |
| 180 | no | YES | YES | YES | 6 | 93, 94, 95 | $\begin{cases} \nu_{4} = α* - (-1)^{u}s[\iota_{4}, \iota_{4}] & \text{if } 2Eα* = E^{2}\nu' \\ \nu_{4} = -α* + (-1)^{u}\left(s + 1\right)[\iota_{4}, \iota_{4}] & \text{if } 2Eα* = -E^{2}\nu' \end{cases}$ |
| 260 | no | no | no | YES | 7 | 153 | $\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ. |
| 290 | no | no | no | YES | 7 | 170 | $\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ. |
| 296 | no | YES | YES | YES | 7 | 180, 295 | $2Eα* = \pm E^{2}\nu'$ |
| 297 | no | YES | YES | YES | 7 | 180, 182 | $H\left([\iota_{4}, \iota_{4}]\right) = 2\iota_{7},\quad E[\iota_{4}, \iota_{4}] = 0,\quad u\text{ is the sign parameter}$ |

### [R9] Equation 5.13

- entry steps: 3
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 46 | no | YES | YES | YES | 4 | 17, 188, 193 | $\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$ |
| 188 | no | YES | YES | YES | 6 | 100 | $\Delta\left(\eta_{11}\eta_{12}\right) = 0$ |
| 193 | no | YES | YES | YES | 6 | 102 | $\Delta\left(\eta_{13}\right) = 0$ |

### [R10] (4.5)

- entry steps: 4
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 52 | no | YES | YES | YES | 4 | 21 | $E^{n - 8}: \pi_{8 + 6}^{8} \to \pi_{n + 6}^{n}$ は同型写像である. |
| 71 | no | YES | YES | YES | 5 | 32 | $E^{n - 7}: \pi_{7 + 5}^{7} \to \pi_{n + 5}^{n}$ は同型写像である. |
| 161 | no | YES | YES | YES | 6 | 84 | $E^{n - 6}: \pi_{6 + 4}^{6} \to \pi_{n + 4}^{n}$ は同型写像である. |
| 293 | no | YES | YES | YES | 7 | 176 | $E^{n - 5}: \pi_{5 + 3}^{5} \to \pi_{n + 3}^{n}$ は同型写像である. |

### [R11] Proposition 5.3

- entry steps: 18
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 60 | no | YES | YES | YES | 5 | 29, 30, 55, 61, 184, 187, 202 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$, $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$, $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$, $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$, $n \ge 5$ が成り立つ. |
| 121 | no | YES | YES | YES | 6 | 60, 122 | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$ |
| 122 | no | YES | YES | YES | 6 | 60, 217 | $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$ |
| 123 | no | YES | YES | YES | 6 | 60 | $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$ |
| 152 | no | no | no | YES | 6 | 81, 250 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$, $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$, $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$, $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$, $n \ge 5$ が成り立つ. |
| 162 | no | no | no | YES | 6 | 86 | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$ |
| 168 | no | YES | YES | YES | 6 | 87 | $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である. |
| 213 | no | YES | YES | YES | 7 | 121 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である. |
| 214 | no | YES | YES | YES | 7 | 121 | $E\eta_{2}\eta_{3} = \eta_{3}^{2}$ |
| 215 | no | YES | YES | YES | 7 | 122 | $E: \pi_{5}^{3} \to \pi_{6}^{4}$ は同型写像である. |
| 216 | no | YES | YES | YES | 7 | 122 | $E\eta_{3}\eta_{4} = \eta_{4}^{2}$ |
| 217 | no | YES | YES | YES | 7 | 123 | $\pi_{n + 2}^{n} = \mathbb{Z}/2\{E^{n - 4}\eta_{4}\eta_{5}\}$ |
| 218 | no | YES | YES | YES | 7 | 123 | $E^{n - 4}\eta_{4}\eta_{5} = \eta_{n}\eta_{n + 1}$ |
| 255 | no | no | no | YES | 7 | 152, 256 | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$ |
| 256 | no | no | no | YES | 7 | 152 | $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}\eta_{5}\}$ |
| 257 | no | no | no | YES | 7 | 152 | $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$ |
| 276 | no | no | no | YES | 7 | 162 | $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である. |
| 277 | no | no | no | YES | 7 | 162 | $E\eta_{2}\eta_{3} = \eta_{3}^{2}$ |

### [R12] Lemma 4.5

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 76 | no | YES | YES | YES | 5 | 37, 78, 113, 201, 207 | $E\eta_{2}\nu' = 0$ |

### [R13] Lemma 5.7

- entry steps: 7
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 80 | no | YES | YES | YES | 5 | 40, 249 | $\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$ |
| 116 | no | YES | YES | YES | 6 | 58 | $\Delta\left(\nu_{5}\right) = \pm \eta_{2}\nu'$ |
| 117 | no | no | no | YES | 6 | 58, 116, 201, 207 | $\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$ |
| 145 | no | YES | YES | YES | 6 | 76, 146, 238 | $E^{2}\nu' \in 2\iota_{5}\circ \pi_{8}^{5}$ |
| 146 | no | YES | YES | YES | 6 | 76 | $E^{2}\eta_{2}\nu' = 0$ |
| 207 | no | YES | YES | YES | 7 | 116 | $\Delta: \pi_{8}^{5} \to \pi_{6}^{2}$ は全射である. |
| 238 | no | YES | YES | YES | 7 | 146 | $E^{2}\eta_{2}\nu' = \eta_{4}E^{2}\nu'$ |

### [R14] Proposition 4.4

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 92 | no | YES | YES | YES | 5 | 43 | $(α, \beta) \mapsto Eα + \nu_{4}\beta: \pi_{i - 1}^{3} \oplus \pi_{i}^{7} \to \pi_{i}^{4}$ は同型写像である. |

### [R15] Equation 5.8

- entry steps: 4
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 96 | no | YES | YES | YES | 5 | 46, 219 | $\Delta\left(\iota_{9}\right) = \pm \left(2\nu_{4} - E\nu'\right) = \pm [\iota_{4}, \iota_{4}]$ |
| 181 | no | YES | YES | YES | 6 | 96, 182, 183 | $\Delta\left(\iota_{9}\right) = \pm \left(2\nu_{4} - E\nu'\right)$ |
| 182 | no | YES | YES | YES | 6 | 96, 183 | $[\iota_{4}, \iota_{4}] = \pm \left(2\nu_{4} - E\nu'\right)$ |
| 183 | no | YES | YES | YES | 6 | 96 | $\Delta\left(\iota_{9}\right) = \pm [\iota_{4}, \iota_{4}]$ |

### [R16] Equation 5.7

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 112 | no | YES | YES | YES | 6 | 55, 59, 202 | $H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$ |
| 151 | no | no | no | YES | 6 | 81, 250 | $H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$ |

### [R17] (5.5)

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 118 | no | YES | YES | YES | 6 | 59, 188, 193 | $\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ. |
| 210 | no | YES | YES | YES | 7 | 118 | $2\nu_{n} = E^{n - 3}\nu'$ |

### [R18] (5.2)

- entry steps: 3
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 120 | no | YES | YES | YES | 6 | 60, 121 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$ |
| 254 | no | no | no | YES | 7 | 152, 255 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$ |
| 275 | no | no | no | YES | 7 | 162 | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$ |

### [R19] Proposition 5.1

- entry steps: 3
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 154 | no | YES | YES | YES | 6 | 82, 83, 155, 159 | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ. |
| 224 | no | no | no | YES | 7 | 129, 134, 192, 193, 220, 221, 230, 239, 300 | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ. |
| 288 | no | no | no | YES | 7 | 168, 169 | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ. |

### [R20] (5.3)

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 165 | no | YES | YES | YES | 6 | 87 | $\nu' \in \pi_{6}^{3}$ |
| 284 | no | YES | YES | YES | 7 | 165 | $2\eta_{3} = 0$ |

### [R21] Proposition 2.5

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 219 | no | YES | YES | YES | 7 | 125 | $\Delta\left(\eta_{9}\right) = \pm 2\nu_{4} - E\nu'\eta_{7}$ |
| 265 | no | no | no | YES | 7 | 156 | $\Delta\left(\eta_{9}\right) = \pm 2\nu_{4} - E\nu'\eta_{7}$ |

### [R22] Proposition 3.1

- entry steps: 2
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 226 | no | YES | YES | YES | 7 | 130 | $\nu_{6}\eta_{9} = 0$ |
| 271 | no | no | no | YES | 7 | 160 | $\nu_{6}\eta_{9} = 0$ |

### [R23] Proposition 5.1

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 239 | no | YES | YES | YES | 7 | 146 | $2\eta_{4} = 0$ |

### [R24] (5.3) / Lemma 5.2

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 283 | no | YES | YES | YES | 7 | 165 | $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ が成り立つ. |

### [R25] (4.8)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 295 | no | YES | YES | YES | 7 | 180 | $H\left(α*\right) = \left(2s + 1\right)\iota_{7}$ |

### [R26] Lemma 5.10

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 303 | no | YES | YES | YES | 7 | 193 | $\Delta\left(\iota_{13}\right) \in \{\nu_{6}, \eta_{9}, 2\iota_{10}\} \pmod{2\pi_{11}^{6}}$ |

### [R27] (5.4)

- entry steps: 1
- root in entry: no
- root selected: no

| node | root | candidate | selected | premise | distance→root | parents | statement |
| ---: | :---: | :---: | :---: | :---: | ---: | --- | --- |
| 304 | no | YES | YES | YES | 7 | 193 | $\{\eta_{n}, 2\iota_{n + 1}, \eta_{n + 1}\} = \{\pm E^{n - 3}\nu'\}$ |
