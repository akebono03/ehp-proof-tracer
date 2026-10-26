# Phase 169 R4G — Hopf fibration を出典検証付き Reference に表示

## 現行コードの確認

GitHub `akebono03/ehp-proof-tracer` の `develop`、HEAD `4305edd24566a2780781db1783e6e462719c74b0` を調査した。修正ファイルの blob は以下。

- `phase165_r52_r27_r5_literature.py`: `b683533badcf80a6568bd22859efa6b7b8f1edd5`
- `phase168_r3_37c_reference_projection.py`: `32b7d01545fe8b37afb0eb85a53caf615064d83f`

元テキスト `sources/toda/Toda_04_2.tex` の Git blob `4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7` を参照し、Proposition 4.4 直前の段落に $n=2,4,8$ の Hopf fibration の存在と Steenrod1951 引用があることを確認した。Toda 第5章の Lemma 5.4 は Proposition 5.3 より後なので使用しない。

## 変更ファイル・クラス・関数

- `phase165_r52_r27_r5_literature.py`
  - import 節: `sha1` と `Path` を追加
  - `TodaProp44UniversalStatement`: 全体を更新し、出典直前段落の適用可能な次元 `(2,4,8)` を型付きメタデータとして保持
  - `verify_prop44_hopf_fibration_source`: **`_SOURCES` 定義の直前に追加**、出典ファイルの Git blob と段落の存在および原文引用を検証
  - `build_typed_literature_bridge`: 全体を更新、登録前に出典検証を行う
- `phase168_r3_37c_reference_projection.py`
  - `project_reference_bodies`: 全体を更新、登録済み Proposition 4.4 の既存 `statement_bodies` 1件の中に「Proposition 4.4 直前の記述」を明示
- 新規監査パッケージ `phase169_r4g_hopf_reference/`: `apply.py`、`audit.py`、`run.ps1`、限定テスト

上記の変更は **Reference の出典説明だけ**に限定する。`R4F1` の本文、R4B の推論規則、Backward Search、Proof Tree、Web API には手を加えない。

## Reference と引用の方針

[R2] Proposition 4.4 の下に「**Proposition 4.4 直前の記述**」と明記して表示する。新たな独立した GIVEN は追加せず、既存の固定命題の型付き情報に、検証済みの直前段落を補足する。したがって **現状の5件の Reference と18ステップを維持**する。独立した Hopf fibration 命題として別の Reference ID を付与する作業は後工程とする。

**重要な制限：** 出典が独立の先行段落であることは表示するが、今回の変更はそれを独立した ProofStep として証明木に組み込むものではない。証明上の独立前提が必要なら、別の型付き命題の登録・公開順序接続が必要になる。

## 出力

実行後 `output` に変更前のファイル、変更後のファイル全文、更新したクラス・関数の全文、`audit.md`、`audit.json`、`web_narrative.md` を保存する。

## 完了条件・境界

限定 pytest が成功し、$\pi_6^4$ 18ステップ complete、Reference 5件、[R2] の下に Hopf fibration の出典が表示され、$\pi_5^3$ の既存表示が維持されること。全体 pytest は Phase 169 末尾にのみ実行する。次の独立 Reference 登録や $\pi_7^5$ への拡張は先取りしない。
