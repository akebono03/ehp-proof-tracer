# Phase 173 R4-R15R9 — 共通 Web 表示への抽象群証明の接続

## 目的

R15R7 の Source-first Proof Search（出典優先の証明探索）と R15R8 の `CertifiedAbstractStructure` による証明済みの抽象群構造を、**既存の共通 Web Adapter にのみ**投影する。

`π_35^4 ≅ (Z/2)^8` は抽象群の結論であり、CSV に登録されている 8 個の記名生成元との対応は別の未証明 Goal のまま保持する。数学的な完全証明と抽象群だけの証明を混同しない。

## 変更対象と責務

1. 既存 `phase165_r52_r3_web_adapter.py` の `build_partial_web_group_proof_view` 関数全体。トップレベル import は変更しない。
2. 新規 `phase173_r4_r15r9_shared_abstract_renderer/projection.py` の `abstract_invariants_latex`、`render_certified_abstract_section`。
3. 新規パッケージの `patch_source.py`、`install.py`、`audit.py`、限定テスト。

既存の Proof Search、証明木、`PartialProofResult`、`ProofNarrativeModel`、Renderer 本体、データベース、EHP 数学規則は変更しない。`n=4` や `k=31` の描画専用分岐も作らない。

## 共通経路

`search_group_from_registered_goal` → `PartialProofResult` → `build_linked_proof_narrative_model` → `render_model_backed_narrative_markdown` → **既存 `build_partial_web_group_proof_view`** → `WebGroupProofView`。

R15R9 が追加するのは、上記 Web Adapter で描画済み Markdown に、証明済み抽象群の節を1回追加する純粋な表示処理だけである。`n,k` に基づく分岐、独立した Narrative 実装、ProofStep への新しい `GIVEN` はない。

## 正規化する数学的表示

- `(('finite',2),)*8` → `\left(\mathbb{Z}/2\right)^{8}`。
- `(('free',0),)` → `\mathbb{Z}`。
- `()` → `0`。
- `('finite',m)` の `m` は2以上の整数だけ許可。位数1、負数、bool、未知の型は拒否。

結論を表示する際は「出典検査済みの抽象群 ProofStep の結論」と「記名生成元の対応は未証明」を明記する。先行 DB 結果が独立の原典証明であると主張しない。

## 安全条件

- `abstract_structure=None` の場合は、既存 Markdown を文字単位で変えない。
- `status` を `complete` に昇格させない。
- `conclusion`、`open_goals`、既存の引用・生成元表示・ProofStep を変更しない。
- `trace` は既存どおり Narrative を出力しない。
- Source Guard は現在の Git HEAD、依存ファイルの Git blob、既存 R15R8 コミットを照合する。
- パッチ後の pytest と Web 監査が失敗した場合は、元の Web Adapter を復元する。

## 完了条件と Phase 境界

R15R9 の完了条件は、公開 Web に `証明済みの抽象群構造` と位数別直和が表示され、同時に `generic-partial-proof` と未解決 Goal を維持すること。対象の限定 pytest と Web 監査が通ること。

記名生成元像の不足（特に ID 56、88）、原典の追加認証、公開証明の全面 `complete` 化は **次工程以降**。全体 pytest は Phase 173 終了時のみ行う。
