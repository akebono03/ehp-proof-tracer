# Phase 162 R10-R8：本文の根拠分岐監査

## 集計

- 証明木ノード：97
- 本文行：47
- 問題候補行：9
- 直接一致のある問題行：7
- 分類：{'OFF_TARGET_H_MAP': 2, 'DELTA_IOTA5': 2, 'WHITEHEAD_SQUARE': 6, 'TRANSPORT_APPENDIX': 1}

## 最終目標の直接前提分岐

- ノード 1、下位ノード 40：`Toda 5.2 pi_4^2 finite-cyclic transport` / `\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}`
- ノード 2、下位ノード 53：`Toda Proposition 5.3 n=3 suspension isomorphism` / `E: \pi_{4}^{2} \xrightarrow{\cong} \pi_{5}^{3}`
- ノード 3、下位ノード 3：`Toda Proposition 5.3 n=3 eta-square suspension bridge` / `E\eta_{2}\eta_{3} = \eta_{3}\eta_{4}`

## 各問題行と根拠ノード

### 行 26 — OFF_TARGET_H_MAP

完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射.

- 本文重複行：[]
- 直接一致：NOT_DIRECTLY_ATTRIBUTED
- 根拠が見つからないため、不要と断定しない

### 行 28 — OFF_TARGET_H_MAP

完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射.

- 本文重複行：[]
- 直接一致：NOT_DIRECTLY_ATTRIBUTED
- 根拠が見つからないため、不要と断定しない

### 行 38 — DELTA_IOTA5, WHITEHEAD_SQUARE

$\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.

- 本文重複行：[38, 54]
- 直接一致：DIRECT_STEP_CANDIDATE
- ノード 40：規則 `Toda Delta iota_5 Whitehead-square relation`、親 [31]、根への経路 (40, 31, 20, 10, 4, 1, 0)、属する直接前提分岐 [1]、同式ノード [40, 61]
- ノード 61：規則 `Toda Delta iota_5 Whitehead-square relation`、親 [47, 92]、根への経路 (61, 47, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [40, 61]

### 行 40 — WHITEHEAD_SQUARE

$[\iota_{2}, \iota_{2}]$.

- 本文重複行：[40, 56]
- 直接一致：DIRECT_STEP_CANDIDATE
- ノード 65：規則 `None`、親 [50]、根への経路 (65, 50, 41, 31, 20, 10, 4, 1, 0)、属する直接前提分岐 [1]、同式ノード [65, 81]
- ノード 81：規則 `None`、親 [71]、根への経路 (81, 71, 62, 47, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [65, 81]

### 行 42 — WHITEHEAD_SQUARE

これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.

- 本文重複行：[42, 58]
- 直接一致：DIRECT_STEP_CANDIDATE
- ノード 50：規則 `Toda Proposition 2.7 iota_2 Whitehead-square Hopf invariant up to sign`、親 [41]、根への経路 (50, 41, 31, 20, 10, 4, 1, 0)、属する直接前提分岐 [1]、同式ノード [50, 71]
- ノード 71：規則 `Toda Proposition 2.7 iota_2 Whitehead-square Hopf invariant up to sign`、親 [62]、根への経路 (71, 62, 47, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [50, 71]

### 行 54 — DELTA_IOTA5, WHITEHEAD_SQUARE

$\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.

- 本文重複行：[38, 54]
- 直接一致：DIRECT_STEP_CANDIDATE
- ノード 40：規則 `Toda Delta iota_5 Whitehead-square relation`、親 [31]、根への経路 (40, 31, 20, 10, 4, 1, 0)、属する直接前提分岐 [1]、同式ノード [40, 61]
- ノード 61：規則 `Toda Delta iota_5 Whitehead-square relation`、親 [47, 92]、根への経路 (61, 47, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [40, 61]

### 行 56 — WHITEHEAD_SQUARE

$[\iota_{2}, \iota_{2}]$.

- 本文重複行：[40, 56]
- 直接一致：DIRECT_STEP_CANDIDATE
- ノード 65：規則 `None`、親 [50]、根への経路 (65, 50, 41, 31, 20, 10, 4, 1, 0)、属する直接前提分岐 [1]、同式ノード [65, 81]
- ノード 81：規則 `None`、親 [71]、根への経路 (81, 71, 62, 47, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [65, 81]

### 行 58 — WHITEHEAD_SQUARE

これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.

- 本文重複行：[42, 58]
- 直接一致：DIRECT_STEP_CANDIDATE
- ノード 50：規則 `Toda Proposition 2.7 iota_2 Whitehead-square Hopf invariant up to sign`、親 [41]、根への経路 (50, 41, 31, 20, 10, 4, 1, 0)、属する直接前提分岐 [1]、同式ノード [50, 71]
- ノード 71：規則 `Toda Proposition 2.7 iota_2 Whitehead-square Hopf invariant up to sign`、親 [62]、根への経路 (71, 62, 47, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [50, 71]

### 行 102 — TRANSPORT_APPENDIX

証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。

- 本文重複行：[]
- 直接一致：DIRECT_STEP_CANDIDATE
- ノード 4：規則 `Toda pi_4^3 eta_3 generator notation`、親 [1]、根への経路 (4, 1, 0)、属する直接前提分岐 [1]、同式ノード [4, 72]
- ノード 63：規則 `Toda 4.5 pi_4^3 finite-cyclic transport`、親 [48]、根への経路 (63, 48, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [63]
- ノード 64：規則 `Toda higher eta-family iterated suspension bridge`、親 [48]、根への経路 (64, 48, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [64]
- ノード 72：規則 `Toda pi_4^3 eta_3 generator notation`、親 [63]、根への経路 (72, 63, 48, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [4, 72]
- ノード 73：規則 `Toda 4.5 stable-range iterated suspension isomorphism`、親 [63]、根への経路 (73, 63, 48, 38, 27, 15, 6, 2, 0)、属する直接前提分岐 [2]、同式ノード [73]

## 判定

証明木のノードは変更していない。上記は「本文に残す数学的必要性」を自動判定するものではない。
