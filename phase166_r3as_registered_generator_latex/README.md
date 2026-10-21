# Phase 166 R3-AS — 登録済み生成元の TeX 表記

対象ファイル：`phase166_r3aj_structured_generator.py` の `_base_element()` および `toda_human_readable_renderer.py` の `_render_generator_symbol_latex()`。既存の import 部は変更しない。両関数の全文は `base_element.txt` と `render_generator.txt` に収録。

`HyoujiGen.csv` の `latex` 列が持つ正規の数式表記を、例外的生成元にも使用する。`kinds=0` で部分添字 `\\mu_{3,` のように終端が開いている場合は、次元の添字をその括弧内に挿入する。それ以外の登録 TeX は重複変換しない。証明目標の型・証明探索・出典・命題台帳・文書には触れない。

`run.ps1` が対象関数を AST の関数境界で置換し、バックアップを保存して4件の限定 pytest を実行する。全体 pytest は Phase 終了時のみ。

完了条件：4件 PASS とブラウザでの2群の表示確認。次 Phase では他の特殊記法の個別監査を実施する。監査結果だけから証明済みと判定しない。
