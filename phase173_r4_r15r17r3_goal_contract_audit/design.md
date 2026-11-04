# Phase 173 R15R17-R3 表示契約監査

## 目的

R15R17-R1 で統合された `ProofNarrativeModel` と R15R17-R2 の内部型名表示の修正を前提に, 未解決 Goal の重複表示と旧 Section を要求するテストの競合を実測する.

## 変更対象

本体コードおよび既存テストは変更しない. 新規監査ディレクトリのみを追加する.

- `audit.py`: `stable_equal`, `reversed_relation`, `inspect_goal_pairs`, `historical_contract_locations`, `check_r2_installation`, `audit_real_cases`, `main`.
- `tests/test_audit_helpers.py`: 型一致と数式一致を混同しないことの限定 pytest.
- `run.ps1`: Git HEAD, Git index, R2 インストール状態の検査と監査実行.

## 原則

1. `PartialProofResult.open_goals` と `ProofNarrativeModel.open_goals` の同一性を保ち, 表示のために数式一致から数学的同値を推論しない.
2. 同じ LaTeX でも型付き Goal が異なれば別の未解決条件として報告する.
3. 逆向きの等式は表示上似ていても, そのまま保存する.
4. `CertifiedAbstractStructure` の推論と記名生成元の完成証明を混同しない.
5. 旧表示の見出しを要求するテストは, 監査で候補を列挙するだけで書き換えない.
6. Phase 173 終了時までは全体 pytest を実施しない.

## 完了条件

GitHub の監査済み HEAD を確認し, R2 のファイル SHA-256 を検証する. Goal の型, 表示, 同値, 逆向き等式を4例で報告し, 旧テストの競合候補を収集する. Git index を維持し, 限定 pytest が PASS する.

## 次工程との境界

R3 は read-only audit に限定する. R3R1 以降で, 実測結果に応じて Goal の公開表示規約と既存テストの期待値を必要最小限に改訂する. 証明探索や推論規則には変更を加えない.

## R3R1 HEAD 検査の修正

R3 作成後, GitHub `develop` に R2 がコミットされ, HEAD が `11fdf0f5` から `aa25a9930d36b61e7588d1ef8e5916a766b569e6` に進んだ. R3 の `run.ps1` だけを現行監査済み HEAD へ更新し, エラー時に実際のブランチ・HEAD を出力する.

`audit.py` の証明状態不変条件, R2 の SHA-256 照合, 既存の型付き Goal 監査は変更しない. 新規 `test_head_guard.py` で修正済み HEAD とページャー・Git index 保持条件を検査する.

## R3R2 Reference 見出し判定修正

R3R1 の実行で, 未完成3例 (`n=4,k=8`, `n=4,k=9`, `n=5,k=3`) はいずれも `reference_sections=1` だった. 続く完成例 (`n=4,k=4`) の描画元は Markdown の `## 使用する結果` ではなく `使用する結果` を出力するため, 旧監査の `markdown.count("## 使用する結果") != 1` によって 0 件を重複と誤判定した.

`audit.py` の `count_canonical_reference_headings(markdown, complete=...)` を `audit_real_cases` の直前に追加し, 証明状態ごとの見出しを **行単位** で数える. 0 件と複数件を識別し, 反対側の見出しが現れる場合は fail-closed とする. `audit_real_cases()` はこの件数を検査・JSON 出力に使用する.

新規 `tests/test_reference_heading_contract.py` で未完成, 完成, 複数, 0 件, 状態不一致, 型不正を検査する. 既存 import・クラスは変更せず, 本体 Renderer, Model, Search, open_goals, Citation, 旧テストには一切触れない. R3 は read-only のままで, 全体 pytest は Phase 173 終了時に限定する.
