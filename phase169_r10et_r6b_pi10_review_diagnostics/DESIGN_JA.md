# R10ET-R6B：pi10_8 の判定根拠の抽出

R6 は必須16件がすべて PASS、追加3件のうち pi10_8 が REVIEW_REQUIRED となった。Trust Boundary と「共通 Definition に置換可能な引用付き像が0件」という結果は、Reference の祖先紐付けまたは共通 Definition の適用可能性／実使用数一致を自動的には保証しない。

この診断は R6 が保存した audit.json の `problems` 配列を正確に提示する。さらに pi10_8/proof_steps.json の引用元、GIVEN 紐付け、root 祖先、像の規則と型付き一致状況を表示する。台帳・Proof Tree・Renderer・Git は変更しない。問題を隠して PASS に変えることもない。

R6B の診断正常終了は R6 の完了条件ではない。個別の理由が特定された後で初めて、追加テストや必要最小の修正を検討する。全体 pytest は Phase 終了時のみ。
