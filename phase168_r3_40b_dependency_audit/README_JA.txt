Phase 168 R3-40B — Proof Tree 依存関係と Narrative 表示順序の監査

目的
- ProofStep.premises が指定する論理的な依存関係と、Narrative Projection の表示順序を区別して監査する。
- pi3_2, pi4_3, pi5_4, pi6_5 を比較する。
- 新しい数学的推論規則、群専用 Renderer、文献引用を追加しない。
- この ZIP は現在の実装を変更しない。R3-40A の適用・取り消しもしない。

対象の既存実装 (監査のみ、変更なし)
- phase168_r3_29_order_projection.py: project_narrative_order
- phase168_r3_27_typed_statement_projection.py: typed_sentence
- phase168_r3_5_model_renderer.py: render_model_backed_narrative_markdown
- phase168_r3_3_proof_narrative_model.py: ProofNarrativeModel
- phase168_r3_38_frozen_fulltext_audit/audit.py: capture

実行
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_40b_dependency_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_40b_dependency_audit\run.ps1"

実行結果
- output/dependency_audit.md
- output/dependency_audit.json
- output/pi3_2_current.md, pi4_3_current.md, pi5_4_current.md, pi6_5_current.md
- output/review_bundle.zip (監査結果の共有に使用)

限定テスト
python -m pytest -q phase168_r3_40b_dependency_audit/tests/test_phase168_r3_40b_dependency_audit.py

判定
- index の欠落・重複は ValueError として処理を停止する。
- Proof Tree の論理的依存違反と、編集上の順序不一致は別々に報告する。
- 表示順に「FAIL」があっても数学的証明の誤りと直結しない。
- 全体 pytest は Phase 168 の最後だけ実行する。

次の境界
- この監査は順序規則の変更を行わない。
- 次に一般化するなら、Proof Tree の既存ステップを用いた宣言的な Narrative 表示依存へ置き換える。
