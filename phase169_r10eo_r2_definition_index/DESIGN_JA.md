# Phase 169 R10EO-R2 — 生成元非依存 Definition Index の監査実装

## 変更対象・追加位置

既存の本番ファイル、既存テスト、主要ドキュメントの**変更はない**。リポジトリ直下に新規 `phase169_r10eo_r2_definition_index/` ディレクトリを追加する。

- `__init__.py`：新規 package 定義。
- `definition_index.py`：新規 `DefinitionOccurrence` クラス、`mask_tex_comments()`、`normalized_tex_with_offsets()`、`normalized_tex()`、`expected_formula()`、`occurrences_for_family()`、`index_definitions()`、`check_existing_reviewed_records()` の各関数を追加。import を含む全文を本ファイルに収録。
- `audit.py`：新規 `render_report()`、`main()` を追加。import を含む全文を本ファイルに収録。
- `tests/test_r10eo_r2_index.py`：新規テスト8件と補助関数の全文を収録。
- `run.ps1`：限定テスト、実行時 Goal、Git 差分ガードを実施。
- `README.md`：英語による起動説明。
- `DESIGN_JA.md`：本書の全文。

`DefinitionOccurrence` は `dataclass(frozen=True)` であり、全文は `definition_index.py` に記載した。`__init__.py` は空ファイル。既存 import の変更、既存クラス・関数・メソッドの変更はない。

## 設計

`HyoujiGen.csv` の `kinds=0` は候補生成元の型付き命名データであって、証明ではない。`n` は候補の開始次元、`k` は次数差、`latex` は文献中の記号照合に使う。`stable` と `stable_orders` は現行 CSV では空欄であり利用しない。

各登録対象から、名前による分岐なしに一般形

$$
\alpha_n:=E^{n-n_0}\alpha_{n_0}
$$

を **字面の検索パターンとしてのみ**構成する。TeX の空白・スペーシング命令・単純な添字波括弧・`\overline{\nu}` の表記差は位置情報を保持したまま正規化する。コメント中の候補を除外し、完全なパターン一致の開始・終了位置を直接取得するため、R1 にあった「130文字幅のスニペットから同一式を2件と数える」問題を避ける。同一式が実際に2回存在すれば曖昧として保持し、勝手に一件に統合しない。

出力は元のファイル、ファイル内容の SHA-256、元ファイル上の行番号・文字位置、候補数、候補の直前に現れる `\paragraph` 情報を含む。これらは出典審査の材料であって、真理値や文献掲載順序を自動認可するものではない。

既存の `SOURCE_RECORDS`（2件）および `CHAPTER_VI_SOURCE_RECORDS`（3件）との型付きパターン整合性を検査する。既存の5件の出典認証はそのまま維持し、未審査の候補を登録しない。従来の $\eta$ の経路にも変更を加えない。

## 信頼境界

`DefinitionOccurrence.classification = TEXT_ONLY_NOT_CITED` を固定し、FIXED_STATEMENT、GIVEN、INFERENCE を一切生成しない。CSV の `id`、記号の一致、転写 TeX での一致、ハッシュ値の一致は、それだけで数学的な Definition の承認にならない。

次工程では、候補の式、出典節、出版順序・採用範囲を独立に審査した source attestation を構成し、既存の `CitedStableFamilyDefinition` → `StableFamilyMemberDefinition` → `GeneratorImage` の型付き推論経路に渡す。生成元ごとの推論規則は追加しない。

群構造輸送は既存の `generator_images_for_group_transport()`、`general_group_transport_rule()` を維持し、零群、巡回群、自由巡回群、直和群、合成生成元への一般性を失わせない。$n\ge k+2$ の安定範囲と Definition の $n\ge n_0$ は別条件として扱う。

## 監査目標

限定 pytest で新規8テストと R1/R10B/R10D2/R10E8/R10E1 の関連テストが PASS。既存の審査済み Definition 5件と矛盾がないこと。`\zeta_n` の定義候補について、字面1箇所なら1件のみを検出すること。11-stem の4件の未解決 Goal をそのまま再取得し、未完成証明の Trust Boundary を PASS と誤表示しないこと。tracked source が一切変更されず、全体 pytest を実施しないこと。

## R10EO-R3 との境界

R2 は原典候補の索引化だけ。Definition の採用審査、GIVEN 登録、既存 SOURCE_RECORDS の縮小・統合、$\pi_{41}^{30}$ の完成証明への変更は R3 以降に保留する。

採用済み転写 `sources/toda/Toda_05_2.tex` と `Toda_06_2.tex` の同定は、原著印刷版を独立に照合したという主張ではない。
