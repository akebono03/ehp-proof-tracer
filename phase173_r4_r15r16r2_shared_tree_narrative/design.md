# Phase 173 R4-R15R16R2 設計

## 目的

完成・未完成で共通の `ProofNarrativeModel` と `render_model_backed_narrative_markdown()` を使用する。R15R16 で加えた、Proposition 4.4 や Lemma 5.4 に特化した途中経過用の文章生成を除去する。

## 証明と表示の境界

- 記名生成元の探索結果 `PartialProofResult` は変更しない。
- 別に検証済みの `CertifiedAbstractStructure.proof_step` から、実在する前提を postorder で列挙する。推論ガードを再検査し、未検証の前提を挿入しない。
- この証明木を表示専用のスコープで既存 `build_proof_narrative_model()` に渡し、**既存 `render_model_backed_narrative_markdown()` をそのまま利用する**。
- 新しいスコープは検索結果を作ったことを意味しない。`PARTIAL` は表示用の型契約にのみ使い、Web 公開の完成判定には用いない。
- 既存の共通 Renderer から出た Reference と数式化可能な ProofStep のみを `検証済みの途中経過` に掲載する。型付き命題で数式レンダリング未対応の場合は推測式を作らず、出典表示に保持する。
- `証明済みの抽象群構造` は従来どおり証明書の結論。記名生成元の同定は依然として未証明。

## 共通表示・文体

見出し、引用、数式、句読点のレイアウトは前 Phase の `canonicalize_proof_layout` をそのまま使う。文章は `,` と `.`、ピリオドで改行。参照番号 4.4 と数式・コードには適用しない。特別な文章生成を新たに追加しない。

## 実装と非対象

本番の既存関数 `_verified_abstract_progress_lines()` を、共通 Renderer への薄い接続だけに置換する。`tree_adapter.py` に対象によらない型付き検証・表示橋渡しを追加する。新しい推論規則や記名生成元の証明、完成状態の変更、特殊な `(n,k)` 分岐、全体 pytest は対象外。

## 完了基準

DryRun・限定 pytest PASS。`(4,8)`, `(4,9)`, `(4,15)`, `(4,31)` で定理、DB prior、Hopf 関係の出典・数式が共通 Renderer によって現れ、未解決 Goal の状態は不変。完成 `(4,4)` で抽象群専用見出しが現れない。
