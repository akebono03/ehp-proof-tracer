# ehp_proof 開発記録

## Phase 1：有限群計算の安定化

### 完了内容

- `GroupElement`
- `GroupMap.apply()`
- `GroupMap.kernel()`
- `GroupMap.image()`
- EHP 完全列の完全性判定
- `n=3, k=5` のテスト
- `n=11, k=18` のテスト

### 状態

完了

---

## Phase 2：部分群を構造として扱う

### 2-1 Subgroup 型

実装:

- `ambient_group`
- `elements`
- `generators`
- `order`
- 部分群の等値判定

完了

### 2-2 kernel / image の Subgroup 化

実装:

- `GroupMap.kernel_subgroup()`
- `GroupMap.image_subgroup()`

完了

### 2-3 生成元の計算

実装:

- `generated_subgroup_elements()`
- `find_generators()`

`Z/2 ⊕ Z/2` の非巡回部分群についてテスト。

完了

### 2-4 部分群の抽象群構造

`Subgroup.structure()` を実装。

例:

```text
0             -> ()
Z/2           -> (2,)
Z/4           -> (4,)
Z/2 ⊕ Z/2     -> (2, 2)
```

完了

### 2-5 structure() の一般化テスト

確認済み:

```text
Z/2 ⊕ Z/4     -> (2, 4)
Z/4 ⊕ Z/12    -> (4, 12)
0              -> ()
```

完了

### 2-6 EHP への統合

`ExactnessResult.image()` と `kernel()` を、
元の集合ではなく `Subgroup` を返すように変更。

追加:

- `image_structure`
- `kernel_structure`

完全性

```text
Im(f) = Ker(g)
```

を `Subgroup` の等号で判定するように変更。

確認例:

- `n=3, k=5`
- `n=11, k=18`

### テスト

2026-08-21

```text
18 passed
```

### 状態

Phase 2 完了

---

# Phase 3：完全列から群構造を推論する

## 3-1 商群

実装:

- `QuotientGroup`
- coset
- quotient addition
- quotient order
- quotient structure

これにより部分群 `H ⊂ G` に対して

```text
G / H
```

を有限アーベル群として扱えるようにした。

完了

---

## 3-2 第一同型定理

実装:

- `InducedMap`

準同型

```text
f : G → H
```

に対して、

```text
G / Ker(f) ≅ Im(f)
```

を構成・検証できるようにした。

確認項目:

- well-defined
- injective
- surjective
- isomorphism

完了

---

## 3-3 完全列と商群

`ExactSequenceStep` を導入。

連続する写像

```text
A --f--> B --g--> C
```

について、

```text
Im(f)
Ker(g)
B / Im(f)
Im(g)
```

をまとめて扱えるようにした。

完全なら

```text
Im(f) = Ker(g)
```

から

```text
B / Im(f) ≅ Im(g)
```

を検証できる。

完了

---

## 3-4 EHP との接続

`EHPSegment` に `ExactSequenceStep` を接続。

追加:

- `exact_step_at_sphere()`
- `exact_step_at_hopf_target()`

確認例:

- `n=3, k=5`
- `n=11, k=18`

既存の `ExactnessResult` API は残し、
商群・誘導同型の処理を追加する形とした。

完了

---

## 3-5 extension candidate

短完全列

```text
0 → A → B → C → 0
```

について、候補 `B` が実際に extension の中間群として
成立し得るかを判定する仕組みを追加。

実装:

- `ExtensionCandidate`
- `all_subgroups()`
- `group_structure()`
- `valid_extension_candidates()`

例:

```text
0 → Z/2 → B → Z/2 → 0
```

では、

```text
B ≅ Z/4
```

と

```text
B ≅ Z/2 ⊕ Z/2
```

の両方が候補となる。

完全列だけでは extension が一意に決まらないことを
候補集合として保持できるようにした。

完了

---

## 3-6 有限アーベル群候補の自動生成

実装:

- `finite_group_order()`
- `finite_abelian_structures()`
- `abstract_abelian_group()`
- `extension_candidates()`

例えば

```text
|B| = 8
```

から有限アーベル群の候補

```text
Z/8
Z/2 ⊕ Z/4
Z/2 ⊕ Z/2 ⊕ Z/2
```

を自動生成できる。

さらに extension 条件を使って、
実際に可能な候補のみを残す。

例:

```text
0 → Z/4 → B → Z/2 → 0
```

では、

```text
Z/8
Z/2 ⊕ Z/4
```

が候補として残り、

```text
Z/2 ⊕ Z/2 ⊕ Z/2
```

は除外される。

完了

---

## 3-7 EHP から群候補を推論

`ExactSequenceStep` から extension に必要な

```text
Im(f)
Im(g)
```

を抽象群として取り出し、
中間群候補を自動生成できるようにした。

追加:

- `extension_left_group`
- `extension_right_group`
- `middle_group_candidates()`
- `middle_group_candidate_structures()`

`EHPSegment` にも候補取得 API を追加。

- `sphere_group_candidates()`
- `sphere_group_candidate_structures()`
- `hopf_target_group_candidates()`
- `hopf_target_group_candidate_structures()`

### 確認例

`n=3, k=5` の sphere 側では、

```text
0 → 0 → π_8(S^3) → Z/2 → 0
```

から

```text
π_8(S^3) ≅ Z/2
```

が一意に候補として得られる。

Hopf target 側では、

```text
0 → Z/2 → π_8(S^5) → Z/4 → 0
```

から

```text
Z/8
Z/2 ⊕ Z/4
```

の2候補が得られる。

既知値

```text
π_8(S^5) = Z/8
```

が候補集合に含まれることを確認。

完了

---

# Phase 3 の到達点

現在、

```text
EHP data
↓
kernel / image
↓
Subgroup
↓
exact sequence
↓
quotient
↓
short exact sequence
↓
extension candidates
↓
possible middle-group structures
```

という推論パイプラインができている。

単に既知の EHP 完全列を検証するだけでなく、
完全性から群構造の候補を生成する段階まで進んだ。

### テスト

2026-08-23

```text
62 passed
```

### 状態

Phase 3 完了

---

# 現在の制限

現段階の quotient / extension 推論は
有限アーベル群を対象としている。

一部の処理では、

- 全元列挙
- 全部分群列挙

を行っているため、大きな有限群では計算量が問題になる可能性がある。

また、自由部分 `Z` を含む群については
代数層の対応がまだ不完全。

---

# 次の予定

## Phase 4：自由部分 Z の扱い

有限群だけでなく、

```text
Z
Z ⊕ Z/2
Z ⊕ Z/4
```

などの自由部分を含むアーベル群を
同じ代数層で扱えるようにする。

特に、

- `GroupElement`
- `GroupMap`
- kernel / image
- subgroup
- quotient
- exact sequence

における自由部分の表現方法を整理する。

---

# 作業メモ

## 2026-08-21

Phase 2 完了。

```text
18 passed
```

次は Phase 3 の商群へ進む。

## 2026-08-23

Phase 3 完了。

```text
62 passed
```

EHP 完全列から有限アーベル群の
extension candidate を生成できるところまで実装。

次は Phase 4 として自由部分 `Z` の扱いを検討する。



