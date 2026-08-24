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

# Expression / HomotopyElement 層

Phase 5-2 では、
`Relation` の左辺・右辺などに現れるホモトピー論的な式を、
単なる文字列ではなく構造化されたオブジェクトとして扱うための
最小 Expression モデルを導入する。

Phase 5-1 では例えば、

```text
2η3 = 0
```

を文字列として保持していた。

Phase 5-2 ではこれを、

```text
Multiple(2, eta(3))
=
Zero()
```

のような構造として表現できるようにする。

これにより、
後の proof / inference 層から式の内部構造を参照し、
relation の適用や式変形を機械的に扱えるようにする。

---

## Expression の設計

`Expression` は、
ホモトピー論的な式を表すための基底クラスとする。

Phase 5-2 では最小構成として、

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
└── Composition
```

を導入する。

現段階では式の評価や簡約は行わず、
数学的な構造を保持することだけを責務とする。

例えば、

```text
2η_3
```

は、

```text
Multiple
├── coefficient = 2
└── expression = η_3
```

として保持する。

また、

```text
η_3η_4
```

は、

```text
Composition
├── left = η_3
└── right = η_4
```

として保持する。

---

## Zero の設計

零元を文字列 `"0"` ではなく、
独立した `Zero` オブジェクトとして表す。

例えば、

```text
2η_3 = 0
```

という relation は、

```text
lhs = Multiple(2, eta(3))
rhs = Zero()
```

として保持する。

零元を専用オブジェクトとして扱うことで、
将来的に文字列表現に依存せず、

```text
式が零か
零との relation か
```

などを判定できるようにする。

---

## HomotopyElement の設計

`HomotopyElement` は、
個々のホモトピー元の名前と添字を保持する。

Phase 5-2 では、

```text
name
dimension
```

を持つ最小構造とする。

例えば、

```text
η_3
ν_4
σ_8
```

をそれぞれ、

```text
HomotopyElement("η", 3)
HomotopyElement("ν", 4)
HomotopyElement("σ", 8)
```

として表す。

現段階では、
その元が実際にどのホモトピー群に属するか、
source / target dimension が何か、
stable element との対応が何か、
といった意味論までは持たせない。

それらは必要になった段階で
homotopy data 層として拡張する。

---

## generator factory の設計

頻繁に使う基本 generator については、
直接 `HomotopyElement` を構築する代わりに、

```text
eta(n)
nu(n)
sigma(n)
```

という factory function を用意する。

例えば、

```text
eta(3)
```

は、

```text
HomotopyElement("η", 3)
```

を生成する。

これにより、
relation データを記述するときの可読性を高める。

将来的に必要に応じて、

```text
mu(n)
epsilon(n)
xi(n)
```

などを追加する。

factory function は数学的な新しい型を導入するものではなく、
`HomotopyElement` を簡潔に生成するための補助とする。

---

## Multiple の設計

整数倍を表すために `Multiple` を導入する。

`Multiple` は、

```text
coefficient
expression
```

を持つ。

例えば、

```text
2η_3
```

を、

```text
Multiple(
  2,
  eta(3),
)
```

として表す。

これにより、

```text
係数が何か
どの式の整数倍か
```

を文字列解析なしで取得できる。

Phase 5-2 では、
係数の正規化や、

```text
1α = α
0α = 0
(-1)α = -α
```

などの簡約は行わない。

式の簡約は Expression のデータモデルとは別の責務として扱う。

---

## Composition の設計

ホモトピー元の合成を表すために
`Composition` を導入する。

`Composition` は、

```text
left
right
```

を持つ。

例えば、

```text
η_3η_4
```

を、

```text
Composition(
  eta(3),
  eta(4),
)
```

として保持する。

Phase 5-2 では、
composition が実際に定義可能かどうかの dimension check は行わない。

また、

```text
Composition(alpha, beta)
```

を数学的にどちら向きの写像合成として解釈するかについても、
現段階では式構造の保持に限定する。

Toda の記法との対応や、
source / target dimension に基づく妥当性検査は
後の homotopy expression 層で追加する。

---

## Expression と文字列表現の分離

Phase 5-2 では、
`Expression` に表示処理を持たせない。

例えば、

```text
eta(3)
```

を、

```text
η3
η₃
\eta_3
```

のどの形式で表示するかは、
Expression 自体の数学的構造とは別の問題である。

将来的には、

```text
Expression
↓
formatter
├── plain text
├── Unicode
└── TeX
```

のように表示層を分離することを想定する。

そのため Phase 5-2 では、
`__str__` や TeX 出力などは導入しない。

---

## Expression と Relation の接続

Phase 5-1 で導入した `Relation` は、

```text
lhs
rhs
```

を持つ。

Phase 5-2 では、
これらに Expression オブジェクトを入れられることを確認する。

例えば、

```text
2η_3 = 0
```

を、

```text
Relation(
  lhs=Multiple(2, eta(3)),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

として保持できる。

これにより、
既知 relation を文字列ではなく
構造化された数学データとして管理する基礎ができる。

---

## Relation の型をまだ Expression に限定しない

Phase 5-2 時点では、
`Relation` の、

```text
lhs
rhs
```

の型を `Expression` に固定しない。

今後、

```text
ord(α) = 2
Ker(H) = ...
Im(E) = ...
π_n(S^m) ≅ Z/2
```

など、
単純なホモトピー元の式とは異なる種類の命題を
proof engine で扱う可能性があるためである。

したがって現段階では、

```text
Expression
```

と、

```text
Statement
```

の責務をまだ統合しない。

Phase 5-2 では、
Relation の中に Expression を格納できることだけを保証する。

より一般的な Statement モデルが必要かどうかは、
実際の proof trace を構築する段階で判断する。

---

## EHP 層との境界

Phase 5-2 では、
`expression.py` と既存の `ehp.py` をまだ接続しない。

現在の EHP 層では、
repository から取得した generator 名などを利用して
準同型を構築している。

Phase 5-2 の目的は、
これを直ちに置き換えることではない。

まず、

```text
数学的な式を構造化して保持できる
```

という独立した基盤を作り、
既存 EHP 計算を壊さないことを優先する。

したがって、

```text
algebra.py
ehp.py
repository.py
```

の既存仕様は Phase 5-2 では変更しない。

---

## Expression 層の責務

`expression.py` は、
ホモトピー論で使用する式の構造だけを担当する。

Phase 5-2 時点での責務は、

* ホモトピー元の表現
* 零元の表現
* 整数倍の表現
* composition の表現

である。

一方、

* 群演算の実計算
* kernel / image / cokernel
* EHP 完全性
* relation の検索
* relation の適用
* expression の簡約
* dimension の整合性判定
* Toda bracket
* Steenrod operation
* suspension
* Hopf invariant

などは担当しない。

---

## algebra 層との境界

`Expression` は、
`algebra.py` の `GroupElement` とは別の概念とする。

`GroupElement` は、
具体的な有限生成アーベル群内部の元として
代数計算を行うためのオブジェクトである。

一方 `HomotopyElement` は、

```text
η_n
ν_n
σ_n
```

などの数学的名称を持つホモトピー元を表す。

したがって、

```text
HomotopyElement
≠
GroupElement
```

とする。

将来的には homotopy data 層によって、

```text
HomotopyElement
↓ 対応付け
GroupElement
```

という関係を持たせる可能性があるが、
両者を同一クラスにはしない。

これにより、

```text
数学的 generator の意味
```

と、

```text
抽象アーベル群内での座標
```

を分離する。

---

## Phase 5-2 時点の設計原則

Phase 5-2 では、次の原則を採用する。

1. ホモトピー論的な式を文字列ではなく構造化して保持する。
2. `Expression` を式構造の基底とする。
3. 零元は `Zero` として独立して表現する。
4. 基本 generator は `HomotopyElement` として表現する。
5. 整数倍は `Multiple` として表現する。
6. composition は `Composition` として表現する。
7. `eta(n)`、`nu(n)`、`sigma(n)` は generator 生成の補助関数とする。
8. Expression 層では式の評価や簡約を行わない。
9. Expression 層では composition の dimension 妥当性をまだ検証しない。
10. Expression と表示形式を分離する。
11. `HomotopyElement` と algebra 層の `GroupElement` を混同しない。
12. `Relation` は Expression を保持できるが、まだ Expression 専用にはしない。
13. Expression より広い Statement モデルの必要性は後の proof engine 実装時に判断する。
14. Phase 5-2 では既存の algebra / EHP / repository の仕様を変更しない。

この境界を維持することで、
今後 relation repository、
proof trace、
composition relations、
Toda bracket などを追加する際にも、
既存の algebra 基盤とホモトピー論的な式表現を分離したまま拡張できる構造を目指す。


# Relation Repository / Proof 構築 / Formatter

Phase 5-3 以降では、
Phase 5-1 で導入した `Relation` / `ProofStep` / `Proof` と、
Phase 5-2 で導入した `Expression` を接続し、
既知 relation の検索から proof trace の構築・表示までを
段階的に実装する。

---

## RelationRepository の設計

既知の数学的 relation を保存・検索するため、
`RelationRepository` を導入する。

`RelationRepository` は、

```text
Relation の保存
Relation の検索
```

のみを責務とする。

検索条件として、

```text
lhs
rhs
relation_type
source
```

を利用できる。

複数条件が指定された場合は AND 条件として扱う。

Expression は構造的 equality を持つため、

```python
Multiple(
  2,
  eta(3),
)
```

のような式を、
文字列へ変換せずそのまま検索キーとして利用する。

`RelationRepository` 自体は、

```text
relation の適用
式変形
proof の生成
自動推論
```

を行わない。

これらは proof / inference 層の責務とする。

---

## Relation から ProofStep への変換

Repository から取得した `Relation` を
証明の一部として扱うため、

```python
relation_proof_step()
```

を導入する。

Relation は、

```text
既知の数学的事実
```

そのものであり、

ProofStep は、

```text
証明の中でその事実を使用可能な形にしたもの
```

とする。

したがって、

```text
Relation
↓
relation_proof_step()
↓
ProofStep
```

という変換を行う。

Relation を直接 Proof の依存関係に置くのではなく、
Proof の中では原則として ProofStep を依存単位とする。

---

## algebra 計算結果の ProofStep 化

kernel / image / cokernel の計算結果についても、
単なる返り値ではなく ProofStep として記録できるようにする。

対応する関数は、

```text
kernel_proof_step()
image_proof_step()
cokernel_proof_step()
```

とする。

それぞれ、

```text
Ker(f)
Im(f)
Coker(f)
```

の一般アーベル群構造を計算し、

```text
KernelStatement
ImageStatement
CokernelStatement
```

として conclusion に保持する。

これらは algebra 層そのものを変更するのではなく、
proof 層から既存 algebra API を呼び出して
計算結果を ProofStep として包む構造とする。

依存方向は引き続き、

```text
proof layer
↓
algebra layer
```

とする。

---

## Exactness の ProofStep 化

連続する準同型

```text
A --f--> B --g--> C
```

について、

```text
Im(f)
Ker(g)
```

の計算結果を premises とし、

```text
Im(f) = Ker(g)
```

を conclusion とする ProofStep を構成する。

基本形は、

```text
image step
kernel step
↓
exactness rule
↓
Im(f) = Ker(g)
```

とする。

このため、

```python
exactness_proof_step()
```

は、

```text
image_step
kernel_step
```

を明示的な premises として保持する。

EHP 完全列については、

```python
ehp_exactness_proof_step()
```

を用い、

```text
ProofRule.EHP_EXACTNESS
```

として一般の exactness と区別する。

---

## EHP Proof の構築

EHP 完全列の一部分について、

```text
Im(E)
Ker(H)
Im(E) = Ker(H)
```

または、

```text
Im(H)
Ker(P)
Im(H) = Ker(P)
```

という proof trace を自動構築する。

例えば sphere 側では、

```text
step 1:
Im(E) を計算

step 2:
Ker(H) を計算

step 3:
step 1, step 2 を前提として
Im(E) = Ker(H)
```

という構造を持つ。

この proof を、

```python
ehp_sphere_proof()
```

および、

```python
ehp_hopf_target_proof()
```

から取得できるようにする。

これにより従来の、

```text
exactness = True
```

という結果だけでなく、

```text
なぜ exact と判定されたか
```

を Proof として保持できる。

---

## Proof の premises

ProofStep の依存関係は `premises` に保持する。

Phase 5 初期では `premises` に汎用値を入れられる設計としていたが、
proof trace を構築する段階では、
ProofStep 同士の依存関係を主要な利用方法とする。

例えば、

```text
step 1
Im(E) ≅ 0

step 2
Ker(H) ≅ 0

step 3
Im(E) = Ker(H)
```

では、

```python
step3.premises == (
  step1,
  step2,
)
```

となる。

これにより Proof の `steps` は順序付きリストのままでも、
各 step がどの step に依存するかを追跡できる。

Phase 5 では完全な DAG オブジェクトはまだ導入せず、
ProofStep の参照によって依存関係を表現する。

---

## Relation を premise とする推論

既知 Relation を使用した推論についても、
Relation を ProofStep に変換した上で
premise として保持する。

基本形は、

```text
Relation
↓
relation_proof_step
↓
relation inference step
```

とする。

例えば、

```text
2η_3 = 0
```

という Relation から、

```text
η_3 has order dividing 2
```

を導く場合、

```text
step 1:
2η_3 = 0
[relation]

step 2:
η_3 has order dividing 2
[relation]
premise = step 1
```

という Proof を構成する。

このため、

```python
relation_inference_proof_step()
```

は `relation_step` を premise として受け取り、
その step が、

```text
ProofRule.RELATION
```

を持ち、かつ conclusion が `Relation` であることを確認する。

これにより、
Repository から取得された既知 relation が、
実際の proof dependency に組み込まれる。

---

## Proof Formatter の設計

Proof の内部データ構造と表示処理を分離するため、
formatter 層を導入する。

formatter は、

```text
Expression
Statement
ProofStep
Proof
```

を人間が読める文字列表現へ変換する。

主な関数は、

```text
format_expression()
format_statement()
format_proof_step()
format_proof()
```

とする。

Expression や Proof 自体には
表示形式を持たせない。

これにより将来的に、

```text
plain text
Unicode
TeX
Markdown
HTML
```

など複数の表示形式へ拡張できる余地を残す。

---

## ProofStep の番号と依存関係表示

Proof を表示するとき、
各 ProofStep に通し番号を付ける。

例えば、

```text
1. Im(E) ≅ 0
2. Ker(H) ≅ 0
3. Im(E) = Ker(H)
```

とする。

さらに step 3 の premises が
step 1 と step 2 である場合、

```text
Premises: 1, 2
```

と表示する。

Proof 内部では ProofStep のオブジェクト参照を保持し、
formatter が Proof 内での番号へ変換する。

したがって proof model 自体は、
表示用の step number を保持しない。

step number は表示層だけの概念とする。

---

## Relation metadata と ProofStep metadata の区別

`Relation` と `ProofStep` は、
それぞれ独立した補足情報を持つことができる。

Relation の、

```text
source
note
```

は、
既知の数学的事実そのものに関する metadata とする。

例えば、

```text
source = "Toda"
note = "stable range"
```

などである。

一方 `ProofStep.note` は、
その relation や計算結果を今回どのように使用したかという
推論上の補足情報とする。

したがって、

```text
Relation.note
```

と、

```text
ProofStep.note
```

は統合しない。

将来的な proof formatter では、
必要に応じて両方を表示できるようにする。

---

## Phase 5-10 時点の proof pipeline

現在の proof / inference 基盤は、

```text
Expression
↓
Relation
↓
RelationRepository
↓
relation_proof_step
↓
ProofStep
↓
premises
↓
Proof
↓
formatter
```

という経路を持つ。

また EHP 計算については、

```text
GroupMap
↓
kernel / image calculation
↓
ProofStep
↓
exactness ProofStep
↓
Proof
↓
formatter
```

という経路を持つ。

これにより、

```text
既知 relation に基づく推論
```

と、

```text
algebra / EHP 計算に基づく推論
```

を同じ Proof / ProofStep モデルで表現できる基盤ができた。

---

## Phase 5-10 時点の設計原則

1. Relation は既知の数学的事実として保持する。
2. Repository は relation の保存・検索のみを担当する。
3. Relation を proof で利用するときは ProofStep に変換する。
4. kernel / image / cokernel の計算結果も ProofStep とする。
5. exactness は image / kernel step を premises とする。
6. EHP exactness は一般 exactness と同じ構造を利用する。
7. ProofStep 同士の依存関係は premises で表現する。
8. Proof の step number は formatter 側だけで付与する。
9. Proof model と表示処理を分離する。
10. Relation の metadata と ProofStep の metadata を区別する。
11. algebra 層は proof 層を知らない。
12. Proof はまだ専用 DAG 型へ変更せず、順序付き step と参照によって依存関係を表現する。
13. Relation の適用は現段階では明示的に構築し、一般的な pattern matching や自動推論はまだ行わない。
14. 既知 relation と algebra 計算の両方を同一の Proof モデルへ統合できる構造を維持する。


# Relation metadata / LiteratureReference

## Relation metadata の表示

Phase 5-11 では、
Relation および ProofStep が保持している metadata を
Proof formatter へ反映する。

対象は、

```text
Relation.source
Relation.note
ProofStep.note
```

である。

`Relation.source` は、
その数学的 relation がどこから得られたかを表す。

`Relation.note` は、
relation 自体についての数学的補足情報を表す。

一方、

`ProofStep.note` は、
その relation や計算結果を今回の推論で
どのように利用したかについての補足とする。

したがって、

```text
Relation.note
```

と、

```text
ProofStep.note
```

は統合しない。

例えば、

```text
1. 2η_3 = 0
   [relation]
   Source: Toda
   Relation note: classical eta relation

2. η_3 has order dividing 2
   [relation]
   Premises: 1
   Note: derived from the zero relation
```

のように、
数学的事実そのものの metadata と
推論 step の metadata を区別して表示する。

---

## LiteratureReference の設計

Phase 5-12 では、
Relation の出典を単なる文字列ではなく、
構造化された文献参照として保持できるようにする。

そのため、

```text
LiteratureReference
```

を導入する。

基本構造は、

```text
label
author
title
year
locator
```

とする。

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

のように文献情報を保持できる。

ここで、

```text
label
```

は Proof 表示や簡潔な識別に使用する名前、

```text
author
title
year
```

は書誌情報、

```text
locator
```

は relation が文献中のどこに記載されているかを表す
位置情報とする。

locator には将来的に、

```text
Theorem ...
Proposition ...
Lemma ...
Chapter ...
p. ...
equation (...)
```

などを格納できる。

現段階では locator の内部構造までは分解せず、
文字列として保持する。

---

## Relation.source の後方互換性

Phase 5-12 では、

```text
Relation.source
```

を完全に `LiteratureReference` 専用にはしない。

型は、

```text
LiteratureReference | str | None
```

とする。

これにより従来の、

```python
source="Toda"
```

も引き続き利用できる。

新しく構造化された source を利用する場合は、

```python
source=LiteratureReference(...)
```

とする。

この後方互換性によって、
既存 Relation データを一度に書き換える必要をなくし、
relation データの追加に合わせて段階的に
structured source へ移行できる。

---

## LiteratureReference と Relation.note の区別

文献情報と数学的補足は混在させない。

例えば、

```text
Toda の Proposition ...
```

のような文献上の位置は、

```text
LiteratureReference.locator
```

に保持する。

一方、

```text
stable range で成立
classical eta relation
```

など relation 自体の数学的説明は、

```text
Relation.note
```

に保持する。

したがって、

```text
LiteratureReference
= relation の出典情報

Relation.note
= relation の数学的補足

ProofStep.note
= その relation を利用した推論上の補足
```

という3つの責務を分離する。

---

## LiteratureReference の表示

formatter 層では、

```text
format_literature_reference()
format_source()
```

によって source を表示する。

structured source の例:

```text
Source: Toda — H. Toda, Composition Methods in Homotopy Groups of Spheres, 1962 — ...
```

従来の文字列 source:

```text
Source: Toda
```

も同じ formatter から表示できる。

文献情報の表示方法は formatter 層の責務とし、
`LiteratureReference` 自体に表示処理を持たせない。

---

## RelationRepository との接続

`LiteratureReference` は frozen dataclass として
構造的 equality を持つ。

そのため既存の `RelationRepository` を変更せず、

```python
repository.find_relations(
  source=reference,
)
```

によって structured source を持つ relation を検索できる。

Phase 5-12 では、

```text
author
title
year
label
locator
```

を個別条件として検索する機能は導入しない。

RelationRepository は引き続き、
Relation オブジェクトの保存と基本検索のみを責務とする。

より高度な文献検索や文献データ管理が必要になった場合に、
別途 literature repository 等の導入を検討する。

---

## Phase 5-12 時点の source pipeline

現在、

```text
LiteratureReference
        ↓
Relation.source
        ↓
Relation
        ↓
relation_proof_step
        ↓
Proof
        ↓
format_source
        ↓
Proof trace
```

という経路が成立している。

これにより Proof trace は、

```text
何を使ったか
```

だけでなく、

```text
その数学的事実はどこから得られたか
```

まで追跡できる基盤を持つ。

---

## Phase 5-12 時点の設計原則

1. 文献情報は構造化された `LiteratureReference` として保持できる。
2. `Relation.source` は当面 `LiteratureReference | str | None` とする。
3. 既存の文字列 source との後方互換性を維持する。
4. 書誌情報と relation の数学的 note を分離する。
5. 文献中の位置は `locator` に保持する。
6. locator は現段階では文字列とし、過剰に構造化しない。
7. 文献の表示方法は formatter 層の責務とする。
8. LiteratureReference 自体に表示処理を持たせない。
9. RelationRepository は structured source でも既存 equality 検索を利用する。
10. 文献検索専用 Repository はまだ導入しない。
11. BibTeX / DOI / ISBN 等の管理は必要になった段階で追加する。
12. テスト用 locator と実際の文献 locator を混同しない。


# 複数 premise を用いる Relation inference

## Phase 5-13：Relation inference の一般化

Phase 5-12 までの relation inference は、

```text
1つの Relation
↓
relation ProofStep
↓
inference ProofStep
```

という形を基本としていた。

しかし実際の数学的推論では、

```text
複数の既知 relation
+
既に得られている計算結果
↓
新しい結論
```

という形が必要になる。

Phase 5-13 では、
relation inference が複数の ProofStep を
premises として利用できるように一般化する。

---

## relation_steps と premises の区別

`relation_inference_proof_step()` では、

```text
relation_steps
premises
```

を別の引数として扱う。

`relation_steps` は、

```text
ProofRule.RELATION
```

を持ち、
conclusion が `Relation` である ProofStep に限定する。

一方 `premises` は、
既に得られている一般の ProofStep を受け取る。

例えば、

```text
relation step 1
relation step 2
kernel computation step
↓
relation inference
↓
conclusion
```

のような推論を表現できる。

この区別により、

```text
relation として利用する既知の数学的事実
```

と、

```text
既に得られている計算結果・推論結果
```

を API 上で区別できる。

---

## Proof dependency の単位

Relation を直接 `premises` に格納するのではなく、

```text
Relation
↓
relation_proof_step()
↓
ProofStep
```

という変換を行った上で dependency に利用する。

したがって proof trace における
主要な依存関係の単位は `ProofStep` とする。

これにより、

```text
既知 relation
計算結果
既に導出された中間結果
```

を同じ dependency model で扱える。

例えば、

```text
Relation 1
↓
ProofStep 1

Relation 2
↓
ProofStep 2

kernel computation
↓
ProofStep 3

ProofStep 1, 2, 3
↓
relation inference
↓
ProofStep 4
```

という構造を表現できる。

---

## 単一 Relation との後方互換性

複数 relation へ一般化したが、
従来の、

```python
relation_inference_proof_step(
  conclusion,
  relation_step,
)
```

という単一 premise の形式も維持する。

内部では単一 ProofStep を、

```text
(step,)
```

へ正規化して処理する。

同様に `relation_inference_proof()` も、

```text
Relation
```

または、

```text
tuple/list of Relation
```

の両方を受け取る。

これにより既存コードに breaking change を導入せず、
複数 relation inference へ拡張する。

---

## normalize helper

入力形式を統一するため、

```text
_normalize_proof_steps()
_normalize_relations()
```

を導入する。

`_normalize_proof_steps()` は、

```text
ProofStep
```

または、

```text
tuple/list of ProofStep
```

を受け取り、
内部的には tuple に統一する。

`_normalize_relations()` は、

```text
Relation
```

または、

```text
tuple/list of Relation
```

を受け取り、
内部的には tuple に統一する。

また、
tuple / list 内に不正な型が含まれている場合は、
早い段階で `TypeError` とする。

これにより inference 本体では、
単一入力と複数入力を個別に処理する必要がなくなる。

---

## relation_steps の検証

`relation_inference_proof_step()` に渡される
`relation_steps` は、
単なる ProofStep であれば何でもよいわけではない。

各 step は、

```text
ProofRule.RELATION
```

を持ち、
さらに、

```text
step.conclusion
```

が `Relation` であることを要求する。

したがって、

```text
kernel computation
image computation
given
exactness
```

などの ProofStep を
`relation_steps` として渡すことはできない。

これらを推論の前提として利用する場合は、

```text
premises
```

として渡す。

---

## 追加 premises

Phase 5-13 では、
Relation 以外の既存 ProofStep を、

```text
premises
```

として追加できる。

例えば、

```text
1. α = β
   [relation]

2. γ = δ
   [relation]

3. Ker(H) ≅ Z/2
   [kernel computation]

4. desired conclusion
   [relation]
   Premises: 1, 2, 3
```

のような proof dependency を構築できる。

これにより、

```text
文献上の既知 relation
+
algebra による計算結果
+
以前に導出された結果
```

を組み合わせるための基礎ができる。

---

## 空 relation の禁止

relation inference は、
少なくとも1つの relation を使用するものとする。

したがって、

```text
relation_steps = ()
```

または、

```text
relations = ()
```

は許可しない。

この場合は `ValueError` とする。

relation を使用しない一般的な推論については、
将来的に別の inference rule / API を導入する。

---

## formatter との接続

formatter は既に ProofStep の `premises` を走査し、

```text
Premises: 1, 2, ...
```

と表示できる。

そのため Phase 5-13 では
formatter 本体の変更は必要ない。

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

のように複数 dependency を表示できる。

Phase 5-13 では integration test を追加し、
複数 Relation を premises とする Proof が
正しく番号表示されることを確認する。

---

## Phase 5-13 時点の inference pipeline

現在、

```text
Relation 1
     ↓
ProofStep 1

Relation 2
     ↓
ProofStep 2

other ProofStep
     ↓

ProofStep 1
ProofStep 2
other ProofStep
     ↓
relation inference
     ↓
new ProofStep
     ↓
Proof
     ↓
formatter
```

という構造を表現できる。

これにより、
単一 relation に基づく例示的な推論から、

```text
複数の数学的事実
+
計算結果
+
既存の推論結果
↓
新しい結論
```

という、
より一般的な proof construction へ進んだ。

---

## ProofStep.premises の型について

`ProofStep` の型定義自体は現在、

```python
premises: tuple[Any, ...]
```

のままとする。

Phase 5-13 の inference API では
premises に ProofStep を要求するが、
既存コードには Relation などを直接 premises に格納する
初期段階の利用例も残っている。

そのため Phase 5-13 では、
`ProofStep.premises` 自体を

```text
tuple[ProofStep, ...]
```

へ変更することは行わない。

Proof 全体で dependency の単位を
ProofStep に統一するかどうかは、
既存コードを整理する後続フェーズで検討する。

---

## Phase 5-13 時点の設計原則

1. Relation は Proof に入る前に ProofStep 化する。
2. Proof dependency の主要単位は ProofStep とする。
3. relation inference は複数 relation を利用できる。
4. relation inference は追加の一般 ProofStep も premise にできる。
5. `relation_steps` と追加 `premises` は API 上区別する。
6. `relation_steps` は `ProofRule.RELATION` を持つ必要がある。
7. `relation_steps` の conclusion は Relation でなければならない。
8. relation inference には少なくとも1つの Relation が必要である。
9. 単一 Relation を利用する従来 API との後方互換性を維持する。
10. 単一入力と複数入力は normalize helper によって統一する。
11. formatter は既存の複数 premises 表示機能をそのまま利用する。
12. `ProofStep.premises` 自体の型制限はまだ強化しない。
13. premises の再帰的収集や DAG 自動構築はまだ行わない。
14. relation の自動検索や pattern matching はまだ導入しない。
15. relation を使用しない一般 inference rule は後続フェーズで検討する。


# InferenceRule と推論規則の構造化

## Phase 5-14：InferenceRule の導入

Phase 5-13 までに、
複数の Relation および既存の ProofStep を
premises とする relation inference を構築できるようになった。

しかし Phase 5-13 時点では、
relation inference によって生成された ProofStep はすべて、

```text
ProofRule.RELATION
```

として扱われていた。

このため、

```text
どの ProofStep を前提として使ったか
```

は `premises` から追跡できる一方、

```text
それらの premises から
どの数学的推論規則を使って
conclusion を導いたのか
```

は構造化されていなかった。

Phase 5-14 では、
この情報を明示的に保持するため、

```text
InferenceRule
```

を導入する。

---

## ProofRule と InferenceRule の区別

`ProofRule` と `InferenceRule` は
異なる責務を持つ。

`ProofRule` は、
ProofStep の処理の大分類を表す。

例えば、

```text
GIVEN
RELATION
EXACTNESS
EHP_EXACTNESS
KERNEL_COMPUTATION
IMAGE_COMPUTATION
COKERNEL_COMPUTATION
```

などである。

一方 `InferenceRule` は、
premises から conclusion を導く際に使用した
具体的な数学的推論規則を表す。

例えば、

```text
zero relation implies order bound
```

という推論規則は、

```text
mα = 0
↓
ord(α) divides m
```

という数学的推論を表す。

したがって、

```text
ProofRule
= ProofStep の大分類

InferenceRule
= premises から conclusion を導く具体的規則
```

とする。

---

## InferenceRule の設計

Phase 5-14 では、
`InferenceRule` を最小構造として導入する。

保持する情報は、

```text
name
description
```

とする。

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

のように表現する。

`name` は Proof trace に表示する短い名称とする。

`description` は、
推論規則の数学的意味を説明する補足情報とする。

Phase 5-14 では、
`description` は保持するだけであり、
Proof formatter にはまだ表示しない。

---

## ProofStep と InferenceRule の接続

`ProofStep` に、

```text
inference_rule
```

を追加する。

型は、

```text
InferenceRule | None
```

とする。

これにより、

```text
premises
↓
InferenceRule
↓
conclusion
```

という構造を ProofStep 内に保持できる。

例えば、

```text
1. 2η_3 = 0
   [relation]

2. η_3 has order dividing 2
   [relation]
   Inference rule: zero relation implies order bound
   Premises: 1
```

という Proof trace を構築できる。

内部構造としては、

```text
ProofStep
├── conclusion
├── premises
├── rule
├── note
└── inference_rule
```

となる。

---

## inference_rule は optional とする

既存の ProofStep には
InferenceRule を持たないものが多数存在する。

例えば、

```text
kernel computation
image computation
cokernel computation
given
```

などについては、
Phase 5-14 で新しい InferenceRule を強制しない。

また既存の relation inference API との
後方互換性も維持する。

したがって、

```text
inference_rule = None
```

を許可する。

従来の、

```python
relation_inference_proof(
  relation,
  conclusion,
)
```

もそのまま動作する。

必要な場合のみ、

```python
relation_inference_proof(
  relation,
  conclusion,
  inference_rule=rule,
)
```

とする。

---

## inference_rule の検証

relation inference API に渡される
`inference_rule` は、

```text
InferenceRule
```

または、

```text
None
```

に限定する。

文字列などを直接渡すことは許可しない。

例えば、

```python
inference_rule=(
  "zero relation implies order bound"
)
```

のような入力は使用しない。

必ず、

```python
InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
  ),
)
```

として構造化する。

これにより将来的に、

```text
rule name
description
premise pattern
conclusion construction
source
```

などへ拡張できる。

---

## relation inference との接続

Phase 5-13 で一般化した、

```text
relation_inference_proof_step()
relation_inference_proof()
```

に、

```text
inference_rule
```

引数を追加する。

例えば、

```python
rule = InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
  ),
)

proof = relation_inference_proof(
  relation,
  conclusion,
  inference_rule=rule,
)
```

とする。

生成された inference ProofStep は、

```text
rule = ProofRule.RELATION
```

を維持しつつ、

```text
inference_rule = rule
```

として具体的な推論規則も保持する。

このため、

```text
ProofRule.RELATION
```

を細かな数学的規則ごとに増やす必要はない。

---

## formatter との接続

formatter に、

```text
format_inference_rule()
```

を追加する。

Phase 5-14 では、
InferenceRule の `name` を表示する。

例えば、

```text
Inference rule: zero relation implies order bound
```

と表示する。

Proof trace 全体では、

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
```

のようになる。

これにより、

```text
使用した数学的事実
使用した推論規則
依存した ProofStep
推論時の補足
```

をそれぞれ区別して表示できる。

---

## metadata の責務分離

Phase 5-14 時点では、
proof trace 上の情報を次のように区別する。

```text
LiteratureReference
= Relation の文献出典

Relation.note
= Relation 自体の数学的補足

ProofStep.note
= その ProofStep における補足

ProofRule
= ProofStep の処理の大分類

InferenceRule
= premises から conclusion を導く具体的な数学的規則
```

これらを統合しない。

例えば、

```text
Source
```

と、

```text
Inference rule
```

は異なる。

Source は、

```text
その数学的事実をどこから得たか
```

を表す。

InferenceRule は、

```text
その事実からどの規則を使って
新しい結論を得たか
```

を表す。

---

## Phase 5-14 時点の inference pipeline

現在の relation inference は、

```text
LiteratureReference
        ↓
Relation
        ↓
relation_proof_step
        ↓
ProofStep
        │
        ├──────────────┐
        │              │
        ↓              ↓
    premises      InferenceRule
        │              │
        └──────┬───────┘
               ↓
       inference ProofStep
               ↓
             Proof
               ↓
           formatter
```

という構造を持つ。

これにより、

```text
何を使ったか
```

だけでなく、

```text
どの推論規則を使ったか
```

も Proof trace に保持できるようになった。

---

## Phase 5-14 ではまだ行わないこと

Phase 5-14 の `InferenceRule` は、
推論規則の metadata を構造化する段階とする。

まだ、

```text
premise pattern の定義
pattern matching
rule applicability 判定
conclusion の自動生成
InferenceRule の apply()
InferenceRule repository
自動 relation 検索
自動 proof construction
```

は行わない。

したがって現段階では、

```text
InferenceRule
```

を指定しても、
その rule が本当に premises に適用可能かを
機械的に判定するわけではない。

conclusion も引き続き明示的に指定する。

自動適用機構は後続フェーズで導入する。

---

## Phase 5-14 時点の設計原則

1. `ProofRule` と `InferenceRule` を区別する。
2. `ProofRule` は ProofStep の大分類とする。
3. `InferenceRule` は具体的な数学的推論規則とする。
4. `InferenceRule` は `name` と `description` を持つ。
5. `ProofStep` は optional な `inference_rule` を保持できる。
6. inference_rule を持たない既存 ProofStep との後方互換性を維持する。
7. relation inference は InferenceRule を明示的に受け取れる。
8. 不正な inference_rule 型は拒否する。
9. formatter は InferenceRule の name を表示する。
10. LiteratureReference と InferenceRule を混同しない。
11. Relation.note と InferenceRule を混同しない。
12. ProofStep.note と InferenceRule を混同しない。
13. InferenceRule の pattern matching はまだ実装しない。
14. InferenceRule の自動適用はまだ実装しない。
15. conclusion は引き続き明示的に構築する。
16. algebra 層には InferenceRule の概念を持ち込まない。


# InferenceRule の premise pattern

## Phase 5-15：InferenceRule に premise pattern を持たせるための最小基盤

Phase 5-14 では、
具体的な数学的推論規則を表す

```text
InferenceRule
```

を導入した。

これにより、

```text
premises
↓
InferenceRule
↓
conclusion
```

という推論構造を ProofStep に保持できるようになった。

ただし Phase 5-14 の `InferenceRule` が持つ情報は、

```text
name
description
```

だけであり、

```text
その inference rule が
どのような premise を必要とするか
```

はまだ構造化されていなかった。

Phase 5-15 では、
InferenceRule が要求する premise の種類を記述するための
最小構造として、

```text
PremisePattern
```

を導入する。

---

## PremisePattern の設計

`PremisePattern` は、

```text
InferenceRule が要求する
1つの premise の条件
```

を表す。

Phase 5-15 では最小構造として、

```text
proof_rule
statement_type
relation_type
```

を保持する。

定義は、

```python
@dataclass(frozen=True)
class PremisePattern:
  proof_rule: ProofRule | None = None
  statement_type: type | None = None
  relation_type: RelationType | None = None
```

とする。

各項目を optional とすることで、
必要な条件だけを指定できる。

---

## proof_rule

`proof_rule` は、
premise として要求する ProofStep の
大分類を表す。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
)
```

は、

```text
ProofRule.RELATION
```

を持つ ProofStep を要求する pattern を表す。

将来的には、

```text
ProofRule.GIVEN
ProofRule.EXACTNESS
ProofRule.EHP_EXACTNESS
ProofRule.KERNEL_COMPUTATION
ProofRule.IMAGE_COMPUTATION
ProofRule.COKERNEL_COMPUTATION
```

なども pattern 条件として利用できる。

Phase 5-15 では、
この条件を保持するだけであり、
実際の ProofStep に対する一致判定はまだ行わない。

---

## statement_type

`statement_type` は、
ProofStep の、

```text
conclusion
```

に要求する型を表す。

例えば、

```python
PremisePattern(
  statement_type=Relation,
)
```

は、

```text
conclusion が Relation
```

である ProofStep を要求する pattern を表す。

将来的には、

```text
KernelStatement
ImageStatement
CokernelStatement
ExactnessStatement
```

なども同じ仕組みで指定できる。

これにより、

```text
ProofRule
```

だけでなく、

```text
どの種類の Statement を
conclusion とする ProofStep か
```

という条件を rule 側に記述できる。

---

## relation_type

`statement_type` が `Relation` である場合、
さらに Relation の種類を限定できるように、

```text
relation_type
```

を持たせる。

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

という premise を要求する pattern を表す。

これにより、

```text
ZERO relation
ORDER relation
EQUALITY relation
```

を rule の要求条件として区別できる。

---

## InferenceRule.premise_patterns

`InferenceRule` に、

```text
premise_patterns
```

を追加する。

型は、

```text
tuple[PremisePattern, ...]
```

とする。

既存の InferenceRule との後方互換性を維持するため、

```text
()
```

をデフォルト値とする。

したがって従来の、

```python
InferenceRule(
  name="example rule",
)
```

もそのまま利用できる。

一方、
premise pattern を持つ rule は、

```python
InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
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

のように表現できる。

この rule は構造上、

```text
ZERO relation を1つ premise として要求する
```

という情報を保持する。

---

## 複数 premise pattern

`premise_patterns` は tuple とするため、
複数の premise を要求する rule も表現できる。

例えば、

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

のように、

```text
ZERO relation
+
GIVEN step
```

を必要とする rule を記述できる。

Phase 5-15 では、
tuple の順序を premise pattern の記述順として保持する。

ただし、

```text
実際の premises と
premise_patterns の順序を
どのように対応させるか
```

についての意味論はまだ確定しない。

実際の matching を実装する段階で整理する。

---

## PremisePattern を独立型とする理由

InferenceRule に直接、

```text
required_proof_rules
required_statement_types
required_relation_types
```

などを個別に持たせるのではなく、

```text
1つの premise に対する条件
```

を `PremisePattern` としてまとめる。

例えば、

```text
ProofRule.RELATION
+
Relation
+
RelationType.ZERO
```

は、
すべて同じ1つの premise に対する条件である。

これらを別々の tuple として保持すると、

```text
どの proof_rule と
どの statement_type と
どの relation_type が
同じ premise を表しているか
```

が不明確になる。

そのため、

```text
PremisePattern
= 1つの premise に対する条件
```

として独立したデータ構造を採用する。

---

## optional field の意味

Phase 5-15 では、
各条件を、

```text
None
```

にできる。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
)
```

は、

```text
ProofRule.RELATION であることだけを要求する
```

という意味になる。

また、

```python
PremisePattern(
  statement_type=ExactnessStatement,
)
```

のように、

```text
ProofRule は問わず
conclusion の型だけを要求する
```

という pattern も表現できる。

この設計によって、
pattern の条件を最初から過度に固定せず、
必要な条件だけを段階的に追加できる。

---

## Phase 5-15 では matching を行わない

Phase 5-15 の目的は、

```text
InferenceRule が
どのような premise を必要とするかを
データとして表現できる
```

ところまでとする。

まだ、

```text
PremisePattern
+
ProofStep
↓
match / no match
```

という判定は行わない。

したがって、

```python
rule = InferenceRule(
  name="example",
  premise_patterns=(pattern,),
)
```

を作成しても、

```text
実際に渡された ProofStep が
pattern に一致しているか
```

は検証されない。

既存の、

```text
relation_inference_proof_step()
relation_inference_proof()
```

の挙動にも変更を加えない。

---

## Expression pattern はまだ導入しない

Phase 5-15 では、

```text
ProofRule
Statement type
RelationType
```

までを premise pattern の条件とする。

例えば、

```text
mα = 0
```

という relation に対して、

```text
lhs が Multiple
rhs が Zero
Multiple.coefficient を m として束縛
Multiple.expression を α として束縛
```

といった Expression 内部の pattern matching はまだ行わない。

したがって、

```python
PremisePattern(
  relation_type=RelationType.ZERO,
)
```

によって、

```text
ZERO relation
```

であることまでは表現できるが、

```text
mα = 0
```

という具体的な式構造までは記述しない。

Expression pattern は、
ProofStep レベルの matching が安定した後の
後続フェーズで導入する。

---

## Pattern variable はまだ導入しない

将来的には、

```text
m
α
β
n
```

などを pattern variable として使い、

```text
mα = 0
↓
ord(α) divides m
```

のような rule を
一般化する必要がある。

しかし Phase 5-15 では、

```text
変数束縛
unification
substitution
```

は導入しない。

まず、

```text
どの種類の ProofStep を premise とするか
```

という粗い構造を記述できるようにする。

---

## Repository との接続はまだ行わない

`PremisePattern` を導入しても、

```text
RelationRepository
```

から pattern に一致する Relation を
自動検索することはまだ行わない。

Phase 5-15 時点では、

```text
RelationRepository
= Relation の保存・基本検索

InferenceRule
= 推論規則と premise 要求の記述
```

として責務を分離する。

将来的には、

```text
InferenceRule
↓
PremisePattern
↓
RelationRepository / existing ProofSteps
↓
candidate premises
```

という接続を検討する。

---

## Phase 5-15 時点の inference rule 構造

Phase 5-15 により、

```text
InferenceRule
├── name
├── description
└── premise_patterns
      │
      ├── PremisePattern
      │     ├── proof_rule
      │     ├── statement_type
      │     └── relation_type
      │
      └── PremisePattern
            └── ...
```

という構造を持つようになった。

Phase 5-14 では、

```text
どの規則を使ったか
```

を記録できるようになった。

Phase 5-15 ではさらに、

```text
その規則が
どのような premise を期待するか
```

を記述できるようになった。

ただしこれはまだ、

```text
rule specification
```

の段階であり、

```text
rule execution
```

ではない。

---

## Phase 5-15 時点の推論基盤

現在の inference 層は、

```text
Expression
↓
Relation
↓
RelationRepository
↓
ProofStep
↓
premises
        +
InferenceRule
        │
        └── premise_patterns
↓
inference ProofStep
↓
Proof
↓
formatter
```

という構造を持つ。

InferenceRule は、

```text
具体的な数学的規則
```

だけでなく、

```text
その規則が要求する premise の種類
```

も保持できるようになった。

---

## Phase 5-15 ではまだ行わないこと

Phase 5-15 では、以下は実装しない。

```text
PremisePattern と ProofStep の matching
InferenceRule applicability 判定
Expression 内部の pattern matching
pattern variable
変数束縛
unification
substitution
conclusion の自動生成
InferenceRule.apply()
InferenceRule repository
RelationRepository からの自動 relation 選択
既存 ProofStep からの自動 premise 選択
proof の自動構築
Proof DAG の自動構築
```

これらは、
premise pattern の最小モデルを基礎として
後続フェーズで段階的に追加する。

---

## Phase 5-15 時点の設計原則

1. `InferenceRule` は要求する premise の pattern を保持できる。
2. 1つの premise に対する条件は `PremisePattern` としてまとめる。
3. `PremisePattern` は `proof_rule` を条件にできる。
4. `PremisePattern` は conclusion の `statement_type` を条件にできる。
5. Relation については `relation_type` も条件にできる。
6. 各 pattern 条件は optional とし、必要な条件だけを指定できる。
7. `InferenceRule.premise_patterns` は tuple とする。
8. premise pattern を持たない既存 InferenceRule との後方互換性を維持する。
9. 複数 premise を要求する rule を表現可能にする。
10. Phase 5-15 では pattern の保持だけを行う。
11. PremisePattern と ProofStep の一致判定はまだ行わない。
12. Expression 内部の pattern matching はまだ行わない。
13. pattern variable や変数束縛はまだ導入しない。
14. conclusion の自動生成はまだ行わない。
15. RelationRepository との自動接続はまだ行わない。
16. algebra 層には premise pattern の概念を持ち込まない。
17. InferenceRule の specification と rule の実行機構を分離する。
18. 次段階では ProofStep が PremisePattern に一致するかを判定する最小 matching 基盤を検討する。


# PremisePattern と ProofStep の matching

## Phase 5-16：PremisePattern と ProofStep の最小 matching 基盤

Phase 5-15 では、
`InferenceRule` が要求する premise の条件を表すため、

```text
PremisePattern
```

を導入した。

これにより、

```text
proof_rule
statement_type
relation_type
```

を用いて、

```text
その inference rule が
どのような ProofStep を premise として期待するか
```

を構造化して記述できるようになった。

ただし Phase 5-15 では、
PremisePattern は rule specification を保持するだけであり、

```text
PremisePattern
+
ProofStep
↓
match / no match
```

という実際の一致判定は行っていなかった。

Phase 5-16 では、
この最小 matching 基盤として、

```text
matches_premise_pattern()
```

を導入する。

---

## matches_premise_pattern() の設計

`matches_premise_pattern()` は、

```text
PremisePattern
ProofStep
```

を受け取り、

```text
True
False
```

を返す。

基本形は、

```python
matches_premise_pattern(
  pattern,
  step,
)
```

とする。

この関数の責務は、

```text
1つの PremisePattern
```

と、

```text
1つの ProofStep
```

の一致判定だけとする。

Phase 5-16 ではまだ、

```text
InferenceRule 全体の applicability
複数 premise の割り当て
premise の自動検索
```

などは扱わない。

---

## 空の PremisePattern

すべての条件が `None` である、

```python
PremisePattern()
```

は、
任意の ProofStep に一致するものとする。

つまり、

```text
proof_rule = None
statement_type = None
relation_type = None
```

は、

```text
その条件について制約を設けない
```

という意味になる。

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

は、

```text
True
```

となる。

この意味論により、
PremisePattern の optional field が、

```text
未指定
=
wildcard
```

として機能する。

---

## proof_rule の matching

`PremisePattern.proof_rule` が指定されている場合、

```text
step.rule
```

との一致を要求する。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.GIVEN,
)
```

は、

```text
ProofRule.GIVEN
```

を持つ ProofStep に一致する。

一方、

```text
ProofRule.RELATION
```

など異なる rule を持つ ProofStep には一致しない。

判定は、

```text
step.rule == pattern.proof_rule
```

を基準とする。

`proof_rule` が `None` の場合は、
ProofStep の rule を条件にしない。

---

## statement_type の matching

`PremisePattern.statement_type` が指定されている場合、

```text
step.conclusion
```

がその型であることを要求する。

例えば、

```python
PremisePattern(
  statement_type=Relation,
)
```

は、

```text
conclusion が Relation
```

である ProofStep に一致する。

判定には、

```python
isinstance(
  step.conclusion,
  pattern.statement_type,
)
```

を使用する。

したがって、
単純な型の完全一致ではなく、
Python の `isinstance()` の意味論に従う。

`statement_type` が `None` の場合は、
conclusion の型を条件にしない。

---

## relation_type の matching

`PremisePattern.relation_type` が指定されている場合、

```text
step.conclusion
```

が `Relation` であり、
さらに、

```text
step.conclusion.relation_type
```

が指定された RelationType と一致することを要求する。

例えば、

```python
PremisePattern(
  relation_type=RelationType.ZERO,
)
```

は、

```text
conclusion が Relation
+
RelationType.ZERO
```

である ProofStep に一致する。

RelationType が異なる場合は一致しない。

また、

```text
relation_type
```

が指定されていても、

```text
step.conclusion
```

が Relation でなければ、
一致しない。

つまり、

```text
relation_type を指定する
```

こと自体が暗黙に、

```text
conclusion は Relation である
```

という条件を含む。

---

## relation_type と statement_type の関係

例えば、

```python
PremisePattern(
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

では、

```text
conclusion が Relation
```

という条件と、

```text
その Relation が ZERO type
```

という条件の両方を検証する。

一方、

```python
PremisePattern(
  relation_type=RelationType.ZERO,
)
```

だけでも、
relation_type の判定時に conclusion が Relation であることを確認する。

したがって、

```text
statement_type=Relation
```

の明示は必須ではない。

ただし InferenceRule の specification を
人間が読む際の明確さを重視する場合には、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

のように、
要求条件を明示的にすべて記述できる。

---

## 複数条件は AND として扱う

PremisePattern に複数の条件が指定されている場合、
すべての条件を満たしたときだけ一致する。

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
step.rule == ProofRule.RELATION
AND
step.conclusion is Relation
AND
step.conclusion.relation_type == RelationType.ZERO
```

を要求する。

このうち1つでも満たさない場合は、

```text
False
```

を返す。

したがって PremisePattern は、

```text
指定された条件の conjunction
```

として解釈する。

---

## matching の判定順序

Phase 5-16 の実装では、
概念的に次の順序で条件を確認する。

```text
proof_rule
↓
statement_type
↓
relation_type
```

条件に一致しないことが判明した時点で、

```text
False
```

を返す。

すべての指定条件を通過した場合に、

```text
True
```

を返す。

ただしこの順序自体を
数学的意味として外部 API に依存させない。

matching の意味はあくまで、

```text
指定されたすべての条件を満たすか
```

である。

---

## 型検証

`matches_premise_pattern()` は、
入力型を明示的に検証する。

第1引数は、

```text
PremisePattern
```

でなければならない。

それ以外を渡した場合は、

```text
TypeError
```

とする。

同様に第2引数は、

```text
ProofStep
```

でなければならない。

それ以外を渡した場合も、

```text
TypeError
```

とする。

これにより、

```text
match しない
```

という数学的・論理的な結果と、

```text
API の利用方法自体が不正
```

というプログラム上のエラーを区別する。

---

## False と TypeError の区別

Phase 5-16 では、

```text
正しい型の pattern と step を比較した結果、
条件が一致しない
```

場合は、

```text
False
```

とする。

一方、

```text
pattern 自体が PremisePattern ではない
step 自体が ProofStep ではない
```

場合は、

```text
TypeError
```

とする。

例えば、

```python
matches_premise_pattern(
  PremisePattern(
    proof_rule=ProofRule.RELATION,
  ),
  given_step,
)
```

で `given_step.rule` が `ProofRule.GIVEN` なら、

```text
False
```

となる。

一方、

```python
matches_premise_pattern(
  "invalid",
  given_step,
)
```

は、

```text
TypeError
```

となる。

この区別により、
matching failure と API misuse を明確に分離する。

---

## InferenceRule との位置づけ

Phase 5-16 で追加するのは、

```text
PremisePattern
+
ProofStep
↓
match / no match
```

という1対1の判定だけである。

まだ、

```text
InferenceRule.premise_patterns
+
複数 ProofStep
↓
rule applicable / not applicable
```

という判定は行わない。

例えば、

```python
rule = InferenceRule(
  name="combined rule",
  premise_patterns=(
    pattern1,
    pattern2,
  ),
)
```

があっても、

```text
2つの pattern に対して
どの ProofStep を対応させるか
```

を自動判定する機能は Phase 5-16 には含めない。

Phase 5-16 で得られるのは、
その後の applicability 判定を実装するための
最小 primitive である。

---

## premise_patterns の順序問題はまだ扱わない

Phase 5-15 では、

```text
InferenceRule.premise_patterns
```

を tuple として保持した。

Phase 5-16 では、
1つの PremisePattern と
1つの ProofStep の matching のみを扱うため、

```text
pattern1 ↔ step1
pattern2 ↔ step2
```

のように、
複数 pattern と複数 step を
位置対応させるかどうかはまだ決めない。

今後 applicability 判定を導入する段階で、

```text
順序付き matching
順序なし matching
重複利用の可否
1つの step が複数 pattern を満たせるか
```

などを整理する。

---

## Expression 内部の matching はまだ行わない

Phase 5-16 で判定する条件は、

```text
proof_rule
statement_type
relation_type
```

だけである。

例えば、

```text
2η_3 = 0
```

と、

```text
3ν_4 = 0
```

は、
どちらも、

```text
ProofRule.RELATION
Relation
RelationType.ZERO
```

であれば、
同じ PremisePattern に一致し得る。

まだ、

```text
lhs が Multiple か
rhs が Zero か
coefficient が何か
expression が何か
```

などは判定しない。

したがって、

```text
mα = 0
```

という数学的 pattern そのものを
認識できる段階ではない。

---

## pattern variable と binding はまだ行わない

Phase 5-16 では、

```text
m
α
β
n
```

などを pattern variable として扱わない。

したがって、

```text
mα = 0
↓
ord(α) divides m
```

という rule について、

```text
m = 2
α = η_3
```

のような binding を生成することはできない。

Phase 5-16 の matching は、

```text
ProofStep レベルの粗い分類条件
```

だけを扱う。

Expression-level matching、
変数束縛、
unification、
substitution は後続フェーズへ分離する。

---

## RelationRepository との接続はまだ行わない

Phase 5-16 では、

```text
RelationRepository
```

から PremisePattern に一致する Relation を
自動取得する機能は追加しない。

現在の責務は、

```text
RelationRepository
= Relation の保存・基本検索

PremisePattern
= premise requirement の specification

matches_premise_pattern()
= ProofStep との1対1 matching
```

とする。

将来的には、

```text
InferenceRule
↓
PremisePattern
↓
existing ProofSteps / RelationRepository
↓
candidate premises
```

という自動選択機構を構築できる。

---

## Phase 5-16 時点の matching pipeline

Phase 5-16 により、

```text
InferenceRule
       │
       ↓
PremisePattern
       │
       │
       ├──────────────┐
       │              │
       ↓              ↓
pattern condition   ProofStep
       │              │
       └──────┬───────┘
              ↓
matches_premise_pattern()
              ↓
         True / False
```

という最小 matching 経路が成立した。

Phase 5-15 まででは、

```text
rule が何を要求するか
```

を記述できるだけだった。

Phase 5-16 ではさらに、

```text
実際の ProofStep が
その要求を満たしているか
```

を機械的に判定できるようになった。

---

## rule specification と matching の分離

現在の責務は、

```text
PremisePattern
= 条件のデータ表現

matches_premise_pattern()
= 条件と ProofStep の照合
```

として分離する。

PremisePattern 自体に、

```text
matches()
```

などの振る舞いを持たせず、
matching は独立した関数として実装する。

これにより、
pattern のデータモデルと
matching algorithm を分離した状態を維持する。

今後 Expression pattern や binding を導入した際にも、
PremisePattern の役割と
matching engine の役割を整理しやすくする。

---

## Phase 5-16 ではまだ行わないこと

Phase 5-16 では、以下は実装しない。

```text
InferenceRule 全体の applicability 判定
複数 PremisePattern と複数 ProofStep の対応付け
premise の順序・順序なし matching の決定
既存 ProofStep からの自動 premise 選択
RelationRepository からの自動 relation 選択
Expression 内部の pattern matching
Multiple / Zero 等の構造 pattern
pattern variable
変数束縛
binding environment
unification
substitution
conclusion の自動生成
InferenceRule.apply()
InferenceRule repository
proof の自動構築
Proof DAG の自動構築
```

まず、

```text
1 pattern
+
1 ProofStep
↓
match / no match
```

という最小 primitive を安定させる。

---

## Phase 5-16 時点の設計原則

1. `PremisePattern` と `ProofStep` の一致を機械的に判定できる。
2. 一致判定は `matches_premise_pattern()` に分離する。
3. `PremisePattern()` の未指定条件は wildcard として扱う。
4. `proof_rule` が指定されている場合は `ProofStep.rule` と一致する必要がある。
5. `statement_type` が指定されている場合は `isinstance()` によって conclusion の型を判定する。
6. `relation_type` が指定されている場合は conclusion が Relation でなければならない。
7. `relation_type` が指定されている場合は RelationType も一致する必要がある。
8. 複数の指定条件は AND 条件として扱う。
9. 条件不一致は `False` とする。
10. pattern または step の入力型が不正な場合は `TypeError` とする。
11. matching failure と API misuse を区別する。
12. PremisePattern は specification、matching 関数は照合処理として責務を分離する。
13. Phase 5-16 では1つの pattern と1つの ProofStep の matching のみを扱う。
14. InferenceRule 全体の applicability 判定はまだ行わない。
15. 複数 pattern と複数 premise の割り当てはまだ行わない。
16. Expression 内部の pattern matching はまだ行わない。
17. pattern variable や変数束縛はまだ導入しない。
18. conclusion の自動生成はまだ行わない。
19. RelationRepository からの自動 premise 選択はまだ行わない。
20. algebra 層には matching の概念を持ち込まない。
21. 次段階では `InferenceRule.premise_patterns` と実際の複数 ProofStep を用いた applicability 判定を検討する。


# InferenceRule 全体の premise matching

## Phase 5-17：InferenceRule.premise_patterns と複数 ProofStep の適合判定

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

という、
1つの premise pattern と1つの ProofStep の
最小 matching 基盤を導入した。

これにより、

```text
proof_rule
statement_type
relation_type
```

という ProofStep レベルの条件について、
実際の ProofStep が pattern を満たすかを
機械的に判定できるようになった。

Phase 5-17 では、
この個別 matching を組み合わせ、

```text
InferenceRule.premise_patterns
+
複数の ProofStep
↓
rule 全体として match / no match
```

を判定する最小基盤を導入する。

---

## matches_inference_rule() の設計

InferenceRule 全体の premise matching を行うため、

```text
matches_inference_rule()
```

を導入する。

基本形は、

```python
matches_inference_rule(
  inference_rule,
  steps,
)
```

とする。

入力は、

```text
InferenceRule
ProofStep または ProofStep の tuple / list
```

であり、

```text
True
False
```

を返す。

この関数は、

```text
InferenceRule.premise_patterns
```

と、

```text
実際に与えられた ProofStep 列
```

を比較する。

---

## ProofStep 入力の正規化

`steps` には、

```text
単一の ProofStep
```

または、

```text
tuple / list of ProofStep
```

を受け取れる。

内部では既存の、

```text
_normalize_proof_steps()
```

を利用し、

```text
tuple[ProofStep, ...]
```

へ統一する。

これにより、

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

新しい normalize mechanism は追加せず、
Phase 5-13 で導入した既存 helper を再利用する。

---

## premise pattern と ProofStep は位置対応とする

Phase 5-17 では、

```text
InferenceRule.premise_patterns
```

と、

```text
steps
```

を順序付きで対応させる。

つまり、

```text
premise_patterns[0] ↔ steps[0]
premise_patterns[1] ↔ steps[1]
premise_patterns[2] ↔ steps[2]
...
```

とする。

例えば、

```text
patterns:

1. RELATION
2. GIVEN
```

に対して、

```text
steps:

1. RELATION
2. GIVEN
```

なら match する。

一方、

```text
steps:

1. GIVEN
2. RELATION
```

では match しない。

したがって Phase 5-17 では、
premise pattern の tuple 順序に意味を持たせる。

---

## 順序付き matching を採用する理由

一般には、

```text
複数 pattern
+
複数 ProofStep
```

について、
順序を無視した matching を考えることもできる。

しかし順序なし matching を導入すると、

```text
どの step をどの pattern に割り当てるか
1つの step を複数 pattern に利用できるか
複数の割り当て候補をどう扱うか
```

などの問題が生じる。

Phase 5-17 では、
InferenceRule matching の最小基盤を構築することを優先し、

```text
pattern と step は位置対応
```

という単純で明確な意味論を採用する。

より柔軟な premise search / assignment は、
自動 inference を実装する後続フェーズで検討する。

---

## premise 数は完全一致を要求する

Phase 5-17 では、

```text
len(inference_rule.premise_patterns)
```

と、

```text
len(steps)
```

が一致することを要求する。

数が異なる場合は、

```text
False
```

を返す。

したがって、

```text
必要な premise より少ない
```

場合だけでなく、

```text
余分な ProofStep が存在する
```

場合も match しない。

例えば、

```text
pattern 数 = 2
step 数 = 1
```

は `False`。

同様に、

```text
pattern 数 = 1
step 数 = 2
```

も `False` とする。

この段階では、

```text
rule が要求する premises
```

と、

```text
rule 適用に渡された ProofSteps
```

が完全に対応することを要求する。

---

## 各 premise の判定

pattern 数と step 数が一致した場合、
対応する各組について、

```text
matches_premise_pattern()
```

を利用する。

概念的には、

```text
pattern 1 ↔ step 1
pattern 2 ↔ step 2
...
```

について、

```text
すべて match
```

した場合のみ、

```text
True
```

を返す。

1組でも match しなければ、

```text
False
```

となる。

実装上は、

```python
all(
  matches_premise_pattern(
    pattern,
    step,
  )
  for pattern, step in zip(
    patterns,
    normalized_steps,
  )
)
```

という構造になる。

したがって Phase 5-16 の
個別 matching logic を重複して実装しない。

---

## 空の premise_patterns

InferenceRule の、

```text
premise_patterns = ()
```

は、

```text
premise を必要としない rule
```

として解釈する。

したがって、

```text
premise_patterns = ()
steps = ()
```

なら、

```text
True
```

となる。

一方、

```text
premise_patterns = ()
steps = (some_step,)
```

なら、

```text
False
```

となる。

これは、

```text
pattern 数と step 数の完全一致
```

という一般ルールの自然な結果である。

---

## 不正な inference_rule

`matches_inference_rule()` の第1引数は、

```text
InferenceRule
```

でなければならない。

文字列などの不正な型を渡した場合は、

```text
TypeError
```

とする。

これは、

```text
rule が premises に適合しない
```

という論理的結果と、

```text
API に渡した値そのものが不正
```

というプログラム上のエラーを区別するためである。

---

## 不正な steps

`steps` は、

```text
ProofStep
```

または、

```text
tuple / list of ProofStep
```

でなければならない。

不正な型を直接渡した場合や、

```text
tuple / list
```

内部に ProofStep 以外の値が含まれている場合は、

```text
TypeError
```

とする。

この検証には既存の、

```text
_normalize_proof_steps()
```

を利用する。

---

## matches_premise_pattern() との責務分離

Phase 5-17 時点では、

```text
matches_premise_pattern()
```

と、

```text
matches_inference_rule()
```

を明確に分離する。

```text
matches_premise_pattern()
= 1 pattern と 1 ProofStep の matching
```

であり、

```text
matches_inference_rule()
= InferenceRule 全体と ProofStep 列の matching
```

である。

後者は前者を組み合わせて使用する。

これにより matching logic の重複を避け、
各層の責務を明確にする。

---

## matching と applicability の境界

Phase 5-17 の `matches_inference_rule()` は、

```text
指定された ProofStep 列が
InferenceRule.premise_patterns に一致するか
```

を判定する。

一方、

```text
手元に存在する多数の ProofStep の中から
rule を適用できる組を自動的に探す
```

ことはまだ行わない。

したがって現段階では、

```text
matching
```

と、

```text
candidate premise search
```

を別の責務とする。

例えば、

```text
existing steps
=
step A
step B
step C
step D
```

から、

```text
rule の pattern に合う
step B と step D を自動選択する
```

ような処理は Phase 5-17 には含まれない。

---

## Expression pattern はまだ扱わない

InferenceRule 全体を matching できるようになったが、
個々の PremisePattern が判定できる条件は引き続き、

```text
proof_rule
statement_type
relation_type
```

だけである。

例えば、

```text
2η_3 = 0
```

という Relation と、

```text
3ν_4 = 0
```

という Relation は、
どちらも、

```text
ProofRule.RELATION
Relation
RelationType.ZERO
```

という pattern に一致し得る。

まだ、

```text
mα = 0
```

という Expression 内部の一般 pattern を認識したり、

```text
m = 2
α = η_3
```

のような変数束縛を行うことはできない。

---

## Phase 5-17 時点の matching pipeline

現在、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

という個別 matching の上に、

```text
InferenceRule
│
└── premise_patterns
      │
      ├── pattern 1
      ├── pattern 2
      └── ...
             +
      ProofStep sequence
             ↓
matches_inference_rule()
             ↓
        True / False
```

という rule-level matching が成立した。

これにより、

```text
rule requirement の記述
```

だけでなく、

```text
実際に与えられた premises が
その rule requirement 全体を満たすか
```

まで機械的に判定できるようになった。

---

## Phase 5-17 ではまだ行わないこと

Phase 5-17 では以下は実装しない。

```text
順序なし premise matching
pattern と step の組合せ探索
candidate ProofStep の自動検索
1つの step の複数 pattern への割り当て
RelationRepository からの自動 relation 選択
InferenceRule の自動選択
Expression-level pattern matching
pattern variable
変数束縛
binding environment
unification
substitution
conclusion の自動生成
InferenceRule.apply()
proof の自動構築
Proof DAG の自動構築
```

まず、

```text
rule specification
+
明示的に与えられた premises
↓
match / no match
```

までを安定した primitive とする。

---

## Phase 5-17 時点の設計原則

1. `InferenceRule.premise_patterns` 全体と複数 ProofStep を比較できる。
2. rule-level matching は `matches_inference_rule()` に分離する。
3. 単一 ProofStep と tuple / list の両方を入力できる。
4. ProofStep 入力は既存 `_normalize_proof_steps()` で正規化する。
5. premise pattern と ProofStep は位置ごとに対応させる。
6. premise matching は順序付きとする。
7. pattern 数と step 数は完全一致を要求する。
8. premise が不足している場合は `False` とする。
9. premise が余分にある場合も `False` とする。
10. 各 pattern / step の判定には `matches_premise_pattern()` を再利用する。
11. すべての pattern / step が一致した場合のみ `True` とする。
12. 空の premise_patterns は空の steps にのみ一致する。
13. 不正な InferenceRule は `TypeError` とする。
14. 不正な ProofStep 入力は `TypeError` とする。
15. matching failure と API misuse を区別する。
16. rule matching と candidate premise search を分離する。
17. 順序なし matching はまだ導入しない。
18. Expression-level matching はまだ導入しない。
19. pattern variable や変数束縛はまだ導入しない。
20. conclusion の自動生成はまだ行わない。
21. algebra 層には inference matching の概念を持ち込まない。
22. 次段階では、既存 ProofStep 集合から InferenceRule に適合する premise 候補を探索する仕組みを検討する。


# InferenceRule に対する premise candidate search

## Phase 5-18：既存 ProofStep 集合から matching premise を探索する

Phase 5-17 では、

```text
InferenceRule.premise_patterns
+
明示的に与えられた ProofStep 列
↓
matches_inference_rule()
↓
True / False
```

という rule-level matching を導入した。

これにより、

```text
この ProofStep 列を
この InferenceRule の premises として
使用できるか
```

を機械的に判定できるようになった。

ただし Phase 5-17 では、
使用する ProofStep 自体は呼び出し側が
明示的に選択する必要があった。

Phase 5-18 では一段階進めて、

```text
InferenceRule
+
利用可能な ProofStep 集合
↓
premise_patterns に適合する ProofStep を探索
↓
matching premise sequence
```

という最小 premise search を導入する。

---

## find_matching_premises() の設計

InferenceRule が要求する premises を、
既存の ProofStep 集合から探索するため、

```text
find_matching_premises()
```

を導入する。

基本形は、

```python
find_matching_premises(
  inference_rule,
  available_steps,
)
```

とする。

入力は、

```text
InferenceRule
ProofStep または ProofStep の tuple / list
```

である。

適合する premises が見つかった場合は、

```text
tuple[ProofStep, ...]
```

を返す。

必要な premise をすべて見つけられない場合は、

```text
None
```

を返す。

これにより、

```text
match の成否だけを判定する
```

`matches_inference_rule()` と、

```text
実際に使用可能な premise を探索する
```

`find_matching_premises()` の責務を分離する。

---

## available_steps の正規化

`available_steps` は、

```text
単一 ProofStep
tuple of ProofStep
list of ProofStep
```

を受け取る。

内部では既存の、

```text
_normalize_proof_steps()
```

を利用し、

```text
tuple[ProofStep, ...]
```

へ正規化する。

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

を同じ入力モデルで扱える。

不正な型が与えられた場合は、
既存の ProofStep 正規化ルールに従って
`TypeError` とする。

---

## premise pattern の順序に従った探索

Phase 5-18 では、

```text
InferenceRule.premise_patterns
```

の順序に従って premise を探索する。

例えば、

```text
pattern 1 = RELATION
pattern 2 = GIVEN
```

であり、
利用可能な step が、

```text
step A = GIVEN
step B = RELATION
```

という順序で保持されていても、

```text
pattern 1
↓
step B

pattern 2
↓
step A
```

という対応を探索できる。

したがって Phase 5-17 の、

```text
明示的な ProofStep 列に対する
position-based matching
```

とは異なり、

Phase 5-18 の premise search では、

```text
available_steps の位置
```

と、

```text
premise_patterns の位置
```

を直接対応させない。

各 pattern ごとに、
利用可能な ProofStep 全体から候補を探索する。

ただし、

```text
どの pattern を先に処理するか
```

については、
`premise_patterns` の順序を維持する。

---

## 最初に一致する ProofStep を採用する

Phase 5-18 の最小実装では、
1つの premise pattern に対して
複数の ProofStep が一致する場合、

```text
available_steps の中で
最初に一致した ProofStep
```

を採用する。

例えば、

```text
pattern = GIVEN
```

に対して、

```text
step 1 = GIVEN
step 2 = GIVEN
```

の両方が一致する場合は、

```text
step 1
```

を選択する。

現段階では、

```text
すべての候補を返す
全組合せを列挙する
最適な premise を選ぶ
backtracking する
```

といった処理は行わない。

探索結果を決定的かつ単純にするため、

```text
first match
```

を採用する。

---

## 同じ ProofStep を複数 premise に再利用しない

1つの ProofStep は、
同じ `find_matching_premises()` 呼び出し内で
複数の premise pattern に再利用しない。

例えば、

```text
pattern 1 = GIVEN
pattern 2 = GIVEN
```

という rule に対して、
利用可能な ProofStep が、

```text
step A = GIVEN
```

1つしかない場合、

```text
step A
```

を2つの pattern の両方へ割り当てることはしない。

この場合、

```text
find_matching_premises(...)
```

は、

```text
None
```

を返す。

一方、

```text
step A = GIVEN
step B = GIVEN
```

という2つの異なる ProofStep が存在すれば、

```text
(
  step A,
  step B,
)
```

を返す。

このため実装では、
既に利用した ProofStep の index を記録し、
後続 pattern の探索対象から除外する。

---

## ProofStep の識別

Phase 5-18 では、
同じ ProofStep を再利用したかどうかを、

```text
available_steps 内の index
```

によって管理する。

これは、

```text
ProofStep の structural equality
```

と、

```text
premise candidate としての個々の出現
```

を不用意に混同しないためである。

探索中に使用済みとなった
`available_steps[index]` は、
後続 pattern では利用しない。

現段階では ProofStep に
専用 ID を導入しない。

ProofStep identity や proof graph node identity が
必要になった段階で、
別途設計を検討する。

---

## pattern matching 自体は既存機能を再利用する

各 pattern と ProofStep の一致判定には、
Phase 5-16 で導入した、

```text
matches_premise_pattern()
```

をそのまま利用する。

したがって現在の premise search が利用する条件は、

```text
proof_rule
statement_type
relation_type
```

のみである。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

に対しては、

```text
ProofRule.RELATION
+
conclusion が Relation
+
RelationType.ZERO
```

をすべて満たす ProofStep を探索する。

Phase 5-18 では、
新しい matching semantics を
`find_matching_premises()` 内に重複実装しない。

```text
PremisePattern
↓
matches_premise_pattern()
```

を個別判定の唯一の基盤として再利用する。

---

## 一部だけ見つかった場合

複数 premise を要求する rule について、
途中まで適合する ProofStep が見つかっても、
すべての premise pattern を満たせなければ
探索全体を失敗とする。

例えば、

```text
pattern 1 = RELATION
pattern 2 = GIVEN
```

に対して、

```text
RELATION step
```

しか存在しない場合、

pattern 1 は満たせるが
pattern 2 は満たせない。

この場合、

```text
None
```

を返す。

部分的に見つかった premise tuple は返さない。

したがって返り値は、

```text
すべての premise が見つかった
→ tuple[ProofStep, ...]

少なくとも1つ不足した
→ None
```

とする。

---

## premise を必要としない rule

InferenceRule が、

```text
premise_patterns = ()
```

を持つ場合、
必要な premise は存在しない。

したがって、

```python
find_matching_premises(
  rule,
  available_steps,
)
```

は、
`available_steps` の内容に関係なく、

```text
()
```

を返す。

これは、

```text
premise を要求しない rule
```

に対して、

```text
premise search は成功しており、
選択された premise は0個である
```

ことを表す。

このため、

```text
()
```

と、

```text
None
```

は明確に区別する。

```text
()
= premise を必要とせず、探索成功

None
= 必要な premise を満たせず、探索失敗
```

とする。

---

## matches_inference_rule() との役割分担

Phase 5-18 時点では、

```text
matches_inference_rule()
```

と、

```text
find_matching_premises()
```

は異なる用途を持つ。

`matches_inference_rule()` は、

```text
InferenceRule
+
既に選択された ProofStep 列
↓
その列が rule 全体に適合するか
```

を判定する。

一方、

`find_matching_premises()` は、

```text
InferenceRule
+
利用可能な ProofStep 集合
↓
rule に利用できる ProofStep 列を探す
```

ための関数である。

概念的には、

```text
available ProofSteps
↓
find_matching_premises()
↓
selected premises
↓
matches_inference_rule()
```

という利用も可能である。

ただし Phase 5-18 では、
`find_matching_premises()` の結果に対して
自動的に inference を適用する機構はまだ導入しない。

---

## greedy search と backtracking の境界

Phase 5-18 の premise search は、
各 premise pattern について、

```text
未使用の available_steps を先頭から調べる
↓
最初に一致した step を採用する
↓
次の pattern へ進む
```

という greedy search とする。

例えば、
ある ProofStep が複数の pattern に一致し得る場合でも、
後の pattern のためにその step を残しておくべきかを考慮して
選択をやり直すことはしない。

したがって理論上、

```text
別の割り当てなら全 pattern を満たせる
```

場合でも、
最初の greedy 選択によって
`None` になる可能性は残る。

これは Phase 5-18 では意図的な制限とする。

一般的な premise assignment は、

```text
backtracking
candidate enumeration
unordered matching
constraint solving
```

などを必要とする可能性があるため、
後続フェーズとして分離する。

---

## RelationRepository とはまだ直接接続しない

Phase 5-18 で探索対象とするのは、

```text
既に ProofStep になっているオブジェクト
```

である。

したがって、

```text
RelationRepository
↓
Relation を検索
↓
relation_proof_step()
↓
premise candidate
```

という処理を
`find_matching_premises()` 自体が行うことはない。

RelationRepository からの relation 自動取得と、
ProofStep 集合内からの premise search は
別の責務として扱う。

将来的には、

```text
RelationRepository
+
existing ProofSteps
+
InferenceRule
↓
candidate facts
↓
premise search
```

という上位 inference engine を構築できるが、
Phase 5-18 ではまだ導入しない。

---

## Expression-level pattern matching はまだ行わない

Phase 5-18 の探索は、
Phase 5-16 以来の、

```text
proof_rule
statement_type
relation_type
```

だけを利用する。

例えば、

```text
RelationType.ZERO
```

を持つ relation を探すことはできる。

しかし、

```text
mα = 0
```

という Expression 内部構造を調べたり、

```text
m = 2
α = η_3
```

のように値を束縛したりすることはできない。

したがって、

```text
premise candidate search
```

と、

```text
expression pattern matching / unification
```

は引き続き分離する。

---

## Phase 5-18 時点の matching pipeline

現在の inference-rule matching 基盤は、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

から始まり、

```text
InferenceRule.premise_patterns
+
明示的 ProofStep 列
↓
matches_inference_rule()
↓
True / False
```

まで拡張されている。

Phase 5-18 ではさらに、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
matched ProofStep tuple
or
None
```

という探索経路が追加された。

これにより、

```text
rule requirement を記述する
↓
個別 step と比較する
↓
明示的 premise 列を検証する
↓
既存 step 集合から premise を探す
```

という段階的な matching 基盤が成立した。

---

## Phase 5-18 ではまだ行わないこと

Phase 5-18 では、
premise candidate search の最小実装だけを扱う。

まだ、

```text
すべての matching candidate の列挙
複数の premise assignment の列挙
backtracking
最適な premise assignment の選択
unordered rule matching
Expression pattern
pattern variable
variable binding
substitution
conclusion の自動生成
InferenceRule.apply()
RelationRepository からの自動 relation 検索
rule applicability の一括探索
複数 InferenceRule の自動選択
自動 inference
recursive proof construction
proof DAG construction
```

は行わない。

特に、

```text
find_matching_premises()
```

は、

```text
premise を見つける
```

ところまでを責務とし、

```text
その rule を実際に適用して
新しい ProofStep を作る
```

ところまでは担当しない。

---

## Phase 5-18 時点の設計原則

1. `find_matching_premises()` は既存 ProofStep 集合から rule の premise を探索する。
2. matching 条件自体は `matches_premise_pattern()` を再利用する。
3. `available_steps` は単一 ProofStep、tuple、list を受け付ける。
4. 入力は `_normalize_proof_steps()` で統一する。
5. premise pattern は `InferenceRule.premise_patterns` の順に処理する。
6. 各 pattern について available_steps の先頭から探索する。
7. 複数候補がある場合は最初に一致した ProofStep を採用する。
8. 同じ available step を複数 premise pattern に再利用しない。
9. 使用済み step は available_steps 内の index で管理する。
10. すべての pattern が満たされた場合のみ ProofStep tuple を返す。
11. 1つでも必要な premise が見つからなければ `None` を返す。
12. premise_patterns が空なら `()` を返す。
13. `()` は premise 不要の成功、`None` は探索失敗として区別する。
14. Phase 5-17 の `matches_inference_rule()` は明示的 premise 列の検証用として維持する。
15. Phase 5-18 の `find_matching_premises()` は available steps からの探索用とする。
16. premise search は greedy とし、backtracking はまだ行わない。
17. available_steps の順序は first-match selection に影響する。
18. RelationRepository から Relation を自動取得する処理はまだ行わない。
19. Expression 内部の pattern matching はまだ行わない。
20. pattern variable、変数束縛、substitution はまだ導入しない。
21. conclusion の自動生成はまだ行わない。
22. InferenceRule の自動適用はまだ行わない。
23. premise search と rule application の責務を分離する。
24. algebra 層には premise search の概念を持ち込まない。
25. 次段階では、premise search の結果を用いた inference-rule applicability または rule application への接続を検討する。


# InferenceRule の applicability 判定

## Phase 5-19：利用可能な ProofStep に対する InferenceRule の適用可能性

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

という premise search を導入した。

これにより、
InferenceRule が要求する premise を、
既存の ProofStep 集合から探索できるようになった。

Phase 5-19 では、
この premise search を利用して、

```text
この InferenceRule は
現在利用可能な ProofStep だけで
適用可能か
```

を直接判定するため、

```text
is_inference_rule_applicable()
```

を導入する。

---

## is_inference_rule_applicable() の設計

基本形は、

```python
is_inference_rule_applicable(
  inference_rule,
  available_steps,
)
```

とする。

返り値は、

```text
True
False
```

である。

内部では、

```python
find_matching_premises(
  inference_rule,
  available_steps,
)
```

を利用し、

```text
matching premises が存在する
→ True

matching premises が存在しない
→ False
```

と判定する。

実装上は、

```python
find_matching_premises(...) is not None
```

という条件に集約する。

---

## premise search への委譲

`is_inference_rule_applicable()` 自体には、

```text
PremisePattern の matching
ProofStep の探索
ProofStep の再利用判定
RelationType の検査
available_steps の正規化
```

などのロジックを持たせない。

これらはすべて Phase 5-18 までに実装した、

```text
matches_premise_pattern()
find_matching_premises()
_normalize_proof_steps()
```

へ委譲する。

したがって、

```text
matches_premise_pattern()
= 1つの pattern と1つの step の一致判定

matches_inference_rule()
= 明示的に与えた premise 列全体の一致判定

find_matching_premises()
= available steps から premise を探索

is_inference_rule_applicable()
= premise が探索可能かを真偽値として判定
```

という責務分離とする。

---

## applicability と premise search の区別

`find_matching_premises()` は、
実際に選択された ProofStep を必要とする場合に利用する。

例えば、

```python
premises = find_matching_premises(
  rule,
  available_steps,
)
```

によって、

```text
(
  relation_step,
  given_step,
)
```

のような具体的な premise sequence を取得できる。

一方、

```python
is_inference_rule_applicable(
  rule,
  available_steps,
)
```

は、

```text
その rule が使えるかどうか
```

だけを必要とする場合の API とする。

したがって、

```text
premise search
```

と、

```text
applicability query
```

を別の公開 API として保持する。

---

## premise を必要としない rule

InferenceRule が、

```text
premise_patterns = ()
```

を持つ場合、

```text
find_matching_premises()
```

は、

```text
()
```

を返す。

`()` は `None` ではないため、

```python
is_inference_rule_applicable(
  rule,
  available_steps,
)
```

は、

```text
True
```

となる。

つまり、

```text
premise を必要としない rule
```

は常に premise requirement を満たしているとみなす。

これは、

```text
()
= premise 不要の探索成功

None
= 必要な premise の探索失敗
```

という Phase 5-18 の設計と整合する。

---

## available_steps の順序と applicability

Phase 5-19 の applicability は、
Phase 5-18 の `find_matching_premises()` の探索結果に依存する。

現在の premise search は、

```text
premise_patterns の順に処理
+
available_steps の先頭から検索
+
最初に一致した未使用 step を採用
```

という greedy search である。

したがって applicability も、
現在の greedy search semantics に基づいて判定される。

一般的な意味で、

```text
何らかの premise assignment が存在するか
```

を完全に探索する判定ではまだない。

例えば、
最初の greedy assignment が後続 pattern を妨げる場合、
別の assignment が理論上存在していても
現在の `find_matching_premises()` が `None` を返す可能性がある。

その場合、

```text
is_inference_rule_applicable()
```

も `False` となる。

この制限は Phase 5-19 では意図的に維持する。

backtracking や全 assignment の探索は
後続フェーズで扱う。

---

## step の再利用禁止との整合

Phase 5-18 と同様、
1つの available ProofStep は、
同じ rule の複数 premise pattern に再利用しない。

例えば、

```text
patterns:
  GIVEN
  GIVEN
```

に対して、

```text
available:
  GIVEN step A
```

しかない場合、

```text
find_matching_premises()
→ None
```

となるため、

```text
is_inference_rule_applicable()
→ False
```

となる。

一方、

```text
available:
  GIVEN step A
  GIVEN step B
```

なら、

```text
is_inference_rule_applicable()
→ True
```

となる。

したがって applicability は、
単なる各 pattern の独立存在判定ではなく、

```text
異なる ProofStep を割り当てられるか
```

という現在の premise search の条件を反映する。

---

## RelationType を利用する applicability

PremisePattern が、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

のような条件を持つ場合、

```text
ZERO Relation
```

を conclusion とする適切な ProofStep が
available_steps に存在するときだけ、
rule は applicable となる。

例えば、

```text
EQUALITY relation
ZERO relation
```

が available_steps に存在すれば、
ZERO relation が premise として選択されるため、

```text
is_inference_rule_applicable()
→ True
```

となる。

EQUALITY relation しか存在しない場合は、

```text
False
```

となる。

---

## input validation の責務

`is_inference_rule_applicable()` では
独自の型検証を追加しない。

不正な、

```text
inference_rule
available_steps
available_steps 内の要素
```

については、

```text
find_matching_premises()
↓
_normalize_proof_steps()
```

が既存の `TypeError` を発生させる。

これにより同じ validation logic の重複を避ける。

---

## applicability と rule application の分離

Phase 5-19 で導入するのは、

```text
InferenceRule が使えるか
```

という判定までである。

まだ、

```text
InferenceRule
+
matched premises
↓
new conclusion
```

という実際の rule application は行わない。

現在の InferenceRule は、

```text
name
description
premise_patterns
```

を保持するが、

```text
conclusion をどのように構成するか
```

という情報を持っていない。

例えば、

```text
mα = 0
↓
ord(α) divides m
```

を自動適用するには、

```text
m
α
```

を premise expression から取り出す必要がある。

これは、

```text
Expression pattern
pattern variable
variable binding
substitution
conclusion construction
```

などの機構を必要とする。

したがって、

```text
applicable
```

と、

```text
apply
```

は明確に分離する。

---

## Phase 5-19 時点の inference matching pipeline

現在は、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

から、

```text
InferenceRule
+
explicit ProofStep sequence
↓
matches_inference_rule()
↓
True / False
```

へ進み、

さらに、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
matched premises / None
```

という探索が可能になった。

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

という applicability query が追加された。

したがって現在の基盤は、

```text
rule requirement を記述
↓
個別 premise を検査
↓
明示的 premise sequence を検査
↓
available steps から premise を検索
↓
rule の applicability を判定
```

という段階まで進んだ。

---

## Phase 5-19 ではまだ行わないこと

Phase 5-19 では、
InferenceRule の applicability を
bool として取得するところまでとする。

まだ、

```text
複数 InferenceRule の一括 applicability 判定
applicable rule の検索
InferenceRule と matched premises の組の保持
InferenceMatch のような結果型
all premise assignments の列挙
backtracking premise search
unordered premise search
Expression pattern
pattern variable
variable binding
substitution
conclusion builder
InferenceRule.apply()
自動 inference
recursive proof construction
proof DAG construction
```

は行わない。

---

## Phase 5-19 時点の設計原則

1. `is_inference_rule_applicable()` は InferenceRule の適用可能性を bool で返す。
2. applicability は matching premises が存在するかによって判定する。
3. matching premise の探索は `find_matching_premises()` に委譲する。
4. PremisePattern matching を applicability 関数内で再実装しない。
5. ProofStep の正規化を applicability 関数内で再実装しない。
6. 型検証も既存 premise search に委譲する。
7. premise_patterns が空の rule は applicable とする。
8. `()` と `None` の意味を区別する。
9. ProofStep の再利用禁止は Phase 5-18 の仕様をそのまま継承する。
10. RelationType などの pattern 条件も既存 matcher の仕様を継承する。
11. applicability は現在の greedy premise search semantics に依存する。
12. applicability は完全な組合せ探索ではまだない。
13. applicability と actual rule application を分離する。
14. Phase 5-19 では conclusion を自動生成しない。
15. InferenceRule に conclusion builder はまだ持たせない。
16. Expression pattern matching はまだ導入しない。
17. pattern variable と variable binding はまだ導入しない。
18. algebra 層には applicability の概念を持ち込まない。
19. 次段階では複数の InferenceRule から applicable rule を検索する機構を検討する。


# 複数 InferenceRule から applicable rule を検索する

## Phase 5-20：InferenceRule collection の検索

Phase 5-19 までに、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
matched premises
```

および、

```text
InferenceRule
+
available ProofSteps
↓
is_inference_rule_applicable()
↓
True / False
```

という、
1つの inference rule に対する premise search と
applicability 判定が可能になった。

Phase 5-20 ではこれを一段上へ拡張し、

```text
複数の InferenceRule
+
available ProofSteps
↓
現在適用可能な rule の検索
```

を行えるようにする。

このため、

```python
find_applicable_inference_rules(
  inference_rules,
  available_steps,
)
```

を導入する。

---

## rule collection と available steps

`find_applicable_inference_rules()` は、

```text
inference_rules
available_steps
```

を受け取る。

`inference_rules` は、

```text
InferenceRule
```

単体、または、

```text
tuple/list of InferenceRule
```

を受け取れる。

`available_steps` は既存の premise search と同様に、

```text
ProofStep
```

単体、または、

```text
tuple/list of ProofStep
```

を受け取れる。

内部では両者を tuple に正規化した上で処理する。

---

## applicable rule の意味

各 `InferenceRule` について、

```python
is_inference_rule_applicable(
  inference_rule,
  available_steps,
)
```

を呼び出し、
結果が `True` の rule のみを返す。

したがって Phase 5-20 では、

```text
applicable
```

の定義を新しく重複実装しない。

applicability の判定責務は引き続き、

```text
find_matching_premises()
↓
is_inference_rule_applicable()
```

に置く。

`find_applicable_inference_rules()` は、
その判定を rule collection 全体へ適用する薄い検索層とする。

現在の流れは、

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

となる。

---

## 入力順の保持

`find_applicable_inference_rules()` は、
適用可能な rule を
入力された rule collection の順序のまま返す。

例えば、

```text
rules:
  rule A
  rule B
  rule C
```

のうち、

```text
rule A
rule C
```

が applicable なら、

```text
(
  rule A,
  rule C,
)
```

を返す。

rule の priority や score による並べ替えは行わない。

これは Phase 5-20 が、

```text
どの rule が利用可能か
```

を検索する段階であり、

```text
どの rule を優先して適用するか
```

を決定する段階ではないためである。

---

## 複数 applicable rule

同じ available steps に対して、
複数の rule が applicable であることを許容する。

例えば、

```text
available:
  GIVEN
```

に対して、

```text
rule A:
  GIVEN を要求

rule B:
  GIVEN を要求
```

であれば、

```python
find_applicable_inference_rules(
  (
    rule_a,
    rule_b,
  ),
  available_steps,
)
```

は、

```text
(
  rule_a,
  rule_b,
)
```

を返す。

Phase 5-20 では、
複数候補の中から1つを選択しない。

これは将来的な、

```text
rule priority
specificity
cost
proof strategy
search strategy
```

などとは別の責務とする。

---

## applicable rule が存在しない場合

どの rule も applicable でない場合は、

```text
()
```

を返す。

これはエラーではない。

例えば、

```text
available:
  GIVEN
```

しか存在せず、

```text
rules:
  RELATION を要求する rule
```

しか存在しない場合、

```python
find_applicable_inference_rules(...)
```

は、

```text
()
```

となる。

したがって、

```text
()
```

は、

```text
検索は正常に行われたが、
現在利用できる inference rule がない
```

ことを表す。

---

## 空の rule collection

```text
inference_rules = ()
```

も有効な入力とする。

この場合、
検索対象そのものがないため、

```text
()
```

を返す。

空 collection を特別なエラーとはしない。

これにより、
呼び出し側で rule collection が空かどうかを
事前に分岐する必要をなくす。

---

## premise-free rule

Phase 5-19 までの設計では、

```text
premise_patterns = ()
```

を持つ rule は、
premise を必要としないため常に applicable である。

この性質は Phase 5-20 でもそのまま維持する。

したがって、

```python
InferenceRule(
  name="no premise rule",
)
```

は available steps が空でも、

```python
find_applicable_inference_rules(
  rules,
  (),
)
```

の結果に含まれる。

これは `find_applicable_inference_rules()` が
独自に premise-free rule を特別扱いしているのではなく、

```text
is_inference_rule_applicable()
```

の既存仕様をそのまま利用した結果である。

---

## relation type を含む rule 検索

rule collection の検索でも、
既存の `PremisePattern` の条件はすべて維持される。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

を要求する rule は、

```text
RelationType.ZERO
```

の Relation を conclusion に持つ ProofStep が存在する場合だけ
applicable になる。

一方、

```text
RelationType.EQUALITY
```

のみが存在する場合は applicable にならない。

したがって Phase 5-20 では、
rule collection 検索のために
新しい pattern matching 規則は導入しない。

既存の、

```text
proof_rule
statement_type
relation_type
```

による判定をそのまま利用する。

---

## 複数 premise pattern を持つ rule

複数の premise pattern を持つ rule も、
そのまま collection search の対象になる。

例えば、

```text
rule A:
  RELATION
  GIVEN

rule B:
  GIVEN
```

があり、

```text
available:
  GIVEN
  RELATION
```

であれば、

```text
rule A
rule B
```

の両方が applicable になり得る。

各 rule の premise search は独立して行う。

ある rule が使用した ProofStep を、
別の rule の検索から除外することはしない。

つまり、

```text
used step
```

の概念は、
1つの `InferenceRule` 内で
複数 premise pattern に同じ step を再利用しないためのものであり、

```text
異なる rule 間
```

で ProofStep を消費する意味ではない。

---

## rule collection の正規化

Phase 5-20 では、
rule collection の入力形式を統一するため、

```python
_normalize_inference_rules()
```

を導入する。

単一の、

```text
InferenceRule
```

を受け取った場合は、

```text
(rule,)
```

へ正規化する。

tuple / list の場合は tuple に変換する。

また collection 内に、

```text
InferenceRule
```

以外の値が含まれている場合は
`TypeError` とする。

これにより、

```python
find_applicable_inference_rules(
  rule,
  step,
)
```

と、

```python
find_applicable_inference_rules(
  [rule],
  [step],
)
```

を同じ内部処理で扱える。

---

## 入力検証

Phase 5-20 では、
rule collection と available steps の双方について
早期に型を検証する。

不正な、

```text
inference_rules
```

には `TypeError` を返す。

また、

```text
tuple/list
```

の中に `InferenceRule` 以外が含まれる場合も
`TypeError` とする。

`available_steps` については、
既存の、

```python
_normalize_proof_steps()
```

を利用する。

したがって、

```text
ProofStep
tuple/list of ProofStep
```

以外の入力や、
collection 内の不正な要素は `TypeError` となる。

入力 validation の責務を
検索アルゴリズム本体と分離し、
rule search の本体を単純に保つ。

---

## Phase 5-20 では matched premises を返さない

`find_applicable_inference_rules()` の返り値は、

```text
tuple of InferenceRule
```

のみとする。

つまり、

```text
どの rule が applicable か
```

は分かるが、

```text
その rule が具体的にどの ProofStep を使って
applicable になったか
```

は返さない。

matched premises が必要な場合は現在、

```python
find_matching_premises(
  rule,
  available_steps,
)
```

を別途呼び出せる。

ただし将来的には、

```text
rule
+
matched premises
```

を1つの構造として返す方が便利になる。

例えば、

```python
InferenceMatch(
  inference_rule=rule,
  premises=matched_steps,
)
```

のような型を導入すれば、

```text
どの rule が applicable か
```

と、

```text
なぜ applicable なのか
```

を同時に保持できる。

Phase 5-20 ではそこまで進めず、
rule collection 検索そのものを独立して完成させる。

---

## greedy premise search の制限は維持される

`find_applicable_inference_rules()` は
内部で `is_inference_rule_applicable()` を利用する。

そのため、
Phase 5-18 / 5-19 から存在する
greedy premise search の制限もそのまま引き継ぐ。

現在の `find_matching_premises()` は、

```text
各 pattern について
available steps を先頭から検索
↓
最初に一致した未使用 step を選択
↓
次の pattern へ進む
```

という greedy algorithm である。

backtracking は行わない。

したがって Phase 5-20 における、

```text
applicable rule
```

も正確には、

```text
現在の greedy premise-search algorithm の下で
applicable と判定された rule
```

を意味する。

rule collection search を導入しても、
premise assignment search の完全性はまだ改善しない。

---

## rule search と rule application の分離

Phase 5-20 で実装するのは、

```text
どの rule が現在 applicable か
```

の検索までである。

まだ、

```text
rule を実際に適用する
conclusion を構築する
新しい ProofStep を生成する
available steps に追加する
次の rule を再検索する
```

ことは行わない。

したがって現在の inference pipeline は、

```text
InferenceRule definitions
+
available ProofSteps
↓
find applicable rules
```

までで止まる。

将来的な automatic inference では、

```text
find applicable rules
↓
choose rule
↓
obtain matched premises
↓
bind variables
↓
construct conclusion
↓
create ProofStep
↓
add to available facts
↓
repeat
```

という流れが必要になる。

Phase 5-20 は、
その最初の rule-discovery 部分を実装した段階である。

---

## Phase 5-20 時点の設計原則

1. 複数の `InferenceRule` から applicable rule を検索できる。
2. applicable 判定そのものは `is_inference_rule_applicable()` に委譲する。
3. premise search のロジックを rule collection search 内で重複実装しない。
4. applicable rule は入力順を維持して返す。
5. 複数の applicable rule をそのまま返す。
6. applicable rule が存在しない場合は空 tuple を返す。
7. 空の rule collection は有効な入力とする。
8. premise-free rule は既存仕様どおり applicable とする。
9. rule 間で ProofStep を消費する概念は導入しない。
10. `InferenceRule` 単体と tuple/list を同じ API で扱う。
11. rule collection の型検証は `_normalize_inference_rules()` に集約する。
12. available steps の検証には既存の `_normalize_proof_steps()` を再利用する。
13. Phase 5-20 では matched premises と rule を組にした構造はまだ導入しない。
14. Phase 5-20 では rule priority や rule selection strategy を導入しない。
15. 現在の applicability は greedy premise search の制限を引き継ぐ。
16. applicable-rule search と actual rule application を分離する。
17. expression-level matching や variable binding はまだ行わない。
18. algebra 層および EHP 層には変更を加えない。

---

## Phase 5-20 の到達点

Phase 5-20 により、
inference-rule matching の流れは、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
```

から始まり、

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

を経て、

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
proof engine が保持する複数の数学的 inference rule の中から、

```text
現在持っている事実だけで利用できる rule はどれか
```

を機械的に検索するための基盤ができた。

ただし現在返されるのは
`InferenceRule` 自体だけであり、

```text
rule
+
matched premises
```

を一体として保持する仕組みはまだない。

次の自然な拡張は、
applicable rule とその premise assignment を
構造化された検索結果として保持することである。


# InferenceMatch / structured inference match

## Phase 5-21：applicable rule と matched premises の構造化

Phase 5-20 までに、

```text
InferenceRule collection
+
available ProofSteps
↓
find_applicable_inference_rules()
↓
applicable InferenceRules
```

という rule collection search が可能になった。

これにより、

```text
現在どの inference rule が利用可能か
```

を検索できるようになった。

一方、`find_applicable_inference_rules()` が返すのは
`InferenceRule` 自体だけであり、

```text
その rule が
どの ProofStep を premise として利用して
applicable になったか
```

という情報は保持していなかった。

matched premises を取得するには、
applicable rule を取得した後に改めて、

```python
find_matching_premises(
  inference_rule,
  available_steps,
)
```

を呼び出す必要があった。

Phase 5-21 では、

```text
applicable InferenceRule
+
matched ProofSteps
```

を1つの構造として保持するため、

```text
InferenceMatch
```

を導入する。

---

## InferenceMatch の設計

`InferenceMatch` は、

```text
どの inference rule が利用可能か
```

と、

```text
その rule に対応して
どの premises が選択されたか
```

をまとめて保持する。

基本構造は、

```python
@dataclass(frozen=True)
class InferenceMatch:
  inference_rule: InferenceRule
  premises: tuple[ProofStep, ...]
```

とする。

概念的には、

```text
InferenceMatch
├── inference_rule
└── premises
```

である。

例えば、

```text
rule:
  RELATION
  GIVEN
```

という premise pattern を持つ rule があり、

```text
available:
  given_step
  relation_step
```

という ProofStep collection が存在する場合、

```text
InferenceMatch
├── inference_rule = rule
└── premises
    ├── relation_step
    └── given_step
```

という structured result を構築できる。

---

## premises の順序

`InferenceMatch.premises` は、

```text
available_steps の保存順
```

ではなく、

```text
InferenceRule.premise_patterns の順序
```

で保持する。

例えば、

```text
premise_patterns:
  RELATION
  GIVEN
```

に対して、

```text
available_steps:
  GIVEN
  RELATION
```

という順序で step が格納されていても、

```text
InferenceMatch.premises:
  relation_step
  given_step
```

となる。

この挙動は新しく実装するのではなく、
既存の、

```python
find_matching_premises()
```

の返却順をそのまま利用する。

したがって Phase 5-21 でも、
premise selection の意味論は
`find_matching_premises()` に集約する。

---

## find_inference_match()

1つの `InferenceRule` と
available ProofSteps から
structured match を取得するため、

```python
find_inference_match(
  inference_rule,
  available_steps,
)
```

を導入する。

基本的な処理は、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
matched premises / None
↓
InferenceMatch / None
```

となる。

実装上は、

```python
matched_premises = find_matching_premises(
  inference_rule,
  available_steps,
)
```

を利用し、

```text
matched_premises is None
```

なら、

```text
None
```

を返す。

premises が見つかった場合は、

```python
InferenceMatch(
  inference_rule=inference_rule,
  premises=matched_premises,
)
```

を返す。

---

## None と空 premises の区別

Phase 5-21 では、

```text
None
```

と、

```text
InferenceMatch(
  inference_rule=rule,
  premises=(),
)
```

を明確に区別する。

`None` は、

```text
必要な premises が見つからず、
rule が現在 applicable ではない
```

ことを表す。

一方、

```text
premise_patterns = ()
```

を持つ premise-free rule は、
premise を必要としないため正常に match する。

この場合、

```python
find_matching_premises(
  rule,
  available_steps,
)
```

は、

```text
()
```

を返す。

したがって、

```python
find_inference_match(
  rule,
  available_steps,
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

つまり、

```text
None
```

は match failure、

```text
InferenceMatch(..., premises=())
```

は premise-free rule の successful match

を意味する。

---

## find_inference_matches()

複数の `InferenceRule` について
structured match を検索するため、

```python
find_inference_matches(
  inference_rules,
  available_steps,
)
```

を導入する。

基本的な流れは、

```text
InferenceRule collection
+
available ProofSteps
↓
各 rule に find_inference_match()
↓
None を除外
↓
tuple[InferenceMatch, ...]
```

とする。

例えば、

```text
rules:
  rule A
  rule B
  rule C
```

について、

```text
rule A
rule C
```

だけが applicable なら、

```text
(
  InferenceMatch(
    inference_rule=rule_a,
    premises=(...),
  ),
  InferenceMatch(
    inference_rule=rule_c,
    premises=(...),
  ),
)
```

を返す。

これにより、

```text
どの rule が使えるか
```

だけでなく、

```text
その rule がどの premises を使うか
```

まで一度の検索で取得できる。

---

## rule collection の順序

`find_inference_matches()` は、
入力された `InferenceRule` collection の順序を維持する。

例えば、

```text
input:
  rule B
  rule A
```

の両方が match する場合、

```text
result:
  InferenceMatch(rule B, ...)
  InferenceMatch(rule A, ...)
```

となる。

Phase 5-21 では、

```text
priority
specificity
cost
proof strategy
```

などによる並べ替えは行わない。

structured match を導入しても、
rule selection policy は別の責務とする。

---

## 複数 rule 間での ProofStep の利用

`find_inference_matches()` では、
各 `InferenceRule` に対して
独立に premise search を行う。

したがって同じ ProofStep が、

```text
rule A の premise
```

と、

```text
rule B の premise
```

の両方に使われることは許容する。

`find_matching_premises()` における
step reuse prevention は、

```text
1つの InferenceRule の複数 premise pattern
```

に対して同じ ProofStep を重複利用しないためのものである。

異なる inference rule 間で
ProofStep を「消費」する概念は導入しない。

---

## relation type を含む structured match

既存の `PremisePattern` が持つ、

```text
proof_rule
statement_type
relation_type
```

の条件は、
`InferenceMatch` の検索でもそのまま利用される。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

を要求する rule は、

```text
RelationType.ZERO
```

を持つ Relation step が存在するときだけ match する。

その場合、

```text
InferenceMatch.premises
```

には実際に選ばれた zero relation step が格納される。

これにより Phase 5-20 の applicable-rule search よりも、

```text
どの条件を満たしたか
```

を具体的な ProofStep として保持できるようになった。

---

## 複数 premise pattern と InferenceMatch

複数 premise pattern を持つ rule についても、
`InferenceMatch` は対応するすべての matched steps を保持する。

例えば、

```text
premise_patterns:
  RELATION
  GIVEN
```

に対し、

```text
available_steps:
  given_step
  relation_step
```

が存在する場合、

```python
InferenceMatch(
  inference_rule=rule,
  premises=(
    relation_step,
    given_step,
  ),
)
```

となる。

1つでも必要な premise が見つからない場合、
`find_inference_match()` は `None` を返すため、
不完全な `InferenceMatch` は生成しない。

---

## input normalization の再利用

`find_inference_match()` は、
内部で `find_matching_premises()` を利用するため、

```text
InferenceRule の型検証
available ProofSteps の正規化
ProofStep collection の要素検証
```

も既存処理を利用する。

`find_inference_matches()` では、

```python
_normalize_inference_rules()
```

と、

```python
_normalize_proof_steps()
```

を利用する。

したがって、

```text
InferenceRule
tuple/list of InferenceRule
```

および、

```text
ProofStep
tuple/list of ProofStep
```

という既存入力仕様を維持する。

Phase 5-21 のために
新しい collection normalization 規則は導入しない。

---

## 既存 API との役割分担

Phase 5-21 では、
既存 API を置き換えない。

それぞれの責務は次のように分ける。

```text
matches_premise_pattern()
```

は、

```text
1つの PremisePattern と
1つの ProofStep が一致するか
```

を判定する。

```text
matches_inference_rule()
```

は、

```text
明示的に与えられた ProofStep sequence が
InferenceRule の premise patterns と一致するか
```

を判定する。

```text
find_matching_premises()
```

は、

```text
available ProofSteps から
必要な premises を検索する
```

ために使う。

```text
is_inference_rule_applicable()
```

は、

```text
rule が applicable か
```

という boolean query を提供する。

```text
find_applicable_inference_rules()
```

は、

```text
複数 rule のうち
どれが applicable か
```

を返す。

```text
find_inference_match()
```

は、

```text
1つの applicable rule
+
matched premises
```

を structured result として返す。

```text
find_inference_matches()
```

は、

```text
複数 rule
+
それぞれの matched premises
```

を structured result collection として返す。

用途に応じて
boolean、rule-only、structured match を
使い分けられる設計とする。

---

## InferenceMatch と ProofStep の違い

`InferenceMatch` はまだ推論結果そのものではない。

例えば、

```text
InferenceMatch
├── inference_rule
└── premises
```

は、

```text
この rule は
この premises を使って適用できる
```

ことを表すだけである。

一方 `ProofStep` は、

```text
premises
↓
rule
↓
conclusion
```

という実際の推論結果を表す。

したがって、

```text
InferenceMatch
≠
ProofStep
```

とする。

Phase 5-21 では、

```text
match を見つける
```

ところまでとし、

```text
match を適用して conclusion を生成する
```

ことは行わない。

---

## InferenceMatch と InferenceRule application の境界

将来的には、

```text
InferenceMatch
↓
rule application
↓
new ProofStep
```

という処理が必要になる。

しかしそのためには、

```text
premise の内部構造を調べる
pattern variable を bind する
conclusion template に substitute する
新しい conclusion を構築する
```

などの仕組みが必要になる。

現在の `PremisePattern` は、

```text
proof_rule
statement_type
relation_type
```

という粗い structural conditions だけを保持しており、

```text
mα = 0
```

のような expression-level pattern はまだ扱わない。

そのため Phase 5-21 では、
`InferenceMatch` を rule application から明確に分離する。

---

## greedy premise search の制限

`InferenceMatch` は、
既存の `find_matching_premises()` の結果を保持する。

したがって、
現在の greedy premise-search algorithm の制限も
そのまま引き継ぐ。

現在は、

```text
各 premise pattern
↓
available steps を先頭から走査
↓
最初の matching unused step を選択
↓
次の pattern
```

という処理であり、
backtracking は行わない。

したがって `InferenceMatch` は、

```text
現在の greedy search が選択した premise assignment
```

を表す。

すべての可能な premise assignment の中から
唯一の正しいものを表すわけではない。

将来的に alternative premise assignments や
backtracking search を導入する場合には、
`InferenceMatch` を複数生成する形へ拡張できる。

---

## Phase 5-21 時点の inference pipeline

Phase 5-21 の完了により、
現在の inference pipeline は、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

```text
InferenceRule
+
explicit ProofSteps
↓
matches_inference_rule()
↓
True / False
```

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
matched ProofSteps / None
```

```text
InferenceRule
+
available ProofSteps
↓
is_inference_rule_applicable()
↓
True / False
```

```text
InferenceRule collection
+
available ProofSteps
↓
find_applicable_inference_rules()
↓
applicable InferenceRules
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
tuple[InferenceMatch, ...]
```

となった。

rule matching の結果を、
単なる boolean や rule object だけでなく、

```text
rule
+
matched premises
```

という structured object として保持できる段階まで進んだ。

---

## Phase 5-21 時点の設計原則

1. applicable rule と matched premises を `InferenceMatch` として一体で保持する。
2. `InferenceMatch` は immutable な frozen dataclass とする。
3. `InferenceMatch.premises` は premise-pattern 順で保持する。
4. premise selection は `find_matching_premises()` に委譲する。
5. matching logic を `find_inference_match()` 内で重複実装しない。
6. match failure は `None` で表す。
7. premise-free rule の successful match は `InferenceMatch(..., premises=())` で表す。
8. `None` と空 premises を明確に区別する。
9. collection search は `find_inference_matches()` で行う。
10. collection search は inference-rule 入力順を維持する。
11. 複数 applicable rule の structured match をすべて返す。
12. 異なる rule 間で ProofStep を消費する概念は導入しない。
13. single / tuple / list input の既存仕様を維持する。
14. input normalization は既存 helper を再利用する。
15. `find_applicable_inference_rules()` は削除せず rule-only query として残す。
16. `InferenceMatch` と `ProofStep` を区別する。
17. Phase 5-21 では conclusion を自動生成しない。
18. Phase 5-21 では inference rule を実際に apply しない。
19. expression-level pattern matching や variable binding はまだ導入しない。
20. greedy premise-search の制限を明示的に維持する。
21. algebra / EHP 層には変更を加えない。

---

## Phase 5-21 の到達点

Phase 5-21 により、

```text
どの inference rule が使えるか
```

だけでなく、

```text
その inference rule が
どの ProofStep を premise として使えるか
```

まで機械的に取得できるようになった。

これは、

```text
rule discovery
```

から、

```text
rule application
```

へ進むための重要な中間表現となる。

現在は、

```text
available facts
+
InferenceRule collection
↓
InferenceMatch collection
```

まで構築できる。

次の段階では、

```text
InferenceMatch
↓
inference application
↓
new ProofStep
```

という流れを検討できる。

ただし実際の数学的な conclusion construction には、
expression-level patterns、
variable binding、
substitution などが必要になるため、
rule application の責務を段階的に設計する。


# InferenceRule の conclusion builder と rule application

## Phase 5-22：InferenceMatch から ProofStep を構築する最小 rule application

Phase 5-21 では、

```text
InferenceRule
+
available ProofSteps
↓
find_inference_match()
↓
InferenceMatch
```

という structured match を導入した。

`InferenceMatch` は、

```text
適用可能な InferenceRule
+
その rule に対応して選択された ProofStep
```

をまとめて保持する。

Phase 5-22 では、
この structured match を実際の推論結果へ変換するため、

```text
InferenceMatch
↓
rule application
↓
ProofStep
```

という最小 application layer を導入する。

---

## conclusion_builder の設計

`InferenceRule` に、

```text
conclusion_builder
```

を追加する。

基本構造は、

```python
@dataclass(frozen=True)
class InferenceRule:
  name: str
  description: str | None = None
  premise_patterns: tuple[PremisePattern, ...] = ()
  conclusion_builder: Any = None
```

とする。

`conclusion_builder` は、
matched premises を受け取り、
新しい conclusion を構築する callable とする。

概念的には、

```text
tuple of matched ProofSteps
↓
conclusion_builder
↓
conclusion
```

という責務を持つ。

例えば、

```python
def builder(premises):
  return (
    premises[0].conclusion,
    premises[1].conclusion,
  )
```

のように、
matched ProofStep の conclusion を利用して
新しい conclusion を構築できる。

---

## conclusion_builder を optional とする理由

`conclusion_builder` の default は、

```text
None
```

とする。

これは、
InferenceRule の、

```text
matching
```

と、

```text
application
```

を分離するためである。

InferenceRule は conclusion builder を持たなくても、

```text
matches_inference_rule()
find_matching_premises()
is_inference_rule_applicable()
find_applicable_inference_rules()
find_inference_match()
find_inference_matches()
```

に利用できる。

したがって、

```text
この rule が使えるかを調べる
```

段階では、
conclusion construction の仕様を要求しない。

一方、

```text
実際に rule を適用する
```

段階では、
conclusion を構築する方法が必要になる。

そのため、

```text
matching:
conclusion_builder 不要

application:
conclusion_builder 必須
```

という設計とする。

これにより、
Phase 5-21 以前に作成した InferenceRule との
後方互換性も維持する。

---

## apply_inference_match() の設計

InferenceMatch を実際の ProofStep へ変換するため、

```python
apply_inference_match(
  inference_match,
)
```

を導入する。

処理は、

```text
InferenceMatch
↓
InferenceRule を取得
↓
conclusion_builder を取得
↓
matched premises を builder に渡す
↓
conclusion を構築
↓
ProofStep を構築
```

とする。

返される ProofStep は概念的に、

```python
ProofStep(
  conclusion=conclusion,
  premises=inference_match.premises,
  rule=ProofRule.INFERENCE,
  inference_rule=inference_match.inference_rule,
)
```

となる。

---

## ProofRule.INFERENCE

Phase 5-22 では、
InferenceMatch を適用して生成された ProofStep を、

```text
ProofRule.INFERENCE
```

として記録する。

これにより、

```text
relation として与えられた既知事実
```

や、

```text
kernel / image computation
```

などと、

```text
InferenceRule を適用して新しく導いた結果
```

を区別できる。

また、
生成された ProofStep は、

```text
inference_rule
```

に実際に使用した `InferenceRule` を保持する。

したがって derived step から、

```text
どの rule で導かれたか
```

を追跡できる。

---

## matched premises をそのまま依存関係とする

`apply_inference_match()` によって生成される ProofStep の
`premises` には、

```text
InferenceMatch.premises
```

をそのまま設定する。

したがって、

```text
available ProofSteps
↓
matching
↓
InferenceMatch
↓
application
↓
derived ProofStep
```

と進んでも、
matching 時に選択された concrete ProofStep との
依存関係は失われない。

例えば、

```text
PremisePattern 1 = RELATION
PremisePattern 2 = GIVEN
```

に対し、
available steps が、

```text
given_step
relation_step
```

という順で保持されていても、
InferenceMatch は pattern order に従って、

```text
(
  relation_step,
  given_step,
)
```

を保持する。

application 後も derived ProofStep の premises は、

```text
(
  relation_step,
  given_step,
)
```

となる。

conclusion builder に渡される順序も同じである。

これにより、

```text
PremisePattern order
↓
InferenceMatch.premises order
↓
conclusion_builder input order
↓
derived ProofStep.premises order
```

を一貫して維持する。

---

## premise-free rule の application

premise pattern を持たない rule、

```text
premise_patterns = ()
```

についても application を可能とする。

この場合、

```text
InferenceMatch.premises = ()
```

であり、
conclusion builder には、

```text
()
```

が渡される。

例えば、

```python
def builder(premises):
  assert premises == ()
  return "axiomatic conclusion"
```

のような rule を適用できる。

生成される ProofStep は、

```text
premises = ()
rule = ProofRule.INFERENCE
inference_rule = rule
```

を持つ。

したがって、

```text
premise-free match
```

と、

```text
premise-free application
```

の両方を一貫して扱える。

---

## invalid input と application failure の区別

`apply_inference_match()` では、
異常入力を明示的に区別する。

`InferenceMatch` 以外が渡された場合は、

```text
TypeError
```

とする。

例えば、

```python
apply_inference_match(
  "invalid"
)
```

は API misuse である。

一方、
正しい InferenceMatch であっても、
InferenceRule に conclusion builder がない場合は、

```text
ValueError
```

とする。

これは、

```text
match 自体は有効
```

だが、

```text
application のための conclusion construction が未定義
```

という状態を表す。

さらに、
`conclusion_builder` が `None` ではないが
callable でもない場合は、

```text
TypeError
```

とする。

したがって、

```text
invalid match object
missing application specification
invalid builder object
```

を区別する。

---

## matching と application の分離

Phase 5-22 の重要な設計原則は、

```text
matching
```

と、

```text
application
```

を同一処理にしないことである。

matching pipeline は引き続き、

```text
InferenceRule
+
available ProofSteps
↓
find_inference_match()
↓
InferenceMatch / None
```

とする。

application はその後に、

```text
InferenceMatch
↓
apply_inference_match()
↓
ProofStep
```

として独立して行う。

したがって、

```text
find_inference_match()
```

や、

```text
find_inference_matches()
```

は conclusion builder の存在を要求しない。

これにより、

```text
rule discovery
rule applicability inspection
premise assignment inspection
```

だけを行いたい場合には、
rule application を発生させずに利用できる。

---

## conclusion_builder と symbolic inference の境界

Phase 5-22 の conclusion builder は、
一般的な Python callable とする。

これは意図的な最小設計である。

現在の `PremisePattern` が扱えるのは、

```text
proof_rule
statement_type
relation_type
```

という ProofStep レベルの structural condition である。

例えば、

```text
RelationType.ZERO
```

を持つ step を探すことはできる。

しかし、

```text
mα = 0
```

という expression の内部から、

```text
m
α
```

を自動的に取り出すことはまだできない。

そのため Phase 5-22 では、

```text
Expression pattern
variable binding
substitution
conclusion template
```

を conclusion builder の中へ無理に組み込まない。

代わりに、

```text
matched concrete ProofSteps
↓
explicit builder function
↓
conclusion
```

という最小機構だけを導入する。

これにより、
rule application pipeline を先に確立し、
symbolic matching の設計を後続フェーズへ分離できる。

---

## InferenceMatch に bindings をまだ持たせない

Phase 5-22 の `InferenceMatch` は引き続き、

```text
inference_rule
premises
```

だけを保持する。

例えば、

```text
mα = 0
```

に対して将来的に、

```text
m -> 2
α -> η_3
```

という binding を得る場合でも、
Phase 5-22 ではその情報をまだ保持しない。

したがって current `InferenceMatch` は、

```text
rule
+
matched ProofSteps
```

を表し、

```text
rule
+
matched ProofSteps
+
expression variable bindings
```

までは表さない。

bindings の必要な形が明確になった段階で、
InferenceMatch を拡張するか、
別オブジェクトとして保持するかを検討する。

---

## Phase 5-22 時点の inference pipeline

Phase 5-22 の完了により、
現在の pipeline は、

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
InferenceMatch
```

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
```

そして、

```text
InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

まで到達した。

よりまとめると、

```text
available ProofSteps
+
InferenceRule
↓
premise search
↓
structured match
↓
conclusion construction
↓
derived ProofStep
```

という最小 inference application pipeline が成立した。

---

## Phase 5-22 時点の設計原則

1. `InferenceRule` は optional な `conclusion_builder` を保持できる。
2. `conclusion_builder` の default は `None` とする。
3. premise matching に conclusion builder は要求しない。
4. applicability 判定に conclusion builder は要求しない。
5. structured match search に conclusion builder は要求しない。
6. conclusion builder は rule application 時だけ必要とする。
7. `InferenceMatch` と rule application を分離する。
8. rule application は `apply_inference_match()` に集約する。
9. conclusion builder には `InferenceMatch.premises` を渡す。
10. builder が返した値を derived ProofStep の conclusion とする。
11. derived ProofStep の premises は matched premises をそのまま保持する。
12. derived ProofStep の rule は `ProofRule.INFERENCE` とする。
13. derived ProofStep は使用した `InferenceRule` を保持する。
14. premise-pattern order を builder input と derived step に維持する。
15. premise-free rule も同じ application API で扱う。
16. invalid InferenceMatch は `TypeError` とする。
17. conclusion builder がない application は `ValueError` とする。
18. non-callable builder は `TypeError` とする。
19. Phase 5-21 以前の builder を持たない rule との後方互換性を維持する。
20. conclusion builder は現段階では一般 callable とし、過剰に構造化しない。
21. expression-level pattern matching はまだ導入しない。
22. pattern variable はまだ導入しない。
23. variable binding はまだ導入しない。
24. substitution はまだ導入しない。
25. structured conclusion template はまだ導入しない。
26. `InferenceMatch` に bindings はまだ保持しない。
27. automatic rule selection はまだ行わない。
28. derived ProofStep の available-step collection への自動追加はまだ行わない。
29. iterative inference はまだ行わない。
30. algebra / EHP 層には変更を加えない。

---

## Phase 5-22 の到達点

Phase 5-22 により、

```text
この rule が使える
```

という applicability 判定から、

```text
この premises で rule が使える
```

という structured match を経て、

```text
実際に rule を適用して
新しい ProofStep を作る
```

ところまで進んだ。

現在は、

```text
available facts
↓
matching
↓
InferenceMatch
↓
application
↓
derived fact
```

という最小 proof-engine cycle の一方向部分が成立している。

ただし、
derived fact はまだ available facts へ自動的に戻されない。

したがって、

```text
derived ProofStep
↓
available ProofSteps に追加
↓
再度 matching
↓
さらに derived ProofStep
```

という iterative inference はまだ実装していない。

また、
数学的に一般的な inference rule を記述するには、

```text
Expression pattern
↓
variable binding
↓
substitution
↓
conclusion
```

が必要になる。

Phase 5-22 の conclusion builder は、
この symbolic inference machinery を導入する前に、
rule application の責務と API 境界を確立するための
最小 mechanism と位置づける。


# 複数 InferenceMatch の一括 application

## Phase 5-23：apply_inference_matches()

Phase 5-22 では、

```text
InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

という単一 rule application を導入した。

これにより、

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

という最小 inference application pipeline が成立した。

Phase 5-23 では、
複数の inference rule が同時に match した場合に、
複数の `InferenceMatch` をまとめて適用できるようにする。

新しい経路は、

```text
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

とする。

---

## apply_inference_matches() の責務

`apply_inference_matches()` は、

```python
apply_inference_matches(
  inference_matches,
)
```

という API とする。

責務は、

```text
InferenceMatch の collection を受け取る
↓
各 InferenceMatch を適用する
↓
derived ProofStep の tuple を返す
```

ことだけとする。

具体的には、

```text
(
  match_a,
  match_b,
)
```

に対して、

```text
(
  derived_step_a,
  derived_step_b,
)
```

を返す。

---

## apply_inference_match() への委譲

collection-level application で
単一 match の application logic を重複実装しない。

`apply_inference_matches()` は内部で、

```text
apply_inference_match()
```

を各 match に対して呼び出す。

概念的には、

```text
apply_inference_matches(matches)
↓
for match in matches
↓
apply_inference_match(match)
↓
tuple of ProofStep
```

とする。

したがって、

```text
conclusion_builder の存在確認
conclusion_builder の callable 判定
conclusion の構築
ProofRule.INFERENCE の設定
matched premises の保存
applied InferenceRule の保存
```

は引き続き `apply_inference_match()` の責務とする。

`apply_inference_matches()` はこれらを再実装しない。

この委譲により、
single application と collection application の挙動を
一貫させる。

---

## _normalize_inference_matches()

既存の API では、

```text
ProofStep
InferenceRule
Relation
```

などについて、

```text
single object
tuple
list
```

を受け取るための normalize helper を使用している。

Phase 5-23 でも同じ方針を採用し、

```python
_normalize_inference_matches()
```

を導入する。

入力として、

```text
single InferenceMatch
tuple of InferenceMatch
list of InferenceMatch
```

を許可し、
内部では、

```text
tuple[InferenceMatch, ...]
```

へ正規化する。

これにより public API では、
単一 match だけを application したい場合でも、

```python
apply_inference_matches(
  match,
)
```

と書ける。

---

## 空 collection の扱い

空の InferenceMatch collection は
正常な入力として扱う。

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

これは、

```text
find_inference_matches()
```

が match のない場合に、

```text
()
```

を返す設計と直接接続するためである。

したがって、

```python
matches = find_inference_matches(
  rules,
  available_steps,
)

derived_steps = apply_inference_matches(
  matches,
)
```

というコードでは、
match が0件でも特別な分岐を必要としない。

---

## 入力順序の維持

`apply_inference_matches()` は、
入力された `InferenceMatch` の順序を維持する。

例えば、

```text
(
  match_b,
  match_a,
)
```

に対して、

```text
(
  derived_step_b,
  derived_step_a,
)
```

を返す。

collection-level application 自体は、
rule priority や application priority を判断しない。

入力順序を変更せず、
与えられた match collection をそのまま適用する。

---

## find_inference_matches() との順序整合性

Phase 5-21 で導入した、

```text
find_inference_matches()
```

は、
InferenceRule の入力順を維持して
InferenceMatch を返す。

したがって、

```text
InferenceRule collection
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

という経路では、

```text
InferenceRule input order
↓
InferenceMatch order
↓
derived ProofStep order
```

が維持される。

これにより、
現在の inference pipeline は deterministic な順序を持つ。

ただし、
この順序は mathematical priority を意味しない。

現段階では単に、

```text
caller が与えた rule order
```

を保存しているだけである。

将来的な rule priority は別の責務として導入する。

---

## matched premises の保存

各 derived ProofStep の `premises` は、
対応する `InferenceMatch.premises` を保持する。

例えば、

```text
match_a.premises
=
(
  step_1,
)
```

なら、

```text
derived_step_a.premises
=
(
  step_1,
)
```

となる。

複数 match をまとめて apply しても、
各 derived step の依存関係は混ざらない。

概念的には、

```text
match_a
├── rule_a
└── premises_a

match_b
├── rule_b
└── premises_b
```

から、

```text
derived_a
├── inference_rule = rule_a
└── premises = premises_a

derived_b
├── inference_rule = rule_b
└── premises = premises_b
```

を生成する。

---

## applied InferenceRule の保存

各 derived ProofStep は、
単一 application と同様に、

```text
inference_rule
```

へ実際に使用した `InferenceRule` を保持する。

したがって collection-level application 後も、

```text
derived_step
↓
どの rule を使用したか
```

を追跡できる。

`apply_inference_matches()` 自体が
複数 rule の情報をまとめた別オブジェクトを作ることはしない。

各 `ProofStep` が自身の推論規則を保持する現在のモデルを維持する。

---

## validation の責務

`_normalize_inference_matches()` は、

```text
InferenceMatch
tuple/list of InferenceMatch
```

以外を拒否する。

例えば、

```text
"invalid"
```

のような入力は `TypeError` とする。

また、

```text
[
  valid_match,
  "invalid",
]
```

のように collection 内に
InferenceMatch 以外が含まれる場合も `TypeError` とする。

一方、
各 InferenceMatch の rule に、

```text
conclusion_builder = None
```

が設定されている場合や、
builder が callable でない場合の validation は、
`apply_inference_match()` に委譲する。

したがって validation の境界は、

```text
collection structure validation
↓
_normalize_inference_matches()

individual application validation
↓
apply_inference_match()
```

とする。

---

## match search と application を統合しない

Phase 5-23 では、

```text
find_inference_matches()
```

と、

```text
apply_inference_matches()
```

を別 API として維持する。

つまり、

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)

derived_steps = apply_inference_matches(
  matches,
)
```

とする。

`apply_inference_matches()` に、

```text
InferenceRule collection
available ProofSteps
```

を渡して、
内部で自動的に match search まで行わせることはしない。

理由は、

```text
matching
```

と、

```text
application
```

を独立した処理として観察・制御できるようにするためである。

caller は必要に応じて、

```text
find matches
↓
matches を確認
↓
一部を選択
↓
application
```

という処理を行える。

これは将来的な、

```text
rule priority
rule selection
user confirmation
proof strategy
search strategy
```

を導入するためにも重要である。

---

## find → apply の接続

Phase 5-23 では、
単に `apply_inference_matches()` 単体が動作するだけでなく、

```text
find_inference_matches()
↓
apply_inference_matches()
```

という実際の接続も保証する。

概念的には、

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
(
  InferenceMatch(
    inference_rule=rule_a,
    premises=(step_a,),
  ),
  InferenceMatch(
    inference_rule=rule_b,
    premises=(step_b,),
  ),
)
↓
apply_inference_matches()
↓
(
  ProofStep(
    conclusion=conclusion_a,
    premises=(step_a,),
    rule=ProofRule.INFERENCE,
    inference_rule=rule_a,
  ),
  ProofStep(
    conclusion=conclusion_b,
    premises=(step_b,),
    rule=ProofRule.INFERENCE,
    inference_rule=rule_b,
  ),
)
```

となる。

これにより、
複数 rule の検索から複数 conclusion の生成までを
既存 primitive の組み合わせだけで実行できる。

---

## high-level API との境界

Phase 5-23 では、

```text
find_inference_matches()
+
apply_inference_matches()
```

をまとめる high-level API はまだ導入しない。

将来的には例えば、

```text
derive_inference_steps(
  inference_rules,
  available_steps,
)
```

のような convenience function を追加する可能性がある。

その場合でも内部構造は、

```text
derive_inference_steps()
↓
find_inference_matches()
↓
apply_inference_matches()
```

という薄い composition とする。

match search や application logic を
high-level API に再実装しない。

---

## iterative inference との境界

Phase 5-23 で得られた derived ProofStep は、
まだ自動的に `available_steps` へ追加しない。

したがって現在は、

```text
available ProofSteps
↓
find matches
↓
apply matches
↓
derived ProofSteps
```

までで処理が終了する。

まだ、

```text
available ProofSteps
+
derived ProofSteps
↓
new available ProofSteps
↓
find matches again
```

とはしない。

これは iterative inference では、

```text
重複 conclusion
premise-free rule の再適用
循環推論
同じ rule の再適用
停止条件
推論 round
```

などの設計が必要になるためである。

これらは collection-level application とは別の責務として扱う。

---

## symbolic inference との境界

Phase 5-23 でも、
expression-level matching は導入しない。

現在の application pipeline は、

```text
ProofStep-level premise matching
↓
InferenceMatch
↓
Python conclusion_builder
↓
ProofStep
```

である。

まだ、

```text
mα = 0
```

から、

```text
m
α
```

を pattern variable として bind することはできない。

したがって Phase 5-23 は、

```text
collection-level orchestration
```

を拡張するフェーズであり、

```text
symbolic mathematical matching
```

を拡張するフェーズではない。

---

## Phase 5-23 時点の inference pipeline

現在の inference pipeline は、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
```

から始まり、

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
InferenceMatch
```

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
```

```text
InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

そして、

```text
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

まで到達した。

よりまとめると、

```text
InferenceRule collection
+
available ProofSteps
↓
structured match search
↓
InferenceMatch collection
↓
collection-level application
↓
derived ProofStep collection
```

という経路が成立した。

---

## Phase 5-23 時点の設計原則

1. 複数の `InferenceMatch` をまとめて application できるようにする。
2. collection-level application は `apply_inference_matches()` に集約する。
3. `apply_inference_matches()` は `apply_inference_match()` を再利用する。
4. single application の logic を collection API に重複実装しない。
5. `InferenceMatch` の single / tuple / list input を許可する。
6. 入力は `_normalize_inference_matches()` で tuple に正規化する。
7. 空 collection は正常な入力として `()` を返す。
8. InferenceMatch 以外の入力は `TypeError` とする。
9. collection 内の不正要素も `TypeError` とする。
10. individual rule application の validation は `apply_inference_match()` に委譲する。
11. InferenceMatch の入力順序を derived ProofStep の順序として維持する。
12. matched premises は対応する derived ProofStep にそのまま保持する。
13. applied InferenceRule は対応する derived ProofStep にそのまま保持する。
14. `find_inference_matches()` と `apply_inference_matches()` は分離する。
15. collection-level application は rule search を行わない。
16. collection-level application は rule priority を判断しない。
17. collection-level application は rule selection を行わない。
18. `find_inference_matches()` → `apply_inference_matches()` の接続を保証する。
19. high-level match-and-apply API はまだ導入しない。
20. derived ProofStep を available facts へ自動追加しない。
21. iterative inference はまだ導入しない。
22. duplicate conclusion detection はまだ導入しない。
23. inference round / fixed-point termination はまだ導入しない。
24. expression-level pattern matching はまだ導入しない。
25. variable binding / substitution はまだ導入しない。
26. algebra / EHP 層には変更を加えない。

---

## Phase 5-23 の到達点

Phase 5-22 では、

```text
1つの InferenceMatch
↓
1つの derived ProofStep
```

まで到達した。

Phase 5-23 では、

```text
複数の InferenceMatch
↓
複数の derived ProofStep
```

まで一般化した。

その結果、

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

という collection-level inference pipeline が成立した。

これにより、
proof engine は複数の同時に applicable な inference rule から
複数の derived fact を生成できる段階まで進んだ。

ただし現段階では、

```text
どの match を apply するか
```

という選択は caller の責務であり、

```text
derived fact を次の推論へ再利用する
```

処理もまだ caller の責務である。

次の設計上の自然な候補は、

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

をまとめる薄い high-level API である。

その後、

```text
derived ProofSteps
↓
available ProofSteps に追加
↓
次の inference round
```

へ進むことで、
iterative automatic inference の基盤へ接続できる。


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

という collection-level pipeline が成立した。

Phase 5-24 では、
この既存 pipeline を一般的な利用側から簡潔に呼び出すため、

```python
derive_inference_steps(
  inference_rules,
  available_steps,
)
```

を導入する。

目的は新しい matching algorithm や application algorithm を
追加することではない。

既存の、

```text
find_inference_matches()
```

と、

```text
apply_inference_matches()
```

を薄く合成する high-level API を用意することである。

---

## derive_inference_steps() の責務

`derive_inference_steps()` の責務は、

```text
InferenceRule collection
+
available ProofSteps
↓
現在 applicable な rule と premises を検索
↓
それぞれを application
↓
derived ProofStep collection
```

を1回の呼び出しで実行することとする。

実装は、

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

という薄い composition とする。

つまり、

```text
derive_inference_steps()
↓
find_inference_matches()
↓
apply_inference_matches()
```

である。

---

## high-level API に logic を再実装しない

`derive_inference_steps()` 自身には、

```text
InferenceRule normalization
ProofStep normalization
premise-pattern matching
premise candidate search
distinct-step assignment
InferenceMatch construction
conclusion_builder validation
conclusion construction
ProofRule.INFERENCE assignment
premise preservation
InferenceRule preservation
```

を実装しない。

これらはすでに、

```text
find_inference_matches()
apply_inference_matches()
apply_inference_match()
```

およびその下位関数に存在している。

したがって Phase 5-24 の high-level API は、
既存 primitive の orchestration だけを担当する。

これにより、

```text
low-level behavior
```

と、

```text
high-level behavior
```

の意味が乖離することを防ぐ。

---

## low-level API は残す

`derive_inference_steps()` を導入しても、

```text
find_inference_matches()
```

と、

```text
apply_inference_matches()
```

を統合・廃止しない。

用途は異なる。

単純に現在 derivable な step をすべて生成したい場合は、

```python
derived_steps = derive_inference_steps(
  inference_rules,
  available_steps,
)
```

とできる。

一方、
matching result を application 前に確認したい場合は、

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)
```

を直接利用する。

例えば将来的に、

```text
rule priority
proof strategy
search strategy
user selection
cost evaluation
branch selection
```

などを導入する場合、

```text
find
↓
inspect
↓
select
↓
apply
```

という経路が必要になる。

そのため high-level API は convenience function とし、
lower-level API を隠さない。

---

## 1 inference round として扱う

`derive_inference_steps()` は、

```text
現在の available ProofSteps
```

だけを対象にする。

この呼び出し中に生成された derived steps を
同じ呼び出しの available steps へ追加しない。

したがって、

```text
rule A
premise: GIVEN
conclusion: intermediate
```

と、

```text
rule B
premise: intermediate
conclusion: final
```

が存在していても、
`intermediate` が呼び出し開始時点の
`available_steps` に存在しなければ、
同一 `derive_inference_steps()` 呼び出しの中で
rule B が新たに applicable になることはない。

概念的には、

```text
available ProofSteps at start
↓
one match search
↓
one application stage
↓
derived ProofSteps
```

であり、

```text
derive
↓
add
↓
derive
↓
add
↓
...
```

ではない。

この distinction を、
iterative inference との境界として維持する。

---

## rule order の保持

Phase 5-24 では、
high-level API でも deterministic な順序を維持する。

既存の、

```text
find_inference_matches()
```

は input の `InferenceRule` 順を保持する。

また、

```text
apply_inference_matches()
```

は input の `InferenceMatch` 順を保持する。

したがって、

```text
derive_inference_steps()
```

も自然に、

```text
InferenceRule input order
↓
InferenceMatch order
↓
derived ProofStep order
```

を保持する。

例えば、

```text
(
  second_rule,
  first_rule,
)
```

がともに applicable なら、
derived step も、

```text
(
  second derived,
  first derived,
)
```

の順となる。

`derive_inference_steps()` 自体には
追加の sorting や ranking を導入しない。

---

## applicable rule がない場合

matching stage で、

```text
find_inference_matches()
```

が、

```text
()
```

を返した場合、

```text
apply_inference_matches(())
```

も、

```text
()
```

を返す。

したがって、

```python
derive_inference_steps(
  inference_rules,
  available_steps,
)
```

は applicable rule が存在しないことを
例外ではなく、

```text
()
```

として表現する。

これは、

```text
successful inference round
but no new currently derivable steps
```

を自然に表現できる。

将来 iterative inference を導入した場合には、
この空 tuple を fixed-point 判定の一部として利用できる可能性がある。

---

## 空 rule collection

`inference_rules=()` も有効な入力とする。

この場合、

```text
find_inference_matches()
↓
()
↓
apply_inference_matches()
↓
()
```

となる。

high-level API のためだけに
空 collection を特殊なエラーとして扱わない。

---

## input normalization の委譲

`derive_inference_steps()` 自身では input normalization を行わない。

`find_inference_matches()` が既存の、

```text
_normalize_inference_rules()
_normalize_proof_steps()
```

を利用するため、
high-level API でも、

```text
single InferenceRule
tuple of InferenceRule
list of InferenceRule
```

および、

```text
single ProofStep
tuple of ProofStep
list of ProofStep
```

を利用できる。

これは、

```text
derive_inference_steps()
```

専用の normalization logic を作らず、
lower-level API の input contract をそのまま継承する設計である。

---

## invalid input の扱い

不正な、

```text
inference_rules
```

または、

```text
available_steps
```

についても、
`derive_inference_steps()` 独自の validation を追加しない。

例えば、

```text
invalid rule collection
```

は `find_inference_matches()` 内の
rule normalization によって `TypeError` となる。

同様に、

```text
invalid ProofStep collection
```

も既存の ProofStep normalization によって
`TypeError` となる。

validation の責務を複製しない。

---

## conclusion_builder validation の委譲

matching 自体には、

```text
conclusion_builder
```

は不要である。

そのため、

```text
InferenceRule
premise matches
conclusion_builder=None
```

という rule は
`InferenceMatch` までは生成できる。

しかし application には conclusion の構築が必要であるため、
`apply_inference_match()` は
`conclusion_builder` が存在しない場合に `ValueError` を送出する。

`derive_inference_steps()` でも
この behavior をそのまま維持する。

つまり、

```text
derive_inference_steps()
↓
find_inference_matches()
↓
matched
↓
apply_inference_matches()
↓
apply_inference_match()
↓
missing builder
↓
ValueError
```

となる。

high-level API がこの例外を握りつぶしたり、
別の default conclusion を生成したりはしない。

---

## find → apply pipeline の正式な high-level 化

Phase 5-23 では caller が、

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)

derived_steps = apply_inference_matches(
  matches,
)
```

と明示的に接続していた。

Phase 5-24 では、

```python
derived_steps = derive_inference_steps(
  inference_rules,
  available_steps,
)
```

を同じ処理の正式な high-level entry point とする。

したがって現在の API は、

```text
low level:

find_inference_match()
apply_inference_match()

collection level:

find_inference_matches()
apply_inference_matches()

high level:

derive_inference_steps()
```

という階層になる。

---

## 現在の inference API 階層

Phase 5-24 時点では、
inference pipeline を次の階層として整理する。

### Pattern matching

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
```

### Explicit rule matching

```text
InferenceRule
+
explicit premises
↓
matches_inference_rule()
```

### Premise search

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
```

### Applicability

```text
InferenceRule
+
available ProofSteps
↓
is_inference_rule_applicable()
```

### Applicable rule collection

```text
InferenceRule collection
+
available ProofSteps
↓
find_applicable_inference_rules()
```

### Structured match

```text
InferenceRule
+
available ProofSteps
↓
find_inference_match()
↓
InferenceMatch
```

### Structured match collection

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
```

### Single application

```text
InferenceMatch
↓
apply_inference_match()
↓
ProofStep
```

### Collection application

```text
InferenceMatch collection
↓
apply_inference_matches()
↓
ProofStep collection
```

### High-level one-round derivation

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
ProofStep collection
```

この階層では、
上位 API は下位 API を組み合わせるだけとし、
下位の意味論を再実装しない。

---

## derived ProofStep の意味

`derive_inference_steps()` が返す各 `ProofStep` は、
従来の `apply_inference_match()` と同じ意味を持つ。

すなわち、

```text
conclusion
= conclusion_builder(matched premises)

premises
= matched ProofSteps

rule
= ProofRule.INFERENCE

inference_rule
= applied InferenceRule
```

である。

high-level API を経由したことによる
特別な ProofStep type や metadata は追加しない。

つまり derived result は、
直接 `apply_inference_match()` で生成した result と同じ
ProofStep model に収まる。

---

## iterative inference との境界

Phase 5-24 は、
high-level one-round inference までを責務とする。

まだ、

```text
derived ProofSteps
↓
available ProofSteps へ追加
```

は行わない。

そのため現在は、

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
new ProofSteps
```

で停止する。

次の段階では、

```text
available
+
derived
↓
merge
↓
expanded available
```

という operation が必要になる。

しかし単純な tuple concatenation だけでは、
以下の問題が生じる。

```text
duplicate conclusion
same conclusion from different proofs
same rule repeated
premise-free rule repeated
cyclic derivation
```

したがって iterative inference を導入する前に、

```text
proof-step collection merge
```

または、

```text
new conclusion detection
```

の設計を明確にする。

---

## duplicate detection との境界

Phase 5-24 では
duplicate detection を `derive_inference_steps()` に含めない。

例えば2つの rule が、
同じ conclusion を生成した場合でも、

```text
derived_step_a
derived_step_b
```

として両方返り得る。

これは現段階では、

```text
same conclusion
```

と、

```text
same proof
```

を同一視する基準がまだ定義されていないためである。

将来的には、

```text
ProofStep identity
conclusion equality
inference rule
premises
proof provenance
```

のどれを使って duplicate とみなすかを設計する必要がある。

この責務は high-level one-round derivation とは分離する。

---

## premise-free rule と iterative inference

現在の `InferenceRule` は、

```text
premise_patterns=()
```

を許している。

そのため premise-free rule は、
available steps の内容にかかわらず applicable となる。

1 round の、

```text
derive_inference_steps()
```

では問題にならない。

しかし iterative inference で同じ rule を毎 round 評価すると、

```text
same premise-free rule
↓
same conclusion
↓
again
↓
same conclusion
↓
...
```

となり得る。

したがって iterative inference の前に、

```text
duplicate suppression
applied-rule history
new conclusion detection
```

のいずれかが必要になる。

Phase 5-24 ではこの問題を解決せず、
one-round API に限定することで境界を維持する。

---

## symbolic inference との境界

Phase 5-24 でも、
matching は ProofStep level に限定する。

例えば、

```text
RelationType.ZERO
```

を持つ Relation の step は認識できるが、

```text
mα = 0
```

という expression structure から、

```text
m
α
```

を variable として抽出することはできない。

したがって現在は、

```text
PremisePattern
↓
ProofStep matching
↓
concrete matched premises
↓
Python conclusion_builder
```

である。

まだ、

```text
ExpressionPattern
↓
bindings
↓
substitution
↓
structured conclusion template
```

ではない。

high-level API はこの symbolic inference を隠す abstraction ではなく、
現在存在する ProofStep-level inference pipeline を
まとめて呼び出すための API とする。

---

## Phase 5-24 の設計原則

Phase 5-24 では、次の原則を採用する。

1. `derive_inference_steps()` を high-level inference API とする。
2. `derive_inference_steps()` は `find_inference_matches()` と `apply_inference_matches()` の薄い composition とする。
3. matching logic を high-level API に再実装しない。
4. application logic を high-level API に再実装しない。
5. input normalization は既存 lower-level API に委譲する。
6. conclusion-builder validation も既存 application API に委譲する。
7. lower-level の match / apply API は引き続き公開・利用可能とする。
8. `derive_inference_steps()` は1 inference round だけを表す。
9. derived ProofStep を同一呼び出し中に available steps へ追加しない。
10. inference-rule input order を derived ProofStep order まで維持する。
11. applicable rule がなければ空 tuple を返す。
12. 空 rule collection も有効な入力とする。
13. high-level API 独自の ProofStep 型は導入しない。
14. duplicate detection はまだ行わない。
15. iterative inference は Phase 5-24 の責務に含めない。
16. premise-free rule の反復問題は iterative inference 側で扱う。
17. expression-level variable binding は別の symbolic inference 課題として維持する。
18. 高レベル機能は既存 primitive の composition として構築する設計方針を維持する。

これにより、

```text
available mathematical facts
+
InferenceRules
↓
derive_inference_steps()
↓
newly derived ProofSteps
```

という最初の high-level inference interface が成立した。

次の主要な設計課題は、

```text
available ProofSteps
+
derived ProofSteps
↓
重複を考慮した merge
↓
expanded ProofSteps
```

である。

これを導入した後、

```text
derive
↓
merge
↓
derive
↓
merge
```

を繰り返すことで、
fixed-point 型の iterative inference へ進むことができる。


# Phase 5-25：derived ProofStep を available ProofSteps に追加する1 round の inference

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

という high-level derivation API を導入した。

ただし返されるのは、

```text
新しく導出された ProofSteps
```

だけであり、

```text
既存 available ProofSteps
+
derived ProofSteps
```

という次の inference に利用できる集合を構築する処理は
caller 側に残されていた。

Phase 5-25 では、

```python
run_inference_round(
  inference_rules,
  available_steps,
)
```

を導入し、

```text
現在 available な ProofSteps を使って
1回 inference を実行
↓
derived ProofSteps を生成
↓
既存 available ProofSteps の後ろへ追加
↓
expanded ProofStep collection を返す
```

という明示的な1 round の inference を定義する。

---

## run_inference_round() の責務

基本 API は、

```python
run_inference_round(
  inference_rules,
  available_steps,
)
```

とする。

責務は、

```text
available ProofSteps の正規化
↓
derive_inference_steps()
↓
derived ProofSteps
↓
existing + derived
```

だけとする。

実装は、

```python
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

という薄い構造とする。

---

## derive と round の責務分離

Phase 5-24 の、

```python
derive_inference_steps()
```

と Phase 5-25 の、

```python
run_inference_round()
```

は異なる責務を持つ。

```text
derive_inference_steps()
↓
新しく導出された ProofSteps のみ返す
```

一方、

```text
run_inference_round()
↓
既存 ProofSteps
+
新しく導出された ProofSteps
を返す
```

とする。

すなわち、

```text
derivation
```

と、

```text
available fact collection の拡張
```

を別の API level として保持する。

---

## 1 round の定義

Phase 5-25 では、
inference round を次のように定義する。

```text
round 開始時点の available ProofSteps
↓
その collection だけを使って matching
↓
その collection だけを premises として derivation
↓
すべての derived ProofSteps をまとめて生成
↓
round 終了時に available ProofSteps の後ろへ追加
```

重要なのは、

```text
round 中に生成された derived ProofStep
```

を、

```text
同じ round の別 inference の premise
```

として使用しないことである。

したがって Phase 5-25 の round は、

```text
snapshot-based one-round inference
```

として扱う。

---

## round 開始時点の snapshot

例えば、

```text
available:
A
```

で、

```text
rule 1:
A → B

rule 2:
B → C
```

という rule がある場合、
1回の、

```python
run_inference_round(
  rules,
  available,
)
```

で生成されるのは、

```text
A
B
```

までである。

同じ round 内で、

```text
B
```

を利用して、

```text
C
```

までは導出しない。

`C` を導出するには、
返された expanded collection を使って
次の round を明示的に実行する。

```text
round 1:
A
↓
B

available after round 1:
A, B

round 2:
A, B
↓
B, C
```

ただし現段階では duplicate handling がないため、
実際の round 2 では rule 1 が再び `B` を生成する可能性がある。

このため自動 iterative inference はまだ導入しない。

---

## available-step order の維持

`run_inference_round()` は、
既存の ProofStep の順序を変更しない。

例えば、

```text
available:
(
  step_a,
  step_b,
  step_c,
)
```

なら、
返り値の先頭は必ず、

```text
(
  step_a,
  step_b,
  step_c,
  ...
)
```

となる。

既存 ProofStep の並び替え、
重複削除、
priority sorting は行わない。

---

## derived-step order の維持

Phase 5-24 までの、

```text
InferenceRule order
↓
find_inference_matches()
↓
InferenceMatch order
↓
apply_inference_matches()
↓
derived ProofStep order
```

という順序保存をそのまま利用する。

したがって、

```text
available order
↓
derived order
```

を連結したものが
`run_inference_round()` の返り値となる。

例えば、

```text
rules:
(
  rule_b,
  rule_a,
)

available:
(
  step_1,
  step_2,
)
```

から、

```text
derived:
(
  derived_from_rule_b,
  derived_from_rule_a,
)
```

が得られた場合、
round result は、

```text
(
  step_1,
  step_2,
  derived_from_rule_b,
  derived_from_rule_a,
)
```

となる。

---

## ProofStep の意味を変更しない

`run_inference_round()` によって追加される derived step は、
`derive_inference_steps()` が返す ProofStep そのものである。

したがって、

```text
conclusion
premises
rule
inference_rule
```

の意味は変更しない。

derived step は、

```text
rule = ProofRule.INFERENCE
```

を持ち、

```text
premises = matched ProofSteps
```

を保持し、

```text
inference_rule = applied InferenceRule
```

を保持する。

round のためだけの新しい ProofStep subtype や flag は
導入しない。

---

## round metadata はまだ導入しない

Phase 5-25 では、

```text
この ProofStep は round 1 で生成された
この ProofStep は round 2 で生成された
```

という metadata は保持しない。

`run_inference_round()` は
単に ProofStep collection を返す。

将来的に iterative inference を導入した際に、

```text
InferenceRound
round index
new steps
existing steps
applied matches
```

などの構造が必要かどうかを改めて判断する。

---

## input normalization

`available_steps` は、
まず、

```python
_normalize_proof_steps(
  available_steps,
  "available_steps",
)
```

によって正規化する。

これにより、

```text
single ProofStep
tuple of ProofStep
list of ProofStep
```

を同じ tuple representation として扱う。

`inference_rules` の normalization は、
`derive_inference_steps()` から既存の、

```text
find_inference_matches()
↓
_normalize_inference_rules()
```

へ委譲する。

したがって `run_inference_round()` 自体で
rule normalization を重複実装しない。

---

## validation の委譲

Phase 5-25 では、
既存の validation hierarchy を維持する。

```text
available-step validation
↓
_normalize_proof_steps()

rule validation
↓
find_inference_matches()
↓
_normalize_inference_rules()

conclusion-builder validation
↓
apply_inference_match()
```

したがって、

```text
invalid inference_rules
invalid available_steps
missing conclusion_builder
non-callable conclusion_builder
```

などについて、
round API 独自の別ルールを導入しない。

---

## no applicable rule

現在 applicable な rule が存在しない場合、

```text
derive_inference_steps()
↓
()
```

となる。

そのため、

```text
normalized_steps + ()
```

により、
`run_inference_round()` は既存 collection をそのまま返す。

これはエラーではなく、

```text
この round では新しい ProofStep が生成されなかった
```

という正常な結果とする。

---

## empty rules

rule collection が空の場合も、

```text
derived_steps = ()
```

となるため、
available steps をそのまま返す。

```text
rules:
()

available:
(
  step_a,
)

result:
(
  step_a,
)
```

となる。

---

## empty available steps

available steps が空でも、
premise-free rule が存在すれば inference は可能である。

例えば、

```text
rule:
premise_patterns = ()
```

かつ有効な、

```text
conclusion_builder
```

を持つ場合、

```text
available:
()

↓ run_inference_round()

result:
(
  derived_step,
)
```

となる。

この挙動は、
既存の premise-free rule matching / application semantics を
そのまま継承する。

---

## duplicate handling との境界

Phase 5-25 で最も重要な設計境界は、
duplicate detection をまだ行わないことである。

例えば、

```text
available:
A

rule:
A → B
```

に対して round 1 を行うと、

```text
A
B
```

となる。

この結果に対して再度同じ round を実行すると、
現状では、

```text
A
B
B
```

となり得る。

`run_inference_round()` は、

```text
B がすでに存在するか
```

を調べない。

また、

```text
同じ conclusion だが premises が異なる
```

場合を同一 fact とみなすかどうかも判断しない。

これらは次の duplicate-aware merge 層の責務とする。

---

## ProofStep equality と conclusion equality の区別

iterative inference へ進む前に、
少なくとも次の概念を区別する必要がある。

```text
ProofStep が等しい
```

```text
conclusion が等しい
```

```text
同じ conclusion に対する別 proof である
```

例えば、

```text
step 1:
A, B → C

step 2:
D, E → C
```

は、
conclusion は同じでも proof dependency は異なる。

これを、

```text
duplicate として1つにする
```

のか、

```text
C の alternative proofs として両方保持する
```

のかは、
Phase 5-25 では決めない。

そのため round API は単純な tuple concatenation に限定する。

---

## premise-free rule と iteration

premise-free rule は、

```text
available facts がなくても applicable
```

である。

したがって iterative inference を単純に、

```text
repeat run_inference_round()
```

として実装すると、
premise-free rule が同じ conclusion を毎 round 生成し続ける可能性がある。

この問題も Phase 5-25 では解決しない。

固定点 inference の前に、

```text
duplicate conclusion detection
```

または、

```text
rule + premises + conclusion
の application history
```

のような再適用制御が必要になる。

---

## Phase 5-25 時点の inference API 階層

現在の inference pipeline は、

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
InferenceMatch
```

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
```

```text
InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

```text
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
derived ProofStep collection
```

そして Phase 5-25 で、

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

まで到達した。

---

## Phase 5-25 時点の設計原則

1. inference の1 round を `run_inference_round()` で表現する。
2. round は開始時点の available ProofSteps を snapshot として扱う。
3. round 中に生成された derived step は同じ round の matching には利用しない。
4. derived step は round 終了時にまとめて追加する。
5. `run_inference_round()` は `derive_inference_steps()` を再利用する。
6. matching / application logic を round API に重複実装しない。
7. existing ProofStep の入力順序を維持する。
8. derived ProofStep の既存 ordering semantics を維持する。
9. round result は existing steps の後ろに derived steps を追加した tuple とする。
10. `derive_inference_steps()` は derived steps のみを返す API として残す。
11. `run_inference_round()` は expanded available steps を返す API とする。
12. derived ProofStep の構造や意味は変更しない。
13. round 専用 ProofStep type は導入しない。
14. round index や round metadata はまだ導入しない。
15. single / tuple / list の既存 input normalization を維持する。
16. invalid input validation は既存 normalization API に委譲する。
17. conclusion-builder validation は既存 application API に委譲する。
18. applicable rule がない場合は available steps をそのまま返す。
19. empty rule collection は正常入力とする。
20. empty available collection でも premise-free rule は適用可能とする。
21. duplicate conclusion detection はまだ行わない。
22. duplicate ProofStep detection はまだ行わない。
23. alternative proofs の統合方針はまだ決めない。
24. automatic repeated rounds はまだ行わない。
25. fixed-point termination はまだ導入しない。
26. repeated rule application の抑制はまだ行わない。
27. premise-free rule の repeated application 制御はまだ行わない。
28. cyclic inference detection はまだ行わない。
29. inference history はまだ導入しない。
30. expression-level pattern matching / bindings / substitution はまだ別課題とする。
31. algebra / EHP 層には変更を加えない。

---

## Phase 5-25 の到達点

Phase 5-24 では、

```text
available ProofSteps
+
InferenceRules
↓
derived ProofSteps
```

まで到達していた。

Phase 5-25 では、

```text
available ProofSteps
+
InferenceRules
↓
derived ProofSteps
↓
available ProofSteps + derived ProofSteps
```

まで進んだ。

これにより、
proof engine は初めて、

```text
1 round 前の knowledge state
↓
inference
↓
1 round 後の expanded knowledge state
```

という形を直接表現できるようになった。

現在の一方向 pipeline は、

```text
available facts
↓
matching
↓
InferenceMatch
↓
application
↓
derived facts
↓
available facts へ追加
```

まで成立している。

残る大きな段階は、

```text
expanded facts
↓
次の round
↓
さらに expanded facts
↓
...
```

を安全に反復することである。

その前に、

```text
duplicate detection
new fact detection
termination condition
repeated application control
```

を設計する必要がある。

したがって次の自然な段階は、
単純な iterative loop を導入することではなく、

```text
existing ProofSteps
+
derived ProofSteps
↓
duplicate-aware merge
↓
genuinely new ProofSteps
```

という merge semantics を定義することである。

その後、

```text
run_inference_round()
↓
new-step detection
↓
new step が存在すれば repeat
↓
存在しなければ fixed point
```

という iterative inference へ進むことができる。


# Phase 5-26：derived ProofStep の duplicate-aware merge

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

という1 round の inference を導入した。

これにより、

```text
round 開始時の knowledge state
↓
inference
↓
round 終了時の expanded knowledge state
```

を直接表現できるようになった。

ただし Phase 5-25 の `run_inference_round()` は、

```text
normalized available steps
+
derived steps
```

という単純な tuple concatenation を行っていた。

そのため、

```text
A → B
```

という rule を同じ knowledge state に対して繰り返し適用すると、

```text
A
B
B
B
...
```

のように同じ conclusion が重複して追加される可能性があった。

Phase 5-26 では、
iterative inference へ進む前提として、

```text
available ProofSteps
+
derived ProofSteps
↓
duplicate-aware merge
↓
expanded ProofSteps
```

を導入する。

---

## merge_proof_steps()

Phase 5-26 では、

```python
merge_proof_steps(
  available_steps,
  derived_steps,
)
```

を導入する。

責務は、

```text
existing available ProofSteps
+
candidate derived ProofSteps
↓
duplicate conclusion detection
↓
new conclusion だけを追加
↓
merged ProofStep collection
```

である。

`merge_proof_steps()` は inference rule の matching や
conclusion construction を担当しない。

それらは引き続き、

```text
find_inference_matches()
apply_inference_matches()
derive_inference_steps()
```

の責務とする。

したがって、

```text
derive
```

と、

```text
merge
```

を別の操作として維持する。

---

## duplicate criterion

Phase 5-26 では、
duplicate の基準として、

```text
ProofStep equality
```

ではなく、

```text
ProofStep.conclusion equality
```

を採用する。

判定は、

```python
step.conclusion == known_conclusion
```

とする。

したがって、

```text
conclusion が同じ
```

なら、

```text
premises が異なる
rule が異なる
inference_rule が異なる
note が異なる
```

場合でも、
available knowledge state へは新しい fact として追加しない。

これは、

```text
available ProofSteps
```

を、

```text
現在利用可能な数学的 conclusions の集合
```

として扱うための最小方針である。

---

## Proof identity と fact identity の分離

Phase 5-26 では、
次の2つを明確に区別する。

```text
ProofStep identity
```

と、

```text
fact / conclusion identity
```

である。

例えば、

```text
A, B
↓ rule 1
C
```

と、

```text
D, E
↓ rule 2
C
```

は、
ProofStep としては異なる。

なぜなら、

```text
premises
inference_rule
```

が異なるためである。

一方、
knowledge state の観点では、

```text
C
```

という conclusion はすでに known である。

Phase 5-26 の `merge_proof_steps()` は、
この knowledge-state 側の identity を採用する。

つまり、

```text
同じ conclusion
→ available facts としては1つ
```

とする。

---

## alternative proof との境界

conclusion equality を duplicate criterion としたため、
同じ conclusion に対する複数の proof が存在しても、

```text
merged available ProofSteps
```

には最初の1つだけが残る。

例えば、

```text
derived:
(
  proof_of_C_from_AB,
  proof_of_C_from_DE,
)
```

の場合、

```text
proof_of_C_from_AB.conclusion
==
proof_of_C_from_DE.conclusion
```

なら、

```text
merged:
(
  ...,
  proof_of_C_from_AB,
)
```

となる。

ただし、
これは alternative proof 自体を無意味とみなすものではない。

`derive_inference_steps()` は引き続き、
candidate derived ProofSteps をそのまま返すため、

```text
複数 rule が同じ conclusion を導いた
```

という情報は merge 前には存在する。

Phase 5-26 では、

```text
knowledge state の重複除去
```

だけを実装し、

```text
alternative proofs の保存・索引化
```

は別の責務として後の phase に残す。

---

## available steps の preservation

`merge_proof_steps()` は、
既存 available steps を削除・並べ替えしない。

例えば、

```text
available:
(
  step_b,
  step_a,
)
```

なら、
result の先頭も必ず、

```text
(
  step_b,
  step_a,
  ...
)
```

となる。

つまり、

```text
existing order
```

は完全に保存する。

Phase 5-26 では、
既存 available collection 内にすでに duplicate conclusion が
含まれていたとしても、
それらを retroactive に削除することはしない。

duplicate filtering の対象は、

```text
これから追加しようとする derived ProofSteps
```

である。

---

## derived step order

derived ProofSteps についても、
入力順を維持する。

ただし、
同じ conclusion を持つ derived steps が複数ある場合は、
最初の1つだけを追加する。

例えば、

```text
derived:
(
  B from rule 2,
  C,
  B from rule 1,
  D,
)
```

で、
B がまだ available でなければ、

```text
added:
(
  B from rule 2,
  C,
  D,
)
```

となる。

したがって Phase 5-26 の ordering rule は、

```text
first occurrence wins
```

である。

これは既存の inference-rule input order と
derived-step order preservation の方針に整合する。

---

## derived collection 内の duplicate

duplicate detection は、
available collection との比較だけではない。

derived collection 内で新しく追加された conclusion も、
その場で known conclusion として扱う。

実装上、

```text
known_conclusions
```

には最初に available conclusions を入れ、
新しい derived step を追加するたびに
その conclusion も追加する。

したがって、

```text
available:
A

derived:
B
B
```

は、

```text
A
B
```

になる。

また、

```text
available:
A
B

derived:
B
B
C
C
```

は、

```text
A
B
C
```

になる。

---

## input normalization

`merge_proof_steps()` では、
既存の、

```python
_normalize_proof_steps()
```

を再利用する。

対象は、

```text
available_steps
derived_steps
```

の両方である。

したがって両入力について、

```text
single ProofStep
tuple of ProofStep
list of ProofStep
```

を受け付ける。

内部表現は tuple に正規化する。

invalid input についても、
新しい validation mechanism は導入せず、
既存 `_normalize_proof_steps()` に委譲する。

---

## empty input

`merge_proof_steps()` は、
empty collection を正常入力として扱う。

### empty available

```text
available:
()

derived:
(
  B,
)
```

なら、

```text
result:
(
  B,
)
```

となる。

### empty derived

```text
available:
(
  A,
)

derived:
()
```

なら、

```text
result:
(
  A,
)
```

となる。

### both empty

```text
available:
()

derived:
()
```

なら、

```text
result:
()
```

となる。

---

## run_inference_round() への統合

Phase 5-25 の `run_inference_round()` は、

```python
return (
  normalized_steps
  + derived_steps
)
```

だった。

Phase 5-26 では、
これを、

```python
return merge_proof_steps(
  normalized_steps,
  derived_steps,
)
```

へ変更する。

したがって pipeline は、

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
normalize available ProofSteps
↓
derive_inference_steps()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
duplicate-safe expanded ProofSteps
```

となる。

---

## round snapshot semantics は変更しない

Phase 5-26 で変更するのは、
round 終了時の merge semantics だけである。

1 round の matching semantics は変更しない。

つまり、

```text
round 開始時の available ProofSteps
```

だけを使って、
その round のすべての `InferenceMatch` を決定する。

例えば、

```text
A → B
B → C
```

という2 rule があり、
round 開始時に、

```text
A
```

だけが available なら、

```text
round 1:
A
B
```

となる。

同じ round 内では newly derived `B` を再利用しないため、

```text
C
```

はまだ得られない。

次の round で、

```text
A
B
```

を available として matching することで、
初めて `C` を derive できる。

この snapshot semantics は Phase 5-25 から維持する。

---

## repeated round の idempotence

Phase 5-26 により、
同じ derivation しか存在しない場合、
`run_inference_round()` の再実行は knowledge state を増やさない。

例えば、

```text
available:
A

rule:
A → B
```

に対して、

```text
round 1:
A
B
```

となる。

次の round でも candidate として `B` は derive されるが、

```text
B == known conclusion
```

なので merge では追加されない。

したがって、

```text
round 2:
A
B
```

のままとなる。

つまりこの例では、

```python
second_result == first_result
```

となる。

これは fixed-point inference の基礎となる性質である。

---

## premise-free rule の repeated application

premise-free rule は、
available steps に関係なく毎 round applicable になり得る。

例えば、

```text
premise_patterns = ()
```

の rule が常に、

```text
B
```

を生成する場合、
Phase 5-25 では、

```text
round 1:
B

round 2:
B
B

round 3:
B
B
B
```

となる可能性があった。

Phase 5-26 では、
conclusion equality により、

```text
round 1:
B

round 2:
B

round 3:
B
```

となる。

したがって、
同じ conclusion を返す premise-free rule に対する
単純な無限 duplicate growth は防止できる。

ただし、

```text
毎回異なる conclusion を生成する builder
```

の場合は別であり、
Phase 5-26 は rule application history 自体を管理しない。

---

## conclusion equality の意味

Phase 5-26 では、
duplicate detection に Python の、

```python
==
```

をそのまま使用する。

したがって、
構造的 equality を持つ frozen dataclass などでは、

```text
同じ構造
```

を duplicate と判定できる。

一方、

```text
数学的には同値だが Python equality では異なる
```

conclusion は duplicate とみなされない。

例えば将来的に、

```text
α + β
```

と、

```text
β + α
```

を数学的には同じと判断したい場合でも、
Expression の canonicalization がなければ
自動的には同一 fact にならない。

したがって Phase 5-26 の duplicate detection は、

```text
mathematical equivalence
```

ではなく、

```text
current conclusion object equality
```

である。

より高度な canonicalization や semantic equivalence は
別課題とする。

---

## new-step detection との境界

`merge_proof_steps()` は、

```text
merged collection
```

を返す。

しかし、

```text
今回実際に追加された ProofSteps
```

を独立には返さない。

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
merge_proof_steps()
```

は、

```text
A
B
C
```

を返すが、

```text
new:
C
```

を直接返す API はまだない。

fixed-point inference では、

```text
new steps == ()
```

を termination condition として利用したいため、
次の段階では、

```text
genuinely new ProofSteps
```

を取得する mechanism が有用になる。

Phase 5-26 では、
まず duplicate-safe merge までを責務とする。

---

## Phase 5-26 時点の inference API 階層

現在の inference pipeline は、

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
InferenceMatch
```

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
```

```text
InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

```text
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
candidate derived ProofStep collection
```

```text
available ProofSteps
+
derived ProofSteps
↓
merge_proof_steps()
↓
duplicate-safe ProofStep collection
```

そして、

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
derive_inference_steps()
↓
merge_proof_steps()
↓
duplicate-safe expanded ProofSteps
```

まで到達した。

---

## Phase 5-26 時点の設計原則

1. duplicate-aware merge を inference derivation とは別責務とする。
2. merge API は `merge_proof_steps()` とする。
3. available steps と derived steps の両方を `_normalize_proof_steps()` で正規化する。
4. duplicate 判定は `ProofStep` 全体ではなく `conclusion` equality を使う。
5. knowledge state では同じ conclusion を複数回追加しない。
6. available ProofSteps の既存順序を維持する。
7. available collection の既存要素は削除しない。
8. derived ProofSteps は入力順に走査する。
9. duplicate derived conclusions では最初の ProofStep を保持する。
10. derived step を追加した時点でその conclusion を known とする。
11. derived collection 内の duplicate conclusion も除去する。
12. `merge_proof_steps()` は tuple を返す。
13. empty available / empty derived は正常入力とする。
14. invalid input validation は既存 normalization に委譲する。
15. `derive_inference_steps()` は candidate derived steps を返す API として変更しない。
16. `run_inference_round()` は `merge_proof_steps()` を利用する。
17. round の snapshot semantics は変更しない。
18. newly derived steps は同じ round の premise search には利用しない。
19. same derivation の repeated round で knowledge state が増えないようにする。
20. premise-free rule の same-conclusion repeated growth を merge で抑制する。
21. rule application history はまだ導入しない。
22. alternative proofs の専用 storage はまだ導入しない。
23. same conclusion の alternative proof は merged knowledge state では最初の1つだけ保持する。
24. merge 前の candidate derived ProofSteps では alternative derivations を確認可能とする。
25. conclusion の mathematical equivalence はまだ扱わない。
26. duplicate 判定は Python equality に依存する。
27. conclusion canonicalization はまだ導入しない。
28. genuinely new ProofSteps を別返り値として取得する API はまだ導入しない。
29. automatic repeated rounds はまだ行わない。
30. fixed-point termination はまだ実装しない。
31. cyclic inference detection はまだ実装しない。
32. inference round metadata / history はまだ導入しない。
33. expression-level pattern matching / binding / substitution は別課題とする。
34. algebra / EHP 層には変更を加えない。

---

## Phase 5-26 の到達点

Phase 5-25 では、

```text
available facts
↓
derive
↓
append
```

まで到達していた。

Phase 5-26 では、

```text
available facts
↓
derive candidate facts
↓
duplicate-aware merge
↓
expanded knowledge state
```

まで進んだ。

これにより、

```text
A
+
A → B
```

から、

```text
round 1:
A
B
```

を得た後、
同じ inference を再実行しても、

```text
round 2:
A
B
```

のまま維持できる。

つまり、

```text
known conclusion
```

と、

```text
new conclusion
```

を merge 時に区別する基盤ができた。

現在の pipeline は、

```text
available ProofSteps
↓
matching
↓
InferenceMatch
↓
application
↓
candidate derived ProofSteps
↓
conclusion equality
↓
duplicate filtering
↓
expanded available ProofSteps
```

となっている。

次の自然な段階は、

```text
candidate derived ProofSteps
↓
duplicate filtering
↓
genuinely new ProofSteps
```

を独立に取得できるようにすることである。

これにより、

```text
new ProofSteps が存在する
→ next round

new ProofSteps が存在しない
→ fixed point
```

という termination semantics を明示できる。

その後、

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

という fixed-point iterative inference へ進むことができる。









