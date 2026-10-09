# Phase 162 R4-B3 共通Renderer出力監査

既存の公開stable専用Rendererは呼び出していない。
既存rootと新しい導出rootを比較した観測結果。

## pi_5^4

### 旧rootからの共通Renderer

エラー: None

flags: `{'has_symbolic_n': True, 'reference_toda45': True, 'has_transport_appendage': True, 'transition_double': True}`

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

### 新しい導出rootからの共通Renderer

エラー: None

flags: `{'has_symbolic_n': True, 'reference_toda45': True, 'has_transport_appendage': True, 'transition_double': True}`

```text
# Group proof narrative

## 使用する結果

**[R1] (4.5).**
$E^{4 - 3}: \pi_{3 + 1}^{3} \to \pi_{4 + 1}^{4}$ は同型写像である.
**[R2] Proposition 5.1.**
$\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ $\;(n \ge 3)$.

---

## 証明

$\pi_{5}^{4}$ の群構造を決定する.

$\eta_{4}=E\eta_{3}$ である.

[R2]より, $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

[R1]より, $\pi_{4 + 1}^{4} = \mathbb{Z}/2\{E^{4 - 3}\eta_{3}\}$.

これより, 以上より, 

$\pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}$.

証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。

$\square$

```

## pi_6^5

### 旧rootからの共通Renderer

エラー: None

flags: `{'has_symbolic_n': True, 'reference_toda45': False, 'has_transport_appendage': True, 'transition_double': True}`

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

### 新しい導出rootからの共通Renderer

エラー: None

flags: `{'has_symbolic_n': True, 'reference_toda45': True, 'has_transport_appendage': True, 'transition_double': True}`

```text
# Group proof narrative

## 使用する結果

**[R1] (4.5).**
$E^{5 - 3}: \pi_{3 + 1}^{3} \to \pi_{5 + 1}^{5}$ は同型写像である.
**[R2] Proposition 5.1.**
$\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ $\;(n \ge 3)$.

---

## 証明

$\pi_{6}^{5}$ の群構造を決定する.

[R2]より, $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

[R1]より, $\pi_{5 + 1}^{5} = \mathbb{Z}/2\{E^{5 - 3}\eta_{3}\}$.

これより, 以上より, 

$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.

証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。

$\square$

```
