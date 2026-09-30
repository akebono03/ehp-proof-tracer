---

<!-- PHASE150_CLOSURE -->
# Phase 150 完了 / Phase 151 以降の計画

## Phase 150 — 完了

Phase 150 / RC4 `Generic provenance / reason prose` は完了した。

完了根拠:

```text
typed reason semantics established
visible reason multiplicity contract established
six representative groups audited
final nine-failure repair focused regression: 17 passed
final full regression: 10478 passed
```

最終全体回帰:

```text
10478 passed in 2505.44s (0:41:45)
pytest exit code: 0
```

Phase 150 の重要な architectural conclusion は、段階的な group-by-group generic route
移行をここで止めることである。

複数 renderer の共存中に個別群を順番に切り替えると、route 差と generic rule の欠陥を
切り分けにくい。

---

# Phase 151 — All-Group Generic Baseline

## 目的

対象群全体を同じ generic Narrative route へ通した baseline を取得する。

public route はまだ変更しない。

## Phase 151-1

現行コードと関連 test を確認し、対象 population 全体を generic renderer へ強制的に通す
audit harness の feasibility を確認する。

production behavior は変更しない。

## baseline で記録する項目

少なくとも次を群ごとに記録する。

```text
generic render success / failure
rendered length
Narrative blocks
Narrative arguments
semantic categories
typed reasons
OTHER blocks
raw / rule-name / type fallback
renderer exception
```

必要に応じて snapshot を保存する。

## Phase 151 の禁止事項

```text
group-specific prose repair
group-specific route exception
public renderer switch
dedicated renderer deletion
legacy renderer deletion
future Phase の defect repair
```

Phase 151 は観測と基準線確立に限定する。

---

# Phase 152 — Generic defect classification

Phase 151 baseline を入力として、generic output の問題を種類ごとに分類する。

例:

```text
selection
ownership
ordering
reason prose
semantic naming
fallback
formatting
result reuse
```

個別群の名前を defect category の代わりにしない。

Phase 152 では「どの一般規則が不足しているか」を決める。

---

# Phase 153 以降 — one general defect per Phase

Phase 152 で確定した defect を1種類ずつ修正する。

各修正後に対象 population 全体の generic baseline を再生成し、局所改善が他群を壊していないかを
確認する。

```text
one defect category
→ minimum general rule
→ focused tests
→ all-group generic regeneration
```

群固有 special case は追加しない。

---

# Public route unification

generic route が全体 population で必要な品質を満たした後、public renderer selection を
一度に generic route へ統一する。

その後に dedicated / legacy route の削除可否を判断する。

```text
generic quality established
→ one-shot public route switch
→ canonical regression
→ dedicated / legacy retirement audit
```

route 削除を先取りしない。

---

# Test Suite Consolidation

Phase 150 final full regression は約42分を要した。

今後は full historical suite を毎 Phase の必須作業にしない。

標準:

```text
focused tests
→ implementation / repair

canonical regression
→ Phase closure

complete historical regression
→ major integration / release milestone
```

別途 Test Suite Consolidation を行い、次を分類する。

```text
current canonical contract
historical compatibility
audit-only
superseded snapshot
duplicate coverage
performance-heavy integration
```

目的は単純な test 数削減ではなく、現在の仕様を十分に保証しながら通常の開発 feedback loop を
短縮することである。

---

# 直近順序

```text
Phase 150 documentation closure
→ Phase 151 All-Group Generic Baseline
→ Phase 152 Generic defect classification
→ Phase 153+ one general defect per Phase
→ public generic route unification
→ dedicated / legacy retirement audit
```
