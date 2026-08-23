# ehp_proof 設計メモ

## 基本方針

EHP 完全列に固有の処理と、
一般的なアーベル群の計算を分離する。

一般的な群論処理は `algebra.py` に置き、
`ehp.py` はそれらを組み合わせて
EHP 完全列を扱う薄い層とする。

将来的に、

- double EHP
- Toda bracket
- composition relations
- その他の完全列

を追加したときにも、同じ algebra 層を再利用できる構造を目指す。

---

## Subgroup の設計

部分群は単なる元の集合ではなく、

- ambient group
- elements
- generators
- abstract structure

を持つオブジェクトとして扱う。

理由:

EHP 完全列で

```text
Im(E)
Ker(H)
Im(H)
Ker(P)
```

などを単なる集合ではなく、
群構造として比較・推論するため。

`Subgroup.structure()` により、

```text
()
(2,)
(4,)
(2, 2)
(2, 4)
```

などの有限アーベル群の抽象構造を取得する。

---

## QuotientGroup の設計

完全列

```text
A --f--> B --g--> C
```

から

```text
B / Im(f) ≅ Im(g)
```

を扱うため、商群を独立したオブジェクトとして表現する。

`QuotientGroup` は、

- ambient_group
- subgroup
- cosets
- quotient addition
- order
- abstract structure

を持つ。

現段階では有限アーベル群のみ対応する。

商群を単に位数だけで扱わず、

```text
Z/4
```

と

```text
Z/2 ⊕ Z/2
```

のような同じ位数を持つ異なる群も区別する。

---

## InducedMap の設計

準同型

```text
f : G → H
```

について、第一同型定理

```text
G / Ker(f) ≅ Im(f)
```

をプログラム上で明示的に扱う。

`InducedMap` は、

- quotient 上で well-defined か
- injective か
- surjective か
- isomorphism か

を検証する。

これは完全列から商群を推論する際の基礎とする。

---

## ExactSequenceStep の設計

連続する2写像

```text
A --f--> B --g--> C
```

を1つの単位として扱う。

主な責務:

- `Im(f)`
- `Ker(g)`
- exactness
- `B / Im(f)`
- `Im(g)`
- induced isomorphism

完全性

```text
Im(f) = Ker(g)
```

から、

```text
B / Im(f) ≅ Im(g)
```

を導く。

この一般的な完全列処理を EHP 固有コードから分離する。

---

## Extension の扱い

短完全列

```text
0 → A → B → C → 0
```

だけでは `B` は一般に一意に決まらない。

例えば、

```text
0 → Z/2 → B → Z/2 → 0
```

では、

```text
B ≅ Z/4
```

または

```text
B ≅ Z/2 ⊕ Z/2
```

が可能。

そのため、未知群を即座に1つへ決定せず、
candidate の集合として保持する設計とする。

この曖昧性はエラーではなく、
完全列から得られる情報そのものとして扱う。

将来的には、

- composition relations
- Toda brackets
- Steenrod operations
- 元の位数
- 文献上の関係式

などを追加条件として使い、
候補集合を絞り込む。

---

## ExtensionCandidate の設計

候補中間群 `B` が

```text
0 → A → B → C → 0
```

の中間群として成立可能かを判定する。

具体的には `B` の部分群 `H` で、

```text
H ≅ A
B / H ≅ C
```

となるものが存在するかを調べる。

現段階では有限アーベル群を対象とし、
小さな群について全部分群を列挙して検証する。

---

## 有限アーベル群候補の自動生成

短完全列

```text
0 → A → B → C → 0
```

では有限群の場合、

```text
|B| = |A| |C|
```

となる。

この位数から有限アーベル群の
invariant factor decomposition

```text
Z/d1 ⊕ ... ⊕ Z/dr

d1 | d2 | ... | dr
```

を満たすすべての同型型を生成する。

例えば

```text
|B| = 8
```

なら、

```text
Z/8
Z/2 ⊕ Z/4
Z/2 ⊕ Z/2 ⊕ Z/2
```

を生成する。

その後 `ExtensionCandidate` によって
実際に short exact sequence を構成可能な候補だけを残す。

候補の列挙と extension の成立判定を分離する。

---

## EHP と extension 推論の接続

EHP の連続する写像

```text
A --f--> B --g--> C
```

が完全なら、

```text
0 → Im(f) → B → Im(g) → 0
```

という短完全列が得られる。

したがって未知の中間群 `B` を推論するときに使うのは、
元の `A`, `C` そのものではなく、

```text
Im(f)
Im(g)
```

である。

`ExactSequenceStep` がこれらを抽象群として取り出し、
extension candidate の生成へ渡す。

EHP 層はこの一般機構を wrapper として利用する。

---

## algebra 層と EHP 層の分離

一般的な群論処理は `algebra.py` に置く。

主な対象:

- group elements
- homomorphisms
- subgroup
- quotient
- induced map
- exact sequence
- extension candidates
- finite abelian group classification

`ehp.py` は、

- E
- H
- P

を構成し、一般的な algebra 層へ渡す。

これにより将来、

- double EHP
- Toda bracket
- その他の完全列

でも同じ algebra 層を再利用できるようにする。

---

## 既知値と推論結果を区別する

`sphere.csv` に記録された群構造は既知データである。

一方、EHP 完全列から生成された

```text
Z/8
Z/2 ⊕ Z/4
```

などは推論候補である。

両者は混同しない。

既知値を使って候補を生成するのではなく、

```text
EHP data
→ exactness
→ extension
→ candidate structures
```

として候補を生成し、
必要に応じて既知値と比較する。

将来的な Proof Tracer では、

- known
- derived
- candidate
- excluded

の区別を明示的に持たせることを検討する。

---

## presentation ベースの一般アーベル群計算

初期実装では、一部の群論処理について

* 群の全元
* 部分群の全列挙
* quotient cosets

を実際に列挙していた。

この方式は小さな有限アーベル群では実装が単純であり、
結果を直接確認しやすいという利点がある。

一方、

```text
Z
Z ⊕ Z/2
Z^2
```

など自由部分を含む群では全元列挙はできない。

そのため Phase 4 では、
有限生成アーベル群を presentation として扱う計算経路を導入した。

基本的な計算経路は、

```text
finitely generated abelian group
↓
relation matrix
↓
integer lattice
↓
Hermite normal form
↓
Smith normal form
↓
kernel / image / cokernel
```

とする。

これにより、

```text
Z^r ⊕ finite torsion
```

という一般の有限生成アーベル群を
同じ algebra 層で扱えるようにする。

---

## 有限群列挙方式の位置づけ

presentation ベースの計算を一般的な計算経路とするが、
有限群の全元列挙方式は削除しない。

有限群では、

```text
全元列挙方式
```

と

```text
presentation / lattice / HNF / SNF
```

という独立した2通りの計算が可能である。

したがって全元列挙方式は、

> presentation 計算を検証するための reference implementation

として利用する。

有限群に対する

```text
kernel
image
cokernel
exactness
```

について両方式を cross-check することで、
presentation ベースの一般計算に対する
回帰テストとして利用する。

---

## algebra 層の責務

`algebra.py` は有限生成アーベル群とその準同型に関する
一般的な代数計算を担当する。

主な責務は、

* finitely generated abelian groups
* group homomorphisms
* presentations
* integer lattices
* kernel
* image
* cokernel
* subgroup
* quotient
* induced map
* exact sequence
* extension candidates
* finite abelian group classification

である。

algebra 層は、

```text
E
H
P
Toda bracket
composition relation
```

などのホモトピー論的意味を知らない。

例えば、

```text
f : G → H
```

が suspension homomorphism `E` であるかどうかに関係なく、
単なる有限生成アーベル群の準同型として処理する。

---

## EHP 層の責務

`ehp.py` は EHP 完全列に固有の情報を管理する。

主な責務は、

* 対象となるホモトピー群を選ぶ
* E, H, P を構成する
* source / target generators を対応させる
* EHP データから準同型行列を構成する
* algebra 層の完全列計算を呼び出す

ことである。

依存方向は、

```text
EHP layer
↓
GroupMap / ExactSequenceStep
↓
algebra layer
```

とする。

`algebra.py` から `ehp.py` への依存は作らない。

これにより将来、

* double EHP
* Toda bracket
* composition relations
* その他の完全列

を導入した場合にも、
同じ algebra 層を再利用できる。

---

## 群構造と generator の数学的名称の分離

抽象アーベル群の構造と、
ホモトピー群の generator の数学的意味は分離する。

例えば、

```text
π ≅ Z/8 ⊕ Z/4 ⊕ Z/2
```

について algebra 層が必要とするのは、

```text
Z/8
Z/4
Z/2
```

という抽象群構造である。

一方、

```text
ξ'
ξ' + λ'
η11 μ̄12
```

などの generator 名や、
それらの Toda 的・ホモトピー論的意味は
homotopy data 層で管理する。

これにより、
純粋なアーベル群計算と
数学的 generator relation を混同しない。

---

## 完全性と抽象群同型の区別

完全列

```text
A --f--> B --g--> C
```

における完全性は、

```text
Im(f) = Ker(g)
```

という `B` の部分群としての一致で判定する。

一方、完全性から第一同型定理により得られる

```text
B / Im(f) ≅ Im(g)
```

は抽象アーベル群としての同型である。

したがって、

```text
部分群として等しい
```

ことと、

```text
抽象群として同型
```

であることを別の概念として扱う。

単に両者の抽象群構造が同じであることを理由に
完全性を判定してはならない。

---

## primary decomposition の設計境界

algebra 層では、

```text
Z/2
Z/4
Z/3
Z/9
Z/5
```

などをすべて同じ有限生成アーベル群として扱う。

algebra 層自体には、

```text
2-primary
3-primary
p-primary
```

というホモトピー論上の区別を持ち込まない。

将来的に、

```text
classical EHP
double EHP
2-primary data
3-primary data
```

など異なる計算・データソースを導入しても、
最終的には同じ `AbelianGroup` / `GroupMap` の計算基盤へ渡す。

したがって primary decomposition は、
必要に応じて homotopy data / inference 層で扱う。

---

## 計算エンジンと proof engine の境界

現在の algebra / EHP 計算基盤が担当するのは、

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
↓
群構造候補
```

という計算である。

一方、

```text
E(α) = β
H(γ) = δ
P(ε) = ζ
```

などの準同型データそのものを
数学的定理から導出することは別の責務とする。

将来の proof / inference layer では、

* composition relations
* Toda brackets
* Steenrod operations
* Hopf invariant
* stable range
* literature references
* 元の位数
* 既知の定理

などを用いて、

```text
数学的事実
↓
準同型・relation
↓
algebra layer
```

という推論を行う。

つまり、

```text
proof / inference layer
↓
homotopy / EHP data layer
↓
abelian group algebra
↓
integer linear algebra
```

という層構造を基本とする。

---

## Phase 4 時点の設計原則

Phase 4 以降は、次の原則を維持する。

1. 有限生成アーベル群を統一的に扱う。
2. 自由部分を特殊ケースとして別実装しない。
3. kernel / image / cokernel の一般計算は presentation を中心とする。
4. 有限群の全元列挙は reference implementation として残す。
5. algebra 層は EHP や Toda の意味論を知らない。
6. 群の抽象構造と generator の数学的名称を分離する。
7. E/H/P の構築は EHP / homotopy data 層の責務とする。
8. exactness は一般の群準同型に対する algebra の概念として扱う。
9. 2-primary / odd-primary の区別を algebra 層へ持ち込まない。
10. 既知データからの代数計算と、定理から事実を導く proof engine を分離する。

この境界を維持することで、
将来 Toda の計算を拡張した場合にも、
algebra 基盤を作り直さずに利用できる構造を目指す。

# Proof / Relation 層

Phase 5 では、algebra 層および EHP 層の上に、
証明過程を追跡するための proof / inference 層を導入する。

---

## Relation の設計

`Relation` は、
既知の数学的事実や関係式を表す。

例えば、

```text
2η_n = 0
E(ν_n) = ν_{n+1}
```

のような関係や、

* 元の位数に関する関係
* composition relation
* suspension に関する関係
* 文献から与えられる既知関係

などを扱う。

`Relation` は数学的な入力データであり、
algebra 層による計算結果そのものではない。

例えば、

```text
2η_n = 0
```

が既知の関係式として与えられている場合は
`Relation` として扱う。

一方、

```text
Ker(f) ≅ Z/2
```

が実際の kernel 計算から得られた場合は、
`Relation` ではなく計算によって得られた
`ProofStep` として扱う。

---

## RelationType の設計

関係式の種類を区別するため、
`RelationType` を持たせる。

Phase 5-1 では最小限として、

```text
EQUALITY
ZERO
ORDER
```

を定義する。

現段階では関係式の種類を細かく分類しすぎず、
必要になった段階で、

* composition
* suspension
* Hopf invariant
* Whitehead product
* Toda bracket

などへ拡張する。

---

## ProofStep の設計

`ProofStep` は、
1回の推論または計算を表す。

基本構造は、

```text
premises
↓
rule
↓
conclusion
```

とする。

`ProofStep` は、

* `premises`
* `rule`
* `conclusion`
* 必要に応じた補足情報

を持つ。

例えば、

```text
Ker(H) = ...
Im(E) = ...
```

という計算結果や、

```text
Im(E) = Ker(H)
```

という EHP 完全性の適用を、
それぞれ独立した `ProofStep` として記録する。

---

## ProofRule の設計

`ProofStep` がどの種類の推論によって得られたかを
`ProofRule` で表す。

Phase 5-1 では、

```text
GIVEN
RELATION
EHP_EXACTNESS
KERNEL_COMPUTATION
IMAGE_COMPUTATION
COKERNEL_COMPUTATION
```

を定義する。

これにより、

```text
既知事実
数学的 relation の適用
EHP 完全性
kernel 計算
image 計算
cokernel 計算
```

を区別して記録できるようにする。

将来的には、

* composition relation
* Toda bracket
* Steenrod operation
* stable range
* literature theorem

などの推論規則を追加する。

---

## Proof の設計

`Proof` は、
ある特定の結論に対する導出全体を表す。

Phase 5-1 では、

```text
conclusion
steps
```

を持つ単純な構造とする。

例えば、

```text
step 1:
  Ker(H) を計算

step 2:
  Im(E) を計算

step 3:
  EHP 完全性を適用

step 4:
  群構造を決定
```

という一連の推論を
1つの `Proof` として保持する。

将来的には複数の推論が同じ中間結果を共有するため、
Proof は依存関係グラフとして扱うことを想定する。

ただし Phase 5-1 では、
まず `ProofStep` の順序付きリストとして保持し、
DAG 構造そのものはまだ実装しない。

---

## Relation と ProofStep の役割分担

`Relation` と `ProofStep` は明確に区別する。

```text
Relation
= 既知の数学的事実・関係式

ProofStep
= 既知事実や計算結果を使った1回の推論

Proof
= 特定の結論に至る ProofStep の集合
```

例えば、

```text
2η_n = 0
```

が文献から既知なら `Relation` である。

一方、

```text
Ker(H) ≅ Z/2
```

を `algebra.py` の kernel 計算によって得た場合は
`ProofStep` である。

この区別により、

```text
数学的入力
```

と

```text
プログラムによる計算・推論
```

を混同しない。

---

## algebra 層との境界

algebra 層は、
Proof / Relation 層の存在を知らない。

`algebra.py` は引き続き、

* finitely generated abelian groups
* homomorphisms
* kernel
* image
* cokernel
* quotient
* exactness
* extension

などの純粋な代数計算だけを担当する。

Proof 層は algebra 層の計算結果を利用できるが、
algebra 層の数学的意味論を変更しない。

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

`algebra.py` から proof 層への依存は作らない。

---

## ホモトピー論的対象との境界

Phase 5-1 では、

```text
η_n
ν_n
σ_n
```

などのホモトピー元を
専用クラスとしてまだ実装しない。

また、

```text
2η_n
η_n ○ η_{n+1}
E(ν_n)
```

などを表す式構造もまだ導入しない。

そのため Phase 5-1 の `Relation` や `ProofStep` では、
`lhs`、`rhs`、`premises`、`conclusion` に
一時的に汎用的な値を保持できる設計とする。

ホモトピー元や式を構造化する仕組みは、
Phase 5-2 以降で導入する。

---

## Phase 5-1 時点の設計原則

Phase 5-1 では、次の原則を採用する。

1. `Relation` は既知の数学的事実を表す。
2. `ProofStep` は1回の推論または計算を表す。
3. `Proof` は特定の結論に対する導出全体を表す。
4. 数学的入力と計算結果を区別する。
5. algebra 層に proof の概念を持ち込まない。
6. Proof 層は algebra 層の計算結果を利用する側とする。
7. Proof は将来的に依存関係グラフへ拡張可能な設計とする。
8. Phase 5-1 では DAG を実装せず、順序付き `ProofStep` の集合として保持する。
9. ホモトピー元や式の構造化は Phase 5-2 以降へ分離する。
10. Phase 5-1 では既存の EHP / algebra 計算機能を変更しない。






