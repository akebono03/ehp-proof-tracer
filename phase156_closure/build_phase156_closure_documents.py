from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

DOCUMENTS = (
  ROOT / "README.md",
  ROOT / "docs" / "design.md",
  ROOT / "docs" / "development_log.md",
  ROOT / "docs" / "roadmap.md",
  ROOT / "docs" / "proof_records.md",
)

OUTPUT_ROOT = (
  ROOT
  / "phase156_closure_output"
  / "documents"
)


README_SECTION = r"""
## Phase 156 closure

Phase 156 refined public Reference statement display without changing the underlying Toda proof facts, proof graph, theorem roots, stable-range mathematics, or proof-search semantics.

The phase established a general minimal-display contract for selected References:

- the Reference theorem / lemma itself continues to be selected by the existing proof-ancestry rules,
- public statement selection prefers boundary-crossing consumers and then entry-external consumers,
- same-Reference internal intermediate statements do not expand the public Reference entry unnecessarily,
- a body `[R#]` marker must always have a matching public Reference header,
- a public Reference header does not require an explicit body `[R#]` marker when the Reference is retained by proof-graph usage,
- a final public canonical Reference statement must not be repeated verbatim in the proof body,
- Reference statement selection remains graph-backed rather than group-specific.

The Phase 156 cross-group audit covered

$$
n=2,\ldots,15,
\qquad
k=0,\ldots,7,
$$

for a total of 112 group queries at proof depth 2.

The final Phase 156-R5 audit reported:

```text
groups: 112
exceptions: 0
non_contiguous_reference_headers: 0
body_marker_without_header: 0
boundary_selection_mismatch: 0
entry_external_selection_mismatch: 0
same_entry_internal_public_expansion: 0
exact_reference_body_restatement: 0
total required violations: 0
```

Phase 156-R6 then partitioned the same 112-group population into four independent shards of 28 groups each. The aggregate result was:

```text
shards: 4 / 4
groups: 112
unique groups: 112
duplicate groups: 0
missing groups: 0
unexpected groups: 0
exceptions: 0
violations: 0
```

The 15 header-without-explicit-marker occurrences across four groups are informational, not violations: their final public Reference statements have graph-backed external consumers and are not duplicated in the proof body.

Phase 156 does not introduce new theorem facts, new proof edges, a new evaluator, new stable-range mathematics, or a new proof-search mechanism.
""".strip()


DESIGN_SECTION = r"""
# Phase 156 Reference minimal-display 設計境界

Phase 156 では、選択済み Reference の内部でどの statement を public 表示するかを一般規則として整理した。

## 基本責務

Reference 表示は次の2段階に分ける。

```text
Reference theorem / lemma selection
→ 既存 proof ancestry に基づく Reference entry selection

statement selection inside Reference
→ Phase 156 minimal-display rule
```

Phase 156 は前者を作り直さない。

## statement selection

選択候補は、同じ LiteratureReference を持つ proof steps のうち public statement candidate として描画可能なものから選ぶ。

優先順は次のとおり。

```text
1. Reference boundary を越えて直接消費される statement
2. Reference entry の外側から消費される statement
3. 上記が無い場合の既存 fallback
```

同じ Reference entry 内だけで使われる intermediate statement を理由に、public statement を複数へ過剰展開しない。

## public Reference / proof body contract

必須 contract:

```text
body [R#]
→ matching public Reference header

public canonical Reference statement
→ proof body exact duplicate を持たない
```

非必須 contract:

```text
public Reference header
→ explicit body [R#] marker
```

後者を必須にしない理由は、generic Narrative renderer が proof-graph usage によって Reference entry を保持する正式経路を持つためである。

したがって、

```text
header without marker
!= unused Reference
```

である。

ただし、graph-backed consumer が存在せず、statement selection invariant も満たさない Reference を許容するという意味ではない。

## ownership

Phase 156 の ownership 判定は最終 public 表示の Reference header と filtering / renumbering 前の graph entry を locator / label により対応付けて確認する。

```text
final public [R#]
→ final public Reference title
→ original graph entry
→ selected ProofStep
→ external consumer
```

この対応により、再採番後の `[R#]` と元 entry number を同一視しない。

## Phase 156 で変更しないもの

```text
Toda theorem fact
ProofStep conclusion
ProofStep premise edge
proof search
operation evaluator
stable-range theorem data
Reference theorem / lemma selection policy
```

Phase 156 の変更対象は Reference statement granularity と presentation contract に限定する。

## regression boundary

R5 final audit:

```text
112 groups
exceptions = 0
required violations = 0
```

R6 sharded regression:

```text
4 shards
28 groups / shard
112 unique groups
duplicates = 0
missing = 0
exceptions = 0
violations = 0
```

repository-wide pytest は Phase 156 closure でのみ実行する。
""".strip()


DEVELOPMENT_LOG_SECTION = r"""
# Phase 156 — Reference statement relevance / minimal display

Phase 156 は、Phase 153 で選択した Reference theorem / lemma の内部について、証明に必要な statement だけを public 表示する一般規則を整理した。

## R1 — duplicate inventory / classification

112群を対象に Reference statement と proof body の重複を棚卸しした。

初期分類:

```text
groups: 112
exceptions: 0
duplicates: 117

unnecessary_duplicate: 11
body_restatement_required: 3
reference_side_overfull: 103
```

117件のうち大半が Reference 側の過剰 statement 表示であることを確認した。

## R2 — consumer usage audit

Reference statement の consumer を proof graph から分類した。

```text
reference_side_overfull: 103
boundary_direct_consumer: 18
internal_consumer_only: 85
no_consumer: 0
aggregate_component_only: 0
```

public 表示で必要な statement と、同一 Reference 内部だけで使う intermediate statement を分離する必要があることを確認した。

## R3 — minimal statement selection

Reference entry 内の statement selector を一般化した。

優先順:

```text
1. boundary direct consumer
2. entry-external consumer
3. existing fallback
```

same-entry internal usage だけでは public statement を複数へ展開しない。

112群監査:

```text
groups: 112
exceptions: 0
selection violations: 0
Reference entries: 228
selected statements: 238
multi-statement References: 20
max statements / Reference: 3
```

## R4 — proof-body duplicate suppression

Reference に表示した statement と proof body の exact restatement を抑制する一般 helper を導入した。

最終監査:

```text
groups: 112
exceptions: 0
suppressible exact restatements: 0
```

## R5 — cross-group Reference minimal-display audit

R5 では当初、`Reference header -> explicit body [R#] marker` も必須と仮定したが、generic route の proof-graph usage と一致しないことが判明した。

4群:

$$
\pi_6^3,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{16}^9
$$

について final public Reference header を filtering / renumbering 前の graph entry へ逆対応した。

確認結果:

```text
exceptions: 0
unmatched public headers: 0
final public statement proof-body occurrences: 0
graph-backed external consumers: present
```

したがって最終 contract は、

```text
body [R#] -> matching header
```

を必須とし、

```text
header -> explicit body [R#]
```

は必須にしない。

R5 final:

```text
groups: 112
exceptions: 0
public Reference groups: 93
public Reference headers: 147
body Reference markers: 143
header without marker: 15 occurrences / 4 groups (informational)
canonical selected statements: 238
displayed canonical statements: 158

non_contiguous_reference_headers: 0
body_marker_without_header: 0
boundary_selection_mismatch: 0
entry_external_selection_mismatch: 0
same_entry_internal_public_expansion: 0
exact_reference_body_restatement: 0

Total required violations: 0
```

## R6 — focused / sharded regression

112群を4 shardへ分割した。

```text
4 shards
28 groups / shard
```

各 shard は $n=2,\ldots,15$ をすべて含み、各 $n$ について2つの $k$ を担当する。

focused regression:

```text
sharding contract: 3 passed
Reference selection / granularity / body regression: 12 passed
Phase153 public Reference audit-only regression: 1 passed
```

shard result:

```text
shard 1: groups=28 exceptions=0 violations=0
shard 2: groups=28 exceptions=0 violations=0
shard 3: groups=28 exceptions=0 violations=0
shard 4: groups=28 exceptions=0 violations=0
```

aggregate:

```text
shards: 4 / 4
groups: 112
unique groups: 112
duplicate groups: 0
missing groups: 0
unexpected groups: 0
exceptions: 0
violations: 0
```

## closure boundary

Phase 156 closure では、この記録と設計文書を更新した後に repository-wide pytest を1回だけ実行する。

Phase 157 の機能は Phase 156 では先取りしない。
""".strip()


ROADMAP_SECTION = r"""
# Phase 156 完了境界と Phase 157 以降

## Phase 156 — Reference statement relevance / minimal display

Phase 156 の実装・監査項目:

```text
R1 duplicate inventory / classification
R2 consumer usage audit
R3 minimal Reference statement selection
R4 proof-body duplicate suppression
R5 112-group cross-group audit
R6 focused / sharded regression
closure documentation + repository-wide pytest
```

R5 / R6 で確定した public Reference contract:

```text
body [R#] -> matching header: required
header -> explicit body [R#]: not required
boundary / entry-external statement selection: required
same-entry internal over-expansion: forbidden
final public Reference / proof-body exact duplicate: forbidden
```

R6 時点:

```text
112 unique groups
4 shards x 28 groups
exceptions = 0
violations = 0
```

Phase 156 closure の repository-wide pytest が成功すれば Phase 156 完了とする。

## Phase 157 境界

Phase 157 では Phase 156 の Reference minimal-display contract を変更しない。

次 Phase の具体的対象は、Phase 156 closure 後の現行 Narrative を改めて監査して決める。

特に Phase 156 中には次を先取りしない。

```text
new theorem fact
new stable-range mathematics
new proof search
new operation evaluator
new Reference ranking
new theorem ranking
group-specific Reference display exception
```

EHP Proof Tracer の主目的は unstable range の proof tracing であり、stable range は既存結果を表示し Freudenthal suspension へ接続できる範囲を基本境界とする。
""".strip()


PROOF_RECORDS_SECTION = r"""
# Phase 156 Reference minimal-display provenance record

Phase 156 は新しい数学的 theorem fact を追加した Phase ではない。

目的は、既存 `ProofStep` provenance から選択済みの LiteratureReference について、public Narrative に表示する statement の粒度と proof body との ownership を整理することだった。

## provenance source

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive proof ancestry
```

である。

Phase 156 の Reference statement selection はこの proof graph の consumer relation を読む。

```text
Reference display selection
!= new theorem inference

Reference statement suppression
!= ProofStep deletion

public Reference renumbering
!= original graph-entry renumbering
```

## selection provenance

public statement candidate は、同一 LiteratureReference に属する proof steps のうち semantic rendering 可能な候補から選択する。

優先する provenance:

```text
boundary-crossing consumer
→ first priority

entry-external consumer
→ second priority

same-entry internal consumer only
→ public over-expansion の根拠にしない
```

この規則は特定の群名ではなく proof graph relation に基づく。

## final public numbering provenance

filtering 後の public `[R#]` は表示上の番号である。

したがって、

```text
final public [R1]
!= original graph entry number 1
```

の場合がある。

Phase 156-R5 では final public Reference title を locator / label で元 graph entry に逆対応し、ownership を確認した。

対象:

$$
\pi_6^3,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{16}^9.
$$

結果:

```text
unmatched public headers = 0
exceptions = 0
final public statement proof-body occurrences = 0
entry-external graph consumers = present
```

したがって、この4群で explicit body `[R#]` marker が無い Reference header は unused Reference ではない。

## public contract

必須:

```text
body [R#]
→ matching public Reference header
```

非必須:

```text
public Reference header
→ explicit body [R#]
```

後者は generic renderer の graph-backed Reference retention と両立しないため必須にしない。

ただし、

```text
header without marker
!= arbitrary unused Reference allowed
```

である。

R3 statement-selection invariant と graph consumer relation により Reference relevance を確認する。

## duplicate provenance

final public canonical Reference statement と proof body の exact duplicate は表示上の ownership 重複として扱う。

```text
public Reference statement
+
same exact proof-body statement
→ suppressible display duplication
```

これは theorem fact を削除することではない。

```text
display suppression
!= proof fact deletion
!= proof edge deletion
```

## R5 final audit record

```text
groups: 112
exceptions: 0
public Reference groups: 93
public Reference headers: 147
body Reference markers: 143
header without marker: 15 occurrences / 4 groups (informational)
canonical selected statements: 238
displayed canonical statements: 158

non_contiguous_reference_headers: 0
body_marker_without_header: 0
boundary_selection_mismatch: 0
entry_external_selection_mismatch: 0
same_entry_internal_public_expansion: 0
exact_reference_body_restatement: 0

Total required violations: 0
```

## R6 sharded provenance record

population:

```text
n=2..15
k=0..7
112 groups
```

partition:

```text
4 shards
28 groups / shard
```

aggregate:

```text
shards: 4 / 4
groups: 112
unique groups: 112
duplicate groups: 0
missing groups: 0
unexpected groups: 0
exceptions: 0
violations: 0
```

この結果は Reference minimal-display rule が代表群専用ではなく、112群の現行監査母集団で同じ一般規則として成立していることを示す。

ただし、

```text
112-group presentation audit
!= all homotopy groups proved
!= all stems complete
!= stable homotopy theorem completeness
```

である。

Phase 156 closure では repository-wide pytest を最後に1回実行し、その結果をこの provenance boundary の最終 regression evidence とする。
""".strip()


def _normalize_newlines(
  text: str,
) -> str:
  return text.replace(
    "\r\n",
    "\n",
  ).replace(
    "\r",
    "\n",
  )


def _append_section_once(
  text: str,
  marker: str,
  section: str,
) -> str:
  normalized = _normalize_newlines(
    text
  ).rstrip()

  if marker in normalized:
    return (
      normalized
      + "\n"
    )

  return (
    normalized
    + "\n\n"
    + section
    + "\n"
  )


def build_documents() -> tuple[
  Path,
  ...,
]:
  OUTPUT_ROOT.mkdir(
    parents=True,
    exist_ok=True,
  )

  sections = {
    ROOT / "README.md": (
      "## Phase 156 closure",
      README_SECTION,
    ),
    ROOT / "docs" / "design.md": (
      "# Phase 156 Reference minimal-display 設計境界",
      DESIGN_SECTION,
    ),
    ROOT / "docs" / "development_log.md": (
      "# Phase 156 — Reference statement relevance / minimal display",
      DEVELOPMENT_LOG_SECTION,
    ),
    ROOT / "docs" / "roadmap.md": (
      "# Phase 156 完了境界と Phase 157 以降",
      ROADMAP_SECTION,
    ),
    ROOT / "docs" / "proof_records.md": (
      "# Phase 156 Reference minimal-display provenance record",
      PROOF_RECORDS_SECTION,
    ),
  }

  outputs = []

  for source_path in DOCUMENTS:
    if not source_path.exists():
      raise FileNotFoundError(
        str(
          source_path
        )
      )

    marker, section = sections[
      source_path
    ]
    current = source_path.read_text(
      encoding="utf-8",
    )
    updated = _append_section_once(
      current,
      marker,
      section,
    )

    relative = source_path.relative_to(
      ROOT
    )
    output_path = (
      OUTPUT_ROOT
      / relative
    )
    output_path.parent.mkdir(
      parents=True,
      exist_ok=True,
    )
    output_path.write_text(
      updated,
      encoding="utf-8",
      newline="\n",
    )
    outputs.append(
      output_path
    )

  return tuple(
    outputs
  )


def apply_documents() -> tuple[
  Path,
  ...,
]:
  outputs = build_documents()

  for output_path in outputs:
    relative = output_path.relative_to(
      OUTPUT_ROOT
    )
    target = (
      ROOT
      / relative
    )
    target.write_text(
      output_path.read_text(
        encoding="utf-8",
      ),
      encoding="utf-8",
      newline="\n",
    )

  return outputs


def main() -> int:
  outputs = apply_documents()

  print(
    "Phase156 closure documents written as full files:"
  )

  for output_path in outputs:
    print(
      "  "
      + str(
        output_path
      )
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
