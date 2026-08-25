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


# Phase 5：Proof / Inference 基盤

## Phase 5-1：Proof / Relation 基盤

Phase 4 までで、

```text
既知の群
+
既知の準同型
↓
kernel / image / cokernel
↓
exactness
↓
quotient / extension
```

という代数計算基盤が整った。

Phase 5 ではその上に、
「なぜその結果が得られたのか」を記録・追跡するための
proof / inference 層を導入する。

Phase 5-1 では、
証明追跡の最小データモデルとして、

```text
Relation
ProofStep
Proof
```

を導入した。

---

### Relation

既知の数学的事実や関係式を表すため、
`Relation` を導入した。

基本構造:

```text
lhs
rhs
relation_type
source
note
```

例えば、

```text
2η3 = 0
```

のような既知 relation を、

```python
Relation(
  lhs="2η3",
  rhs="0",
  relation_type=RelationType.ZERO,
  source="Toda",
)
```

として保持できる。

現段階では `lhs`、`rhs` の型を特定の式クラスに限定せず、
汎用的な値を保持できる設計とした。

これは将来的に、

```text
ord(α) = 2
Ker(H) = ...
Im(E) = ...
π_n(S^m) ≅ ...
```

など、
単純なホモトピー元の式以外の命題も扱う可能性があるためである。

---

### RelationType

relation の種類を区別するため、
`RelationType` を導入した。

Phase 5-1 では最小限として、

```text
EQUALITY
ZERO
ORDER
```

を定義した。

現段階では relation の分類を細かくしすぎず、
必要になった段階で、

```text
composition
suspension
Hopf invariant
Toda bracket
Whitehead product
```

などへ拡張する方針とする。

---

### ProofStep

1回の推論または計算を表すため、
`ProofStep` を導入した。

基本構造は、

```text
premises
↓
rule
↓
conclusion
```

とする。

保持する情報:

```text
conclusion
premises
rule
note
```

例えば、

```text
Ker(H) = ...
```

という algebra 層による計算や、

```text
Im(E) = Ker(H)
```

という EHP 完全性の適用を、
独立した ProofStep として記録できる。

---

### ProofRule

ProofStep がどの種類の処理から得られたかを区別するため、
`ProofRule` を導入した。

Phase 5-1 では、

```text
GIVEN
RELATION
EHP_EXACTNESS
KERNEL_COMPUTATION
IMAGE_COMPUTATION
COKERNEL_COMPUTATION
```

を定義した。

これにより、

```text
既知事実
relation の利用
EHP 完全性
kernel 計算
image 計算
cokernel 計算
```

を区別して記録できる。

---

### Proof

特定の結論へ至る一連の ProofStep を保持するため、
`Proof` を導入した。

基本構造:

```text
conclusion
steps
```

Phase 5-1 では、
ProofStep の順序付きリストとして保持する。

例えば、

```text
step 1
Ker(H) を計算

step 2
Im(E) を計算

step 3
EHP 完全性を適用
```

という推論過程を、
1つの Proof としてまとめられる。

将来的には、
複数の推論が同じ中間結果を共有する場合を考慮して
依存関係グラフへの拡張を想定する。

ただし Phase 5-1 では DAG は導入しない。

---

### Relation と ProofStep の区別

Phase 5-1 では、
数学的入力と計算・推論結果を明確に分離した。

```text
Relation
= 既知の数学的事実

ProofStep
= Relation や計算結果を使った1回の推論

Proof
= 特定の結論へ至る ProofStep の集合
```

例えば、

```text
2η_n = 0
```

が文献から既知である場合は `Relation` とする。

一方、

```text
Ker(H) ≅ Z/2
```

が `algebra.py` の kernel 計算によって得られた場合は
`ProofStep` として扱う。

---

### algebra 層との境界

Phase 5-1 では、
既存の algebra 層に proof の概念を追加していない。

依存方向は、

```text
proof / inference layer
↓
homotopy / EHP data layer
↓
algebra layer
↓
integer linear algebra
```

とする。

`algebra.py` は引き続き、

```text
kernel
image
cokernel
quotient
exactness
extension
```

などの純粋な代数計算だけを担当する。

---

### Phase 5-1 の到達点

Phase 5-1 により、

```text
数学的入力
↓
Relation

計算・推論
↓
ProofStep

証明全体
↓
Proof
```

という proof tracking の基本構造を導入できた。

ただしこの段階では、
ホモトピー元や式を構造化する仕組みはまだ持たず、
文字列などの汎用値を relation に格納する形としている。

---

### テスト

確認した主な内容:

```text
Relation の生成
RelationType の保持
ProofStep の生成
premises の保持
ProofRule の保持
Proof の step 順序保持
```

既存の algebra / EHP 計算には変更を加えていない。

### 状態

Phase 5-1 完了

---

## Phase 5-2：Expression / HomotopyElement

Phase 5-1 では Relation の `lhs` / `rhs` に
文字列などを格納していた。

Phase 5-2 では、

```text
η_n
ν_n
σ_n
2η_n
η_nη_{n+1}
0
```

などのホモトピー論的な式を、
文字列ではなく構造化されたオブジェクトとして
保持するための最小 Expression モデルを導入した。

---

### Expression

ホモトピー論的な式の基底として、
`Expression` を導入した。

Phase 5-2 では、

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
└── Composition
```

という最小構成とした。

Expression 層は、
式の数学的構造を保持することだけを責務とし、

```text
評価
簡約
relation 適用
dimension check
```

などは行わない。

---

### Zero

零元を文字列 `"0"` ではなく、
`Zero` オブジェクトとして表現できるようにした。

例えば、

```text
2η3 = 0
```

の右辺を、

```python
Zero()
```

として保持できる。

これにより将来的に、
文字列解析をせずに零元かどうかを判定できる。

---

### HomotopyElement

基本的なホモトピー元を表すため、
`HomotopyElement` を導入した。

保持する情報:

```text
name
dimension
```

例えば、

```text
η3
ν4
σ8
```

を、

```python
HomotopyElement("η", 3)
HomotopyElement("ν", 4)
HomotopyElement("σ", 8)
```

として表現できる。

現段階では、

```text
どのホモトピー群に属するか
source / target dimension
stable element との対応
```

などの意味論は持たせていない。

---

### generator factory

基本 generator を簡潔に生成するため、

```text
eta(n)
nu(n)
sigma(n)
```

を導入した。

例えば、

```python
eta(3)
```

は、

```python
HomotopyElement("η", 3)
```

を生成する。

これにより relation データを記述するときの
可読性を高めた。

---

### Multiple

整数倍を表すため、
`Multiple` を導入した。

保持する情報:

```text
coefficient
expression
```

例えば、

```text
2η3
```

を、

```python
Multiple(
  2,
  eta(3),
)
```

として構造的に保持できる。

Phase 5-2 では、

```text
1α = α
0α = 0
```

などの式簡約はまだ行わない。

---

### Composition

合成を表すため、
`Composition` を導入した。

保持する情報:

```text
left
right
```

例えば、

```text
η3η4
```

を、

```python
Composition(
  eta(3),
  eta(4),
)
```

として保持できる。

現段階では、
composition が dimension 上定義可能かどうかの検査は行わない。

---

### Expression の構造的 equality

各 Expression クラスは frozen dataclass として実装した。

このため、

```python
eta(3) == eta(3)
```

や、

```python
Multiple(
  2,
  eta(3),
) == Multiple(
  2,
  eta(3),
)
```

のような構造的 equality が利用できる。

これは後続の relation repository で、
式を文字列へ変換せず検索するための基礎となる。

---

### Relation と Expression の接続

Phase 5-1 で導入した `Relation` の `lhs` / `rhs` に、
Expression オブジェクトを格納できることを確認した。

例えば、

```text
2η3 = 0
```

を、

```python
Relation(
  lhs=Multiple(
    2,
    eta(3),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

として表現できる。

これにより、

```text
文字列としての relation
```

から、

```text
構造化された数学的 relation
```

へ進む基盤ができた。

---

### Relation の型はまだ Expression に限定しない

Phase 5-2 では、
`Relation.lhs` / `Relation.rhs` を
`Expression` 型へ限定する変更は行っていない。

将来的に、

```text
ord(α) = 2
Ker(H) = ...
Im(E) = ...
π_n(S^m) ≅ ...
```

など、
単純な Expression より広い命題を扱う可能性があるためである。

より一般的な `Statement` モデルが必要かどうかは、
実際に proof engine を構築する段階で判断する。

---

### GroupElement との区別

`HomotopyElement` と、
algebra 層の `GroupElement` は別概念として扱う。

```text
HomotopyElement
= η_n, ν_n, σ_n などの数学的 generator

GroupElement
= 抽象アーベル群内の具体的な座標
```

したがって、

```text
HomotopyElement
≠
GroupElement
```

とする。

将来的には homotopy data 層で両者を対応付ける可能性はあるが、
同一クラスにはしない。

---

### Expression と表示処理の分離

Phase 5-2 では、
Expression 自体に表示形式を持たせていない。

例えば `eta(3)` を、

```text
η3
η₃
\eta_3
```

のどの形式で表示するかは、
数学的な式構造とは別の責務とする。

将来的には、

```text
Expression
↓
formatter
├── plain text
├── Unicode
└── TeX
```

という表示層を追加できる構造を想定する。

---

### Phase 5-2 の到達点

Phase 5-2 により、

```text
HomotopyElement
↓
Multiple / Composition
↓
Expression
↓
Relation
```

という構造ができた。

これにより既知の数学的 relation を、

```text
文字列
```

ではなく、

```text
構造化された式
```

として保持できるようになった。

ただし、

```text
relation の検索
relation の適用
式変形
pattern matching
自動推論
```

はまだ行わない。

これらは後続フェーズの責務とする。

---

### テスト

確認した主な内容:

```text
HomotopyElement
eta()
nu()
sigma()
Zero
Multiple
Composition
Expression の構造的 equality
Relation への Expression 格納
```

既存の algebra / EHP / repository の仕様には変更を加えていない。

### 状態

Phase 5-2 完了


## Phase 5-3：Relation Repository

既知の数学的 relation を保存・検索するため、
`RelationRepository` を導入した。

実装:

- `add_relation()`
- `all_relations()`
- `find_relations()`

検索条件:

- `lhs`
- `rhs`
- `relation_type`
- `source`

複数条件は AND として扱う。

Expression は frozen dataclass として構造的 equality を持つため、

Multiple(2, eta(3))

などを文字列へ変換することなく検索キーとして使用できる。

`SphereRepository` とは責務を分離し、
既存の EHP / sphere.csv データ取得機能には変更を加えていない。

現段階では relation の検索のみを担当し、

- relation の適用
- 式変形
- pattern matching
- 自動推論

は行わない。

これらは後続の proof / inference layer の責務とする。

### テスト

2026-08-24

164 passed in 54.81s

既存の algebra / EHP / proof / expression を含め、
すべてのテストが成功した。

### 状態

Phase 5-3 完了


## Phase 5-4〜5-10：Proof 構築と依存関係の導入

Relation Repository の導入後、
既知 relation と algebra / EHP 計算結果を
実際の Proof trace として構築する機能を段階的に追加した。

---

### algebra 計算結果の ProofStep 化

以下の計算結果を ProofStep として保持できるようにした。

```text
Ker(f)
Im(f)
Coker(f)
```

追加:

```text
KernelStatement
ImageStatement
CokernelStatement

kernel_proof_step()
image_proof_step()
cokernel_proof_step()
```

各 ProofStep は、
既存の `GroupMap` の presentation ベース計算を利用して
一般アーベル群構造を conclusion として保持する。

algebra 層自体には proof の概念を追加していない。

---

### exactness の ProofStep 化

連続する準同型、

```text
A --f--> B --g--> C
```

について、

```text
Im(f)
Ker(g)
```

の ProofStep を premises とし、

```text
Im(f) = Ker(g)
```

を conclusion とする
`ExactnessStatement` を導入した。

追加:

```text
ExactnessStatement
exactness_proof_step()
```

これにより完全性判定の結果だけでなく、

```text
どの image 計算と kernel 計算を使ったか
```

を ProofStep の依存関係として保持できるようになった。

---

### EHP exactness proof

一般の exactness ProofStep を EHP 層へ接続した。

追加:

```text
ehp_exactness_proof_step()
ehp_exactness_proof()
ehp_sphere_proof()
ehp_hopf_target_proof()
```

例えば sphere 側では、

```text
Im(E)
Ker(H)
Im(E) = Ker(H)
```

という3 step の Proof を構築できる。

Hopf target 側では、

```text
Im(H)
Ker(P)
Im(H) = Ker(P)
```

という Proof を構築できる。

これにより、

```text
exact = True
```

だけではなく、
完全性の計算過程を明示的に保持できるようになった。

---

### Proof formatter

Proof の内部モデルと表示処理を分離するため、
formatter を導入した。

追加:

```text
format_expression()
format_statement()
format_proof_step()
format_proof()
```

Expression について、

```text
0
η_n
2η_n
η_nη_{n+1}
```

を人間が読める形式で表示できる。

また、

```text
KernelStatement
ImageStatement
CokernelStatement
ExactnessStatement
Relation
```

も同じ formatter から表示できる。

---

### ProofStep の番号表示

Proof 全体を表示するとき、
各 ProofStep に通し番号を付けるようにした。

例:

```text
1. Im(E) ≅ 0
   [image computation]

2. Ker(H) ≅ 0
   [kernel computation]

3. Im(E) = Ker(H)
   [ehp exactness]
```

step number は Proof model に保持せず、
formatter が Proof.steps の順序から生成する。

---

### premises の表示

ProofStep の `premises` を
Proof 表示へ反映するようにした。

例えば、

```text
3. Im(E) = Ker(H)
   [ehp exactness]
   Premises: 1, 2
```

と表示される。

ProofStep の内部では step object への参照を保持し、
formatter がその参照を Proof 内の step number へ変換する。

これにより Proof の依存関係を人間が確認できるようになった。

---

### Relation を ProofStep 化

Repository から取得された既知 relation を
proof の中で利用するため、

```text
relation_proof_step()
```

を導入した。

例えば、

```text
2η_3 = 0
```

という Relation は、

```text
1. 2η_3 = 0
   [relation]
```

という ProofStep として扱える。

Relation 自体は数学的入力として維持し、
Proof の依存関係には ProofStep を利用する。

---

### Relation を premise とする推論

Relation を実際の推論の premise として利用する仕組みを追加した。

追加:

```text
relation_inference_proof_step()
relation_inference_proof()
```

例えば、

```text
2η_3 = 0
```

から、

```text
η_3 has order dividing 2
```

を導く Proof を、

```text
1. 2η_3 = 0
   [relation]

2. η_3 has order dividing 2
   [relation]
   Premises: 1
```

として構築できる。

`relation_inference_proof_step()` は、
premise が、

```text
ProofRule.RELATION
```

を持つ ProofStep であり、
その conclusion が Relation であることを検証する。

これにより Relation Repository の検索結果を、
実際の proof dependency へ接続できた。

---

### Phase 5-10 の到達点

現在、

```text
Expression
↓
Relation
↓
RelationRepository
↓
relation ProofStep
↓
inference ProofStep
↓
Proof
↓
formatter
```

という経路が動作している。

また EHP 計算についても、

```text
GroupMap
↓
image / kernel calculation
↓
ProofStep
↓
EHP exactness
↓
Proof
↓
formatter
```

という trace を構築できる。

したがって、
既知 relation による数学的推論と、
algebra / EHP による計算結果を、
同じ Proof / ProofStep モデルで扱う基盤ができた。

### 状態

Phase 5-10 完了。

次は Phase 5-11 として、

```text
Relation.source
Relation.note
ProofStep.note
```

などの metadata を
Proof formatter に反映する。


## Phase 5-11：Relation metadata の Proof 表示

Relation および ProofStep が保持している metadata を
Proof formatter に反映した。

対象:

```text
Relation.source
Relation.note
ProofStep.note
```

---

### Relation source の表示

Relation が `source` を持つ場合、
relation ProofStep に出典を表示するようにした。

例:

```text
1. 2η_3 = 0
   [relation]
   Source: Toda
```

これにより、
Proof trace 上で relation の数学的内容だけでなく、
その relation がどの文献・データソースに由来するかを
確認できるようになった。

---

### Relation note の表示

Relation 自体に付随する補足情報を表示できるようにした。

例:

```text
1. 2η_3 = 0
   [relation]
   Source: Toda
   Relation note: classical eta relation
```

`Relation.note` は、
relation そのものについての metadata とする。

---

### ProofStep note の表示

ProofStep 自体に付随する補足情報も
formatter に反映した。

例:

```text
2. η_3 has order dividing 2
   [relation]
   Premises: 1
   Note: derived from the zero relation
```

`ProofStep.note` は、
relation 自体の metadata ではなく、
その step における推論・利用方法についての補足とする。

したがって、

```text
Relation.note
```

と、

```text
ProofStep.note
```

は別の意味として維持する。

---

### metadata を持たない場合

`source` / `note` が `None` の場合には、
対応する行を表示しない。

これにより既存の EHP proof や
metadata を持たない ProofStep の表示形式は維持される。

---

### 確認例

```text
1. 2η_3 = 0
   [relation]
   Source: Toda
   Relation note: classical eta relation

2. η_3 has order dividing 2
   [relation]
   Premises: 1
   Note: derived from the zero relation

Conclusion:

η_3 has order dividing 2
```

これにより、

```text
数学的事実
+
出典
+
relation の補足
+
その relation を使った推論
+
proof dependency
```

を同じ Proof trace 上で確認できるようになった。

---

### テスト

追加した主なテスト:

```text
test_format_relation_source
test_format_relation_note
test_format_proof_step_note
test_format_relation_and_proof_step_notes
```

2026-08-24:

```text
200 passed in 24.79s
```

既存の algebra / EHP / expression / proof / repository を含め、
すべてのテストが成功した。

### 状態

Phase 5-11 完了。


## Phase 5-12：Relation source の構造化

Phase 5-11 では、

```text
Relation.source
```

を Proof formatter に表示できるようにしたが、
source 自体は、

```python
source="Toda"
```

のような単純な文字列だった。

Phase 5-12 では、
relation の出典をより詳細に追跡できるようにするため、
構造化された文献参照を導入した。

---

### LiteratureReference

追加:

```text
LiteratureReference
```

保持する情報:

```text
label
author
title
year
locator
```

例えば、

```python
LiteratureReference(
  label="Toda",
  author="H. Toda",
  title=(
    "Composition Methods in "
    "Homotopy Groups of Spheres"
  ),
  year=1962,
  locator="...",
)
```

のように、
relation の文献情報を構造として保持できる。

`locator` は、
relation が文献中のどこに記載されているかを表す。

現段階では locator は文字列として保持し、
theorem / proposition / page 等を専用型には分割しない。

---

### Relation.source の拡張

Relation の `source` を、

```text
LiteratureReference | str | None
```

として扱えるようにした。

これにより、

```python
source="Toda"
```

という既存形式を維持したまま、

```python
source=LiteratureReference(...)
```

という structured source へ段階的に移行できる。

既存 Relation データに対する breaking change は導入していない。

---

### formatter の拡張

追加:

```text
format_literature_reference()
format_source()
```

structured source の場合には、

```text
label
author
title
year
locator
```

を組み合わせて表示する。

例:

```text
Source: Toda — H. Toda, Composition Methods in Homotopy Groups of Spheres, 1962 — ...
```

一方、従来の、

```python
source="Toda"
```

については、

```text
Source: Toda
```

と従来通り表示される。

---

### Relation metadata との責務分離

Phase 5-11 で導入した metadata の区別を維持した。

```text
LiteratureReference
= relation の出典

Relation.note
= relation 自体の数学的補足

ProofStep.note
= その relation を利用した推論上の補足
```

文献上の theorem / proposition / page 等の情報は
`Relation.note` ではなく、
`LiteratureReference.locator` に保持する。

---

### RelationRepository との互換性

`LiteratureReference` は frozen dataclass のため、
構造的 equality を利用できる。

既存の `RelationRepository.find_relations()` を変更せず、

```python
repository.find_relations(
  source=reference,
)
```

によって structured source を持つ Relation を検索できることを確認した。

Phase 5-12 では source の、

```text
author
title
year
locator
```

などによる部分検索は追加していない。

---

### Proof 表示確認

structured source を持つ relation について、
次の形式で Proof 表示できることを確認した。

```text
1. 2η_3 = 0
   [relation]
   Source: Toda — H. Toda, Composition Methods in Homotopy Groups of Spheres, 1962 — ...
   Relation note: classical eta relation

2. η_3 has order dividing 2
   [relation]
   Premises: 1
   Note: derived from the zero relation

Conclusion:

η_3 has order dividing 2
```

probe で使用した locator は
Phase 5-12 の structured source 表示を確認するための
ダミー値であり、実際の Toda 文献上の proposition 番号を
確定したものではない。

---

### テスト

追加した主なテスト:

```text
test_literature_reference
test_relation_with_literature_reference
test_format_literature_reference
test_format_source_string
test_format_source_literature_reference
test_format_relation_structured_source
test_relation_repository_find_by_structured_source
```

2026-08-24:

```text
207 passed in 20.65s
```

既存の algebra / EHP / expression / proof / formatter /
repository を含め、すべてのテストが成功した。

structured source 導入による regression は確認されなかった。

### 状態

Phase 5-12 完了。


## Phase 5-13：複数 Relation / ProofStep を用いる inference

Phase 5-12 までの relation inference は、
基本的に1つの Relation ProofStep を premise としていた。

Phase 5-13 では、
複数の既知 relation および
既存の ProofStep を同時に premise とできるように
relation inference を一般化した。

---

### ProofStep 入力の正規化

追加:

```text
_normalize_proof_steps()
_normalize_relations()
```

単一の、

```text
ProofStep
Relation
```

と、

```text
tuple / list
```

の両方を受け取り、
内部では tuple に統一する。

`_normalize_proof_steps()` は、
ProofStep または ProofStep の tuple / list を受け取る。

`_normalize_relations()` は、
Relation または Relation の tuple / list を受け取る。

不正な型が含まれている場合は
`TypeError` とする。

これにより既存の単一入力 API を維持したまま、
複数入力へ拡張できるようになった。

---

### 複数 relation inference

`relation_inference_proof_step()` を拡張し、

```text
relation_steps
```

として複数の Relation ProofStep を
受け取れるようにした。

例えば、

```text
1. 2η_3 = 0
   [relation]

2. 2η_4 = 0
   [relation]

3. combined result
   [relation]
   Premises: 1, 2
```

という Proof を構築できる。

---

### 追加 ProofStep の利用

relation 以外の既存 ProofStep も、

```text
premises
```

として inference に追加できるようにした。

これにより将来的に、

```text
文献 relation
+
別の relation
+
kernel / image 計算結果
+
以前に導出した中間結果
↓
新しい結論
```

という推論を同じ Proof モデルで表現できる。

`relation_steps` と追加の `premises` を分離したことで、

```text
既知の数学的 relation
```

と、

```text
既存の計算・推論結果
```

を API 上で区別できる。

---

### relation step の検証

`relation_steps` に指定された ProofStep は、

```text
ProofRule.RELATION
```

を持ち、

```text
conclusion
```

が `Relation` であることを要求する。

一般の ProofStep を利用する場合は、
追加の `premises` として渡す。

例えば `ProofRule.GIVEN` の step を
`relation_steps` に渡した場合は
`ValueError` とする。

一方、

```text
premises
```

として渡す場合は、
一般の ProofStep を利用できる。

---

### 空 relation の禁止

relation inference には
少なくとも1つの Relation が必要とした。

したがって、

```text
relation_steps = ()
```

および、

```text
relations = ()
```

は `ValueError` とする。

relation を使用しない一般的な inference は、
今後別の API として設計する。

---

### 後方互換性

従来の、

```python
relation_inference_proof_step(
  conclusion,
  relation_step,
)
```

および、

```python
relation_inference_proof(
  relation,
  conclusion,
)
```

もそのまま利用できる。

単一 input は内部で tuple へ正規化する。

既存コードへの breaking change は導入していない。

---

### formatter

formatter は既に複数 premise の番号表示に対応していたため、
Phase 5-13 では formatter 本体の変更は行わなかった。

integration test により、

```text
Premises: 1, 2
```

が正しく表示されることを確認した。

---

### probe による確認

複数の Relation を利用する probe を作成した。

使用した relation:

```text
2η_3 = 0
2η_4 = 0
```

出力:

```text
1. 2η_3 = 0
   [relation]
   Source: Toda — H. Toda, Composition Methods in Homotopy Groups of Spheres, 1962
   Relation note: first example relation

2. 2η_4 = 0
   [relation]
   Source: Toda — H. Toda, Composition Methods in Homotopy Groups of Spheres, 1962
   Relation note: second example relation

3. combined result
   [relation]
   Premises: 1, 2
   Note: derived from two relations

Conclusion:

combined result
```

これにより、
複数の Relation ProofStep が
実際の proof dependency として利用されることを確認した。

---

### テスト

追加した主なテスト:

```text
test_relation_inference_proof_step_multiple_relations
test_relation_inference_proof_step_with_additional_premise
test_relation_inference_proof_multiple_relations
test_relation_inference_proof_with_additional_premise
test_relation_inference_proof_step_rejects_empty_relations
test_relation_inference_proof_rejects_empty_relations
test_relation_inference_proof_step_rejects_invalid_additional_premise
test_format_multiple_relation_inference_proof
```

2026-08-24:

```text
215 passed in 20.68s
```

既存の algebra / EHP / expression / proof / formatter /
repository を含め、
すべてのテストが成功した。

Phase 5-13 の一般化による regression は確認されなかった。

---

### Phase 5-13 の到達点

Phase 5-13 により、

```text
Relation
↓
ProofStep

Relation
↓
ProofStep

既存の計算・推論
↓
ProofStep

複数 ProofStep
↓
relation inference
↓
新しい ProofStep
```

という推論構造を扱えるようになった。

これにより、
単一 relation を premise とする最小 proof から、
複数の数学的事実や計算結果を組み合わせる
一般的な proof dependency へ一段階進んだ。

ただし、

```text
premise の再帰的収集
Proof DAG の自動構築
relation の pattern matching
relation の自動選択
結論の自動生成
```

はまだ実装していない。

これらは後続フェーズの課題とする。

### 状態

Phase 5-13 完了。


## Phase 5-14：InferenceRule の導入

Phase 5-13 までに、
複数の Relation および既存 ProofStep を
premises とする inference を構築できるようになった。

しかし inference step は、

```text
ProofRule.RELATION
```

という大分類しか持たず、

```text
どの数学的規則を用いて
premises から conclusion を導いたか
```

は構造化されていなかった。

Phase 5-14 では、
具体的な数学的推論規則を表すため、

```text
InferenceRule
```

を導入した。

---

### InferenceRule

追加:

```text
InferenceRule
```

保持する情報:

```text
name
description
```

例えば、

```python
InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
  ),
  description=(
    "If m alpha = 0, "
    "the order of alpha divides m."
  ),
)
```

のように推論規則を構造化できる。

---

### ProofStep への接続

`ProofStep` に、

```text
inference_rule
```

を追加した。

型は、

```text
InferenceRule | None
```

とした。

これにより、

```text
premises
+
InferenceRule
↓
conclusion
```

という推論構造を保持できる。

既存の ProofStep との互換性を維持するため、
`inference_rule` は optional とした。

---

### ProofRule との区別

Phase 5-14 では、

```text
ProofRule
```

と、

```text
InferenceRule
```

を別概念として扱う。

`ProofRule` は、

```text
RELATION
EXACTNESS
EHP_EXACTNESS
KERNEL_COMPUTATION
IMAGE_COMPUTATION
COKERNEL_COMPUTATION
```

など、
ProofStep の処理の大分類を表す。

一方 `InferenceRule` は、

```text
zero relation implies order bound
```

など、
具体的な数学的推論規則を表す。

そのため relation inference step は、

```text
ProofRule.RELATION
```

を維持したまま、

```text
InferenceRule
```

も保持する。

---

### relation inference API の拡張

以下に、

```text
inference_rule
```

引数を追加した。

```text
relation_inference_proof_step()
relation_inference_proof()
```

これにより、

```python
relation_inference_proof(
  relation,
  conclusion,
  inference_rule=rule,
)
```

として推論規則を明示できる。

従来形式も維持しているため、

```python
relation_inference_proof(
  relation,
  conclusion,
)
```

も引き続き利用できる。

---

### inference_rule の型検証

追加:

```text
_validate_inference_rule()
```

`inference_rule` は、

```text
InferenceRule
```

または、

```text
None
```

のみを受け付ける。

文字列などの不正な値を渡した場合は、

```text
TypeError
```

とする。

---

### formatter の拡張

追加:

```text
format_inference_rule()
```

ProofStep が InferenceRule を持つ場合、

```text
Inference rule: ...
```

を表示するようにした。

確認例:

```text
1. 2η_3 = 0
   [relation]
   Source: Toda — H. Toda, Composition Methods in Homotopy Groups of Spheres, 1962
   Relation note: example zero relation

2. η_3 has order dividing 2
   [relation]
   Inference rule: zero relation implies order bound
   Premises: 1
   Note: derived from the zero relation

Conclusion:

η_3 has order dividing 2
```

これにより、

```text
relation の内容
relation の出典
relation の補足
使用した inference rule
premises
inference step の補足
```

を同じ Proof trace 上で区別して確認できる。

---

### 後方互換性

InferenceRule は optional としたため、
既存の ProofStep や relation inference は
変更せず利用できる。

InferenceRule を指定しない場合、

```text
step.inference_rule is None
```

となる。

既存の algebra / EHP proof にも
InferenceRule の指定を強制していない。

---

### 実装整理

Phase 5-14 実装時に、
`proof.py` 内で重複していた、

```text
_normalize_proof_steps()
_normalize_relations()
```

の定義を1つずつに整理した。

動作上は後側の定義が使用されていたため
テスト結果への影響はなかったが、
同一 helper の重複定義を削除して
実装を整理した。

---

### テスト

追加した主なテスト:

```text
test_inference_rule
test_relation_inference_proof_step_with_inference_rule
test_relation_inference_proof_with_inference_rule
test_relation_inference_without_inference_rule_is_backward_compatible
test_relation_inference_rejects_invalid_inference_rule
test_multiple_relation_inference_with_inference_rule
test_format_inference_rule
test_format_proof_step_inference_rule
test_format_relation_inference_with_rule
```

2026-08-24:

```text
224 passed in 21.47s
```

既存の algebra / EHP / expression / proof / formatter /
repository を含め、
すべてのテストが成功した。

InferenceRule 導入による regression は確認されなかった。

---

### Phase 5-14 の到達点

Phase 5-14 により、

```text
premises
↓
InferenceRule
↓
conclusion
```

という推論規則そのものを
ProofStep に明示できるようになった。

Phase 5-13 では、

```text
何を premise として使ったか
```

まで追跡できる状態だった。

Phase 5-14 ではさらに、

```text
どの規則で導いたか
```

まで追跡できるようになった。

ただし現段階の InferenceRule は、
推論規則の metadata を保持するだけであり、

```text
premise pattern
pattern matching
applicability 判定
conclusion 自動生成
rule 自動適用
```

はまだ行わない。

これらは後続フェーズの課題とする。

### 状態

Phase 5-14 完了。


## Phase 5-15：InferenceRule に premise pattern を持たせるための最小基盤

Phase 5-14 では、
具体的な数学的推論規則を表す

```text
InferenceRule
```

を導入し、

```text
premises
↓
InferenceRule
↓
conclusion
```

という構造を ProofStep に保持できるようになった。

Phase 5-15 ではさらに、

```text
その InferenceRule が
どのような premise を必要とするか
```

を構造化して保持するための
最小基盤を導入した。

---

### PremisePattern

追加:

```text
PremisePattern
```

保持する情報:

```text
proof_rule
statement_type
relation_type
```

定義:

```python
@dataclass(frozen=True)
class PremisePattern:
  proof_rule: ProofRule | None = None
  statement_type: type | None = None
  relation_type: RelationType | None = None
```

各項目は optional とし、
必要な条件だけを指定できる。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

によって、

```text
ProofRule.RELATION
+
conclusion が Relation
+
RelationType.ZERO
```

という premise の要求を表現できる。

---

### InferenceRule の拡張

`InferenceRule` に、

```text
premise_patterns
```

を追加した。

現在の構造:

```python
@dataclass(frozen=True)
class InferenceRule:
  name: str
  description: str | None = None
  premise_patterns: tuple[PremisePattern, ...] = ()
```

既存の InferenceRule との
後方互換性を維持するため、

```text
premise_patterns = ()
```

をデフォルトとした。

そのため従来の、

```python
InferenceRule(
  name="example rule",
)
```

も変更せず利用できる。

---

### ZERO relation を要求する rule

例えば、

```python
InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
  ),
  description=(
    "If m alpha = 0, "
    "the order of alpha divides m."
  ),
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.RELATION,
      statement_type=Relation,
      relation_type=RelationType.ZERO,
    ),
  ),
)
```

のように、

```text
ZERO relation を premise とする推論規則
```

を構造として記述できるようになった。

Phase 5-14 では、

```text
zero relation implies order bound
```

という rule 名と説明だけを保持していたが、

Phase 5-15 では、

```text
その rule が ZERO relation を要求する
```

こともデータとして保持できる。

---

### 複数 premise pattern

`premise_patterns` は tuple としたため、
複数の premise を要求する rule も表現できる。

例えば、

```text
ZERO relation
+
GIVEN ProofStep
```

を要求する rule を、

```python
InferenceRule(
  name="combined rule",
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.RELATION,
      statement_type=Relation,
      relation_type=RelationType.ZERO,
    ),
    PremisePattern(
      proof_rule=ProofRule.GIVEN,
    ),
  ),
)
```

として保持できる。

現段階では、
実際の premises と pattern の対応付けや
matching は行わない。

---

### PremisePattern の構造的 equality

`PremisePattern` は frozen dataclass とした。

そのため、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

同士は構造的 equality によって比較できる。

これは後続フェーズで、

```text
pattern の比較
rule definition のテスト
matching の検証
```

を行うための基礎となる。

---

### 既存 inference API への影響

Phase 5-15 では、

```text
relation_inference_proof_step()
relation_inference_proof()
```

の挙動は変更していない。

InferenceRule が `premise_patterns` を持っていても、

```text
実際に与えられた premises が
その pattern に一致しているか
```

はまだ検証しない。

したがって今回の変更は、

```text
InferenceRule の specification を拡張
```

するものであり、

```text
InferenceRule の自動適用
```

を導入するものではない。

---

### Expression pattern は未導入

Phase 5-15 では、

```text
ProofRule
statement type
RelationType
```

までを pattern 条件として扱う。

例えば、

```text
mα = 0
```

について、

```text
lhs が Multiple
rhs が Zero
coefficient を m として束縛
expression を α として束縛
```

といった Expression 内部の pattern matching は
まだ導入していない。

また、

```text
pattern variable
unification
substitution
```

もまだ行わない。

---

### 実装整理

Phase 5-14 時点で整理した
`proof.py` の既存 helper 構造を維持したまま、

```text
PremisePattern
```

と、

```text
InferenceRule.premise_patterns
```

のみを追加した。

既存の、

```text
Relation
ProofStep
Proof
InferenceRule
relation inference
EHP proof
formatter
```

の API には breaking change を導入していない。

---

### テスト

新規追加:

```text
tests/test_inference_rule_pattern.py
```

追加したテスト:

```text
test_premise_pattern_defaults
test_premise_pattern_relation
test_inference_rule_without_premise_patterns
test_inference_rule_with_premise_pattern
test_inference_rule_multiple_premise_patterns
test_premise_pattern_is_structurally_equal
```

確認内容:

```text
PremisePattern のデフォルト値
proof_rule の保持
statement_type の保持
relation_type の保持
InferenceRule の後方互換性
単一 premise pattern
複数 premise pattern
PremisePattern の構造的 equality
```

2026-08-24:

```text
230 passed in 20.65s
```

既存の algebra / EHP / expression / proof / formatter /
repository を含め、
すべてのテストが成功した。

PremisePattern 導入による regression は確認されなかった。

---

### Phase 5-15 の到達点

Phase 5-14 では、

```text
どの数学的 inference rule を使ったか
```

を ProofStep に記録できるようになった。

Phase 5-15 ではさらに、

```text
その inference rule が
どの種類の premise を必要とするか
```

を構造化して保持できるようになった。

現在、

```text
InferenceRule
├── name
├── description
└── premise_patterns
      ├── proof_rule
      ├── statement_type
      └── relation_type
```

という rule specification を表現できる。

ただし現段階では、

```text
PremisePattern
+
ProofStep
↓
match / no match
```

という判定はまだ行わない。

また、

```text
Expression pattern
pattern variable
変数束縛
InferenceRule applicability
conclusion 自動生成
relation 自動選択
rule 自動適用
```

もまだ実装していない。

これらは後続フェーズで段階的に追加する。

### 状態

Phase 5-15 完了。

次は Phase 5-16 として、

```text
PremisePattern と ProofStep の match 判定
```

を導入し、

```text
rule が要求する premise
```

と、

```text
実際の ProofStep
```

を機械的に比較できる最小基盤へ進む。


## Phase 5-16：PremisePattern と ProofStep の match 判定

Phase 5-15 では、

```text
InferenceRule
└── premise_patterns
      ├── proof_rule
      ├── statement_type
      └── relation_type
```

という構造を導入し、

```text
InferenceRule が
どのような premise を要求するか
```

を記述できるようにした。

ただし Phase 5-15 時点では、
PremisePattern は specification を保持するだけであり、

```text
実際の ProofStep が
その pattern に一致するか
```

を判定する機能はまだ存在しなかった。

Phase 5-16 では、
1つの PremisePattern と
1つの ProofStep を比較する
最小 matching 基盤を追加した。

---

### matches_premise_pattern()

追加:

```text
matches_premise_pattern()
```

基本形:

```python
matches_premise_pattern(
  pattern,
  step,
)
```

`PremisePattern` と `ProofStep` を受け取り、

```text
True
False
```

を返す。

Phase 5-16 では、

```text
proof_rule
statement_type
relation_type
```

の3条件を判定対象とする。

---

### 空 pattern の matching

条件を何も指定しない、

```python
PremisePattern()
```

は、
任意の ProofStep に一致するようにした。

つまり、

```text
None
```

になっている pattern field は、

```text
その項目について条件を設けない
```

という wildcard として扱う。

例えば、

```python
pattern = PremisePattern()

step = ProofStep(
  conclusion="given fact",
  premises=(),
  rule=ProofRule.GIVEN,
)
```

に対して、

```python
matches_premise_pattern(
  pattern,
  step,
)
```

は `True` となる。

---

### proof_rule の matching

pattern に、

```text
proof_rule
```

が指定されている場合、

```text
step.rule
```

と一致することを要求する。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.GIVEN,
)
```

は `ProofRule.GIVEN` の step に一致する。

一方、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
)
```

に対して `ProofRule.GIVEN` の step を渡した場合は、

```text
False
```

となる。

---

### statement_type の matching

pattern に、

```text
statement_type
```

が指定されている場合、

```text
step.conclusion
```

がその型であることを `isinstance()` で確認する。

例えば、

```python
PremisePattern(
  statement_type=Relation,
)
```

は conclusion が Relation である ProofStep に一致する。

conclusion が文字列など別の型である場合は、

```text
False
```

となる。

---

### relation_type の matching

pattern に、

```text
relation_type
```

が指定されている場合、

まず、

```text
step.conclusion
```

が Relation であることを確認する。

Relation でなければ、

```text
False
```

とする。

Relation である場合は、

```text
step.conclusion.relation_type
```

と、

```text
pattern.relation_type
```

を比較する。

例えば、

```python
PremisePattern(
  relation_type=RelationType.ZERO,
)
```

は、

```text
RelationType.ZERO
```

の Relation を conclusion とする step に一致する。

`RelationType.EQUALITY` などであれば一致しない。

---

### 複数条件の matching

複数条件を指定した場合は、
すべての条件を満たすことを要求する。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

は、

```text
ProofRule.RELATION
+
conclusion が Relation
+
RelationType.ZERO
```

をすべて満たす ProofStep にのみ一致する。

一部だけ一致する場合は、

```text
False
```

となる。

これにより PremisePattern の各 field を、
AND 条件として機械的に解釈できるようになった。

---

### 不正な入力型の検証

`matches_premise_pattern()` に
不正な型を渡した場合は、
match failure ではなく `TypeError` とする。

例えば、

```python
matches_premise_pattern(
  "invalid",
  step,
)
```

は、

```text
TypeError
```

となる。

同様に、

```python
matches_premise_pattern(
  pattern,
  "invalid",
)
```

も `TypeError` とする。

これにより、

```text
正しい pattern / step を比較して一致しなかった
```

場合の `False` と、

```text
API の入力自体が不正
```

な場合を区別できるようにした。

---

### InferenceRule との接続範囲

Phase 5-16 では、

```text
InferenceRule.premise_patterns
```

全体の applicability 判定までは追加していない。

今回追加したのは、

```text
1つの PremisePattern
+
1つの ProofStep
↓
match / no match
```

という最小 primitive のみである。

したがって、

```text
複数 premise pattern
+
複数 ProofStep
```

について、

```text
どの step をどの pattern に対応させるか
```

はまだ自動判定しない。

この部分は次の段階で扱う。

---

### Expression matching は未導入

Phase 5-16 の matching は、

```text
ProofRule
statement type
RelationType
```

までに限定した。

例えば、

```text
2η_3 = 0
```

と、

```text
3ν_4 = 0
```

がともに、

```text
ProofRule.RELATION
Relation
RelationType.ZERO
```

であれば、
同じ PremisePattern に一致する。

まだ、

```text
Multiple
Zero
coefficient
HomotopyElement
```

など Expression 内部の構造は判定しない。

また、

```text
pattern variable
variable binding
unification
substitution
```

も導入していない。

---

### テスト

`tests/test_inference_rule_pattern.py` に
matching 関係のテストを追加した。

新規追加した主なテスト:

```text
test_empty_premise_pattern_matches_any_step
test_premise_pattern_matches_proof_rule
test_premise_pattern_rejects_wrong_proof_rule
test_premise_pattern_matches_statement_type
test_premise_pattern_rejects_wrong_statement_type
test_premise_pattern_matches_relation_type
test_premise_pattern_rejects_wrong_relation_type
test_relation_type_requires_relation_conclusion
test_premise_pattern_matches_all_conditions
test_premise_pattern_requires_all_conditions
test_matches_premise_pattern_rejects_invalid_pattern
test_matches_premise_pattern_rejects_invalid_step
```

確認内容:

```text
空 pattern が任意 step に一致すること
proof_rule の一致
proof_rule の不一致
statement_type の一致
statement_type の不一致
relation_type の一致
relation_type の不一致
relation_type 指定時に Relation conclusion を要求すること
複数条件の完全一致
複数条件の一部不一致
不正 pattern の拒否
不正 ProofStep の拒否
```

Phase 5-15 までの PremisePattern 関係テストを含む
`test_inference_rule_pattern.py` 全体について、

```text
18 passed
```

を確認した。

Phase 5-15 完了時の全テスト数は、

```text
230 passed
```

であり、
Phase 5-16 では12テストを追加している。

プロジェクト全体の最新テスト結果は、
全テストスイート実行時に改めて記録する。

---

### Phase 5-16 の到達点

Phase 5-15 では、

```text
InferenceRule が
どの種類の premise を要求するか
```

を specification として記述できるようになった。

Phase 5-16 ではさらに、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

という最小 matching 基盤ができた。

これにより、

```text
rule requirement
```

と、

```text
実際の proof step
```

を機械的に比較する最初の機能が導入された。

現在の matching は、

```text
proof_rule
statement_type
relation_type
```

という ProofStep レベルの条件だけを扱う。

まだ、

```text
InferenceRule applicability
複数 pattern と複数 premise の対応
Expression pattern
pattern variable
変数束縛
conclusion 自動生成
relation 自動選択
premise 自動選択
rule 自動適用
```

は行わない。

### 状態

Phase 5-16 完了。

次は、

```text
InferenceRule.premise_patterns
+
実際の複数 ProofStep
↓
applicable / not applicable
```

という InferenceRule 全体の applicability 判定を
導入する段階へ進む。


## Phase 5-17：InferenceRule.premise_patterns 全体と複数 ProofStep の適合判定

Phase 5-16 では、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

という個別 premise matching を導入した。

Phase 5-17 では、
この個別 matcher を組み合わせ、

```text
InferenceRule.premise_patterns
+
複数 ProofStep
↓
rule-level match / no match
```

を判定できるようにした。

---

### matches_inference_rule()

追加:

```text
matches_inference_rule()
```

基本形:

```python
matches_inference_rule(
  inference_rule,
  steps,
)
```

`InferenceRule` と、
単一または複数の ProofStep を受け取り、

```text
True
False
```

を返す。

---

### ProofStep の正規化

`steps` は、

```text
ProofStep
tuple of ProofStep
list of ProofStep
```

を受け付ける。

既存の、

```text
_normalize_proof_steps()
```

を利用して内部では tuple に統一する。

これにより単一 premise の rule について、

```python
matches_inference_rule(
  rule,
  step,
)
```

と、

```python
matches_inference_rule(
  rule,
  (step,),
)
```

および、

```python
matches_inference_rule(
  rule,
  [step],
)
```

を同じ意味で扱える。

---

### pattern と step の順序付き対応

Phase 5-17 では、

```text
premise_patterns[0] ↔ steps[0]
premise_patterns[1] ↔ steps[1]
...
```

という位置対応を採用した。

例えば、

```text
pattern 1 = RELATION
pattern 2 = GIVEN
```

に対して、

```text
step 1 = RELATION
step 2 = GIVEN
```

なら match する。

一方、

```text
step 1 = GIVEN
step 2 = RELATION
```

のように順序を逆にした場合は match しない。

これにより Phase 5-15 以来未確定だった
`premise_patterns` の tuple 順序について、

```text
premise の対応順を表す
```

という意味を Phase 5-17 で確定した。

---

### premise 数の完全一致

InferenceRule が持つ、

```text
premise_patterns
```

の数と、
実際に渡された ProofStep の数が
一致することを要求する。

数が異なる場合は、

```text
False
```

を返す。

したがって、

```text
premise 不足
```

だけでなく、

```text
余分な premise
```

も不適合とする。

---

### 個別 matching の再利用

各 pattern と step の適合判定には、
Phase 5-16 で導入した、

```text
matches_premise_pattern()
```

をそのまま利用する。

すべての対応する pattern / step が一致した場合のみ、

```text
True
```

となる。

これにより、

```text
proof_rule
statement_type
relation_type
```

に関する個別 matching logic を
`matches_inference_rule()` 側へ重複実装していない。

---

### 空 premise rule

```python
InferenceRule(
  name="no premise rule",
)
```

のように、

```text
premise_patterns = ()
```

である rule は、

```text
steps = ()
```

に一致する。

一方、
空 pattern の rule に非空の steps を渡した場合は
一致しない。

これにより、

```text
premise_patterns = ()
```

を、

```text
premise を必要としない rule
```

として一貫して扱える。

---

### 不正な入力

第1引数が InferenceRule でない場合は、

```text
TypeError
```

とする。

また steps が、

```text
ProofStep
tuple/list of ProofStep
```

でない場合や、
tuple / list 内に ProofStep 以外が含まれる場合も、

```text
TypeError
```

とする。

これにより、

```text
正しい rule と steps を比較した結果の不一致
```

と、

```text
API への不正入力
```

を区別する。

---

### matching の設計境界

Phase 5-17 では、

```text
明示的に与えられた ProofStep 列が
InferenceRule.premise_patterns に一致するか
```

だけを判定する。

まだ、

```text
多数の既存 ProofStep の中から
rule に一致する premise の組を探す
```

ことは行わない。

また、

```text
順序なし matching
複数候補の探索
Expression-level pattern
pattern variable
変数束縛
conclusion 自動生成
```

も導入していない。

---

### テスト

`tests/test_inference_rule_pattern.py` に
Phase 5-17 のテストを追加した。

追加した主なテスト:

```text
test_inference_rule_matches_single_premise
test_inference_rule_rejects_single_wrong_premise
test_inference_rule_matches_multiple_premises
test_inference_rule_rejects_wrong_multiple_premise
test_inference_rule_matching_is_ordered
test_inference_rule_rejects_too_few_steps
test_inference_rule_rejects_too_many_steps
test_empty_inference_rule_matches_empty_steps
test_empty_inference_rule_rejects_nonempty_steps
test_matches_inference_rule_accepts_single_proof_step
test_matches_inference_rule_accepts_tuple
test_matches_inference_rule_accepts_list
test_matches_inference_rule_rejects_invalid_rule
test_matches_inference_rule_rejects_invalid_steps
test_matches_inference_rule_rejects_invalid_step_in_list
```

確認内容:

```text
単一 premise の一致
単一 premise の不一致
複数 premise の一致
複数 premise の一部不一致
順序違いの拒否
premise 不足の拒否
余分な premise の拒否
空 rule と空 steps の一致
空 rule と非空 steps の不一致
単一 ProofStep 入力
tuple 入力
list 入力
不正 rule の拒否
不正 steps の拒否
list 内の不正 step の拒否
```

---

### 全テスト

2026-08-24:

```text
257 passed in 20.88s
```

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
```

を含め、
全257テストが成功した。

Phase 5-17 の rule-level matching 導入による
regression は確認されなかった。

---

### Phase 5-17 の到達点

Phase 5-16 では、

```text
1 pattern
+
1 ProofStep
↓
match / no match
```

までを実装した。

Phase 5-17 ではさらに、

```text
InferenceRule
└── premise_patterns

        +

複数 ProofStep
        ↓
matches_inference_rule()
        ↓
True / False
```

という rule-level matching が可能になった。

これにより、

```text
InferenceRule が要求する premise specification
```

と、

```text
実際に使用しようとしている ProofStep 群
```

を機械的に比較できるようになった。

現段階では、
premise は順序付き・完全一致で比較する。

まだ、

```text
既存 ProofStep 群からの候補 premise 探索
順序なし matching
Expression pattern
pattern variable
変数束縛
conclusion 自動生成
rule 自動適用
```

は行わない。

### 状態

Phase 5-17 完了。

次は、
既存の ProofStep 集合から
InferenceRule の premise_patterns に適合する
premise 候補を探索する最小機構を検討する。


## Phase 5-18：既存 ProofStep 集合から matching premise を探索

Phase 5-17 では、

```text
InferenceRule.premise_patterns
+
明示的に指定した ProofStep 列
↓
matches_inference_rule()
↓
True / False
```

という rule-level matching を導入した。

Phase 5-18 では一段階進めて、
利用可能な ProofStep 集合の中から、

```text
InferenceRule.premise_patterns
```

に適合する ProofStep を
実際に探索する機能を追加した。

---

### find_matching_premises()

追加:

```text
find_matching_premises()
```

基本形:

```python
find_matching_premises(
  inference_rule,
  available_steps,
)
```

`InferenceRule` と、
利用可能な ProofStep を受け取り、

```text
matching ProofStep tuple
```

または、

```text
None
```

を返す。

これにより、

```text
この premises が rule に合うか
```

を確認するだけでなく、

```text
既存の ProofStep の中から
rule に必要な premises を探す
```

ことが可能になった。

---

### available_steps の正規化

`available_steps` には、

```text
ProofStep
tuple of ProofStep
list of ProofStep
```

を指定できる。

既存の、

```text
_normalize_proof_steps()
```

を利用して内部では tuple に統一する。

したがって、

```python
find_matching_premises(
  rule,
  step,
)
```

と、

```python
find_matching_premises(
  rule,
  (step,),
)
```

および、

```python
find_matching_premises(
  rule,
  [step],
)
```

を同じ形式で扱える。

---

### available_steps 全体からの探索

Phase 5-17 の `matches_inference_rule()` では、

```text
premise_patterns[0] ↔ steps[0]
premise_patterns[1] ↔ steps[1]
```

という明示的な位置対応を利用していた。

Phase 5-18 の `find_matching_premises()` では、
各 premise pattern ごとに、

```text
available_steps
```

全体から一致する ProofStep を探索する。

例えば、

```text
available steps:
1. GIVEN
2. RELATION
```

に対して、

```text
patterns:
1. RELATION
2. GIVEN
```

であれば、

```text
pattern 1 → available step 2
pattern 2 → available step 1
```

として、

```text
(
  relation_step,
  given_step,
)
```

を返すことができる。

これにより、
available_steps 自体を
rule の premise 順に事前整列して渡す必要がなくなった。

---

### first-match selection

1つの pattern に複数の ProofStep が一致する場合は、

```text
available_steps 内で
最初に一致した ProofStep
```

を採用する。

例えば、

```text
pattern = GIVEN
```

に対して、

```text
first_step  = GIVEN
second_step = GIVEN
```

が存在する場合、

```text
first_step
```

を返すことを確認した。

Phase 5-18 では、
すべての候補や候補組合せを列挙せず、
最初の一致を利用する最小実装とした。

---

### ProofStep の再利用禁止

複数 premise pattern が同じ条件を要求していても、
1つの ProofStep を複数 pattern に使い回さない。

例えば、

```text
patterns:
GIVEN
GIVEN
```

に対して、
利用可能な step が、

```text
GIVEN step
```

1つだけの場合は、

```text
None
```

を返す。

一方、

```text
GIVEN step 1
GIVEN step 2
```

の2つが存在すれば、

```text
(
  step 1,
  step 2,
)
```

を返す。

実装では、
使用済みの available step index を記録して
後続 pattern の探索から除外する。

---

### premise 不足

必要な premise pattern の一部しか
満たせない場合は、

```text
None
```

を返す。

例えば、

```text
patterns:
RELATION
GIVEN
```

に対して、

```text
RELATION step
```

だけが存在する場合、
最初の pattern は一致するが
2つ目を満たせないため、
探索全体を失敗とする。

部分的に一致した tuple は返さない。

---

### premise を持たない rule

```text
premise_patterns = ()
```

の InferenceRule については、

```text
()
```

を返す。

この場合、
available_steps に ProofStep が存在していても
それらは使用しない。

これにより、

```text
()
= premise を必要としない rule の探索成功

None
= 必要な premise が見つからなかった
```

を区別できる。

---

### RelationType を含む pattern search

既存の `matches_premise_pattern()` を利用するため、

```text
proof_rule
statement_type
relation_type
```

を条件とする検索がそのまま利用できる。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

を持つ rule に対して、

```text
EQUALITY relation
ZERO relation
```

の順で available_steps が存在する場合、
ZERO relation の ProofStep を正しく選択することを確認した。

---

### matching 処理の再利用

`find_matching_premises()` 内で、
PremisePattern の条件判定を再実装せず、

```text
matches_premise_pattern()
```

を利用する構造とした。

現在の関係は、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
```

を最小単位として、

```text
InferenceRule
+
explicit ProofSteps
↓
matches_inference_rule()
```

および、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
```

の両方が構築されている。

---

### greedy search

Phase 5-18 の探索は、
各 premise pattern について、

```text
available_steps の先頭から探索
↓
最初に一致した未使用 step を採用
↓
次の pattern へ進む
```

という greedy な方式とした。

現段階では、

```text
最初の選択を後から取り消す
別の組合せを試す
すべての candidate assignment を列挙する
```

といった backtracking は行わない。

一般的な premise assignment は
後続フェーズで検討する。

---

### 入力検証

以下を確認した。

```text
不正な inference_rule
不正な available_steps
list 内の不正な ProofStep
```

これらについて、
既存 API と同様に `TypeError` とする。

---

### 追加テスト

追加した主なテスト:

```text
test_find_matching_premises_single_step
test_find_matching_premises_searches_available_steps
test_find_matching_premises_multiple_patterns
test_find_matching_premises_returns_first_match
test_find_matching_premises_does_not_reuse_step
test_find_matching_premises_uses_distinct_steps
test_find_matching_premises_returns_none_when_missing
test_find_matching_premises_partial_failure
test_find_matching_premises_empty_rule
test_find_matching_premises_empty_rule_ignores_available_steps
test_find_matching_premises_matches_relation_type
test_find_matching_premises_accepts_single_step
test_find_matching_premises_accepts_list
test_find_matching_premises_rejects_invalid_rule
test_find_matching_premises_rejects_invalid_steps
test_find_matching_premises_rejects_invalid_step_in_list
```

Phase 5-18 では、
`find_matching_premises()` に関する
16個のテストを追加した。

プロジェクト全体の最新テスト件数は、
全テストスイート実行結果を確認した時点で
改めて記録する。

---

### Phase 5-18 の到達点

Phase 5-16 では、

```text
1 PremisePattern
+
1 ProofStep
↓
match / no match
```

を実装した。

Phase 5-17 では、

```text
InferenceRule
+
明示的 ProofStep 列
↓
rule-level match / no match
```

まで進んだ。

Phase 5-18 ではさらに、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
selected ProofSteps
```

という premise candidate search が可能になった。

これにより、

```text
rule requirement の記述
↓
個別 matching
↓
rule 全体の matching
↓
existing ProofSteps からの premise search
```

という段階的な inference 基盤ができた。

ただし現段階の探索は、

```text
premise_patterns の順に探索
available_steps の先頭から first match
同一 step の再利用なし
greedy
```

という最小方式である。

まだ、

```text
全 candidate の列挙
backtracking
複数 assignment
Expression pattern
pattern variable
variable binding
conclusion 自動生成
RelationRepository からの自動 relation 選択
InferenceRule の自動適用
recursive proof construction
proof DAG
```

は行わない。

### 状態

Phase 5-18 完了。

次は、
探索された premises を利用して、

```text
InferenceRule
+
available ProofSteps
↓
matching premises
↓
rule applicability
↓
inference step
```

へ接続する最小機構を検討する。


## Phase 5-19：InferenceRule の applicability 判定

Phase 5-18 では、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
matched premises / None
```

という premise search を追加した。

Phase 5-19 では、
この機能を利用して、

```text
現在利用できる ProofStep だけで
InferenceRule を適用可能か
```

を直接判定する API を追加した。

---

### is_inference_rule_applicable()

追加:

```text
is_inference_rule_applicable()
```

基本形:

```python
is_inference_rule_applicable(
  inference_rule,
  available_steps,
)
```

返り値:

```text
True
False
```

実装は、

```python
find_matching_premises(
  inference_rule,
  available_steps,
) is not None
```

という形とした。

これにより、
premise search の matching logic を重複させず、

```text
matching premise が存在する
→ applicable

matching premise が存在しない
→ not applicable
```

という判定だけを追加した。

---

### premise search への委譲

`is_inference_rule_applicable()` 自体には、

```text
PremisePattern matching
available_steps search
used-step management
input normalization
RelationType matching
```

などを実装していない。

これらは既存の、

```text
find_matching_premises()
matches_premise_pattern()
_normalize_proof_steps()
```

へ委譲する。

そのため現在は、

```text
matches_premise_pattern()
= individual premise matching

matches_inference_rule()
= explicit premise sequence matching

find_matching_premises()
= premise search

is_inference_rule_applicable()
= applicability query
```

という役割分担になった。

---

### applicable な基本例

```text
pattern:
GIVEN

available:
GIVEN
```

の場合、

```text
find_matching_premises()
→ (given_step,)
```

となるため、

```text
is_inference_rule_applicable()
→ True
```

となることを確認した。

一方、

```text
pattern:
RELATION

available:
GIVEN
```

では、

```text
find_matching_premises()
→ None
```

となり、

```text
is_inference_rule_applicable()
→ False
```

となる。

---

### 複数 premise

例えば、

```text
patterns:
RELATION
GIVEN
```

という rule に対して、

```text
available:
GIVEN
RELATION
```

という順で ProofStep が存在していても、
Phase 5-18 の premise search が、

```text
RELATION → relation_step
GIVEN    → given_step
```

と検索するため、

```text
is_inference_rule_applicable()
→ True
```

となる。

したがって applicability は、
available_steps 自体が
premise pattern 順に並んでいることを要求しない。

---

### premise 不足

```text
patterns:
RELATION
GIVEN
```

に対して、

```text
available:
RELATION
```

しか存在しない場合は、

```text
find_matching_premises()
→ None
```

となる。

したがって、

```text
is_inference_rule_applicable()
→ False
```

となることを確認した。

---

### premise を必要としない rule

```text
premise_patterns = ()
```

の InferenceRule については、

```text
find_matching_premises()
→ ()
```

となる。

`()` は `None` ではないため、

```text
is_inference_rule_applicable()
→ True
```

となる。

available_steps に無関係な ProofStep が存在していても、
premise 不要 rule は applicable と判定される。

---

### ProofStep の再利用禁止

Phase 5-18 の仕様をそのまま継承する。

例えば、

```text
patterns:
GIVEN
GIVEN
```

に対して、
GIVEN ProofStep が1つしかない場合、

```text
False
```

となる。

同じ ProofStep を
2つの premise pattern に再利用しないためである。

一方、
異なる GIVEN ProofStep が2つ存在すれば、

```text
True
```

となる。

---

### RelationType による applicability

以下のような pattern:

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

について、

```text
EQUALITY relation
ZERO relation
```

が available_steps に存在する場合、
ZERO relation が検索されるため
rule が applicable になることを確認した。

一方、
EQUALITY relation しか存在しなければ、
not applicable となる。

---

### 入力形式

`available_steps` には引き続き、

```text
single ProofStep
tuple of ProofStep
list of ProofStep
```

を指定できる。

applicability API 側では
独自に正規化せず、
`find_matching_premises()` に処理を委譲した。

---

### 入力検証

以下を確認した。

```text
不正な InferenceRule
不正な available_steps
list 内の不正な ProofStep
```

これらは、
`find_matching_premises()` の既存 validation により
`TypeError` となる。

applicability API に同じ validation logic は追加していない。

---

### 追加テスト

Phase 5-19 では、
以下の applicability テストを追加した。

```text
test_inference_rule_is_applicable
test_inference_rule_is_not_applicable
test_inference_rule_applicable_with_multiple_patterns
test_inference_rule_not_applicable_when_premise_missing
test_empty_inference_rule_is_applicable
test_empty_inference_rule_is_applicable_with_available_steps
test_inference_rule_applicability_searches_available_steps
test_inference_rule_applicability_does_not_reuse_step
test_inference_rule_applicability_uses_distinct_steps
test_inference_rule_applicability_matches_relation_type
test_inference_rule_applicability_rejects_wrong_relation_type
test_is_inference_rule_applicable_accepts_single_step
test_is_inference_rule_applicable_accepts_list
test_is_inference_rule_applicable_rejects_invalid_rule
test_is_inference_rule_applicable_rejects_invalid_steps
test_is_inference_rule_applicable_rejects_invalid_step_in_list
```

---

### テスト

2026-08-24:

```text
289 passed in 20.72s
```

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
premise pattern matching
inference-rule matching
premise search
```

を含め、
すべてのテストが成功した。

Phase 5-19 の applicability API 導入による
regression は確認されなかった。

---

### Phase 5-19 の到達点

現在の inference matching pipeline は、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
```

から、

```text
InferenceRule
+
explicit ProofSteps
↓
matches_inference_rule()
```

さらに、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
```

へ進み、

Phase 5-19 では、

```text
InferenceRule
+
available ProofSteps
↓
is_inference_rule_applicable()
↓
True / False
```

まで到達した。

これにより proof / inference layer は、

```text
この rule が現在使えるか
```

を機械的に問い合わせられるようになった。

ただし現段階では、

```text
applicable な rule を複数 rule から自動検索する
matched premises と rule をまとめて保持する
rule を適用して conclusion を生成する
```

ところまでは進んでいない。

### 状態

Phase 5-19 完了。

次は Phase 5-20 として、

```text
複数の InferenceRule
+
available ProofSteps
↓
applicable InferenceRule の検索
```

を行う最小機構を導入する。


## Phase 5-20：複数の InferenceRule から applicable rule を検索

Phase 5-19 までに、
1つの `InferenceRule` と available ProofSteps について、

```text
必要な premises を検索
↓
rule が applicable か判定
```

できるようになった。

Phase 5-20 では、
複数の inference rule をまとめて調べ、

```text
現在の available ProofSteps で
適用可能な rule の集合
```

を取得する機能を追加した。

---

### find_applicable_inference_rules()

追加:

```python
find_applicable_inference_rules(
  inference_rules,
  available_steps,
)
```

この関数は、
複数の `InferenceRule` を入力順に調べ、

```python
is_inference_rule_applicable(
  inference_rule,
  available_steps,
)
```

が `True` となる rule のみを tuple として返す。

基本的な処理は、

```text
InferenceRule collection
↓
各 rule を入力順に走査
↓
is_inference_rule_applicable()
↓
applicable な rule のみ残す
↓
tuple で返す
```

とした。

applicability 判定のロジックを新しく実装せず、
Phase 5-19 までに作成した既存 API を再利用した。

---

### 単一 applicable rule

例えば、

```text
given rule
relation rule
```

という2つの rule があり、

```text
GIVEN
```

の ProofStep だけが available の場合、

```python
find_applicable_inference_rules(...)
```

は、

```text
(
  given_rule,
)
```

を返す。

これにより、
rule collection の中から
現在利用可能な rule だけを抽出できるようになった。

---

### 複数 applicable rule

複数の rule が同時に applicable な場合も、
すべて返す。

例えば、

```text
first given rule
second given rule
```

がどちらも、

```text
GIVEN
```

を要求する場合、

```text
available:
  GIVEN
```

に対して、

```text
(
  first_given_rule,
  second_given_rule,
)
```

が返る。

Phase 5-20 では、
複数の rule の中から1つを選択する処理は行わない。

---

### rule order の保持

applicable rule の返却順は、
入力された rule collection の順序を維持する。

例えば、

```text
input:
  second_rule
  first_rule
```

の順で渡した場合、
両方 applicable なら結果も、

```text
(
  second_rule,
  first_rule,
)
```

となる。

priority や rule 名による並べ替えは行わない。

---

### applicable rule がない場合

どの rule も applicable でない場合は、

```text
()
```

を返す。

例えば、

```text
RELATION を要求する rule
```

に対して、

```text
GIVEN
```

しか available でない場合、
検索結果は空 tuple になる。

これは正常な検索結果として扱う。

---

### 空 rule collection

```text
inference_rules = ()
```

にも対応した。

検索対象となる rule が存在しないため、

```text
()
```

を返す。

呼び出し側で空 collection を特別処理する必要はない。

---

### premise-free rule

```text
premise_patterns = ()
```

を持つ rule は、
Phase 5-19 までと同様に
premise を必要としないため applicable となる。

そのため available steps が空でも、
premise-free rule は検索結果へ含まれる。

確認例:

```text
rules:
  relation rule
  no premise rule

available:
  none
```

結果:

```text
(
  no_premise_rule,
)
```

---

### 複数 premise pattern

複数 premise pattern を要求する rule についても、
既存の `is_inference_rule_applicable()` を通じて
正しく検索できることを確認した。

例えば、

```text
combined rule:
  RELATION
  GIVEN

given rule:
  GIVEN
```

に対して、

```text
available:
  GIVEN
  RELATION
```

が存在すれば、

```text
(
  combined_rule,
  given_rule,
)
```

が返る。

available steps の保存順と
rule の premise pattern 順が一致している必要はない。

---

### relation type を使った rule search

`RelationType` を条件に持つ rule についても確認した。

例えば、

```text
zero relation rule
```

が、

```text
ProofRule.RELATION
statement_type = Relation
relation_type = RelationType.ZERO
```

を要求し、

```text
equality relation rule
```

が、

```text
RelationType.EQUALITY
```

を要求する場合を考える。

available steps に、

```text
RelationType.ZERO
```

の Relation step だけが存在すると、

```text
zero relation rule
```

だけが検索結果に含まれる。

これにより collection search でも、
既存の PremisePattern 条件が維持されることを確認した。

---

### _normalize_inference_rules()

rule collection の入力を正規化するため、

```python
_normalize_inference_rules()
```

を追加した。

受け付ける入力:

```text
InferenceRule
tuple of InferenceRule
list of InferenceRule
```

単一 rule は、

```text
(rule,)
```

へ正規化する。

tuple / list 内に `InferenceRule` 以外が含まれる場合は
`TypeError` とする。

これにより、

```python
find_applicable_inference_rules(
  rule,
  step,
)
```

という単一入力と、

```python
find_applicable_inference_rules(
  [rule],
  [step],
)
```

という collection 入力を
同じ API で扱えるようになった。

---

### available steps の正規化

available steps については、
既存の、

```python
_normalize_proof_steps()
```

を再利用した。

そのため、

```text
ProofStep
tuple of ProofStep
list of ProofStep
```

を受け取れる。

不正な型や、
collection 内に ProofStep 以外が含まれている場合は
`TypeError` となる。

rule collection 側と available-step 側で
同じ形式の入力 validation を持つようになった。

---

### Phase 5-20 で追加したテスト

主な追加テスト:

```text
test_find_applicable_inference_rules
test_find_applicable_inference_rules_multiple_matches
test_find_applicable_inference_rules_preserves_order
test_find_applicable_inference_rules_returns_empty
test_find_applicable_inference_rules_empty_rules
test_find_applicable_inference_rules_includes_empty_rule
test_find_applicable_inference_rules_multiple_patterns
test_find_applicable_inference_rules_relation_type
test_find_applicable_inference_rules_accepts_single_rule
test_find_applicable_inference_rules_accepts_list
test_find_applicable_inference_rules_rejects_invalid_rules
test_find_applicable_inference_rules_rejects_invalid_rule_in_list
test_find_applicable_inference_rules_rejects_invalid_steps
test_find_applicable_inference_rules_rejects_invalid_step_in_list
```

確認した内容:

```text
単一 applicable rule
複数 applicable rule
入力順保持
該当 rule なし
空 rule collection
premise-free rule
複数 premise pattern
relation type
単一 InferenceRule 入力
list 入力
不正な rule collection
不正な rule entry
不正な available steps
不正な ProofStep entry
```

---

### テスト

2026-08-24

```text
303 passed in 23.01s
```

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
PremisePattern
InferenceRule
premise matching
inference-rule matching
premise search
applicability
```

を含む全テストが成功した。

Phase 5-20 の追加による regression は確認されなかった。

---

### Phase 5-20 の到達点

Phase 5-20 により、
inference rule の検索経路は、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
```

```text
InferenceRule
+
explicit ProofSteps
↓
matches_inference_rule()
```

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
```

```text
InferenceRule
+
available ProofSteps
↓
is_inference_rule_applicable()
```

から、

```text
InferenceRule collection
+
available ProofSteps
↓
find_applicable_inference_rules()
↓
applicable InferenceRules
```

まで拡張された。

これにより、

```text
1つの rule が使えるか
```

を確認するだけでなく、

```text
現在登録されている rule 群の中で
どの rule が使えるか
```

を検索できるようになった。

これは、
将来的に proof engine が多数の数学的規則を保持し、
現在得られている事実から
次に使用可能な推論規則を発見するための基礎となる。

ただし現段階では、

```text
applicable rule
```

だけを返しており、

```text
rule
+
その rule に対応する matched premises
```

をまとめた構造はまだ持たない。

また、

```text
rule の選択
rule の適用
conclusion の自動生成
```

もまだ行わない。

### 状態

Phase 5-20 完了。

次は、

```text
applicable InferenceRule
+
matched ProofSteps
```

を一体として保持する
structured match の導入が自然な候補となる。

例えば、

```text
InferenceMatch
```

のような型を導入し、

```text
どの rule が使えるか
```

だけでなく、

```text
その rule がどの premises によって使えるのか
```

まで1つの検索結果として保持できるようにすることを検討する。


## Phase 5-21：InferenceMatch と structured premise match

Phase 5-20 では、

```text
InferenceRule collection
+
available ProofSteps
↓
find_applicable_inference_rules()
↓
applicable InferenceRules
```

を実装し、
現在利用可能な inference rule を
複数の rule から検索できるようにした。

Phase 5-21 では、
applicable rule だけでなく、

```text
その rule に対応して
実際に選択された premises
```

も同時に保持するため、
structured match を導入した。

---

### InferenceMatch

追加:

```python
@dataclass(frozen=True)
class InferenceMatch:
  inference_rule: InferenceRule
  premises: tuple[ProofStep, ...]
```

`InferenceMatch` は、

```text
利用可能な InferenceRule
+
その rule に対応する matched ProofSteps
```

を1つの object として保持する。

例えば、

```text
premise patterns:
  RELATION
  GIVEN
```

に対して、

```text
available:
  given_step
  relation_step
```

が存在する場合、

```text
InferenceMatch
├── inference_rule = combined_rule
└── premises
    ├── relation_step
    └── given_step
```

となる。

---

### find_inference_match()

追加:

```python
find_inference_match(
  inference_rule,
  available_steps,
)
```

1つの `InferenceRule` について、
available ProofSteps から
matched premises を検索し、

```text
InferenceMatch
```

または、

```text
None
```

を返す。

内部では既存の、

```python
find_matching_premises()
```

をそのまま利用した。

処理は、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
matched premises
↓
InferenceMatch
```

となる。

必要な premises が見つからない場合は、

```text
None
```

を返す。

matching algorithm 自体は追加せず、
既存の premise search を再利用した。

---

### premise-pattern 順の保持

`InferenceMatch.premises` が、
available-step 順ではなく
premise-pattern 順に保持されることを確認した。

例えば、

```text
available:
  GIVEN
  RELATION
```

でも、

```text
patterns:
  RELATION
  GIVEN
```

なら、

```text
premises:
  relation_step
  given_step
```

となる。

これは `find_matching_premises()` の
既存仕様をそのまま利用している。

---

### premise-free rule

premise を必要としない、

```text
premise_patterns = ()
```

の rule についても structured match を確認した。

この場合、

```python
find_inference_match(
  rule,
  (),
)
```

は、

```python
InferenceMatch(
  inference_rule=rule,
  premises=(),
)
```

を返す。

したがって、

```text
None
```

は、

```text
rule が match しなかった
```

ことを意味し、

```text
InferenceMatch(..., ())
```

は、

```text
premise-free rule が正常に match した
```

ことを意味する。

この2つを明確に区別した。

---

### relation type 条件

`RelationType` 条件を持つ premise pattern についても
`InferenceMatch` に正しい step が格納されることを確認した。

例えば、

```text
RelationType.EQUALITY
RelationType.ZERO
```

の2種類の relation step がある場合に、

```text
RelationType.ZERO
```

を要求する rule では、
zero relation step が選択される。

これにより、

```text
rule が applicable
```

という情報だけでなく、

```text
実際にどの relation が選択されたか
```

を structured result として保持できるようになった。

---

### find_inference_matches()

複数 rule をまとめて structured match へ変換するため、

```python
find_inference_matches(
  inference_rules,
  available_steps,
)
```

を追加した。

処理は、

```text
InferenceRule collection
↓
各 rule について find_inference_match()
↓
None を除外
↓
tuple of InferenceMatch
```

となる。

例えば、

```text
rule A
rule B
```

がそれぞれ異なる ProofStep に match する場合、

```text
(
  InferenceMatch(rule A, premises A),
  InferenceMatch(rule B, premises B),
)
```

を返す。

---

### 複数 match

複数の inference rule が同時に applicable な場合、
それぞれの `InferenceMatch` を返すことを確認した。

rule A が GIVEN を要求し、
rule B が RELATION を要求する場合に、

```text
available:
  GIVEN
  RELATION
```

があれば、

```text
InferenceMatch(rule A, GIVEN)
InferenceMatch(rule B, RELATION)
```

の両方を取得できる。

---

### rule input order

`find_inference_matches()` が
rule collection の入力順を維持することを確認した。

例えば、

```text
input:
  second_rule
  first_rule
```

の両方が match する場合、
結果も、

```text
second_rule
first_rule
```

の順となる。

Phase 5-21 では
rule ranking や priority は導入していない。

---

### match がない場合

どの rule にも matched premises が存在しない場合、

```text
()
```

を返す。

空の rule collection に対しても、

```text
()
```

を返す。

どちらも正常な検索結果として扱う。

---

### single input / list input

既存 API と同様に、

```text
InferenceRule
tuple/list of InferenceRule
```

を利用できることを確認した。

available steps についても、

```text
ProofStep
tuple/list of ProofStep
```

を利用できる。

既存の normalization helper を再利用することで、
Phase 5-20 までの API との一貫性を維持した。

---

### input validation

以下の異常入力について
`TypeError` になることを確認した。

```text
invalid InferenceRule input
invalid rule entry in collection
invalid available-steps input
invalid ProofStep entry in collection
```

`find_inference_match()` は
`find_matching_premises()` の validation を利用する。

`find_inference_matches()` は、

```text
_normalize_inference_rules()
_normalize_proof_steps()
```

を利用する。

---

### Phase 5-21 で追加した主なテスト

追加した主なテスト:

```text
test_inference_match
test_find_inference_match
test_find_inference_match_returns_none
test_find_inference_match_preserves_pattern_order
test_find_inference_match_empty_rule
test_find_inference_match_empty_rule_with_steps
test_find_inference_match_relation_type
test_find_inference_match_accepts_single_step
test_find_inference_match_accepts_list
test_find_inference_match_rejects_invalid_rule
test_find_inference_match_rejects_invalid_steps
test_find_inference_match_rejects_invalid_step_in_list

test_find_inference_matches
test_find_inference_matches_multiple
test_find_inference_matches_preserves_rule_order
test_find_inference_matches_returns_empty
test_find_inference_matches_empty_rules
test_find_inference_matches_includes_empty_rule
test_find_inference_matches_multiple_patterns
test_find_inference_matches_relation_type
test_find_inference_matches_accepts_single_rule
test_find_inference_matches_accepts_list
test_find_inference_matches_rejects_invalid_rules
test_find_inference_matches_rejects_invalid_rule_in_list
test_find_inference_matches_rejects_invalid_steps
test_find_inference_matches_rejects_invalid_step_in_list
```

確認した内容:

```text
InferenceMatch の構造
single rule match
non-applicable rule
premise-pattern order
premise-free rule
relation type
single ProofStep input
list input
multiple rule matches
rule input order
empty result
empty rule collection
multiple premise patterns
input normalization
invalid inputs
```

---

### テスト

2026-08-24

```text
329 passed in 21.71s
```

Phase 5-20 終了時は、

```text
303 passed
```

だったため、
Phase 5-21 で26テストが追加された。

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
PremisePattern
InferenceRule
explicit premise matching
premise search
applicability
applicable-rule search
```

を含む全テストが成功した。

Phase 5-21 の変更による regression は確認されなかった。

---

### Phase 5-21 の到達点

Phase 5-21 により、
inference-rule search は、

```text
どの rule が applicable か
```

を返す段階から、

```text
どの rule が applicable で、
その rule がどの premises を使うか
```

を structured data として返す段階へ進んだ。

現在の pipeline は、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
```

```text
InferenceRule
+
explicit ProofSteps
↓
matches_inference_rule()
```

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
```

```text
InferenceRule
+
available ProofSteps
↓
is_inference_rule_applicable()
```

```text
InferenceRule collection
+
available ProofSteps
↓
find_applicable_inference_rules()
```

```text
InferenceRule
+
available ProofSteps
↓
find_inference_match()
↓
InferenceMatch / None
```

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
tuple of InferenceMatch
```

となった。

これにより、
automatic proof inference に必要となる、

```text
rule discovery
+
premise selection
```

までを1つの structured result として
扱える基盤ができた。

---

### 現在の制限

`InferenceMatch` は、
rule と premises を保持するだけであり、

```text
conclusion
```

はまだ持たない。

また、

```text
InferenceMatch
↓
ProofStep
```

への自動変換はまだ行わない。

現在の `PremisePattern` も、

```text
proof_rule
statement_type
relation_type
```

の構造的条件だけを扱い、

```text
mα = 0
```

などの expression 内部の pattern は認識しない。

したがって現在はまだ、

```text
variable binding
substitution
conclusion construction
automatic rule application
```

は行えない。

また premise search は引き続き greedy であり、
alternative assignment の backtracking は行わない。

---

### 状態

Phase 5-21 完了。

次の自然な段階は、

```text
InferenceMatch
↓
inference application
↓
ProofStep
```

への接続を設計することである。

ただし actual rule application に進む前に、

```text
InferenceRule が conclusion を
どのように記述するか
```

を決める必要がある。

今後、

```text
conclusion template
conclusion builder
expression pattern
pattern variable
binding
substitution
```

などをどの順で導入するかを整理する。


## Phase 5-22：InferenceMatch の適用と conclusion builder

Phase 5-21 までに、

```text
InferenceRule
+
available ProofSteps
↓
find_inference_match()
↓
InferenceMatch
```

および、

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
```

という structured match search を実装した。

これにより、

```text
どの rule が使えるか
```

だけでなく、

```text
どの concrete ProofStep を premises として
その rule が使えるか
```

まで保持できるようになった。

Phase 5-22 では、
この `InferenceMatch` を実際に適用し、

```text
InferenceMatch
↓
new ProofStep
```

へ変換する最小 rule-application 機構を追加した。

---

### InferenceRule.conclusion_builder

`InferenceRule` に、

```text
conclusion_builder
```

を追加した。

現在の構造は、

```python
@dataclass(frozen=True)
class InferenceRule:
  name: str
  description: str | None = None
  premise_patterns: tuple[PremisePattern, ...] = ()
  conclusion_builder: Any = None
```

となる。

`conclusion_builder` は optional とし、
default は、

```text
None
```

とした。

これにより既存の InferenceRule は変更せず利用できる。

---

### matching と application の分離

Phase 5-22 では、

```text
rule matching
```

と、

```text
rule application
```

を明確に分離した。

以下の既存 API は、
conclusion builder を持たない rule に対しても
従来通り利用できる。

```text
matches_inference_rule()
find_matching_premises()
is_inference_rule_applicable()
find_applicable_inference_rules()
find_inference_match()
find_inference_matches()
```

つまり、

```text
この rule が適用可能か
```

を調べる段階では、
conclusion construction は要求しない。

実際に rule を適用するときだけ
conclusion builder を要求する。

---

### apply_inference_match()

追加:

```python
apply_inference_match(
  inference_match,
)
```

この関数は、

```text
InferenceMatch
↓
matched InferenceRule
↓
conclusion_builder
↓
matched premises
↓
new conclusion
↓
ProofStep
```

という処理を行う。

生成される ProofStep は、

```text
conclusion
= builder の返り値

premises
= InferenceMatch.premises

rule
= ProofRule.INFERENCE

inference_rule
= InferenceMatch.inference_rule
```

を持つ。

これにより、
生成された step から、

```text
どの premises を使用したか
どの InferenceRule を使用したか
```

の両方を追跡できる。

---

### conclusion_builder への premises の受け渡し

conclusion builder には、

```text
InferenceMatch.premises
```

を tuple のまま渡す。

例えば、

```python
def builder(premises):
  return (
    premises[0].conclusion,
    premises[1].conclusion,
  )
```

のように、
具体的な matched ProofStep を利用して
conclusion を構築できる。

builder に渡される premises の順序は、
InferenceMatch が保持する順序である。

Phase 5-21 までに、
InferenceMatch.premises は
`premise_patterns` の順序を保持することを確認している。

したがって、

```text
premise pattern order
↓
InferenceMatch.premises
↓
conclusion_builder
↓
derived ProofStep.premises
```

で順序が維持される。

---

### multiple premises

複数 premise を必要とする rule についても、
structured match からそのまま application できることを確認した。

例えば、

```text
PremisePattern(
  proof_rule=ProofRule.RELATION,
)

PremisePattern(
  proof_rule=ProofRule.GIVEN,
)
```

を要求する rule に対し、
available steps が、

```text
given_step
relation_step
```

の順であっても、

```text
InferenceMatch.premises
=
(
  relation_step,
  given_step,
)
```

となる。

builder はこの順序で premises を受け取り、
derived ProofStep も同じ premises を保持する。

---

### premise-free rule

premise pattern を持たない rule も
apply できることを確認した。

この場合、

```text
InferenceMatch.premises
=
()
```

となり、
builder には空 tuple が渡される。

builder が conclusion を返せば、

```text
ProofRule.INFERENCE
```

を持つ新しい ProofStep を生成する。

これにより、
premise-free rule についても、

```text
match
↓
application
```

を同じ API で扱える。

---

### builder result の型を制限しない

Phase 5-22 では、
conclusion builder の返り値を
特定の Statement 型には限定していない。

例えば、

```text
文字列
Relation
tuple
その他の structured statement
```

を conclusion として返すことができる。

これは現在の `ProofStep.conclusion` が
汎用値を保持できる設計と整合する。

Phase 5-22 の目的は、

```text
symbolic conclusion language を確定すること
```

ではなく、

```text
InferenceMatch
↓
conclusion construction
↓
ProofStep
```

という application boundary を確立することである。

---

### invalid application の validation

`apply_inference_match()` に対し、
InferenceMatch 以外を渡した場合は、

```text
TypeError
```

とする。

また、
InferenceRule に、

```text
conclusion_builder = None
```

しかない場合に application を行うと、

```text
ValueError
```

とする。

これは、

```text
matching は可能
application specification はない
```

という状態である。

さらに、

```text
conclusion_builder
```

が `None` ではないが callable でない場合は、

```text
TypeError
```

とする。

これにより、

```text
invalid match
missing builder
invalid builder
```

を区別した。

---

### matching-only rule の後方互換性

conclusion builder を持たない InferenceRule について、

```text
find_inference_match()
find_inference_matches()
```

が引き続き正常に動作することを確認した。

したがって Phase 5-22 の追加によって、

```text
InferenceRule = rule specification
```

という既存用途は変更されない。

builder は、

```text
rule application capability
```

を必要に応じて追加する optional field として扱われる。

---

### searched InferenceMatch の直接適用

Phase 5-22 では、

```text
find_inference_match()
↓
InferenceMatch
↓
apply_inference_match()
↓
ProofStep
```

という一連の経路も確認した。

例えば、

```text
given fact
```

を premise として検索し、

```text
derived from given fact
```

という conclusion を builder で構築できることを確認した。

これにより、

```text
available ProofSteps
↓
premise search
↓
structured match
↓
rule application
↓
derived ProofStep
```

という最小 inference pipeline が実際に接続された。

---

### Phase 5-22 で追加した主なテスト

追加した主なテスト:

```text
test_inference_rule_conclusion_builder_defaults_to_none
test_inference_rule_conclusion_builder
test_inference_rule_conclusion_builder_is_backward_compatible
test_apply_inference_match
test_apply_inference_match_builder_receives_premises
test_apply_inference_match_builder_result_is_conclusion
test_apply_inference_match_multiple_premises
test_apply_inference_match_preserves_pattern_order
test_apply_inference_match_premise_free_rule
test_apply_inference_match_rejects_invalid_match
test_apply_inference_match_requires_conclusion_builder
test_apply_inference_match_rejects_non_callable_builder
test_find_inference_match_does_not_require_builder
test_find_inference_matches_do_not_require_builders
test_apply_found_inference_match
```

確認内容:

```text
conclusion_builder の default が None
builder の保持
既存 InferenceRule との後方互換性
InferenceMatch から ProofStep を生成
builder への premises の受け渡し
builder の返り値を conclusion として使用
multiple premise application
premise-pattern order の維持
premise-free rule application
invalid match の拒否
builder 未定義時の application 拒否
non-callable builder の拒否
builder なしでの matching
builder なし rule collection の matching
search で得た InferenceMatch の直接 application
```

---

### テスト

2026-08-24:

```text
344 passed in 20.98s
```

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
PremisePattern
InferenceRule matching
premise search
applicability
applicable-rule search
structured InferenceMatch search
```

を含め、
すべてのテストが成功した。

Phase 5-22 の rule-application 機構導入による
regression は確認されなかった。

---

### Phase 5-22 の到達点

Phase 5-21 では、

```text
available ProofSteps
+
InferenceRule
↓
InferenceMatch
```

まで進んでいた。

Phase 5-22 では、

```text
InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

を追加した。

したがって現在の inference pipeline は、

```text
PremisePattern
↓
ProofStep matching
↓
InferenceRule matching
↓
premise search
↓
rule applicability
↓
applicable-rule search
↓
InferenceMatch
↓
rule application
↓
derived ProofStep
```

まで到達した。

これは、

```text
既存の proof facts
+
推論規則
↓
新しい proof fact
```

を生成する最初の完全な最小経路である。

ただし現在の conclusion construction は、

```text
explicit Python callable
```

に委譲している。

まだ、

```text
Expression pattern
pattern variable
variable binding
substitution
conclusion template
```

による一般的な symbolic inference は行っていない。

また、
生成された ProofStep を自動的に、

```text
available ProofSteps
```

へ追加し、

```text
再検索
↓
再適用
↓
さらに新しい ProofStep
```

と反復する機構もまだない。

### 状態

Phase 5-22 完了。

次の段階では、

```text
Expression-level pattern matching
```

または、

```text
InferenceRule collection
+
available ProofSteps
↓
matches
↓
derived ProofSteps
```

という collection-level application のどちらを先に導入するかを検討する。

一般的な数学的 inference rule を表現するためには、
最終的に、

```text
expression pattern
↓
variable binding
↓
substitution
↓
conclusion
```

という機構が必要になる。


## Phase 5-23：複数 InferenceMatch の一括 application

Phase 5-22 では、

```text
InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

を実装し、
1つの structured match を実際の推論結果へ変換できるようにした。

Phase 5-23 では、
複数の `InferenceMatch` をまとめて適用し、

```text
InferenceMatch collection
↓
derived ProofStep collection
```

へ変換する collection-level application を追加した。

---

### apply_inference_matches()

追加:

```python
apply_inference_matches(
  inference_matches,
)
```

この関数は、
複数の `InferenceMatch` を受け取り、
各 match を `apply_inference_match()` へ渡す。

基本構造:

```text
InferenceMatch collection
↓
normalize
↓
apply_inference_match() for each match
↓
derived ProofStep tuple
```

実装上は、

```python
return tuple(
  apply_inference_match(
    inference_match
  )
  for inference_match
  in normalized_matches
)
```

という薄い wrapper とした。

これにより、
Phase 5-22 で実装した single application logic を
collection-level API で重複させていない。

---

### single application logic の再利用

各 InferenceMatch の application は、
既存の、

```text
apply_inference_match()
```

へ完全に委譲する。

したがって、

```text
conclusion_builder の取得
builder が存在するかの確認
builder が callable かの確認
conclusion の生成
ProofRule.INFERENCE の設定
premises の保存
InferenceRule の保存
```

は Phase 5-22 の実装をそのまま利用する。

Phase 5-23 で追加した責務は、

```text
複数 match の入力処理
+
複数 application の orchestration
```

だけである。

---

### _normalize_inference_matches()

追加:

```python
_normalize_inference_matches(
  inference_matches,
)
```

入力として、

```text
single InferenceMatch
tuple of InferenceMatch
list of InferenceMatch
```

を受け付ける。

内部ではすべて、

```text
tuple
```

へ正規化する。

例えば、

```python
apply_inference_matches(
  match,
)
```

も、

```python
apply_inference_matches(
  (
    match,
  ),
)
```

と同じ意味になる。

---

### 空 collection

空 tuple に対して、

```python
apply_inference_matches(
  (),
)
```

は、

```text
()
```

を返す。

これにより、

```python
matches = find_inference_matches(
  rules,
  available_steps,
)

derived_steps = apply_inference_matches(
  matches,
)
```

という経路で、
match が0件の場合にも特別な分岐を必要としない。

---

### application order の維持

複数の InferenceMatch を適用するとき、
入力順を維持して derived ProofStep を返すことを確認した。

例えば、

```text
(
  second_match,
  first_match,
)
```

に対して、

```text
(
  second derived step,
  first derived step,
)
```

となる。

Phase 5-21 の `find_inference_matches()` も
InferenceRule の入力順を維持するため、

```text
InferenceRule input order
↓
InferenceMatch order
↓
derived ProofStep order
```

が一貫して維持される。

---

### premises の保存

collection-level application 後も、
各 derived ProofStep が
対応する InferenceMatch の premises を
そのまま保持することを確認した。

例えば、

```text
match_a.premises = (given_step,)
```

なら、

```text
derived_step_a.premises = (given_step,)
```

となる。

複数 match をまとめて apply しても、
異なる match の premises が混在しない。

---

### InferenceRule の保存

各 derived ProofStep の、

```text
inference_rule
```

には、
対応する InferenceMatch の `inference_rule` が保存される。

例えば、

```text
match_a.inference_rule = rule_a
match_b.inference_rule = rule_b
```

なら、

```text
derived_a.inference_rule = rule_a
derived_b.inference_rule = rule_b
```

となる。

これにより collection-level application 後も、
各 derived fact がどの rule によって導かれたかを追跡できる。

---

### invalid input

`apply_inference_matches()` に、

```text
InferenceMatch
tuple/list of InferenceMatch
```

以外を渡した場合は `TypeError` とする。

確認例:

```text
"invalid"
```

また、

```text
[
  valid_match,
  "invalid",
]
```

のように、
collection 内に InferenceMatch 以外が含まれる場合も
`TypeError` とする。

collection-level input validation は
`_normalize_inference_matches()` が担当する。

一方、

```text
missing conclusion_builder
non-callable conclusion_builder
```

など individual application の validation は、
引き続き `apply_inference_match()` が担当する。

---

### find_inference_matches() との接続

Phase 5-23 では、

```text
find_inference_matches()
↓
apply_inference_matches()
```

という実際の collection-level pipeline を確認した。

例えば、

```text
first rule
requires GIVEN

second rule
requires RELATION
```

という2つの rule と、

```text
given_step
relation_step
```

がある場合、

```python
matches = find_inference_matches(
  (
    first_rule,
    second_rule,
  ),
  (
    given_step,
    relation_step,
  ),
)
```

から、

```text
(
  InferenceMatch(
    inference_rule=first_rule,
    premises=(given_step,),
  ),
  InferenceMatch(
    inference_rule=second_rule,
    premises=(relation_step,),
  ),
)
```

を得る。

これを、

```python
derived_steps = apply_inference_matches(
  matches
)
```

とすることで、

```text
(
  first derived step,
  second derived step,
)
```

を生成できることを確認した。

各 derived step は、
それぞれ対応する premise を保持する。

---

### matching と application の分離

Phase 5-23 でも、

```text
find_inference_matches()
```

と、

```text
apply_inference_matches()
```

は統合しなかった。

現在の利用方法は、

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)

derived_steps = apply_inference_matches(
  matches,
)
```

である。

これにより、

```text
matching
↓
結果確認・選択
↓
application
```

という処理を可能にしている。

Phase 5-23 の `apply_inference_matches()` は、
rule collection や available steps を直接受け取らず、
すでに確定した InferenceMatch だけを適用する。

---

### Phase 5-23 で追加した主なテスト

追加したテスト:

```text
test_apply_inference_matches
test_apply_inference_matches_preserves_order
test_apply_inference_matches_preserves_premises
test_apply_inference_matches_preserves_rules
test_apply_inference_matches_empty
test_apply_inference_matches_accepts_single_match
test_apply_inference_matches_accepts_list
test_apply_inference_matches_rejects_invalid_input
test_apply_inference_matches_rejects_invalid_match_in_list
test_apply_found_inference_matches
```

確認内容:

```text
複数 InferenceMatch の application
複数 derived ProofStep の生成
input order の維持
premises の維持
InferenceRule の維持
空 collection
single InferenceMatch input
list input
invalid top-level input
invalid collection entry
find_inference_matches() から apply_inference_matches() への接続
```

---

### テスト

2026-08-24:

```text
354 passed in 21.65s
```

Phase 5-22 完了時は、

```text
344 passed
```

だったため、
Phase 5-23 では10テストを追加した。

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
PremisePattern
InferenceRule matching
premise search
applicability
applicable-rule search
InferenceMatch search
single InferenceMatch application
```

を含め、
すべてのテストが成功した。

Phase 5-23 の collection-level application 導入による
regression は確認されなかった。

---

### Phase 5-23 の到達点

Phase 5-22 までの inference pipeline は、

```text
InferenceRule
+
available ProofSteps
↓
find_inference_match()
↓
InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

だった。

Phase 5-23 ではこれを collection level へ拡張し、

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

まで到達した。

これにより、

```text
複数の applicable rule
↓
複数の structured match
↓
複数の derived fact
```

という処理が可能になった。

現在も、

```text
matching
```

と、

```text
application
```

は別 API である。

そのため caller は、
InferenceMatch collection を確認・選択した上で
application できる。

---

### 現在まだ行わないこと

Phase 5-23 では、
以下はまだ実装しない。

```text
match search と application の一体化
derived step の available facts への自動追加
derived conclusion の重複判定
同じ rule の再適用制御
inference round
fixed-point iteration
automatic rule priority
automatic rule selection
alternative premise assignment
backtracking
Expression-level matching
pattern variable
variable binding
substitution
structured conclusion template
```

特に、

```text
derived ProofSteps
↓
available ProofSteps に追加
↓
再度 find_inference_matches()
```

という反復処理はまだ行わない。

この段階へ進む前に、
duplicate conclusion や停止条件などの設計が必要になる。

---

### 状態

Phase 5-23 完了。

現在の collection-level pipeline:

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

次の自然な候補は、

```text
InferenceRule collection
+
available ProofSteps
↓
find
↓
apply
↓
derived ProofSteps
```

をまとめる high-level API の導入である。

例えば、

```text
derive_inference_steps()
```

のような関数を用意し、

```text
find_inference_matches()
↓
apply_inference_matches()
```

を内部で組み合わせる。

その後、

```text
derived ProofSteps
↓
available ProofSteps へ追加
↓
次の inference round
```

へ進むことで、
iterative inference の基盤へ接続できる。

一方、
一般的な数学的 inference rule を表現するためには、
別方向として、

```text
Expression pattern
↓
variable binding
↓
substitution
↓
conclusion
```

という symbolic inference 機構も必要になる。


# Phase 5-24：match search と application をまとめる high-level inference API

Phase 5-23 までに、

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

という collection-level inference pipeline が完成した。

Phase 5-24 では、
この2段階を一般的な caller から簡潔に利用するため、

```python
derive_inference_steps()
```

を追加した。

---

## derive_inference_steps() の追加

`proof.py` に、

```python
def derive_inference_steps(
  inference_rules,
  available_steps,
):
  matches = find_inference_matches(
    inference_rules,
    available_steps,
  )

  return apply_inference_matches(
    matches
  )
```

を追加した。

この関数は、

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

を1回の関数呼び出しで実行する。

---

## thin composition として実装

Phase 5-24 では、
`derive_inference_steps()` の内部に
新しい matching logic や application logic を追加しなかった。

内部処理は、

```text
find_inference_matches()
↓
apply_inference_matches()
```

だけである。

したがって、

```text
premise search
InferenceMatch construction
rule order preservation
input normalization
conclusion_builder validation
conclusion construction
premise preservation
InferenceRule preservation
```

は既存 implementation をそのまま利用する。

これにより、
Phase 5-23 までに確認済みの lower-level behavior と
high-level API の behavior が一致する。

---

## 単一 rule の high-level derivation

例えば、

```python
rule = InferenceRule(
  name="given inference",
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.GIVEN,
    ),
  ),
  conclusion_builder=lambda premises: (
    "derived"
  ),
)

step = ProofStep(
  conclusion="given",
  premises=(),
  rule=ProofRule.GIVEN,
)
```

に対して、

```python
result = derive_inference_steps(
  (
    rule,
  ),
  (
    step,
  ),
)
```

とすると、

```text
derived
```

を conclusion とする
1つの derived `ProofStep` が得られる。

さらに、

```text
premises = (step,)
rule = ProofRule.INFERENCE
inference_rule = rule
```

が維持されることを確認した。

---

## 複数 rule の high-level derivation

異なる premise pattern を持つ複数 rule についても、

```python
result = derive_inference_steps(
  (
    first_rule,
    second_rule,
  ),
  (
    given_step,
    relation_step,
  ),
)
```

から、

```text
(
  first derived,
  second derived,
)
```

という複数の ProofStep を生成できることを確認した。

これにより Phase 5-23 で、

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)

derived_steps = apply_inference_matches(
  matches,
)
```

と2段階で記述していた処理を、

```python
derived_steps = derive_inference_steps(
  inference_rules,
  available_steps,
)
```

と記述できるようになった。

---

## rule order の保持

`derive_inference_steps()` が、
入力 rule の順序を derived step まで維持することを確認した。

例えば、

```text
(
  second_rule,
  first_rule,
)
```

を入力した場合、

```text
(
  "second",
  "first",
)
```

の順で conclusion が返る。

これは、

```text
find_inference_matches()
```

が rule order を維持し、

```text
apply_inference_matches()
```

が match order を維持するためである。

`derive_inference_steps()` 自体では
sorting や ranking を行わない。

---

## applicable rule がない場合

premise pattern に一致する step がない場合、

```python
derive_inference_steps(
  inference_rules,
  available_steps,
)
```

は、

```text
()
```

を返すことを確認した。

つまり、

```text
no applicable rule
```

はエラーではなく、
新しく derivable な step が存在しない状態として表現する。

---

## 空 rule collection

```python
derive_inference_steps(
  (),
  available_steps,
)
```

についても、

```text
()
```

を返すことを確認した。

空 rule collection は正常な入力として扱う。

---

## single input と list input

既存 normalization を経由するため、

```text
single InferenceRule
single ProofStep
```

を直接渡せることを確認した。

例えば、

```python
derive_inference_steps(
  rule,
  step,
)
```

でも derived step が得られる。

また、

```python
derive_inference_steps(
  [
    rule,
  ],
  [
    step,
  ],
)
```

という list input も利用できる。

Phase 5-24 専用の normalization は追加していない。

---

## invalid rule input

不正な rule input について、

```python
derive_inference_steps(
  "invalid",
  (
    step,
  ),
)
```

が `TypeError` となることを確認した。

validation は、
内部で呼び出される `find_inference_matches()` の
既存 rule normalization によって行われる。

---

## invalid ProofStep input

同様に、

```python
derive_inference_steps(
  (
    rule,
  ),
  "invalid",
)
```

が `TypeError` となることを確認した。

ProofStep input validation についても、
high-level API に新しい validation logic は追加していない。

---

## matched rule の conclusion_builder 要件

matching 可能な rule でも、

```text
conclusion_builder = None
```

の場合は application できない。

例えば、

```python
rule = InferenceRule(
  name="given rule",
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.GIVEN,
    ),
  ),
)
```

が available step に match した場合、

```python
derive_inference_steps(
  (
    rule,
  ),
  (
    step,
  ),
)
```

は `ValueError` となることを確認した。

これは、

```text
derive_inference_steps()
↓
find_inference_matches()
↓
apply_inference_matches()
↓
apply_inference_match()
```

と進み、
既存の conclusion-builder validation が働くためである。

high-level API では、
この validation を回避・変更しない。

---

## lower-level API との共存

Phase 5-24 では、
high-level API を追加したが、

```text
find_inference_matches()
```

と、

```text
apply_inference_matches()
```

はそのまま残している。

現在は用途に応じて、

```text
直接 derive したい
↓
derive_inference_steps()
```

または、

```text
match を先に確認したい
↓
find_inference_matches()
↓
必要な match を選択
↓
apply_inference_matches()
```

を選べる。

これにより将来、

```text
rule selection
priority
search strategy
proof strategy
user confirmation
```

などを追加しても、
matching と application の間に処理を挿入できる。

---

## Phase 5-24 の inference pipeline

Phase 5-24 により、
現在の high-level inference pipeline は、

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
derived ProofStep collection
```

となった。

内部では、

```text
derive_inference_steps()
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

となっている。

これにより、

```text
available facts
+
inference rules
↓
new derived facts
```

という1 round の inference を
単一 API で実行できるようになった。

---

## Phase 5-24 で追加した主なテスト

追加したテスト:

```text
test_derive_inference_steps
test_derive_inference_steps_multiple_rules
test_derive_inference_steps_preserves_rule_order
test_derive_inference_steps_returns_empty
test_derive_inference_steps_empty_rules
test_derive_inference_steps_accepts_single_rule_and_step
test_derive_inference_steps_accepts_lists
test_derive_inference_steps_rejects_invalid_rules
test_derive_inference_steps_rejects_invalid_steps
test_derive_inference_steps_requires_builder_for_matched_rule
```

確認内容:

```text
single rule derivation
multiple rule derivation
derived ProofStep generation
premise preservation
InferenceRule preservation
rule order preservation
no applicable rules
empty rule collection
single rule / step normalization
list normalization
invalid rule input
invalid ProofStep input
missing conclusion_builder validation
```

---

## テスト

2026-08-24:

```text
364 passed in 52.84s
```

Phase 5-23 完了時は、

```text
354 passed
```

だったため、
Phase 5-24 では10テストを追加した。

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
PremisePattern
InferenceRule matching
premise search
applicability
applicable-rule search
InferenceMatch search
single InferenceMatch application
collection-level InferenceMatch application
```

を含め、
すべてのテストが成功した。

Phase 5-24 の high-level inference API 導入による
regression は確認されなかった。

---

## Phase 5-24 の到達点

Phase 5-24 により、

```text
PremisePattern
↓
ProofStep matching
↓
InferenceRule applicability
↓
InferenceMatch
↓
InferenceMatch collection
↓
ProofStep application
↓
ProofStep collection application
↓
high-level derivation
```

という inference 基盤がつながった。

特に、

```python
derive_inference_steps(
  inference_rules,
  available_steps,
)
```

だけで、

```text
現在の facts から
現在の rules で
何を新しく導けるか
```

を ProofStep collection として取得できる。

これは今後の automatic inference loop に対する
最初の high-level entry point となる。

---

## 現在の制限

`derive_inference_steps()` は
1 round の inference だけを行う。

生成した、

```text
derived ProofSteps
```

を自動的に、

```text
available ProofSteps
```

へ追加することはまだない。

したがって、

```text
available
↓
derive
↓
derived
↓
available + derived
↓
derive again
```

という iterative inference は未実装である。

また、
derived conclusions の重複判定もまだ行わない。

例えば、

```text
rule A → conclusion X
rule B → conclusion X
```

の場合に、
両方の ProofStep を保持するか、
1つだけ保持するかという policy はまだ定義していない。

premise-free rule についても、
iterative inference で無制限に再適用されないための
仕組みはまだない。

---

## 次の候補

次の自然な段階は、

```text
available ProofSteps
+
derived ProofSteps
↓
expanded available ProofSteps
```

を構築する処理である。

ただし単純に追加する前に、

```text
duplicate conclusion detection
```

を整理する必要がある。

例えば、

```text
既存 conclusion と同じ conclusion を
新しい ProofStep が生成した場合どうするか
```

を決める必要がある。

候補としては、

```text
same conclusion → 追加しない
```

だけでなく、

```text
same conclusion
+
different premises / different rule
→ alternative proof として保持
```

という設計も考えられる。

したがって次の段階では、

```text
ProofStep collection
+
new ProofSteps
↓
duplicate / novelty 判定
↓
merge
```

を独立した責務として検討する。

これができれば、

```text
round 1:
derive_inference_steps()

↓ merge

round 2:
derive_inference_steps()

↓ merge

...

↓ no new steps
```

という fixed-point inference へ進める。

一方、
一般的な数学的 inference rule の実用化には、
別方向として引き続き、

```text
Expression pattern
↓
variable binding
↓
substitution
↓
structured conclusion
```

が必要である。

---

## 状態

Phase 5-24 完了。

現在の high-level inference pipeline:

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
derived ProofStep collection
```

内部構造:

```text
derive_inference_steps()
↓
find_inference_matches()
↓
apply_inference_matches()
```

これにより、
collection-level match search と application が
高レベル API として接続された。

次の主要候補は、

```text
derived ProofSteps
+
available ProofSteps
↓
duplicate-aware merge
↓
expanded ProofSteps
```

である。

その後、

```text
derive
↓
merge
↓
derive
↓
merge
↓
fixed point
```

という iterative automatic inference へ進める。

同時に、
より一般的な数学的推論のためには、

```text
Expression pattern
↓
variable binding
↓
substitution
↓
conclusion
```

という symbolic inference 機構を
別軸で発展させる必要がある。


## Phase 5-25：derived ProofStep を available ProofSteps に追加する1 round の inference

Phase 5-24 では、

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
derived ProofStep collection
```

という high-level inference derivation を導入した。

これにより、
matching と application を caller が個別に接続しなくても、

```text
現在 available な facts
+
inference rules
↓
新しい facts
```

を1回の API 呼び出しで生成できるようになった。

ただし Phase 5-24 の返り値は、

```text
derived ProofSteps のみ
```

であり、
生成された facts を、

```text
次の inference で利用可能な ProofSteps
```

へ追加する処理は caller 側に残されていた。

Phase 5-25 では、

```python
run_inference_round(
  inference_rules,
  available_steps,
)
```

を追加し、

```text
現在の available ProofSteps
↓
1回 inference
↓
derived ProofSteps
↓
available ProofSteps の後ろへ追加
```

という明示的な1 inference round を実装した。

---

### run_inference_round()

追加:

```python
run_inference_round(
  inference_rules,
  available_steps,
)
```

実装:

```python
def run_inference_round(
  inference_rules,
  available_steps,
):
  normalized_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  derived_steps = derive_inference_steps(
    inference_rules,
    normalized_steps,
  )

  return (
    normalized_steps
    + derived_steps
  )
```

処理は、

```text
available_steps を normalize
↓
derive_inference_steps()
↓
derived_steps
↓
normalized_steps + derived_steps
```

という薄い構造とした。

新しい matching algorithm や
application algorithm は追加していない。

---

### 既存 high-level derivation の再利用

Phase 5-25 では、
Phase 5-24 で追加した、

```python
derive_inference_steps()
```

をそのまま利用する。

したがって、

```text
run_inference_round()
↓
derive_inference_steps()
↓
find_inference_matches()
↓
apply_inference_matches()
```

という delegation structure になる。

これにより、

```text
premise matching
rule matching
premise search
InferenceMatch construction
application
conclusion building
```

を `run_inference_round()` に重複実装しない。

---

### derive_inference_steps() との違い

2つの high-level API は、
返す collection の意味が異なる。

```python
derive_inference_steps(
  inference_rules,
  available_steps,
)
```

は、

```text
derived ProofSteps
```

だけを返す。

一方、

```python
run_inference_round(
  inference_rules,
  available_steps,
)
```

は、

```text
existing available ProofSteps
+
derived ProofSteps
```

を返す。

例えば、

```text
available:
(
  given_step,
)
```

から、

```text
derived:
(
  derived_step,
)
```

が得られる場合、

```text
derive_inference_steps()
```

は、

```text
(
  derived_step,
)
```

を返し、

```text
run_inference_round()
```

は、

```text
(
  given_step,
  derived_step,
)
```

を返す。

---

### 1 round の境界

Phase 5-25 では、
1 round 中に生成された ProofStep を、
同じ round の inference には使用しない。

処理順序は、

```text
round 開始時点の available ProofSteps
↓
derive_inference_steps()
↓
すべての derived ProofSteps を生成
↓
round 終了時に追加
```

となる。

例えば、

```text
rule 1:
given → intermediate

rule 2:
intermediate → final
```

で、
round 開始時点に、

```text
given
```

だけが存在する場合、
1 round では、

```text
intermediate
```

までを生成する。

同じ `run_inference_round()` の中で、

```text
intermediate
```

を rule 2 の premise として再利用し、

```text
final
```

まで生成することはない。

これは intentional な設計とした。

---

### available step の順序維持

既存 available steps は、
入力順序を維持したまま結果の先頭へ置く。

例えば、

```text
(
  first_step,
  second_step,
)
```

を入力した場合、
result の先頭も、

```text
(
  first_step,
  second_step,
  ...
)
```

となることを確認した。

`run_inference_round()` 自体は、

```text
sorting
priority
deduplication
```

を行わない。

---

### derived step の順序維持

derived steps は、
`derive_inference_steps()` の返す順序をそのまま維持する。

Phase 5-24 までに、

```text
InferenceRule input order
↓
InferenceMatch order
↓
derived ProofStep order
```

が維持されることを確認済みである。

Phase 5-25 では、
この derived collection を既存 collection の後ろへ
そのまま連結する。

したがって、

```text
existing order
+
derived order
```

が round result の順序になる。

---

### multiple derived steps

複数の rule が同時に applicable な場合、
複数の derived ProofStep がまとめて追加される。

例えば、

```text
first_rule:
GIVEN → first derived

second_rule:
RELATION → second derived
```

と、

```text
given_step
relation_step
```

が available な場合、

```python
result = run_inference_round(
  (
    first_rule,
    second_rule,
  ),
  (
    given_step,
    relation_step,
  ),
)
```

から、

```text
(
  given_step,
  relation_step,
  first_derived_step,
  second_derived_step,
)
```

を得られることを確認した。

---

### no applicable rules

applicable な rule が存在しない場合、

```text
derived_steps = ()
```

となるため、

```text
existing steps
```

だけを返す。

例えば、

```text
rule requires RELATION
```

に対して、

```text
available = GIVEN
```

だけの場合、

```text
result == available
```

となる。

これは正常な inference round として扱う。

---

### empty rule collection

```text
inference_rules = ()
```

の場合も、
derived step は存在しない。

そのため、

```text
run_inference_round(
  (),
  available_steps,
)
```

は、
normalized available steps をそのまま返す。

---

### empty available steps と premise-free rule

available steps が空でも、

```text
premise_patterns = ()
```

の inference rule は applicable である。

そのため、

```text
available = ()
```

でも、
premise-free rule に有効な `conclusion_builder` があれば、

```text
(
  derived_step,
)
```

を生成できることを確認した。

derived step は、

```text
premises = ()
rule = ProofRule.INFERENCE
```

を持つ。

---

### input normalization

`run_inference_round()` でも、
既存 API と同じ input forms を維持した。

確認:

```text
single InferenceRule
single ProofStep

tuple input

list input
```

list input の場合も、
返り値は tuple に正規化される。

---

### invalid input

invalid rule input について、

```text
"invalid"
```

を渡した場合は `TypeError` となることを確認した。

invalid available-step input についても、

```text
"invalid"
```

を渡した場合は `TypeError` となる。

available-step validation は、

```text
_normalize_proof_steps()
```

が担当する。

rule validation は、
`derive_inference_steps()` 以下の既存 API に委譲される。

---

### missing conclusion builder

applicable な rule に、

```text
conclusion_builder = None
```

しか設定されていない場合、
`run_inference_round()` でも `ValueError` となる。

これは、

```text
run_inference_round()
↓
derive_inference_steps()
↓
apply_inference_matches()
↓
apply_inference_match()
```

という既存 validation path を利用しているためである。

round API 独自の validation は追加していない。

---

### duplicate detection はまだ行わない

Phase 5-25 では、
generated ProofStep を available steps へ追加できるようになったが、

```text
同じ conclusion がすでに存在するか
```

は確認していない。

例えば、

```text
A → B
```

という rule に対して、
1回目の round で、

```text
A, B
```

となった後、
再び同じ round を実行すると、

```text
A, B, B
```

となる可能性がある。

これは現段階では intentional である。

duplicate の意味について、

```text
same ProofStep
same conclusion
same rule + premises
same mathematical fact
```

のどれを採用するかを、
iterative inference の前に設計する必要がある。

---

### Phase 5-25 で追加した主なテスト

追加:

```text
test_run_inference_round
test_run_inference_round_appends_multiple_derived_steps
test_run_inference_round_preserves_available_step_order
test_run_inference_round_preserves_derived_step_order
test_run_inference_round_no_applicable_rules
test_run_inference_round_empty_rules
test_run_inference_round_empty_steps
test_run_inference_round_accepts_single_rule_and_step
test_run_inference_round_accepts_lists
test_run_inference_round_rejects_invalid_rules
test_run_inference_round_rejects_invalid_steps
test_run_inference_round_requires_builder_for_matched_rule
```

確認内容:

```text
basic one-round inference
existing + derived の結合
multiple derived steps
available-step order preservation
derived-step order preservation
no applicable rule
empty rule collection
empty available-step collection
premise-free rule
single input
list input
invalid rule input
invalid ProofStep input
missing conclusion builder
```

---

### テスト

2026-08-24:

```text
376 passed in 44.79s
```

Phase 5-24 完了時は、

```text
364 passed
```

だったため、
Phase 5-25 では12テストを追加した。

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
PremisePattern
InferenceRule matching
premise search
applicability
applicable-rule search
InferenceMatch search
single InferenceMatch application
collection-level InferenceMatch application
high-level derive_inference_steps()
```

を含め、
すべてのテストが成功した。

Phase 5-25 の one-round inference 導入による
regression は確認されなかった。

---

### Phase 5-25 の到達点

Phase 5-24 までの pipeline は、

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
derived ProofStep collection
```

だった。

Phase 5-25 では、

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
available ProofSteps
+
derived ProofSteps
```

まで進んだ。

したがって現在の inference pipeline は、

```text
available facts
↓
premise matching
↓
rule matching
↓
InferenceMatch
↓
application
↓
derived facts
↓
available facts へ追加
```

という1 round の complete path を持つ。

これは iterative proof engine に向けた重要な境界である。

ただし、

```text
run_inference_round()
```

は1回しか inference を行わない。

新しく追加された derived fact を使った次の inference は、
別の round が必要である。

---

### 現在まだ行わないこと

Phase 5-25 では、
以下はまだ実装しない。

```text
automatic repeated inference rounds
duplicate ProofStep detection
duplicate conclusion detection
new-fact-only merge
fixed-point termination
rule application history
premise-free rule の repeated application 抑制
cyclic inference detection
inference round metadata
alternative proof management
automatic rule priority
automatic rule selection
alternative premise assignments
backtracking
Expression-level pattern matching
pattern variables
variable bindings
substitution
structured conclusion templates
```

特に、
現在の `run_inference_round()` を単純に繰り返すだけでは、

```text
同じ derived conclusion
```

を何度も追加する可能性がある。

そのため fixed-point iteration より先に、

```text
existing ProofSteps
+
derived ProofSteps
↓
duplicate-aware merge
↓
genuinely new ProofSteps
```

を定義する必要がある。

---

### 状態

Phase 5-25 完了。

現在の high-level inference path:

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
derive_inference_steps()
↓
find_inference_matches()
↓
apply_inference_matches()
↓
derived ProofSteps
↓
available ProofSteps + derived ProofSteps
```

次の自然な段階は、

```text
derived ProofSteps
+
available ProofSteps
↓
duplicate detection
↓
new ProofSteps だけを追加
```

する merge mechanism の導入である。

これにより、

```text
round
↓
new facts
↓
round
↓
new facts
↓
...
↓
no new facts
```

という fixed-point iterative inference へ安全に進める。


## Phase 5-26：derived ProofStep の duplicate-aware merge

Phase 5-25 では、

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
available ProofSteps
+
derived ProofSteps
```

という1 round の inference を実装した。

ただし Phase 5-25 の `run_inference_round()` は、

```python
return (
  normalized_steps
  + derived_steps
)
```

という単純な tuple concatenation を行っていた。

そのため、
同じ rule を次の round でも適用すると、

```text
same conclusion
```

を何度も追加する可能性があった。

例えば、

```text
A → B
```

に対して、

```text
round 1:
A
B

round 2:
A
B
B
```

となり得た。

Phase 5-26 では、
fixed-point iterative inference へ進む前に、
derived ProofSteps を duplicate-safe に available collection へ
統合する仕組みを追加した。

---

### merge_proof_steps() の追加

`proof.py` に、

```python
def merge_proof_steps(
  available_steps,
  derived_steps,
):
```

を追加した。

実装:

```python
def merge_proof_steps(
  available_steps,
  derived_steps,
):
  normalized_available_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  normalized_derived_steps = (
    _normalize_proof_steps(
      derived_steps,
      "derived_steps",
    )
  )

  merged_steps = list(
    normalized_available_steps
  )

  known_conclusions = [
    step.conclusion
    for step in merged_steps
  ]

  for step in normalized_derived_steps:
    if any(
      step.conclusion
      == known_conclusion
      for known_conclusion
      in known_conclusions
    ):
      continue

    merged_steps.append(
      step
    )

    known_conclusions.append(
      step.conclusion
    )

  return tuple(
    merged_steps
  )
```

---

### conclusion equality を duplicate criterion とした

Phase 5-26 では、
duplicate 判定を、

```text
ProofStep 全体の equality
```

ではなく、

```text
ProofStep.conclusion equality
```

で行う。

実装上は、

```python
step.conclusion == known_conclusion
```

を使用する。

したがって、
derived ProofStep が、

```text
different premises
different rule
different inference_rule
```

を持っていても、
conclusion がすでに available collection に存在する場合は
追加しない。

これは、

```text
available ProofSteps
=
現在 known な conclusions を利用可能にする knowledge state
```

という扱いを優先したためである。

---

### existing conclusion の duplicate suppression

例えば、

```text
available:
(
  "given",
  "already known",
)
```

に対して、
rule が、

```text
"already known"
```

を再び derive しても、
result は、

```text
(
  "given",
  "already known",
)
```

のままとなる。

Phase 5-25 のように、
同じ conclusion を後ろへ追加しない。

---

### duplicate derived conclusions

同じ round で複数 rule が、
同じ conclusion を derive した場合も、
最初の1つだけを追加する。

例えば、

```text
rule 1:
A → B

rule 2:
A → B
```

なら、
candidate derived steps としては、

```text
B from rule 1
B from rule 2
```

が生成され得る。

しかし merge 後は、

```text
A
B from rule 1
```

となる。

derived steps は入力順に走査するため、

```text
first occurrence wins
```

という deterministic な挙動となる。

---

### order preservation

existing available steps の順序を変更しないことを確認した。

例えば、

```text
available:
(
  second,
  first,
)
```

なら、
merged result も、

```text
(
  second,
  first,
  ...
)
```

から始まる。

また、
新しく追加される derived steps についても、
duplicate を除いた上で入力順を維持する。

---

### empty collections

次の case を確認した。

```text
empty available
+
non-empty derived
```

では、
derived steps がそのまま result となる。

```text
non-empty available
+
empty derived
```

では、
available steps がそのまま result となる。

empty collection は error としない。

---

### input normalization

`merge_proof_steps()` は、
available / derived の両方について、
既存の、

```python
_normalize_proof_steps()
```

を利用する。

したがって、

```text
single ProofStep
tuple of ProofStep
list of ProofStep
```

を受け付ける。

返り値は tuple とする。

---

### invalid input

invalid available-step input と、
invalid derived-step input の両方について、
`TypeError` となることを確認した。

validation は新しい独自処理を作らず、

```text
_normalize_proof_steps()
```

へ委譲した。

---

### run_inference_round() の変更

Phase 5-25 では、

```python
return (
  normalized_steps
  + derived_steps
)
```

だった。

Phase 5-26 では、

```python
return merge_proof_steps(
  normalized_steps,
  derived_steps,
)
```

へ変更した。

現在の implementation:

```python
def run_inference_round(
  inference_rules,
  available_steps,
):
  normalized_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  derived_steps = derive_inference_steps(
    inference_rules,
    normalized_steps,
  )

  return merge_proof_steps(
    normalized_steps,
    derived_steps,
  )
```

これにより、

```text
run_inference_round()
↓
derive_inference_steps()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
duplicate-safe expanded ProofSteps
```

という high-level path になった。

---

### one-round semantics は維持

Phase 5-26 では、
duplicate merge を導入しただけで、
1 round の matching semantics は変更していない。

つまり、

```text
round 開始時の available steps
```

だけを premise search に使用する。

round 中に derive された step は、
同じ round では premise として利用しない。

例えば、

```text
A → B
B → C
```

で、
initial available が、

```text
A
```

だけなら、
1 round では、

```text
A
B
```

までである。

`C` の derivation には、
別 round が必要である。

---

### repeated round の idempotence

Phase 5-26 の重要な確認として、
same derivation に対する repeated round が
knowledge state を増加させないことをテストした。

例えば、

```text
A → B
```

について、
1回目:

```text
A
B
```

2回目:

```text
A
B
```

となる。

test では、

```python
assert second_result == first_result
```

を確認した。

これにより、
単純な same-conclusion duplicate による
無限 growth を防げるようになった。

---

### alternative proof の扱い

Phase 5-26 では、
same conclusion に対する alternative proof を
merged available collection へ複数保持しない。

例えば、

```text
A, B → C
```

と、

```text
D, E → C
```

が存在しても、
merge 後の knowledge state では
最初の `C` ProofStep だけが残る。

ただし、

```text
derive_inference_steps()
```

自体は candidate derived steps を返す API のままであり、
merge 前であれば複数の derivation を確認できる。

したがって Phase 5-26 では、

```text
fact availability
```

と、

```text
alternative proof storage
```

を分離した。

alternative proof の専用管理は、
今後必要になった段階で別途設計する。

---

### Phase 5-26 で追加した主なテスト

追加:

```text
test_merge_proof_steps
test_merge_proof_steps_skips_existing_conclusion
test_merge_proof_steps_skips_duplicate_derived_conclusion
test_merge_proof_steps_preserves_available_order
test_merge_proof_steps_preserves_first_new_step_order
test_merge_proof_steps_empty_available
test_merge_proof_steps_empty_derived
test_merge_proof_steps_accepts_single_steps
test_merge_proof_steps_accepts_lists
test_merge_proof_steps_rejects_invalid_available_steps
test_merge_proof_steps_rejects_invalid_derived_steps
test_run_inference_round_does_not_duplicate_existing_conclusion
test_run_inference_round_does_not_duplicate_same_derived_conclusion
test_run_inference_round_is_idempotent_for_same_derivation
```

確認内容:

```text
basic merge
new ProofStep insertion
existing conclusion duplicate suppression
derived conclusion duplicate suppression
available-step order preservation
first-new-step order preservation
empty available collection
empty derived collection
single ProofStep input
list input
invalid available input
invalid derived input
duplicate-safe run_inference_round()
same conclusion from multiple inference rules
repeated-round idempotence
```

---

### inference-rule pattern tests

2026-08-24:

```text
166 passed in 3.27s
```

Phase 5-26 で追加した merge / duplicate tests を含め、
`tests/test_inference_rule_pattern.py` の全テストが成功した。

---

### 全テスト

2026-08-24:

```text
390 passed
```

Phase 5-25 完了時は、

```text
376 passed
```

だったため、
Phase 5-26 では14テストを追加した。

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
PremisePattern
InferenceRule matching
premise search
applicability
applicable-rule search
InferenceMatch search
single InferenceMatch application
collection-level InferenceMatch application
derive_inference_steps()
run_inference_round()
```

を含め、
すべてのテストが成功した。

Phase 5-26 の duplicate-aware merge 導入による
regression は確認されなかった。

---

### Phase 5-26 の到達点

Phase 5-25 までの pipeline は、

```text
available ProofSteps
↓
derive
↓
append
```

だった。

Phase 5-26 では、

```text
available ProofSteps
↓
derive candidate ProofSteps
↓
merge_proof_steps()
↓
duplicate conclusion removal
↓
expanded available ProofSteps
```

まで進んだ。

したがって現在の inference pipeline は、

```text
available facts
↓
premise matching
↓
rule matching
↓
InferenceMatch
↓
application
↓
candidate derived facts
↓
conclusion equality
↓
duplicate-aware merge
↓
expanded knowledge state
```

となった。

これにより、
同じ derived conclusion を何度も追加する問題を
解消できた。

また、

```text
same derivation
↓
same knowledge state
```

という repeated-round idempotence を
単純なケースで確認できた。

これは fixed-point inference の
termination semantics を導入するための基礎となる。

---

### 現在まだ行わないこと

Phase 5-26 では、
以下はまだ実装しない。

```text
automatic repeated inference rounds
genuinely new ProofSteps の独立取得
new-step count
fixed-point loop
explicit fixed-point result
round number
round metadata
inference history
rule application history
alternative proof repository
same conclusion の複数 proof preservation
mathematical equivalence based duplicate detection
conclusion canonicalization
cyclic inference detection
automatic rule priority
automatic rule selection
alternative premise assignments
backtracking
Expression-level pattern matching
pattern variables
variable bindings
substitution
structured conclusion templates
```

特に、
現在の `merge_proof_steps()` は、

```text
merged result
```

のみを返す。

例えば、

```text
available:
A
B

derived:
B
C
```

に対して、

```text
A
B
C
```

は返せるが、

```text
newly added:
C
```

を直接返す API はまだない。

fixed-point inference では、

```text
newly added == ()
```

を termination condition として利用できるため、
次の段階では、

```text
genuinely new ProofSteps
```

を明示的に取得する仕組みが有用である。

---

### 状態

Phase 5-26 完了。

現在の high-level inference path:

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
derive_inference_steps()
↓
find_inference_matches()
↓
apply_inference_matches()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
duplicate-safe expanded ProofSteps
```

次の自然な段階は、

```text
available ProofSteps
+
candidate derived ProofSteps
↓
duplicate filtering
↓
genuinely new ProofSteps
```

を取得する mechanism の導入である。

これができれば、

```text
round
↓
new facts?
├── yes → next round
└── no  → fixed point
```

という iterative inference の termination condition を
明示できる。

その後、

```text
derive
↓
new-step detection
↓
merge
↓
repeat
↓
fixed point
```

という automatic fixed-point inference へ進む。


## Phase 5-27：1 round で本当に新しく追加された ProofStep を取得する

Phase 5-26 では、

```text
available ProofSteps
+
candidate derived ProofSteps
↓
merge_proof_steps()
↓
duplicate-safe expanded ProofSteps
```

を実装した。

これにより、
already-known conclusion や
同じ round 内で重複して derive された conclusion を
knowledge state へ複数追加しないようにできた。

ただし、

```text
今回の round で実際に何個の新しい fact が増えたか
```

を直接取得する API はまだなかった。

Phase 5-27 では、
fixed-point iterative inference へ進むための
termination condition を構成する目的で、

```python
derive_new_inference_steps()
```

を追加した。

---

### derive_new_inference_steps() の追加

`proof.py` に、

```python
def derive_new_inference_steps(
  inference_rules,
  available_steps,
):
```

を追加した。

基本実装:

```python
def derive_new_inference_steps(
  inference_rules,
  available_steps,
):
  normalized_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  derived_steps = derive_inference_steps(
    inference_rules,
    normalized_steps,
  )

  merged_steps = merge_proof_steps(
    normalized_steps,
    derived_steps,
  )

  return merged_steps[
    len(normalized_steps):
  ]
```

---

### existing duplicate semantics を再利用

Phase 5-27 では、
new-step detection のための独自 duplicate 判定は実装しなかった。

Phase 5-26 の、

```python
merge_proof_steps()
```

を利用する。

これにより、

```text
same conclusion
→ duplicate
```

という現在の knowledge-state semantics を
1箇所に集約した。

Phase 5-27 側で、

```text
known_conclusions
```

を再構築して独自 filtering を行わないため、
duplicate criterion が複数箇所でずれることを防げる。

---

### merged suffix から new steps を取得

`merge_proof_steps()` は、
available steps を result の先頭へそのまま保持する。

例えば、

```text
available:
A
B

candidate:
B
C
D
```

なら、

```text
merged:
A
B
C
D
```

となる。

したがって、

```python
merged_steps[
  len(normalized_steps):
]
```

によって、

```text
C
D
```

だけを取得できる。

この suffix が、

```text
genuinely new ProofSteps
```

である。

---

### candidate derivation との区別

既存の、

```python
derive_inference_steps()
```

は変更していない。

これは引き続き、

```text
currently applicable rules
↓
candidate derived ProofSteps
```

を返す。

Phase 5-27 では、
新しく、

```text
derive_inference_steps()
=
candidate

derive_new_inference_steps()
=
new
```

という区別を導入した。

例えば、

```text
available:
A
B

rules:
A → B
A → C
```

なら、

```text
derive_inference_steps():
B
C
```

である一方、

```text
derive_new_inference_steps():
C
```

となる。

---

### already-known conclusion の除外

already-known conclusion を derive する rule が
applicable であっても、
new steps には含めないことを確認した。

例えば、

```text
available:
given
already known
```

に対し、
rule が、

```text
given
→ already known
```

を derive しても、

```text
new:
()
```

となる。

---

### duplicate derived conclusion の除外

複数の inference rule が
同じ unknown conclusion を導く場合について確認した。

例えば、

```text
rule 1:
given → same derived

rule 2:
given → same derived
```

なら、
candidate としては2つの ProofStep が生成され得る。

しかし、

```text
derive_new_inference_steps()
```

は最初の1つだけを返す。

また、
保持される step の `inference_rule` が
first rule であることも確認した。

---

### existing と new が混在する場合

candidate derived steps の中に、

```text
already known
```

と、

```text
new conclusion
```

が混在する場合、
new conclusion だけが返ることを確認した。

例えば、

```text
candidate:
already known
new conclusion
```

なら、

```text
new:
new conclusion
```

となる。

---

### new-step order preservation

複数の new conclusions が存在する場合、
rule input order に基づく derived-step order が
preserve されることを確認した。

例えば、

```text
rules:
second rule
first rule
```

が、

```text
second derived
first derived
```

を生成する場合、

```text
new:
second derived
first derived
```

の順になる。

---

### no applicable rule

applicable rule が存在しない場合、

```text
new:
()
```

となることを確認した。

これは、

```text
candidate == ()
```

なので、
そのまま、

```text
new == ()
```

となる。

---

### empty rules

empty inference-rule collection に対して、

```text
new:
()
```

となることを確認した。

empty rule collection は error としない。

---

### empty available steps

available steps が empty でも、
premise-free rule が存在する場合は
new step を生成できることを確認した。

例えば、

```text
available:
()

premise-free rule:
→ derived
```

なら、

```text
new:
derived
```

となる。

---

### same derivation の再実行

Phase 5-27 で特に重要な確認として、

```text
すでに一度 derive して knowledge state に追加済み
```

の conclusion について、
次回は、

```text
new:
()
```

となることを確認した。

例えば、

```text
given → derived
```

について1 round 実行後、

```text
given
derived
```

が available になっている場合、

```python
derive_new_inference_steps(
  rules,
  first_round,
)
```

は、

```text
()
```

を返す。

これにより、

```text
new steps が空
```

という fixed-point termination condition を
直接利用できるようになった。

---

### input normalization

次の入力を確認した。

```text
single InferenceRule
single ProofStep
```

および、

```text
list of InferenceRule
list of ProofStep
```

どちらでも正常に動作する。

返り値は tuple とする。

---

### invalid input

invalid inference-rules input について、
`TypeError` になることを確認した。

invalid available-steps input についても、
`TypeError` になることを確認した。

validation は既存の、

```text
_normalize_inference_rules()
_normalize_proof_steps()
```

経路を再利用する。

---

### missing conclusion builder

premises が match した rule に
`conclusion_builder` が存在しない場合、

```text
ValueError
```

となることを確認した。

これは、

```text
derive_new_inference_steps()
↓
derive_inference_steps()
↓
apply_inference_match()
```

という既存 application path の validation を
そのまま引き継いでいる。

---

### run_inference_round() の整理

Phase 5-27 では、
`run_inference_round()` を、

```text
available state
+
genuinely new steps
```

として構成する形に整理した。

Conceptually:

```python
normalized_steps = (
  _normalize_proof_steps(
    available_steps,
    "available_steps",
  )
)

new_steps = derive_new_inference_steps(
  inference_rules,
  normalized_steps,
)

return (
  normalized_steps
  + new_steps
)
```

これにより、

```text
derive_new_inference_steps()
=
round delta

run_inference_round()
=
next state
```

という役割分担が明確になった。

---

### Phase 5-27 で追加したテスト

追加:

```text
test_derive_new_inference_steps
test_derive_new_inference_steps_excludes_existing_conclusion
test_derive_new_inference_steps_excludes_duplicate_derived_conclusion
test_derive_new_inference_steps_returns_only_new_conclusions
test_derive_new_inference_steps_preserves_new_step_order
test_derive_new_inference_steps_returns_empty_when_no_rule_matches
test_derive_new_inference_steps_empty_rules
test_derive_new_inference_steps_empty_available_steps
test_derive_new_inference_steps_returns_empty_after_same_derivation
test_derive_new_inference_steps_accepts_single_rule_and_step
test_derive_new_inference_steps_accepts_lists
test_derive_new_inference_steps_rejects_invalid_rules
test_derive_new_inference_steps_rejects_invalid_steps
test_derive_new_inference_steps_requires_builder_for_matched_rule
```

追加テスト数:

```text
14
```

---

### inference-rule pattern tests

2026-08-24:

```text
180 passed in 3.40s
```

Phase 5-27 の new-step detection tests を含め、
`tests/test_inference_rule_pattern.py` の全テストが成功した。

---

### 全テスト

2026-08-24:

```text
404 passed in 43.45s
```

Phase 5-26 完了時:

```text
390 passed
```

Phase 5-27 で14 tests を追加し、
既存 test を含む全404 tests が成功した。

既存の、

```text
algebra
EHP
expression
formatter
proof
repository
PremisePattern
InferenceRule
premise search
applicability
InferenceMatch
application
candidate derivation
duplicate-aware merge
one-round inference
```

に regression は確認されなかった。

---

### state / delta の分離

Phase 5-27 により、
inference engine の high-level state transition を、

```text
state_n
+
delta_n
=
state_{n+1}
```

として整理できるようになった。

ここで、

```text
state_n
=
available ProofSteps
```

であり、

```text
delta_n
=
derive_new_inference_steps(...)
```

である。

したがって、

```text
delta_n == ()
```

なら、
その round では knowledge state が増えていない。

---

### fixed-point termination condition

Phase 5-27 の最大の到達点は、

```python
new_steps = derive_new_inference_steps(
  inference_rules,
  available_steps,
)

if not new_steps:
  ...
```

によって、
fixed-point inference の termination condition を
直接表現できるようになったことである。

ただし Phase 5-27 では、
自動 iteration 自体はまだ行わない。

---

### Phase 5-27 の到達点

Phase 5-26:

```text
available
+
candidate derived
↓
merge
↓
expanded state
```

Phase 5-27:

```text
available
+
candidate derived
↓
merge
↓
genuinely new steps
```

まで進んだ。

現在の high-level inference pipeline は、

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
derive_new_inference_steps()
↓
genuinely new ProofSteps
↓
run_inference_round()
↓
next knowledge state
```

となった。

---

### 現在まだ行わないこと

Phase 5-27 では、
以下はまだ実装しない。

```text
automatic repeated rounds
while-loop based inference
fixed-point result object
round count
maximum-round limit
round history
per-round delta history
rule application history
cycle detection
alternative-proof repository
multiple proofs of the same conclusion in the knowledge state
mathematical equivalence based duplicate detection
conclusion canonicalization
backtracking premise search
all premise-assignment enumeration
pattern-variable binding
expression substitution
structured conclusion templates
automatic relation selection
```

---

### 状態

Phase 5-27 完了。

テスト:

```text
180 inference-rule pattern tests passed
404 total tests passed
```

現在、

```text
new_steps == ()
```

を直接判定できるため、
次の自然な段階は、

```text
Phase 5-28:
new ProofStep がなくなるまで
inference round を繰り返す
fixed-point iterative inference
```

である。

基本形は、

```text
state
↓
derive new steps
↓
new steps?
├── yes
│   ↓
│   state += new steps
│   ↓
│   repeat
│
└── no
    ↓
    fixed point
```

となる。


# Phase 5-28：fixed-point iterative inference

Phase 5-27 までに、

```text
candidate derived ProofSteps
↓
duplicate-aware merge
↓
genuinely new ProofSteps
```

という1 round の delta を取得できるようになった。

さらに、

```text
new_steps == ()
```

を、

```text
現在の inference rules と matching semantics の下で
これ以上 knowledge state が増えない
```

という fixed-point termination condition として
利用できる状態になっていた。

Phase 5-28 では、
この termination condition を automatic iteration へ接続し、

```text
new ProofStep がなくなるまで
inference round を自動的に繰り返す
```

fixed-point inference を実装した。

---

## run_inference_until_stable()

追加:

```python
run_inference_until_stable(
  inference_rules,
  available_steps,
)
```

基本実装:

```python
def run_inference_until_stable(
  inference_rules,
  available_steps,
):
  normalized_rules = (
    _normalize_inference_rules(
      inference_rules
    )
  )

  current_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  while True:
    new_steps = (
      derive_new_inference_steps(
        normalized_rules,
        current_steps,
      )
    )

    if not new_steps:
      return current_steps

    current_steps = (
      current_steps
      + new_steps
    )
```

---

## fixed-point inference の流れ

初期 knowledge state を、

```text
state_0
```

とする。

各 round で、

```text
delta_n
=
derive_new_inference_steps(
  inference_rules,
  state_n,
)
```

を計算する。

`delta_n` が非空なら、

```text
state_{n+1}
=
state_n + delta_n
```

として次の round へ進む。

`delta_n` が空なら、

```text
state_n
```

を返して終了する。

したがって、

```text
state
↓
derive new steps
↓
new steps?
├── yes
│   ↓
│   state += new steps
│   ↓
│   repeat
│
└── no
    ↓
    fixed point
```

という処理が実装された。

---

## multi-round inference

Phase 5-28 により、
ある round で導出された ProofStep を
次の round の premise として利用できるようになった。

例えば、

```text
initial
↓
rule 1
↓
intermediate
↓
rule 2
↓
final
```

という inference chain について、

```text
round 0:
initial
```

から開始し、

```text
round 1:
intermediate を追加
```

その後、

```text
round 2:
intermediate を premise として
final を追加
```

さらに、

```text
round 3:
new_steps == ()
```

となって停止する。

これにより、
one-round inference だけでなく、
新しく得られた fact が次の推論を駆動する
chained inference が可能になった。

---

## Proof dependency の保持

複数 round にまたがる inference でも、
derived ProofStep の `premises` は保持される。

例えば、

```text
A
↓
B
↓
C
```

なら、

```text
B.premises = (A,)
C.premises = (B,)
```

となる。

fixed-point iteration は ProofStep を再構築せず、
各 round の genuinely new ProofStep を
knowledge state の末尾へ追加するだけなので、
既存 dependency semantics をそのまま維持できる。

---

## duplicate conclusion と termination

Phase 5-28 では、
同じ conclusion を何度も導く rule が存在しても、
Phase 5-26 / Phase 5-27 の duplicate semantics によって
再追加されない。

例えば、

```text
A → B
```

という rule は、
`A` が残っている限り毎 round applicable であり得る。

しかし、

```text
B
```

がすでに knowledge state に存在すれば、

```text
derive_new_inference_steps()
```

は、

```text
()
```

を返す。

したがって、

```text
rule が applicable
```

であることと、

```text
new knowledge が増える
```

ことを区別できる。

fixed-point termination は後者だけを見る。

---

## premise-free rule

premise-free rule についても
fixed-point inference を確認した。

例えば、

```text
→ A
```

という rule と empty initial state について、

最初の round では、

```text
A
```

が追加される。

次の round では同じ `A` が candidate となるが、
既知 conclusion なので new step にはならず、

```text
new_steps == ()
```

となって終了する。

したがって premise-free rule も
現在の duplicate semantics の範囲では
同一 conclusion を無限に追加しない。

---

## ordering

fixed-point iteration でも、
既存の ordering semantics を維持する。

最終 state は、

```text
initial steps
↓
round 1 new steps
↓
round 2 new steps
↓
...
```

という順序になる。

各 round の new-step order は
既存の、

```text
InferenceRule input order
↓
InferenceMatch order
↓
candidate derived-step order
↓
first genuinely new occurrence
```

をそのまま利用する。

---

## input normalization

`run_inference_until_stable()` は、

```text
InferenceRule
```

または、

```text
tuple/list of InferenceRule
```

を受け取る。

また available steps は、

```text
ProofStep
```

または、

```text
tuple/list of ProofStep
```

を受け取る。

最初に、

```text
_normalize_inference_rules()
_normalize_proof_steps()
```

を利用して tuple に正規化する。

したがって既存 inference API と
同じ input convention を維持している。

---

## validation

Phase 5-28 では新しい validation semantics は導入していない。

不正な rules や ProofSteps は、
既存 normalize helper によって `TypeError` となる。

また applicable rule に、

```text
conclusion_builder
```

が存在しない場合は、
既存 inference application semantics に従って
`ValueError` となる。

---

## Phase 5-28 で追加した主なテスト

追加:

```text
test_run_inference_until_stable
test_run_inference_until_stable_requires_multiple_rounds
test_run_inference_until_stable_returns_initial_steps_when_no_rule_matches
test_run_inference_until_stable_empty_rules
test_run_inference_until_stable_empty_initial_steps
test_run_inference_until_stable_preserves_initial_order
test_run_inference_until_stable_preserves_derivation_order
test_run_inference_until_stable_does_not_duplicate_conclusions
test_run_inference_until_stable_preserves_dependencies
test_run_inference_until_stable_accepts_single_rule_and_step
test_run_inference_until_stable_accepts_lists
test_run_inference_until_stable_rejects_invalid_rules
test_run_inference_until_stable_rejects_invalid_steps
test_run_inference_until_stable_requires_builder_for_matched_rule
```

追加テスト数:

```text
14
```

確認内容:

```text
basic fixed-point inference
multi-round chained inference
termination when no rule matches
empty inference-rule collection
empty initial knowledge state
premise-free inference
initial-step order preservation
derived-step order preservation
duplicate-conclusion suppression
dependency preservation across rounds
single input normalization
list input normalization
invalid rule rejection
invalid ProofStep rejection
missing conclusion builder
```

---

## inference-rule pattern tests

2026-08-25:

```text
194 passed in 3.69s
```

Phase 5-27 完了時:

```text
180 passed
```

Phase 5-28 では14 tests を追加し、
`tests/test_inference_rule_pattern.py` の
全194 tests が成功した。

---

## fixed-point semantics

Phase 5-28 により、
inference engine の state transition は、

```text
state_n
+
delta_n
=
state_{n+1}
```

という1 round の関係だけでなく、

```text
state_0
↓
state_1
↓
state_2
↓
...
↓
state_k
```

という iteration 全体として扱えるようになった。

停止条件は、

```text
delta_k == ()
```

である。

したがって、

```text
state_{k+1}
=
state_k
```

となり、
knowledge state が安定する。

---

## inference-engine fixed point

Phase 5-28 の fixed point は、

```text
現在登録されている InferenceRule
+
現在の premise matching semantics
+
現在の duplicate semantics
```

の下での fixed point である。

これは、

```text
数学的にすべての帰結を導出した
```

ことを意味しない。

現在の premise search は greedy であり、
alternative premise assignments を列挙しない。

また未登録の inference rule から得られる結論は
当然 derivation の対象にならない。

そのため fixed point は、

```text
inference-engine fixed point
```

として理解する。

---

## Phase 5-28 時点の inference pipeline

現在の high-level inference pipeline は、

```text
InferenceRule collection
+
initial ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
derive_new_inference_steps()
↓
genuinely new ProofSteps
↓
current state に追加
↓
repeat
↓
new_steps == ()
↓
run_inference_until_stable()
↓
stable knowledge state
```

となった。

Phase 5-24 まででは、

```text
candidate derivation
```

Phase 5-25 では、

```text
one-round state expansion
```

Phase 5-26 では、

```text
duplicate-safe merge
```

Phase 5-27 では、

```text
one-round delta extraction
```

Phase 5-28 では、

```text
automatic fixed-point iteration
```

まで到達した。

---

## 現在まだ行わないこと

Phase 5-28 では、
以下はまだ実装しない。

```text
round count
round history
per-round delta history
fixed-point result object
maximum-round safeguard
explicit termination-reason metadata
rule application history
general cycle detection
alternative-proof repository
multiple proofs of the same conclusion
mathematical-equivalence based duplicate detection
conclusion canonicalization
alternative premise assignment enumeration
backtracking premise search
pattern variables
variable binding
expression substitution
structured conclusion templates
automatic relation selection
```

特に現在の、

```python
run_inference_until_stable()
```

は、

```text
最終 stable knowledge state
```

のみを返す。

どの round で何が得られたかという
execution history はまだ保持しない。

---

## Phase 5-28 の到達点

Phase 5-27 では、

```text
Did this round add anything new?
```

を判定できるところまで進んだ。

Phase 5-28 では、

```text
Keep running rounds until the answer becomes no.
```

という処理まで自動化した。

現在、

```text
initial facts
↓
matching
↓
application
↓
candidate derivation
↓
novelty detection
↓
new facts
↓
knowledge-state expansion
↓
newly derived facts become premises
↓
repeat
↓
fixed point
```

という iterative inference の基本 loop が完成している。

この段階で proof / inference layer は、
単発の inference-rule applicability 判定から、

```text
rule system
+
initial knowledge
↓
stable derived knowledge
```

を計算する基盤まで進んだ。

---

## 状態

Phase 5-28 完了。

inference-rule pattern tests:

```text
194 passed in 3.69s
```

次の自然な課題は、
fixed-point execution の結果だけでなく、

```text
round count
per-round new steps
round history
termination information
```

をどのように保持するかを設計することである。

候補として、

```text
InferenceRunResult
FixedPointInferenceResult
```

のような dedicated result object を導入し、

```text
final state
+
round metadata
```

を分離して保持する方向が考えられる。


---

# Phase 5-29：per-round history / result object

Phase 5-28 では、

```python
run_inference_until_stable(
  inference_rules,
  available_steps,
)
```

によって、
new ProofStep がなくなるまで inference round を繰り返し、
fixed point の final knowledge state を取得できるようになった。

ただし返り値は、

```text
tuple of ProofStep
```

だけだった。

そのため、

```text
round 1 で何が追加されたか
round 2 で何が追加されたか
何 round で fixed point に到達したか
```

という execution information を
直接取得することはできなかった。

Phase 5-29 では、
fixed-point inference の per-round history を保持する
structured result object を導入した。

---

## InferenceRunResult の追加

追加:

```python
@dataclass(frozen=True)
class InferenceRunResult:
  steps: tuple[ProofStep, ...]
  round_history: tuple[
    tuple[ProofStep, ...],
    ...
  ]

  @property
  def round_count(self):
    return len(
      self.round_history
    )
```

`steps` は、

```text
fixed point 到達時の final knowledge state
```

を表す。

`round_history` は、

```text
各 productive round で
genuinely new だった ProofSteps
```

を表す。

`round_count` は、

```text
productive round 数
```

を表す。

---

## productive round

Phase 5-29 では、

```text
1個以上の genuinely new ProofStep を
knowledge state に追加した round
```

を productive round とした。

したがって、
fixed-point termination を確認する最後の、

```text
new_steps == ()
```

という iteration は
`round_history` に含めない。

例えば、

```text
initial:
A

round 1:
B

round 2:
C

termination check:
()
```

なら、

```python
round_history = (
  (
    B,
  ),
  (
    C,
  ),
)
```

であり、

```text
round_count == 2
```

となる。

---

## run_inference_until_stable_with_history()

追加:

```python
run_inference_until_stable_with_history(
  inference_rules,
  available_steps,
)
```

基本実装:

```python
def run_inference_until_stable_with_history(
  inference_rules,
  available_steps,
):
  normalized_rules = (
    _normalize_inference_rules(
      inference_rules
    )
  )

  current_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  round_history = []

  while True:
    new_steps = (
      derive_new_inference_steps(
        normalized_rules,
        current_steps,
      )
    )

    if not new_steps:
      return InferenceRunResult(
        steps=current_steps,
        round_history=tuple(
          round_history
        ),
      )

    round_history.append(
      new_steps
    )

    current_steps = (
      current_steps
      + new_steps
    )
```

---

## per-round delta history

history に保存するのは、
各 round の complete state ではなく、

```text
new_steps
```

だけとした。

例えば、

```text
initial:
A

round 1:
B
C

round 2:
D
```

なら、

```python
round_history = (
  (
    B,
    C,
  ),
  (
    D,
  ),
)
```

となる。

final state は、

```text
A
B
C
D
```

である。

append-only knowledge state なので、

```text
initial state
+
round_history
```

から各中間 state を復元できる。

そのため各 round の complete state を
重複して保存しない。

---

## simple API の後方互換性

既存の、

```python
run_inference_until_stable()
```

の返り値を `InferenceRunResult` に変更すると、
Phase 5-28 までの caller に対する breaking change となる。

そのため既存 API は、

```text
final ProofSteps only
```

という contract を維持した。

実装を、

```python
def run_inference_until_stable(
  inference_rules,
  available_steps,
):
  result = (
    run_inference_until_stable_with_history(
      inference_rules,
      available_steps,
    )
  )

  return result.steps
```

へ変更した。

これにより、

```text
run_inference_until_stable()
=
simple final-state API
```

と、

```text
run_inference_until_stable_with_history()
=
detailed execution API
```

を分離した。

---

## fixed-point loop の一元化

Phase 5-28 の fixed-point loop と
Phase 5-29 の history-aware loop を
別々に持たないようにした。

fixed-point execution logic は、

```python
run_inference_until_stable_with_history()
```

へ集約し、

```python
run_inference_until_stable()
```

はその wrapper とした。

したがって、
将来 fixed-point semantics を変更する場合も、

```text
single execution implementation
```

だけを変更すればよい。

---

## round history と dependency

history に格納されるのは、
derived `ProofStep` object 自体である。

例えば、

```text
A
↓
B
↓
C
```

が2 round で導出された場合、

```text
round 1:
B

round 2:
C
```

であり、

```text
B.premises == (A,)
C.premises == (B,)
```

をそのまま保持する。

したがって per-round history を導入しても、
ProofStep dependency graph の semantics は変化しない。

---

## multiple new steps in one round

1 round で複数 rule が
それぞれ genuinely new conclusion を生成した場合も、
同じ history entry にまとめて保存する。

例えば、

```text
round 1:
B
C
```

なら、

```python
round_history[0] == (
  B,
  C,
)
```

となる。

inner tuple の順序は、
既存 derivation order を保持する。

---

## no-new-step case

initial state の時点ですでに stable なら、

```python
InferenceRunResult(
  steps=initial_steps,
  round_history=(),
)
```

となる。

この場合、

```text
round_count == 0
```

である。

empty rule collection も同様である。

---

## empty initial state

empty initial state と empty rule collection では、

```python
InferenceRunResult(
  steps=(),
  round_history=(),
)
```

となる。

premise-free rule によって fact が生成される場合は、
その生成 round が history に保存される。

---

## duplicate candidates は history に含めない

`round_history` に追加する値は、

```python
derive_new_inference_steps()
```

の返り値そのものである。

したがって、

```text
rule は applicable
candidate ProofStep も生成された
しかし conclusion は既知だった
```

という candidate は history には残らない。

Phase 5-29 の history は、

```text
attempted inference history
```

ではなく、

```text
knowledge-state growth history
```

である。

---

## Phase 5-29 で追加した主なテスト

追加:

```text
test_inference_run_result
test_run_inference_until_stable_with_history
test_run_inference_until_stable_with_history_multiple_rounds
test_run_inference_until_stable_with_history_excludes_empty_terminal_round
test_run_inference_until_stable_with_history_no_new_steps
test_run_inference_until_stable_with_history_empty_initial_state
test_run_inference_until_stable_with_history_records_multiple_new_steps_in_round
test_run_inference_until_stable_with_history_preserves_dependencies
test_run_inference_until_stable_with_history_final_steps_match_simple_api
test_run_inference_until_stable_with_history_accepts_single_rule_and_step
test_run_inference_until_stable_with_history_accepts_lists
test_run_inference_until_stable_with_history_rejects_invalid_rules
test_run_inference_until_stable_with_history_rejects_invalid_steps
test_run_inference_until_stable_with_history_requires_builder_for_matched_rule
```

追加テスト数:

```text
14
```

確認内容:

```text
InferenceRunResult basic structure
round_count
single productive round
multiple productive rounds
terminal empty round exclusion
zero productive rounds
empty initial state
multiple new ProofSteps in one round
cross-round dependency preservation
simple API / detailed API consistency
single input normalization
list input normalization
invalid inference-rule rejection
invalid ProofStep rejection
missing conclusion builder
```

---

## inference-rule pattern tests

2026-08-25:

```text
208 passed in 4.30s
```

Phase 5-28 完了時:

```text
194 passed
```

だったため、
Phase 5-29 では14テストを追加した。

`tests/test_inference_rule_pattern.py` の
全208 tests が成功した。

---

## regression

Phase 5-29 では、
既存の、

```text
PremisePattern
InferenceRule
InferenceMatch
matching
premise search
applicability
match search
single-match application
multiple-match application
derive_inference_steps()
merge_proof_steps()
derive_new_inference_steps()
run_inference_round()
run_inference_until_stable()
```

に関する既存テストもすべて成功した。

特に、

```text
run_inference_until_stable()
```

が detailed API へ委譲する実装に変更された後も、
Phase 5-28 の既存 behavior が維持されていることを確認した。

また、

```text
detailed_result.steps
==
run_inference_until_stable(...)
```

もテストした。

Phase 5-29 の result-object 導入による regression は
確認されなかった。

---

## Phase 5-29 時点の fixed-point pipeline

現在の high-level inference pipeline は、

```text
InferenceRule collection
+
initial ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
derive_new_inference_steps()
↓
round delta
↓
round_history に記録
↓
knowledge state に追加
↓
repeat
↓
delta == ()
↓
InferenceRunResult
├── final steps
├── round history
└── round count
```

となった。

simple API ではさらに、

```text
InferenceRunResult
↓
.steps
↓
final stable ProofSteps
```

を返す。

---

## Phase 5-24 から Phase 5-29 までの進展

Phase 5-24:

```text
InferenceRules
+
available ProofSteps
↓
candidate derived ProofSteps
```

Phase 5-25:

```text
one-round knowledge-state expansion
```

Phase 5-26:

```text
duplicate-aware merge
```

Phase 5-27:

```text
genuinely new one-round delta
```

Phase 5-28:

```text
automatic fixed-point iteration
```

Phase 5-29:

```text
structured fixed-point result
+
per-round delta history
+
productive round count
```

まで進んだ。

---

## Phase 5-29 の到達点

Phase 5-28 までは、

```text
What is known at the fixed point?
```

に答えられる状態だった。

Phase 5-29 では、

```text
What became known in each round?
```

にも答えられるようになった。

例えば、

```text
initial:
A

round 1:
B
C

round 2:
D

fixed point
```

を、

```text
final:
A B C D

history:
round 1 = B C
round 2 = D

round_count:
2
```

として直接取得できる。

これにより、
fixed-point inference は単なる計算 API から、

```text
推論がどの段階で進んだか
```

を追跡できる execution model へ進んだ。

---

## 現在まだ行わないこと

Phase 5-29 では、
以下はまだ実装しない。

```text
max_rounds
maximum-round termination
termination reason
termination enum
terminal empty round history
complete state snapshot per round
InferenceMatch history
applicable-rule history
candidate derivation history
duplicate-rejected candidate history
rule application count
cycle detection
nontermination detection
alternative-proof repository
multiple proofs of the same conclusion
mathematical equivalence based duplicate detection
conclusion canonicalization
all premise-assignment enumeration
backtracking
pattern variables
variable binding
expression substitution
structured conclusion templates
automatic relation selection
```

特に、
現在の `InferenceRunResult` は、

```text
knowledge growth
```

だけを表す。

```text
何を試したが追加されなかったか
```

という execution trace はまだ扱わない。

---

## 状態

Phase 5-29 完了。

inference-rule pattern tests:

```text
208 passed in 4.30s
```

Phase 5-29 により、

```text
fixed-point execution
+
final knowledge state
+
per-round new knowledge
+
productive round count
```

を一つの structured result として扱えるようになった。

次の自然な課題は、
fixed-point iteration が必ず停止するとは限らないことへの
safeguard である。

次の候補:

```text
Phase 5-30:
max_rounds
+
termination reason
```

これにより、

```text
fixed point reached
```

と、

```text
round limit reached
```

を明示的に区別できるようにする。


---

# Phase 5-30：max_rounds + termination reason

Phase 5-29 では、

```text
fixed-point inference
+
per-round history
+
productive round count
```

を、

```python
InferenceRunResult
```

として取得できるようにした。

ただし fixed-point loop は、

```text
new ProofStep がなくなるまで
```

無制限に実行されていた。

通常の rule set では duplicate suppression によって
停止することが期待できるが、

```text
毎 round genuinely new conclusion を生成できる rule
```

が存在すれば、
iteration が終了しない可能性がある。

Phase 5-30 では、
この問題に対する execution-level safeguard として、

```text
max_rounds
```

を追加した。

また、

```text
fixed point 到達
```

と、

```text
round limit 到達
```

を区別するため、

```text
termination reason
```

を `InferenceRunResult` に追加した。

---

## InferenceTerminationReason の追加

追加:

```python
class InferenceTerminationReason(Enum):
  FIXED_POINT = "fixed_point"
  MAX_ROUNDS = "max_rounds"
```

Phase 5-30 では termination reason を、

```text
FIXED_POINT
MAX_ROUNDS
```

の2種類に限定した。

---

## InferenceRunResult の拡張

変更前:

```python
@dataclass(frozen=True)
class InferenceRunResult:
  steps: tuple[ProofStep, ...]
  round_history: tuple[
    tuple[ProofStep, ...],
    ...
  ]

  @property
  def round_count(self):
    return len(
      self.round_history
    )
```

変更後:

```python
@dataclass(frozen=True)
class InferenceRunResult:
  steps: tuple[ProofStep, ...]
  round_history: tuple[
    tuple[ProofStep, ...],
    ...
  ]
  termination_reason: InferenceTerminationReason

  @property
  def round_count(self):
    return len(
      self.round_history
    )
```

これにより、
fixed-point execution の停止理由を
structured data として取得できるようになった。

---

## max_rounds validation

追加:

```python
def _validate_max_rounds(
  max_rounds,
):
  if max_rounds is None:
    return

  if (
    isinstance(
      max_rounds,
      bool,
    )
    or not isinstance(
      max_rounds,
      int,
    )
  ):
    raise TypeError(
      "max_rounds must be "
      "an int or None"
    )

  if max_rounds < 0:
    raise ValueError(
      "max_rounds must be "
      "non-negative"
    )
```

有効値:

```text
None
0
1
2
...
```

無効値:

```text
negative integer
float
string
bool
```

とした。

---

## max_rounds の semantics

`max_rounds` は、

```text
maximum productive round count
```

として定義した。

例えば、

```python
max_rounds=2
```

なら、

```text
round 1
round 2
```

まで state expansion を許可する。

round 2 が完了した時点で、

```text
round_count == 2
```

となるため、
次の derivation attempt を行わず終了する。

---

## run_inference_until_stable_with_history() の拡張

signature:

```python
def run_inference_until_stable_with_history(
  inference_rules,
  available_steps,
  max_rounds=None,
):
```

とした。

fixed-point loop の先頭に、

```python
if (
  max_rounds is not None
  and len(
    round_history
  ) >= max_rounds
):
```

を追加した。

limit に到達した場合:

```python
return InferenceRunResult(
  steps=current_steps,
  round_history=tuple(
    round_history
  ),
  termination_reason=(
    InferenceTerminationReason.MAX_ROUNDS
  ),
)
```

を返す。

---

## fixed-point termination

limit に到達していない場合のみ、

```python
new_steps = derive_new_inference_steps(
  normalized_rules,
  current_steps,
)
```

を実行する。

`new_steps` が empty の場合:

```python
return InferenceRunResult(
  steps=current_steps,
  round_history=tuple(
    round_history
  ),
  termination_reason=(
    InferenceTerminationReason.FIXED_POINT
  ),
)
```

を返す。

したがって、

```text
FIXED_POINT
```

は、

```text
実際に next delta == ()
```

を確認した場合にのみ設定される。

---

## exact-limit behavior

以下の例を確認した。

```text
initial:
A

round 1:
B

round 2:
C
```

ここで、

```python
max_rounds=2
```

なら、
2 productive rounds 後に limit に到達する。

この時点では、
次の、

```text
new_steps == ()
```

をまだ確認していない。

したがって、

```text
termination_reason
=
MAX_ROUNDS
```

とする。

これは Phase 5-30 の意図した semantics である。

---

## max_rounds = 0

```python
max_rounds=0
```

も正常入力とした。

この場合、

```text
initial state
↓
limit check
↓
MAX_ROUNDS
```

となる。

結果:

```text
steps
=
initial steps

round_history
=
()

round_count
=
0

termination_reason
=
MAX_ROUNDS
```

となる。

inference builder は実行されない。

---

## simple API の拡張

Phase 5-30 の実装途中で、

```python
run_inference_until_stable_with_history()
```

には `max_rounds` が追加されていたが、

```python
run_inference_until_stable()
```

が旧 signature のまま残っていることが
テストによって検出された。

最初の test run では:

```text
217 passed
1 failed
```

となり、

```text
test_run_inference_until_stable_respects_max_rounds
```

が、

```text
TypeError:
run_inference_until_stable()
got an unexpected keyword argument 'max_rounds'
```

で失敗した。

原因は simple wrapper に
`max_rounds` parameter が追加されていなかったことだった。

---

## simple API の修正

修正後:

```python
def run_inference_until_stable(
  inference_rules,
  available_steps,
  max_rounds=None,
):
  result = (
    run_inference_until_stable_with_history(
      inference_rules,
      available_steps,
      max_rounds=max_rounds,
    )
  )

  return result.steps
```

とした。

これにより、

```python
run_inference_until_stable(
  inference_rules,
  available_steps,
  max_rounds=1,
)
```

も使用可能になった。

また simple API と detailed API が
同一の round-limit implementation を共有する形を維持した。

---

## Phase 5-30 で追加したテスト

追加:

```text
test_inference_termination_reason_values
test_run_inference_until_stable_with_history_reports_fixed_point
test_run_inference_until_stable_with_history_stops_at_max_rounds
test_run_inference_until_stable_with_history_max_rounds_zero
test_run_inference_until_stable_with_history_reaches_fixed_point_before_limit
test_run_inference_until_stable_with_history_limit_equal_to_productive_rounds
test_run_inference_until_stable_with_history_rejects_negative_max_rounds
test_run_inference_until_stable_with_history_rejects_non_integer_max_rounds
test_run_inference_until_stable_with_history_rejects_bool_max_rounds
test_run_inference_until_stable_respects_max_rounds
```

追加テスト数:

```text
10
```

また既存の、

```text
test_inference_run_result
```

を `termination_reason` field に合わせて更新した。

---

## テストで確認した semantics

Phase 5-30 のテストでは、

```text
InferenceTerminationReason enum values
normal fixed-point termination
max-round termination
max_rounds = 0
fixed point before limit
limit exactly equal to productive round count
negative limit rejection
float limit rejection
bool limit rejection
simple API limit propagation
```

を確認した。

---

## 最終 test result

修正後:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

結果:

```text
218 passed in 3.90s
```

Phase 5-29 完了時:

```text
208 passed
```

だったため、
Phase 5-30 では10 tests が増加した。

inference-rule pattern tests は
全218件成功した。

---

## regression

Phase 5-30 では、

```text
PremisePattern matching
InferenceRule matching
premise search
rule applicability
applicable-rule search
InferenceMatch
InferenceMatch application
derive_inference_steps()
merge_proof_steps()
derive_new_inference_steps()
run_inference_round()
run_inference_until_stable()
InferenceRunResult
round_history
round_count
```

を含む既存 inference-rule tests が
すべて成功した。

Phase 5-30 の termination mechanism 導入による
regression は確認されなかった。

---

## Phase 5-30 時点の fixed-point pipeline

現在の pipeline:

```text
InferenceRules
+
initial ProofSteps
↓
normalize
↓
validate max_rounds
↓
round-limit check
├── reached
│   ↓
│   MAX_ROUNDS
│
└── not reached
    ↓
    find inference matches
    ↓
    apply matches
    ↓
    candidate derived ProofSteps
    ↓
    duplicate-aware merge
    ↓
    genuinely new ProofSteps
    ↓
    delta empty?
    ├── yes
    │   ↓
    │   FIXED_POINT
    │
    └── no
        ↓
        append delta to round_history
        ↓
        expand knowledge state
        ↓
        repeat
```

最終結果:

```text
InferenceRunResult
├── steps
├── round_history
├── round_count
└── termination_reason
```

となった。

---

## Phase 5-24 から Phase 5-30 までの進展

Phase 5-24:

```text
candidate derivation
```

Phase 5-25:

```text
one-round state expansion
```

Phase 5-26:

```text
duplicate-aware merge
```

Phase 5-27:

```text
one-round genuinely-new delta
```

Phase 5-28:

```text
automatic fixed-point iteration
```

Phase 5-29:

```text
per-round history
+
structured result object
```

Phase 5-30:

```text
bounded fixed-point iteration
+
explicit termination reason
```

まで進んだ。

---

## Phase 5-30 の到達点

Phase 5-29 では、

```text
What was derived?
When was it derived?
How many productive rounds ran?
```

まで取得できた。

Phase 5-30 ではさらに、

```text
Why did inference stop?
```

を structured data として取得できるようになった。

現在は、

```text
FIXED_POINT
MAX_ROUNDS
```

を明示的に区別できる。

また、

```python
max_rounds=N
```

により、
potentially unbounded な inference execution に
有限の upper bound を設定できるようになった。

---

## 現在まだ行わないこと

Phase 5-30 では以下はまだ実装しない。

```text
cycle detection
semantic loop detection
timeout
wall-clock execution limit
memory limit
rule-application limit
InferenceRound object
per-round complete-state snapshots
applicable-rule history
InferenceMatch history
candidate derivation history
duplicate-rejected candidate history
termination diagnostics
alternative proofs
multiple proofs for same conclusion
mathematical-equivalence duplicate detection
canonicalization
alternative premise assignments
backtracking
expression-level matching
pattern variables
variable bindings
substitution
structured conclusion templates
automatic relation selection
```

特に、

```text
MAX_ROUNDS
```

は cycle detection ではない。

また、

```text
FIXED_POINT
```

も mathematical completeness を意味しない。

現在の、

```text
InferenceRule set
greedy premise matching
conclusion equality
```

の下での fixed point である。

---

## 状態

Phase 5-30 完了。

inference-rule pattern tests:

```text
218 passed in 3.90s
```

Phase 5-30 により、

```text
fixed-point inference
+
history
+
productive round count
+
round limit
+
explicit termination reason
```

まで一つの inference execution model として扱えるようになった。

次の候補としては、

```text
structured per-round execution result
```

を導入して、

```text
各 round で新しく追加された ProofSteps
どの rules / matches が使用されたか
```

をより詳細に追跡する方向が考えられる。

別の大きな方向としては、

```text
alternative premise assignments
backtracking
expression-level premise matching
pattern variables
variable binding
substitution
```

へ進み、
inference matching 自体を強化することも候補となる。


# Phase 5-31：structured per-round result object

Phase 5-30 までに、
fixed-point inference execution について、

```text
final / limited state
per-round new-step history
productive-round count
termination reason
max-round safeguard
```

を扱えるようになった。

Phase 5-29 で導入した `round_history` は、
各 productive round の、

```text
genuinely new ProofSteps
```

を、

```text
tuple[ProofStep, ...]
```

として保存していた。

Phase 5-31 では、
今後 round ごとの execution metadata を拡張できるように、
各 productive round を独立した structured result object として
表現するよう変更した。

---

## InferenceRoundResult の追加

追加:

```python
@dataclass(frozen=True)
class InferenceRoundResult:
  new_steps: tuple[ProofStep, ...]
```

`InferenceRoundResult` は、

```text
1回の productive inference round の結果
```

を表す。

Phase 5-31 時点では、

```text
new_steps
```

のみを保持する。

ここには従来 `round_history` の各要素として保存していた、

```text
その round で本当に新しく追加された ProofSteps
```

を格納する。

---

## InferenceRunResult の変更

従来:

```python
@dataclass(frozen=True)
class InferenceRunResult:
  steps: tuple[ProofStep, ...]
  round_history: tuple[
    tuple[ProofStep, ...],
    ...
  ]
  termination_reason: InferenceTerminationReason
```

Phase 5-31:

```python
@dataclass(frozen=True)
class InferenceRunResult:
  steps: tuple[ProofStep, ...]
  round_results: tuple[
    InferenceRoundResult,
    ...
  ]
  termination_reason: InferenceTerminationReason
```

これにより、
run 全体の result と、
個々の productive round の result を分離した。

現在の構造は、

```text
InferenceRunResult
├── steps
├── round_results
│   └── InferenceRoundResult
│       └── new_steps
└── termination_reason
```

となる。

---

## round_history の後方互換性

既存コードでは、

```python
result.round_history
```

を使用しているため、
Phase 5-31 ではこの API を削除しなかった。

代わりに compatibility property とした。

```python
@property
def round_history(self):
  return tuple(
    round_result.new_steps
    for round_result
    in self.round_results
  )
```

これにより、

```python
result.round_history[0]
```

は従来通り、

```text
tuple[ProofStep, ...]
```

を返す。

一方、
structured representation は、

```python
result.round_results[0]
```

から取得できる。

例えば、

```python
result.round_results[0].new_steps
```

により、
第1 productive round の new steps を取得できる。

---

## single source of truth

Phase 5-31 では、

```text
round_results
round_history
```

の両方を stored field にはしなかった。

canonical data は、

```text
round_results
```

だけに保存し、

```text
round_history
```

は property で導出する。

これにより、

```text
round_results と round_history の不整合
```

が発生しないようにした。

---

## round_count の変更

従来:

```python
@property
def round_count(self):
  return len(
    self.round_history
  )
```

Phase 5-31:

```python
@property
def round_count(self):
  return len(
    self.round_results
  )
```

semantics は変更していない。

引き続き、

```text
round_count
=
number of productive rounds
```

である。

---

## fixed-point loop の変更

`run_inference_until_stable_with_history()` では、
従来の、

```python
round_history = []
```

を、

```python
round_results = []
```

へ変更した。

productive round では、

```python
round_results.append(
  InferenceRoundResult(
    new_steps=new_steps,
  )
)
```

として structured object を保存する。

fixed-point termination 時には、

```python
InferenceRunResult(
  steps=current_steps,
  round_results=tuple(
    round_results
  ),
  termination_reason=(
    InferenceTerminationReason.FIXED_POINT
  ),
)
```

を返す。

max-round termination 時には、

```python
InferenceRunResult(
  steps=current_steps,
  round_results=tuple(
    round_results
  ),
  termination_reason=(
    InferenceTerminationReason.MAX_ROUNDS
  ),
)
```

を返す。

---

## max_rounds 判定

Phase 5-30 では、
productive-round history の長さによって
round limit を判定していた。

Phase 5-31 では canonical history が
`round_results` に変わったため、

```python
if (
  max_rounds is not None
  and len(
    round_results
  ) >= max_rounds
):
```

とした。

意味は変更していない。

```text
max_rounds
=
maximum number of productive rounds allowed
```

である。

---

## productive-round semantics

例えば、

```text
initial:
A

round 1:
B

round 2:
C

termination check:
no new step
```

の場合、

```python
round_results == (
  InferenceRoundResult(
    new_steps=(
      B,
    ),
  ),
  InferenceRoundResult(
    new_steps=(
      C,
    ),
  ),
)
```

となる。

最後の empty termination check は
`InferenceRoundResult` として保存しない。

したがって、

```text
len(round_results)
==
round_count
==
2
```

となる。

この semantics は Phase 5-29 から変更していない。

---

## 追加テスト

Phase 5-31 では以下のテストを追加した。

```text
test_inference_round_result
test_inference_round_result_is_structurally_equal
test_run_inference_until_stable_with_round_results
test_round_results_preserve_round_order
test_round_history_is_compatibility_view_of_round_results
```

確認内容:

```text
InferenceRoundResult が new_steps を保持する
InferenceRoundResult が structural equality を持つ
fixed-point execution が round_results を生成する
複数 productive round の順序が保持される
round_history が round_results の compatibility view になる
round_count が structured round results と一致する
```

---

## 既存 test の調整

`InferenceRunResult` の constructor が、

```text
round_history
```

から、

```text
round_results
```

へ変更されたため、
直接 `InferenceRunResult` を構築する既存 test を更新した。

一方、

```python
result.round_history
```

を利用する既存 fixed-point history tests は、
compatibility property によってそのまま維持できた。

これにより、
Phase 5-29 / Phase 5-30 で導入した、

```text
round_history
round_count
termination_reason
max_rounds
```

の外部 semantics を維持できた。

---

## 最終 test result

実行:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

結果:

```text
223 passed in 4.45s
```

Phase 5-30 完了時:

```text
218 passed in 3.90s
```

だったため、
Phase 5-31 では5 tests が増加した。

inference-rule pattern tests は
全223件成功した。

---

## regression

Phase 5-31 では、

```text
PremisePattern matching
InferenceRule matching
premise search
rule applicability
applicable-rule search
InferenceMatch
single / multiple InferenceMatch application
derive_inference_steps()
merge_proof_steps()
derive_new_inference_steps()
run_inference_round()
run_inference_until_stable()
run_inference_until_stable_with_history()
InferenceRunResult
round_history
round_count
InferenceTerminationReason
max_rounds
```

を含む既存 tests がすべて成功した。

structured round result 導入による
既存 inference semantics への regression は確認されなかった。

---

## Phase 5-31 時点の fixed-point pipeline

現在の pipeline:

```text
InferenceRules
+
initial ProofSteps
↓
normalize
↓
validate max_rounds
↓
round-limit check
├── reached
│   ↓
│   MAX_ROUNDS
│
└── not reached
    ↓
    find inference matches
    ↓
    apply matches
    ↓
    candidate derived ProofSteps
    ↓
    duplicate-aware merge
    ↓
    genuinely new ProofSteps
    ↓
    delta empty?
    ├── yes
    │   ↓
    │   FIXED_POINT
    │
    └── no
        ↓
        InferenceRoundResult(
          new_steps=delta
        )
        ↓
        append to round_results
        ↓
        expand knowledge state
        ↓
        repeat
```

最終 result:

```text
InferenceRunResult
├── steps
├── round_results
│   ├── InferenceRoundResult
│   │   └── new_steps
│   ├── InferenceRoundResult
│   │   └── new_steps
│   └── ...
├── round_history
│   └── compatibility view
├── round_count
└── termination_reason
```

となった。

---

## Phase 5-24 から Phase 5-31 までの進展

Phase 5-24:

```text
candidate derivation
```

Phase 5-25:

```text
one-round state expansion
```

Phase 5-26:

```text
duplicate-aware merge
```

Phase 5-27:

```text
one-round genuinely-new delta
```

Phase 5-28:

```text
automatic fixed-point iteration
```

Phase 5-29:

```text
per-round history
+
structured run result
```

Phase 5-30:

```text
bounded fixed-point iteration
+
explicit termination reason
```

Phase 5-31:

```text
structured productive-round result
+
round_history compatibility view
```

まで進んだ。

---

## Phase 5-31 の到達点

Phase 5-29 では、

```text
What was derived?
When was it derived?
How many productive rounds ran?
```

を取得できるようになった。

Phase 5-30 では、

```text
Why did inference stop?
```

を追加した。

Phase 5-31 ではさらに、

```text
What is the structured result of each productive round?
```

を表現できるようになった。

現在、

```text
run-level result
```

と、

```text
round-level result
```

を別の dataclass として扱える。

これにより、
今後 round trace に新しい情報を追加する場合でも、

```text
InferenceRunResult
```

へすべての metadata を直接追加する必要がなくなった。

---

## 現在まだ行わないこと

Phase 5-31 では以下はまだ実装しない。

```text
round index
per-round complete-state snapshot
state-before / state-after recording
applicable-rule history
InferenceMatch history
candidate derivation history
duplicate-rejected candidate history
rule-application count
terminal empty-round object
configured max_rounds in result
cycle detection
semantic loop detection
timeout
wall-clock execution limit
memory limit
alternative proofs
multiple proofs for same conclusion
mathematical-equivalence duplicate detection
canonicalization
alternative premise assignments
backtracking
expression-level matching
pattern variables
variable bindings
substitution
structured conclusion templates
automatic relation selection
```

`InferenceRoundResult` は現段階では、

```text
productive round output の container
```

であり、
完全な round execution trace ではない。

---

## 次の予定

Phase 5-31 により、
round-level metadata を追加する場所が確立した。

次の自然な段階は、

```text
InferenceMatch history
```

を各 `InferenceRoundResult` に保持することである。

概念的には、

```text
current state
↓
find InferenceMatches
↓
apply matches
↓
candidate ProofSteps
↓
duplicate filtering
↓
new ProofSteps
```

のうち、
現在 round result に保存しているのは、

```text
new ProofSteps
```

だけである。

次段階では、

```text
InferenceMatch objects
+
new ProofSteps
```

を同じ round object に記録することで、

```text
何が導出されたか
```

だけでなく、

```text
どの rule / premises の組から導出されたか
```

を round execution の単位で追跡できるようにする。

---

## 状態

Phase 5-31 完了。

inference-rule pattern tests:

```text
223 passed in 4.45s
```

Phase 5-31 により、

```text
fixed-point inference
+
history
+
structured run result
+
termination reason
+
round limit
+
structured round result
+
backward-compatible round history
```

まで一つの inference execution model として扱えるようになった。


# Phase 5-32: per-round InferenceMatch tracing

Phase 5-32 では、
Phase 5-31 で導入した

```python
InferenceRoundResult
```

を拡張し、

```text
その round で追加された ProofStep
```

だけでなく、

```text
その round で成立した InferenceMatch
```

も保存できるようにした。

---

## 背景

Phase 5-31 完了時点では、
fixed-point inference の各 productive round は、

```python
InferenceRoundResult(
  new_steps=...,
)
```

として記録されていた。

これにより、

```text
round 1 で何が追加されたか
round 2 で何が追加されたか
```

を構造化して取得できるようになった。

一方で、

```text
その round でどの InferenceRule が match したか
どの ProofStep が premises として選択されたか
```

という matching information は、
round 実行後には直接取得できなかった。

Phase 5-32 ではこの情報を
`InferenceRoundResult` に統合した。

---

## InferenceRoundResult.matches

`InferenceRoundResult` に、

```python
matches: tuple[InferenceMatch, ...] = ()
```

を追加した。

これにより、

```python
InferenceRoundResult(
  new_steps=...,
  matches=...,
)
```

という構造になった。

default を空 tuple としたため、

```python
InferenceRoundResult(
  new_steps=...,
)
```

という Phase 5-31 までの構築方法も維持される。

---

## derive_inference_round_result()

Phase 5-32 では新たに、

```python
derive_inference_round_result(
  inference_rules,
  available_steps,
)
```

を one-round detailed API として導入した。

内部処理:

```text
normalize inference rules
↓
normalize available ProofSteps
↓
find_inference_matches()
↓
matches
↓
apply_inference_matches()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
duplicate filtering
↓
genuinely new ProofSteps
↓
InferenceRoundResult
```

となる。

返り値:

```python
InferenceRoundResult(
  new_steps=new_steps,
  matches=matches,
)
```

である。

---

## derive_new_inference_steps() の再利用

既存の、

```python
derive_new_inference_steps()
```

は削除せず、

```python
round_result = (
  derive_inference_round_result(
    inference_rules,
    available_steps,
  )
)

return round_result.new_steps
```

という simple wrapper に変更した。

これにより、

```text
derive_inference_round_result()
=
詳細 API

derive_new_inference_steps()
=
new delta のみ必要な simple API
```

という役割分担になった。

one-round execution logic を
`derive_inference_round_result()` に集約できた。

---

## fixed-point runner の更新

`run_inference_until_stable_with_history()` も、

従来の、

```python
new_steps = derive_new_inference_steps(...)
```

ではなく、

```python
round_result = derive_inference_round_result(...)
new_steps = round_result.new_steps
```

を使用するように変更した。

productive round では、

```python
round_results.append(
  round_result
)
```

を行うため、

fixed-point execution 後に、

```python
result.round_results[
  round_index
].matches
```

から、
その round の matching information を取得できる。

---

## duplicate filtering 前の match を保持

Phase 5-32 では、

```text
matches
```

を、

```text
duplicate filtering 前の inference matches
```

として定義した。

例えば、

```text
rule A → "same derived"
rule B → "same derived"
```

の両方が match した場合、

```text
matches:
  rule A
  rule B
```

の2件を保持する。

一方、
knowledge state に追加される conclusion は重複除外されるため、

```text
new_steps:
  "same derived"
```

は1件のみとなる。

これにより、

```text
2 rules matched
```

という inference information を失わず、
従来の duplicate semantics も維持できる。

---

## 既知 conclusion の場合も match を保持

次のケースもテストした。

```text
available:
given
already known

rule:
given → already known
```

この場合、

rule matching 自体は成功するため、

```python
len(result.matches) == 1
```

となる。

しかし conclusion はすでに known なので、

```python
result.new_steps == ()
```

となる。

このテストにより、

```text
applicable inference
```

と、

```text
knowledge-state expansion
```

が明確に分離されていることを確認した。

---

## multi-round match preservation

複数 round の fixed-point inference についても
matches を保持できることを確認した。

例:

```text
initial
↓
relation
↓
final
```

という2段階 derivation では、

round 1:

```text
matches:
  first_rule
```

round 2:

```text
matches:
  first_rule
  second_rule
```

となる。

`first_rule` は round 2 でも依然として match するが、
その conclusion は既知なので再追加されない。

したがって、

```text
round_results[n].matches
```

は、

```text
その knowledge state において成立した rule matches
```

を表し、

```text
round_results[n].new_steps
```

は、

```text
その match 群から実際に追加された knowledge delta
```

を表す。

---

## Phase 5-32 で追加した主な tests

以下を追加・確認した。

```text
test_inference_round_result_matches_default_to_empty

test_derive_inference_round_result

test_derive_inference_round_result_new_steps_match_simple_api

test_derive_inference_round_result_no_matches

test_derive_inference_round_result_keeps_all_matches_before_duplicate_filtering

test_run_inference_until_stable_records_round_matches

test_run_inference_until_stable_preserves_per_round_matches

test_derive_inference_round_result_keeps_match_when_conclusion_is_already_known
```

---

## test result

実行:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

結果:

```text
231 passed in 5.67s
```

inference-rule pattern test は
全231件成功した。

---

## regression

Phase 5-32 では、

```text
PremisePattern
matches_premise_pattern()
matches_inference_rule()
find_matching_premises()
is_inference_rule_applicable()
find_applicable_inference_rules()
InferenceMatch
find_inference_match()
find_inference_matches()
apply_inference_match()
apply_inference_matches()
derive_inference_steps()
merge_proof_steps()
derive_new_inference_steps()
run_inference_round()
run_inference_until_stable()
run_inference_until_stable_with_history()
InferenceRunResult
InferenceRoundResult
round_history
round_results
round_count
max_rounds
termination_reason
```

を含む既存 tests がすべて成功した。

per-round match trace の導入による regression は
確認されなかった。

---

## Phase 5-32 時点の inference pipeline

現在の pipeline:

```text
InferenceRules
+
current ProofSteps
↓
find_inference_matches()
↓
InferenceMatches
↓
apply_inference_matches()
↓
candidate ProofSteps
↓
merge_proof_steps()
↓
duplicate filtering
↓
genuinely new ProofSteps
↓
InferenceRoundResult
├── matches
└── new_steps
↓
new_steps empty?
├── yes
│   ↓
│   FIXED_POINT
│
└── no
    ↓
    append InferenceRoundResult
    ↓
    expand knowledge state
    ↓
    next round
```

`max_rounds` に到達した場合は、

```text
MAX_ROUNDS
```

で終了する。

---

## Phase 5-24 から Phase 5-32 までの進展

Phase 5-24:

```text
candidate derivation
```

Phase 5-25:

```text
one-round state expansion
```

Phase 5-26:

```text
duplicate-aware merge
```

Phase 5-27:

```text
one-round genuinely-new delta
```

Phase 5-28:

```text
automatic fixed-point iteration
```

Phase 5-29:

```text
per-round history
+
structured run result
```

Phase 5-30:

```text
max-round safeguard
+
explicit termination reason
```

Phase 5-31:

```text
structured per-round result
+
round_results
```

Phase 5-32:

```text
per-round InferenceMatch trace
+
structured one-round derivation API
```

まで進んだ。

---

## Phase 5-32 の到達点

Phase 5-31 では、

```text
What was newly derived in each round?
```

を構造化して答えられるようになった。

Phase 5-32 ではさらに、

```text
Which inference rules matched in each round?
```

を答えられるようになった。

したがって現在は、

```text
match
```

と、

```text
new knowledge
```

を区別して inspection できる。

これは proof-tracing engine として重要な進展である。

特に将来、

```text
同じ結論への複数 proof path
適用可能だが新情報を生まない rule
rule selection
priority
search pruning
diagnostics
explanation generation
```

を扱う際の基礎情報となる。

---

## 次の課題

Phase 5-32 では、

```text
matches
```

と

```text
new_steps
```

を round 単位で保持できるようになった。

ただし現時点では、

```text
各 InferenceMatch
```

と、

```text
その match が生成した candidate ProofStep
```

と、

```text
その candidate が採用されたかどうか
```

の対応関係までは
専用 object として保持していない。

例えば、

```text
match A
↓
candidate X
↓
accepted

match B
↓
candidate X
↓
duplicate
```

という違いは、
`matches` と `new_steps` を比較することで推測できるが、
直接構造化されてはいない。

今後の自然な拡張候補は、

```text
match
+
candidate
+
acceptance status
+
rejection reason
```

を表す derivation-level result object である。

Phase 5-32 ではそこまで進めず、

```text
per-round matches
+
per-round genuinely-new ProofSteps
```

という最小限で安定した execution trace の構築までを完了した。


# Phase 5-33：candidate derived steps / duplicate-rejected candidate history

Phase 5-32 では、
各 productive round について、

```text
InferenceMatch
new ProofStep
```

を `InferenceRoundResult` に記録できるようにした。

Phase 5-33 では、
その間に存在する、

```text
candidate derived ProofStep
```

と、

```text
duplicate として rejected された candidate
```

も round execution trace に保存できるようにした。

---

## InferenceRoundResult の拡張

`InferenceRoundResult` を次の構造へ拡張した。

```python
@dataclass(frozen=True)
class InferenceRoundResult:
  new_steps: tuple[ProofStep, ...]
  matches: tuple[InferenceMatch, ...] = ()
  candidate_steps: tuple[ProofStep, ...] = ()
  duplicate_rejected_steps: tuple[ProofStep, ...] = ()
```

追加した field:

```text
candidate_steps
duplicate_rejected_steps
```

`candidate_steps` は、

```text
InferenceMatch を apply して生成された
duplicate filtering 前の全 ProofStep
```

を表す。

`duplicate_rejected_steps` は、

```text
candidate_steps のうち
conclusion duplicate により knowledge state へ
追加されなかった ProofStep
```

を表す。

どちらも default を、

```python
()
```

としたため、
Phase 5-31 / Phase 5-32 までの
`InferenceRoundResult` 構築方法との互換性を維持した。

---

## partition_new_and_duplicate_proof_steps()

candidate を、

```text
genuinely new
```

と、

```text
duplicate rejected
```

へ分けるため、

```python
partition_new_and_duplicate_proof_steps(
  available_steps,
  candidate_steps,
)
```

を追加した。

返り値:

```python
(
  new_steps,
  duplicate_rejected_steps,
)
```

とする。

処理は、

```text
available_steps の conclusion
↓
seen_conclusions

candidate を順番に確認
↓
already seen?
├── yes
│   ↓
│   duplicate_rejected_steps
│
└── no
    ↓
    new_steps
    ↓
    conclusion を seen に追加
```

という形とした。

---

## already-known duplicate

available state にすでに存在する conclusion を
candidate が再度生成した場合、
その candidate を明示的に保存できるようになった。

例:

```text
available:
given
known

rule:
given → known
```

結果:

```text
matches:
1

candidate_steps:
known

new_steps:
()

duplicate_rejected_steps:
known
```

従来は、

```text
match は確認できる
new_steps は空
```

という状態だったが、
Phase 5-33 では実際に生成された candidate も確認できる。

---

## same-round duplicate

同じ round 内で複数 rule が
同一 conclusion を生成する場合も記録できるようにした。

例:

```text
first_rule:
given → same

second_rule:
given → same
```

結果:

```text
matches:
2

candidate_steps:
same from first_rule
same from second_rule

new_steps:
same from first_rule

duplicate_rejected_steps:
same from second_rule
```

最初の candidate が採用された時点で
その conclusion を `seen_conclusions` に追加するため、
2件目は same-round duplicate として拒否される。

従来からの、

```text
同じ conclusion は knowledge state に1件だけ追加する
```

という semantics は変更していない。

---

## candidate order

`candidate_steps` が
`InferenceMatch` の順序を維持することをテストした。

例えば、

```text
first_rule → first
second_rule → second
```

なら、

```text
candidate_steps:
first
second
```

となる。

これにより、

```text
matches[i]
```

と、

```text
candidate_steps[i]
```

を対応付けて trace できる。

---

## accepted / rejected order

`partition_new_and_duplicate_proof_steps()` について、

```text
new_steps
```

の順序と、

```text
duplicate_rejected_steps
```

の順序が、
元の candidate processing order を維持することを確認した。

duplicate candidates を set 等へ変換せず、
execution order を保持した tuple として返す。

---

## derive_inference_round_result() の更新

Phase 5-32 で導入した、

```python
derive_inference_round_result()
```

を更新した。

現在の処理:

```text
normalize rules
↓
normalize steps
↓
find_inference_matches()
↓
matches
↓
apply_inference_matches()
↓
candidate_steps
↓
partition_new_and_duplicate_proof_steps()
├── new_steps
└── duplicate_rejected_steps
↓
InferenceRoundResult
```

返り値:

```python
InferenceRoundResult(
  new_steps=new_steps,
  matches=matches,
  candidate_steps=candidate_steps,
  duplicate_rejected_steps=(
    duplicate_rejected_steps
  ),
)
```

となった。

これにより、
one-round detailed API だけで、

```text
matching
candidate generation
duplicate filtering
accepted delta
```

をすべて確認できる。

---

## fixed-point inference への統合

`run_inference_until_stable_with_history()` は、
`derive_inference_round_result()` が返した
`InferenceRoundResult` を productive round ごとに
そのまま保存する。

そのため multi-round execution でも、

```python
result.round_results[
  n
].candidate_steps
```

および、

```python
result.round_results[
  n
].duplicate_rejected_steps
```

を取得できるようになった。

確認例では、

round 1:

```text
first_rule
↓
relation
```

round 2:

```text
first_rule
↓
relation
↓
duplicate

second_rule
↓
final
↓
new
```

という状況を作り、

round 2 に、

```text
duplicate_rejected_steps:
relation generated by first_rule
```

が保存されることを確認した。

---

## productive-round semantics

`InferenceRunResult.round_results` は
これまで通り productive round のみを保存する。

したがって、

```text
duplicate candidate が存在する
+
少なくとも1つ new candidate が存在する
```

round では、
duplicate history も保存される。

一方で、

```text
candidate がすべて duplicate
```

となった最終 fixed-point check は、

```text
new_steps == ()
```

なので `round_results` へ追加されない。

Phase 5-33 では terminal empty round の保存までは行っていない。

---

## 追加した tests

Phase 5-33 では以下のテストを追加した。

```text
test_inference_round_result_candidate_steps_default_to_empty

test_inference_round_result_duplicate_rejected_steps_default_to_empty

test_partition_new_and_duplicate_proof_steps

test_partition_new_and_duplicate_proof_steps_rejects_same_round_duplicate

test_partition_new_and_duplicate_proof_steps_preserves_order

test_partition_new_and_duplicate_proof_steps_preserves_rejected_order

test_derive_inference_round_result_records_candidate_steps

test_derive_inference_round_result_records_existing_duplicate_candidate

test_derive_inference_round_result_records_same_round_duplicate_candidate

test_derive_inference_round_result_preserves_candidate_order

test_run_inference_until_stable_records_duplicate_rejected_steps_per_round
```

合計11 tests を追加した。

---

## test result

実行対象:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

Phase 5-33 の inference-rule pattern tests:

```text
242 passed
```

Phase 5-32:

```text
231 passed
```

から11件増加した。

全242件が成功した。

---

## regression

Phase 5-33 では、
既存の、

```text
PremisePattern
matches_premise_pattern()
matches_inference_rule()
find_matching_premises()
is_inference_rule_applicable()
find_applicable_inference_rules()
InferenceMatch
find_inference_match()
find_inference_matches()
apply_inference_match()
apply_inference_matches()
derive_inference_steps()
merge_proof_steps()
derive_new_inference_steps()
run_inference_round()
run_inference_until_stable()
run_inference_until_stable_with_history()
InferenceRunResult
InferenceRoundResult
round_history
round_results
round_count
max_rounds
termination_reason
per-round matches
```

に関する tests もすべて成功した。

candidate / duplicate-rejection trace の追加による
regression は確認されなかった。

---

## Phase 5-33 時点の inference pipeline

現在の one-round pipeline:

```text
InferenceRules
+
current ProofSteps
↓
find_inference_matches()
↓
matches
↓
apply_inference_matches()
↓
candidate_steps
↓
partition_new_and_duplicate_proof_steps()
├── new_steps
└── duplicate_rejected_steps
↓
InferenceRoundResult
```

fixed-point execution では、

```text
InferenceRoundResult
↓
new_steps empty?
├── yes
│   ↓
│   FIXED_POINT
│
└── no
    ↓
    round_results に保存
    ↓
    new_steps を knowledge state へ追加
    ↓
    next round
```

となる。

`max_rounds` に到達した場合は従来通り、

```text
MAX_ROUNDS
```

で終了する。

---

## Phase 5-24 から Phase 5-33 までの進展

Phase 5-24:

```text
candidate derivation
```

Phase 5-25:

```text
one-round state expansion
```

Phase 5-26:

```text
duplicate-aware merge
```

Phase 5-27:

```text
one-round genuinely-new delta
```

Phase 5-28:

```text
automatic fixed-point iteration
```

Phase 5-29:

```text
per-round history
+
structured run result
```

Phase 5-30:

```text
max-round safeguard
+
explicit termination reason
```

Phase 5-31:

```text
structured per-round result
+
round_results
```

Phase 5-32:

```text
per-round InferenceMatch trace
+
structured one-round derivation API
```

Phase 5-33:

```text
per-round candidate trace
+
duplicate-rejected candidate history
+
explicit new / duplicate partition
```

まで進んだ。

---

## Phase 5-33 の到達点

Phase 5-32 では、

```text
Which inference rules matched?
```

と、

```text
What new knowledge was produced?
```

を round 単位で確認できた。

Phase 5-33 ではさらに、

```text
What candidate did each match generate?
```

と、

```text
Which candidate was rejected as a duplicate?
```

を確認できるようになった。

現在の round execution trace は、

```text
match
↓
candidate
↓
accepted / duplicate rejected
```

まで追跡できる。

これにより、

```text
rule が match しなかった
```

と、

```text
rule は match して candidate も生成したが
knowledge state を変化させなかった
```

を明確に区別できるようになった。

また、
同じ conclusion に対する複数 derivation のうち、
knowledge state には最初の ProofStep だけを残しながら、
duplicate として除外された derivation を
round trace から観測できる基盤ができた。

---

## 次の課題

現在は、

```text
matches
candidate_steps
new_steps
duplicate_rejected_steps
```

を parallel collections として保持している。

次の自然な拡張候補は、
各 rule application を、

```text
match
candidate
acceptance status
rejection reason
```

まで含む structured object として表現することである。

例えば、

```python
InferenceApplicationResult
```

のような object を導入すれば、

```text
この rule が何を生成したか
その candidate が採用されたか
採用されなかったならなぜか
```

を1つの object から取得できる。

その後、

```text
alternative premise assignments
backtracking
expression-level pattern matching
pattern variables
variable bindings
substitution
alternative proof preservation
```

などへ進むことができる。

---

## 状態

Phase 5-33 完了。

inference-rule pattern tests:

```text
242 passed
```

Phase 5-33 により、

```text
fixed-point inference
+
per-round structured trace
+
InferenceMatch history
+
candidate ProofStep history
+
accepted-new history
+
duplicate-rejected history
```

まで一つの inference execution model として扱えるようになった。


# Phase 5-34：InferenceApplicationResult / match-to-candidate tracing

Phase 5-33 では、
1 round の execution trace として、

```text
matches
candidate_steps
new_steps
duplicate_rejected_steps
```

を保持できるようになった。

これにより、

```text
match
↓
candidate
↓
accepted / duplicate rejected
```

まで追跡可能になった。

ただし、

```text
matches[i]
```

と、

```text
candidate_steps[i]
```

の対応は、
2つの ordered collection の同じ index を見ることで
復元する必要があった。

Phase 5-34 では、
この match-to-candidate relationship を
独立した structured object として表現した。

---

## InferenceApplicationResult を追加

`proof.py` に、

```python
@dataclass(frozen=True)
class InferenceApplicationResult:
  match: InferenceMatch
  candidate_step: ProofStep
```

を追加した。

これにより、
1回の inference application を、

```text
match
+
candidate ProofStep
```

としてまとめて保持できるようになった。

概念的には、

```text
InferenceMatch
↓
apply
↓
candidate ProofStep
```

を、

```text
InferenceApplicationResult
```

という1 object で表す。

---

## structural equality

`InferenceApplicationResult` は frozen dataclass とした。

そのため、

```text
同じ InferenceMatch
+
同じ candidate ProofStep
```

を持つ2つの application result は
structurally equal となる。

execution trace の result object として、
既存の structured inference data と同じ
value-object semantics を採用した。

---

## apply_inference_matches_with_results()

複数の `InferenceMatch` を application result として
処理するため、

```python
apply_inference_matches_with_results()
```

を追加した。

基本処理:

```text
InferenceMatch collection
↓
normalize
↓
for each match
  ↓
  apply_inference_match()
  ↓
  candidate ProofStep
  ↓
  InferenceApplicationResult(
    match,
    candidate_step,
  )
↓
tuple[InferenceApplicationResult, ...]
```

とした。

---

## single / tuple / list input

入力 normalization には、
既存の、

```python
_normalize_inference_matches()
```

を利用した。

したがって、

```text
single InferenceMatch
tuple
list
```

を受け付ける。

空 collection に対しては、

```python
()
```

を返す。

invalid input は、
既存の match collection API と同じく
`TypeError` とする。

---

## application order

`apply_inference_matches_with_results()` は
入力 `InferenceMatch` の order を保持する。

例えば、

```text
second_match
first_match
```

という順で渡した場合、

```text
application_results[0]
=
second_match の result

application_results[1]
=
first_match の result
```

となる。

candidate order も同じ application order に対応する。

これにより、
Phase 5-33 まで暗黙的だった、

```text
match order
=
candidate order
```

を structured application result の順序として確認できる。

---

## InferenceRoundResult.application_results

`InferenceRoundResult` に、

```python
application_results: tuple[
  InferenceApplicationResult,
  ...
] = ()
```

を追加した。

Phase 5-34 時点の構造:

```text
InferenceRoundResult
├── new_steps
├── matches
├── candidate_steps
├── duplicate_rejected_steps
└── application_results
```

となった。

default は、

```python
()
```

としたため、
既存の、

```python
InferenceRoundResult(
  new_steps=...,
)
```

という construction はそのまま有効である。

---

## derive_inference_round_result() の変更

Phase 5-33 では、

```text
matches
↓
apply_inference_matches()
↓
candidate_steps
↓
duplicate partition
```

としていた。

Phase 5-34 では、

```text
matches
↓
apply_inference_matches_with_results()
↓
application_results
↓
candidate_steps extraction
↓
duplicate partition
```

とした。

実装上は、

```python
application_results = (
  apply_inference_matches_with_results(
    matches
  )
)
```

から、

```python
candidate_steps = tuple(
  application_result.candidate_step
  for application_result
  in application_results
)
```

を構築する。

その後、

```python
partition_new_and_duplicate_proof_steps(
  normalized_steps,
  candidate_steps,
)
```

を従来通り使用する。

---

## existing fields との整合性

Phase 5-34 では、
`application_results` を追加しても、

```text
matches
candidate_steps
```

を削除していない。

テストでは、

```python
tuple(
  application_result.match
  for application_result
  in result.application_results
) == result.matches
```

を確認した。

また、

```python
tuple(
  application_result.candidate_step
  for application_result
  in result.application_results
) == result.candidate_steps
```

も確認した。

したがって、

```text
application_results
```

は既存 fields と矛盾しない
structured relationship として導入されている。

---

## duplicate candidate の保持

同じ conclusion を生成する複数 rule の場合も確認した。

例えば、

```text
first rule
↓
"same"

second rule
↓
"same"
```

では、

```text
application_results = 2
candidate_steps = 2
```

となる。

一方 duplicate partition 後は、

```text
new_steps = 1
duplicate_rejected_steps = 1
```

となる。

さらに、

```text
application_results[0].candidate_step
```

が採用された `new_steps[0]` に対応し、

```text
application_results[1].candidate_step
```

が `duplicate_rejected_steps[0]` に対応することを確認した。

これにより、
duplicate candidate であっても、

```text
どの match がその candidate を生成したか
```

という derivation information が失われないことを確認した。

---

## fixed-point execution への統合

`run_inference_until_stable_with_history()` の
productive round results にも、

```text
application_results
```

が保存されることを確認した。

テストでは、

```text
initial
↓
first rule
↓
relation
↓
second rule
↓
final
```

という multi-round inference を使用した。

round 1 では、

```text
application_results:
first rule → relation
```

を保持する。

round 2 では、

```text
application_results:
first rule → relation
second rule → final
```

を保持する。

round 2 の first rule による relation は
すでに既知であるため duplicate rejected されるが、
application result 自体は残る。

したがって、

```text
candidate が新規 knowledge にならなかった
```

場合でも、

```text
rule application が行われた
```

という情報を保持できる。

---

## application と duplicate decision の分離

Phase 5-34 の
`InferenceApplicationResult` は、

```text
match
candidate_step
```

だけを保持する。

現段階では、

```text
accepted
rejected
rejection_reason
```

は持たせていない。

duplicate decision は引き続き、

```text
candidate_steps
↓
partition_new_and_duplicate_proof_steps()
├── new_steps
└── duplicate_rejected_steps
```

によって round level で管理する。

これは、

```text
rule application
```

と、

```text
knowledge-state acceptance
```

を別処理として維持するためである。

---

## backward compatibility

Phase 5-34 では既存の、

```python
apply_inference_matches()
```

を変更していない。

この関数は従来通り、

```text
tuple[ProofStep, ...]
```

を返す。

詳細 trace が必要な場合のみ、

```python
apply_inference_matches_with_results()
```

を使用する。

また、

```text
derive_inference_steps()
derive_new_inference_steps()
run_inference_round()
run_inference_until_stable()
run_inference_until_stable_with_history()
round_history
round_count
termination_reason
max_rounds
```

の既存 contract も変更していない。

---

## Phase 5-34 で追加した主なテスト

追加した application-result 関連テストでは、

```text
test_inference_application_result
test_inference_application_result_is_structurally_equal
test_inference_round_result_application_results_default_to_empty
test_apply_inference_matches_with_results
test_apply_inference_matches_with_results_multiple
test_apply_inference_matches_with_results_preserves_order
test_apply_inference_matches_with_results_empty
test_apply_inference_matches_with_results_accepts_list
test_apply_inference_matches_with_results_rejects_invalid_matches
test_derive_inference_round_result_records_application_results
test_derive_inference_round_result_application_results_match_existing_fields
test_derive_inference_round_result_application_results_preserve_duplicate_candidates
test_run_inference_until_stable_records_application_results
```

を確認した。

主な確認内容:

```text
InferenceApplicationResult construction
structural equality
default empty application_results
single match application
multiple match application
order preservation
empty collection
list normalization
invalid input rejection
round-level integration
matchesとの整合性
candidate_stepsとの整合性
duplicate candidate preservation
multi-round fixed-point integration
```

である。

---

## 最終 test result

実行:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

結果:

```text
255 passed in 1.06s
```

Phase 5-33 完了時:

```text
242 passed
```

だったため、
Phase 5-34 では13 tests が増加した。

inference-rule pattern tests は
全255件成功した。

---

## regression

Phase 5-34 では、

```text
PremisePattern matching
InferenceRule matching
premise search
rule applicability
applicable-rule search
InferenceMatch construction
InferenceMatch application
apply_inference_matches()
candidate derivation
duplicate-aware merge
partition_new_and_duplicate_proof_steps()
one-round inference
fixed-point inference
round history
max-round termination
termination reasons
structured round results
per-round InferenceMatch tracing
candidate-step tracing
duplicate-rejection tracing
```

を含む既存 inference-rule tests が
すべて成功した。

`InferenceApplicationResult` 導入による
既存 inference semantics への regression は
確認されなかった。

---

## Phase 5-34 時点の inference pipeline

現在の one-round pipeline は、

```text
InferenceRules
+
current ProofSteps
↓
find_inference_matches()
↓
InferenceMatch
↓
apply_inference_matches_with_results()
↓
InferenceApplicationResult
├── match
└── candidate_step
↓
candidate_steps
↓
partition_new_and_duplicate_proof_steps()
├── new_steps
└── duplicate_rejected_steps
↓
InferenceRoundResult
```

となった。

fixed-point execution では、

```text
InferenceRunResult
├── steps
├── round_results
│   └── InferenceRoundResult
│       ├── matches
│       ├── application_results
│       │   └── InferenceApplicationResult
│       │       ├── match
│       │       └── candidate_step
│       ├── candidate_steps
│       ├── new_steps
│       └── duplicate_rejected_steps
├── round_history
├── round_count
└── termination_reason
```

となる。

---

## Phase 5-24 から Phase 5-34 までの進展

Phase 5-24:

```text
candidate derivation
```

Phase 5-25:

```text
one-round state expansion
```

Phase 5-26:

```text
duplicate-aware merge
```

Phase 5-27:

```text
one-round genuinely-new delta
```

Phase 5-28:

```text
automatic fixed-point iteration
```

Phase 5-29:

```text
per-round history
+
structured run result
```

Phase 5-30:

```text
bounded fixed-point iteration
+
explicit termination reason
```

Phase 5-31:

```text
structured productive-round result
```

Phase 5-32:

```text
per-round InferenceMatch tracing
```

Phase 5-33:

```text
candidate ProofStep tracing
+
duplicate-rejection tracing
```

Phase 5-34:

```text
structured InferenceApplicationResult
+
explicit match-to-candidate relationship
```

まで進んだ。

---

## Phase 5-34 の到達点

Phase 5-33 時点では、

```text
Which rules matched?
Which candidates were generated?
Which candidates were accepted?
Which candidates were duplicate rejected?
```

を確認できた。

Phase 5-34 ではさらに、

```text
Which candidate was generated by this specific match?
```

を直接確認できるようになった。

つまり、

```text
match
```

と、

```text
candidate
```

の関係が、
parallel collection の index relationship ではなく、

```text
InferenceApplicationResult
```

という明示的な object になった。

現在の inference trace は、

```text
premise matching
↓
InferenceMatch
↓
InferenceApplicationResult
↓
candidate ProofStep
↓
duplicate partition
↓
knowledge-state expansion
```

まで構造化されている。

---

## 次の課題

現在の `InferenceApplicationResult` は、

```text
match
candidate_step
```

までを保持する。

したがって、

```text
その candidate が採用されたか
```

を確認するには、

```text
new_steps
```

または、

```text
duplicate_rejected_steps
```

との対応を見る必要がある。

次の自然な拡張候補は、

```text
match
candidate
acceptance status
rejection reason
```

を application-level result に統合することである。

例えば、

```text
accepted
```

と、

```text
duplicate rejected
```

を明示的に区別し、
さらに duplicate rejection を、

```text
already known before round
same-round duplicate
```

などへ分類できれば、

```text
なぜこの rule application が
knowledge state を変化させなかったのか
```

をより直接説明できる。

その後、

```text
alternative premise assignments
backtracking
expression-level pattern matching
pattern variables
variable bindings
substitution
alternative proof preservation
```

へ進むことができる。

---

## 状態

Phase 5-34 完了。

inference-rule pattern tests:

```text
255 passed in 1.06s
```

Phase 5-34 により、

```text
fixed-point inference
+
per-round structured trace
+
InferenceMatch history
+
explicit match-to-candidate application results
+
candidate history
+
accepted-new history
+
duplicate-rejected history
```

まで一つの inference execution model として扱えるようになった。









