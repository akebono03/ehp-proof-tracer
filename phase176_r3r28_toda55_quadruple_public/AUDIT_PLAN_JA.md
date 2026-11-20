# Phase 176 R3R28 — 公開接続計画

## 対象と実装境界

変更ファイル：`phase165_r52_r9_shared_math.py`。

変更関数は `build_shared_typed_bridge()` と `shared_expansion_provider()` の2件。module-level import は変更しない。元の全関数を保持して、各関数内に出典登録／一般候補接続の短い節だけ挿入する。

新規：`phase176_r3r28_toda55_quadruple_public/install.py` の `git`, `checked_root`, `functions_in`, `proposed`, `full_code_md`, `output_dir`, `execute`, `main`。追加位置は当該新規ファイルの先頭から。

新規：`tests/test_public.py` の5つのテスト。既存テストは変更しない。

## 数学的意味

Toda (5.5) の既存原典から以下を一般 GIVEN として登録する。

$$4\nu_n=\eta_n\circ\eta_{n+1}\circ\eta_{n+2}\qquad(n\ge5).$$

ただし具体的な $n=5$ の等式は GIVEN ではなく、ν-family の型付き生成元定義と η-family の一般定義を使って導出する。

## 保守性

既存の第1関係、出典 ID、全体探索順序、Narrative は変更しない。標的群の直接 GIVEN は追加しない。完全証明は主張しない。

## 完了条件

DryRun、本実行、限定 pytest PASS、および共有 `reconstruct_registered_goal` が `ProofRule.INFERENCE` を返すこと。全体 pytest は Phase 終了時のみ。

## 次段階

R3R29 で Hopf 像の型付き代入と四倍関係を接続する。
