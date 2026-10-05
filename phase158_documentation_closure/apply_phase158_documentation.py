from pathlib import Path
import shutil

ROOT = Path.cwd()

README = ROOT / "README.md"
DESIGN = ROOT / "docs" / "design.md"
DEVLOG = ROOT / "docs" / "development_log.md"
ROADMAP = ROOT / "docs" / "roadmap.md"
PROOF = ROOT / "docs" / "proof_records.md"

OUTPUT = ROOT / "phase158_documentation_closure" / "output_full_documents"
BACKUP = ROOT / "phase158_documentation_closure" / "backup_before_phase158_docs"

for path in (README, DESIGN, DEVLOG, ROADMAP, PROOF):
    if not path.exists():
        raise FileNotFoundError(path)

OUTPUT.mkdir(parents=True, exist_ok=True)
BACKUP.mkdir(parents=True, exist_ok=True)

for path in (README, DESIGN, DEVLOG, ROADMAP, PROOF):
    rel = path.relative_to(ROOT)
    backup_path = BACKUP / rel
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if not backup_path.exists():
        shutil.copy2(path, backup_path)


def append_once(path: Path, marker: str, section: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + section.strip() + "\n"
    path.write_text(text, encoding="utf-8")


def insert_before_once(
    path: Path,
    marker: str,
    anchor: str,
    section: str,
) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    if anchor in text:
        text = text.replace(
            anchor,
            section.strip() + "\n\n" + anchor,
            1,
        )
    else:
        if not text.endswith("\n"):
            text += "\n"
        text += "\n" + section.strip() + "\n"
    path.write_text(text, encoding="utf-8")


README_SECTION = r'''
<!-- PHASE158_DOCUMENTATION_CLOSURE -->
## Phase 158 closure

Phase 158 unified the public depth-2 Narrative presentation contract without changing the underlying proof graph or theorem facts.

For `max_depth >= 2`, public Narrative now uses one generic multi-argument route rather than selecting a dedicated renderer by group identity. The common route is:

```text
TodaGroupProofPresentation
→ semantic closure
→ semantic sidecar
→ Narrative blocks
→ Narrative arguments
→ contribution-aware multi-argument renderer
→ public wrapper
→ public-contract normalization
```

The normalized public document shell is:

```text
# Group proof narrative

## 証明対象

...

## 使用する結果

...

---

## 証明

...

□
```

Phase 158 also established the following public-presentation rules:

- the Reference section starts directly with the first `[R1]` entry rather than an extra introductory sentence,
- equation numbers are assigned only to visible equations that are actually cited later,
- equation numbering is distinct from proof-item numbering such as `(3), (4) より,`,
- retained equation tags are compact and do not create forward references,
- structured root arguments preserve premise / transport / derivation order before the root conclusion,
- the Web Narrative at depth 2 uses the same public ordering contract,
- legacy dedicated public routes are not used for the full depth-2 public Narrative when the generic structured route is available,
- the final QED marker is the literal `□`.

The Phase 158-R5-6 closure repair verified the integrated R5 contract with:

```text
direct repaired-contract verification:
32 passed

R5 focused closure regression:
45 passed

git diff --check:
PASS
```

A repository-wide pytest was intentionally not run for Phase 158. Phase 158 is closed on the focused public-Narrative verification above.

The next development direction is Phase 159: sequential proof completion from low stems. It starts at `k=1, n=2`, advances in increasing `n`, adds only the general mathematical rules that are actually missing, and stops individual unstable proof expansion once the relevant stable range can be handled by Freudenthal suspension.
'''

DESIGN_SECTION = r'''
<!-- PHASE158_DOCUMENTATION_CLOSURE -->
# Phase 158 設計確定 — public Narrative contract の統一

Phase 158 では数学的 `ProofStep`、theorem fact、proof search を変更対象とせず、public Narrative の表示経路と最終表示契約を統一した。

## public depth-2 route

`max_depth >= 2` の public Narrative は群名による dedicated route 選択を行わず、次の generic route を利用する。

```text
TodaGroupProofPresentation
→ semantic closure
→ semantic sidecar
→ Narrative blocks
→ Narrative arguments
→ contribution-aware multi-argument renderer
→ public wrapper
→ Phase 158 public-contract normalization
```

`max_depth < 2` の direct API fallback は既存互換性のため維持する。

この境界は、

```text
public route unification
!= proof graph rewrite
!= theorem fact replacement
!= new proof search
```

である。

## public document shell

depth 2 以上の public Narrative は最終的に次の shell へ正規化する。

```text
# Group proof narrative

## 証明対象

...

## 使用する結果

...

---

## 証明

...

□
```

`## 使用する結果` の直後に旧来表示されていた

```text
使用する結果を先にまとめる.
```

は削除し、Reference section は `[R1]` から直接開始する。

Reference attribution、fixed statement / proof-internal boundary、Reference numbering 自体はこの shell 正規化では変更しない。

## equation numbering

Phase 158 の equation numbering は、proof-item numbering と明確に分離する。

equation numbering:

```text
\tag{1}
...
(1) より,
```

proof-item numbering:

```text
(3), (4) より,
```

後者は `\tag{N}` との対応を要求しない。

式番号を付与する条件は次である。

```text
1. 現在の Narrative に source equation が実際に表示されている
2. その source が後続 derivation で利用される
3. source equation が citation connector より前に表示される
```

したがって、

```text
structural transition が存在するだけ
→ equation tag を付けない

後続参照がない terminal equation
→ equation tag を付けない

source より先に reference connector が来る
→ forward reference を作らない
```

最終 public normalization では unreferenced / duplicate equation tag を除外し、保持する番号を compact にする。

## generic ordering

Phase 158-R5 では、群固有の `(n,k)` 判定ではなく、

```text
depth >= 2
and
root conclusion を支える structured Narrative Argument が存在する
```

ことを public generic ordering route の条件として用いる。

これにより、たとえば

$$
\pi_7^4
$$

では $\nu_4$ decomposition premise が root group conclusion より前に置かれ、

$$
\pi_{15}^8
$$

では transported decomposition が final group conclusion より前に置かれる。

これは表示順の規則であり、

```text
Narrative ordering
!= ProofStep.premises の変更
!= presentation edge の変更
!= semantic fact の追加
```

である。

## Web boundary

Web Narrative depth 2 は public Markdown と同じ generic route と ordering contract を利用する。

`---` は separator として parse し、terminal `□` は通常 text segment として扱う。

Web adapter は別の数学 engine を持たない。

## Phase 158 closure boundary

Phase 158-R5-6 repair1 後の verification:

```text
direct repaired-contract verification:
32 passed

R5 focused closure regression:
45 passed

git diff --check:
PASS
```

repository-wide pytest は利用者判断により実行しない。

Phase 158 の closure 根拠は public Narrative に直接関係する focused verification とする。

## Phase 159 との境界

Phase 159 は表示統一の続きではなく、数学的 proof coverage の不足を低い stem から順に埋める。

開始順序:

$$
(k,n)=(1,2),(1,3),(1,4),\ldots
$$

その後、

$$
k=2,3,\ldots
$$

へ進む。

各 group 専用規則を追加するのではなく、

```text
current proof replay
→ missing mathematical step の特定
→ 再利用可能な一般規則へ抽象化
→ focused verification
→ 次の n
```

とする。

stable range に達した後は、必要に応じて Freudenthal suspension theorem による suspension isomorphism を利用し、非安定部分を主対象とする。
'''

DEVLOG_SECTION = r'''
<!-- PHASE158_DOCUMENTATION_CLOSURE -->
# Phase 158 — Public Narrative contract unification 完了

Phase 158 は public Narrative の表示方式を群ごとの dedicated / legacy route から、一般的な depth-2 public contract へ統一する Phase として実施した。

数学的 theorem fact、proof graph、proof search を新たに一般化する Phase ではない。

## R1 — Narrative public contract inventory

depth 2 の標準対象について public Narrative shell を監査した。

監査した contract:

```text
# Group proof narrative
## 証明対象
## 使用する結果
## 証明
terminal QED
```

R1 は audit-only であり production code を変更していない。

## R2 — public shell normalization

`toda_group_proof_narrative_renderer.py` に public shell normalization を導入した。

depth 2 以上では renderer route に依存せず、

```text
# Group proof narrative
## 証明対象
## 使用する結果
---
## 証明
□
```

へ正規化する。

この段階では Reference attribution、proof body の数学的 derivation、generic semantic renderer の内容は変更していない。

## R3 — Reference intro normalization

Reference section 冒頭の

```text
使用する結果を先にまとめる.
```

を削除した。

Reference entry、statement、番号、帰属は変更せず、Reference section は `[R1]` から直接開始する契約とした。

旧 intro を固定していた historical test は stale expectation として test-only repair を行った。

## R4 — equation numbering / prose formatting continuity

public Narrative の equation tag と prose connector を監査した。

重要な区別:

```text
equation reference:
\tag{N} ↔ (N) より,

proof-item reference:
(3), (4) より,
```

proof-item numbering を equation reference と誤認しないよう audit / normalization boundary を修正した。

final public equation contract では、

```text
visible source equation
and
later canonical equation reference
```

を満たす式だけを番号付けする。

forward reference、未使用 tag、duplicate tag を public output に残さず、保持する番号は compact にする。

## R5 — public Narrative route unification

R5 の目的は、特定群ごとの表示方式ではなく、どの群でも同じ public Narrative pipeline を利用することだった。

### R5-3 — single generic public route

`max_depth >= 2` の public Narrative を generic multi-argument with contributions route へ一本化した。

```text
TodaGroupProofPresentation
→ semantic closure
→ semantic sidecar
→ blocks
→ arguments
→ contribution-aware multi-argument renderer
→ final public normalization
```

群名による dedicated route dispatch は public baseline から除外した。

`max_depth < 2` の direct API fallback は維持した。

### R5-4 — common equation numbering

route 統一後に equation numbering を再監査した。

代表群監査では、旧 route 差が消えた一方、visible equation と later reference の対応だけを使う共通 numbering rule が必要であることを確認した。

$\pi_8^5$ で検出した forward-reference 問題を一般規則で修正した。

### R5-5 — derivation completeness / ordering

proof body の

```text
premise
→ transport / derivation
→ root conclusion
```

の順序を監査した。

$\pi_7^4$ と $\pi_{15}^8$ について、proof graph / semantic block / Narrative Argument 自体の順序は正しく、public renderer route が表示順を逆転させていることを診断した。

そのため group-specific `(n,k)` 分岐ではなく、

```text
structured root Narrative Argument が存在する
```

ことを generic ordering route の条件として利用した。

Web depth 2 についても同じ ordering を確認した。

## R5-6 — focused closure verification

最初の focused closure regression:

```text
34 passed
11 failed
```

失敗は3系統に分類した。

```text
1. Phase 157 QED expectation:
   production は terminal "□"
   old test は "$\square$"
   → stale expectation

2. pi_6^3 equation numbering:
   tags {1,2,3}
   later references {1,2}
   → production numbering defect

3. Phase 150 prose / dedicated-route expectations:
   old prose 固定
   old pi_8^5 dedicated-route requirement
   → Phase 158 single generic route に対する stale expectation
```

repair1 では production change を equation numbering のみに限定し、後続で実際に参照されない transition target へ番号を付けないよう修正した。

historical test は現在の public contract に合わせて更新した。

最終確認:

```text
direct repaired-contract verification:
32 passed in 16.16s

complete Phase 158-R5 focused closure regression:
45 passed in 20.24s

git diff --check:
PASS
```

これにより Phase 158-R5 を closure とした。

## Phase 158 completion boundary

利用者判断により repository-wide pytest は実行しない。

したがって Phase 158 completion evidence は、

```text
R1-R5 focused audits / repairs
+
R5-6 direct repaired-contract verification: 32 passed
+
R5-6 focused closure regression: 45 passed
+
git diff --check: PASS
```

である。

repository-wide all-pass は claim しない。

Phase 158 完了。

## 次 Phase

Phase 159 は `k=1, n=2` から開始する sequential proof completion とする。

```text
k=1:
n=2 → n=3 → n=4 → ...

その後:
k=2 → k=3 → ...
```

各点で current proof を実際に生成し、不足する数学的 statement / rule があれば、群専用 special case ではなく再利用可能な一般規則として追加する。

非安定部分を主対象とし、stable range 到達後は Freudenthal suspension theorem による同型移送で処理できる境界を監査する。
'''

ROADMAP_SECTION = r'''
<!-- PHASE158_DOCUMENTATION_CLOSURE -->
# Phase 158 完了後ロードマップ

## 現在地

Phase 158 `Public Narrative contract unification` 完了。

Phase 158 で確定した public depth-2 contract:

```text
TodaGroupProofPresentation
→ semantic closure
→ semantic sidecar
→ Narrative blocks
→ Narrative arguments
→ contribution-aware generic renderer
→ public normalization
```

最終 shell:

```text
# Group proof narrative
## 証明対象
## 使用する結果
---
## 証明
□
```

追加で確定した規則:

```text
Reference section は [R1] から直接開始
depth >= 2 public Narrative は single generic route
equation numbering != proof-item numbering
later reference のない式には equation tag を付けない
forward equation reference を作らない
structured root Argument の dependency order を public / Web で維持
legacy dedicated public route を full depth-2 contract の基準にしない
```

Phase 158-R5-6 最終 focused verification:

```text
direct repaired-contract:
32 passed

R5 focused closure:
45 passed

git diff --check:
PASS
```

repository-wide pytest は利用者判断により実行しない。

---

# Phase 159 — Sequential proof completion from low stems

## 目的

Phase 159 は「現在登録されている群を一括分類する Phase」ではない。

実際に低い stem から順番に proof を生成し、証明に不足する一般規則を発見した時だけ追加する。

開発順序そのものを数学的順序に合わせる。

最初は:

$$
k=1
$$

について

$$
n=2,3,4,\ldots
$$

と進む。

すなわち開始点は

$$
\pi_3^2
$$

である。

$k=1$ の非安定部分と stable boundary を処理できた後に、

$$
k=2,3,\ldots
$$

へ進む。

## Phase 159-R1 — $k=1,n=2$ starting-point audit

最初に current repository の既存規則だけで

$$
\pi_3^2
$$

の proof replay / public Narrative を生成する。

確認するもの:

```text
root conclusion まで証明が到達するか
必要な premise が proof graph に存在するか
semantic rendering が不足していないか
fallback が proof gap を隠していないか
literature statement が不足していないか
群専用表示 route に依存していないか
```

不足がなければ $n=3$ へ進む。

## missing-rule の処理原則

ある $(k,n)$ で証明が止まった場合:

```text
failure / missing derivation
→ 数学的に不足する statement を特定
→ 他の群にも適用できる一般規則か確認
→ minimum generic rule を実装
→ focused verification
→ 同じ群を再確認
→ 次の n
```

禁止:

```text
その群だけ通す n/k hardcoding
将来の k で必要かもしれない規則の先取り
proof provenance と無関係な説明文による穴埋め
一般 evaluator の無制限導入
```

## stable boundary

このプロジェクトの主対象は unstable homotopy groups（非安定ホモトピー群）である。

したがって各 $k$ について、

```text
lowest n
→ unstable proof を順番に完成
→ stable boundary を確認
→ それ以降は Freudenthal suspension theorem による同型移送
```

という終了条件を検討する。

stable 判定の一般 API を先に作って全群へ適用するのではなく、sequential proof audit から実際に必要になった時点で最小限実装する。

## Phase 159 の想定 progression

```text
159-R1:
k=1, n=2 starting-point audit

159-R2以降:
n を1ずつ増やす
↓
最初の proof gap を分類
↓
必要なら generic rule を1つ追加
↓
focused verification
↓
次の n

k=1 closure
↓
k=2
↓
同じ手順
```

Phase 159 は固定された「112群」を母集団として設計しない。

今後 repository に群が増えても同じ $(k,n)$ の数学的走査規則で進められる構成とする。

## test boundary

利用者方針により repository-wide pytest は自動的には実行しない。

各 repair では、その一般規則に直接関係する focused verification を使用する。

---

# 最新の直近順序

```text
Phase 158 documentation closure
→ Phase 159-R1: k=1, n=2 starting-point audit
→ k=1 を n 昇順で sequential proof completion
→ stable boundary まで到達
→ k=2 へ
```
'''

PROOF_SECTION = r'''
<!-- PHASE158_DOCUMENTATION_CLOSURE -->
# Phase 158 public Narrative contract provenance record

Phase 158 は新しい Toda theorem fact を追加することを主目的とした Phase ではない。

対象は existing proof provenance を public Narrative として表示する際の route、shell、equation linkage、derivation ordering の統一である。

## provenance ground truth

Phase 158 後も数学的 ground truth は引き続き:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
LiteratureReference
```

である。

Phase 158 の public contract はこれらを表示する presentation policy であり、

```text
public route unification
!= theorem unification

shell normalization
!= proof rewrite

equation numbering
!= mathematical inference

Narrative ordering
!= premise-edge mutation
```

である。

## public shell provenance boundary

depth 2 以上では route に依存せず:

```text
# Group proof narrative
## 証明対象
## 使用する結果
---
## 証明
□
```

を public shell とする。

`## 使用する結果` の導入文を削除しても `LiteratureReference`、Reference entry、statement、番号、consumer relation は保持される。

## single generic route provenance

`max_depth >= 2` の public Narrative は generic multi-argument / contribution route を利用する。

```text
presentation
→ semantic closure
→ semantic sidecar
→ blocks
→ arguments
→ contributions
→ public Narrative
```

これは existing proof graph を別の graph に置換するものではない。

旧 dedicated helper がコード上に残っていても、full public depth-2 route の数学的根拠は同じ stored provenance から取得する。

## equation linkage provenance

equation number は visible proof fact の identity ではなく、現在の Narrative 内で後続 derivation が参照するための local display label である。

したがって:

```text
visible source + later reference
→ \tag{N}

transition target であるだけ
→ tag 不要

terminal conclusion
→ later reference がなければ tag 不要
```

proof-item numbering は別 presentation structure であり、equation tag identity と混同しない。

## ordering provenance

$\pi_7^4$ と $\pi_{15}^8$ の診断では、

```text
proof graph ordering
semantic block ordering
Narrative Argument ordering
```

は成立していた。

public output だけが root conclusion を早く表示する route を通っていたため、structured root Argument の存在を generic ordering route の条件とした。

したがって ordering repair は、

```text
existing dependency order
→ public output へ忠実に反映
```

したもので、新しい dependency を追加していない。

## R5-6 closure record

initial focused closure:

```text
34 passed
11 failed
```

failure classification:

```text
stale Phase 157 QED expectation
production equation-numbering defect
stale Phase 150 prose / dedicated-route expectations
```

production repair は equation-numbering function のみに限定した。

terminal / unreferenced transition target を numbering set へ追加しないことで、

```text
generated equation tags
=
equations actually referenced later
```

という current contract を回復した。

最終 verification:

```text
direct repaired-contract:
32 passed in 16.16s

R5 focused closure:
45 passed in 20.24s

git diff --check:
PASS
```

repository-wide pytest は実行していないため、Phase 158 について repository-wide all-pass は provenance record として claim しない。

## next provenance pressure

Phase 159 は presentation route ではなく mathematical proof coverage を扱う。

開始点:

$$
\pi_3^2
$$

すなわち

$$
k=1,\quad n=2.
$$

以後 $n$ を増やしながら existing proof provenance の不足を調べる。

不足する規則が見つかった場合のみ、群固有の special case ではなく、既存文献事実と proof structure に基づく再利用可能な一般規則を追加する。

stable range では Freudenthal suspension theorem による同型移送を利用できる境界を必要に応じて導入する。
'''

insert_before_once(
    README,
    "<!-- PHASE158_DOCUMENTATION_CLOSURE -->",
    "## Current boundaries",
    README_SECTION,
)

append_once(
    DESIGN,
    "<!-- PHASE158_DOCUMENTATION_CLOSURE -->",
    DESIGN_SECTION,
)
append_once(
    DEVLOG,
    "<!-- PHASE158_DOCUMENTATION_CLOSURE -->",
    DEVLOG_SECTION,
)
append_once(
    ROADMAP,
    "<!-- PHASE158_DOCUMENTATION_CLOSURE -->",
    ROADMAP_SECTION,
)
append_once(
    PROOF,
    "<!-- PHASE158_DOCUMENTATION_CLOSURE -->",
    PROOF_SECTION,
)

for path in (README, DESIGN, DEVLOG, ROADMAP, PROOF):
    rel = path.relative_to(ROOT)
    output_path = OUTPUT / rel
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, output_path)

checks = {
    "README English Phase 158 section": (
        "<!-- PHASE158_DOCUMENTATION_CLOSURE -->"
        in README.read_text(encoding="utf-8")
        and "## Phase 158 closure"
        in README.read_text(encoding="utf-8")
    ),
    "design Phase 158 section": (
        "# Phase 158 設計確定"
        in DESIGN.read_text(encoding="utf-8")
    ),
    "development log Phase 158 closure": (
        "# Phase 158 — Public Narrative contract unification 完了"
        in DEVLOG.read_text(encoding="utf-8")
    ),
    "roadmap Phase 159 start": (
        "Phase 159-R1: k=1, n=2 starting-point audit"
        in ROADMAP.read_text(encoding="utf-8")
    ),
    "proof record Phase 158": (
        "# Phase 158 public Narrative contract provenance record"
        in PROOF.read_text(encoding="utf-8")
    ),
}

failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise RuntimeError(
        "documentation self-check failed: " + ", ".join(failed)
    )

print("Phase 158 documentation closure applied.")
print("")
print("Updated full files:")
for path in (README, DESIGN, DEVLOG, ROADMAP, PROOF):
    print("  -", path.relative_to(ROOT))
print("")
print("Full updated copies:")
for path in (README, DESIGN, DEVLOG, ROADMAP, PROOF):
    print(
        "  -",
        (OUTPUT / path.relative_to(ROOT)).relative_to(ROOT),
    )
print("")
print("pytest: NOT RUN (per user instruction)")
