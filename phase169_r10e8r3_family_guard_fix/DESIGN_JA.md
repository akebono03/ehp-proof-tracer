# Phase 169 R10E8-R3 — 置換ガード修正

## 原因

R10E8 の既存 `transformed_sources()` は、`source.family_id not in {record.family_id for record in SOURCE_RECORDS}` が2件あると仮定していた。しかし GitHub develop HEAD `940d1d1cc2e9943e9d2955c7204a4392984d65e9` で確認した実ファイルでは、`canonical_member()` 内の `source.family_id` が1件、`cited_family_reference_sentence()` 内の `statement.family_id` が1件である。このため CRLF 対応後もガード不一致が発生していた。

## 変更対象

既存の R10E8/R10D2 コードそのものの修正は行わず、追加する `phase169_r10e8r3_family_guard_fix/patch.py` の `_function_body`、`transformed_sources_r3`、`apply_guarded_r3_patch`、`main` に修正内容を限定する。既存 R10E8 が意図した `phase169_r10d2_general_family_definition/family_citation.py` の import、`canonical_member()`、`cited_family_reference_sentence()` および `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` のみが置換対象になる。

## 信頼境界

- 置換前に2種類の正確な式を各1件確認し、それぞれの関数内部に存在することを AST で検証する。
- 追加された既存の `SOURCE_RECORDS` は変えず、Chapter VI の定義への受理対象だけを広げる。
- `HyoujiGen.csv` は系列の型同定にのみ使用する。CSV データだけから `GeneratorImage` を証明しない。
- 懸垂像の証明は既存の `expand_cited_stable_family()` の `INFERENCE` を使用する。
- LF／CRLF は元のファイルごとに維持する。混在改行は拒否する。
- Git の HEAD 祖先関係と変更対象の厳密な blob SHA を検証する。未確認の本番変更は拒否する。
- 限定 pytest または監査が失敗した場合、対象本番2ファイルと既存監査出力をバイト単位で戻す。

## 変更前と変更後の差分の意義

`canonical_member()` では `source.family_id` を検証し、`cited_family_reference_sentence()` では `statement.family_id` を検証する。修正により両方の関数が `SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS` を参照する。系列ごとの推論関数は追加しない。

## テストと Phase 境界

R10E8-R3 と既存 R10E8-R2/R10E8/R10D2/R10E5/R10E4 の限定 pytest、さらに $\pi_{23}^{15}$ と $\pi_{24}^{15}$ の探索監査を行う。complete の判定を先取りしない。全体 pytest は Phase 169 終了時にのみ実施する。
