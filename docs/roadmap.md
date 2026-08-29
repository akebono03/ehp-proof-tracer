# EHP Proof Tracer Roadmap

## 1. この文書の目的

この文書は、EHP Proof Tracer の将来拡張に関する長期的な設計方針を記録する。

`docs/design.md` が現在採用している仕様と実装境界を記録する文書であるのに対し、
この `docs/roadmap.md` は、まだ未実装の機能を含む将来構想と、その依存関係を整理するための文書とする。

特に、Toda の著作に現れるホモトピー群の計算を将来的に表現・推論できるようにするため、
以下のような代数的・論理的表現と不定性の扱いを段階的に導入する方針を記録する。

- ホモトピー群の加法
- 逆元と符号
- scalar multiplication
- 準同型としての写像
- source / target / ambient homotopy group による型付け
- 集合・部分群・包含関係
- coset / modulo
- symbolic integer / scalar constraint
- 符号・係数・剰余による不定性
- theorem representation
- 仮定・結論・量化
- 存在量化と witness
- 既存テーブルを known fact source として利用する仕組み
- structured generator notation
- iterated suspension `E^t`
- index / degree parameter を持つ Toda bracket
- higher / variable-arity Toda bracket
- Toda bracket の不定性と containment
- fixed-point termination を壊さない arithmetic reasoning

この文書に記載された項目は、記載されているだけでは実装済みを意味しない。
各機能は必要な Phase において個別に仕様化し、
既存 API と推論基盤を壊さない最小変更で導入する。

---

## 2. 現在までの基盤

現在の EHP Proof Tracer では、将来の拡張に利用できる以下の基盤がすでに構築されている。

- 有限生成アーベル群の計算
- `GroupElement`
- `GroupMap`
- `Subgroup`
- kernel / image
- quotient group
- EHP exact sequence
- `Relation`
- `ProofStep`
- `InferenceRule`
- premise pattern matching
- binding の共有
- fixed-point inference
- provenance / dependency chain
- generic ZERO relation
- equality symmetry / transitivity / closure
- ORDER reasoning
- Suspension reasoning
- composition reasoning
- generalized Hopf invariant reasoning

一方で、Proof / Relation の expression layer では、
一般のホモトピー群の加法、不定性、集合値表現、量化された定理、
高次 Toda bracket などはまだ十分に扱っていない。

今後は既存の inference engine を作り直すのではなく、
可能な限り expression / statement / theorem / inference rule / known fact source を追加することで拡張する。

---

## 3. 基本設計原則

### 3.1 不定性を消さずに保持する

Toda 型のホモトピー群計算では、結果が常に一意な元として確定するとは限らない。

例えば次のような情報が現れる。

```text
α = ±β

α ≡ β mod A

α = kβ + γ
k is odd

α ∈ β + A
```

これらを単なる「未確定」として捨ててはいけない。

EHP Proof Tracer では、

```text
値そのものは未確定でも、
その値について判明している制約を保持する
```

ことを基本方針とする。

保持された部分情報は、後続の inference rule の premise として利用できるようにする。

---

### 3.2 数学的対象と表示上の略記を区別する

例えば

```text
±α
```

を単なる文字列として扱うのではなく、

```text
{α, -α}
```

あるいは符号による不定性を持つ数学的対象として意味付けする。

同様に

```text
α ≡ β mod A
```

も文字列として保存するだけではなく、

```text
α - β ∈ A
```

または

```text
α + A = β + A
```

という数学的意味に接続できる構造として設計する。

Toda bracket の

```text
{a, E^t b, E^t c}_t
```

に現れる下付きの `t` も、
単なる表示上の decoration として捨てず、
bracket の構造情報として保持する。

表示用 notation と内部 semantics を分離する。

---

### 3.3 数学的に well-defined な式だけを許す

将来の expression layer では、
式を構築できるだけでなく、その式が数学的に well-defined かを検査する。

例えば、

```text
a + b
```

は `a` と `b` が同じ ambient group の元である場合にのみ定義される。

また、

```text
α ∘ β
```

は source / target が適合する場合にのみ定義される。

expression 構築時または theorem application 時に、
必要な型条件を検証できる設計とする。

---

### 3.4 既存の generic inference engine を優先する

新しい数学的構造を追加するときも、
可能な限り既存の

```text
premise
↓
conclusion
```

という inference rule の枠組みを利用する。

例えば、

```text
α ∈ A
A ⊆ B
↓
α ∈ B
```

や

```text
α = β
↓
f(α) = f(β)
```

といった規則は、現在の fixed-point inference と同じ形式で扱うことを基本とする。

将来機能のためだけに inference engine 全体を特殊化しない。

---

### 3.5 無限生成を避ける

数学的には正しい推論でも、
無制限に結論を列挙すると fixed-point inference が停止しなくなる場合がある。

例えば、

```text
ord(a) = 2
```

から、

```text
2a = 0
4a = 0
6a = 0
8a = 0
...
```

をすべて生成してはいけない。

このような場合は、

```text
ord(a) = n
n divides m
↓
ma = 0
```

という goal-directed reasoning や、
divisibility / annihilator constraint として情報を保持する方法を優先する。

---

### 3.6 将来 Phase の機能を先取りしない

このロードマップは依存関係を示すものであり、
各 Phase ではその Phase に必要な最小限の構造だけを追加する。

例えば Toda bracket を実装する前に、
将来必要になりそうだからという理由だけで、
完全な symbolic algebra system や一般目的の論理体系を先に導入しない。

必要になった時点で、

- expression
- statement
- theorem
- inference rule
- provenance
- regression test

を段階的に追加する。

---

## 4. Typed Homotopy Elements

### 4.1 source / target

将来的に各ホモトピー元について、少なくとも

```text
source sphere
target sphere
```

を追跡できるようにする。

例えば、

```text
α : S^m → S^n
```

という情報を持てば、

```text
α ∈ π_m(S^n)
```

を意味する。

---

### 4.2 ambient homotopy group

各 element について、

```text
ambient_group(α) = π_m(S^n)
```

を明示的または導出可能な情報として扱う。

---

### 4.3 加法の型条件

```text
α + β
```

を構築するためには、

```text
ambient_group(α) = ambient_group(β)
```

が必要である。

例えば、

```text
α ∈ π_8(S^5)
β ∈ π_9(S^5)
```

なら、

```text
α + β
```

は ill-typed / undefined とする。

---

### 4.4 equality の型条件

```text
α = β
```

についても、
原則として同じ ambient group の元同士であることを要求する。

ただし、
既存実装との互換性のため、
導入時には validation の範囲を段階的に拡張する。

---

### 4.5 composition の型条件

```text
α ∘ β
```

について、

```text
target(β) = source(α)
```

を必要条件とする。

これにより、
Toda bracket の定義条件に現れる隣接 composition についても、
型レベルで検証できるようにする。

---

### 4.6 Suspension による型移動

```text
α : S^m → S^n
```

なら、

```text
Eα : S^(m+1) → S^(n+1)
```

として型を移動できるようにする。

iterated suspension では、

```text
E^t α : S^(m+t) → S^(n+t)
```

を表現できるようにする。

---

## 5. Structured Generator Representation

### 5.1 生成元を単なる文字列にしない

Toda の計算では、

```text
η_3
ν'
μ_3
ι_7
\barν
ε
ζ
σ
```

などの記号が頻繁に現れる。

これらを単なる表示文字列として保存するだけではなく、
generator identity を構造化して保持する。

---

### 5.2 generator symbol

概念的には、

```text
GeneratorSymbol
  family
  sphere_dimension / index
  decoration
  source
  target
  ambient_group
```

のような構造を想定する。

---

### 5.3 decoration

Toda 記法に現れる、

```text
prime
bar
tilde
hat
subscript
superscript
```

などが generator identity に必要な場合は、
明示的に保持できるようにする。

例えば、

```text
ν
ν'
\barν
```

を同じ generator name の表示違いとして扱わない。

---

### 5.4 expression との分離

```text
Eν'
```

を新しい generator name として保存するのではなく、

```text
Suspension(ν')
```

として expression で構成する。

同様に、

```text
8ι_7
```

は、

```text
ScalarMultiple(8, ι_7)
```

として表現する。

---

## 6. Algebraic Expression Layer

### 6.1 加法

将来的に、ホモトピー群の元について

```text
α + β
```

を表現できるようにする。

内部表現の候補は例えば、

```text
Sum(α, β)
```

である。

`Sum` は typed expression とし、
項が同じ ambient group に属することを検証する。

---

### 6.2 scalar multiplication

現在存在する

```text
nα
```

という表現は、将来的には一般の群演算体系の一部として整理する。

概念的には、

```text
ScalarMultiple(n, α)
```

として扱う。

既存の ORDER reasoning との互換性を維持する。

---

### 6.3 逆元

将来的に

```text
-α
```

を表現できるようにする。

内部的には、

```text
ScalarMultiple(-1, α)
```

として扱う方法を第一候補とする。

---

### 6.4 ZERO

既存の `Zero()` と、新しい加法表現を整合させる。

将来的には例えば、

```text
α + 0 = α
0 + α = α
α + (-α) = 0
```

のような性質を inference rule または normalization として扱う可能性がある。

ただし、どこまでを rewrite / normalization とし、
どこまでを証明可能な Relation として残すかは、
実装 Phase ごとに判断する。

---

## 7. Homomorphism Reasoning

### 7.1 一般方針

E、H、P などの写像について、
現在は必要な数学的性質を個別の theorem / inference rule として追加している。

将来的に加法が導入された場合、
写像が準同型として作用する場面では、

```text
f(α + β) = f(α) + f(β)
f(nα) = n f(α)
f(-α) = -f(α)
f(0) = 0
```

といった構造を表現できるようにする。

---

### 7.2 E, H, P の扱い

E、H、P を無条件に同じ抽象的準同型として扱わない。

それぞれについて、

- domain / codomain
- 次元条件
- 定義している写像の種類
- generalized Hopf invariant との区別
- unstable / stable な状況
- 文献上成立する条件

を確認しながら theorem rule を追加する。

数学的条件を省略した generic rewrite を導入しない。

---

## 8. Iterated Suspension

### 8.1 `E^t α`

Toda の記法では、反復 suspension

```text
E^t α
```

が頻繁に現れる。

これを単なる文字列として扱わず、
将来的には例えば、

```text
IteratedSuspension(α, t)
```

のような expression として保持する。

---

### 8.2 suspension exponent

`t` は具体的な非負整数だけでなく、
symbolic integer となる可能性も考慮する。

例えば、

```text
E^t α
E^(t+1) α
E^(n-r) α
```

のような表現に拡張できる余地を残す。

---

### 8.3 型情報

```text
α : S^m → S^n
```

なら、

```text
E^t α : S^(m+t) → S^(n+t)
```

を導出可能にする。

---

### 8.4 composition of iterated suspension

必要になった段階で、

```text
E^s(E^t α) = E^(s+t) α
```

のような関係を扱えるようにする。

ただし、
一般的な指数式 simplifier を先に実装するのではなく、
実際の theorem reasoning に必要な範囲から導入する。

---

## 9. ORDER / Annihilator Reasoning

### 9.1 現在の基本形

現在は、

```text
ord(a) = n
↓
na = 0
```

という reasoning を扱う。

---

### 9.2 倍数 ZERO

数学的には、

```text
ord(a) = n
n divides m
↓
ma = 0
```

が成立する。

例えば、

```text
ord(a) = 2
```

なら、

```text
4a = 0
6a = 0
8a = 0
...
```

である。

---

### 9.3 無限列挙を禁止する

上記を fixed-point inference で無制限に列挙しない。

```text
2a = 0
4a = 0
6a = 0
...
```

という無限系列を自動生成すると termination が壊れるためである。

---

### 9.4 推奨する将来設計

以下のいずれか、または組み合わせを検討する。

```text
goal-directed divisibility check
```

```text
Annihilator(a, n)
```

```text
ord(a) = n
```

```text
Divides(n, m)
```

つまり、

```text
query: ma = 0 ?
+
ord(a) = n
+
n divides m
↓
yes
```

という形を優先する。

---

## 10. Set / Subgroup Reasoning

### 10.1 membership

将来的に、

```text
α ∈ A
```

を first-class statement として表現できるようにする。

概念的には、

```text
MembershipStatement(α, A)
```

のような構造を想定する。

---

### 10.2 subset

将来的に、

```text
A ⊆ B
```

を表現できるようにする。

概念的には、

```text
SubsetStatement(A, B)
```

のような構造を想定する。

---

### 10.3 基本推論

例えば、

```text
α ∈ A
A ⊆ B
↓
α ∈ B
```

を generic inference rule として扱えるようにする。

また、

```text
A = B
α ∈ A
↓
α ∈ B
```

など、既存 equality reasoning と接続する。

---

### 10.4 既存 Subgroup との接続

Phase 2 以降で実装済みの `Subgroup`、
kernel、image、quotient group などの低レベル代数構造と、
Proof / Relation の theorem reasoning を接続する。

同じ数学的対象を別々の独立した表現として二重管理しないよう注意する。

---

## 11. Coset / Modulo Reasoning

### 11.1 coset

将来的に、

```text
α + A
```

という coset を表現できるようにする。

これは Toda bracket の indeterminacy を扱う上で重要な基盤となる。

概念的には、

```text
Coset(α, A)
```

のような expression を想定する。

---

### 11.2 modulo relation

将来的に、

```text
α ≡ β mod A
```

を表現できるようにする。

数学的には、

```text
α - β ∈ A
```

あるいは、

```text
α + A = β + A
```

として意味付けできる構造を採用する。

---

### 11.3 表示と内部表現

ユーザー向け表示では、

```text
α = β mod A
```

や

```text
α ≡ β (mod A)
```

のような Toda の文献に近い表記を利用できるようにする。

内部では membership / coset equality など、
より明示的な semantics に接続する。

---

## 12. Symbolic Integer / Scalar Constraints

### 12.1 symbolic integer

将来的に、具体的な整数だけではなく、

```text
k
m
n
t
```

のような symbolic integer variable を binding の対象として扱えるようにする。

例えば、

```text
α = kβ + γ
```

や

```text
E^t β
```

を保持できるようにする。

---

### 12.2 parity constraint

Toda の計算で現れる、

```text
k is odd
```

や

```text
k is even
```

を first-class constraint として表現できるようにする。

概念的には、

```text
Odd(k)
Even(k)
```

のような statement を想定する。

---

### 12.3 divisibility constraint

ORDER reasoning と接続するため、

```text
n divides m
```

を symbolic constraint として扱えるようにする。

概念的には、

```text
Divides(n, m)
```

のような statement を想定する。

---

### 12.4 その他の arithmetic constraint

必要になった場合にのみ、次のような制約を追加する。

```text
k ≠ 0
k > 0
t ≥ 0
gcd(k,n) = 1
k ≡ r mod n
```

ただし、一般的な数式処理システムを先に実装しない。

Toda / EHP の実際の theorem inference に必要な制約から追加する。

---

## 13. Indeterminacy

### 13.1 sign indeterminacy

Toda の文献に現れる、

```text
±α
```

を表現できるようにする。

単なる文字列ではなく、

```text
α または -α
```

という不定性として意味付けする。

---

### 13.2 coset indeterminacy

次のような情報を保持できるようにする。

```text
α ∈ β + A
```

ここでは値を一意に確定させず、
coset に属するという情報そのものを証明結果として扱う。

---

### 13.3 coefficient indeterminacy

次のような結果を保持できるようにする。

```text
α = kβ + γ
k is odd
```

ここで `k` の具体値が不明でも、
奇数であるという情報を失わない。

このような部分情報を後続の inference に利用する。

---

### 13.4 不定性の narrowing

将来的には、複数の証明から得られた制約を組み合わせて、
不定性を狭める推論も可能にする。

例えば、

```text
α ∈ β + A
α ∈ β + B
```

から必要に応じて、

```text
α ∈ β + (A ∩ B)
```

に相当する情報を導く可能性がある。

ただし intersection などの集合演算は、
実際の Toda reasoning で必要になった Phase で追加する。

---

## 14. Theorem Representation

### 14.1 定理をデータとして保持する

将来的には、
数学的定理を単に Python コード内の個別 inference rule として書くだけではなく、
次の構造を持つ theorem data として表現できるようにする。

```text
theorem name
source / provenance
variables
variable types
quantification
assumptions
side conditions
conclusion
```

---

### 14.2 仮定と結論

定理は明示的に、

```text
assumptions
↓
conclusion
```

を持つ。

複数の仮定がある場合も、
現在の複数 premise inference と接続する。

---

### 14.3 typed variables

定理中の変数には必要に応じて型・所属先を持たせる。

例えば、

```text
α ∈ π_n(S^k)
```

を、

```text
α : HomotopyElement
ambient_group(α) = π_n(S^k)
```

のような typed / constrained variable として表現できるようにする。

---

### 14.4 theorem と inference rule の関係

theorem data と inference engine を完全に別体系にしない。

理想的には、

```text
Theorem
↓ compile / instantiate
InferenceRule
↓
ProofStep
```

のように接続する。

---

## 15. Quantifiers

### 15.1 任意の

現在の pattern variable は、
実質的に「マッチする任意の対象」に対する規則として機能している。

将来的にはこれを theorem representation 上で明示できるようにする。

例えば、

```text
for every α ∈ π_n(S^k)
```

を、

```text
∀ α : π_n(S^k)
```

に相当する情報として保持する。

ただし、
内部実装を全面的な一階述語論理系にする必要はない。

多くの場合は、

```text
typed pattern variables
+
side conditions
```

で表現することを優先する。

---

### 15.2 存在する

将来的に、

```text
∃ β, α = 2β
```

のような存在命題を表現できるようにする。

概念的には、

```text
Exists(β, α = 2β)
```

のような statement を想定する。

---

### 15.3 witness

存在命題から後続の推論に利用可能な対象を導入する必要がある場合、
symbolic witness を生成する仕組みを検討する。

概念的には、

```text
∃ β, P(β)
↓
introduce β₀
P(β₀)
```

のような処理である。

ただし witness 導入は現在の forward inference より論理的に一段高度であるため、
実際に必要になる Phase まで導入しない。

---

## 16. Knowledge Tables / Existing Data

### 16.1 既存テーブルは原則として再利用する

過去に作成したホモトピー群テーブルや E/H/P 関連データは、
将来的に利用することを基本方針とする。

ただし、
テーブルそのものを最終的な推論結果として扱うのではなく、

```text
table / database
↓
known fact
↓
Relation / Statement
↓
InferenceRule
↓
derived fact
```

という形で、
既知事実の供給源として利用する。

---

### 16.2 Known group facts

例えば、

```text
π_n(S^k) = G
```

のような既知の群構造を、
known group fact として利用する。

---

### 16.3 Known generator facts

例えば、

```text
π_n(S^k) is generated by α, β, ...
```

のような generator 情報を、
将来の element reasoning に利用する。

structured generator representation と接続する。

---

### 16.4 Known map facts

例えば、

```text
E(α) = β
H(γ) = δ
P(η) = θ
```

のような既知の写像値を、
provenance 付き Relation として利用する。

---

### 16.5 Known order / composition / theorem facts

Toda の文献や既存データから得られる、

```text
ord(α) = n
α ∘ β = γ
H(α) = β
```

などの個別事実も、
known fact source として取り込めるようにする。

---

### 16.6 table lookup と proof generation の分離

長期的には、

```text
query
↓
table lookup
↓
answer
```

だけで終えるのではなく、

```text
known table facts
+
known theorems
+
user assumptions
↓
fixed-point inference
↓
derived conclusion with provenance
```

という形を目標とする。

テーブルは「答えそのもの」ではなく、
proof graph の出発点の一部となる。

---

## 17. Toda Bracket

### 17.1 基本表現

将来的に、

```text
{α, β, γ}
```

という Toda bracket を expression または statement として表現できるようにする。

単純に一つの element を返す関数として設計しない。

---

### 17.2 higher / variable-arity Toda bracket

Toda の議論では、3項だけでなく高次の bracket が現れる。

例えば、

```text
μ_3 ∈ {η_3, Eν', 8ι_7, ν_7}
```

のような式を扱えるようにする。

したがって Toda bracket を、

```text
TodaBracket(a, b, c)
```

という固定3項クラスに限定しない。

概念的には、

```text
TodaBracket(
  entries=(...)
)
```

のように variable arity を持てる構造を第一候補とする。

---

### 17.3 order / degree / arity を混同しない

Toda bracket の、

```text
項数
order
degree
index
```

が記法上似た形で現れる場合でも、
内部では別概念として扱う。

特に「4個の写像が並んでいる」ことと
「3次 Toda bracket」であることを、
単純に同一視しない。

文献上の定義に従って metadata として保持する。

---

### 17.4 membership

Toda bracket は集合値の対象として扱えるようにする。

例えば、

```text
μ_3 ∈ {η_3, Eν', 8ι_7, ν_7}
```

を、

```text
Membership(
  μ_3,
  TodaBracket(...)
)
```

に相当する statement として扱う。

---

### 17.5 indexed Toda bracket

Toda の記法では、

```text
{a, E^t b, E^t c}_t
```

のように、bracket 自体に下付きの index / degree parameter `t` が付く場合がある。

この `t` を表示上の decoration として捨てず、
Toda bracket の構造情報として保持する。

概念的には例えば、

```text
TodaBracket(
  entries=(
    a,
    IteratedSuspension(b, t),
    IteratedSuspension(c, t),
  ),
  index=t,
)
```

のような内部表現を想定する。

---

### 17.6 bracket index と suspension exponent の区別

次の2つは別の情報として保持する。

```text
E^t b
```

に現れる suspension exponent `t` と、

```text
{a, E^t b, E^t c}_t
```

の bracket index `t`。

記法上同じ文字を使う場合でも、
内部では別フィールドとして保持し、
必要な theorem によって両者の一致条件を表現する。

---

### 17.7 stem / dimension metadata

Toda bracket に関して、

```text
9-stem
```

のような情報が必要になる場合に備え、

```text
stem
domain
codomain
source dimensions
target dimension
bracket index
suspension exponents
```

などを metadata または導出可能情報として扱える余地を残す。

ただし、
既存の element type から一意に導出できる情報を重複保持しない。

---

### 17.8 composability / defining conditions

Toda bracket の各 entry について、
隣接する composition が数学的に定義可能かを型情報から検査できるようにする。

また、
bracket の定義条件に必要な zero composition 等を theorem assumptions として明示できるようにする。

---

### 17.9 set-valued nature

Toda bracket は一般に不定性を持つため、
結果を集合または coset として扱える構造が必要となる。

例えば、

```text
{α,β,γ}_t ⊆ δ + A
```

や、

```text
δ ∈ {α,β,γ}_t
```

といった statement を扱えるようにする。

---

### 17.10 indeterminacy

Toda bracket の indeterminacy は、
個別の特殊処理ではなく、
既に導入した

- membership
- subset
- subgroup
- coset
- modulo
- symbolic scalar constraint
- iterated suspension
- typed homotopy elements

の上に構築する。

Toda bracket 専用の ad hoc な文字列表現を増やさない。

---

### 17.11 Toda bracket theorem

Toda bracket に関する theorem は、
将来的には theorem representation を使って、

```text
variables
quantification
typed entries
composition-zero assumptions
dimension / suspension conditions
bracket index conditions
order / degree conditions
conclusion
indeterminacy
```

を明示できるようにする。

---

### 17.12 provenance

Toda bracket の値や包含関係を導出した場合も、
現在の Proof / ProofStep / Relation の provenance を維持する。

例えば、

```text
known composition fact
+
zero composition
+
Toda bracket theorem
↓
μ_3 ∈ {η_3, Eν', 8ι_7, ν_7}
```

のような dependency chain を追跡可能にする。

---

## 18. 入力源の長期構成

長期的には、推論エンジンへ入る知識を大きく次の3種類に分ける。

### 18.1 Known data

```text
homotopy group tables
generator tables
E/H/P map tables
order facts
composition facts
known bracket facts
```

---

### 18.2 Theorems

```text
variables
quantification
assumptions
side conditions
conclusion
source
```

---

### 18.3 User assumptions / query-specific facts

```text
specific α, β, γ
specific dimensions
specific stem
temporary assumptions
target statement
```

これらを最終的には共通の

```text
Statement / Relation / Theorem application
```

へ接続し、
fixed-point inference の入力として利用する。

---

## 19. 推奨する依存順

将来拡張は、概ね次の順番で進める。

```text
Typed homotopy elements
  source / target
  ambient group
        ↓
Structured generators
  η_n, ν', μ_n, ι_n, ...
        ↓
Abelian group expression
  α + β
  -α
  nα
  0
        ↓
Homomorphism reasoning
        ↓
Iterated suspension
  E^t α
        ↓
ORDER / divisibility constraints
        ↓
Set / subgroup reasoning
  α ∈ A
  A ⊆ B
        ↓
Coset / modulo
  α + A
  α ≡ β mod A
        ↓
Symbolic integer / scalar constraints
  kβ
  Odd(k)
  Even(k)
  Divides(n,m)
  t ≥ 0
        ↓
Indeterminacy
  ±α
  α ∈ β + A
  α = kβ + γ, k odd
        ↓
Theorem representation
  assumptions
  conclusion
  typed variables
  quantification
        ↓
Existential statements / witness
        ↓
Knowledge-table integration
        ↓
Toda bracket
  {α,β,γ}_t
  {a,E^t b,E^t c}_t
  higher / variable-arity bracket
  membership
  containment
  indeterminacy
```

これは厳密な Phase 番号ではなく、設計上の依存関係を示す。

実際の Phase 分割は、その時点のコードと必要な theorem scenario に応じて決定する。

---

## 20. 直近 Phase との境界

現在までの Phase では、
EHP / ORDER / Suspension / Composition / generalized Hopf invariant / Sum representation などの
基盤を段階的に実装している。

このロードマップに記載した将来項目を、
既存 Phase に遡って一括導入しない。

各新機能は、
その機能を必要とする Phase で最小限の仕様を定めて導入する。

---

## 21. 実装状況の表記

今後この文書を更新するときは、各大項目について必要に応じて次の状態を記録する。

```text
PLANNED
DESIGNING
IMPLEMENTING
IMPLEMENTED
DEFERRED
```

意味は次の通り。

- `PLANNED`
  - 将来必要と認識しているが、具体的な Phase 仕様は未確定。
- `DESIGNING`
  - 実装前の仕様化を行っている。
- `IMPLEMENTING`
  - 現在の Phase で実装中。
- `IMPLEMENTED`
  - コード・テスト・ドキュメントまで完了している。
- `DEFERRED`
  - 必要性は認識しているが、依存機能または数学的検討のため延期している。

---

## 22. 現時点のロードマップ状態

| 項目 | 状態 | 備考 |
|---|---|---|
| source / target typing | PLANNED | composition / suspension / Toda bracket の基盤 |
| ambient homotopy group | PLANNED | 加法の well-definedness に必須 |
| structured generator notation | PLANNED | prime / bar / 添字等を保持 |
| 一般の加法 `α + β` | PLANNED | 同じ ambient group を要求 |
| 逆元 `-α` | PLANNED | scalar multiplication との統一を検討 |
| 符号不定性 `±α` | PLANNED | set / indeterminacy と統一する |
| E/H/P の準同型性 | PLANNED | 成立条件ごとに theorem rule とする |
| iterated suspension `E^t α` | PLANNED | Toda bracket で重要 |
| order divisor reasoning | PLANNED | 無限 ZERO 列挙を避ける |
| membership `α ∈ A` | PLANNED | Toda bracket の基盤 |
| subset `A ⊆ B` | PLANNED | subgroup reasoning と接続 |
| coset `α + A` | PLANNED | indeterminacy の中心構造 |
| modulo `α ≡ β mod A` | PLANNED | coset / membership と意味を統一 |
| symbolic coefficient `kβ` | PLANNED | 具体的 `nα` から拡張 |
| symbolic suspension exponent `t` | PLANNED | `E^t` と bracket index に利用 |
| `Odd(k)` / `Even(k)` | PLANNED | symbolic constraint |
| `Divides(n,m)` | PLANNED | ORDER reasoning と接続 |
| `α = kβ + γ` | PLANNED | 加法 + symbolic coefficient が前提 |
| theorem representation | PLANNED | 仮定・結論・出典を保持 |
| universal quantification | PLANNED | typed pattern variable を基本に検討 |
| existential statement | PLANNED | witness 導入は後段 |
| knowledge-table integration | PLANNED | known fact source として再利用 |
| Toda bracket `{α,β,γ}_t` | PLANNED | index `t` を first-class に保持 |
| `{a,E^t b,E^t c}_t` | PLANNED | suspension exponent と bracket index を区別 |
| higher / variable-arity Toda bracket | PLANNED | 4項以上も表現可能にする |
| Toda bracket membership | PLANNED | 例 `μ_3 ∈ {...}` |
| stem metadata | PLANNED | 例 `9-stem` |
| Toda bracket composability check | PLANNED | source / target typing と接続 |

---

## 23. 完了時の長期目標

最終的には、EHP Proof Tracer が次のような推論を同じ proof graph 上で扱えることを目標とする。

```text
known homotopy group facts
+
known generator / map tables
+
user assumptions
+
quantified theorems
+
typed homotopy elements
+
EHP exactness
+
ORDER
+
Suspension
+
iterated Suspension
+
composition
+
Hopf invariant
+
group arithmetic
+
subgroup membership
+
modulo / coset
+
symbolic constraints
+
higher Toda bracket
↓
new homotopy-theoretic conclusions
```

その際、結果が完全に一意に決まらない場合でも、

```text
±α
mod A
k odd
E^t α
element of a coset
element of a Toda bracket
subset of an indexed Toda bracket
```

といった不定性や symbolic information を情報として保持し、
さらに後続の theorem inference に接続できることを重要な完成条件とする。

また、

```text
a + b
```

が同じ群の元同士でのみ許されることや、

```text
α ∘ β
```

の source / target が適合することなど、
数学的な well-definedness を expression / theorem application の段階で検証できることも重要な完成条件とする。

EHP Proof Tracer の長期的な方向性は、
単に既知の等式を確認するプログラムではなく、

```text
数学的に判明している情報を、
型・確定値・部分情報・不定性・量化された定理を含めて構造化し、
known data と theorem を接続しながら、
provenance を保った fixed-point inference を行う
```

proof tracer / reasoning system へ発展させることである。
