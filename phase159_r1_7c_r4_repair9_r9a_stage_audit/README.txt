Phase 159 R1-7c R4 repair9 R9-A stage audit

目的
====
pi_6^3 の必要な relation

  2nu' = eta_3^3

が Phase 159 の current generic contribution pipeline の
どの stage で消えるかを特定する。

Production change
=================
なし。

方法
====
`toda_group_proof_narrative_contribution_renderer` の主要 stage function を
runtime monkeypatch で wrapper 化し、各呼び出しについて

  before=<target relation present?>
  after=<target relation present?>

を出力する。

`before=True after=False` になった最初の stage が
drop candidate。

対象 stage
==========
- connector normalization
- numeric equality normalization
- Reference linking
- reflexive suppression
- surjectivity ordering
- short exact ordering
- repeated Reference suppression
- dangling connector suppression
- visible relation dependency ordering
- repeated unique-step suppression
- map-property dependency insertion
- injective-image order reason ordering
- literal reflexive suppression
- body-usage Reference filtering
- fixed Reference restoration

注意
====
audit-only。
production file を書き換えない。
pytest も実行しない。
