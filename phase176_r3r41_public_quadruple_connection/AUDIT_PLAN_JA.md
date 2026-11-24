# R3R41 公開接続監査

- 確認済み GitHub HEAD: `5796fa3344c31564e10fa820a59579e1b3934d38`。
- 共有ファイルの LF blob: `2b10c184942bd9ce1adb910ba2536f7ab3d0b22f`。
- 変更対象: `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 内だけ。既存候補の相対順と root gate は保持する。新規候補は `options` の先頭に追加する。既存の早期 return は変更しない。
- 新規 `source.py` の `public_quadruple_backward_plan()` と `build_public_quadruple_connection_provider()` は、目標の型と選別済み Hopf 関係から R3R40R1 の監査済み計画を組み立てる。型付き値が一致する Toda (5.5) 特化だけを候補にする。曖昧な候補は拒否する。推論候補だけを保持し、証明や GIVEN は保持しない。
- 監査: 通常の `shared_expansion_provider(screened, proof_target=root)` を使う。監査用 Provider の注入なし。18段階の表記接続、3件の独立懸垂、R3R39 の6段階、Toda (5.5) の出典、最終推移律を検証する。
- 数学的目標: $H(\nu'\eta_6^2)=4\nu_5$（監査側の型付き生成元）。登録済み DB 生成元への拡張は次工程。
- Phase 175 の `same_typed_generator_notation()` は一重懸垂の `Suspension` と `IteratedSuspension` の比較に限定される。今回の直接合成の同一視に流用しない。
- 全体 pytest は実施しない。最終 Gate: `PASS_R3R41_PUBLIC_QUADRUPLE_FOCUSED_TESTS`。

## R3R41R1 — パッチ位置検査修正

- 旧検査は同一モジュールの import 文をファイル全体で一意と仮定していた。現行 blob には91行目と452行目の2か所が存在する。
- `apply.py` の `_unique_function()`、`updated_source()`、`main()` を変更する。AST で対象の共有関数と直下の `expand()` を一意に特定し、完全な複数行アンカーを使う。
- 実ファイルのアンカー照合では setup 1件、dispatch 1件、既存 R3R39 hook 1件、追加8行、追加除去後の元内容完全一致、LF 保持を確認した。
- `tests/test_apply.py` の5件で重複 import、対象外の同一 setup、誤った dispatch、部分・移動パッチ、既存 hook 欠落と CRLF を検証する。模擬ファイルの5件は作成環境で PASS。実プロジェクトの DFS・限定テストはユーザー環境で実行する。
- `source.py`、`audit.py`、`tests/test_public_connection.py` は R3R41 と同一。数学規則・出典の変更なし。全体 pytest は実行しない。
- 追加 Gate: `PASS_R3R41R1_SCOPED_PATCH_FOCUSED_TESTS`。
