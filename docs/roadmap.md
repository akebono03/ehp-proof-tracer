# EHP Proof Tracer 繝ｭ繝ｼ繝峨・繝・・

縺薙・譁・嶌縺ｯ **莉雁ｾ後・ capability dependency 縺ｨ Phase 鬆・ｺ・*繧定ｨ倬鹸縺吶ｋ縲・
迴ｾ蝨ｨ縺ｮ莉墓ｧ倥・ `README.md` / `docs/design.md` 繧貞━蜈医＠縲・℃蜴ｻ縺ｮ隧ｳ邏ｰ縺ｪ螳溯｣・ｱ･豁ｴ縺ｯ `docs/development_log.md`縲∽ｻ｣陦ｨ險ｼ譏弱・infrastructure record 縺ｯ `docs/proof_records.md` 繧貞盾辣ｧ縺吶ｋ縲・
---

# 1. 譁・嶌驕狗畑譁ｹ驥・
roadmap 縺ｯ future-oriented 縺ｫ菫昴▽縲・
螳御ｺ・ｸ医∩ Phase 縺ｮ隧ｳ邏ｰ縺ｪ subphase縲’ocused test縲（mplementation history 縺ｯ roadmap 縺ｫ闢・ｩ阪○縺壹［ilestone summary 縺ｮ縺ｿ縺ｫ蝨ｧ邵ｮ縺吶ｋ縲・
```text
README.md
= current status / current capability

docs/design.md
= current architecture / semantics / boundaries

docs/development_log.md
= chronological implementation history

docs/code_reference.md
= current code navigation / public infrastructure

docs/proof_records.md
= representative mathematical proof records
  + infrastructure records

docs/roadmap.md
= future plan / dependency / deferred boundary
```

---

# 2. 髢狗匱蜴溷援

```text
螳滄圀縺ｮ謨ｰ蟄ｦ逧・ｿ・ｦ・/ capability need
竊・current code / related tests audit
竊・譌｢蟄・semantics / API compatibility
竊・荳崎ｶｳ縺励※縺・ｋ譛蟆・representation / orchestration
竊・focused implementation
竊・actual integration
竊・applicability / provenance / safety
竊・representative probe
竊・full regression
竊・completion documentation
```

蜴溷援:

```text
future Phase 縺ｮ framework 繧貞・蜿悶ｊ縺励↑縺・譌｢蟄・API 繧剃ｸ榊ｿ・ｦ√↓螢翫＆縺ｪ縺・generic theorem prover 蛹悶＠縺ｪ縺・representation 縺ｨ theorem knowledge 繧呈ｷｷ蜷後＠縺ｪ縺・險ｺ譁ｭ邨先棡縺ｨ螳溯｡檎ｵ瑚ｷｯ繧剃ｸ閾ｴ縺輔○繧・repository 縺ｯ譏守､ｺ縺励↑縺・剞繧企撼遐ｴ螢・```

---

# 3. 螳御ｺ・ｸ医∩ milestone summary

```text
Phase 1窶・7
generic proof / algebra / Toda-bracket foundation

Phase 28窶・8
actual H branch
PrimaryComponent / TodaPrimaryGroup
WhiteheadProduct
Toda Lemma 4.1
Proposition 4.2
Toda (4.5)
Proposition 4.4

Phase 49窶・3
ﾎｷ-family / ﾎｽ-family concrete branch
Proposition 5.1
Lemma 5.2
Proposition 5.3
Lemma 5.4
Lemma 5.5
Toda (5.5)
Toda (5.6)

Phase 64
performance stabilization

Phase 65窶・7
Toda Chapter V finite-dimensional continuation
Proposition 5.6
Equation (5.8)
Lemma 5.7
Proposition 5.8
Equation (5.10)
Proposition 5.9
Equation (5.12)
Lemma 5.10 canonical correction
Proposition 5.11
Lemma 5.12
Proposition 5.15
Equation (5.16)
Lemma 5.16

Phase 78
stable G_0 through G_7 consolidation

Phase 79
minimal in-memory Proof Repository

Phase 80
repository-assisted automatic inference
with explicitly supplied rules

Phase 81
automatic goal-compatible rule selection

Phase 82
one-level goal-directed missing-premise production

Phase 83
multiple one-level producers

Phase 84
bounded depth=2 producer search / execution
shared dependency reuse

Phase 85
search-failure diagnostics
execution-failure diagnostics
unified bounded-search report
integrated selected-path execution
actual Toda Lemma 5.16 verification

Phase 86-1
hard-coded depth=2 compatibility audit

Phase 86-2
explicit max_depth parameterization
max_depth=2 Phase 85 compatibility
representative compatibility probe
```

Phase 86-2 completion repository-wide regression:

```text
6969 passed in 34.72s
```

Wall-clock time is machine-dependent because development is performed on multiple PCs. Test count, semantics, provenance coverage, and focused regression remain the primary cross-machine signals.

---

# 4. 迴ｾ蝨ｨ縺ｮ謨ｰ蟄ｦ capability

Low stable stems:

```text
G_0=Z{ﾎｹ}

(G_1;2)=Z/2{ﾎｷ}
(G_2;2)=Z/2{ﾎｷﾂｲ}
(G_3;2)=Z/8{ﾎｽ}
(G_4;2)=0
(G_5;2)=0
(G_6;2)=Z/2{ﾎｽﾂｲ}
(G_7;2)=Z/16{ﾏマ
```

Toda Lemma 5.16 縺ｾ縺ｧ縺ｮ concrete proof spine 縺ｯ provenance 莉倥″縺ｧ formalized 縺輔ｌ縺ｦ縺・ｋ縲・
莉｣陦ｨ actual theorem:

```text
Toda Lemma 5.16 final bracket-sum consequence
```

縺ｯ迴ｾ蝨ｨ:

```text
initial repository facts
竊・automatic bounded search
竊・selected producer dependency DAG
竊・integrated execution
竊・final ProofStep
```

縺ｨ縺励※蜀榊ｰ主・蜿ｯ閭ｽ縲・
---

# 5. 迴ｾ蝨ｨ縺ｮ proof-search capability

迴ｾ蝨ｨ縺ｮ high-level flow:

```text
goal
竊・goal-compatible final-rule selection
竊・missing-premise analysis
竊・bounded producer search
竊・search-failure diagnostics
竊・execution-failure diagnostics
竊・unified report
竊・exact selected-path execution
竊・goal ProofStep
```

迴ｾ蝨ｨ縺ｮ bounded search:

```text
explicit max_depth API present
currently supported max_depth = 2
unique producer policy
shared producer identity deduplication
dependency-first execution
producer max_rounds = 1
repository non-mutation
```

default call 縺ｨ explicit call:

```text
default
=
max_depth=2
```

Phase 85/86 status model:

```text
SUCCESS
GOAL_ALREADY_AVAILABLE

NO_FINAL_RULE
AMBIGUOUS_FINAL_RULE
NO_PRODUCER
UNSAFE_PRODUCER
AMBIGUOUS_PRODUCER
CYCLE_DETECTED
DEPTH_LIMIT

PRODUCER_NOT_APPLICABLE
PRODUCER_OUTPUT_NOT_USABLE
FINAL_RULE_NOT_APPLICABLE
GOAL_NOT_DERIVED
```

Actual Toda Lemma 5.16 representative path:

```text
final
笏懌楳 bracket-sum              depth 1 and 2
笏披楳 composition              depth 1
   笏披楳 bracket-sum           depth 2
```

shared bracket-sum:

```text
depths = (1, 2)
is_shared = True
```

Phase 86-2 regression confirms default behavior and explicit `max_depth=2` behavior are identical in selected path, dependencies, diagnostics, execution result, and provenance.

---

# 6. 迴ｾ蝨ｨ縺ｮ螳牙・蠅・阜

Phase 86-2 螳御ｺ・凾轤ｹ縺ｧ諢丞峙逧・↓譛ｪ螳溯｣・

```text
max_depth > 2
arbitrary recursive producer search
retry / backtracking
multiple alternative-path planning
producer ranking
proof-cost model
best-proof selection
DFS / BFS / A*
mathematical-equivalence goal normalization
persistent search cache
persistent Proof Repository
automatic proof narrative generation
generic theorem prover
```

縺薙ｌ繧峨・莠偵＞縺ｫ迢ｬ遶九＠縺・capability 縺ｨ縺励※謇ｱ縺・・
迚ｹ縺ｫ:

```text
depth parameterization
!=
depth > 2 search
!=
backtracking
!=
ranking
!=
general theorem proving
```

繧堤ｶｭ謖√☆繧九・
---

# 7. 谺｡ Phase・啀hase 86-3 bounded depth > 2

Phase 86-1 / 86-2 縺ｯ COMPLETE縲・
Phase 86-3 縺ｮ逶ｮ逧・・縲￣hase 86-2 縺ｧ蝗ｺ螳壹＠縺・`max_depth=2` compatibility 繧貞｣翫＆縺壹∵怏髯舌↑ explicit depth limit 縺ｮ遽・峇縺ｧ depth > 2 縺ｮ荳諢・producer chain 繧呈桶縺医ｋ繧医≧縺ｫ縺吶ｋ縺薙→縲・
譛蛻昴°繧・arbitrary recursive theorem search 繧貞ｮ溯｣・＠縺ｪ縺・・
## Phase 86-3 譛蟆・target

譛蛻昴・莉｣陦ｨ synthetic dependency:

```text
final
竊・depth 1 producer
竊・depth 2 producer
竊・depth 3 producer
```

蜷後§ dependency 縺ｫ蟇ｾ縺励※:

```text
max_depth=2
竊・DEPTH_LIMIT

max_depth=3
竊・success
```

繧貞ｯｾ縺ｧ遒ｺ隱阪☆繧九・
## 蠢・・invariant

```text
finite explicit max_depth
cycle-safe
unique producer policy preserved
shared dependency identity preserved
deterministic dependency-first ordering
diagnostic context preserved
exact selected-path execution
ProofStep provenance preserved
repository non-mutation
```

Phase 86-2 baseline:

```text
default
=
max_depth=2
```

縺ｯ regression 縺ｧ邯咏ｶ壼崋螳壹☆繧九・
## Phase 86-3 縺ｧ蜷梧凾蟆主・縺励↑縺・ｂ縺ｮ

```text
retry / backtracking
producer ranking
proof-cost model
best-proof selection
DFS / BFS / A*
alternative path retry
generic theorem prover
```

---

# 8. Phase 86 莉･髯阪・蛻･蛟呵｣・
Phase 86 縺ｨ迢ｬ遶九＠縺ｦ縲∝ｰ・擂莉･荳九ｒ讀懆ｨ弱〒縺阪ｋ縲・
## Alternative producer planning

迴ｾ蝨ｨ:

```text
distinct producer ambiguity
竊・stop
```

蟆・擂蛟呵｣・

```text
multiple safe producer alternatives
竊・explicit planning policy
```

縺溘□縺・ranking / cost model 縺悟ｿ・ｦ√↓縺ｪ繧九∪縺ｧ蜈亥叙繧翫＠縺ｪ縺・・
## Retry / backtracking

迴ｾ蝨ｨ:

```text
selected unique path fails execution
竊・diagnostic failure
```

蟆・擂蛟呵｣・

```text
execution failure
竊・alternative path retry
```

縺薙ｌ縺ｯ depth parameterization 縺ｨ縺ｯ蛻･ Phase 縺ｨ縺吶ｋ縲・
## Proof ranking / cost model

蟆・擂蛟呵｣・

```text
multiple valid proofs
竊・cost / provenance / depth policy
竊・preferred proof
```

迴ｾ蝨ｨ縺ｯ荳崎ｦ√・
---

# 9. Persistent Proof Repository / search cache

迴ｾ蝨ｨ縺ｮ `ProofRepository` 縺ｯ process-local in-memory catalog縲・
generated proof steps 縺ｯ repository 縺ｫ閾ｪ蜍慕匳骭ｲ縺輔ｌ縺ｪ縺・・
蟆・擂 persistence 繧貞ｰ主・縺吶ｋ蝣ｴ蜷医∝ｰ代↑縺上→繧・

```text
typed conclusion
ProofRule
premise edges
inference-rule identity
literature provenance
repository metadata
schema / semantic compatibility version
```

繧剃ｿ晏ｭ倥☆繧句ｿ・ｦ√′縺ゅｋ縲・
迴ｾ蝨ｨ縺ｯ:

```text
DEFERRED
```

persistent search cache 縺ｨ persistent Proof Repository 縺ｯ蜷御ｸ capability 縺ｨ縺ｿ縺ｪ縺輔↑縺・・
---

# 10. Automatic proof narrative generation

迴ｾ蝨ｨ:

```text
proof inference       = automatic
proof provenance      = automatic
bounded proof search  = automatic through depth 2
explicit max_depth    = implemented for value 2
diagnostics           = automatic
proof records         = human curated
probe narrative       = hand-authored
```

蟆・擂 target:

```text
ProofStep graph
+ Expression tree
+ InferenceRule provenance
+ LiteratureStatement
+ search diagnostic / execution metadata
竊・relevant-path extraction
竊・step grouping / compression
竊・equation-chain generation
竊・citation insertion
竊・console / Markdown / LaTeX narrative
```

formal mathematical proof records 縺ｯ迴ｾ蝨ｨ13莉ｶ縲・
Phase 79窶・6 infrastructure records 縺ｯ謨ｰ蟄ｦ逧・proof record 縺ｨ縺ｯ蛻･縺ｫ邂｡逅・☆繧九・
迥ｶ諷・

```text
DEFERRED
```

---

# 11. 險ｼ譏手ｨ倬鹸

謨ｰ蟄ｦ逧・formal proof records:

```text
13
```

infrastructure records:

```text
Phase 79
Phase 80
Phase 81
Phase 82
Phase 83
Phase 84
Phase 85
Phase 86

total = 8
```

Phase 86 infrastructure record 縺ｯ:

```text
hard-coded depth=2 audit
explicit max_depth=2 compatibility
representative compatibility probe
Phase 86-3 boundary
```

繧定ｨ倬鹸縺吶ｋ縲・
---

# 12. 諤ｧ閭ｽ譁ｹ驥・
Phase 64 same-machine baseline:

```text
3657 passed in 259.11s
竊・3657 passed in 29.97s
```

Phase 86-2 final regression:

```text
6969 passed in 34.72s
```

逡ｰ縺ｪ繧輝C髢薙・ wall-clock time 繧偵さ繝ｼ繝画ｧ閭ｽ縺ｮ逶ｴ謗･豈碑ｼ・↓菴ｿ逕ｨ縺励↑縺・・
performance regression 縺碁｡戊送縺ｫ縺ｪ縺｣縺溷ｴ蜷医・縺ｿ:

```text
pytest duration
cProfile
repeated builder reconstruction
premise matching
algebra crosscheck
```

繧貞・隱ｿ譟ｻ縺吶ｋ縲・
heavy deterministic builder 縺悟酔縺・object graph 繧堤ｹｰ繧願ｿ斐＠蛻ｩ逕ｨ縺吶ｋ蝣ｴ蜷医・:

```python
@lru_cache(maxsize=1)
```

繧貞━蜈医☆繧九・
---

# 13. 菫晉蕗荳ｭ縺ｮ荳闊ｬ蛹・
謨ｰ蟄ｦ / representation:

```text
general existential quantification
general witness / uniqueness framework
generic sign algebra
generic Toda-bracket coset algebra
generic symbolic dimension solver
generic map typing solver
generic stable theorem engine
stable ring machinery
```

proof search:

```text
unbounded / arbitrary recursion
backtracking
alternative-path planning
ranking
cost model
best-proof selection
DFS / BFS / A*
```

storage / presentation:

```text
persistent Proof Repository
persistent search cache
proof graph serialization
automatic proof narrative generation
```

縺薙ｌ繧峨・ concrete need 縺檎匱逕溘＠縺滓凾轤ｹ縺ｧ蛟句挨 Phase 縺ｨ縺励※險ｭ險医☆繧九・
---

# 14. 迴ｾ蝨ｨ蝨ｰ轤ｹ

```text
mathematical frontier:
Toda Lemma 5.16
stable G_0 through G_7

proof infrastructure frontier:
bounded depth=2 producer search
explicit max_depth=2
search / execution diagnostics
unified report
integrated selected-path execution

repository-wide regression:
6969 passed in 34.72s
```

谺｡縺ｮ髢狗匱髢句ｧ狗せ:

```text
Phase 86-3
bounded depth > 2
```

Phase 86-3 縺ｧ繧よ怙蟆丞､画峩蜴溷援繧堤ｶｭ謖√＠縲￣hase 86-2 縺ｮ explicit `max_depth=2` 螳悟・莠呈鋤繧・regression baseline 縺ｨ縺吶ｋ縲・
