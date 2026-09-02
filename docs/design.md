# EHP Proof Tracer 設計

この文書は、EHP Proof Tracer の現在の architecture、semantics、設計境界を記録する。

historical な実装経緯は `docs/development_log.md`、将来構想は `docs/roadmap.md` に分離する。

```text
README.md
=
現在できること / 現在の状態

docs/design.md
=
現在の architecture / semantics / boundaries

docs/development_log.md
=
時系列の実装履歴

docs/roadmap.md
=
将来機能と依存関係
```

---

# 1. 基本設計原則

EHP Proof Tracer は次の順序で拡張する。

```text
実際の数学的必要
↓
必要最小限の表現
↓
explicit fact / domain rule
↓
既存 generic inference engine
```

generic engine を先に一般化しない。

新しい数学的 theorem / knowledge を導入するときは、それを generic mechanism と混同しない。

---

# 2. layer separation

主要 layer:

```text
literature-backed theorem facts / repository
explicit generator facts / repository
explicit composition facts / repository
explicit map facts / repository
        ↓
homotopy / EHP / map-property domain rules
        ↓
generic proof / inference engine
        ↓
proof-level expressions / statements
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
```

重要な分離:

```text
MapSymbol
!=
MapTypingFact
!=
MapIsomorphismFact
!=
IsomorphismStatement
```

```text
GeneratorSymbol
!=
GeneratorTypingFact
!=
GeneratorAmbientGroupFact
```

```text
representation
!=
typing
!=
theorem knowledge
```

---

# 3. Expression model

現在の主要 expression:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── SmashProduct
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

`SmashProduct` は Phase 31 で追加した structural syntax である。

```text
SmashProduct(
  left=a,
  right=b,
)
```

は:

```text
a ∧ b
```

を lossless に保持する。

---

# 4. structural equality と theorem equality

frozen dataclass の structural equality は syntax tree の一致を意味する。

例えば:

```text
SmashProduct(a,b)
==
SmashProduct(a,b)
```

一方:

```text
SmashProduct(a,b)
!=
SmashProduct(b,a)
```

である。

これは smash product の数学的非可換性を主張しているのではない。

```text
different syntax tree
→
structurally distinct
```

というだけである。

将来 theorem により二つの expression が等しいことが分かる場合は、`RelationType.EQUALITY` と `ProofStep` を用いて proof-level equality として表現する。

---

# 5. typing boundary

`HomotopyElement` は必要に応じて source / target を保持できる。

`Suspension` は内部 expression の typing が得られる場合に source / target を持つ。

しかし `SmashProduct` は Phase 32 完了時点でも source / target typing を持たない。

したがって:

```text
c : S^m → S^n
```

であっても、

```text
c ∧ c
```

の source / target を自動生成しない。

さらに:

```text
E(c∧c).source = None
E(c∧c).target = None
```

である。

重要:

```text
Prop.2.2 の式に E(c∧c) が現れる
↛
E(c∧c) の typing が実装済み
```

---

# 6. theorem applicability と hidden knowledge

notation から hidden theorem knowledge を作らない。

例えば:

```text
GeneratorSymbol(family="eta", index=3)
```

を見ただけで source / target を自動決定しない。

同様に:

```text
SmashProduct(c,c)
```

を見ただけで Barratt–Hilton formula を適用しない。

また:

```text
type-compatible
```

であることから:

```text
composition = 0
```

を自動導出しない。

基本原則:

```text
representable
≠
valid
```

```text
type-compatible
≠
zero composition
≠
Toda definedness
```

---

# 7. actual H map identity

production Hopf map identity:

```text
HOPF_MAP
=
EHP_H_MAP
=
MapSymbol(name="H")
```

この identity は canonical object として扱う。

actual-H theorem rule / bridge が conclusion を作る場合、単に同じ名前を持つ新しい `MapSymbol("H")` を作るのではなく、production `EHP_H_MAP` を直接使用する。

したがって regression では:

```text
step.conclusion.lhs.map is HOPF_MAP
```

のように object identity まで確認する。

---

# 8. generalized HopfInvariantStatement と actual H equality

`HopfInvariantStatement`:

```text
H(alpha)=beta
```

は generalized Hopf invariant の statement family であり、map identity を直接保持しない。

actual H equality は:

```text
Relation(
  lhs=MapApplication(
    map=HOPF_MAP,
    expression=alpha,
  ),
  rhs=beta,
  relation_type=EQUALITY,
)
```

で表現する。

両者は意図的に別 family とする。

bridge:

```text
HopfInvariantStatement
↓
hopf_invariant_statement_to_ehp_h_equality_inference_rule()
↓
actual H equality
```

---

# 9. Toda Prop.2.2 の current semantics

[Toda] Prop.2.2:

```text
H(a ∘ Eb)=H(a) ∘ Eb

H((Ec) ∘ a)=E(c ∧ c) ∘ H(a)
```

Phase 30 / 32 完了後は、両式とも direct theorem rule として扱う。

---

# 10. Toda Prop.2.2 右側 direct theorem

production rule:

```text
toda_prop22_right_inference_rule(
  alpha=a,
  gamma=b,
)
```

結論:

```text
H(a∘Eb)=H(a)∘Eb
```

premises:

```text
()
```

つまり:

```text
H(a)=β
```

は Prop.2.2 本体の premise ではない。

actual H identity は conclusion builder で canonical `EHP_H_MAP` を直接使う。

---

# 11. Toda Prop.2.2 左側 direct theorem

production rule:

```text
toda_prop22_left_inference_rule(
  alpha=a,
  gamma=c,
)
```

結論:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

構造:

```text
lhs:
MapApplication(
  map=EHP_H_MAP,
  expression=Composition(
    left=Suspension(c),
    right=a,
  ),
)
```

```text
rhs:
Composition(
  left=Suspension(
    SmashProduct(c,c)
  ),
  right=MapApplication(
    map=EHP_H_MAP,
    expression=a,
  ),
)
```

premises:

```text
()
```

---

# 12. direct theorem と specialization の分離

Phase 30 / 32 の途中では、既知の:

```text
H(a)=β
```

を使って formula を構成し、最後に equality reasoning で `H(a)` へ戻す経路を実装した。

これは現在、Prop.2.2 本体の証明経路とは解釈しない。

current semantics:

```text
Toda Prop.2.2
↓
direct theorem equality
```

と:

```text
H(a)=β
↓
specialized concrete-value reasoning
```

は別である。

β-based path は次の目的で残す。

```text
generalized Hopf machinery
actual-H bridge
equality symmetry
staged composition congruence
equality transitivity
```

の integration / consistency regression。

最終結果が direct theorem と一致することを regression で確認する。

---

# 13. right specialization path

既知:

```text
H(a)=β
```

から:

```text
H(a∘Eb)=β∘Eb
```

を generalized Hopf machinery で得られる。

また:

```text
H(a)=β
↓ symmetry
β=H(a)
↓ staged right composition
β∘Eb=H(a)∘Eb
```

を得られる。

transitivity:

```text
H(a∘Eb)=β∘Eb
β∘Eb=H(a)∘Eb
↓
H(a∘Eb)=H(a)∘Eb
```

この最終結果が direct theorem の conclusion と一致する。

---

# 14. left specialization path

既知:

```text
H(a)=β
```

と `c` から:

```text
H((Ec)∘a)=E(c∧c)∘β
```

を generalized Hopf machinery で得られる。

また:

```text
H(a)=β
↓ symmetry
β=H(a)
↓ staged left composition
E(c∧c)∘β=E(c∧c)∘H(a)
```

を得られる。

transitivity:

```text
H((Ec)∘a)=E(c∧c)∘β
E(c∧c)∘β=E(c∧c)∘H(a)
↓
H((Ec)∘a)=E(c∧c)∘H(a)
```

これも direct theorem の conclusion と一致する。

---

# 15. composition congruence の staged execution

right-composition equality:

```text
x=y
↓
x∘z=y∘z
```

left-composition equality:

```text
x=y
↓
z∘x=z∘y
```

は expression growth を生む。

例えば left-composition rule を unrestricted fixed point に常駐させると:

```text
x=y
↓
z∘x=z∘y
↓
z∘(z∘x)=z∘(z∘y)
↓
...
```

となり得る。

したがって current design では staged one-shot application とする。

```text
structural growth rule
→
scenario-specific staged execution
```

generic fixed-point rule set に無条件で常駐させない。

---

# 16. Phase 32 capability

Phase 32 の canonical capability:

```text
a, c
↓
Toda Prop.2.2
↓
H((Ec)∘a)=E(c∧c)∘H(a)
```

proof object:

```text
rule = ProofRule.INFERENCE
premises = ()
inference_rule.name =
  "Toda Prop.2.2 left formula"
```

canonical actual H identity:

```text
lhs H is HOPF_MAP
rhs H is HOPF_MAP
```

---

# 17. Phase 32 representative probe

実行:

```powershell
python -m probes.probe_phase32_capabilities
```

表示する主要情報:

```text
Theorem:
H((Ec)∘a)=E(c∧c)∘H(a)
```

```text
premises: none
```

```text
Structural confirmation:
lhs correct = True
rhs correct = True
actual H map preserved = True
```

typing boundary:

```text
SmashProduct has source: False
SmashProduct has target: False
E(c∧c).source = None
E(c∧c).target = None
```

---

# 18. Phase 32 regression policy

最終 representative regression は direct theorem を主役とする。

確認:

1. direct theorem を premise なしで適用可能。
2. conclusion が exact structural formula。
3. lhs actual H identity。
4. rhs actual H identity。
5. `Ec` の Suspension structure。
6. `E(c∧c)` の Suspension + SmashProduct structure。
7. SmashProduct typing は未実装のまま。
8. β specialization は別 regression で direct theorem と一致。
9. generic engine 変更なし。

---

# 19. Phase 30 design correction

Phase 32 direct theorem 化に合わせて Phase 30 も同じ設計へ修正した。

旧説明:

```text
H(a)=β
↓
...
↓
H(a∘Eb)=H(a)∘Eb
```

current explanation:

```text
Toda Prop.2.2
↓
H(a∘Eb)=H(a)∘Eb
```

β branch は specialization / integration test とする。

これにより Prop.2.2 左右の theorem semantics が対称になった。

---

# 20. current non-goals

Phase 32 完了時点でも未実装:

```text
general SmashProduct typing
general smash-product algebra
SmashProduct normalization
Barratt-Hilton theorem knowledge
symbolic (-1)^n expression tree
parity reduction of symbolic signs
Toda Prop.3.1
actual H((2ι₂)η₂) evaluation
actual H((2ι₂)η₂)=H(4η₂)
actual (2ι₂)η₂=4η₂
```

Toda (2.1) foundational composition laws も未実装。

Toda (5.1) foundational sphere-group facts も concrete need に応じて導入する。

---

# 21. Barratt–Hilton への設計境界

長期目標:

```text
(2ι₂)η₂=4η₂
```

想定 chain:

```text
H((2ι₂)η₂)
↓ Toda Prop.2.2 left
E(2ι₁∧2ι₁)H(η₂)
↓ Toda Prop.3.1 / required smash-product facts
4ι₃
```

一方:

```text
H(4η₂)
↓ homomorphism
4H(η₂)
↓ H(η₂)=ι₃
4ι₃
```

よって:

```text
H((2ι₂)η₂)=H(4η₂)
```

Phase 29 machinery:

```text
Isomorphism(H)
↓
Injective(H)
```

により:

```text
(2ι₂)η₂=4η₂
```

へ反射する。

---

# 22. 次 Phase の候補

Phase 32 の次は、Toda Prop.3.1 Barratt–Hilton に実際に必要な prerequisite を最小単位で導入する。

有力候補:

```text
symbolic scalar expression
(-1)^n
```

および parity reduction:

```text
n even
↓
(-1)^n=1
```

```text
n odd
↓
(-1)^n=-1
```

既存 `IteratedSuspension` は再利用し、Barratt–Hilton の具体的 typing requirement が現れた場合にのみ拡張する。

---

# 23. generic-engine boundary

Phase 32 では generic inference engine を変更していない。

今後も:

```text
domain-specific mathematical requirement
↓
existing generic mechanism では表現不能
```

が確認された場合のみ generic feature を追加する。

---

# 24. テスト原則

新しい数学的 layer ごとに:

1. representation
2. structural distinction
3. validity / applicability
4. invalid case
5. typing compatibility
6. integration
7. provenance
8. representative scenario
9. termination / scope
10. full regression
11. human-readable executable probe

を確認する。

---

# 25. Phase 32 完了時点の verified status

```text
tests/test_phase30_prop22.py
25 passed
```

```text
tests/test_phase32_prop22.py
39 passed
```

```text
tests/test_hopf_rules.py
31 passed
```

```text
tests/test_map_facts.py
54 passed
```

```text
full suite
1512 passed in 63.58s
```

No failures.

---

# 26. 文書運用方針

```text
README.md
=
current capabilities / current status

docs/design.md
=
current architecture / semantics / boundaries

docs/development_log.md
=
chronological implementation history

docs/roadmap.md
=
future capability dependency
```

historical limitation と current limitation を混同しない。

current specification は latest README / design を優先する。
