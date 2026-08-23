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

## 4-5 presentation による完全列計算の一般化

Phase 4-4 までに、

```text
kernel_structure()
image_structure()
cokernel_structure()
```

を presentation ベースで計算できるようになり、

```text
Z^r ⊕ finite torsion
```

という一般の有限生成アーベル群に対する
準同型の kernel / image / cokernel の抽象群構造を
扱えるようになった。

Phase 4-5 ではこの仕組みを完全列計算へ接続し、

```text
A --f--> B --g--> C
```

について、有限群の全元列挙に依存せず、

```text
Im(f)
Ker(g)
B / Im(f)
Im(g)
```

の構造を presentation から計算し、
完全性および第一同型定理から得られる構造関係を
一般の有限生成アーベル群に対して扱えるようにした。

---

### presentation による完全性判定

連続する準同型

```text
A --f--> B --g--> C
```

について、

```text
Im(f) = Ker(g)
```

を presentation / lattice ベースで判定できるようにした。

これにより、中間群 `B` に自由部分が含まれる場合でも
完全性を判定できる。

基本例として、

```text
Z --×2--> Z --mod 2--> Z/2
```

を確認した。

このとき、

```text
Im(×2) = 2Z
Ker(mod 2) = 2Z
```

なので完全であり、

```text
is_exact() = True
```

となる。

一方、

```text
Z --×2--> Z --mod 4--> Z/4
```

では、

```text
Im(×2) = 2Z
Ker(mod 4) = 4Z
```

であるため、

```text
Im(×2) != Ker(mod 4)
```

となり、完全ではないことを正しく判定する。

これにより、

```text
free group
→ free group
→ finite group
```

という、従来の有限群全元列挙方式では扱えなかった
完全列についても判定可能になった。

---

### mixed group を含む完全列

自由部分と torsion 部分を同時に含む
mixed group に対しても完全性判定を確認した。

これにより、

```text
Z^r ⊕ finite torsion
```

を中間群とする完全列についても、

```text
Im(f)
Ker(g)
```

を presentation から計算し、
両者が一致するかを判定できるようになった。

Phase 4-4 で実装した一般準同型計算が、
単独の kernel / image / cokernel 計算だけでなく、
完全列という複数の写像を組み合わせた計算でも
利用できることを確認した。

---

### 有限群での完全性 cross-check

presentation ベースの完全性判定についても、
有限アーベル群では既存の全元列挙方式との
cross-check を追加した。

有限群の場合は従来通り、

```text
Im(f)
Ker(g)
```

を実際の部分群として全元列挙できる。

そこで、

```text
従来方式:
Subgroup の実際の元を比較

presentation 方式:
integer lattice / presentation から比較
```

という独立した2通りの計算を行い、
判定結果が一致することを確認した。

これにより、自由部分を扱うために導入した
presentation ベースの完全性判定が、
既存の有限群計算とも整合していることを確認した。

---

### ExactSequenceStep の一般構造 API

`ExactSequenceStep` から、
完全列の各部分に現れる抽象アーベル群構造を
一般形式で取得できるようにした。

対象は、

```text
A --f--> B --g--> C
```

に対する

```text
Im(f)
Ker(g)
B / Im(f)
Im(g)
```

である。

一般構造として、

```text
image_of_first_structure
kernel_of_second_structure
quotient_structure
image_structure
```

を扱えるようにした。

これらは従来の有限群専用の

```text
()
(2,)
(2,4)
```

のような tuple 表現ではなく、
自由階数と torsion 部分を保持できる
一般のアーベル群構造として扱われる。

そのため、例えば

```text
Z
Z ⊕ Z/2
Z^2
Z/2 ⊕ Z/4
```

などを同じ API で表現できる。

---

### quotient / image の構造比較

完全列

```text
A --f--> B --g--> C
```

が完全なら、

```text
Ker(g) = Im(f)
```

なので第一同型定理から、

```text
B / Im(f) ≅ Im(g)
```

となる。

この関係を、有限群の coset 列挙だけに依存せず、
一般のアーベル群構造として比較できるようにした。

追加された一般構造 API により、

```text
quotient_structure
```

と

```text
image_structure
```

を比較し、

```text
B / Im(f) ≅ Im(g)
```

という構造上の同型関係を確認できる。

これにより自由部分を含む場合でも、
完全列から得られる quotient / image の関係を
追跡できるようになった。

---

### 完全性と「構造が同型」の区別

Phase 4-5 では、

```text
Im(f) = Ker(g)
```

という部分群としての一致と、

```text
B / Im(f) ≅ Im(g)
```

という抽象群構造としての同型を
別の条件として扱うことも確認した。

抽象群構造が同じであることだけから
完全性を判定するのではなく、
完全性そのものは

```text
Im(f) = Ker(g)
```

で判定する。

一方、

```text
quotient_structure
image_structure
```

は完全列から導かれる構造関係を確認するための
別の情報として保持する。

これにより、

```text
部分群として等しい
```

ことと、

```text
抽象アーベル群として同型
```

であることを混同しない設計とした。

---

### EHP 層への一般構造 API の接続

presentation ベースの完全列計算を
EHP 層にも接続した。

`ExactnessResult` に、

```text
image_abelian_structure
kernel_abelian_structure
quotient_abelian_structure
right_image_abelian_structure
```

を追加した。

例えば、

```text
result = segment.exactness_at_sphere()
```

に対して、

```text
result.image_abelian_structure
result.kernel_abelian_structure
result.quotient_abelian_structure
result.right_image_abelian_structure
```

から、

```text
Im(E)
Ker(H)
π / Im(E)
Im(H)
```

の一般アーベル群構造を取得できる。

同様に Hopf target 側では、

```text
Im(H)
Ker(P)
π / Im(H)
Im(P)
```

を同じ API で扱える。

---

### ExactnessResult と ExactSequenceStep の統合

EHP 層で完全列計算のロジックを重複して持たないように、
`ExactnessResult` から `ExactSequenceStep` を利用する形に整理した。

`ExactnessResult` に

```text
exact_step
```

を持たせ、

```text
ExactSequenceStep(
  first_map=left_map,
  second_map=right_map,
)
```

を生成する。

一般構造 API はこの `ExactSequenceStep` に委譲する。

具体的には、

```text
image_abelian_structure
```

は

```text
exact_step.image_of_first_structure
```

に、

```text
kernel_abelian_structure
```

は

```text
exact_step.kernel_of_second_structure
```

に、

```text
quotient_abelian_structure
```

は

```text
exact_step.quotient_structure
```

に、

```text
right_image_abelian_structure
```

は

```text
exact_step.image_structure
```

に対応する。

また、

```text
is_exact()
```

も `ExactSequenceStep.is_exact()` に委譲するようにした。

これにより、

```text
algebra layer
↓
ExactSequenceStep
↓
EHP ExactnessResult
```

という依存関係が明確になり、
完全列計算の中心ロジックを algebra 層へ集約できた。

---

### EHP での確認例

既存の有限 EHP データについて、
新しい一般構造 API が従来結果と一致することを確認した。

#### n = 3, k = 5 の sphere 側

```text
π_7(S^2)
  --E-->
π_8(S^3)
  --H-->
π_8(S^5)
```

について、

```text
Im(E) = 0
Ker(H) = 0
```

なので、

```text
image_abelian_structure
= 0

kernel_abelian_structure
= 0
```

となる。

さらに、

```text
π_8(S^3) / Im(E)
≅ Im(H)
≅ Z/2
```

なので、

```text
quotient_abelian_structure
= Z/2

right_image_abelian_structure
= Z/2
```

となることを確認した。

---

#### n = 3, k = 5 の Hopf target 側

```text
π_8(S^3)
  --H-->
π_8(S^5)
  --P-->
π_6(S^2)
```

では、

```text
Im(H) = Ker(P) ≅ Z/2
```

となり、

```text
image_abelian_structure
= Z/2

kernel_abelian_structure
= Z/2
```

を確認した。

また、

```text
π_8(S^5) / Im(H)
≅ Im(P)
≅ Z/4
```

なので、

```text
quotient_abelian_structure
= Z/4

right_image_abelian_structure
= Z/4
```

となる。

---

#### n = 11, k = 18 の非巡回例

非巡回有限アーベル群を含む既存例でも、

```text
image_abelian_structure
= Z/2 ⊕ Z/2 ⊕ Z/4

kernel_abelian_structure
= Z/2 ⊕ Z/2 ⊕ Z/4
```

となり、

```text
Im(E) = Ker(H)
```

の構造が一致する。

さらに、

```text
quotient_abelian_structure
= Z/2 ⊕ Z/2

right_image_abelian_structure
= Z/2 ⊕ Z/2
```

となり、

```text
B / Im(E) ≅ Im(H)
```

も一般構造 API で確認できた。

---

### 旧 API との後方互換性

既存の有限群用 API は削除せず残した。

従来は、

```text
image_structure
kernel_structure
```

によって、

```text
()
(2,)
(2,2,4)
```

のような有限群の torsion structure を取得していた。

新しい一般構造 API では、
同じ有限群について自由階数が

```text
free_rank = 0
```

となり、

```text
torsion_orders
```

が従来の

```text
image_structure
kernel_structure
```

と一致することをテストした。

つまり有限群に対しては、

```text
旧 API
```

と

```text
新しい presentation ベースの一般 API
```

が同じ結果を返す。

これにより既存コードを維持しながら、
今後 `Z` を含む EHP データへ段階的に移行できる設計となった。

---

### Phase 4-5 の到達点

Phase 4-5 により、

```text
A --f--> B --g--> C
```

という完全列について、

```text
presentation of A, B, C
↓
presentation of f, g
↓
Im(f)
Ker(g)
↓
exactness
↓
B / Im(f)
Im(g)
↓
quotient / image structure comparison
```

という計算経路を、
有限群だけでなく自由部分を含む
有限生成アーベル群へ一般化できた。

Phase 4-4 まででは、

```text
1つの準同型
↓
kernel / image / cokernel
```

を一般化した段階だったが、

Phase 4-5 では、

```text
複数の準同型
↓
完全列
↓
quotient / image relation
```

まで一般化された。

さらに EHP 層も `ExactSequenceStep` を通じて
この一般計算を利用するようになったため、

```text
finite-only EHP calculation
```

から

```text
finitely generated abelian group
を対象とする EHP calculation
```

へ移行するための基盤ができた。

現在の推論経路は、

```text
group presentation
↓
homomorphism matrix
↓
integer lattice
↓
kernel / image / cokernel
↓
exact sequence
↓
quotient / image structure
↓
EHP exactness result
```

となっている。

---

### テスト

2026-08-23

追加・確認した主なテスト:

```text
test_presentation_exact_z_times2_mod2
test_presentation_nonexact_z_times2_mod4
test_presentation_exact_mixed_group
test_finite_exactness_presentation_crosscheck
test_exact_sequence_general_structures_free
test_exact_sequence_general_structures_mixed
test_nonexact_sequence_general_structure_isomorphism
test_ehp_general_structure_api_at_sphere
test_ehp_general_structure_api_at_hopf_target
test_ehp_general_structure_api_noncyclic
test_ehp_old_new_structure_api_agree
test_ehp_exactness_result_delegates_to_exact_step
```

全テスト:

```text
126 passed in 58.91s
```

既存の有限群計算、
Subgroup、
QuotientGroup、
extension candidate、
EHP 完全列計算を含め、
すべてのテストが成功した。

Phase 4-5 の一般化による regression は確認されなかった。

### 状態

Phase 4-5 完了

Phase 4-6a では、自由部分を含む最初の実 EHP 例として
(n,k) = (6,5) を採用する。

EHP segment は

π10(S5) --E--> π11(S6) --H--> π11(S11) --P--> π9(S5)

であり、現在の sphere.csv のデータから

Z/2 --0--> Z --×2--> Z --mod 2--> Z/2

となる。

これは finite → free、free → free、free → finite を
一つの完全列で含み、Phase 4 で導入した presentation ベースの
一般アーベル群計算を実 EHP データで検証する最初の例として適している。

# Phase 4-8：Phase 4 の成果と設計境界の整理

## 4-8a Phase 4 の成果と設計境界

Phase 4 で導入した presentation ベースの計算について、
今後の実装で責務が混在しないように
設計境界を整理した。

Phase 4 の中心的な成果は、

```text
finite abelian group
```

を前提としていた代数計算を、

```text
Z^r ⊕ finite torsion
```

という一般の有限生成アーベル群へ拡張したことである。

現在の一般計算経路は、

```text
finitely generated abelian group
↓
relation matrix
↓
integer lattice
↓
HNF / SNF
↓
kernel / image / cokernel
↓
exact sequence
↓
quotient / image structure
↓
EHP exactness
```

となっている。

---

### algebra 層と EHP 層の境界

一般的な有限生成アーベル群計算は
`algebra.py` の責務とする。

対象には、

```text
kernel
image
cokernel
subgroup
quotient
exact sequence
extension
```

などを含む。

一方、

```text
E
H
P
```

という写像のホモトピー論的意味や、
どの generator がどの generator に写るかというデータは
EHP / homotopy data 層の責務とする。

依存方向は、

```text
EHP layer
↓
ExactSequenceStep / GroupMap
↓
algebra layer
```

とし、algebra 層から EHP 層には依存しない。

---

### 群構造と generator 名の分離

algebra 層では、

```text
Z
Z/2
Z/8 ⊕ Z/4 ⊕ Z/2
```

などの抽象アーベル群構造を扱う。

一方、

```text
η
ν
σ
ξ'
λ'
```

などの generator 名や、
composition relation 上の意味は
homotopy data / proof 層で扱う。

この2つを分離することで、
一般代数計算へ Toda 固有の知識を持ち込まない。

---

### finite enumeration の位置づけ

有限群で使用してきた全元列挙方式は削除せず、

```text
reference implementation
```

として残す。

一般計算では presentation / lattice / HNF / SNF を利用し、
有限群については全元列挙方式との cross-check を行う。

これにより、
自由部分を含む一般計算を実現しながら、
既存の有限群計算を独立した検証手段として利用する。

---

### primary component の境界

algebra 層では、

```text
Z/2
Z/3
Z/4
Z/9
```

などを区別せず、
有限生成アーベル群として統一的に扱う。

したがって、

```text
2-primary
3-primary
double EHP
```

などの区別は上位の homotopy / inference 層で扱う。

これにより将来 odd-primary の計算を追加しても、
algebra 層を変更せず再利用できる設計とする。

---

### 計算と数学的推論の境界

Phase 4 までの基盤が担当するのは、

```text
既知の群
+
既知の準同型
↓
代数計算
```

である。

一方、

```text
なぜその E/H/P の値になるのか
```

を composition relation や Toda bracket などから導くことは、
将来の proof / inference layer の責務とする。

将来的な構造は、

```text
proof / inference
↓
homotopy / EHP data
↓
abelian group algebra
↓
integer linear algebra
```

を基本とする。

### 状態

設計境界の整理完了。

コード変更なし。

---

## 4-8b ドキュメントへの反映

Phase 4-8a で整理した設計方針を
プロジェクトドキュメントへ反映する。

対象:

```text
docs/design.md
docs/development_log.md
README.md
```

主な更新内容:

* presentation ベース計算を現在の標準経路として明記
* 有限群全列挙を reference implementation として位置づけ
* algebra 層と EHP 層の責務を明確化
* 群構造と generator 名を分離
* primary decomposition を algebra 層から分離
* algebra calculation と proof / inference の境界を明確化
* Phase 4 で自由部分を扱えるようになったことを README に反映
* Phase 3 時点の古い README 記述を更新

### Phase 4 の設計上の到達点

Phase 4 によって、

```text
finite-only algebra
```

から、

```text
finitely generated abelian group algebra
```

へ計算基盤を拡張できた。

今後の EHP / Toda 関連の実装では、
有限群・自由部分・mixed group ごとに
別の代数エンジンを作るのではなく、

```text
AbelianGroup
GroupMap
presentation
ExactSequenceStep
```

を共通基盤として利用する。

### Phase 4 完了条件

Phase 4 の完了条件を次のように定める。

* 自由部分を含む有限生成アーベル群を表現できる
* 一般の準同型について kernel / image / cokernel を計算できる
* 自由部分を含む完全列の exactness を判定できる
* quotient / image の抽象群構造を一般形式で比較できる
* EHP 層が一般 presentation 計算を利用できる
* finite enumeration と presentation 計算を明確に分離できる
* algebra / EHP / proof 層の設計境界が文書化されている

extension candidate の自由部分対応や、
Toda relation そのものから準同型を導出する機構は、
この完了条件には含めない。

これらは Phase 4 の algebra 基盤の上に構築する
後続フェーズの課題とする。

### 状態

Phase 4 の成果・責務・完了条件の文書化完了。

コード変更なし。





