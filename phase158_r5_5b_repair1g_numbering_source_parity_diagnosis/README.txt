Phase 158-R5-5b repair1g — numbering source parity diagnosis

背景
----
repair1f で次を確認した。

- numbering 対象の plain equation は raw Markdown に存在する。
- _numbered_step_line() は実際に tag 付き文字列を生成する。
- しかし number_toda_group_proof_narrative_equations() の結果は
  raw Markdown と完全に同一。
- raw_equals_direct=True
- tag inventory は N1〜N6 全て False。

現行 GitHub の関数実装どおりなら、
plain line が一致した行は tagged_by_id に置換されるため、
この結果とは整合しない。

目的
----
ローカルで実行されている numbering 関数本体と
multi renderer が参照している関数 object を確認する。

診断内容
--------
1. numbering module の実ファイル path。
2. number_toda_group_proof_narrative_equations の runtime source。
3. _numbered_step_line の runtime source。
4. multi renderer alias と numbering module function が同一 object か。
5. runtime source SHA256。
6. module file 上の関数本文。
7. 次の key implementation の有無:
   - plain_by_id
   - tagged_by_id
   - matching_id
   - lines[index] = tagged_by_id[matching_id]
   - duplicate/ambiguous guard

変更対象
--------
新規 audit bundle のみ。

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。

完了条件
--------
1. 実行中の numbering source が確認できる。
2. GitHub 現行実装との相違有無を判断できる。
3. multi renderer が別 function object を参照していないか確認できる。
4. production code を変更しない。
