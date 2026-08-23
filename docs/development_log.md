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

## 4-4 一般 presentation 計算の堅牢化

Phase 4-3 までに導入した presentation ベースの

* `kernel_structure()`
* `image_structure()`
* `cokernel_structure()`

について、自由部分・有限部分・mixed group を含む一般的なケースで
安定して計算できることを確認した。

### 零群 source の well-defined 判定修正

零群を現在の内部表現では

```text
order = 0
```

として表している。

これは presentation としては

```text
Z / <1> = 0
```

に対応するため、source 側の generator には
1 倍で 0 になる relation がある。

従来の `is_well_defined_homomorphism()` では
`source_order == 0` をそのままスキップしていたため、

```text
0 → Z/4
```

に対する非零行列

```text
[1]
```

などを well-defined と誤判定する可能性があった。

そこで `source_order == 0` の場合は

```text
relation_order = 1
```

として扱い、source relation が target relation に写るかを
通常の presentation の条件として判定するよう修正した。

確認:

```text
0 → Z/4
matrix = [1]
```

は invalid。

一方、

```text
0 → Z/4
matrix = [0]
```

および

```text
0 → Z/4
matrix = [4]
```

は同じ零写像を表す well-defined な準同型として扱える。

このとき、

```text
Ker = 0
Im = 0
Coker = Z/4
```

となることを確認した。

---

### 非対角自由群写像の確認

対角行列だけでなく、基底間の混合を含む一般行列について
presentation 計算を確認した。

例:

```text
f : Z^2 → Z^2
```

行列

```text
[2 1]
[0 2]
```

に対して、

```text
Ker(f)   = 0
Im(f)    = Z^2
Coker(f) = Z/4
```

を正しく計算できることを確認した。

これにより Smith normal form / lattice 計算が
単純な対角写像だけに依存していないことを確認した。

---

### mixed group の非対角写像

自由部分と torsion 部分を同時に含む例として、

```text
f : Z ⊕ Z/4 → Z/6
```

を

```text
f(x,y) = 2x + 3y
```

で定義した。

行列表現:

```text
[2 3]
```

このとき、

```text
Ker(f)   = Z ⊕ Z/2
Im(f)    = Z/6
Coker(f) = 0
```

を正しく計算できることを確認した。

これにより、

```text
free → torsion
torsion → torsion
```

が同時に存在する非対角 mixed map についても
presentation ベースの計算が機能することを確認した。

---

### 有限群との自動 cross-check

presentation 計算の信頼性を高めるため、
有限アーベル群について既存の全元列挙方式と
presentation 方式を自動照合するテストを追加した。

対象群:

```text
0
Z/2
Z/3
Z/4
Z/2 ⊕ Z/2
Z/2 ⊕ Z/4
Z/3 ⊕ Z/3
```

これらの source / target の組について、
係数

```text
0, 1, 2, 3
```

からなる行列を生成し、
well-defined な群準同型だけを抽出した。

各準同型について、

```text
全元列挙方式
```

による

```text
kernel
image
cokernel
```

と、

```text
presentation / lattice / HNF / SNF
```

による

```text
kernel_structure()
image_structure()
cokernel_structure()
```

を比較した。

有限群では全元を列挙できるため、
既存の列挙方式を独立した参照計算として利用した。

比較したすべてのケースで、

```text
Ker
Im
Coker
```

の抽象アーベル群構造が一致した。

これにより presentation ベースの計算が、
個別に用意した例だけでなく、
多数の有限アーベル群準同型についても
既存の列挙計算と整合することを確認した。

---

### Phase 4-4 の到達点

一般アーベル群の準同型について、

```text
G = Z^r ⊕ finite torsion
H = Z^s ⊕ finite torsion
```

という形の source / target に対して、

```text
relation matrix
↓
integer lattice
↓
Hermite normal form
↓
Smith normal form
↓
kernel / image / cokernel structure
```

という計算経路が安定して動作するところまで確認できた。

確認したケースには、

* 自由群
* 有限群
* 自由部分と torsion 部分を含む mixed group
* 零群
* 零写像
* 非対角行列
* 非全射
* 全射
* 非自明 kernel
* 非自明 cokernel
* invalid な準同型
* presentation 上は異なるが同じ写像を表す行列

が含まれる。

また、有限群については
全元列挙方式との大量 cross-check を導入したため、
presentation 計算に対する回帰テストとしても利用できる。

---

### テスト

2026-08-23

```text
114 passed
```

既存の EHP 関連テストを含め、すべて成功。

Phase 4-4 の変更による既存機能への regression は確認されなかった。

### 状態

Phase 4-4 完了




