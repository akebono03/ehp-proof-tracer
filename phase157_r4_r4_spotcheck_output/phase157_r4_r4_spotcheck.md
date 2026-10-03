# Phase157-R4-R4 representative output spot-check

- production code changes: none
- existing test changes: none
- depth: 3
- each representative rendered exactly once

## pi_8^5

- Reference markers: 2
- Reference chars: 79
- Body chars: 628
- Forbidden Reference hits: none

### Reference section

## 使用する結果

**[R1] Toda (5.5) の ν-family 有限次元結果.**

**[R2] Toda (5.6) の ν₄ 分解.**

### Body prefix

## 証明

まず, $\nu_{5}$ の位数を求める.

**(1)** $\nu_{5}$ を $\nu$-family の定義により取る.

[R1], (1) より,

\[
2\nu_{5} = E^{2}\nu'\tag{2}
\]

既に,

\[
\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}\tag{3}
\]

[R2] より,
**(4)** E²: π₆³ → π₈⁵ の単射性.

(3), (4) より,
**(5)** $E^{2}\nu'$ の位数は $4$ である.

(2), (5), (1) より,
**(6)** $\nu_{5}$ の位数は $8$ である.

[R2] より,
**(7)** π₈⁵ / E²π₆³ が位数 2 であること.

最後に, これらの結果から $\pi_{8}^{5}$ の群構造を決定する.

(3), (4), (7) より, $E^{2}\pi_{6}^{3}$ は位数 $4$ の部分群であり, その商が位数 $2$ なので, $\pi_{8}^{5}$ の位数は $8$ である.

(6) より $\nu_{5}$ も位数 $8$ であるから, $\nu_{5}$ は $\pi_{8}^{5}$ を生成する.

したがって,

\[
\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}\tag{8}
\]

を得る.

## pi_10^4

- Reference markers: 1
- Reference chars: 330
- Body chars: 103
- Forbidden Reference hits: none

### Reference section

使用する結果を先にまとめる.

**[R1] Proposition 5.6.**
$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$
$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$
$\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$
$\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$

$\pi_{10}^{4}$ の群構造を決定する.

$\pi_{9}^{3} = 0$

$\pi_{10}^{7} = \mathbb{Z}/8\{\nu_{7}\}$

### Body prefix

以上で得た群構造, 生成元, および写像に関する結果を合わせると, 

$\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$

$\nu_{4}$ の分解を用いる.

## pi_12^5

- Reference markers: 4
- Reference chars: 348
- Body chars: 594
- Forbidden Reference hits: none

### Reference section

## 使用する結果

使用する結果を先にまとめる.

**[R1] Proposition 5.15.**
$\pi_{11}^{4} = 0$
**[R2] Lemma 5.13.**
$\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.
**[R3] Proposition 5.11.**
$\pi_{9}^{3} = 0$
$\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$
**[R4] Equation 5.13.**
$\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$

### Body prefix

## 証明

まず, $\nu_{n}$ を定める.

$\nu_{n}$ を \(\nu\)-family の元として定める.

次に, $\sigma'''$ を定める.

$H: \pi_{12}^{5} \to \pi_{12}^{9}$ は単射である.

$\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}$

`ScalarGreaterEqualStatement`

$2\nu_{n} = E^{n - 3}\nu'$

$4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$

最後に, $\pi_{12}^{5}$ の群構造を決定するために, 次の完全列を考える.

$\pi_{11}^{4} \xrightarrow{E} \pi_{12}^{5} \xrightarrow{H} \pi_{12}^{9} \xrightarrow{\Delta} \pi_{10}^{4}$

以上より, 

[R3]を用いる.

以上で得た群構造, 生成元, および写像に関する結果を合わせると, 

この完全性, 既知の群構造, および写像の像に関する結果を合わせると, 対象となる写像の像と核が決まる.
したがって, 

$\pi_{12}^{5} = \mathbb{Z}/2\{\sigma'''\}$

## pi_15^8

- Reference markers: 1
- Reference chars: 181
- Body chars: 427
- Forbidden Reference hits: none

### Reference section

## 使用する結果

**[R1] Toda Proposition 4.4 の分解同型.**

次の写像は同型である.

\[
\pi_{14}^{7} \oplus \pi_{15}^{15} \longrightarrow \pi_{15}^{8}
\]

\[
(α, \beta) \longmapsto Eα + \sigma_{8}\beta
\]

### Body prefix

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

## pi_16^9

- Reference markers: 3
- Reference chars: 552
- Body chars: 684
- Forbidden Reference hits: none

### Reference section

使用する結果を先にまとめる.

**[R1] Lemma 5.14.**
$\sigma_{8} = xα* + -1\,y\Delta\left(\iota_{17}\right)$, $H\left(\sigma_{8}\right) = \iota_{15}$, $E\sigma_{8} = xEα*$, $2E\sigma_{8} = E^{2}\sigma'$ が成り立つ.
$2\sigma' = E\sigma''$, $H\left(\sigma'\right) = \eta_{13}$ が成り立つ.
$E^{3}\sigma'' = 4\,xEα*, \qquad 2\sigma'' = E\sigma''', \qquad H\left(\sigma''\right) = \eta_{11}\eta_{12}$
**[R2] Lemma 5.13.**
$\sigma''' \in \{\nu_{5}, 8\iota_{8}, \nu_{8}\}_{3}$, $H(\sigma''') = 4\nu_{9}$ が成り立つ.
**[R3] Equation 5.13.**
$\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$

### Body prefix

まず, $\sigma'''$ を定める.

次の短完全列を得る.

$0\longrightarrow \pi_{13}^{6}\xrightarrow{E} \pi_{14}^{7}\xrightarrow{H} \pi_{14}^{13}\longrightarrow 0$

$H: \pi_{12}^{5} \to \pi_{12}^{9}$ は単射である.

$\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}$

次に, $\sigma_{9}$ を定める.

$\sigma_{9}$ を \(\sigma\)-family の元として定める.

$\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}$

最後に, $\pi_{16}^{9}$ の群構造を決定する.

この群構造と写像による移送の結果を合わせると, 対象の群の位数と写像の単射性が決まる.
したがって, 

$|\pi_{16}^{9}| = 16$ であり, $E^{4}: \pi_{12}^{5} \to \pi_{16}^{9}$ は単射である.

この完全性, 既知の群構造, および写像の像に関する結果を合わせると, 対象となる写像の像と核が決まる.
したがって, 

$\pi_{12}^{5} = \mathbb{Z}/2\{\sigma'''\}$

以上で得た群構造, 生成元, および写像に関する結果を合わせると, 

$\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$
