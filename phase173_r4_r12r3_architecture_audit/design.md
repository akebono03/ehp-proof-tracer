# Phase 173 R4-R12R3：Narrative 構造監査・統一設計

## 目的と境界

この段階では本体コード・ProofStep・証明探索・引用情報を変更しない。読み取り専用監査の結果から、共通 Renderer への移行を行う対象を定める。Phase 終了時以外は全体 pytest を行わない。

## 現行コード確認（GitHub develop 188f707e）

- `phase165_r52_r3_web_adapter.py`：Model Renderer の出力を `project_verified_toda56_narrative` によって後処理する。
- `phase173_r4_r12_common_narrative/projection.py`：`group_dimension == 7` と `LEGACY_ROOT` の組合せで専用 `project_verified_pi74_narrative` に分岐。`sphere_dimension != 4` も表示経路の対象限定として存在する。
- `phase173_r4_r1_narrative_source_fix/projection.py`：証明対象と出典番号を専用に検証し、特定の生成元表記を含む文章を手組みしている。
- `phase168_r3_5_model_renderer.py`：ProofNarrativeModel に基づく共通経路がある一方、`(n,i)=(4,...)` という文字列を生成する特殊化が残る。
- `phase173_r4_r12_common_narrative/tests/test_projection.py`：専用出力とのバイト一致、生成元像、零群補足の出現を要求する。
- `phase173_r4_r13_narrative_audit/tests/test_audit.py`：零群の補足文章自体を確認する。

## 原因分類

1. 探索規則の差：一般的な型付き命題と、個別証明の導出手順の違い。これは文章 Renderer の問題とは区別する。
2. Renderer の分岐：型付き証明木の形ではなく、具体的な次元、規則名、生成元名によって文章を選ぶこと。
3. 後段の文章上書き：共通 Renderer の結果を専用テンプレートで置き換えること。
4. テストの固定化：検証すべき数学的事実ではなく、過去の文言や構成上不要な説明を成功条件にすること。

## 移行後の契約

`Proof Search -> Verified Proof Tree -> ProofNarrativeModel -> Common Narrative Renderer -> Web` の単方向とする。Renderer は ProofStep の Conclusion、Premise、Reference、型、論理構造から文章を作り、別名の専用 Renderer に分岐しない。先行 DB は認証マーカーと証明根との結合を保持し、表示上の群記号のみ TeX 化する。

表示プロファイルは、証明木に実在する型付き命題に基づく一般則に限る。特定の `(n, k)`、`\pi_7^4`、生成元名文字列への一致条件を許可しない。零群では零群の結論を表示すればよく、追加の独立した生成元像の文章は作らない。

## 二層の再発防止テスト

- **構造テスト（AST）**：中央 Renderer と Web adapter について専用関数定義・呼出し・import、次元リテラル分岐、固定球面次元を持つコンストラクタ、legacy root 分岐、render 後の上書きを検出する。監査段階では違反を列挙するだけで PASS とし、移行後に `future_gate/architecture_gate_spec.py` のゼロ違反条件を必須化する。
- **意味テスト（実行時）**：完成5群について、complete・認証済み証明根・同じ型付き結論・実出典に結合した citation・Web 完成を確認する。文言のバイト一致や必須ではない補足文の存在は要求しない。未証明 `\pi_{12}^4` が完了しないことも確認する。

構造テスト単体は数学的な文章の正当性を保証しない。完全な移行ゲートには意味テスト・出典対応テスト・データ由来の文字列表示テストを併用する。

## 進め方

1. R4-R12R3：監査 ZIP を実行し、旧実装の入口、依存、既存 pytest の衝突を確定する。実装変更なし。
2. 続工程：共通 Renderer の「検証済み同型の表示」という一般処理に統合する。必要なら証明木に型付き文を加えるが、証明根や出典は改変しない。
3. 旧 projector の呼出しを公開経路から外す。旧モジュールの物理的削除は既存 API への影響を確認するまで行わない。
4. 旧文言固定テストを意味テストに置換し、構造ゲートを有効化する。限定 pytest を通過させる。

## 完了の判定

この監査の完了条件は、GitHub とローカルの HEAD 合致、監査レポート生成、限定 pytest PASS、変更なしを記録できること。Renderer の統一完了を意味しない。統一完了の判定は、後続実装時の構造ゲート PASS と既存完成証明の意味テスト PASS の両方で行う。
