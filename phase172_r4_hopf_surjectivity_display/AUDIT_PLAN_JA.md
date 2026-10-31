# Phase 172 R4 — H の全射性の重複表示

## 前提

- Phase 172 R3R2 の実行結果は `PASS_R3_HOPF_DISPLAY_ONLY`、限定 pytest 5セット PASS。
- R1 の `proof_steps.json` では Step 27 が `TodaHopfInvariantSurjectiveStatement`、Step 29 がその全射性を前提とする `TodaDeltaZeroStatement`、Step 30 が同じ写像の `MapSurjective` である。
- Step 30 は Step 29 と Step 28（EHP exactness）から証明され、後続の短完全列 Step 31 に用いられる。従って Step 30 を Proof Tree から取り除かない。
- GitHub `akebono03/ehp-proof-tracer` の `develop` で、共通 Renderer、R2 Projection とテスト、R3 の検証済みパッチ、`typed_sentence` の型付き map property 処理を事前に確認。

## 変更対象

1. 既存 `phase168_r3_5_model_renderer.py` の関数 `render_model_backed_narrative_markdown()` のみ。R3 Projection の呼出直後に R4 Projection を呼び、検証済みの重複 Step の表示インデックスを集合へ追加する。関数内 import を1件追加する。**変更後の関数全体とソース全文は DryRun 出力フォルダに保存する。**
2. 新規 `phase172_r4_hopf_surjectivity_display/projection.py`：`redundant_hopf_surjectivity_indices()` を追加。トップレベル import の全文を含む。
3. 新規 `phase172_r4_hopf_surjectivity_display/tests/test_projection.py`：実証明を使う fixture とテスト6件を追加。import 全文を含む。
4. 新規 `install.py`、`run.ps1`、`__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

既存クラス定義・他の関数・数学的ルール・Reference・ProofStep・既存テスト・その他ドキュメントを変更しない。

## Fail-closed 条件

- Proof Search の状態が complete で、未解決 Goal が0。
- 根の祖先に属する検証済み ProofStep についてのみ評価。
- Step 27 相当の先行全射性と Step 30 相当の後続全射性が **同一の型付き TodaHopfInvariantMap** を参照。
- 後続 `MapSurjective` が `TodaDeltaZeroStatement` と `TodaProp42ExactnessStatement` を前提とする。
- その `TodaDeltaZeroStatement` が同じ完全性と、表示されている先行 `TodaHopfInvariantSurjectiveStatement` を前提とする。
- 先行全射性と EHP exactness には引用付き GIVEN 祖先が存在。後続全射性自身は引用を持たない。
- 先行全射性が他の Projection で非表示なら省略しない。
- 生成元・球面次元・群をハードコードせず、TeX 文字列一致で数学的同値性を認定しない。

## 実行と完了条件

限定 pytest は6セット：R4 新規、R3、R2、Phase 171 η 表示、Phase 171 位数4表示、Phase 169 π₆⁴ 表示。各セットを独立に実行する。全体 pytest は Phase 172 終了時のみ。

目標 Web 表示：$H:\pi_6^3\to\pi_6^5$ の全射性は Step 27 の1回だけ表示する。Step 29 の全射性を用いた $\Delta=0$ は維持し、Step 30 の同一内容の表示のみ省略する。50件の ProofStep、8件の Reference、未解決0、$\pi_6^3=\mathbb Z/4\{\nu'\}$ の結論を維持。

R5 の `DB prior` の出典表記変更には着手しない。Phase 172 R6 まで全体テストはしない。
