# Phase 148 RC2-2 — Minimal General Exposure Rule Design

## 1. 目的

Phase 147 / RC1 で確立した Argument 単位の exactness method ownership（完全性論証手段の所有関係）を利用し、
recursive exactness evidence（再帰的に到達した完全性証拠）を main Narrative（本文）へ表示するかを一般規則として定義する。

RC2-2 は設計のみを行う。production code は変更しない。

## 2. 現行挙動

現行の `filter_toda_group_proof_narrative_exactness_body_contributions()` は次のように動作する。

1. `primary_component is None` の場合、すべての contribution を本文候補として保持する。
2. block が primary component の evidence block でない場合、すべての contribution を本文候補として保持する。
3. block が primary component の evidence block の場合、`EXACTNESS_WINDOW` を抑制する。
4. `DERIVED_SHORT_EXACT_SEQUENCE` 等の非 window contribution は保持する。

RC2-1 では、この 1 と 2 により recursive evidence が本文へ露出することを確認した。

## 3. RC2-1 から得られた分類

### 3.1 Owned primary method

Argument の relevant group に直接関係し、Phase 147 の ownership selection によりその Argument の primary exactness component として選択される component。

例:
- $\pi_6^3$ group structure
- $\pi_6^3$ order
- $\pi_{12}^5$ group structure

### 3.2 Unowned recursive evidence

Argument の method evidence traversal では到達するが、その Argument の relevant group に直接関係する primary component として所有されない component。

RC2-1 で確認された例:
- $\pi_8^5$ group structure
- $\pi_8^5$ 一部の order
- $\pi_{10}^4$ group structure
- $\pi_{12}^5$ definition
- $\pi_{16}^9$ group structure / definition

これらは proof graph / provenance には必要だが、その Argument 自身の主要 method として本文へ自動展開する根拠はない。

## 4. 最小一般規則

### Rule E1 — Provenance preservation

exactness evidence は exposure 判定によって proof graph / provenance から削除しない。

RC2 が変更するのは main Narrative への exposure のみとする。

### Rule E2 — Ownership before exposure

exactness component を main Narrative の method evidence として露出するには、
その component が現在の Argument に owned（所有）されていることを必要条件とする。

ownership は新しい heuristic ではなく、Phase 147 で確立した relevant groups と
exactness component の semantic relation（意味的関係）から判定する。

### Rule E3 — Owned primary component

現在の Argument が一意の primary exactness component を所有する場合、
その component の evidence block は現在の Phase 143 規則を維持する。

- raw `EXACTNESS_WINDOW` は本文で重複表示しない。
- `DERIVED_SHORT_EXACT_SEQUENCE` のような既存の higher-level contribution
  （上位の表示用寄与）は保持する。

したがって $\pi_6^3$ の現在の short exact sequence 表示は RC2 により削除しない。

### Rule E4 — Unowned recursive component

method evidence traversal により到達した component であっても、
現在の Argument がその component を owned primary method として所有しない場合、
その component の contribution は原則 main Narrative へ自動展開しない。

ただし evidence 自体は provenance に残す。

### Rule E5 — `primary is None` is not itself the policy

`primary_component is None` だけを理由に全 evidence を隠してはならない。

`None` には少なくとも次の可能性がある。

1. relevant component が 0 個
2. relevant component が複数あり一意に選べない

したがって RC2-3 の API は単なる

`primary_component: Component | None`

だけで exposure を決めず、各 component/block が現在の Argument に owned / directly relevant かを判定できる入力を持つべきである。

複数の directly relevant component が存在する曖昧ケースを RC2 で勝手に削除してはならない。
その場合は conservative fallback（保守的フォールバック）として既存表示を維持する。

### Rule E6 — No new mathematical heuristic

RC2 では次のような新規 heuristic を導入しない。

- Argument role ごとの特例
- $\pi_6^3$ 等の特定群の特例
- block index による判定
- LaTeX 文字列による判定
- depth 固有の特例

判定材料は既存 semantic ownership / relevance / component structure に限定する。

## 5. RC2-3 に必要な最小 API 形

RC2-3 では production code の変更を次の責務に限定する。

### A. component exposure classification

既存の relevant groups と component relevance を使い、
Argument に対する component の exposure class を判定する小さな API を追加する。

必要な区別は最小限でよい。

- `OWNED_PRIMARY`
- `UNOWNED_RECURSIVE`
- `AMBIGUOUS_RELEVANT`

名前は実装時に既存 naming convention に合わせて確定する。

### B. contribution filtering

exactness block の contribution filtering に component exposure classification を渡す。

期待挙動:

| component class | EXACTNESS_WINDOW | DERIVED_SHORT_EXACT_SEQUENCE | provenance |
|---|---|---|---|
| OWNED_PRIMARY | suppress | keep | keep |
| UNOWNED_RECURSIVE | suppress from body | suppress from body | keep |
| AMBIGUOUS_RELEVANT | preserve current behavior | preserve current behavior | keep |

### C. renderer integration

`render_toda_group_proof_narrative_multi_argument_markdown()` が
method evidence / components / relevant groups から exposure classification を作り、
body renderer / contribution filter に渡す。

proof graph traversal 自体は変更しない。

## 6. RC2-3 で変更候補となる production file

設計上の候補であり、RC2-2 では変更しない。

1. `toda_group_proof_narrative_exactness_relevance.py`
   - 既存 relevance API を再利用する。
   - 必要なら component exposure 判定 helper の置き場所候補。

2. `toda_group_proof_narrative_exactness_contribution_ownership.py`
   - contribution exposure filtering の最小変更候補。

3. `toda_group_proof_narrative_argument_multi_renderer.py`
   - Argument 単位の exposure classification を renderer に接続する候補。

新規 module を作るか既存 module に置くかは RC2-3 実装前に current code を再確認して決定する。

## 7. RC2-3 focused tests の必須境界

### $\pi_6^3$

- group structure の derived short exact sequence が残る。
- owned primary raw exactness windows は現在どおり重複表示されない。
- order ownership を壊さない。

### $\pi_8^5$

- group structure に再帰的に流入する $\pi_6^3$ exactness evidence は provenance に残る。
- unowned recursive contribution はその Argument の本文へ自動展開されない。
- owned order component の必要な higher-level contribution は残る。

### $\pi_{10}^4$

- unowned recursive exactness windows が本文へ自動展開されない。
- proof graph / provenance は維持される。

### $\pi_{12}^5$

- group structure の owned primary method を維持する。
- definition に流入した同じ exactness evidence は本文へ再展開しない。

### $\pi_{15}^8$

- exactness evidence がない現状を変えない。

### $\pi_{16}^9$

- unowned recursive exactness evidence の本文露出を抑制する。
- provenance は維持する。

## 8. 非目標

RC2 では以下を行わない。

- Argument ordering の変更
- conclusion と short exact sequence の表示順変更
- Narrative transition の変更
- proof depth の変更
- proof graph / provenance の削除
- Phase 149 / RC3 の先取り
- exactness 以外の evidence exposure の一般化

## 9. RC2-2 完了条件

RC2-2 は次を満たせば完了とする。

1. exposure 判定を ownership / relevance に基づく一般規則として定義した。
2. `primary is None` を単純な非表示条件にしないことを明記した。
3. owned primary の higher-level contribution を維持することを明記した。
4. unowned recursive evidence は provenance に保持することを明記した。
5. ambiguous relevant case は conservative fallback とした。
6. $\pi_6^3$ 固有規則を導入していない。
7. Phase 149 / RC3 の ordering 問題を明確に境界外とした。

## 10. 次 Phase 境界

次は Phase 148 RC2-3 — Minimal Implementation。

RC2-3 ではこの設計を実装するために必要な最小 API と renderer 接続のみを変更する。

RC2-4 で複数群横断監査を行い、
RC2-5 で focused regression と Phase 148 最終の repository-wide pytest を行う。
