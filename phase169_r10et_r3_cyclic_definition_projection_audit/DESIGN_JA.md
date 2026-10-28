# Phase 169 R10ET-R3 — 共通 Definition の巡回群 Projection 監査

## 対象

R10ET-R2 の共通 Definition 優先探索は16件すべてで complete / Trust PASS だったが、既存の巡回群反復懸垂 Projection は2件で不成立となった。現行 `phase169_r10a_verified_stable_chain_projection/projection.py` は、画像の `GeneratorImage` に付く引用付き GIVEN 祖先を必須としているため、すべてを共通 Definition から証明すると引用番号が空になる。

## 読み取り対象

- `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()`。
- `phase169_r10eq_r1_universal_stable_definition/definition.py` の共通 Definition 推論。
- `phase169_r10a_verified_stable_chain_projection/projection.py` の `project_verified_stable_image_chain()`。
- `phase169_r10en_shared_citation_provenance/core.py` の引用祖先追跡。
- `phase169_r10ec_direct_sum_narrative_projection/projection.py` の直和群の先例。
- `phase168_r3_5_model_renderer.py` の圧縮等式前置詞。
- R10EQ、R10ER、R10A、R10EN、R10ES の限定テスト。

## 監査方式

AUDIT_ONLY。ファイルを上書きしない。探索 Factory と引用番号抽出を実行中だけ置換し、最後に必ず復帰する。各ケースで完成証明の標準 Trust Boundary 検証を行う。

共通 Definition の認定は `canonical_definition_inference()` による推論規則の構造一致と再生可能性検査を要求する。ほかの `GeneratorImage` には従来の引用祖先検査を適用する。

巡回群の根の **先行群構造** と **同型の根拠** の両方について、実際の別々の GIVEN の引用祖先が必要。引用を捏造しない。どちらかが欠ければ圧縮しない。

## 注意点

`render_model_backed_narrative_markdown()` は `citation_numbers=()` のときも `より,` を出す。R3 では Renderer を修正せず、引用なし文言を検出する。候補 Projection が成功しても、この表示不具合は別途直す必要がある。

既存の `test_r10a_4fold_eta_square_is_single_certified_display()` などは引用番号非空を要求している。製品実装時には、共通 Definition の証明と引用付き証明を区別する限定回帰テストが必要である。新しい生成元別規則は追加しない。

## 次の作業の境界

R10ET-R4 までは製品コードの探索順・Reference・Renderer を変更しない。監査で復旧可能性、既存直和表示の維持、ProofStep/引用不変、未解決の前置詞を確定してから、最小限の関数単位で実装する。
