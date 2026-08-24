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








