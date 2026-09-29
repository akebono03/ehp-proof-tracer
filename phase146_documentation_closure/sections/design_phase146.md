# 30. Phase 146 historical Narrative difference audit / root-cause boundary

Phase 146 は、現在の generic Narrative が historical Phase 136-2 の
$\pi_6^3=\mathbb Z/4\{\nu'\}$ Narrative と同等の数学的説明構造を一般規則だけで
再構成できているかを監査した。

Phase 146 の基準 historical commit は

```text
908e24db89669750949fa9ad149f5e306ac05546
```

とする。

## current generic route boundary

現行 $\pi_6^3$ public Narrative は target-specific な route gate を通るが、その gate 内部では

```text
presentation
→ semantic sidecar
→ Narrative blocks
→ Narrative arguments
→ contribution-aware generic renderer
```

を使用する。

Phase 146-5 では current public $\pi_6^3$ output と current generic contribution renderer
output の exact parity を確認した。

これは

```text
current public pi_6^3
=
current generic pi_6^3
```

を意味するが、

```text
current generic pi_6^3
=
historical Phase 136-2 Narrative
```

を意味しない。

したがって route parity と historical quality parity を区別する。

## Phase 146-7 generic prose repair

Phase 146-7 では `render_toda_group_proof_narrative_argument_header_method_section()` に
generic argument-purpose prose fusion を追加した。

従来の

```text
$X$ の位数を決定する.
そのために、次の完全列を考える.
```

を、primary exactness method が argument に対応する場合に

```text
$X$ の位数を決定するために、次の完全列を考える.
```

と一文に統合する。

これは target-specific な $\pi_6^3$ 文面ではなく argument role と method component に基づく
一般表示規則である。

focused regression:

```text
11 passed
```

existing $\pi_6^3$ public-route regression:

```text
4 passed
```

Phase 146-7 では EHP naming、exactness ownership、contribution ordering、Reference prose、
equation numbering は変更していない。

## Phase 146-8 historical full structural diff

Phase 146-8 では historical Phase 136-2 と current generic Narrative を構造比較した。

raw unit inventory:

```text
historical units: 17
current units: 82
PRESERVED: 0
LOST: 17
ADDED: 47
MOVED: 0
DUPLICATED: 35
REWORDED: 0
UNMATCHED: 0

sequence-related units:
historical 4
current 44

[R#] units:
historical 8
current 1
```

ただし historical と current では unit 粒度が異なるため、

```text
PRESERVED=0
LOST=17
```

を「数学的事実が17件失われた」と解釈してはならない。

この audit の有効な結論は、historical と current の文章構造に大きな差があり、
特に exactness の過剰展開、Reference provenance の縮退、重複、配置順の差が
定量的に存在することである。

## Phase 146-9 root-cause classification

Phase 146-9 は production code を変更せず、Phase 146-8 で整理した12の visible difference
families を内部原因へ分類した。

$\pi_6^3$ current argument diagnostics:

```text
establish_group_structure:
  method_evidence=3
  components=1
  primary=True
  primary_windows=3
  contributions=2

establish_order:
  method_evidence=2
  components=1
  primary=True
  primary_windows=2
  contributions=2

establish_definition:
  method_evidence=0
  components=0
  primary=False
  primary_windows=0
  contributions=0
```

したがって order argument の問題は

```text
primary exactness component が存在しない
```

ことではない。

正しくは、

```text
current argument-method ownership / selection
!= historical proof-purpose ownership / explanatory placement
```

である。

また renderer layer では

```text
base multi-argument chars: 1377
contribution-connected chars: 1579
contribution renderer changes output: True
argument builder uses direct dependency indices: True
contribution renderer performs post-render insertion: True
```

を確認した。

## six root causes

Phase 146-8 の12 visible difference families は次の6 root causes に集約する。

### RC1 — Argument-method ownership

historical proof-purpose と current argument-method ownership の差。

主対象:

```text
order argument と主要 EHP 完全列の ownership
method introduction の一部
```

### RC2 — Recursive exactness evidence exposure

primary method に吸収されない recursive exactness evidence が body / contribution として
露出する。

主対象:

```text
主要完全列の範囲選択
補助完全列の本文抑制
exactness contribution 重複の一部
```

### RC3 — Contribution ownership / insertion ordering

argument dependency narration と contribution の ownership / post-render insertion が別経路である。

主対象:

```text
contribution 重複の一部
dependency order に沿った式配置
map-property chain の配置
short exact sequence → group structure の順序
```

### RC4 — Generic provenance / reason prose

compact Reference は保持されても historical の

```text
[R#] の n=... の場合より
```

のような derived-fact reason prose を一般的に再構成できていない。

主対象:

```text
Reference section の詳細
Reference → derived fact の理由付け
definition argument の理由文章の一部
```

### RC5 — EHP semantic naming

generic transition は

```text
次の完全列を考える
```

と表示するが、stored semantics から

```text
EHP 完全列
```

という method family name をまだ一般的に表示しない。

### RC6 — Final equation numbering / prose formatting

equation numbering は selected / ordered Narrative stream の下流にある。

したがって RC1〜RC5 より先に target-specific tag rule で historical numbering を再現してはならない。

## dependency order

修正順序は

```text
RC1
→ RC2
→ RC3
→ RC4
→ RC5
→ RC6
```

とする。

RC6 は selection / ordering の下流なので最後に扱う。

## Phase 146 closure boundary

Phase 146 で実施した production change は Phase 146-7 の generic argument-purpose prose fusion
のみである。

Phase 146-8 / 146-9 は audit only であり、次は変更していない。

```text
pi_6^3 public route gate
exactness ownership
contribution selection
generic provenance rendering
EHP semantic naming
final equation numbering
```

Phase 146 完了時点では $\pi_6^3$ 専用 route gate を削除しない。

Phase 147 以降は上記 root cause を1件ずつ一般規則として扱う。

```text
one root cause
→ minimum general rule
→ focused regression
→ historical/current structural comparison
→ existing proof preservation
```

Phase 146 closure documentation 自体は production semantics を変更しない。
