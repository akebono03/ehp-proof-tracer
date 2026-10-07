Phase 159 pi6_3 reason surface audit

目的
====

repair7 の新規 zero-map / concise-reason order tests は 2/2 PASS。

既存 Phase 157 test では kernel reason

  完全性より,
  ker Delta = Im H = pi7^5

の簡潔形が見つからず failure。

この audit は production を変更せず、
contribution renderer と actual public renderer で次の文を
repr のまま表示する。

- ker Delta reason
- Delta zero-map statement
- E injectivity reason / statement

これにより、
- 文が本当に消えたのか
- 「である.」付きの verbose form が残っているだけか
- 順序はどうなっているか

を確定する。

production code:
- 変更なし

test code:
- 変更なし

pytest:
- 実行しない

full suite:
- 実行しない
