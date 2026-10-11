# Phase 163 R4-R47：TeX 本文登録結果

第1〜5章の抽出済み TeX 環境を独立カタログへ保存した。
命題本文は `catalog.json` の `tex_body` に保持し、文献掲載順は `publication_position` に保存する。
原稿との外部照合、構造化、証明探索への接続は実施していない。

- 登録環境数：108
- 既存 Reference：23
- 既存 Assertion：67
- 文献番号未解決の環境にも内部 source_unit_id のみを付与。
- `reference_id_candidate` は提案値であり、既存 Registry に登録・確定していない。
- 既存 Assertion と TeX 環境の対応は Reference 単位に限定。
- TeX 上の環境外の Definition 等は今回の対象外。
