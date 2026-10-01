# Phase 154-R1 — Representative proof prose defect audit

この監査では production code を変更していない.
public Narrative route を depth=2 で取得し、代表群を同一条件で比較した.

## Representative groups

- $\pi_6^3$（primary）
- $\pi_{10}^4$（primary）
- $\pi_{11}^4$（primary）
- $\pi_{12}^5$（secondary）
- $\pi_{16}^9$（secondary）

## Cross-group defect counts

| category | affected groups | findings |
| --- | ---: | ---: |
| transition_repetition | 2 | 3 |
| semantic_duplication | 3 | 6 |
| internal_rule_name_leakage | 2 | 3 |
| english_statement_prose | 1 | 1 |
| reference_body_linkage | 5 | 6 |
| argument_contribution_ordering | 0 | 0 |
| punctuation | 5 | 11 |

## Group-by-group audit

### $\pi_6^3$

Connector counts: `{"さらに": 0, "したがって": 3, "まず": 1, "また": 1, "以上より": 2, "次に": 1}`

#### transition_repetition

- `connector_repetition`: {"connector": "以上より", "count": 2, "examples": ["以上より、", "以上より、"], "kind": "connector_repetition"}
- `connector_repetition`: {"connector": "したがって", "count": 3, "examples": ["したがって、", "したがって、", "したがって、"], "kind": "connector_repetition"}

#### semantic_duplication

- `exact_line_duplicate`: {"count": 2, "examples": ["以上より、", "以上より、"], "kind": "exact_line_duplicate", "normalized": "以上より,"}
- `exact_line_duplicate`: {"count": 2, "examples": ["以上で得た群構造、生成元、および写像に関する結果を合わせると、", "以上で得た群構造、生成元、および写像に関する結果を合わせると、"], "kind": "exact_line_duplicate", "normalized": "以上で得た群構造,生成元,および写像に関する結果を合わせると,"}
- `exact_line_duplicate`: {"count": 3, "examples": ["したがって、", "したがって、", "したがって、"], "kind": "exact_line_duplicate", "normalized": "したがって,"}
- `repeated_scalar_chain`: {"example": "また、$\\nu'$ は中央の群に属し、$\\operatorname{ord}(\\nu')=4=4$ であるから、$\\nu'$ は中央の群を生成する.", "kind": "repeated_scalar_chain", "repeated_term": "4"}

#### internal_rule_name_leakage

- machine-detected finding: 0

#### english_statement_prose

- machine-detected finding: 0

#### reference_body_linkage

- `reference_used_but_not_declared`: {"kind": "reference_used_but_not_declared", "reference_numbers": [1, 2, 3, 4, 5, 6]}

#### argument_contribution_ordering

- machine-detected finding: 0

#### punctuation

- `japanese_comma_usage`: {"count": 18, "examples": ["まず、$\\nu'$ を定める.", "この前提条件を満たすので、Lemma 5.2 を適用できる.", "Lemma 5.2 の $\\beta$ を $\\nu'$ と定めると、", "次に、$\\nu'$ の位数を決定するために、次の完全列を考える.", "以上より、", "以上で得た群構造、生成元、および写像に関する結果を合わせると、", "この完全性と $Δ=0$ より、$\\ker E=\\operatorname{Im}Δ=0$ である.", "したがって、"], "kind": "japanese_comma_usage"}
- `mixed_punctuation_style`: {"kind": "mixed_punctuation_style", "styles": [",", ".", "、"]}

#### ordering trace

```text
016 まず: まず、$\nu'$ を定める.
021 次に: 次に、$\nu'$ の位数を決定するために、次の完全列を考える.
026 以上より: 以上より、
030 したがって: したがって、
033 したがって: したがって、
042 以上より: 以上より、
044 また: また、$\nu'$ は中央の群に属し、$\operatorname{ord}(\nu')=4=4$ であるから、$\nu'$ は中央の群を生成する.
045 したがって: したがって、
```

#### numbered proof body

```text
001: 使用する結果を先にまとめる.
002: **[R1] (5.3).**
003: $\nu' \in \pi_{6}^{3}$
004: $2\nu' = \eta_{3}E\eta_{3}\eta_{5}$
005: **[R2] Proposition 5.3.**
006: $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.
007: $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$
008: **[R3] Lemma 5.4.**
009: $\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$
010: **[R4] (5.3) / Lemma 5.2.**
011: $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ が成り立つ.
012: **[R5] (5.2).**
013: $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である.
014: **[R6] Proposition 5.1.**
015: $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ.
016: まず、$\nu'$ を定める.
017: $2\eta_{3} = 0$
018: この前提条件を満たすので、Lemma 5.2 を適用できる.
019: Lemma 5.2 の $\beta$ を $\nu'$ と定めると、
020: $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$
021: 次に、$\nu'$ の位数を決定するために、次の完全列を考える.
022: $\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$
023: $2\nu' = \eta_{3}E\eta_{3}\eta_{5}\tag{1}$
024: $\eta_{3}E\eta_{3}\eta_{5} = \eta_{3}^{3}\tag{2}$
025: $\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$
026: 以上より、
027: 以上で得た群構造、生成元、および写像に関する結果を合わせると、
028: $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$
029: この完全性と $Δ=0$ より、$\ker E=\operatorname{Im}Δ=0$ である.
030: したがって、
031: $E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.
032: $\operatorname{ord}(\eta_{3}\eta_{4}\eta_{5})=2$ かつ $2\nu'=\eta_{3}\eta_{4}\eta_{5}$ より、$4\nu'=0$ かつ $2\nu'\neq0$ である.
033: したがって、
034: $\operatorname{ord}\left(\nu'\right) = 4$
035: (1) と (2) より、
036: $2\nu' = \eta_{3}^{3}\tag{3}$
037: 最後に、$\pi_{6}^{3}$ の群構造を決定するために、次の完全列を考える.
038: $\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}$
039: この完全性と、左の写像が単射、右の写像が全射であることより、次の短完全列を得る.
040: $0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$
041: 以上で得た群構造、生成元、および写像に関する結果を合わせると、
042: 以上より、
043: この短完全列と両端の群の位数より、中央の群の位数は $2\cdot2=4$ である.
044: また、$\nu'$ は中央の群に属し、$\operatorname{ord}(\nu')=4=4$ であるから、$\nu'$ は中央の群を生成する.
045: したがって、
046: $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$
```

### $\pi_{10}^4$

Connector counts: `{"さらに": 0, "したがって": 0, "まず": 0, "また": 0, "以上より": 1, "次に": 0}`

#### transition_repetition

- machine-detected finding: 0

#### semantic_duplication

- `exact_line_duplicate`: {"count": 2, "examples": ["以上で得た群構造、生成元、および写像に関する結果を合わせると、", "以上で得た群構造、生成元、および写像に関する結果を合わせると、"], "kind": "exact_line_duplicate", "normalized": "以上で得た群構造,生成元,および写像に関する結果を合わせると,"}

#### internal_rule_name_leakage

- `internal_rule_name_leakage`: {"example": "Toda (5.6) nu_4 decomposition integration", "kind": "internal_rule_name_leakage", "patterns": ["\\bToda\\b"]}

#### english_statement_prose

- `english_statement_prose`: {"ascii_words": ["nu_4", "decomposition", "integration"], "example": "Toda (5.6) nu_4 decomposition integration", "kind": "english_statement_prose", "outside_math": "Toda (5.6) nu_4 decomposition integration"}

#### reference_body_linkage

- `reference_used_but_not_declared`: {"kind": "reference_used_but_not_declared", "reference_numbers": [1, 2]}

#### argument_contribution_ordering

- machine-detected finding: 0

#### punctuation

- `japanese_comma_usage`: {"count": 3, "examples": ["以上で得た群構造、生成元、および写像に関する結果を合わせると、", "以上より、", "以上で得た群構造、生成元、および写像に関する結果を合わせると、"], "kind": "japanese_comma_usage"}
- `mixed_punctuation_style`: {"kind": "mixed_punctuation_style", "styles": [",", ".", "、"]}

#### ordering trace

```text
010 以上より: 以上より、
```

#### numbered proof body

```text
001: 使用する結果を先にまとめる.
002: **[R1] Proposition 5.6.**
003: $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$, $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$, $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$, $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$, $n \ge 6$ が成り立つ.
004: **[R2] Lemma 5.4.**
005: $\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ.
006: $\pi_{10}^{4}$ の群構造を決定する.
007: $\pi_{9}^{3} = 0$
008: 以上で得た群構造、生成元、および写像に関する結果を合わせると、
009: $\pi_{10}^{7} = \mathbb{Z}/8\{\nu_{7}\}$
010: 以上より、
011: 以上で得た群構造、生成元、および写像に関する結果を合わせると、
012: $\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$
013: Toda (5.6) nu_4 decomposition integration
```

### $\pi_{11}^4$

Connector counts: `{"さらに": 1, "したがって": 1, "まず": 2, "また": 2, "以上より": 0, "次に": 0}`

#### transition_repetition

- `connector_repetition`: {"connector": "まず", "count": 2, "examples": ["まず、Hopf 写像の単射性を用いる。", "まず、[R2]を用いる。"], "kind": "connector_repetition"}

#### semantic_duplication

- machine-detected finding: 0

#### internal_rule_name_leakage

- `internal_rule_name_leakage`: {"example": "Toda Proposition 5.15を用いる。", "kind": "internal_rule_name_leakage", "patterns": ["\\bToda\\b"]}
- `internal_rule_name_leakage`: {"example": "このことから、Toda (5.6) の ν₄ 分解同型を得る。", "kind": "internal_rule_name_leakage", "patterns": ["\\bToda\\b"]}

#### english_statement_prose

- machine-detected finding: 0

#### reference_body_linkage

- `bare_reference_use`: {"description": "Reference の数学的役割を本文側で説明せず、参照だけで文が完結している候補", "example": "また、[R1]を用いる。", "kind": "bare_reference_use"}
- `bare_reference_use`: {"description": "Reference の数学的役割を本文側で説明せず、参照だけで文が完結している候補", "example": "まず、[R2]を用いる。", "kind": "bare_reference_use"}

#### argument_contribution_ordering

- machine-detected finding: 0

#### punctuation

- `japanese_comma_usage`: {"count": 8, "examples": ["まず、Hopf 写像の単射性を用いる。", "また、$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2} \\text{ is injective}$を用いる。", "さらに、$\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} \\xrightarrow{\\Delta} \\pi_{8}^{2} \\text{ is exact}$を用いる。", "これらから、$\\pi_{10}^{3} = 0$を得る。", "また、[R1]を用いる。", "まず、[R2]を用いる。", "このことから、Toda (5.6) の ν₄ 分解同型を得る。", "したがって、$\\pi_{11}^{4} = 0$を得る。"], "kind": "japanese_comma_usage"}
- `japanese_period_usage`: {"count": 9, "examples": ["Toda Proposition 5.15を用いる。", "まず、Hopf 写像の単射性を用いる。", "また、$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2} \\text{ is injective}$を用いる。", "さらに、$\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} \\xrightarrow{\\Delta} \\pi_{8}^{2} \\text{ is exact}$を用いる。", "これらから、$\\pi_{10}^{3} = 0$を得る。", "また、[R1]を用いる。", "まず、[R2]を用いる。", "このことから、Toda (5.6) の ν₄ 分解同型を得る。"], "kind": "japanese_period_usage"}
- `mixed_punctuation_style`: {"kind": "mixed_punctuation_style", "styles": [",", ".", "、", "。"]}

#### ordering trace

```text
001 まず: まず、Hopf 写像の単射性を用いる。
002 また: また、$\Delta: \pi_{10}^{5} \to \pi_{8}^{2} \text{ is injective}$を用いる。
003 さらに: さらに、$\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} \xrightarrow{\Delta} \pi_{8}^{2} \text{ is exact}$を用いる。
005 また: また、[R1]を用いる。
006 まず: まず、[R2]を用いる。
008 したがって: したがって、$\pi_{11}^{4} = 0$を得る。
```

#### numbered proof body

```text
001: まず、Hopf 写像の単射性を用いる。
002: また、$\Delta: \pi_{10}^{5} \to \pi_{8}^{2} \text{ is injective}$を用いる。
003: さらに、$\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} \xrightarrow{\Delta} \pi_{8}^{2} \text{ is exact}$を用いる。
004: これらから、$\pi_{10}^{3} = 0$を得る。
005: また、[R1]を用いる。
006: まず、[R2]を用いる。
007: このことから、Toda (5.6) の ν₄ 分解同型を得る。
008: したがって、$\pi_{11}^{4} = 0$を得る。
```

### $\pi_{12}^5$

Connector counts: `{"さらに": 0, "したがって": 1, "まず": 1, "また": 0, "以上より": 1, "次に": 0}`

#### transition_repetition

- machine-detected finding: 0

#### semantic_duplication

- machine-detected finding: 0

#### internal_rule_name_leakage

- machine-detected finding: 0

#### english_statement_prose

- machine-detected finding: 0

#### reference_body_linkage

- `reference_used_but_not_declared`: {"kind": "reference_used_but_not_declared", "reference_numbers": [1, 2, 3, 4]}

#### argument_contribution_ordering

- machine-detected finding: 0

#### punctuation

- `japanese_comma_usage`: {"count": 6, "examples": ["まず、$\\sigma'''$ を定める.", "最後に、$\\pi_{12}^{5}$ の群構造を決定するために、次の完全列を考える.", "以上より、", "以上で得た群構造、生成元、および写像に関する結果を合わせると、", "この完全性、既知の群構造、および写像の像に関する結果を合わせると、対象となる写像の像と核が決まる.", "したがって、"], "kind": "japanese_comma_usage"}
- `mixed_punctuation_style`: {"kind": "mixed_punctuation_style", "styles": [",", ".", "、"]}

#### ordering trace

```text
011 まず: まず、$\sigma'''$ を定める.
015 以上より: 以上より、
018 したがって: したがって、
```

#### numbered proof body

```text
001: 使用する結果を先にまとめる.
002: **[R1] Lemma 5.13.**
003: $\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.
004: **[R2] Proposition 5.11.**
005: $\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}$
006: $\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}$, $\pi_{9}^{3} = 0$, $\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$, $\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}\nu_{8}\}$, $\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}\nu_{9}\}$, $\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}\nu_{10}\}$, $\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}\nu_{11}\}$, $\pi_{n + 6}^{n} = \mathbb{Z}/2\{\nu_{n}\nu_{n + 3}\}$, $n \ge 9$ が成り立つ.
007: **[R3] Equation 5.13.**
008: $\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$
009: **[R4] (5.5).**
010: $\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ.
011: まず、$\sigma'''$ を定める.
012: $H: \pi_{12}^{5} \to \pi_{12}^{9}$ は単射である.
013: 最後に、$\pi_{12}^{5}$ の群構造を決定するために、次の完全列を考える.
014: $\pi_{12}^{5} \xrightarrow{H} \pi_{12}^{9} \xrightarrow{\Delta} \pi_{10}^{4}$
015: 以上より、
016: 以上で得た群構造、生成元、および写像に関する結果を合わせると、
017: この完全性、既知の群構造、および写像の像に関する結果を合わせると、対象となる写像の像と核が決まる.
018: したがって、
019: $\pi_{12}^{5} = \mathbb{Z}/2\{\sigma'''\}$
```

### $\pi_{16}^9$

Connector counts: `{"さらに": 0, "したがって": 1, "まず": 1, "また": 0, "以上より": 1, "次に": 1}`

#### transition_repetition

- machine-detected finding: 0

#### semantic_duplication

- `exact_line_duplicate`: {"count": 2, "examples": ["以上で得た群構造、生成元、および写像に関する結果を合わせると、", "以上で得た群構造、生成元、および写像に関する結果を合わせると、"], "kind": "exact_line_duplicate", "normalized": "以上で得た群構造,生成元,および写像に関する結果を合わせると,"}

#### internal_rule_name_leakage

- machine-detected finding: 0

#### english_statement_prose

- machine-detected finding: 0

#### reference_body_linkage

- `reference_used_but_not_declared`: {"kind": "reference_used_but_not_declared", "reference_numbers": [1, 2, 3]}

#### argument_contribution_ordering

- machine-detected finding: 0

#### punctuation

- `japanese_comma_usage`: {"count": 8, "examples": ["まず、$\\sigma'''$ を定める.", "次に、$\\sigma_{9}$ を定める.", "最後に、$\\pi_{16}^{9}$ の群構造を決定する.", "この群構造と写像による移送の結果を合わせると、対象の群の位数と写像の単射性が決まる.", "したがって、", "以上で得た群構造、生成元、および写像に関する結果を合わせると、", "以上より、", "以上で得た群構造、生成元、および写像に関する結果を合わせると、"], "kind": "japanese_comma_usage"}
- `mixed_punctuation_style`: {"kind": "mixed_punctuation_style", "styles": [",", ".", "、"]}

#### ordering trace

```text
009 まず: まず、$\sigma'''$ を定める.
010 次に: 次に、$\sigma_{9}$ を定める.
015 したがって: したがって、
019 以上より: 以上より、
```

#### numbered proof body

```text
001: 使用する結果を先にまとめる.
002: **[R1] Lemma 5.14.**
003: $\sigma_{8} = xα* + -1\,y\Delta\left(\iota_{17}\right)$, $H\left(\sigma_{8}\right) = \iota_{15}$, $E\sigma_{8} = xEα*$, $2E\sigma_{8} = E^{2}\sigma'$ が成り立つ.
004: $2\sigma' = E\sigma''$, $H\left(\sigma'\right) = \eta_{13}$ が成り立つ.
005: **[R2] Theorem 3.6.**
006: $8\,xEα* = E^{4}\sigma'''$ が成り立つ.
007: **[R3] Lemma 5.13.**
008: $\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.
009: まず、$\sigma'''$ を定める.
010: 次に、$\sigma_{9}$ を定める.
011: $\sigma_{9}$ を \(\sigma\)-family の元として定める.
012: $\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}$
013: 最後に、$\pi_{16}^{9}$ の群構造を決定する.
014: この群構造と写像による移送の結果を合わせると、対象の群の位数と写像の単射性が決まる.
015: したがって、
016: $|\pi_{16}^{9}| = 16$ であり, $E^{4}: \pi_{12}^{5} \to \pi_{16}^{9}$ は単射である.
017: 以上で得た群構造、生成元、および写像に関する結果を合わせると、
018: $\pi_{12}^{5} = \mathbb{Z}/2\{\sigma'''\}$
019: 以上より、
020: 以上で得た群構造、生成元、および写像に関する結果を合わせると、
021: $\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$
```

## R1 interpretation rule

この report は機械検出結果であり、R2 の修正対象を自動決定しない.
R2 では複数群に共通し、かつより上流の一般規則で説明できる defect category を1つ選ぶ.
$\pi_6^3$ 専用修正は行わない.

Test Suite Consolidation は Phase 154 の対象外とする.
