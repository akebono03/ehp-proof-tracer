# EHP Proof Tracer ロードマップ

この文書は**今後の 機能依存関係 と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

運用計算:

```text
生の n,k 入力
→ python main.py n k
→ 標準運用リポジトリ
→ 証明レポート
```

生成元探索:

```text
生成元
→ 再帰的証明範囲
→ 生成元-specific specialization
→ Toda membership / 既知の写像関係
→ 適用候補
→ 関連度分類済み表示
```

既知群の証明再生:

```text
生成元
→ 既知群同一性
→ 既存 ProofStep
→ 直接証明再生
→ python main.py show-proof ...
```

利用者向け qualified execution:

```text
生成元 input
→ 実行可能対象の解決
→ NONE / AMBIGUOUS / executable target
→ 候補一覧 / 1-based 候補選択
→ qualified execution
→ 最終実行済み ProofStep
→ 結果 + 証明
→ python main.py execute ...
```

演算問い合わせ:

```text
演算問い合わせ
→ 既存 repository / proof-scope 事実検索
→ 重複除去済み数学表示
→ 保持された provenance
→ python main.py query ...
```

演算問い合わせの証明再生:

```text
選択された問い合わせ事実
→ 主要 provenance
→ 事実自身の ProofStep
→ 有界直接再生
→ 安全な数式表示
→ python main.py query-proof ...
```

最新:

```text
Phase 110 closure:
9055 passed in 455.09s (0:07:35)
git diff --check: clean
```

Phase 110 は完了。

---

# 2. 完了済み機能

Phase 90–104:

```text
問い合わせ / 正規化
EHP / 証明 provenance
計算オーケストレーション / レポート
生成元探索
再帰的証明範囲
適用可能性探索
関連度分類
安全な候補引き渡し
有界実行 provenance
```

Phase 105:

```text
第1 qualified family
正確な source seed
family grouping
明示的 root + source 選択
標準 first-family facade
```

Phase 106:

```text
適用可能性性能監査
生成元-relevant scope prefilter
```

Phase 107:

```text
複数前提 recovery
正確な premise tuple seed
第2 qualified family
明示的 root + source + family 選択
family dispatch
multi-family 標準 facade
```

Phase 108:

```text
利用者向け実行可能対象 resolver
曖昧性に安全な workflow
1-based 候補指定
最終実行済み ProofStep extraction
minimal 結果 + 証明 presentation
候補一覧表示
execute CLI
Windows UTF-8 CLI 境界
```

Phase 109:

```text
既知群同一性 integration
証明由来の ambient group fallback
一般的な concrete indexed sigma_n 具体化
proof-scope 具体化統合
既知群の証明再生
show-proof CLI
既知群優先の曖昧 execute 表示
候補順 / 定理 ranking 境界の確定
```

Phase 110:

```text
最小演算問い合わせ parser
既存 H / E / Delta / 合成事実検索
query CLI
生 occurrence の保持
同一 statement の重複除去表示
浅い depth を優先する表示順
問い合わせ事実選択
事実を root とする証明再生
query-proof CLI
限定的な数学 statement 表示
安全な aggregate 型 fallback
完了時 regression
```

---

# 3. 現在の実行 API

Phase 107 multi-family:

```text
execute_standard_repository_生成元_適用可能性_result_by_root_source_and_family(
  適用可能性_result,
  root_entry,
  source_step,
  family_name,
  goal,
  max_depth=2,
  retry_policy=None,
)
```

Phase 108 利用者 workflow:

```text
run_standard_repository_生成元_user_execution_workflow(
  生成元_input,
  candidate_number=None,
  max_depth=2,
  retry_policy=None,
)
```

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

第3 qualified family はまだ追加していない。

---

# 4. 現在の再生 API

既知群再生:

```text
build_standard_repository_生成元_known_group_proof_replay_input(
  生成元_input,
  max_depth=1,
)
```

operation-query replay:

```text
build_repository_operation_query_proof_replay(
  presentation,
  fact_number=None,
  max_depth=1,
)
```

両者は別 semantics。

```text
show-proof
→ 既知群同一性 proof replay

query-proof
→ selected 演算事実の証明再生
```

---

# 5. 現在の CLI

```text
python main.py n k
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
python main.py show-proof nu_prime
python main.py show-proof sigma_11
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"
python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "E(eta_2 o nu_prime)"
```

---

# 6. 確定した利用者向け境界

曖昧性:

```text
複数の実行可能対象
→ 自動選択しない
```

候補番号:

```text
1-based addressing
!= 定理順位付け
```

既知群再生:

```text
show-proof
!= execute
```

演算問い合わせ:

```text
lookup
!= inference
!= evaluator
```

重複除去:

```text
deduplicated presentation
!= 生 provenance の削除
```

query-proof:

```text
選択事実自身の ProofStep
!= 包含する repository 定理 root
```

複数の問い合わせ事実:

```text
--fact omitted
→ 暗黙の自動選択 しない
```

未知の再生 statement:

```text
安全な型名 fallback
!= 推測した branch 説明
```

---

# 7. Phase 111 第一候補：CLI 機能 / 利用者ニーズ監査

Phase 110 までで 計算、探索、適用可能性、既知群再生、qualified execution、演算事実問い合わせ、演算事実の証明再生 が CLI から利用可能になった。

次は 一般 evaluator を先に実装せず、利用者視点で現在の CLI 機能 を監査する。

監査候補:

```text
どの操作が 発見しやすい か
query / query-proof / show-proof / execute の役割分離
演算問い合わせ grammar の実際の不足
証明再生 depth 1 の十分性
別 provenance 選択の必要性
合成問い合わせ の見つけやすさ
CLI help / コマンドの見つけやすさ
既存 full 証明レポート の presentation 残課題
```

実需要が確認された項目だけを次の実装 Phase にする。

---

# 8. 保留：演算問い合わせ grammar expansion

現在の最小 grammar:

```text
H(<operand>)
E(<operand>)
Delta(<operand>)
<生成元> o <生成元>
```

保留:

```text
入れ子合成
3項合成
Unicode ∘
LaTeX 入力
暗黙の合成
一般式 parser
```

grammar 拡張だけを目的に先取りしない。

---

# 9. 保留：演算 evaluator

未実装:

```text
一般合成 evaluator
一般 E evaluator
一般 H evaluator
一般 Delta evaluator
repository に未表現の fact の自動導出
```

Phase 110 の `query` は lookup のまま維持する。

---

# 10. 保留：証明再生拡張

現在の `show-proof` / `query-proof` は default direct-premise depth 1。

必要性が確認された場合のみ検討:

```text
CLI --depth
再帰 ancestry 表示
依存関係優先 narrative
共有依存関係表示
別 provenance selection
高度な証明可視化
```

---

# 11. 保留：意味論的な自動対象選択

複数候補から数学的に「最善」を選ぶ機能は未実装。

```text
定理順位付け
最短証明 ranking
証明コスト最適化
意味論的 goal 優先度
自動対象優先
```

候補順を ranking と解釈しない。

---

# 12. 保留：追加 qualified family

third family 以降は coverage 拡張だけを目的に admission しない。

次を確認する。

```text
actual production source
execution safety
goal compatibility
required seed context
rule identity preservation
producer-search behavior
user-facing need
new architectural pressure
```

---

# 13. 保留：数学的 より広い数学的 coverage

```text
一般 Toda bracket solver
不定性 / coset 正規化
より広い unstable stem
奇素数成分統合
all-primary ordinary sphere-homotopy 計算
```

---

# 14. 保留：最適化 / versioning

```text
一般 backtracking
producer ranking
証明コスト最適化
best-proof 選択
永続 cache
並列化
repository snapshot / versioning
古い search report の検出
```

Phase 106 の prefilter 以降、次の optimization は実測圧力を確認してから行う。

---

# 15. 保留：UI 拡張

現在 CLI で 計算 / 探索 / 適用可能性 / replay / execution / 演算問い合わせ が利用できる。

未実装:

```text
Web UI
対話的候補選択
永続実行履歴
rich recursive proof visualization
```

---

# 16. 次 Phase の開始境界

Phase 110 の operation-query capability を機械的に拡張しない。

次はまず:

```text
Phase 111
CLI 機能 / 利用者ニーズ監査
```

その監査結果から、実際に不足している最小 capability を次の実装範囲にする。
