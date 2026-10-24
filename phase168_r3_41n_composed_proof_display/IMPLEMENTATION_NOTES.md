# Phase 168 R3-41N — 型付き後続推論に吸収される中間表示の整理

## 変更対象

- 既存ファイル: `phase168_r3_5_model_renderer.py`
- 既存関数: `render_model_backed_narrative_markdown()` 全文置換
- 既存テスト: `phase168_r3_41l_reasoned_prose/tests/test_phase168_r3_41l_reasoned_prose.py`（中間群構造の表示を要求する2件を変更）
- 新規テスト: `phase168_r3_41n_composed_proof_display/tests/test_phase168_r3_41n_composed_proof_display.py`
- 新規実行コード: `install.py`, `run.ps1`, `audit.py`
- モジュール先頭 import、Proof Tree、Reference 台帳、登録命題、文献順、公開 API は変更しない。

## 変更内容

1. `Im Δ = ker E` の型付きステップが、その直接の後続にある具体的な `ker E` の型付きステップに一意に利用されているときだけ、前者の本文表示を省く。
2. 一回懸垂の巡回群輸送の中間表示が、実証済み `GeneratorSuspension` によって最終生成元へ正規化される直接の前提になっているときだけ、中間表示を省く。
3. どちらも中間ステップ自体は削除せず、文献引用番号がある場合や複数の後続から参照される場合は省略しない。
4. 未完成証明表示、群ごとの特例、最終結論の数式は変更しない。
5. 変更する既存テストの import は変更しない。

## 検証と完了条件

- R3-41N の追加テストに加え、R3-41M2/J2/L/I/26a/19/10 の限定 pytest を実行する。
- π₄³ の `ImΔ=ker E` の重複と π₅⁴ の `Z/2{Eη₃}` の重複が解消する。
- π₃² の Hopf 写像論証、3群の Reference 使用、基準論証、公開経路が保たれる。
- 監査の `BASELINE_REVIEW_REQUIRED` は全文の単純な不一致を示すもので、差分件数が0であることを要求しない。
- 全体 pytest は Phase 168 の終了時まで実行しない。

## 次 Phase との境界

証明探索規則、安定輸送や対象群の追加、文献順の一般改修は扱わない。
