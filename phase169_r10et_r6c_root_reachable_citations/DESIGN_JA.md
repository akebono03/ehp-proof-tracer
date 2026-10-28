# Phase 169 R10ET-R6C — 完成証明の root 到達可能引用

## 現象と原因

R6B の `pi_10^8` は COMPLETE / TRUST PASS、共通 Definition の生成元像は
適用可能4件・実使用4件、引用付き残存依存0件であった。しかし、元の DB prior
`(n=7,k=2)` は `GIVEN=True` であっても結論の祖先ではなかった。
旧 Narrative Model は検証済み検索結果の全ステップを引用対象としているため、
最終証明で使用されない別経路の prior が本文と Reference に表示された。

## 変更対象と変更境界

1. `phase168_r3_3_proof_narrative_model.py`:
   新規 `root_ancestor_step_indices` を `ProofNarrativeModel` の直後に追加。
   `build_proof_narrative_model` の COMPLETE 分岐の引用対象だけを root 祖先に制限。
   全 `ProofStep` と未完成証明の挙動は維持。
2. `phase168_r3_5_model_renderer.py`:
   `render_model_backed_narrative_markdown` の関数内 import に上記 helper を追加。
   COMPLETE 時の描画順と完全列表示を root 祖先に限定。
3. 新規パッケージ内の `tests/test_r6c_root_citations.py`:
   orphan の抑止、番号詰め、部分証明維持、無効依存の拒否、実際の pi10_8 を検証。

定理・命題・DB データ、Proof Tree、Search、Replay、Trust Boundary、
共通 Definition provider、旧資料は変更しない。

## 監査と完了条件

適用前に現在のコードが GitHub HEAD の blob と一致し、R5D の5ファイルが
完全に残っていることを確認。適用後は限定 pytest、R6 必須16件と追加3件の
検証を実施。`pi_10^8` の Reference は `(n=4,k=2)` の DB prior と
Toda `(4.5)` の2件のみ。根拠の存在を新規検索・引用名から推測しない。
Git index は完全保持。失敗時には本体2ファイルをバックアップから復元。
全体 pytest は Phase 169 の最後だけ。

## 次 Phase との境界

R6C は不要な Reference の表示抑制のみ。未検証の一般式、新 stem の導出、
命題台帳の削除、Definition provider の拡張には進まない。
