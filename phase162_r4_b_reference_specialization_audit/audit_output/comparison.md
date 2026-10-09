# Phase 162 R4-B Reference / specialization audit

観測結果。数学的な特殊化の妥当性を自動証明したものではない。

## pi_5^4

Tree steps: 24; Presentation nodes: 8; edges: 7

### Reference candidates before filtering

- (4.5): includes root=False; equivalent root conclusion=False

### Explicit / inferred references in full root ancestry

- Step 2: (4.5) (inferred_or_boundary); Relation; boundary=TodaLiteratureStatementClassification.PROOF_INTERNAL
- Step 5: (4.5) (inferred_or_boundary); Toda45IsomorphismStatement; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 14: Proposition 5.1 (explicit); Relation; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 20: (5.1) (explicit); TodaPrimaryGroupZeroStatement; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 22: (5.1) (explicit); Relation; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 23: Proposition 5.1 (explicit); TodaDeltaImageUpToSignStatement; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT

### Toda (4.5) in tree

- Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=ScalarSum(left=ScalarSymbol(name='n'), right=ScalarProduct(left=-1, right=3)), source_group=TodaPrimaryGroup(group_dimension=ScalarSum(left=3, right=1), sphere_dimension=3), target_group=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n'))))

### Independently built canonical specialization (not tree evidence)

- Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=ScalarSum(left=4, right=ScalarProduct(left=-1, right=3)), source_group=TodaPrimaryGroup(group_dimension=ScalarSum(left=3, right=1), sphere_dimension=3), target_group=TodaPrimaryGroup(group_dimension=ScalarSum(left=4, right=1), sphere_dimension=4)))

### Baseline flags

- baseline_has_symbolic_n: True
- baseline_contains_toda45_reference: True
- baseline_has_target_in_reference_section: False

### Baseline Markdown

```text
# Group proof narrative

## 使用する結果

**[R1] (4.5).**
$E^{n - 3}: \pi_{3 + 1}^{3} \to \pi_{n + 1}^{n}$ は同型写像である.

---

## 証明

$\pi_{5}^{4}$ の群構造を決定する.

$E^{n - 3}\eta_{3} = \eta_{n}$.

$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

[R1]より, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$.

$\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$.

これより, 以上より, 

$\pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}$.

証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。

$\square$
```

## pi_6^5

Tree steps: 39; Presentation nodes: 11; edges: 13

### Reference candidates before filtering

- Lemma 5.4: includes root=True; equivalent root conclusion=True
- Proposition 5.1: includes root=False; equivalent root conclusion=False
- (5.1): includes root=False; equivalent root conclusion=False
- (4.5): includes root=False; equivalent root conclusion=False

### Explicit / inferred references in full root ancestry

- Step 0: Lemma 5.4 (inferred_or_boundary); Relation; boundary=TodaLiteratureStatementClassification.PROOF_INTERNAL
- Step 1: Proposition 5.1 (explicit); TodaProp51FiniteDimensionalStatement; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 4: Proposition 5.1 (explicit); TodaDeltaImageUpToSignStatement; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 7: (5.1) (explicit); Relation; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 9: (4.5) (inferred_or_boundary); Relation; boundary=TodaLiteratureStatementClassification.PROOF_INTERNAL
- Step 14: (4.5) (inferred_or_boundary); Toda45IsomorphismStatement; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 17: (5.1) (explicit); TodaPrimaryGroupZeroStatement; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 29: Proposition 5.1 (explicit); Relation; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 33: (5.1) (explicit); TodaSuspensionIsomorphismStatement; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 36: (5.1) (explicit); TodaPrimaryGroupZeroStatement; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT
- Step 38: (5.1) (explicit); Relation; boundary=TodaLiteratureStatementClassification.FIXED_STATEMENT

### Toda (4.5) in tree

- Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=ScalarSum(left=ScalarSymbol(name='n'), right=ScalarProduct(left=-1, right=3)), source_group=TodaPrimaryGroup(group_dimension=ScalarSum(left=3, right=1), sphere_dimension=3), target_group=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n'))))

### Independently built canonical specialization (not tree evidence)

- Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=ScalarSum(left=5, right=ScalarProduct(left=-1, right=3)), source_group=TodaPrimaryGroup(group_dimension=ScalarSum(left=3, right=1), sphere_dimension=3), target_group=TodaPrimaryGroup(group_dimension=ScalarSum(left=5, right=1), sphere_dimension=5)))

### Baseline flags

- baseline_has_symbolic_n: True
- baseline_contains_toda45_reference: False
- baseline_has_target_in_reference_section: True

### Baseline Markdown

```text
# Group proof narrative

## 使用する結果

**[R1] (5.1).**
$\pi_{i}^{1} = 0\ (i > 1)$.
$\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}\qquad (n \ge 1)$.
**[R2] Proposition 5.1.**
$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.

---

## 証明

$\pi_{6}^{5}$ の群構造を決定する.

[R1]より, $\pi_{2}^{1} = 0$.

[R1]より, $E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型写像である.

これより, これより, 

これより, これより, 

[R1]より, $\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}$.

これより, これより, 

$\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$.

これより, 以上より, 

[R2]より, $\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.

証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。

$\square$
```

