# Phase157-R4-R1 representative boundary audit

Production code changes: none.

## Reference locator summary

| Reference | Groups | FIXED | PROOF_INTERNAL | UNTRACKED |
| --- | --- | ---: | ---: | ---: |
| (5.2) | pi_8^5 | 0 | 0 | 1 |
| (5.3) | pi_8^5 | 2 | 1 | 0 |
| (5.5) | pi_12^5, pi_16^9, pi_8^5 | 0 | 0 | 5 |
| Equation 5.13 | pi_12^5, pi_16^9 | 3 | 0 | 0 |
| Equation 5.8 | pi_12^5 | 0 | 0 | 1 |
| Lemma 5.13 | pi_12^5, pi_16^9 | 4 | 0 | 0 |
| Lemma 5.14 | pi_15^8, pi_16^9 | 6 | 0 | 0 |
| Lemma 5.4 | pi_10^4, pi_12^5, pi_16^9, pi_8^5 | 0 | 0 | 10 |
| Proposition 4.4 | pi_10^4 | 0 | 0 | 1 |
| Proposition 5.1 | pi_8^5 | 1 | 1 | 0 |
| Proposition 5.11 | pi_10^4, pi_12^5, pi_15^8, pi_16^9 | 11 | 16 | 0 |
| Proposition 5.15 | pi_12^5, pi_15^8, pi_16^9 | 13 | 15 | 0 |
| Proposition 5.3 | pi_8^5 | 1 | 2 | 0 |
| Proposition 5.6 | pi_10^4, pi_12^5, pi_8^5 | 13 | 16 | 0 |
| Proposition 5.8 | pi_10^4, pi_16^9 | 0 | 0 | 2 |
| Proposition 5.9 | pi_10^4 | 0 | 0 | 1 |

## pi_8^5 depth=2

### Current public Reference prefix

```text
# Group proof narrative

## 証明対象

Toda Proposition 5.6 のうち,

\[
\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}
\]

を示す.

## 使用する結果

**[R1] Toda (5.5) の ν-family 有限次元結果.**

**[R2] Toda (5.6) の ν₄ 分解.**

## 証明
```

### Reference entries

#### 1. Proposition 5.6

Selected statement lines:
- `$\operatorname{ord}\left(\nu_{5}\right) = 8$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | Relation | pi8_5_group_relation | Toda Proposition 5.6 pi_8^5 finite cyclic |
| proof_internal | Relation |  | Toda Proposition 5.6 nu_5 order eight |
| fixed_statement | Relation | pi6_3_group_relation | Toda Proposition 5.6 pi_6^3 finite cyclic |
| proof_internal | TodaIteratedSuspensionInjectiveStatement |  | Toda Proposition 5.6 E^2 pi_6^3 injective |
| proof_internal | TodaProp56Pi8_5QuotientStatement |  | Toda Proposition 5.6 pi_8^5 quotient by E^2 pi_6^3 |
| proof_internal | Relation |  | Toda Proposition 5.6 nu_5 double relation |
| proof_internal | Relation |  | Toda Proposition 5.6 E^2 nu-prime order four |
| proof_internal | Relation |  | Toda Proposition 5.6 nu-prime order four |
| fixed_statement | Relation | pi5_2_group_relation | Toda Proposition 5.6 pi_5^2 eta_2 cube |
| proof_internal | TodaSuspensionInjectiveStatement |  | Toda Proposition 5.6 pi_5^2 suspension injective |
#### 2. (5.3)

Selected statement lines:
- `$\nu' \in \pi_{6}^{3}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | HomotopyGroupMembershipStatement | nu_prime_membership | Toda 5.3 nu-prime Lemma 5.2 membership specialization |
#### 3. Proposition 5.3

Selected statement lines:
- `$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| proof_internal | TodaHopfInvariantSurjectiveStatement |  | Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity |
#### 4. Lemma 5.4

Selected statement lines:
- `$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | Relation |  | Toda Lemma 5.4 pi_6^5 finite-cyclic specialization |

## pi_8^5 depth=3

### Current public Reference prefix

```text
# Group proof narrative

## 証明対象

Toda Proposition 5.6 のうち,

\[
\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}
\]

を示す.

## 使用する結果

**[R1] Toda (5.5) の ν-family 有限次元結果.**

**[R2] Toda (5.6) の ν₄ 分解.**

## 証明
```

### Reference entries

#### 1. Proposition 5.6

Selected statement lines:
- `$\operatorname{ord}\left(\nu_{5}\right) = 8$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | Relation | pi8_5_group_relation | Toda Proposition 5.6 pi_8^5 finite cyclic |
| proof_internal | Relation |  | Toda Proposition 5.6 nu_5 order eight |
| fixed_statement | Relation | pi6_3_group_relation | Toda Proposition 5.6 pi_6^3 finite cyclic |
| proof_internal | TodaIteratedSuspensionInjectiveStatement |  | Toda Proposition 5.6 E^2 pi_6^3 injective |
| proof_internal | TodaProp56Pi8_5QuotientStatement |  | Toda Proposition 5.6 pi_8^5 quotient by E^2 pi_6^3 |
| proof_internal | Relation |  | Toda Proposition 5.6 nu_5 double relation |
| proof_internal | Relation |  | Toda Proposition 5.6 E^2 nu-prime order four |
| proof_internal | Relation |  | Toda Proposition 5.6 nu-prime order four |
| fixed_statement | Relation | pi5_2_group_relation | Toda Proposition 5.6 pi_5^2 eta_2 cube |
| proof_internal | TodaSuspensionInjectiveStatement |  | Toda Proposition 5.6 pi_5^2 suspension injective |
| proof_internal | Relation |  | Toda Proposition 5.6 eta_3 cube order two |
| proof_internal | TodaDeltaZeroStatement |  | Toda Proposition 5.6 pi_7^5 Delta zero |
#### 2. (5.3)

Selected statement lines:
- `$\nu' \in \pi_{6}^{3}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | HomotopyGroupMembershipStatement | nu_prime_membership | Toda 5.3 nu-prime Lemma 5.2 membership specialization |
| proof_internal | Toda53NuPrimeBracketSpecializationStatement |  | Toda 5.3 nu-prime Lemma 5.2 bracket specialization |
#### 3. Proposition 5.3

Selected statement lines:
- `$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.`
- `$\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| proof_internal | TodaHopfInvariantSurjectiveStatement |  | Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity |
| fixed_statement | Relation | pi5_3_group_relation | Toda Proposition 5.3 n=3 pi_5^3 finite-cyclic transport |
#### 4. Lemma 5.4

Selected statement lines:
- `$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$`
- `$\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | Relation |  | Toda Lemma 5.4 pi_6^5 finite-cyclic specialization |
| UNTRACKED | TodaLemma54Statement |  | Toda Lemma 5.4 integration |
#### 5. (5.5)

Selected statement lines:
- `$\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | Toda55NuFamilyFiniteDimensionalStatement |  | Toda 5.5 nu-family finite-dimensional integration |
#### 6. Proposition 5.1

Selected statement lines:
- `$2\eta_{3} = 0$`
- `$\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| proof_internal | Relation |  | Toda 5.3 eta_3 twice zero |
| fixed_statement | TodaProp51FiniteDimensionalStatement |  | Toda Proposition 5.1 finite-dimensional integration |
#### 7. (5.2)

Selected statement lines:
- `$\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | Toda52CompositionIsomorphismStatement |  | Toda 5.2 eta_2 composition isomorphism |

## pi_10^4 depth=2

### Current public Reference prefix

```text
$\pi_{10}^{4}$ の群構造を決定する.
```

### Reference entries

#### 1. Proposition 5.11

Selected statement lines:
- `$\pi_{9}^{3} = 0$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | Relation | pi10_4_group_relation | Toda Proposition 5.11 pi_10^4 generated by nu_4 squared |
| fixed_statement | TodaPrimaryGroupZeroStatement | pi9_3_zero | Toda Proposition 5.11 pi_9^3 zero |
| proof_internal | Relation |  | Toda Proposition 5.11 pi_10^7 nu_7 specialization |
| proof_internal | TodaHopfInvariantInjectiveStatement |  | Toda Proposition 5.11 zero E implies H injective |
| proof_internal | TodaDeltaInjectiveStatement |  | Toda Proposition 5.11 pi_9^5 to pi_7^2 Delta injective |
| proof_internal | TodaProp42ExactnessStatement |  | Toda Proposition 5.11 pi_9^3 concrete EHP exactness |
#### 2. Proposition 5.6

Selected statement lines:
- `$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$, $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$, $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$, $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$, $n \ge 6$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaProp56FiniteDimensionalStatement |  | Toda Proposition 5.6 finite-dimensional integration |
#### 3. Lemma 5.4

Selected statement lines:
- `$\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | TodaLemma54Statement |  | Toda Lemma 5.4 integration |

## pi_10^4 depth=3

### Current public Reference prefix

```text
使用する結果を先にまとめる.

**[R1] Proposition 5.6.**
$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$
$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$
$\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$
$\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$
```

### Reference entries

#### 1. Proposition 5.11

Selected statement lines:
- `$\pi_{9}^{3} = 0$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | Relation | pi10_4_group_relation | Toda Proposition 5.11 pi_10^4 generated by nu_4 squared |
| fixed_statement | TodaPrimaryGroupZeroStatement | pi9_3_zero | Toda Proposition 5.11 pi_9^3 zero |
| proof_internal | Relation |  | Toda Proposition 5.11 pi_10^7 nu_7 specialization |
| proof_internal | TodaHopfInvariantInjectiveStatement |  | Toda Proposition 5.11 zero E implies H injective |
| proof_internal | TodaDeltaInjectiveStatement |  | Toda Proposition 5.11 pi_9^5 to pi_7^2 Delta injective |
| proof_internal | TodaProp42ExactnessStatement |  | Toda Proposition 5.11 pi_9^3 concrete EHP exactness |
| proof_internal | TodaSuspensionZeroStatement |  | Toda Proposition 5.11 E pi_8^2 zero |
| proof_internal | TodaProp42ExactnessStatement |  | Toda Proposition 5.11 pi_9^3 concrete EHP exactness |
| proof_internal | TodaDeltaSurjectiveStatement |  | Toda Proposition 5.11 zero E implies Delta surjective |
#### 2. Proposition 5.6

Selected statement lines:
- `$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$, $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$, $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$, $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$, $n \ge 6$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaProp56FiniteDimensionalStatement |  | Toda Proposition 5.6 finite-dimensional integration |
| fixed_statement | Relation | pi5_2_group_relation | Toda Proposition 5.6 pi_5^2 eta_2 cube |
| fixed_statement | Relation | pi6_3_group_relation | Toda Proposition 5.6 pi_6^3 finite cyclic |
| fixed_statement | Relation | pi7_4_group_relation | Toda Proposition 5.6 pi_7^4 decomposition |
| fixed_statement | Relation | pi8_5_group_relation | Toda Proposition 5.6 pi_8^5 finite cyclic |
#### 3. Lemma 5.4

Selected statement lines:
- `$\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | TodaLemma54Statement |  | Toda Lemma 5.4 integration |
| UNTRACKED | HomotopyGroupMembershipStatement |  | Toda Lemma 5.4 nu_4 membership |
| UNTRACKED | Relation |  | Toda Lemma 5.4 nu_4 Hopf correction |
| UNTRACKED | Relation |  | Toda Lemma 5.4 nu_4 double suspension |
#### 4. Proposition 5.8

Selected statement lines:
- `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | TodaProp58FiniteDimensionalStatement |  | Toda Proposition 5.8 finite-dimensional integration |
#### 5. Proposition 5.9

Selected statement lines:
- `$\pi_{7}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}$, $\pi_{8}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\eta_{7}\}$, $\pi_{9}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\eta_{8}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\eta_{8}\}$, $\pi_{10}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\eta_{9}\}$, $\pi_{11}^{6} = \mathbb{Z}\{\Delta\left(\iota_{13}\right)\}$, $\pi_{n + 5}^{n} = 0$, $n \ge 7$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | TodaProp59FiniteDimensionalStatement |  | Toda Proposition 5.9 finite-dimensional integration |
#### 6. Proposition 4.4

Selected statement lines:
- `$(α, \beta) \mapsto Eα + \nu_{4}\beta: \pi_{i - 1}^{3} \oplus \pi_{i}^{7} \to \pi_{i}^{4}$ は同型写像である.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | TodaProp44IsomorphismStatement |  | Toda Proposition 4.4 nu_4 n=4 decomposition specialization |

## pi_12^5 depth=2

### Current public Reference prefix

```text
使用する結果を先にまとめる.

**[R1] Lemma 5.13.**
$\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.
**[R2] Equation 5.13.**
$\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$
```

### Reference entries

#### 1. Proposition 5.15

Selected statement lines:
- `$H: \pi_{12}^{5} \xrightarrow{\cong} \mathbb{Z}/2\{4\nu_{9}\}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | Relation | pi12_5_group_relation | Toda Proposition 5.15 pi_12^5 finite cyclic |
| proof_internal | TodaProp515Pi12_5HopfIsomorphismStatement |  | Toda Proposition 5.15 pi_12^5 Hopf isomorphism |
| proof_internal | TodaProp42ExactnessStatement |  | Toda Proposition 5.15 pi_12^5 concrete EHP exactness |
#### 2. Lemma 5.13

Selected statement lines:
- `$\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaLemma513Statement | sigma_triple_prime_statement | Toda Lemma 5.13 sigma triple-prime definition |
#### 3. Proposition 5.11

Selected statement lines:
- `$\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}$`
- `$\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}$, $\pi_{9}^{3} = 0$, $\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$, $\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}\nu_{8}\}$, $\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}\nu_{9}\}$, $\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}\nu_{10}\}$, $\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}\nu_{11}\}$, $\pi_{n + 6}^{n} = \mathbb{Z}/2\{\nu_{n}\nu_{n + 3}\}$, $n \ge 9$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| proof_internal | Relation |  | Toda Proposition 5.11 pi_12^9 nu_9 specialization |
| fixed_statement | TodaProp511FiniteDimensionalStatement |  | Toda Proposition 5.11 finite-dimensional integration |
#### 4. Equation 5.13

Selected statement lines:
- `$\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaDeltaImageUpToSignStatement | delta_nu9_relation | Toda Equation 5.13 Delta nu_9 |
#### 5. (5.5)

Selected statement lines:
- `$\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | Toda55NuFamilyFiniteDimensionalStatement |  | Toda 5.5 nu-family finite-dimensional integration |

## pi_12^5 depth=3

### Current public Reference prefix

```text
使用する結果を先にまとめる.

**[R1] Proposition 5.11.**
$\pi_{9}^{3} = 0$
$\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$
```

### Reference entries

#### 1. Proposition 5.15

Selected statement lines:
- `$H: \pi_{12}^{5} \xrightarrow{\cong} \mathbb{Z}/2\{4\nu_{9}\}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.`
- `$\pi_{11}^{4} = 0$`
- `$\pi_{11}^{4} \xrightarrow{E} \pi_{12}^{5} \xrightarrow{H} \pi_{12}^{9}$ は完全である.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | Relation | pi12_5_group_relation | Toda Proposition 5.15 pi_12^5 finite cyclic |
| proof_internal | TodaProp515Pi12_5HopfIsomorphismStatement |  | Toda Proposition 5.15 pi_12^5 Hopf isomorphism |
| proof_internal | TodaProp42ExactnessStatement |  | Toda Proposition 5.15 pi_12^5 concrete EHP exactness |
| fixed_statement | TodaPrimaryGroupZeroStatement | pi11_4_zero | Toda Proposition 5.15 pi_11^4 zero |
| proof_internal | TodaProp42ExactnessStatement |  | Toda Proposition 5.15 pi_12^5 concrete EHP exactness |
#### 2. Lemma 5.13

Selected statement lines:
- `$\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaLemma513Statement | sigma_triple_prime_statement | Toda Lemma 5.13 sigma triple-prime definition |
#### 3. Proposition 5.11

Selected statement lines:
- `$\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}$`
- `$\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}$, $\pi_{9}^{3} = 0$, $\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$, $\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}\nu_{8}\}$, $\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}\nu_{9}\}$, $\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}\nu_{10}\}$, $\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}\nu_{11}\}$, $\pi_{n + 6}^{n} = \mathbb{Z}/2\{\nu_{n}\nu_{n + 3}\}$, $n \ge 9$ が成り立つ.`
- `$\pi_{9}^{3} = 0$`
- `$\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| proof_internal | Relation |  | Toda Proposition 5.11 pi_12^9 nu_9 specialization |
| fixed_statement | TodaProp511FiniteDimensionalStatement |  | Toda Proposition 5.11 finite-dimensional integration |
| fixed_statement | Relation | pi8_2_group_relation | Toda Proposition 5.11 pi_8^2 from Proposition 5.9 and Toda (5.2) |
| fixed_statement | TodaPrimaryGroupZeroStatement | pi9_3_zero | Toda Proposition 5.11 pi_9^3 zero |
| fixed_statement | Relation | pi10_4_group_relation | Toda Proposition 5.11 pi_10^4 generated by nu_4 squared |
| fixed_statement | TodaProp511NuSquaredFiniteDimensionalStatement | higher_nu_squared_group_relation | Toda Proposition 5.11 nu-squared finite-dimensional integration |
#### 4. Equation 5.13

Selected statement lines:
- `$\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaDeltaImageUpToSignStatement | delta_nu9_relation | Toda Equation 5.13 Delta nu_9 |
#### 5. (5.5)

Selected statement lines:
- `$\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | Toda55NuFamilyFiniteDimensionalStatement |  | Toda 5.5 nu-family finite-dimensional integration |
| UNTRACKED | Relation |  | Toda 5.5 nu-family double suspension transport |
#### 6. Proposition 5.6

Selected statement lines:
- `$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$, $\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$, $\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$, $\pi_{n + 3}^{n} = \mathbb{Z}/8\{\nu_{n}\}$, $n \ge 6$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaProp56FiniteDimensionalStatement |  | Toda Proposition 5.6 finite-dimensional integration |
#### 7. Equation 5.8

Selected statement lines:
- `$\Delta\left(\iota_{9}\right) = \pm \left(2\nu_{4} - E\nu'\right) = \pm [\iota_{4}, \iota_{4}]$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | Toda58EquationStatement |  | Toda Equation 5.8 integration |
#### 8. Lemma 5.4

Selected statement lines:
- `$\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | TodaLemma54Statement |  | Toda Lemma 5.4 integration |

## pi_15^8 depth=2

### Current public Reference prefix

```text
# Group proof narrative

## 証明対象

Toda Proposition 5.15 のうち,

\[
\pi_{15}^{8} = \mathbb{Z}\{\sigma_{8}\} \oplus \mathbb{Z}/8\{E\sigma'\}
\]

を示す.

## 使用する結果

**[R1] Toda Proposition 4.4 の分解同型.**

次の写像は同型である.

\[
\pi_{14}^{7} \oplus \pi_{15}^{15} \longrightarrow \pi_{15}^{8}
\]

\[
(α, \beta) \longmapsto Eα + \sigma_{8}\beta
\]

## 証明

既に,

\[
\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}
\]

である.

また,

\[
\pi_{15}^{15} = \mathbb{Z}\{\iota_{15}\}
\]

である.

[R1] より, これらの生成元はそれぞれ

\[
\sigma' \longmapsto E\sigma',
\qquad
\iota_{15} \longmapsto \sigma_{8}
\]

と写る.

したがって,

\[
\pi_{15}^{8} \cong \mathbb{Z}/8\{E\sigma'\} \oplus \mathbb{Z}\{\sigma_{8}\}
\]

を得る.

直和因子の順序を入れ替えると,

\[
\pi_{15}^{8} = \mathbb{Z}\{\sigma_{8}\} \oplus \mathbb{Z}/8\{E\sigma'\}
\]

を得る.
```

### Reference entries

#### 1. Proposition 5.15

Selected statement lines:
- `$\pi_{15}^{8} \cong \mathbb{Z}/8\{E\sigma'\} \oplus \mathbb{Z}\{\sigma_{8}\}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | Relation | pi15_8_group_relation | Toda Proposition 5.15 pi_15^8 final decomposition |
| proof_internal | Toda515Sigma8TransportedDecompositionStatement |  | Toda Proposition 5.15 sigma_8 transported decomposition |
| proof_internal | TodaProp44IsomorphismStatement |  | Toda Proposition 5.15 sigma_8 n=8 Proposition 4.4 decomposition specialization |
| fixed_statement | Relation | pi14_7_group_relation | Toda Proposition 5.15 pi_14^7 finite cyclic |

## pi_15^8 depth=3

### Current public Reference prefix

```text
# Group proof narrative

## 証明対象

Toda Proposition 5.15 のうち,

\[
\pi_{15}^{8} = \mathbb{Z}\{\sigma_{8}\} \oplus \mathbb{Z}/8\{E\sigma'\}
\]

を示す.

## 使用する結果

**[R1] Toda Proposition 4.4 の分解同型.**

次の写像は同型である.

\[
\pi_{14}^{7} \oplus \pi_{15}^{15} \longrightarrow \pi_{15}^{8}
\]

\[
(α, \beta) \longmapsto Eα + \sigma_{8}\beta
\]

## 証明

既に,

\[
\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}
\]

である.

また,

\[
\pi_{15}^{15} = \mathbb{Z}\{\iota_{15}\}
\]

である.

[R1] より, これらの生成元はそれぞれ

\[
\sigma' \longmapsto E\sigma',
\qquad
\iota_{15} \longmapsto \sigma_{8}
\]

と写る.

したがって,

\[
\pi_{15}^{8} \cong \mathbb{Z}/8\{E\sigma'\} \oplus \mathbb{Z}\{\sigma_{8}\}
\]

を得る.

直和因子の順序を入れ替えると,

\[
\pi_{15}^{8} = \mathbb{Z}\{\sigma_{8}\} \oplus \mathbb{Z}/8\{E\sigma'\}
\]

を得る.
```

### Reference entries

#### 1. Proposition 5.15

Selected statement lines:
- `$\pi_{13}^{6} = \mathbb{Z}/4\{\sigma''\}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | Relation | pi15_8_group_relation | Toda Proposition 5.15 pi_15^8 final decomposition |
| proof_internal | Toda515Sigma8TransportedDecompositionStatement |  | Toda Proposition 5.15 sigma_8 transported decomposition |
| proof_internal | TodaProp44IsomorphismStatement |  | Toda Proposition 5.15 sigma_8 n=8 Proposition 4.4 decomposition specialization |
| fixed_statement | Relation | pi14_7_group_relation | Toda Proposition 5.15 pi_14^7 finite cyclic |
| proof_internal | Toda515Sigma8Prop44SpecializationStatement |  | Toda Proposition 5.15 sigma_8 Proposition 4.4 specialization premises |
| fixed_statement | Relation | pi13_6_group_relation | Toda Proposition 5.15 pi_13^6 finite cyclic |
#### 2. Lemma 5.14

Selected statement lines:
- `$2\sigma' = E\sigma''$, $H\left(\sigma'\right) = \eta_{13}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaLemma514SigmaPrimeStatement | sigma_prime_statement | Toda Lemma 5.14 sigma-prime branch |
#### 3. Proposition 5.11

Selected statement lines:
- `$\pi_{14}^{13} = \mathbb{Z}/2\{\eta_{13}\}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| proof_internal | Relation |  | Toda Proposition 5.11 pi_14^13 eta_13 |

## pi_16^9 depth=2

### Current public Reference prefix

```text
使用する結果を先にまとめる.

**[R1] Lemma 5.14.**
$\sigma_{8} = xα* + -1\,y\Delta\left(\iota_{17}\right)$, $H\left(\sigma_{8}\right) = \iota_{15}$, $E\sigma_{8} = xEα*$, $2E\sigma_{8} = E^{2}\sigma'$ が成り立つ.
$2\sigma' = E\sigma''$, $H\left(\sigma'\right) = \eta_{13}$ が成り立つ.
**[R2] Lemma 5.13.**
$\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.
```

### Reference entries

#### 1. Proposition 5.15

Selected statement lines:
- `$\pi_{12}^{5} = \mathbb{Z}/2\{\sigma'''\}$`
- `$\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}$`
- `$H: \pi_{12}^{5} \xrightarrow{\cong} \mathbb{Z}/2\{4\nu_{9}\}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| proof_internal | Relation |  | Toda Proposition 5.15 pi_16^9 generated by sigma_9 |
| fixed_statement | Relation | pi12_5_group_relation | Toda Proposition 5.15 pi_12^5 finite cyclic |
| fixed_statement | Relation | pi14_7_group_relation | Toda Proposition 5.15 pi_14^7 finite cyclic |
| proof_internal | TodaProp515Pi12_5HopfIsomorphismStatement |  | Toda Proposition 5.15 pi_12^5 Hopf isomorphism |
#### 2. Lemma 5.14

Selected statement lines:
- `$\sigma_{8} = xα* + -1\,y\Delta\left(\iota_{17}\right)$, $H\left(\sigma_{8}\right) = \iota_{15}$, $E\sigma_{8} = xEα*$, $2E\sigma_{8} = E^{2}\sigma'$ が成り立つ.`
- `$2\sigma' = E\sigma''$, $H\left(\sigma'\right) = \eta_{13}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaLemma514Sigma8Statement | sigma8_statement | Toda Lemma 5.14 sigma_8 branch |
| fixed_statement | TodaLemma514SigmaPrimeStatement | sigma_prime_statement | Toda Lemma 5.14 sigma-prime branch |
#### 3. Lemma 5.13

Selected statement lines:
- `$\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaLemma513Statement | sigma_triple_prime_statement | Toda Lemma 5.13 sigma triple-prime definition |

## pi_16^9 depth=3

### Current public Reference prefix

```text
使用する結果を先にまとめる.

**[R1] Lemma 5.14.**
$\sigma_{8} = xα* + -1\,y\Delta\left(\iota_{17}\right)$, $H\left(\sigma_{8}\right) = \iota_{15}$, $E\sigma_{8} = xEα*$, $2E\sigma_{8} = E^{2}\sigma'$ が成り立つ.
$2\sigma' = E\sigma''$, $H\left(\sigma'\right) = \eta_{13}$ が成り立つ.
$E^{3}\sigma'' = 4\,xEα*, \qquad 2\sigma'' = E\sigma''', \qquad H\left(\sigma''\right) = \eta_{11}\eta_{12}$
**[R2] Lemma 5.13.**
$\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.
**[R3] Equation 5.13.**
$\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$
```

### Reference entries

#### 1. Proposition 5.15

Selected statement lines:
- `$\pi_{12}^{5} = \mathbb{Z}/2\{\sigma'''\}$`
- `$\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}$`
- `$H: \pi_{12}^{5} \xrightarrow{\cong} \mathbb{Z}/2\{4\nu_{9}\}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.`
- `$\pi_{13}^{6} = \mathbb{Z}/4\{\sigma''\}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| proof_internal | Relation |  | Toda Proposition 5.15 pi_16^9 generated by sigma_9 |
| fixed_statement | Relation | pi12_5_group_relation | Toda Proposition 5.15 pi_12^5 finite cyclic |
| fixed_statement | Relation | pi14_7_group_relation | Toda Proposition 5.15 pi_14^7 finite cyclic |
| proof_internal | TodaProp515Pi12_5HopfIsomorphismStatement |  | Toda Proposition 5.15 pi_12^5 Hopf isomorphism |
| fixed_statement | Relation | pi13_6_group_relation | Toda Proposition 5.15 pi_13^6 finite cyclic |
| proof_internal | TodaProp42ExactnessStatement |  | Toda Proposition 5.15 pi_12^5 concrete EHP exactness |
#### 2. Lemma 5.14

Selected statement lines:
- `$\sigma_{8} = xα* + -1\,y\Delta\left(\iota_{17}\right)$, $H\left(\sigma_{8}\right) = \iota_{15}$, $E\sigma_{8} = xEα*$, $2E\sigma_{8} = E^{2}\sigma'$ が成り立つ.`
- `$2\sigma' = E\sigma''$, $H\left(\sigma'\right) = \eta_{13}$ が成り立つ.`
- `$E^{3}\sigma'' = 4\,xEα*, \qquad 2\sigma'' = E\sigma''', \qquad H\left(\sigma''\right) = \eta_{11}\eta_{12}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaLemma514Sigma8Statement | sigma8_statement | Toda Lemma 5.14 sigma_8 branch |
| fixed_statement | TodaLemma514SigmaPrimeStatement | sigma_prime_statement | Toda Lemma 5.14 sigma-prime branch |
| fixed_statement | TodaLemma514SigmaDoublePrimeStatement | sigma_double_prime_statement | Toda Lemma 5.14 sigma double-prime branch |
#### 3. Lemma 5.13

Selected statement lines:
- `$\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaLemma513Statement | sigma_triple_prime_statement | Toda Lemma 5.13 sigma triple-prime definition |
#### 4. Lemma 5.4

Selected statement lines:
- `$\nu_{4} \in \pi_{7}^{4}$, $H\left(\nu_{4}\right) = \iota_{7}$, $2E\nu_{4} = E^{2}\nu'$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | TodaLemma54Statement |  | Toda Lemma 5.4 integration |
#### 5. Proposition 5.11

Selected statement lines:
- `$\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}$, $\pi_{9}^{3} = 0$, $\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$, $\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}\nu_{8}\}$, $\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}\nu_{9}\}$, $\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}\nu_{10}\}$, $\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}\nu_{11}\}$, $\pi_{n + 6}^{n} = \mathbb{Z}/2\{\nu_{n}\nu_{n + 3}\}$, $n \ge 9$ が成り立つ.`
- `$\pi_{14}^{13} = \mathbb{Z}/2\{\eta_{13}\}$`
- `$\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaProp511FiniteDimensionalStatement |  | Toda Proposition 5.11 finite-dimensional integration |
| proof_internal | Relation |  | Toda Proposition 5.11 pi_14^13 eta_13 |
| proof_internal | Relation |  | Toda Proposition 5.11 pi_12^9 nu_9 specialization |
#### 6. Proposition 5.8

Selected statement lines:
- `$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, $\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}$, $\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}$, $\pi_{n + 4}^{n} = 0$, $n \ge 6$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | TodaProp58FiniteDimensionalStatement |  | Toda Proposition 5.8 finite-dimensional integration |
#### 7. Equation 5.13

Selected statement lines:
- `$\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| fixed_statement | TodaDeltaImageUpToSignStatement | delta_nu9_relation | Toda Equation 5.13 Delta nu_9 |
#### 8. (5.5)

Selected statement lines:
- `$\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ.`

| classification | statement type | component | rule |
| --- | --- | --- | --- |
| UNTRACKED | Toda55NuFamilyFiniteDimensionalStatement |  | Toda 5.5 nu-family finite-dimensional integration |

## R4-R2 gate

R4-R2 では、この監査で UNTRACKED となった文献について、
fixed statement の境界を確認できたものだけ catalog に追加する。
rule name や literature_reference が同じという理由だけで
Reference へ採用しない。
