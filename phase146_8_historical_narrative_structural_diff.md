# Phase 146-8 Historical Narrative Full Structural Diff Audit

## Summary

- historical units: 17
- current units: 82
- PRESERVED: 0
- LOST: 17
- ADDED: 47
- MOVED: 0
- DUPLICATED: 35
- REWORDED: 0
- UNMATCHED: 0

Classification is structural/heuristic. REWORDED and MOVED candidates must be reviewed before production changes.

## Exactness / sequence inventory

- historical sequence-related units: 4
- current sequence-related units: 44

## Reference-reason inventory

- historical [R#] units: 8
- current [R#] units: 1

## Numbered-formula inventory

- historical tagged units: 5
- current tagged units: 11

## LOST

### Historical unit H1 (PROSE)

```text
# Group proof narrative
## 証明対象
Toda Proposition 5.6 のうち,
\[
\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}
\]
を示す.
```

### Historical unit H2 (PROSE)

```text
## 使用する結果
**[R1] Toda (5.2) の η₂ 合成同型.**
次の合成写像は同型である.
```

### Historical unit H3 (PROSE)

```text
\[
\eta_{2}\circ - : \pi_{i}^{3} \longrightarrow \pi_{i}^{2}.
```

### Historical unit H4 (PROSE)

```text
\]
**[R2] Toda Proposition 5.1.**
\[
\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}\qquad (n \ge 3).
```

### Historical unit H5 (PROSE)

```text
\]
**[R3] Toda Proposition 5.3.**
\[
\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}^{2}\}\qquad (n \ge 2).
```

### Historical unit H6 (PROSE)

```text
\]
\[
\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\},\qquad\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}.
```

### Historical unit H7 (PROSE)

```text
\]
**[R4] Toda Lemma 5.2.**
まず Lemma 5.2 の一般形を記す.
```

### Historical unit H8 (PROSE)

```text
$\alpha\in\pi_i^3$, $2\alpha=0$ であり,
\[
\beta \in \{\eta_{3},2\iota_{4},E\alpha\}_{1}
\]
ならば,
\[
\beta\in\pi_{i+2}^{3},
\qquad
H(\beta)=E^{2}\alpha,
\qquad
2\beta=\eta_{3}\circ E\alpha\circ\eta_{i+1},
\qquad
\Delta(E^{2}\alpha)=0.
```

### Historical unit H9 (PROSE)

```text
\]
この証明では $\alpha=\eta_{3}$, $i=4$ とする. まず $2\eta_{3}=0$ を確認すると, Toda bracket
\[
\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}
\]
が定義できる. この bracket のある元を $\nu'$ と定める. すなわち,
\[
\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}.
```

### Historical unit H10 (PROSE)

```text
\]
すると Lemma 5.2 より,
\[
\nu'\in\pi_{6}^{3},
\qquad
H(\nu')=E^{2}\eta_{3},
\qquad
2\nu'=\eta_{3}\circ E\eta_{3}\circ\eta_{5},
\qquad
\Delta(E^{2}\eta_{3})=0
\]
を得る.
```

### Historical unit H11 (PROSE)

```text
**[R5] Toda Proposition 2.2 の右合成公式.**
\[
H(\alpha\circ E\beta)=H(\alpha)\circ E\beta.
```

### Historical unit H12 (PROSE)

```text
\]
## 証明
まず, Lemma 5.2 を $\alpha=\eta_{3}$, $i=4$, $\beta=\nu'$ として適用するための仮定を確認する.
```

### Historical unit H13 (PROSE)

```text
[R2] の $n=3$ の場合より,
\[
2\eta_{3}=0.\tag{1}
\]
したがって Toda bracket $\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}$ が定義できる. [R4] でこの bracket のある元を $\nu'$ と定めたので,
\[
\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}.\tag{2}
\]
(1), (2) により Lemma 5.2 の仮定が満たされる. したがって Lemma 5.2 の結論から,
\[
\nu'\in\pi_{6}^{3}.\tag{3}
\]
さらに $H(\beta)=E^{2}\alpha$ と $E^{2}\eta_{3}=\eta_{5}$ から,
\[
H(\nu')=\eta_{5}.\tag{4}
\]
また $2\beta=\eta_{3}\circ E\alpha\circ\eta_{i+1}$ と $E\eta_{3}=\eta_{4}$ から,
\[
2\nu'=\eta_{3}\circ E\eta_{3}\circ\eta_{5}=\eta_{3}^{3}.\tag{5}
\]
[R3] の $n=3$ の場合より,
\[
\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}.\tag{6}
\]
(6), [R1] より,
\[
\pi_{5}^{2}=\mathbb{Z}/2\{\eta_{2}^{3}\}.\tag{7}
\]
$\nu'$ の位数を決定するために, 次の EHP 完全列を考える.
```

### Historical unit H14 (PROSE)

```text
\[
\pi_{7}^{3}\xrightarrow{H}\pi_{7}^{5}\xrightarrow{\Delta}\pi_{5}^{2}\xrightarrow{E}\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}\quad\text{は完全である.}\tag{8}
\]
[R2] の $n=6$ の場合より $\eta_{6}\in\pi_{7}^{6}$ であり, (3) と合成して,
\[
\nu'\eta_{6}\in\pi_{7}^{3}.\tag{9}
\]
また η-family の suspension relation $\eta_{6}=E\eta_{5}$ を用いる. [R5] の Toda Proposition 2.2 に $\alpha=\nu'$, $\beta=\eta_{5}$ を代入すると,
\[
H(\nu'\eta_{6})=H(\nu'\circ E\eta_{5})=H(\nu')\circ E\eta_{5}=\eta_{5}\eta_{6}=\eta_{5}^{2}.\tag{10}
\]
[R3] の $n=5$ の場合より,
\[
\pi_{7}^{5}=\mathbb{Z}/2\{\eta_{5}^{2}\}.\tag{11}
\]
(9), (10), (11) より, $H:\pi_{7}^{3}\to\pi_{7}^{5}$ は生成元 $\eta_{5}^{2}$ を像に持つ. したがって,
\[
H:\pi_{7}^{3}\to\pi_{7}^{5}\quad\text{は全射である.}\tag{12}
\]
(8), (12) の完全性より $\operatorname{Im}H=\ker\Delta=\pi_{7}^{5}$ である. よって,
\[
\Delta:\pi_{7}^{5}\to\pi_{5}^{2}\quad\text{は零写像である.}\tag{13}
\]
さらに (8), (13) より $\operatorname{Im}\Delta=\ker E=0$ なので,
\[
E:\pi_{5}^{2}\to\pi_{6}^{3}\quad\text{は単射である.}\tag{14}
\]
(7), (14) と η-family の suspension relation $E(\eta_{2}^{3})=\eta_{3}^{3}$ より,
\[
\eta_{3}^{3}\text{ の位数は }2\text{ である.}\tag{15}
\]
(5), (15) より,
\[
\nu'\text{ の位数は }4\text{ である.}\tag{16}
\]
最後に, $\pi_{6}^{3}$ の群構造を決定する.
```

### Historical unit H15 (PROSE)

```text
[R2] の $n=5$ の場合より,
\[
\pi_{6}^{5}=\mathbb{Z}/2\{\eta_{5}\}.\tag{17}
\]
(4), (17) より,
\[
H:\pi_{6}^{3}\to\pi_{6}^{5}\quad\text{は全射である.}\tag{18}
\]
(8), (14), (18) より, $E$ は単射, $H$ は全射なので, 次の短完全列を得る.
```

### Historical unit H16 (PROSE)

```text
\[
0\longrightarrow\pi_{5}^{2}\xrightarrow{E}\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}\longrightarrow 0.\tag{19}
\]
(7), (17), (19) より $\pi_{6}^{3}$ の位数は 4 である. 一方, (3), (16) より $\nu'\in\pi_{6}^{3}$ は位数 4 の元なので, $\nu'$ が群全体を生成する.
```

### Historical unit H17 (PROSE)

```text
以上により,
\[
\pi_{6}^{3}=\mathbb{Z}/4\{\nu'\}\tag{20}
\]
を得る.
```

## ADDED

### Current unit C1 (PROSE)

```text
使用する結果を先にまとめる.
```

### Current unit C2 (PROSE)

```text
**[R1] (5.3) / Lemma 5.2.**
**[R2] (5.2).**
**[R3] Proposition 5.1.**
**[R4] Proposition 4.4.**
まず、$\nu'$ を定める.
```

### Current unit C3 (MATH)

```text
$2\eta_{3} = 0$
```

### Current unit C4 (MATH)

```text
$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$
```

### Current unit C5 (MATH)

```text
$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$
```

### Current unit C6 (MATH)

```text
$\pi_{4}^{3} = \mathbb{Z}/2\{E\eta_{2}\}$
```

### Current unit C7 (MATH)

```text
$\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}$
```

### Current unit C8 (PROSE)

```text
Proposition 5.3 を順次適用し、suspension による安定化を用いると、
```

### Current unit C9 (MATH)

```text
$\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$
```

### Current unit C10 (PROSE)

```text
$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である.
```

### Current unit C11 (PROSE)

```text
これより、
$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である.
```

### Current unit C12 (PROSE)

```text
$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.
```

### Current unit C17 (PROSE)

```text
次に、$\nu'$ の位数を決定する.
```

### Current unit C18 (MATH)

```text
$2\nu' = \eta_{3}E\eta_{3}\eta_{5}\tag{1}$
```

### Current unit C19 (MATH)

```text
$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$
```

### Current unit C21 (MATH)

```text
$\operatorname{ord}\left(\nu'\right) = 4$
```

### Current unit C22 (PROSE)

```text
(4) より、
```

### Current unit C23 (MATH)

```text
$\eta_{3}E\eta_{3}\eta_{5} = \eta_{3}^{3}\tag{2}$
```

### Current unit C24 (PROSE)

```text
(1) と (2) より、
```

### Current unit C25 (MATH)

```text
$2\nu' = \eta_{3}^{3}\tag{3}$
```

### Current unit C26 (PROSE)

```text
(5) より、
```

### Current unit C27 (MATH)

```text
$E\eta_{3}\eta_{5} = \eta_{4}^{2}\tag{4}$
```

### Current unit C28 (MATH)

```text
$E\eta_{3} = \eta_{4}\tag{5}$
```

### Current unit C31 (MATH)

```text
$H\left(\nu'\right) = E^{2}\eta_{3}\tag{6}$
```

### Current unit C32 (MATH)

```text
$E^{2}\eta_{3} = \eta_{5}\tag{7}$
```

### Current unit C33 (PROSE)

```text
(6) と (7) より、
```

### Current unit C34 (MATH)

```text
$H\left(\nu'\right) = \eta_{5}\tag{8}$
```

### Current unit C35 (PROSE)

```text
(8) より、
```

### Current unit C36 (MATH)

```text
$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}\tag{9}$
```

### Current unit C38 (PROSE)

```text
$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2}$ は完全である.
```

### Current unit C39 (MATH)

```text
$\eta_{3} = E\eta_{2}\tag{10}$
```

### Current unit C40 (PROSE)

```text
(10) より、
```

### Current unit C41 (MATH)

```text
$E^{n - 3}\eta_{3} = \eta_{n}\tag{11}$
```

### Current unit C43 (PROSE)

```text
$\pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3}$ は完全である.
```

### Current unit C45 (PROSE)

```text
$\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}$ は完全である.
```

### Current unit C47 (PROSE)

```text
$\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2}$ は完全である.
```

### Current unit C49 (PROSE)

```text
$\pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2}$ は完全である.
```

### Current unit C67 (PROSE)

```text
$\pi_{5}^{3} \xrightarrow{E} \pi_{6}^{4} \xrightarrow{H} \pi_{6}^{7}$ は完全である.
```

### Current unit C72 (PROSE)

```text
最後に、$\pi_{6}^{3}$ の群構造を決定するために、次の完全列を考える.
```

### Current unit C73 (MATH)

```text
$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$
```

### Current unit C75 (MATH)

```text
$\nu' \in \pi_{6}^{3}$
```

### Current unit C76 (PROSE)

```text
$\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}$ は完全である.
```

### Current unit C77 (PROSE)

```text
$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.
```

### Current unit C78 (MATH)

```text
$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$
```

### Current unit C80 (MATH)

```text
$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$
```

### Current unit C81 (PROSE)

```text
この完全性と両端の写像の性質より, 次の短完全列を得る.
```

### Current unit C82 (MATH)

```text
$0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$
```

## DUPLICATED

### Current unit C13 (PROSE)

```text
次の完全列を考える.
```

### Current unit C14 (PROSE)

```text
$\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.
```

### Current unit C15 (PROSE)

```text
次の完全列を考える.
```

### Current unit C16 (PROSE)

```text
$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.
```

### Current unit C20 (PROSE)

```text
以上より、
```

### Current unit C29 (PROSE)

```text
次の完全列を考える.
```

### Current unit C30 (PROSE)

```text
$\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$ は完全である.
```

### Current unit C37 (PROSE)

```text
次の完全列を考える.
```

### Current unit C42 (PROSE)

```text
次の完全列を考える.
```

### Current unit C44 (PROSE)

```text
次の完全列を考える.
```

### Current unit C46 (PROSE)

```text
次の完全列を考える.
```

### Current unit C48 (PROSE)

```text
次の完全列を考える.
```

### Current unit C50 (PROSE)

```text
次の完全列を考える.
```

### Current unit C51 (PROSE)

```text
$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.
```

### Current unit C52 (PROSE)

```text
次の完全列を考える.
```

### Current unit C53 (PROSE)

```text
$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1}$ は完全である.
```

### Current unit C54 (PROSE)

```text
次の完全列を考える.
```

### Current unit C55 (PROSE)

```text
$\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.
```

### Current unit C56 (PROSE)

```text
次の完全列を考える.
```

### Current unit C57 (PROSE)

```text
$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.
```

### Current unit C58 (PROSE)

```text
次の完全列を考える.
```

### Current unit C59 (PROSE)

```text
$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.
```

### Current unit C60 (PROSE)

```text
次の完全列を考える.
```

### Current unit C61 (PROSE)

```text
$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1}$ は完全である.
```

### Current unit C62 (PROSE)

```text
次の完全列を考える.
```

### Current unit C63 (PROSE)

```text
$\pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.
```

### Current unit C64 (PROSE)

```text
次の完全列を考える.
```

### Current unit C65 (PROSE)

```text
$\pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.
```

### Current unit C66 (PROSE)

```text
次の完全列を考える.
```

### Current unit C68 (PROSE)

```text
次の完全列を考える.
```

### Current unit C69 (PROSE)

```text
$\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.
```

### Current unit C70 (PROSE)

```text
次の完全列を考える.
```

### Current unit C71 (PROSE)

```text
$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.
```

### Current unit C74 (PROSE)

```text
$\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$ は完全である.
```

### Current unit C79 (PROSE)

```text
以上より、
```
