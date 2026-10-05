Phase157 R5-R10 repair8

repair7 の結果:
- 60 passed
- 4 failed

4 failure は R10 実装の不具合ではなく、
Phase157 より前の historical test contract が現在の Reference selection と
Reference/body boundary に追随していないことが原因。

更新内容:
1. Phase144:
   `(5.2)` の公開 Reference 必須という旧契約を削除。
   Phase157 で実際に残る Reference を確認する。
2. Phase156:
   nu-prime bracket definition は Reference に存在してよい。
   proof body に重複しないことを確認する。
3. Phase153:
   Proposition 5.6 locator 全体を禁止せず、
   root result 自体が Reference に自己参照されないことを確認する。
   同じ Proposition 5.6 の earlier fixed group result は許可する。

Production code changes: none.

全体 pytest は Phase157 closure の最後だけ実行する。
