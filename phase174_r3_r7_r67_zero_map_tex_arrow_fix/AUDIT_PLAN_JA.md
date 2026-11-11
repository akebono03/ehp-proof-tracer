# Phase 174 R67 — 表示上の `\\to` の修正

## 事前確認

- GitHub `akebono03/ehp-proof-tracer` の `develop` で `phase168_r3_27_typed_statement_projection.py` を確認。Git blob は `5b7bf647a7f7f427e2790cbe915709f014480d11`。
- `typed_sentence` の `ImageZeroStatement` 分岐だけ raw f-string 内に二重の `\\to` が存在する。
- 関連テスト `phase174_r3_r7_r55r3r2_narrative_removal/tests/test_typed.py`、公開監査 `phase174_r3_r7_r57_narrative_source_cleanup/audit.py`、直近 R66 ログを確認。
- R66 の段落7は `\\to`、同じ証明の他の矢印は `\to` であり表示上の欠陥が残っている。

## 変更対象と追加位置

既存の変更対象：`phase168_r3_27_typed_statement_projection.py` の `typed_sentence` 関数のみ。分岐内1行の文字列修正。import とほかの関数は変更しない。

新規ディレクトリ：`phase174_r3_r7_r67_zero_map_tex_arrow_fix/`。
`install.py` の全関数、`tests/test_install.py` の全テスト関数、`run.ps1` と文書。新規関数は同ファイル内に記載順で追加。

## 完了条件

- Source Guard PASS、DryRun PASS、Installer 成功。
- 限定 pytest PASS、R57 公開証明が2群とも complete、Reference は7件・3件を維持。
- 公開 Narrative の零写像矢印は `\to` 一つ、`\\to` なし。
- 全体 pytest は Phase 174 の終了時のみ。

## 次段階との境界

R67 は表示修正に限定する。R66 までの文章単位の出典監査の数学的妥当性を新規認定しない。既存監査の Source Guard は監査時点のファイルに固定されているため、本修正後の古い R63/R66 監査を再実行することは目的としない。
