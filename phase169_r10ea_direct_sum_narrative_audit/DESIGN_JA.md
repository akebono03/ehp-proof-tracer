# Phase 169 R10EA — 直和群の証明文章監査

## 対象と目的

対象は π₂₂¹³、π₂₃¹⁵、π₂₄¹⁵、π₃₉³⁰。R10E9 により各目標が `complete` と報告されたため、表示の整形より先に、正式な検索経路と Trust Boundary（信頼境界）を通して再確認する。

ユーザーが報告した π₃₉³⁰ の証明文章では、η 系列の一段懸垂等式が二重に表示され、ν の長い逐次等式も大量に並ぶ。`element_tex()` は μ・ε・bar-ν と一般の合成元を表示できないため、その未対応件数も観測する。これは現時点では **表示の問題として観測** される。検証済みの ProofStep（証明ステップ）や引用そのものを削除してよいことは意味しない。

## 既存コードの監査結果

- `phase168_r3_5_model_renderer.py`：共通 Renderer（文章生成器）の `render_model_backed_narrative_markdown()`。
- `phase169_r10a_verified_stable_chain_projection/projection.py`：既存の複数懸垂の要約は主として `FiniteCyclicGroup` を扱う。直和群には直結しない。
- `phase165_r12_r21_eta_generator_chain.py`：R10E9 により `_eta_pair()` の表記判定のみ修正済み。
- `phase168_r3_41p13_trust_boundary/verification.py`：文献前提と推論の再生検証。今回変更しない。

## 新規ファイルと新規関数

- `audit.py`：`audit_case()`、`main()` を新規追加。型付き検索の証明を再生検証した後に、既存 Renderer の出力を観測する。
- `prose_metrics.py`：`count_rendered_image_equations()`、`render_report()` を新規追加。本体を読み込まない純粋な表示計測器。
- `tests/test_r10ea_audit.py`：重複式の計数と誤検知防止の独立した限定テストを6件追加。
- `run.ps1`：Git の source guard、限定 pytest、監査、追跡対象ファイルの整合性検査。
- `README.md`：英語の実行手順。`DESIGN_JA.md`：本ファイル。

既存のクラス・関数・import は変更しない。すべての新規コードは ZIP 内に全文収録する。

## 監査基準と Phase の境界

Proof Tree → Trust Boundary → Narrative Model → 共通 Renderer の順序は固定する。文献名を使った追加の数学的推論は行わず、`E(f)=g` の表示回数だけを観測する。公開画面が完成を主張しても、信頼境界を再生通過しなければ未検証として報告する。

完了条件は、4目標の実探索結果と Trust Boundary の成否が記録され、描画された等式の重複数と文章の長さが記録され、既存の追跡対象ファイルが変更されていないことである。

次の実装段階では、重複と長い懸垂列を**文章表示に限って**簡素化する。未証明の生成元像を補ったり、ProofStep・引用・ルールを変更したりしない。全体 pytest は Phase 169 終了時にのみ行う。
